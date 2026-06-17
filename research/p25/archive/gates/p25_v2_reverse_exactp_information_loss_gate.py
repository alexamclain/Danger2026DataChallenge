#!/usr/bin/env python3
"""Guard against reversing the exact-P -> unified-target spine.

The current theorem lattice is intentionally one-way:

    compact exact-P theorem -> unified H0/conductor-39 support-156 target.

A theorem for the unified target would be a first-pass win, but it does not by
itself reconstruct the exact-P 75-atom packet.  This lightweight gate records
the information that is lost at the unified target surface so future source
snippets do not get over-promoted.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ReverseBoundary:
    name: str
    role: str
    statement: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ReverseExactPInformationLoss:
    evidence_markers: tuple[EvidenceMarker, ...]
    boundaries: tuple[ReverseBoundary, ...]
    exactp_packet_present: bool
    unified_payload_present: bool
    unified_payload_contains_exactp_packet: bool
    reverse_requires_extra_structure: bool
    evidence_markers_ok: int
    boundary_rows_ok: int
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text() if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    text = read(path)
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_contract",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "raw center C = (47, 28)",
        ),
        marker(
            "exactp_to_unified_spine",
            "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
            "unified target theorem hit -> exact-P theorem hit is not proved",
        ),
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "payload_rows = 4",
        ),
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
    )


def boundary_rows(
    exactp_contract: str, exactp_spine: str, unified_payload: str, extraction_router: str
) -> tuple[ReverseBoundary, ...]:
    exactp_packet_strings = (
        "raw center C = (47, 28)",
        "raw D        = (22, 3)",
        "raw K        = (57, 0)",
        "orientation",
    )
    unified_row_strings = (
        "m=1",
        "constants = (3, 3, -3, -3)",
        "lifted = +78 / -78",
        "Norm_156(Y_507)",
    )
    return (
        ReverseBoundary(
            name="forward_exactp_to_unified",
            role="accept",
            statement=(
                "A compact exact-P theorem may feed the unified support-156 "
                "H0/conductor-39 target."
            ),
            first_missing_or_falsifier="missing exact equal-weight 75-atom or theta2 payload",
            ok=(
                "exact-P theorem hit -> unified H0/conductor-39 target" in exactp_spine
                and all(s in exactp_contract for s in exactp_packet_strings)
            ),
        ),
        ReverseBoundary(
            name="reverse_unified_to_exactp",
            role="reject",
            statement=(
                "A unified support-156 value/divisor theorem alone reconstructs "
                "the exact-P C,D,K,orientation packet."
            ),
            first_missing_or_falsifier=(
                "unified payload records only the four support-156 product rows; "
                "the exact-P packet is absent"
            ),
            ok=(
                "unified target theorem hit -> exact-P theorem hit is not proved"
                in exactp_spine
                and all(s in unified_payload for s in unified_row_strings)
                and not any(s in unified_payload for s in exactp_packet_strings)
            ),
        ),
        ReverseBoundary(
            name="reverse_repair_payload",
            role="repair",
            statement=(
                "A reverse exact-P claim must add the exact 75-atom theorem, "
                "C,D,K,orientation data, or an accepted period-156 theta2 payload."
            ),
            first_missing_or_falsifier="no exact-P selector theorem or theta2 payload supplied",
            ok=(
                "period-156 theta2 divisor/additive payload" in exactp_contract
                and "75 -> 300 -> 12 -> 312 -> 156" in exactp_spine
            ),
        ),
        ReverseBoundary(
            name="unified_theorem_routing",
            role="route",
            statement=(
                "A unified theorem hit should route to DANGER3 extraction before "
                "being described as certificate-ready or exact-P-ready."
            ),
            first_missing_or_falsifier="same-j X_1(8112), X_1(16), halving/direct x0, vpp.py",
            ok=(
                "source theorem" in extraction_router
                and "same-j" in extraction_router
                and "official vpp.py" in extraction_router
            ),
        ),
    )


def build_profile() -> ReverseExactPInformationLoss:
    exactp_contract = read(
        "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md"
    )
    exactp_spine = read(
        "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md"
    )
    unified_payload = read(
        "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md"
    )
    extraction_router = read(
        "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md"
    )
    ms = evidence_markers()
    rows = boundary_rows(exactp_contract, exactp_spine, unified_payload, extraction_router)
    exactp_packet_strings = (
        "raw center C = (47, 28)",
        "raw D        = (22, 3)",
        "raw K        = (57, 0)",
    )
    exactp_packet_present = all(s in exactp_contract for s in exactp_packet_strings)
    unified_payload_present = (
        "payload_rows = 4" in unified_payload
        and "support-156 product rows" in unified_payload
        and "lifted = +78 / -78" in unified_payload
    )
    unified_contains_exactp = any(s in unified_payload for s in exactp_packet_strings)
    reverse_requires_extra_structure = (
        "unified target theorem hit -> exact-P theorem hit is not proved" in exactp_spine
        and not unified_contains_exactp
        and "equal-weight 75-atom normalized-y product" in exactp_spine
        and "theta2/divisor payload" in exactp_spine
    )
    evidence_ok = sum(m.ok for m in ms)
    boundary_ok = sum(r.ok for r in rows)
    row_ok = (
        evidence_ok == len(ms)
        and len(rows) == 4
        and boundary_ok == 4
        and exactp_packet_present
        and unified_payload_present
        and not unified_contains_exactp
        and reverse_requires_extra_structure
    )
    return ReverseExactPInformationLoss(
        evidence_markers=ms,
        boundaries=rows,
        exactp_packet_present=exactp_packet_present,
        unified_payload_present=unified_payload_present,
        unified_payload_contains_exactp_packet=unified_contains_exactp,
        reverse_requires_extra_structure=reverse_requires_extra_structure,
        evidence_markers_ok=evidence_ok,
        boundary_rows_ok=boundary_ok,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    for marker_ in profile.evidence_markers:
        print(f"marker {marker_.name}: {'ok' if marker_.ok else 'MISSING'}")
    for row in profile.boundaries:
        print(f"boundary {row.name}: role={row.role} ok={int(row.ok)}")
    print(f"exactp_packet_present={int(profile.exactp_packet_present)}")
    print(f"unified_payload_present={int(profile.unified_payload_present)}")
    print(
        "unified_payload_contains_exactp_packet="
        f"{int(profile.unified_payload_contains_exactp_packet)}"
    )
    print(f"reverse_requires_extra_structure={int(profile.reverse_requires_extra_structure)}")
    print(f"evidence_markers_ok={profile.evidence_markers_ok}/{len(profile.evidence_markers)}")
    print(f"boundary_rows_ok={profile.boundary_rows_ok}/{len(profile.boundaries)}")
    print(f"p25_v2_reverse_exactp_information_loss_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
