# Crypto-Agility Readiness Inventory

> Educational inventory only. This is not a cryptographic audit, compliance determination, or penetration test.

| Priority | System | Component | Algorithm | Disposition | Rationale |
|---:|---|---|---|---|---|
| 1 | customer-portal | tls-certificate | RSA | MIGRATE | Public-key algorithm is vulnerable to a sufficiently capable cryptanalytic quantum computer. |
| 1 | customer-portal | token-signature | ECDSA | MIGRATE | Public-key algorithm is vulnerable to a sufficiently capable cryptanalytic quantum computer. |
| 2 | migration-lab | legacy-batch-encryption | 3DES | REVIEW | Review key strength, lifetime, implementation, and migration policy; this is not equivalent to public-key breakage. |
| 3 | customer-portal | session-encryption | AES-256 | REVIEW | Not an immediate public-key PQC migration target; confirm approved configuration and crypto-agility. |
| 4 | migration-lab | document-signature-pilot | ML-DSA | PQC_STANDARD | NIST-standardized post-quantum algorithm; validate implementation and interoperability. |
| 4 | migration-lab | key-establishment-pilot | ML-KEM | PQC_STANDARD | NIST-standardized post-quantum algorithm; validate implementation and interoperability. |
