# Start Here: Your First Guided SecureFlow Session

This guide is intentionally slower than asking AI to build everything. The objective is to create **understanding and evidence**, not merely a functioning repository.

## Session objective

By the end of this session, you should be able to explain one complete path:

```text
Login → authenticated session → create record → classify risk → save to database → return API response → verify persisted state
```

Expected time: 60–90 minutes.

---

## Step 1 — Confirm your tools

Open PowerShell in the project folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\check_environment.ps1
```

What this does:

- Checks whether Windows can find Python.
- Checks whether Git is installed.
- Confirms that you are in the project root.
- Does **not** install or change anything.

Write in `LEARNING_LOG.md`:

- Which Python version was found?
- Is Git available?
- What folder are you working in?

---

## Step 2 — Create an isolated Python environment

```powershell
.\scripts\setup_windows.ps1
```

What this does:

1. Creates `.venv`, an isolated Python environment for this project.
2. Installs SecureFlow and its development dependencies.
3. Downloads Playwright Chromium for browser tests.

Why isolation matters:

- The project gets its own dependency versions.
- Package changes do not contaminate your global Python installation.
- CI can reproduce the same installation process.

Verify the installation:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pytest --version
.\.venv\Scripts\python.exe -m playwright --version
```

---

## Step 3 — Start the application

In **Terminal 1**:

```powershell
.\scripts\run_windows.ps1
```

What happens:

- `SECUREFLOW_DB_PATH` points the app at a local SQLite file.
- `SECUREFLOW_SECRET` signs local session cookies.
- Uvicorn starts the FastAPI application on `127.0.0.1:8000`.
- `--reload` restarts the server when Python files change.

Open:

```text
http://127.0.0.1:8000
```

Manual exploration:

1. Sign in as the analyst.
2. Create a record with risk score `72`.
3. Verify that it is classified `HIGH`.
4. Submit it.
5. Sign out.

Do not treat this as proof. Manual exploration gives context; automated tests produce repeatable evidence.

---

## Step 4 — Run the fast evidence layers

In **Terminal 2**:

```powershell
.\scripts\run_fast_tests.ps1
```

This excludes the browser test and runs:

- Unit tests
- API workflow tests
- Database cross-layer verification
- Security-requirement regression tests
- Coverage reporting

Read the result instead of only looking for green:

- How many tests ran?
- Which source lines were not covered?
- Was any test skipped?

---

## Step 5 — Trace one test end to end

Run only the database-integrity test:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_data_integrity.py -vv -s
```

Read these files in order:

1. `tests/api/test_data_integrity.py`
2. `tests/conftest.py`
3. `src/secureflow/app.py` — find `add_record`
4. `src/secureflow/auth.py` — find `get_authenticated_user`
5. `src/secureflow/repository.py` — find `create_record` and `classify_risk`
6. `src/secureflow/db.py`

Explain the path in your own words:

> The fixture logs in and captures a CSRF token. The test sends a POST request. The route authenticates the session and checks the role. The repository classifies the risk and inserts the record. The API serializes the row. The test then queries SQLite independently and compares persisted values with the API result.

Do not copy that sentence into your log until you can say why each step exists.

---

## Step 6 — Break the rule on purpose

Open:

```text
src/secureflow/repository.py
```

Temporarily change:

```python
if score < 70:
```

to:

```python
if score < 75:
```

Now run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_api_workflow.py::test_risk_boundary_classification -vv
```

Expected result: the test should fail at the `70` boundary.

Why this matters:

- You saw the test detect a real requirement regression.
- You learned the difference between code that runs and code that is correct.
- You used a boundary-value test rather than random examples.

Revert the change to `70` and run the test again. It must pass before you continue.

---

## Step 7 — Inspect a security decision

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_security_regression.py::test_horizontal_access_is_blocked -vv -s
```

Trace:

```text
Analyst One creates record
    ↓
Client clears Analyst One's cookie
    ↓
Analyst Two logs in
    ↓
Analyst Two requests Analyst One's record directly
    ↓
Route checks owner_id against authenticated user id
    ↓
403 denied + audit event
```

Key idea: hiding a button is not authorization. The server must enforce the access rule even when a caller goes directly to the endpoint.

---

## Step 8 — Record your ownership

Complete one session entry in `LEARNING_LOG.md`.

Your entry must include:

- One requirement you can explain
- One failure you intentionally created
- One test that caught it
- One security invariant
- One part you still do not understand
- One change you made without asking AI to write it

## Definition of done

This first session is complete only when:

- The application runs locally.
- The fast suite passes.
- You have observed one intentional failure.
- You restored the correct behavior.
- You can explain the request path without reading a generated summary.
- `LEARNING_LOG.md` contains your own notes.
