# SecureFlow Learning Log

This log records what AI accelerated, what I independently executed, and what I can explain without treating generated code as proof.

## Baseline architecture review

**What I reviewed:** The path from pytest fixtures through FastAPI routes, authentication, repository functions, SQLite persistence, and API responses.

**What I can explain:**
- `conftest.py` provides reusable fixtures; fixtures are not tests themselves.
- PowerShell files are runner/wrapper scripts that invoke Python and pytest.
- Pytest discovers `test_*.py` files and `test_*` functions under the configured test path.
- `-m "not e2e"` is a marker expression that excludes the test decorated with `@pytest.mark.e2e`.
- API-to-database comparison proves cross-layer consistency, but a separate business-rule oracle is still needed because two layers can be consistently wrong.

## Fast-suite execution

**I ran:** `scripts/run_fast_tests.ps1` on my Windows development machine.

**I observed:** Pytest collected 12 items, deselected the one E2E test, and passed the remaining 11 tests. I initially interpreted bracketed percentages beside test files as per-file coverage. I corrected that interpretation: they showed cumulative execution progress. The actual coverage table reported 84% non-browser application coverage.

**What I learned:** Test count, execution progress, and source coverage are different measurements. A green suite and high coverage are useful evidence, not proof that every requirement or risk is covered.

## Browser E2E execution

**I ran:** `scripts/run_e2e_tests.ps1`.

**I observed:** Pytest selected the single test marked `e2e`, launched the Playwright-controlled browser workflow, and passed the analyst create-and-submit scenario.

**What I can explain:** The test crosses the browser, login/session controls, API route, business rules, persistence, submission transition, and visible UI state. It verifies one critical path, not comprehensive product correctness.

## Human-review rule

For future AI-assisted changes I will record:
1. The requirement and risk.
2. The proposed diff.
3. What I independently checked or rejected.
4. The narrow and full tests executed.
5. Remaining uncertainty and the next smallest action.
