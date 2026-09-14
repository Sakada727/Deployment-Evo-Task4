from flask import Flask, render_template_string
import socket
import datetime

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Deployment Task 4.2</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #111; color: #eee; padding: 40px; }
        img { max-width: 400px; border-radius: 8px; margin-top: 20px; }
        figcaption { margin-top: 10px; font-style: italic; color: #aaa; }
        .meta { margin-top: 30px; font-size: 0.85em; color: #666; }
    </style>
</head>
<body>
    <h1>Deployment Task 4.2</h1>
    <figure>
        <img src="/static/bananaleclerc.png" alt="Banana Leclerc">
        <figcaption>Banana Leclerc</figcaption>
    </figure>
    <p class="meta">Served from container: {{ hostname }} &mdash; {{ timestamp }}</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        PAGE,
        hostname=socket.gethostname(),
        timestamp=datetime.datetime.utcnow().isoformat() + "Z"
    )

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)