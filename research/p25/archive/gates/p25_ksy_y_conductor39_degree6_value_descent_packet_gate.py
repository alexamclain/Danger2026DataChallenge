#!/usr/bin/env python3
"""Degree-6 value-descent packet for the conductor-39 source route.

The minimal theorem query says what source theorem would close the
conductor-39 stage.  This gate sharpens the value side: a candidate cannot use
a direct F_p order-39 root or sqrt(-39) scalar shortcut.  It must either work
over the degree-6 cyclotomic orbit and descend by conjugates/norms, or provide
an explicit Hilbert-90/ratio boundary whose finite value is period-156
compatible.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_conductor39_minimal_theorem_query_packet_gate import (
    profile_minimal_theorem_query_packet,
)
from p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_gate import (
    profile_yang_y507_conductor39_coset_frobenius_pairing,
)
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import (
    profile_yang_y507_conductor39_frobenius_contract,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    profile_yang_y507_conductor39_hilbert90_boundary,
)


@dataclass(frozen=True)
class Degree6ValueDescentRow:
    name: str
    candidate_shape: str
    uses_direct_fp_order39_root: bool
    uses_sqrt_minus39_in_fp: bool
    has_degree6_cyclotomic_orbit: bool
    has_conjugate_or_norm_descent_to_fp: bool
    has_hilbert90_or_ratio_boundary: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    expected_decision: str
    source_theorem_closes: bool
    first_missing_clause: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class Conductor39Degree6ValueDescentPacket:
    minimal_query_ok: bool
    frobenius_contract_ok: bool
    coset_pairing_ok: bool
    hilbert90_boundary_ok: bool
    p_order_mod39: int
    p_cubed_is_minus_one_mod39: bool
    primitive_39_roots_first_in_degree_6: bool
    discriminant_is_nonsquare_mod_p: bool
    q_value_frobenius_inverse_contract: bool
    w_value_frobenius_inverse_contract: bool
    balanced_h90_support: int
    sparse_h90_support: int
    route_rows: tuple[Degree6ValueDescentRow, ...]
    route_count: int
    rejected_shortcut_rows: int
    conditional_rows: int
    helper_only_rows: int
    source_theorem_closing_rows: int
    period156_closing_rows: int
    row_ok: bool


def classify_row(
    name: str,
    candidate_shape: str,
    *,
    direct_root: bool = False,
    sqrt_minus39: bool = False,
    degree6: bool = False,
    norm_descent: bool = False,
    h90_boundary: bool = False,
    finite_theorem: bool = False,
    period156: bool = False,
    first_falsifier: str,
) -> Degree6ValueDescentRow:
    if direct_root:
        decision = "reject_direct_Fp_order39_root_shortcut"
        closes = False
        missing = "primitive 39th roots first occur over degree 6"
    elif sqrt_minus39:
        decision = "reject_sqrt_minus39_scalar_shortcut"
        closes = False
        missing = "sqrt(-39) is not in F_p"
    elif not degree6 and not h90_boundary:
        decision = "conditional_missing_degree6_or_hilbert90_descent"
        closes = False
        missing = "degree-6 cyclotomic orbit, conjugate/norm descent, or Hilbert-90 boundary"
    elif degree6 and not norm_descent and not h90_boundary:
        decision = "conditional_degree6_orbit_without_descent_to_Fp"
        closes = False
        missing = "conjugate/norm descent back to F_p"
    elif h90_boundary and not finite_theorem:
        decision = "helper_only_hilbert90_boundary_value_theorem_missing"
        closes = False
        missing = "finite-field value identity or divisor/additive theorem for the boundary"
    elif finite_theorem and not period156:
        decision = "conditional_value_theorem_missing_period156_context"
        closes = False
        missing = "period-156 branch/root/telescoping context"
    else:
        decision = "source_theorem_closed_policy_or_framing_missing"
        closes = True
        missing = "DANGER3 finite-identity/non-CM framing"

    return Degree6ValueDescentRow(
        name=name,
        candidate_shape=candidate_shape,
        uses_direct_fp_order39_root=direct_root,
        uses_sqrt_minus39_in_fp=sqrt_minus39,
        has_degree6_cyclotomic_orbit=degree6,
        has_conjugate_or_norm_descent_to_fp=norm_descent,
        has_hilbert90_or_ratio_boundary=h90_boundary,
        finite_value_or_divisor_theorem=finite_theorem,
        period156_context=period156,
        expected_decision=decision,
        source_theorem_closes=closes,
        first_missing_clause=missing,
        first_falsifier=first_falsifier,
        ok=True,
    )


def route_rows() -> tuple[Degree6ValueDescentRow, ...]:
    return (
        classify_row(
            "direct_fp_order39_root",
            "theorem evaluates U_chi using a primitive 39th root inside F_p",
            direct_root=True,
            first_falsifier="ord_39(p)=6, so no primitive order-39 root lies in F_p",
        ),
        classify_row(
            "sqrt_minus39_scalar",
            "theorem collapses the mixed character using sqrt(-39) in F_p",
            sqrt_minus39=True,
            first_falsifier="(-39/p)=-1",
        ),
        classify_row(
            "degree6_orbit_no_descent",
            "theorem computes over F_{p^6} but does not descend the conjugates",
            degree6=True,
            first_falsifier="degree-6 computation has no norm/trace/product statement back in F_p",
        ),
        classify_row(
            "hilbert90_boundary_no_value",
            "theorem identifies Q with Frob_p(Q)=Q^-1 or W=(1-Frob_p)V but no value",
            h90_boundary=True,
            first_falsifier="boundary shape is only source certification unless a finite value/divisor identity is proved",
        ),
        classify_row(
            "degree6_norm_descent_bare_value",
            "theorem descends a degree-6 cyclotomic value but omits period-156 branch context",
            degree6=True,
            norm_descent=True,
            finite_theorem=True,
            first_falsifier="bare finite value has no support-period branch/root/telescoping context",
        ),
        classify_row(
            "degree6_norm_descent_period156_value",
            "theorem descends the degree-6 value and supplies period-156 context",
            degree6=True,
            norm_descent=True,
            finite_theorem=True,
            period156=True,
            first_falsifier="DANGER3 finite-identity/non-CM framing still absent",
        ),
        classify_row(
            "hilbert90_ratio_period156_value",
            "theorem gives a Hilbert-90/ratio value identity with period-156 context",
            h90_boundary=True,
            finite_theorem=True,
            period156=True,
            first_falsifier="DANGER3 finite-identity/non-CM framing still absent",
        ),
    )


def profile_degree6_value_descent_packet() -> Conductor39Degree6ValueDescentPacket:
    query = profile_minimal_theorem_query_packet()
    frob = profile_yang_y507_conductor39_frobenius_contract()
    pairing = profile_yang_y507_conductor39_coset_frobenius_pairing()
    h90 = profile_yang_y507_conductor39_hilbert90_boundary()
    rows = route_rows()
    rejected = sum(row.expected_decision.startswith("reject_") for row in rows)
    conditional = sum(row.expected_decision.startswith("conditional_") for row in rows)
    helper = sum(row.expected_decision.startswith("helper_only_") for row in rows)
    closing = sum(row.source_theorem_closes for row in rows)
    period_closing = sum(row.source_theorem_closes and row.period156_context for row in rows)
    row_ok = (
        query.row_ok
        and frob.row_ok
        and pairing.row_ok
        and h90.row_ok
        and frob.p_order_mod_39 == 6
        and frob.p_cubed_is_minus_one_mod_39
        and frob.primitive_39_roots_first_in_degree_6
        and frob.discriminant_is_nonsquare_mod_p
        and pairing.q_value_frobenius_inverse_contract
        and pairing.w_value_frobenius_inverse_contract
        and h90.balanced_support == 24
        and h90.sparse_support == 12
        and len(rows) == 7
        and rejected == 2
        and conditional == 2
        and helper == 1
        and closing == 2
        and period_closing == 2
        and tuple(row.expected_decision for row in rows)
        == (
            "reject_direct_Fp_order39_root_shortcut",
            "reject_sqrt_minus39_scalar_shortcut",
            "conditional_degree6_orbit_without_descent_to_Fp",
            "helper_only_hilbert90_boundary_value_theorem_missing",
            "conditional_value_theorem_missing_period156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
        )
        and all(row.ok for row in rows)
    )
    return Conductor39Degree6ValueDescentPacket(
        minimal_query_ok=query.row_ok,
        frobenius_contract_ok=frob.row_ok,
        coset_pairing_ok=pairing.row_ok,
        hilbert90_boundary_ok=h90.row_ok,
        p_order_mod39=frob.p_order_mod_39,
        p_cubed_is_minus_one_mod39=frob.p_cubed_is_minus_one_mod_39,
        primitive_39_roots_first_in_degree_6=frob.primitive_39_roots_first_in_degree_6,
        discriminant_is_nonsquare_mod_p=frob.discriminant_is_nonsquare_mod_p,
        q_value_frobenius_inverse_contract=pairing.q_value_frobenius_inverse_contract,
        w_value_frobenius_inverse_contract=pairing.w_value_frobenius_inverse_contract,
        balanced_h90_support=h90.balanced_support,
        sparse_h90_support=h90.sparse_support,
        route_rows=rows,
        route_count=len(rows),
        rejected_shortcut_rows=rejected,
        conditional_rows=conditional,
        helper_only_rows=helper,
        source_theorem_closing_rows=closing,
        period156_closing_rows=period_closing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_degree6_value_descent_packet()
    print("p25 KSY-y conductor-39 degree-6 value-descent packet gate")
    print("dependencies")
    print(f"  minimal_query_ok={int(profile.minimal_query_ok)}")
    print(f"  frobenius_contract_ok={int(profile.frobenius_contract_ok)}")
    print(f"  coset_pairing_ok={int(profile.coset_pairing_ok)}")
    print(f"  hilbert90_boundary_ok={int(profile.hilbert90_boundary_ok)}")
    print("arithmetic")
    print(f"  p_order_mod39={profile.p_order_mod39}")
    print(f"  p_cubed_is_minus_one_mod39={int(profile.p_cubed_is_minus_one_mod39)}")
    print(
        "  primitive_39_roots_first_in_degree_6="
        f"{int(profile.primitive_39_roots_first_in_degree_6)}"
    )
    print(f"  discriminant_is_nonsquare_mod_p={int(profile.discriminant_is_nonsquare_mod_p)}")
    print(f"  q_value_frobenius_inverse_contract={int(profile.q_value_frobenius_inverse_contract)}")
    print(f"  w_value_frobenius_inverse_contract={int(profile.w_value_frobenius_inverse_contract)}")
    print(f"  balanced_h90_support={profile.balanced_h90_support}")
    print(f"  sparse_h90_support={profile.sparse_h90_support}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.expected_decision} "
            f"degree6={int(row.has_degree6_cyclotomic_orbit)} "
            f"norm_descent={int(row.has_conjugate_or_norm_descent_to_fp)} "
            f"h90={int(row.has_hilbert90_or_ratio_boundary)} "
            f"finite={int(row.finite_value_or_divisor_theorem)} "
            f"period156={int(row.period156_context)} "
            f"closes={int(row.source_theorem_closes)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    shape={row.candidate_shape}")
        print(f"    falsifier={row.first_falsifier}")
    print("counts")
    print(f"  route_count={profile.route_count}")
    print(f"  rejected_shortcut_rows={profile.rejected_shortcut_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  period156_closing_rows={profile.period156_closing_rows}")
    print("interpretation")
    print("  value_theorem_must_use_degree6_or_hilbert90_descent_not_Fp_shortcut=1")
    print("  degree6_orbit_alone_is_not_enough_without_norm_descent_to_Fp=1")
    print("  period156_context_is_required_for_value_level_source_closure=1")
    print("  closing_value_descent_still_needs_DANGER3_framing_extraction_and_vpp=1")
    print(f"ksy_y_conductor39_degree6_value_descent_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 degree-6 value-descent packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
