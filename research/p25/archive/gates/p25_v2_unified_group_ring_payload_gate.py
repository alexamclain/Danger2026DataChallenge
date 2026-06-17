#!/usr/bin/env python3
"""Machine-check the group-ring payload behind the unified p25 theorem ask.

The review packet is intentionally human-facing.  This gate records the
algebraic object behind it: the conductor-39 Hilbert-90 word, the level-507
Yang lift, the period norm of Y_507, and the four support-156 product rows.
It still does not prove the missing arithmetic value/divisor theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (
    profile_sparse_hilbert90_yang_lift,
)
from p25_ksy_y_yang_y507_period_norm_character_gate import (
    profile_yang_y507_period_norm_character,
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class PayloadRow:
    multiplier: int
    constants: tuple[int, int, int, int]
    positive_mod39: tuple[int, ...]
    negative_mod39: tuple[int, ...]
    lifted_positive_entries: tuple[int, ...]
    lifted_negative_entries: tuple[int, ...]
    coefficient: int
    product_formula: str
    payload_sha256: str
    row_ok: bool


@dataclass(frozen=True)
class GroupRingPayload:
    evidence_markers: tuple[EvidenceMarker, ...]
    level: int
    conductor: int
    lift_length: int
    support_period: int
    p_mod_39: int
    h90_character_support: int
    balanced_potential_support: int
    sparse_potential_support: int
    period_norm_support: int
    period_norm_counts: tuple[tuple[int, int], ...]
    legal_product_rows: tuple[PayloadRow, ...]
    payload_rows_ok: int
    one_doubling_orbit: bool
    stabilizer: tuple[int, ...]
    quotient_representatives: tuple[int, ...]
    formal_one_coset_rejected: bool
    source_theorem_in_hand: bool
    direct_closer: bool
    evidence_markers_ok: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_target",
            "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
            "p25_v2_h0_conductor39_unified_target_rows=1/1",
        ),
        marker(
            "theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "source_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "hidden_selector_or_gauge_freedom_remaining = no",
        ),
        marker(
            "value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
    )


def lifted_entries(residues: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(residue + 39 * k_value for residue in residues for k_value in range(13)))


def payload_text(row) -> str:
    lines: list[str] = []
    for entry in lifted_entries(row.source_positive_residues):
        lines.append(f"{entry}\t6")
    for entry in lifted_entries(row.source_negative_residues):
        lines.append(f"{entry}\t-6")
    return "\n".join(sorted(lines)) + "\n"


def payload_row(row) -> PayloadRow:
    pos_entries = lifted_entries(row.source_positive_residues)
    neg_entries = lifted_entries(row.source_negative_residues)
    text = payload_text(row)
    row_ok = (
        len(pos_entries) == 78
        and len(neg_entries) == 78
        and len(set(pos_entries) | set(neg_entries)) == 156
        and set(pos_entries).isdisjoint(set(neg_entries))
        and all(0 <= entry < 507 for entry in pos_entries + neg_entries)
        and row.lifted_positive_count == 78
        and row.lifted_negative_count == 78
        and row.lifted_support == 156
        and row.boundary_equals_period_norm
        and row.row_ok
    )
    return PayloadRow(
        multiplier=row.multiplier_from_canonical,
        constants=row.source_constants,
        positive_mod39=row.source_positive_residues,
        negative_mod39=row.source_negative_residues,
        lifted_positive_entries=pos_entries,
        lifted_negative_entries=neg_entries,
        coefficient=6,
        product_formula=row.product_formula,
        payload_sha256=sha256(text.encode()).hexdigest(),
        row_ok=row_ok,
    )


def build_payload() -> GroupRingPayload:
    markers = evidence_markers()
    h90 = profile_yang_y507_conductor39_hilbert90_boundary()
    lift = profile_sparse_hilbert90_yang_lift()
    product = profile_sparse_h90_product_normal_form()
    period = profile_yang_y507_period_norm_character()
    rows = tuple(payload_row(row) for row in product.legal_rows)
    markers_ok = sum(m.ok for m in markers)
    rows_ok = sum(row.row_ok for row in rows)
    source_theorem = False
    direct_closer = False
    row_ok = (
        markers_ok == len(markers)
        and h90.row_ok
        and lift.row_ok
        and product.row_ok
        and period.row_ok
        and product.conductor == 39
        and product.target_level == 507
        and product.lift_length == 13
        and product.support_period == 156
        and h90.p_mod_39 == 23
        and h90.balanced_support == 24
        and h90.sparse_support == 12
        and lift.period_norm_support == 312
        and lift.period_norm_coefficient_counts == ((-6, 156), (6, 156))
        and len(rows) == 4
        and rows_ok == 4
        and product.legal_rows_form_one_doubling_orbit
        and product.canonical_stabilizer == (1, 16, 22)
        and product.quotient_representatives == (1, 2, 4, 8)
        and product.formal_one_coset_controls_rejected
        and not source_theorem
        and not direct_closer
    )
    return GroupRingPayload(
        evidence_markers=markers,
        level=product.target_level,
        conductor=product.conductor,
        lift_length=product.lift_length,
        support_period=product.support_period,
        p_mod_39=h90.p_mod_39,
        h90_character_support=len(h90.character_word),
        balanced_potential_support=h90.balanced_support,
        sparse_potential_support=h90.sparse_support,
        period_norm_support=lift.period_norm_support,
        period_norm_counts=lift.period_norm_coefficient_counts,
        legal_product_rows=rows,
        payload_rows_ok=rows_ok,
        one_doubling_orbit=product.legal_rows_form_one_doubling_orbit,
        stabilizer=product.canonical_stabilizer,
        quotient_representatives=product.quotient_representatives,
        formal_one_coset_rejected=product.formal_one_coset_controls_rejected,
        source_theorem_in_hand=source_theorem,
        direct_closer=direct_closer,
        evidence_markers_ok=markers_ok,
        row_ok=row_ok,
    )


def main() -> int:
    payload = build_payload()
    for marker_row in payload.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("ambient")
    print(f"  level={payload.level}")
    print(f"  conductor={payload.conductor}")
    print(f"  lift_length={payload.lift_length}")
    print(f"  support_period={payload.support_period}")
    print(f"  p_mod_39={payload.p_mod_39}")
    print(f"  h90_character_support={payload.h90_character_support}")
    print(f"  balanced_potential_support={payload.balanced_potential_support}")
    print(f"  sparse_potential_support={payload.sparse_potential_support}")
    print(f"  period_norm_support={payload.period_norm_support}")
    print(f"  period_norm_counts={payload.period_norm_counts}")
    print("legal_payload_rows")
    for row in payload.legal_product_rows:
        print(
            "  "
            f"m={row.multiplier} constants={row.constants} "
            f"pos39={row.positive_mod39} neg39={row.negative_mod39} "
            f"lifted=+{len(row.lifted_positive_entries)}/-{len(row.lifted_negative_entries)} "
            f"coefficient={row.coefficient} sha256={row.payload_sha256} ok={int(row.row_ok)}"
        )
    print("checks")
    print(f"  evidence_markers_ok={payload.evidence_markers_ok}/{len(payload.evidence_markers)}")
    print(f"  payload_rows_ok={payload.payload_rows_ok}/{len(payload.legal_product_rows)}")
    print(f"  one_doubling_orbit={int(payload.one_doubling_orbit)}")
    print(f"  stabilizer={payload.stabilizer}")
    print(f"  quotient_representatives={payload.quotient_representatives}")
    print(f"  formal_one_coset_rejected={int(payload.formal_one_coset_rejected)}")
    print(f"  source_theorem_in_hand={int(payload.source_theorem_in_hand)}")
    print(f"  direct_closer={int(payload.direct_closer)}")
    print(f"p25_v2_unified_group_ring_payload_rows={int(payload.row_ok)}/1")
    return 0 if payload.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
