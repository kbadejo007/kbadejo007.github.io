# RAID Log Apps (Flask and Express)

Minimal RAID log web apps in Python (Flask) and Node.js (Express) with CSV export.

## Features

- Add entries across RAID categories: Risk, Assumption, Issue, Dependency
- List entries by category
- Export all entries to CSV
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
python /workspace/raid-log-flask/app.py
```

Visit `http://localhost:5000`.

## Option B: Node.js Express

Requires Node.js 18+.

### Setup

```bash
cd /workspace/raid-log-express
npm install
```

### Run

```bash
npm start
```

Visit `http://localhost:5000`.

If you want to run Flask and Express at the same time, run Express on another port (e.g. 5001):

```bash
PORT=5001 npm start
```

Visit `http://localhost:5001`.

## Notes

- CSV export is available at `/export`.
- Data is stored in memory and will reset on restart.
- To persist data, replace the in-memory array with a database or file-backed store.