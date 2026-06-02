# AI News Portal

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=000000)](https://render.com/)
[![GitHub Actions](https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)

An automated AI news website that turns YouTube uploads into readable news articles and publishes them to a live Flask site.

## Live Website

[https://ai-daily-news-geck.onrender.com/](https://ai-daily-news-geck.onrender.com/)

## Overview

This project monitors a YouTube channel, extracts the latest transcript, generates a structured article with Gemini, stores it as JSON, and serves it through a web interface.

## Features

- Automatic YouTube video monitoring
- Transcript extraction with Apify
- AI-generated article writing with Gemini
- Structured JSON article storage
- Flask-powered frontend
- Automated updates with GitHub Actions
- Deployment on Render

## Workflow

```text
YouTube Upload
    ->
YouTube API Check
    ->
Transcript Extraction
    ->
Gemini Article Generation
    ->
JSON Article Save
    ->
GitHub Actions
    ->
Render Deployment
    ->
Live Website
```

## Tech Stack

- Python
- Flask
- Google Gemini 2.5 Flash
- LangChain Google GenAI
- YouTube Data API v3
- Apify
- GitHub Actions
- Render
- HTML
- Tailwind CSS

## Project Structure

```text
ytnews/
├── app.py
├── watcher.py
├── requirements.txt
├── state.json
├── articles/
│   └── *.json
├── templates/
│   ├── index.html
│   └── article.html
└── .github/
    └── workflows/
        └── watcher.yml
```

## Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
YOUTUBE_API_KEY=your_youtube_api_key
APIFY_TOKEN=your_apify_token
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/theMessiMagic/ytnews.git
cd ytnews
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the website:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Generate Articles Manually

```bash
python watcher.py
```

## Deployment

The site is deployed on Render and updated automatically through GitHub Actions.

Live URL:
[https://ai-daily-news-geck.onrender.com/](https://ai-daily-news-geck.onrender.com/)

## Notes

This project generates articles from publicly available YouTube transcripts. Content should be reviewed before professional or commercial publishing.

## License

MIT License
