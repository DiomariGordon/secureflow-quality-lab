# AI-Assisted Development Without Losing the Learning

AI is allowed to accelerate implementation. It is not allowed to replace your engineering judgment.

## Before prompting AI

Write:

- Requirement
- Security or quality invariant
- Expected files
- Expected tests
- What should not change

Example:

> Requirement: a viewer cannot create records. Invariant: authorization must be enforced at the server route, not only in the UI. Expected files: route or policy code plus a negative API test. The login flow should not change.

## After AI responds

Use this review sequence:

```powershell
git diff
.\scripts\run_fast_tests.ps1
```

Then ask yourself:

1. Did AI change more files than expected?
2. Is the assertion testing behavior or merely implementation detail?
3. Could the test pass for the wrong reason?
4. Is there a missing negative case?
5. Did the change weaken authentication, authorization, input validation, logging, or secrets handling?

## Required ownership exercise

For every AI-generated feature, manually do at least one of these:

- Write one additional test.
- Refactor one unclear name.
- Add one meaningful negative case.
- Deliberately introduce a defect and identify which test catches it.
- Explain the route-to-database flow without assistance.

## AI assistance log template

Copy this into `LEARNING_LOG.md`:

```markdown
### Change

**Requirement:**

**AI tool and prompt summary:**

**Files AI proposed changing:**

**What I expected before seeing the answer:**

**What I rejected or changed manually:**

**Targeted test command:**

**Intentional failure introduced:**

**Why the final assertions are trustworthy:**

**Remaining risk or open question:**
```

## Commenting rule

Comments should explain **why**, an invariant, or a non-obvious trade-off. Avoid comments that simply translate Python syntax into English.

Good:

```python
# The status predicate prevents a stale client from approving a record that is no longer submitted.
```

Weak:

```python
# Set the status to approved.
```

## Interview value

A mature explanation sounds like:

> I used AI to accelerate scaffolding and candidate tests, but I controlled requirements, reviewed diffs, added adversarial cases, ran targeted and full suites, and documented remaining risk. I can show where generated code was wrong or incomplete and how the evidence changed my decision.

That demonstrates AI-native engineering rather than AI dependence.
