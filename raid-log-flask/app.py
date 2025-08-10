from flask import Flask, render_template, request, redirect, url_for, Response
import csv
import io
from datetime import datetime
from typing import List, Dict

app = Flask(__name__)

# In-memory storage for simplicity. Replace with a database for persistence.
entries: List[Dict[str, str]] = []
next_id: int = 1

CATEGORIES = ["Risk", "Assumption", "Issue", "Dependency"]


def generate_csv(entries_list: List[Dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "category",
            "title",
            "description",
            "owner",
            "status",
            "due_date",
            "created_at",
        ],
    )
    writer.writeheader()
    for row in entries_list:
        writer.writerow(row)
    return output.getvalue()


@app.route("/", methods=["GET"])
def index():
    grouped = {cat: [e for e in entries if e["category"] == cat] for cat in CATEGORIES}
    return render_template("index.html", categories=CATEGORIES, grouped=grouped)


@app.route("/add", methods=["POST"])
def add():
    global next_id
    category = request.form.get("category", "").strip()
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    owner = request.form.get("owner", "").strip()
    status = request.form.get("status", "").strip()
    due_date = request.form.get("due_date", "").strip()

    if category not in CATEGORIES or not title:
        return redirect(url_for("index"))

    entry = {
        "id": str(next_id),
        "category": category,
        "title": title,
        "description": description,
        "owner": owner,
        "status": status,
        "due_date": due_date,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    entries.append(entry)
    next_id += 1
    return redirect(url_for("index"))


@app.route("/export", methods=["GET"])
def export_csv():
    csv_data = generate_csv(entries)
    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=raid_log.csv"},
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)