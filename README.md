# RAID Log Apps (Flask and Express)

Minimal RAID log web apps in Python (Flask) and Node.js (Express) with CSV export.

## Features

- Add entries across RAID categories: Risk, Assumption, Issue, Dependency
- List entries by category
- Export all RAID entries to CSV
- UAT checklist: add items, view list, export to CSV
- Login with simple session (default admin/admin)
- In-memory storage (ephemeral). Swap in a database for persistence.

## Option A: Python Flask

### Setup

```bash
python3 -m venv /workspace/raid-log-flask/.venv
source /workspace/raid-log-flask/.venv/bin/activate
pip install --upgrade pip
pip install -r /workspace/raid-log-flask/requirements.txt
```

### Run

```bash
FLASK_SECRET=change-me FLASK_ADMIN_USER=admin FLASK_ADMIN_PASSWORD=admin \
python /workspace/raid-log-flask/app.py
```

Visit `http://localhost:5000`.

- RAID CSV export: `/export`
- UAT checklist CSV export: `/uat/export`
- Login at `/login` (default `admin`/`admin`)

## Option B: Node.js Express

Requires Node.js 18+.

### Setup

```bash
cd /workspace/raid-log-express
npm install
```

### Run

```bash
SESSION_SECRET=change-me ADMIN_USER=admin ADMIN_PASSWORD=admin \
npm start
```

Visit `http://localhost:5000`.

If you want to run Flask and Express at the same time, run Express on another port (e.g. 5001):

```bash
PORT=5001 SESSION_SECRET=change-me ADMIN_USER=admin ADMIN_PASSWORD=admin \
npm start
```

Visit `http://localhost:5001`.

- RAID CSV export: `/export`
- UAT checklist CSV export: `/uat/export`
- Login at `/login` (default `admin`/`admin`)

## Notes

- Data is stored in memory and will reset on restart.
- For anything beyond demos, replace in-memory storage and simple auth with proper persistence and auth (e.g. OAuth).