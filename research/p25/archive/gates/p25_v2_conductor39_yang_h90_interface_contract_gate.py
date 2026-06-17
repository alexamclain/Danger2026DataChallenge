#!/usr/bin/env python3
"""Lightweight validator for the conductor-39 Yang/H90 interface contract.

The contract was built from seven older gates.  This v2 gate does not replay
those gates during the live production fleet.  It verifies that the promoted
evidence page still contains the exact structural clauses that make conductor
39 a first-pass target, and that it still states the missing object precisely:
a finite value/divisor theorem for one legal support-156 Yang/H90 product.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P25 = 10**25 + 13
EVIDENCE_PATH = "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md"

REQUIRED_CLAUSES = (
    "U_chi = -chi_39 = -chi_3 * chi_13",
    "proper pushforward mod 3 = 0",
    "proper pushforward mod 13 = 0",
    "U_chi = 1_{7<2>} - 1_{<2>}",
    "Frob_p swaps the two cosets",
    "ord_39(p) = 6",
    "p^3 = -1 mod 39",
    "Legendre(-39, p) = -1",
    "W = 6 * U_chi",
    "W = (1 - Frob_p) V",
    "target_level = 507",
    "support_period = 156",
    "Norm_156(Y_507) support = 312",
    "legal Yang lift support = 156",
    "(1 - Frob_p) of each legal lift = Norm_156(Y_507)",
    "quotient_representatives = (1, 2, 4, 8)",
    "lifted product = 78 positive Yang-fiber factors over 78 negative factors",
    "boundary = Norm_156(Y_507)",
    "still_missing = finite-field value/divisor theorem for the legal support-156",
)

REJECT_CLAUSES = (
    "prime-axis projection or pullback",
    "conductor-3-only or conductor-13-only source",
    "additively separated mod-3/mod-13 explanation",
    "formal one-coset sparse gauge without Hilbert-90 or ratio boundary",
    "direct F_p primitive 39th-root or sqrt(-39) shortcut",
    "value theorem without period-156 branch/root/telescoping context",
    "norm-only statement without Frobenius anti-invariance or Hilbert-90 descent",
)


@dataclass(frozen=True)
class ContractCheck:
    evidence_path: Path
    marker_present: bool
    required_clauses_ok: int
    required_clauses_total: int
    reject_clauses_ok: int
    reject_clauses_total: int
    p_mod_39: int
    p3_is_minus_one_mod_39: bool
    ord_39_p: int
    continue_conductor39: bool
    current_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd
    for parent in (cwd, *cwd.parents):
        if (parent / "research/p25").exists():
            return parent
    raise FileNotFoundError("run from repo root or inside repo")


def multiplicative_order(value: int, modulus: int) -> int:
    residue = value % modulus
    current = residue
    for order in range(1, modulus + 1):
        if current == 1:
            return order
        current = (current * residue) % modulus
    raise ValueError("order not found")


def build_check(root: Path) -> ContractCheck:
    path = root / EVIDENCE_PATH
    text = path.read_text() if path.exists() else ""
    marker_present = "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1" in text
    required_ok = sum(clause in text for clause in REQUIRED_CLAUSES)
    reject_ok = sum(clause in text for clause in REJECT_CLAUSES)
    p_mod_39 = P25 % 39
    p3_is_minus_one = pow(P25, 3, 39) == 38
    ord_39 = multiplicative_order(P25, 39)
    continue_conductor39 = "continue_conductor39 = yes" in text
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        path.exists()
        and marker_present
        and required_ok == len(REQUIRED_CLAUSES)
        and reject_ok == len(REJECT_CLAUSES)
        and p_mod_39 == 23
        and p3_is_minus_one
        and ord_39 == 6
        and continue_conductor39
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return ContractCheck(
        evidence_path=Path(EVIDENCE_PATH),
        marker_present=marker_present,
        required_clauses_ok=required_ok,
        required_clauses_total=len(REQUIRED_CLAUSES),
        reject_clauses_ok=reject_ok,
        reject_clauses_total=len(REJECT_CLAUSES),
        p_mod_39=p_mod_39,
        p3_is_minus_one_mod_39=p3_is_minus_one,
        ord_39_p=ord_39,
        continue_conductor39=continue_conductor39,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(repo_root())
    print("p25 v2 conductor-39 Yang/H90 interface contract")
    print(f"evidence_path={check.evidence_path}")
    print(f"marker_present={int(check.marker_present)}")
    print(f"required_clauses_ok={check.required_clauses_ok}/{check.required_clauses_total}")
    print(f"reject_clauses_ok={check.reject_clauses_ok}/{check.reject_clauses_total}")
    print(f"p_mod_39={check.p_mod_39}")
    print(f"p3_is_minus_one_mod_39={int(check.p3_is_minus_one_mod_39)}")
    print(f"ord_39_p={check.ord_39_p}")
    print(f"continue_conductor39={int(check.continue_conductor39)}")
    print(f"current_source_theorems={check.current_source_theorems}")
    print(f"current_submission_ready={check.current_submission_ready}")
    print(f"p25_v2_conductor39_yang_h90_interface_contract_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
