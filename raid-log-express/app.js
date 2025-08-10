const express = require('express');
const path = require('path');

const app = express();
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const CATEGORIES = ['Risk', 'Assumption', 'Issue', 'Dependency'];
const entries = [];
let nextId = 1;

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

app.get('/', (req, res) => {
  const grouped = {};
  for (const c of CATEGORIES) {
    grouped[c] = entries.filter((e) => e.category === c);
  }
  res.render('index', { categories: CATEGORIES, grouped });
});

app.post('/add', (req, res) => {
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

app.get('/export', (req, res) => {
  const csv = toCsv(entries);
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename=raid_log.csv');
  res.send(csv);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`RAID log app listening on http://localhost:${PORT}`);
});