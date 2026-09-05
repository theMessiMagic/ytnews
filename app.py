from flask import Flask, render_template, abort
import os
import json

# --------------------------------------------------------------
import psycopg2
import psycopg2.extras
import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, session, redirect, url_for
#-----------------------------------------------------------------

app = Flask(__name__)

#-------------------------------------------------
app.secret_key = os.environ.get("SECRET_KEY")

DATABASE_URL = os.environ.get("DATABASE_URL")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
#---------------------------------------------------

ARTICLES_DIR = "articles"
CHANNEL_NAME = "NeonMan"
CHANNEL_URL = "https://www.youtube.com/@NeonMan"

#---------------------------------------------------
# =========================
# ANALYTICS DATABASE
# =========================

def get_db():
    return psycopg2.connect(DATABASE_URL)


def init_analytics_db():

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            id SERIAL PRIMARY KEY,
            visitor_id TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            user_agent TEXT,
            referrer TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id TEXT PRIMARY KEY,
            first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_page_views_created_at
        ON page_views(created_at)
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_page_views_path
        ON page_views(path)
    """)

    db.commit()

    cur.close()
    db.close()


init_analytics_db()
#---------------------------------------------------

#----------------------------------------------------------------------
# =========================
# VISITOR TRACKING
# =========================

def get_visitor_id():

    visitor_id = request.cookies.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    return visitor_id


def track_visit():

    visitor_id = get_visitor_id()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO page_views
        (visitor_id, path, user_agent, referrer)
        VALUES (%s, %s, %s, %s)
    """, (
        visitor_id,
        request.path,
        request.headers.get("User-Agent", "")[:500],
        request.referrer or ""
    ))

    cur.execute("""
        INSERT INTO visitors
        (visitor_id)
        VALUES (%s)
        ON CONFLICT (visitor_id)
        DO UPDATE SET last_seen = NOW()
    """, (visitor_id,))

    db.commit()

    cur.close()
    db.close()

    return visitor_id
#----------------------------------------------------------------------

def load_articles():

    articles = []

    if not os.path.exists(ARTICLES_DIR):
        return []

    for file in os.listdir(ARTICLES_DIR):

        if file.endswith(".json"):

            path = os.path.join(
                ARTICLES_DIR,
                file
            )

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                article = json.load(f)

                article["id"] = file.replace(
                    ".json",
                    ""
                )

                articles.append(article)

    articles.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    return articles


@app.route("/")
def home():

    articles = load_articles()

    return render_template(
        "index.html",
        articles=articles,
        channel_name=CHANNEL_NAME,
        channel_url=CHANNEL_URL
    )


@app.route("/article/<article_id>")
def article(article_id):

    file_path = os.path.join(
        ARTICLES_DIR,
        f"{article_id}.json"
    )

    if not os.path.exists(file_path):
        abort(404)

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        article = json.load(f)

    return render_template(
        "article.html",
        article=article,
        channel_name=CHANNEL_NAME,
        channel_url=CHANNEL_URL
    )

#-----------------------------------------------------------
# =========================
# AUTOMATIC PAGE TRACKING
# =========================

@app.after_request
def analytics_after_request(response):

    if (
        request.method == "GET"
        and response.status_code == 200
        and request.path != "/favicon.ico"
        and not request.path.startswith("/admin")
        and not request.path.startswith("/api")
        and response.content_type
        and "text/html" in response.content_type
    ):

        try:

            visitor_id = track_visit()

            response.set_cookie(
                "visitor_id",
                visitor_id,
                max_age=60 * 60 * 24 * 365,
                httponly=True,
                samesite="Lax",
                secure=True
            )

        except Exception as e:

            print("Analytics error:", e)

    return response
#-----------------------------------------------------------

#-----------------------------------------------------------
@app.route("/api/analytics/heartbeat", methods=["POST"])
def analytics_heartbeat():

    visitor_id = get_visitor_id()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO visitors
        (visitor_id)
        VALUES (%s)
        ON CONFLICT (visitor_id)
        DO UPDATE SET last_seen = NOW()
    """, (visitor_id,))

    db.commit()

    cur.close()
    db.close()

    response = jsonify({
        "success": True
    })

    response.set_cookie(
        "visitor_id",
        visitor_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax",
        secure=True
    )

    return response
#-----------------------------------------------------------

# ----------------------------------------------------------
# =========================
# ADMIN AUTHENTICATION
# =========================

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return func(*args, **kwargs)

    return wrapper


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template(
        "admin_login.html"
    )


@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


@app.route("/admin/analytics")
@admin_required
def admin_dashboard():

    return render_template(
        "analytics.html"
    )
# ----------------------------------------------------------

# --------------------------------------------------------------------
@app.route("/admin/api/analytics")
@admin_required
def analytics_api():

    days = request.args.get("days", "7")

    try:
        days = int(days)
    except ValueError:
        days = 7

    if days not in [1, 7, 30, 90, 365]:
        days = 7

    db = get_db()
    cur = db.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    # Total views
    cur.execute("""
        SELECT COUNT(*) AS count
        FROM page_views
        WHERE created_at >= NOW() - (%s * INTERVAL '1 day')
    """, (days,))

    total_views = cur.fetchone()["count"]

    # Unique visitors
    cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) AS count
        FROM page_views
        WHERE created_at >= NOW() - (%s * INTERVAL '1 day')
    """, (days,))

    unique_visitors = cur.fetchone()["count"]

    # Active visitors
    cur.execute("""
        SELECT COUNT(*) AS count
        FROM visitors
        WHERE last_seen >= NOW() - INTERVAL '60 seconds'
    """)

    active_visitors = cur.fetchone()["count"]

    # Today views
    cur.execute("""
        SELECT COUNT(*) AS count
        FROM page_views
        WHERE created_at >= CURRENT_DATE
    """)

    today_views = cur.fetchone()["count"]

    # Today visitors
    cur.execute("""
        SELECT COUNT(DISTINCT visitor_id) AS count
        FROM page_views
        WHERE created_at >= CURRENT_DATE
    """)

    today_visitors = cur.fetchone()["count"]

    # Daily traffic
    cur.execute("""
        SELECT
            DATE(created_at) AS date,
            COUNT(*) AS views,
            COUNT(DISTINCT visitor_id) AS visitors
        FROM page_views
        WHERE created_at >= NOW() - (%s * INTERVAL '1 day')
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (days,))

    daily = cur.fetchall()

    # Top pages
    cur.execute("""
        SELECT
            path,
            COUNT(*) AS views,
            COUNT(DISTINCT visitor_id) AS visitors
        FROM page_views
        WHERE created_at >= NOW() - (%s * INTERVAL '1 day')
        GROUP BY path
        ORDER BY views DESC
        LIMIT 10
    """, (days,))

    top_pages = cur.fetchall()

    # Referrers
    cur.execute("""
        SELECT
            referrer,
            COUNT(*) AS views
        FROM page_views
        WHERE created_at >= NOW() - (%s * INTERVAL '1 day')
          AND referrer != ''
        GROUP BY referrer
        ORDER BY views DESC
        LIMIT 10
    """, (days,))

    referrers = cur.fetchall()

    # Live visitors
    cur.execute("""
        SELECT
            visitor_id,
            last_seen
        FROM visitors
        WHERE last_seen >= NOW() - INTERVAL '60 seconds'
        ORDER BY last_seen DESC
        LIMIT 50
    """)

    live_visitors = cur.fetchall()

    cur.close()
    db.close()

    return jsonify({
        "total_views": total_views,
        "unique_visitors": unique_visitors,
        "active_visitors": active_visitors,
        "today_views": today_views,
        "today_visitors": today_visitors,
        "daily": [
            {
                "date": str(x["date"]),
                "views": x["views"],
                "visitors": x["visitors"]
            }
            for x in daily
        ],
        "top_pages": [
            {
                "path": x["path"],
                "views": x["views"],
                "visitors": x["visitors"]
            }
            for x in top_pages
        ],
        "referrers": [
            {
                "referrer": x["referrer"],
                "views": x["views"]
            }
            for x in referrers
        ],
        "live_visitors": [
            {
                "visitor": x["visitor_id"][:8],
                "last_seen": x["last_seen"].isoformat()
            }
            for x in live_visitors
        ]
    })
# --------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
