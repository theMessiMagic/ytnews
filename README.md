# 🚀 AI News Portal

An automated AI-powered news website that transforms YouTube videos into professional news articles.

🌐 Live Website: https://ai-daily-news-geck.onrender.com/

The system continuously monitors YouTube channels, extracts transcripts, uses Google's Gemini AI to generate high-quality news articles, and automatically publishes them to a live website.

---

## ✨ Features

* 🎥 Monitors YouTube channels automatically
* 📝 Extracts video transcripts using Apify
* 🤖 Generates SEO-friendly news articles with Gemini AI
* 🖼️ Fetches video thumbnails automatically
* 📚 Stores articles as structured JSON files
* 🌐 Displays articles on a Flask-powered website
* ⚡ Fully automated using GitHub Actions
* 🔄 Auto-deploys on Render
* 📱 Responsive modern UI with Tailwind CSS

---

## 🏗️ Architecture

```text
YouTube Upload
      ↓
YouTube API
      ↓
Transcript Extraction (Apify)
      ↓
Gemini AI Article Generation
      ↓
JSON Article Storage
      ↓
GitHub Actions
      ↓
GitHub Repository
      ↓
Render Deployment
      ↓
Live News Website
```

---

## 📂 Project Structure

```text
ytnews/
│
├── app.py
├── watcher.py
├── requirements.txt
├── state.json
│
├── articles/
│   └── *.json
│
├── templates/
│   ├── index.html
│   └── article.html
│
└── .github/
    └── workflows/
        └── watcher.yml
```

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Gunicorn

### AI

* Google Gemini 2.5 Flash
* LangChain Google GenAI

### Data Sources

* YouTube Data API v3
* Apify YouTube Transcript Scraper

### Automation

* GitHub Actions

### Deployment

* Render

### Frontend

* HTML
* Tailwind CSS

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
YOUTUBE_API_KEY=your_youtube_api_key
APIFY_TOKEN=your_apify_token
```

---

## 🚀 Local Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ytnews.git
cd ytnews
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run website:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔄 Running the News Generator

Generate articles manually:

```bash
python watcher.py
```

The script will:

1. Check latest YouTube upload
2. Extract transcript
3. Generate article using Gemini
4. Save article JSON
5. Update website automatically

---

## 🤖 Automated Workflow

GitHub Actions runs automatically on schedule.

```text
Every Hour
      ↓
Check YouTube Channel
      ↓
Generate New Article
      ↓
Commit Changes
      ↓
Push To GitHub
      ↓
Render Auto Deploy
```

No PC required.

---

## 📸 Screenshots

Add screenshots of:

* Homepage
* Article page
* GitHub Actions workflow
* Render deployment dashboard

---

## 🎯 Future Improvements

* Multiple YouTube channels
* Search functionality
* Categories and tags
* User accounts
* Dark mode
* Newsletter support
* AI article summaries
* Trending news section
* RSS feeds

---

## ⚠️ Disclaimer

This project generates articles using AI based on publicly available YouTube video transcripts. Generated content should be reviewed before use in professional publishing environments.

---

## 📜 License

MIT License

---

## ⭐ Support

If you found this project useful:

* Star the repository ⭐
* Fork the project 🍴
* Share it with others 🚀

Built with ❤️ using Python, Gemini AI, GitHub Actions, and Render.
