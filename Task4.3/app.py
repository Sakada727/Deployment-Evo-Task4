from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import socket
import datetime
import random
import httpx
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

APP_NAME = os.environ.get("APP_NAME", "Deployment Task 4.3")
# --- Quote cache, fetched once at startup to avoid ZenQuotes' rate limit ---
QUOTE_CACHE = []

def load_quotes():
    global QUOTE_CACHE
    try:
        response = httpx.get("https://zenquotes.io/api/quotes", timeout=5)
        response.raise_for_status()
        QUOTE_CACHE = response.json()
    except Exception:
        QUOTE_CACHE = [{"q": "Stay hungry, stay foolish.", "a": "Steve Jobs"}]

load_quotes()  # fetch once when the app starts

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{app_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; background: #111; color: #eee; padding: 40px; }}
        h1 {{ color: #6cf; }}
        img {{ max-width: 400px; border-radius: 8px; margin-top: 20px; }}
        figcaption {{ margin-top: 10px; font-style: italic; color: #aaa; }}
        .meta {{ margin-top: 30px; font-size: 0.85em; color: #666; }}
        a {{ color: #6cf; }}
        nav {{ margin-top: 20px; }}
        nav a {{ margin: 0 10px; }}
        #quote-box {{ margin-top: 30px; padding: 20px; background: #1c1c1c; border-radius: 8px; max-width: 500px; margin-left: auto; margin-right: auto; }}
        #quote-author {{ margin-top: 8px; color: #6cf; font-size: 0.9em; }}
        button {{ margin-top: 15px; padding: 8px 16px; background: #6cf; border: none; border-radius: 5px; cursor: pointer; font-size: 0.9em; }}
        button:hover {{ background: #4ab; }}
    </style>
</head>
<body>
    <h1>{app_name}</h1>
    <figure>
        <img src="/static/bananaleclerc.png" alt="Banana Leclerc">
        <figcaption>Banana Leclerc</figcaption>
    </figure>

    <div id="quote-box">
        <p id="quote-text">Loading a quote...</p>
        <p id="quote-author"></p>
        <button onclick="getQuote()">New Quote</button>
    </div>

    <nav>
        <a href="/">Home</a>
        <a href="/api/info">API (/api/info)</a>
        <a href="/api/quote">Quote API (/api/quote)</a>
        <a href="/docs">Interactive API docs (/docs)</a>
        <a href="/health">Health check</a>
    </nav>
    <p class="meta">Served from: {hostname} &mdash; {timestamp}</p>

    <script>
        async function getQuote() {{
            const res = await fetch('/api/quote');
            const data = await res.json();
            document.getElementById('quote-text').textContent = data.quote;
            document.getElementById('quote-author').textContent = '— ' + data.author;
        }}
        getQuote();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE_TEMPLATE.format(
        app_name=APP_NAME,
        hostname=socket.gethostname(),
        timestamp=datetime.datetime.utcnow().isoformat() + "Z"
    )

@app.get("/api/info")
def api_info():
    return {
        "app_name": APP_NAME,
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "ok"
    }

@app.get("/api/quote")
def api_quote():
    if not QUOTE_CACHE:
        load_quotes()
    entry = random.choice(QUOTE_CACHE)
    return {"quote": entry["q"], "author": entry["a"]}

@app.get("/health")
def health():
    return {"status": "ok"}