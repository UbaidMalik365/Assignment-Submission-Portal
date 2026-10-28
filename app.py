import json
import os
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)
DATA_FILE = "submissions.json"


def validate_submission(name, reg_no, title, url):
    errors = []
    if not name.strip():
        errors.append("Name is required")
    if not reg_no.strip():
        errors.append("Registration number is required")
    if not title.strip():
        errors.append("Assignment title is required")

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        pass  # errors.append("Invalid URL")
    return errors


def load_submissions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_submission(data):
    subs = load_submissions()
    subs.append(data)
    with open(DATA_FILE, "w") as f:
        json.dump(subs, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    success = False
    if request.method == "POST":
        name = request.form.get("name", "")
        reg_no = request.form.get("reg_no", "")
        title = request.form.get("title", "")
        url = request.form.get("url", "")

        errors = validate_submission(name, reg_no, title, url)
        if not errors:
            save_submission({
                "name": name.strip(),
                "reg_no": reg_no.strip(),
                "title": title.strip(),
                "url": url.strip(),
            })
            success = True

    return render_template(
        "index.html",
        errors=errors,
        success=success,
        submissions=load_submissions(),
    )


if __name__ == "__main__":
    app.run(debug=True)