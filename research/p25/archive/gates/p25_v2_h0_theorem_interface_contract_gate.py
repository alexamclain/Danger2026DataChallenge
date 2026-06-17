#!/usr/bin/env python3
"""Lightweight validator for the p25 H0 theorem-interface contract.

The H0 interface was assembled from nine archived gates.  This v2 validator
does not replay them during the live production run.  It checks that the
promoted evidence page still records the exact legal H0 rows, the two accepted
source-stage theorem shapes, the period/Hilbert-90 constraints, the downstream
same-j bridge payload, and the first falsifiers.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
EVIDENCE_PATH = "research/p25/evidence/p25_v2_h0_theorem_interface_contract_20260616.md"

LEGAL_ROW_CLAUSES = (
    "m = 1",
    "constants = (3, 3, -3, -3)",
    "positive residues = (7, 17, 23, 34, 37, 38)",
    "negative residues = (4, 8, 10, 11, 20, 25)",
    "m = 2  constants = (-3,  3,  3, -3)",
    "m = 4  constants = (-3, -3,  3,  3)",
    "m = 8  constants = ( 3, -3, -3,  3)",
)

SOURCE_EXIT_CLAUSES = (
    "exact finite H0 value identity",
    "period-156 branch/root/telescoping context",
    "boundary (1 - Frob_p) H0 = Norm_156(Y_507)",
    "exact H0 divisor/additive identity",
    "Hilbert-90 boundary to Norm_156(Y_507)",
)

PERIOD_BOUNDARY_CLAUSES = (
    "Y_507 minimum doubling period = 156",
    "H0 support period = 156",
    "support-period root gcd = 1",
    "ambient-period root gcd = 11",
    "ord_39(p) = 6",
    "primitive 39th roots first appear in degree 6",
    "sqrt(-39) is not in F_p",
)

DOWNSTREAM_CLAUSES = (
    "DANGER3 finite-identity / non-CM framing",
    "same-j X_1(8112) bridge",
    "X_1(16) y, model root, A, and xP16 extraction",
    "halving chain to x0",
    "official vpp.py verification",
    "levels = 16 and 507, coprime",
    "inv_507 mod 16 = 3",
    "inv_16 mod 507 = 412",
    "P16 = [3*507]R = [1521]R",
    "Q507 = [412*16]R = [6592]R",
    "1521 + 6592 = 1 mod 8112",
)

FALSIFIER_CLAUSES = (
    "nonlegal H0 product or formal one-coset product",
    "Koo-Shin 2010 source certification only",
    "boundary-only H0 data with no finite value/divisor theorem",
    "finite payload with no arithmetic source theorem",
    "value theorem without period-156 branch/root/telescoping context",
    "divisor/additive statement without Hilbert-90 boundary",
    "direct F_p order-39-root or sqrt(-39) shortcut",
    "same-j bridge missing after source closure",
    "unglued level-16 and level-507 data",
    "X_1(16) relation with no y/model-root/A/xP16 extraction",
    "unverified concrete triple",
)


@dataclass(frozen=True)
class H0TheoremInterfaceContractCheck:
    evidence_path: Path
    marker_present: bool
    archived_gate_summary_present: bool
    legal_rows_ok: int
    legal_rows_total: int
    source_exits_ok: int
    source_exits_total: int
    period_boundary_ok: int
    period_boundary_total: int
    downstream_ok: int
    downstream_total: int
    falsifiers_ok: int
    falsifiers_total: int
    p_mod_39: int
    ord_39_p: int
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    same_j_crt_payload_ok: bool
    continue_h0: bool
    current_h0_source_theorems: int
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


def build_check(root: Path) -> H0TheoremInterfaceContractCheck:
    path = root / EVIDENCE_PATH
    text = path.read_text() if path.exists() else ""
    marker_present = "p25_v2_h0_theorem_interface_contract_rows=1/1" in text
    archived_summary = "All nine gates returned their expected `rows=1/1` markers" in text
    legal_ok = sum(clause in text for clause in LEGAL_ROW_CLAUSES)
    exits_ok = sum(clause in text for clause in SOURCE_EXIT_CLAUSES)
    period_ok = sum(clause in text for clause in PERIOD_BOUNDARY_CLAUSES)
    downstream_ok = sum(clause in text for clause in DOWNSTREAM_CLAUSES)
    falsifiers_ok = sum(clause in text for clause in FALSIFIER_CLAUSES)
    p_mod_39 = P25 % 39
    ord_39 = multiplicative_order(P25, 39)
    support_period_root_gcd = gcd(4**156 - 1, P25 - 1)
    ambient_period_root_gcd = gcd(4**780 - 1, P25 - 1)
    same_j_crt_payload_ok = (
        (3 * 507) % 16 == 1
        and (412 * 16) % 507 == 1
        and (1521 + 6592) % 8112 == 1
        and gcd(16, 507) == 1
    )
    continue_h0 = "continue_h0 = yes" in text
    current_h0_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        path.exists()
        and marker_present
        and archived_summary
        and legal_ok == len(LEGAL_ROW_CLAUSES)
        and exits_ok == len(SOURCE_EXIT_CLAUSES)
        and period_ok == len(PERIOD_BOUNDARY_CLAUSES)
        and downstream_ok == len(DOWNSTREAM_CLAUSES)
        and falsifiers_ok == len(FALSIFIER_CLAUSES)
        and p_mod_39 == 23
        and ord_39 == 6
        and support_period_root_gcd == 1
        and ambient_period_root_gcd == 11
        and same_j_crt_payload_ok
        and continue_h0
        and current_h0_source_theorems == 0
        and current_submission_ready == 0
    )
    return H0TheoremInterfaceContractCheck(
        evidence_path=Path(EVIDENCE_PATH),
        marker_present=marker_present,
        archived_gate_summary_present=archived_summary,
        legal_rows_ok=legal_ok,
        legal_rows_total=len(LEGAL_ROW_CLAUSES),
        source_exits_ok=exits_ok,
        source_exits_total=len(SOURCE_EXIT_CLAUSES),
        period_boundary_ok=period_ok,
        period_boundary_total=len(PERIOD_BOUNDARY_CLAUSES),
        downstream_ok=downstream_ok,
        downstream_total=len(DOWNSTREAM_CLAUSES),
        falsifiers_ok=falsifiers_ok,
        falsifiers_total=len(FALSIFIER_CLAUSES),
        p_mod_39=p_mod_39,
        ord_39_p=ord_39,
        support_period_root_gcd=support_period_root_gcd,
        ambient_period_root_gcd=ambient_period_root_gcd,
        same_j_crt_payload_ok=same_j_crt_payload_ok,
        continue_h0=continue_h0,
        current_h0_source_theorems=current_h0_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(repo_root())
    print("p25 v2 H0 theorem-interface contract")
    print(f"evidence_path={check.evidence_path}")
    print(f"marker_present={int(check.marker_present)}")
    print(f"archived_gate_summary_present={int(check.archived_gate_summary_present)}")
    print(f"legal_rows_ok={check.legal_rows_ok}/{check.legal_rows_total}")
    print(f"source_exits_ok={check.source_exits_ok}/{check.source_exits_total}")
    print(f"period_boundary_ok={check.period_boundary_ok}/{check.period_boundary_total}")
    print(f"downstream_ok={check.downstream_ok}/{check.downstream_total}")
    print(f"falsifiers_ok={check.falsifiers_ok}/{check.falsifiers_total}")
    print(f"p_mod_39={check.p_mod_39}")
    print(f"ord_39_p={check.ord_39_p}")
    print(f"support_period_root_gcd={check.support_period_root_gcd}")
    print(f"ambient_period_root_gcd={check.ambient_period_root_gcd}")
    print(f"same_j_crt_payload_ok={int(check.same_j_crt_payload_ok)}")
    print(f"continue_h0={int(check.continue_h0)}")
    print(f"current_h0_source_theorems={check.current_h0_source_theorems}")
    print(f"current_submission_ready={check.current_submission_ready}")
    print(f"p25_v2_h0_theorem_interface_contract_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
