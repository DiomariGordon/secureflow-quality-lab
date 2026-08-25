# Learning Workbook

## The seven-step loop

Use this loop for every feature or test:

1. **Read** — State the requirement in plain language.
2. **Predict** — Name the code and test files you expect to change.
3. **Run** — Execute the smallest relevant test before editing.
4. **Break** — Create or reproduce a meaningful failure.
5. **Fix** — Make the smallest justified change.
6. **Explain** — Describe the data flow, risk, and evidence in your own words.
7. **Commit** — Save only understood, tested work.

AI can assist in steps 2, 4, and 5. You retain ownership of steps 1, 3, 6, and 7.

## Knowledge levels

Do not call a tool a skill merely because AI produced working code.

| Level | Evidence |
|---|---|
| Exposure | You can run an existing command. |
| Familiarity | You can explain the major components. |
| Working skill | You can change a requirement and update the right tests. |
| Independent competence | You can diagnose failures without asking AI for the answer first. |
| Engineering ownership | You can defend architecture, trade-offs, risk, and release criteria. |

The project should move you from exposure toward working skill and ownership.

## Milestone 1 learning checks

You should be able to answer:

- Why are risk scores `39`, `40`, `69`, and `70` useful test values?
- Why is an API test not a replacement for a browser test, and vice versa?
- Why does the data-integrity test query SQLite after reading the API response?
- What is the difference between authentication and authorization?
- Why is a hidden UI button not a security control?
- Why is CSRF required for state-changing requests but not ordinary reads?
- What does server-side session invalidation protect that a signed cookie alone does not?
- What information should an audit event contain?

## Milestone 2 learning checks

Before claiming framework-engineering experience, you should be able to:

- Explain fixture scope and test isolation.
- Build one reusable API client.
- Create deterministic test data and cleanup.
- Add failure screenshots and traces.
- Categorize a failure as product, test, data, environment, or infrastructure.
- Explain when retries hide a defect instead of improving reliability.
- Run tests in CI and find the evidence artifact.

## Milestone 3 learning checks

Before claiming security-testing experience, you should be able to:

- Convert a security requirement into a positive and negative test.
- Explain horizontal versus vertical privilege escalation.
- Distinguish regression testing from penetration testing.
- Explain why automated scanners produce false positives and false negatives.
- Identify which security decisions require manual review.
- State the authorization scope before testing any system.

## Weekly cadence

A sustainable sequence is three sessions per week:

### Session A — Understand

Read one path, draw the flow, and run one targeted test.

### Session B — Change

Implement one small requirement and update its tests.

### Session C — Challenge

Add a negative test, break the implementation, diagnose the failure, and document the result.

One understood change per week is more valuable than a large AI-generated feature you cannot defend.
