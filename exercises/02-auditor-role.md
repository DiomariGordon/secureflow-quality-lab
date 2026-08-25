# Exercise 2 — Add an Auditor Role

## Requirement

An auditor may:

- Read all records.
- Read audit events.

An auditor may not:

- Create records.
- Submit records.
- Approve records.

## Before coding

Write a permission matrix for analyst, viewer, approver, and auditor.

## Baseline command

```powershell
.\scripts\run_security_tests.ps1
```

## Expected files

- `src/secureflow/db.py`
- `src/secureflow/repository.py`
- `src/secureflow/app.py`
- `tests/conftest.py`
- `tests/api/test_security_regression.py`

AI may propose a different set. Compare its proposal with yours before accepting it.

## Required tests

- Auditor can list all records.
- Auditor can read audit events.
- Auditor receives `403` when creating.
- Auditor receives `403` when submitting.
- Auditor receives `403` when approving.

## Security question

Would a new UI button be enough to implement this role? Explain why or why not.
