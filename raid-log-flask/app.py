from flask import Flask, render_template, request, redirect, url_for, Response, session
import csv
import io
import os
from datetime import datetime
from typing import List, Dict
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

# In-memory storage for simplicity. Replace with a database for persistence.
entries: List[Dict[str, str]] = []
next_id: int = 1

CATEGORIES = ["Risk", "Assumption", "Issue", "Dependency"]

# UAT checklist in-memory storage
uat_items: List[Dict[str, str]] = []
next_uat_id: int = 1
UAT_STATUSES = ["Not Started", "In Progress", "Passed", "Failed", "Blocked"]

# Simple credentials (override via env)
ADMIN_USER = os.environ.get("FLASK_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("FLASK_ADMIN_PASSWORD", "admin")


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            next_url = request.path
            return redirect(url_for("login", next=next_url))
        return view_func(*args, **kwargs)
    return wrapper


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


def generate_uat_csv(items_list: List[Dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "title",
            "owner",
            "status",
            "due_date",
            "notes",
            "created_at",
        ],
    )
    writer.writeheader()
    for row in items_list:
        writer.writerow(row)
    return output.getvalue()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["user"] = username
            next_url = request.args.get("next") or url_for("index")
            return redirect(next_url)
    return render_template("login.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
@login_required
def index():
    grouped = {cat: [e for e in entries if e["category"] == cat] for cat in CATEGORIES}
    return render_template(
        "index.html",
        categories=CATEGORIES,
        grouped=grouped,
        uat_items=uat_items,
        uat_statuses=UAT_STATUSES,
        current_user=session.get("user"),
    )


@app.route("/add", methods=["POST"])
@login_required
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
@login_required
def export_csv():
    csv_data = generate_csv(entries)
    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=raid_log.csv"},
    )


@app.route("/uat/add", methods=["POST"])
@login_required
def uat_add():
    global next_uat_id
    title = request.form.get("title", "").strip()
    owner = request.form.get("owner", "").strip()
    status = request.form.get("status", "Not Started").strip()
    due_date = request.form.get("due_date", "").strip()
    notes = request.form.get("notes", "").strip()

    if not title:
        return redirect(url_for("index"))

    item = {
        "id": str(next_uat_id),
        "title": title,
        "owner": owner,
        "status": status if status in UAT_STATUSES else "Not Started",
        "due_date": due_date,
        "notes": notes,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    uat_items.append(item)
    next_uat_id += 1
    return redirect(url_for("index"))


@app.route("/uat/export", methods=["GET"])
@login_required
def uat_export_csv():
    csv_data = generate_uat_csv(uat_items)
    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=uat_checklist.csv"},
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)