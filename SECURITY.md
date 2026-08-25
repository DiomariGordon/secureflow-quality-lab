# Security Policy and Scope

SecureFlow is for local learning, portfolio development, and explicitly authorized environments.

Do not point its tests or future scanners at systems you do not own or lack written permission to assess. Do not use employer code, credentials, production data, patient data, customer data, or proprietary requirements in this repository.

## Configuration boundary

- `.env` and local SQLite databases are ignored by Git.
- The Windows launcher generates a process-scoped development signing secret.
- Docker Compose requires a secret supplied outside version control.
- `SECUREFLOW_ENV=production` rejects a missing or short secret, insecure cookies, and seeded demonstration accounts.
- Test fixtures use fixed synthetic credentials and secrets only for deterministic automated tests.

See [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md) for demonstrated controls and known gaps.

## Reporting

This is a personal portfolio repository. Please open a GitHub issue for a reproducible defect that contains no sensitive information. Do not include credentials, tokens, private data, or exploit attempts against systems outside this repository.

The included crypto inventory is educational and is not a cryptographic audit, certification, penetration test, or compliance opinion. Production cryptography should use approved libraries and qualified security review; do not invent cryptographic algorithms.
