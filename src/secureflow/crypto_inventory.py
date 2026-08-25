from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

Disposition = Literal["MIGRATE", "REVIEW", "PQC_STANDARD", "OUT_OF_SCOPE"]

PQC_STANDARDS = {"ML-KEM", "ML-DSA", "SLH-DSA"}
QUANTUM_VULNERABLE_PUBLIC_KEY = {
    "RSA",
    "ECDSA",
    "ECDH",
    "DH",
    "DSA",
}
REVIEW_SYMMETRIC = {"AES-128", "3DES"}


@dataclass(frozen=True)
class Finding:
    system: str
    component: str
    algorithm: str
    disposition: Disposition
    rationale: str
    priority: int


def classify_algorithm(algorithm: str) -> tuple[Disposition, str, int]:
    normalized = algorithm.strip().upper()
    if normalized in PQC_STANDARDS:
        return (
            "PQC_STANDARD",
            "NIST-standardized post-quantum algorithm; validate implementation and interoperability.",
            4,
        )
    if normalized in QUANTUM_VULNERABLE_PUBLIC_KEY:
        return (
            "MIGRATE",
            "Public-key algorithm is vulnerable to a sufficiently capable cryptanalytic quantum computer.",
            1,
        )
    if normalized in REVIEW_SYMMETRIC:
        return (
            "REVIEW",
            "Review key strength, lifetime, implementation, and migration policy; this is not equivalent to public-key breakage.",
            2,
        )
    if normalized in {"AES-256", "SHA-256", "SHA-384", "SHA-512", "HMAC-SHA256"}:
        return (
            "REVIEW",
            "Not an immediate public-key PQC migration target; confirm approved configuration and crypto-agility.",
            3,
        )
    return (
        "OUT_OF_SCOPE",
        "Algorithm is not classified by this educational inventory; obtain specialist review.",
        5,
    )


def analyze_inventory(payload: dict) -> list[Finding]:
    findings: list[Finding] = []
    for system in payload.get("systems", []):
        system_name = str(system.get("name", "unnamed-system"))
        for component in system.get("components", []):
            component_name = str(component.get("name", "unnamed-component"))
            algorithm = str(component.get("algorithm", "unknown"))
            disposition, rationale, priority = classify_algorithm(algorithm)
            findings.append(
                Finding(
                    system=system_name,
                    component=component_name,
                    algorithm=algorithm,
                    disposition=disposition,
                    rationale=rationale,
                    priority=priority,
                )
            )
    return sorted(findings, key=lambda finding: (finding.priority, finding.system, finding.component))


def render_markdown(findings: list[Finding]) -> str:
    lines = [
        "# Crypto-Agility Readiness Inventory",
        "",
        "> Educational inventory only. This is not a cryptographic audit, compliance determination, or penetration test.",
        "",
        "| Priority | System | Component | Algorithm | Disposition | Rationale |",
        "|---:|---|---|---|---|---|",
    ]
    for finding in findings:
        lines.append(
            f"| {finding.priority} | {finding.system} | {finding.component} | "
            f"{finding.algorithm} | {finding.disposition} | {finding.rationale} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a synthetic cryptographic inventory.")
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with args.inventory.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    findings = analyze_inventory(payload)
    if args.format == "markdown":
        rendered = render_markdown(findings)
    else:
        rendered = json.dumps([asdict(finding) for finding in findings], indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
