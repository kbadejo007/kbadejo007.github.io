const express = require('express');
const path = require('path');
const session = require('express-session');

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({
  secret: process.env.SESSION_SECRET || 'dev-secret',
  resave: false,
  saveUninitialized: false,
}));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const CATEGORIES = ['Risk', 'Assumption', 'Issue', 'Dependency'];
const entries = [];
let nextId = 1;

// UAT checklist in-memory storage
const uatItems = [];
let nextUatId = 1;
const UAT_STATUSES = ['Not Started', 'In Progress', 'Passed', 'Failed', 'Blocked'];

const ADMIN_USER = process.env.ADMIN_USER || 'admin';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin';

function requireAuth(req, res, next) {
  if (req.session && req.session.user) return next();
  const nextParam = encodeURIComponent(req.originalUrl || '/');
  return res.redirect(`/login?next=${nextParam}`);
}

function toCsv(rows) {
  const headers = ['id', 'category', 'title', 'description', 'owner', 'status', 'due_date', 'created_at'];
  const escape = (v) => {
    if (v == null) return '';
    const s = String(v);
    if (/[",\n]/.test(s)) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  };
  const lines = [headers.join(',')];
  for (const row of rows) {
    lines.push(headers.map((h) => escape(row[h])).join(','));
  }
  return lines.join('\n');
}

function toUatCsv(rows) {
  const headers = ['id', 'title', 'owner', 'status', 'due_date', 'notes', 'created_at'];
  const escape = (v) => {
    if (v == null) return '';
    const s = String(v);
    if (/[",\n]/.test(s)) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  };
  const lines = [headers.join(',')];
  for (const row of rows) {
    lines.push(headers.map((h) => escape(row[h])).join(','));
  }
  return lines.join('\n');
}

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  if (username === ADMIN_USER && password === ADMIN_PASSWORD) {
    req.session.user = username;
    const nextUrl = req.query.next || '/';
    return res.redirect(nextUrl);
  }
  return res.render('login');
});

app.post('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login');
  });
});

app.get('/', requireAuth, (req, res) => {
  const grouped = {};
  for (const c of CATEGORIES) {
    grouped[c] = entries.filter((e) => e.category === c);
  }
  res.render('index', { categories: CATEGORIES, grouped, uatItems, uatStatuses: UAT_STATUSES, currentUser: req.session.user });
});

app.post('/add', requireAuth, (req, res) => {
  const { category, title, description, owner, status, due_date } = req.body;
  if (!CATEGORIES.includes(category) || !title) return res.redirect('/');
  entries.push({
    id: String(nextId++),
    category,
    title,
    description,
    owner,
    status,
    due_date,
    created_at: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  });
  res.redirect('/');
});

app.get('/export', requireAuth, (req, res) => {
  const csv = toCsv(entries);
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename=raid_log.csv');
  res.send(csv);
});

app.post('/uat/add', requireAuth, (req, res) => {
  const { title, owner, status, due_date, notes } = req.body;
  if (!title) return res.redirect('/');
  uatItems.push({
    id: String(nextUatId++),
    title,
    owner,
    status: UAT_STATUSES.includes(status) ? status : 'Not Started',
    due_date,
    notes,
    created_at: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  });
  res.redirect('/');
});

app.get('/uat/export', requireAuth, (req, res) => {
  const csv = toUatCsv(uatItems);
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename=uat_checklist.csv');
  res.send(csv);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`RAID log app listening on http://localhost:${PORT}`);
});