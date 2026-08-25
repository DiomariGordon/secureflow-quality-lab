# Exercise 1 — Risk Boundary Ownership

## Requirement

- `0–39` is LOW.
- `40–69` is MEDIUM.
- `70–100` is HIGH.

## Baseline command

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_api_workflow.py::test_risk_boundary_classification -vv
```

## Tasks

1. Explain why the test uses `39`, `40`, `69`, and `70`.
2. Add valid extremes `0` and `100`.
3. Find where Pydantic rejects out-of-range scores.
4. Add negative tests for `-1` and `101`.
5. Temporarily change the threshold and confirm the boundary test fails.
6. Restore the rule and record the evidence in `LEARNING_LOG.md`.

## Definition of done

- Valid boundaries pass.
- Invalid values are rejected with the expected response status.
- You can explain whether the rejection occurred in the model, route, repository, or database.
