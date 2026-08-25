from __future__ import annotations

from fastapi.responses import HTMLResponse


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SecureFlow Quality Lab</title>
  <style>
    :root { color-scheme: light dark; font-family: Inter, system-ui, sans-serif; }
    body { max-width: 1050px; margin: 0 auto; padding: 2rem; line-height: 1.5; }
    header { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
    main { display: grid; gap: 1.25rem; }
    section { border: 1px solid #8887; border-radius: 12px; padding: 1.2rem; }
    form { display: grid; gap: .75rem; max-width: 620px; }
    label { display: grid; gap: .25rem; font-weight: 600; }
    input, textarea, select, button { font: inherit; padding: .65rem; border-radius: 8px; border: 1px solid #8889; }
    button { cursor: pointer; font-weight: 700; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: .6rem; border-bottom: 1px solid #8885; vertical-align: top; }
    .muted { opacity: .72; }
    .error { color: #d33; font-weight: 700; }
    .success { color: #178b3b; font-weight: 700; }
    .hidden { display: none; }
    .actions { display: flex; gap: .5rem; flex-wrap: wrap; }
    code { background: #7772; border-radius: 4px; padding: .1rem .3rem; }
  </style>
</head>
<body>
<header>
  <div>
    <h1>SecureFlow Quality Lab</h1>
    <p class="muted">Synthetic workflow for UI, API, data, access-control, audit, and CI validation.</p>
  </div>
  <button id="logout" class="hidden" type="button">Log out</button>
</header>
<main>
  <section id="login-panel">
    <h2>Demo login</h2>
    <form id="login-form">
      <label>Email
        <input id="email" name="email" type="email" value="analyst.one@example.test" required>
      </label>
      <label>Password
        <input id="password" name="password" type="password" value="AnalystPass!1" required>
      </label>
      <button type="submit">Sign in</button>
    </form>
    <p class="muted">Other roles: <code>viewer@example.test</code> / <code>ViewerPass!1</code>, <code>approver@example.test</code> / <code>ApproverPass!1</code>.</p>
  </section>

  <section id="workspace" class="hidden">
    <h2>Workspace</h2>
    <p id="identity"></p>
    <p id="message" aria-live="polite"></p>

    <form id="record-form">
      <h3>Create a risk record</h3>
      <label>Title
        <input id="title" name="title" minlength="3" maxlength="120" required>
      </label>
      <label>Description
        <textarea id="description" name="description" minlength="3" maxlength="1000" required></textarea>
      </label>
      <label>Risk score (0–100)
        <input id="risk-score" name="risk_score" type="number" min="0" max="100" value="72" required>
      </label>
      <button type="submit">Create record</button>
    </form>

    <h3>Visible records</h3>
    <table>
      <thead><tr><th>ID</th><th>Title</th><th>Risk</th><th>Status</th><th>Owner</th><th>Actions</th></tr></thead>
      <tbody id="records"></tbody>
    </table>
  </section>
</main>
<script>
  let csrfToken = null;
  let currentUser = null;
  const $ = (selector) => document.querySelector(selector);

  function showMessage(text, kind = '') {
    const el = $('#message');
    el.textContent = text;
    el.className = kind;
  }

  async function api(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
    if (csrfToken && options.method && !['GET', 'HEAD'].includes(options.method)) {
      headers.set('X-CSRF-Token', csrfToken);
    }
    const response = await fetch(path, { ...options, headers });
    const data = response.status === 204 ? null : await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`);
    return data;
  }

  async function loadRecords() {
    const records = await api('/api/records');
    const tbody = $('#records');
    tbody.innerHTML = '';
    for (const record of records) {
      const row = document.createElement('tr');
      row.dataset.recordId = record.id;
      const actions = [];
      if (record.status === 'DRAFT' && (record.owner_id === currentUser.id || currentUser.role === 'approver')) {
        actions.push(`<button type="button" data-action="submit" data-id="${record.id}">Submit</button>`);
      }
      if (record.status === 'SUBMITTED' && currentUser.role === 'approver') {
        actions.push(`<button type="button" data-action="approve" data-id="${record.id}">Approve</button>`);
      }
      row.innerHTML = `<td>${record.id}</td><td>${escapeHtml(record.title)}</td><td>${record.risk_score} / ${record.risk_class}</td><td>${record.status}</td><td>${record.owner_id}</td><td class="actions">${actions.join('')}</td>`;
      tbody.appendChild(row);
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  $('#login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      const data = await api('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: $('#email').value, password: $('#password').value })
      });
      csrfToken = data.csrf_token;
      currentUser = data.user;
      $('#identity').textContent = `${currentUser.display_name} — ${currentUser.role}`;
      $('#login-panel').classList.add('hidden');
      $('#workspace').classList.remove('hidden');
      $('#logout').classList.remove('hidden');
      $('#record-form').classList.toggle('hidden', currentUser.role === 'viewer');
      showMessage('Authenticated.', 'success');
      await loadRecords();
    } catch (error) {
      const message = document.querySelector('#login-panel .error') || document.createElement('p');
      message.className = 'error';
      message.textContent = error.message;
      $('#login-panel').appendChild(message);
    }
  });

  $('#record-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      const record = await api('/api/records', {
        method: 'POST',
        body: JSON.stringify({
          title: $('#title').value,
          description: $('#description').value,
          risk_score: Number($('#risk-score').value)
        })
      });
      showMessage(`Created record ${record.id} with ${record.risk_class} risk.`, 'success');
      event.target.reset();
      $('#risk-score').value = '72';
      await loadRecords();
    } catch (error) { showMessage(error.message, 'error'); }
  });

  $('#records').addEventListener('click', async (event) => {
    const button = event.target.closest('button[data-action]');
    if (!button) return;
    try {
      const result = await api(`/api/records/${button.dataset.id}/${button.dataset.action}`, { method: 'POST' });
      showMessage(`Record ${result.id} is now ${result.status}.`, 'success');
      await loadRecords();
    } catch (error) { showMessage(error.message, 'error'); }
  });

  $('#logout').addEventListener('click', async () => {
    try { await api('/api/auth/logout', { method: 'POST' }); } catch (_) {}
    csrfToken = null;
    currentUser = null;
    $('#workspace').classList.add('hidden');
    $('#logout').classList.add('hidden');
    $('#login-panel').classList.remove('hidden');
  });
</script>
</body>
</html>"""


def render_ui() -> HTMLResponse:
    return HTMLResponse(HTML)
