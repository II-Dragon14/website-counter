from flask import Flask, jsonify
from flask_cors import CORS
import requests, os, base64, json

app = Flask(__name__)
CORS(app)

GITHUB_TOKEN = os.environ.get("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")
REPO = "II-Dragon14/website-counter"
FILE_PATH = "counter.json"
API_URL = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def load_count():
    r = requests.get(API_URL, headers=HEADERS)
    if r.status_code == 404:
        return 0, None
    data = r.json()
    content = json.loads(base64.b64decode(data["content"]).decode())
    return content.get("count", 0), data["sha"]

def save_count(count, sha):
    content = base64.b64encode(json.dumps({"count": count}).encode()).decode()
    payload = {
        "message": f"visit #{count}",
        "content": content,
    }
    if sha:
        payload["sha"] = sha
    requests.put(API_URL, headers=HEADERS, json=payload)

@app.route("/api/visit")
def visit():
    count, sha = load_count()
    count += 1
    save_count(count, sha)
    return jsonify({"visits": count})

@app.route("/")
def home():
    return "Visitor counter API running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
