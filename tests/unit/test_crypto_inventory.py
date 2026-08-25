from __future__ import annotations

from secureflow.crypto_inventory import analyze_inventory, classify_algorithm, render_markdown


def test_classifies_public_key_migration_targets():
    disposition, rationale, priority = classify_algorithm("RSA")
    assert disposition == "MIGRATE"
    assert "Public-key" in rationale
    assert priority == 1


def test_recognizes_nist_pqc_standard_names():
    assert classify_algorithm("ML-KEM")[0] == "PQC_STANDARD"
    assert classify_algorithm("ML-DSA")[0] == "PQC_STANDARD"
    assert classify_algorithm("SLH-DSA")[0] == "PQC_STANDARD"


def test_inventory_prioritizes_migration_before_review():
    payload = {
        "systems": [
            {
                "name": "demo",
                "components": [
                    {"name": "symmetric", "algorithm": "AES-256"},
                    {"name": "certificate", "algorithm": "RSA"},
                ],
            }
        ]
    }
    findings = analyze_inventory(payload)
    assert findings[0].component == "certificate"
    assert findings[0].disposition == "MIGRATE"
    report = render_markdown(findings)
    assert "Educational inventory only" in report
    assert "| 1 | demo | certificate | RSA | MIGRATE |" in report
