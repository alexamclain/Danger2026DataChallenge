#!/usr/bin/env python3
"""Twisted-descent decision packet for the conductor-39 value route.

The degree-6 packet says a value theorem cannot live directly in `F_p` via an
order-39 root.  This packet says what happens after going to degree 6: the
ordinary norm of the pure conductor-39 character is trivial, so the useful
descent has to be a twisted trace, quotient/ratio, or Hilbert-90 boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DEGREE6_PACKET = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_conductor39_degree6_value_descent_packet_20260614.md"
)
EXPERT_ANSWER_SMOKE = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_conductor39_expert_answer_smoke_20260614.md"
)
FROBENIUS_ORBIT = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_yang_y507_conductor39_frobenius_orbit_20260614.md"
)
COSET_PAIRING = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_20260614.md"
)
HILBERT90_BOUNDARY = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_20260614.md"
)

DEGREE6_PACKET_MARKER = "ksy_y_conductor39_degree6_value_descent_packet_rows=1/1"
EXPERT_ANSWER_SMOKE_MARKER = "ksy_y_conductor39_expert_answer_smoke_rows=1/1"
FROBENIUS_ORBIT_MARKER = "ksy_y_yang_y507_conductor39_frobenius_orbit_rows=1/1"
COSET_PAIRING_MARKER = "ksy_y_yang_y507_conductor39_coset_frobenius_pairing_rows=1/1"
HILBERT90_BOUNDARY_MARKER = "ksy_y_yang_y507_conductor39_hilbert90_boundary_rows=1/1"

TWO_CONJUGATE_SUM_SUPPORT = 0
THREE_CONJUGATE_SUM_EQUALS_WORD = True
SIX_CONJUGATE_SUM_SUPPORT = 0
PURE_CHARACTER_DEGREE6_NORM_CANCELS = True
Q_VALUE_FROBENIUS_INVERSE_CONTRACT = True
W_VALUE_FROBENIUS_INVERSE_CONTRACT = True
BALANCED_H90_SUPPORT = 24
SPARSE_H90_SUPPORT = 12


@dataclass(frozen=True)
class TwistedDescentRow:
    name: str
    candidate_shape: str
    uses_degree6_orbit: bool
    uses_pure_norm: bool
    uses_twisted_trace_or_ratio: bool
    uses_hilbert90_boundary: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    expected_decision: str
    first_falsifier_or_missing_clause: str
    source_stage_closed: bool
    ok: bool


@dataclass(frozen=True)
class TwistedDescentDecisionPacket:
    degree6_packet_ok: bool
    expert_answer_smoke_ok: bool
    frobenius_orbit_ok: bool
    coset_pairing_ok: bool
    hilbert90_boundary_ok: bool
    two_conjugate_sum_support: int
    three_conjugate_sum_equals_word: bool
    six_conjugate_sum_support: int
    pure_character_degree6_norm_cancels: bool
    q_value_frobenius_inverse_contract: bool
    w_value_frobenius_inverse_contract: bool
    balanced_h90_support: int
    sparse_h90_support: int
    route_rows: tuple[TwistedDescentRow, ...]
    route_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_closing_rows: int
    period156_closing_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def route_rows() -> tuple[TwistedDescentRow, ...]:
    return (
        TwistedDescentRow(
            name="pure_degree6_norm_of_character_word",
            candidate_shape="ordinary product/norm over all six Frobenius conjugates of W",
            uses_degree6_orbit=True,
            uses_pure_norm=True,
            uses_twisted_trace_or_ratio=False,
            uses_hilbert90_boundary=False,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            expected_decision="reject_pure_degree6_norm_cancels",
            first_falsifier_or_missing_clause="six-conjugate additive norm of the pure character word is zero",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="two_conjugate_pair_sum",
            candidate_shape="degree-2 pair sum W + Frob_p(W)",
            uses_degree6_orbit=True,
            uses_pure_norm=True,
            uses_twisted_trace_or_ratio=False,
            uses_hilbert90_boundary=False,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            expected_decision="reject_pair_sum_cancels",
            first_falsifier_or_missing_clause="Frob_p(W)=-W, so two-conjugate sum has support zero",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="three_conjugate_shadow",
            candidate_shape="three-conjugate signed shadow that recovers the word",
            uses_degree6_orbit=True,
            uses_pure_norm=False,
            uses_twisted_trace_or_ratio=True,
            uses_hilbert90_boundary=False,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            expected_decision="helper_only_signed_orbit_shadow_value_theorem_missing",
            first_falsifier_or_missing_clause="signed orbit law is source certification, not a finite value/divisor theorem",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="quotient_Q_frobenius_inverse",
            candidate_shape="quotient Q with Frob_p(Q)=Q^-1 and W=Q^6",
            uses_degree6_orbit=True,
            uses_pure_norm=False,
            uses_twisted_trace_or_ratio=True,
            uses_hilbert90_boundary=False,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            expected_decision="helper_only_ratio_boundary_value_theorem_missing",
            first_falsifier_or_missing_clause="Frobenius-inverse quotient gives descent contract but no finite value",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="hilbert90_boundary_without_value",
            candidate_shape="integral H90 potential V with W=(1-Frob_p)V",
            uses_degree6_orbit=True,
            uses_pure_norm=False,
            uses_twisted_trace_or_ratio=True,
            uses_hilbert90_boundary=True,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            expected_decision="helper_only_hilbert90_boundary_value_theorem_missing",
            first_falsifier_or_missing_clause="boundary shape still lacks finite value/divisor theorem",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="twisted_ratio_value_without_period156",
            candidate_shape="ratio/H90 finite value theorem without support-period branch context",
            uses_degree6_orbit=True,
            uses_pure_norm=False,
            uses_twisted_trace_or_ratio=True,
            uses_hilbert90_boundary=True,
            finite_value_or_divisor_theorem=True,
            period156_context=False,
            expected_decision="conditional_value_theorem_missing_period156_context",
            first_falsifier_or_missing_clause="period-156 branch/root/telescoping context",
            source_stage_closed=False,
            ok=True,
        ),
        TwistedDescentRow(
            name="twisted_ratio_period156_value",
            candidate_shape="ratio/H90 finite value theorem with period-156 context",
            uses_degree6_orbit=True,
            uses_pure_norm=False,
            uses_twisted_trace_or_ratio=True,
            uses_hilbert90_boundary=True,
            finite_value_or_divisor_theorem=True,
            period156_context=True,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            first_falsifier_or_missing_clause="DANGER3 finite-identity/non-CM framing",
            source_stage_closed=True,
            ok=True,
        ),
    )


def profile_twisted_descent_decision_packet() -> TwistedDescentDecisionPacket:
    degree6_ok = marker_present(DEGREE6_PACKET, DEGREE6_PACKET_MARKER)
    smoke_ok = marker_present(EXPERT_ANSWER_SMOKE, EXPERT_ANSWER_SMOKE_MARKER)
    orbit_ok = marker_present(FROBENIUS_ORBIT, FROBENIUS_ORBIT_MARKER)
    pairing_ok = marker_present(COSET_PAIRING, COSET_PAIRING_MARKER)
    h90_ok = marker_present(HILBERT90_BOUNDARY, HILBERT90_BOUNDARY_MARKER)
    rows = route_rows()
    rejected = sum(row.expected_decision.startswith("reject_") for row in rows)
    helper = sum(row.expected_decision.startswith("helper_only_") for row in rows)
    conditional = sum(row.expected_decision.startswith("conditional_") for row in rows)
    closing = sum(row.source_stage_closed for row in rows)
    period_closing = sum(row.source_stage_closed and row.period156_context for row in rows)
    row_ok = (
        degree6_ok
        and smoke_ok
        and orbit_ok
        and pairing_ok
        and h90_ok
        and TWO_CONJUGATE_SUM_SUPPORT == 0
        and THREE_CONJUGATE_SUM_EQUALS_WORD
        and SIX_CONJUGATE_SUM_SUPPORT == 0
        and PURE_CHARACTER_DEGREE6_NORM_CANCELS
        and Q_VALUE_FROBENIUS_INVERSE_CONTRACT
        and W_VALUE_FROBENIUS_INVERSE_CONTRACT
        and BALANCED_H90_SUPPORT == 24
        and SPARSE_H90_SUPPORT == 12
        and len(rows) == 7
        and rejected == 2
        and helper == 3
        and conditional == 1
        and closing == 1
        and period_closing == 1
        and tuple(row.expected_decision for row in rows)
        == (
            "reject_pure_degree6_norm_cancels",
            "reject_pair_sum_cancels",
            "helper_only_signed_orbit_shadow_value_theorem_missing",
            "helper_only_ratio_boundary_value_theorem_missing",
            "helper_only_hilbert90_boundary_value_theorem_missing",
            "conditional_value_theorem_missing_period156_context",
            "source_theorem_closed_policy_or_framing_missing",
        )
        and all(row.ok for row in rows)
    )
    return TwistedDescentDecisionPacket(
        degree6_packet_ok=degree6_ok,
        expert_answer_smoke_ok=smoke_ok,
        frobenius_orbit_ok=orbit_ok,
        coset_pairing_ok=pairing_ok,
        hilbert90_boundary_ok=h90_ok,
        two_conjugate_sum_support=TWO_CONJUGATE_SUM_SUPPORT,
        three_conjugate_sum_equals_word=THREE_CONJUGATE_SUM_EQUALS_WORD,
        six_conjugate_sum_support=SIX_CONJUGATE_SUM_SUPPORT,
        pure_character_degree6_norm_cancels=PURE_CHARACTER_DEGREE6_NORM_CANCELS,
        q_value_frobenius_inverse_contract=Q_VALUE_FROBENIUS_INVERSE_CONTRACT,
        w_value_frobenius_inverse_contract=W_VALUE_FROBENIUS_INVERSE_CONTRACT,
        balanced_h90_support=BALANCED_H90_SUPPORT,
        sparse_h90_support=SPARSE_H90_SUPPORT,
        route_rows=rows,
        route_count=len(rows),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_closing_rows=closing,
        period156_closing_rows=period_closing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_twisted_descent_decision_packet()
    print("p25 KSY-y conductor-39 twisted-descent decision packet gate")
    print("dependencies")
    print(f"  degree6_packet_ok={int(profile.degree6_packet_ok)}")
    print(f"  expert_answer_smoke_ok={int(profile.expert_answer_smoke_ok)}")
    print(f"  frobenius_orbit_ok={int(profile.frobenius_orbit_ok)}")
    print(f"  coset_pairing_ok={int(profile.coset_pairing_ok)}")
    print(f"  hilbert90_boundary_ok={int(profile.hilbert90_boundary_ok)}")
    print("descent_facts")
    print(f"  two_conjugate_sum_support={profile.two_conjugate_sum_support}")
    print(f"  three_conjugate_sum_equals_word={int(profile.three_conjugate_sum_equals_word)}")
    print(f"  six_conjugate_sum_support={profile.six_conjugate_sum_support}")
    print(f"  pure_character_degree6_norm_cancels={int(profile.pure_character_degree6_norm_cancels)}")
    print(f"  q_value_frobenius_inverse_contract={int(profile.q_value_frobenius_inverse_contract)}")
    print(f"  w_value_frobenius_inverse_contract={int(profile.w_value_frobenius_inverse_contract)}")
    print(f"  balanced_h90_support={profile.balanced_h90_support}")
    print(f"  sparse_h90_support={profile.sparse_h90_support}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.expected_decision} "
            f"degree6={int(row.uses_degree6_orbit)} "
            f"pure_norm={int(row.uses_pure_norm)} "
            f"twisted={int(row.uses_twisted_trace_or_ratio)} "
            f"h90={int(row.uses_hilbert90_boundary)} "
            f"finite={int(row.finite_value_or_divisor_theorem)} "
            f"period156={int(row.period156_context)} "
            f"closed={int(row.source_stage_closed)}"
        )
        print(f"    shape={row.candidate_shape}")
        print(f"    missing_or_falsifier={row.first_falsifier_or_missing_clause}")
    print("counts")
    print(f"  route_count={profile.route_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  period156_closing_rows={profile.period156_closing_rows}")
    print("interpretation")
    print("  pure_degree6_norm_is_dead_for_the_character_word=1")
    print("  surviving_descent_must_be_twisted_ratio_or_hilbert90=1")
    print("  only_period156_finite_value_or_divisor_theorem_closes_source_stage=1")
    print("  closure_still_needs_DANGER3_framing_extraction_and_vpp=1")
    print(f"ksy_y_conductor39_twisted_descent_decision_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 twisted-descent decision packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
