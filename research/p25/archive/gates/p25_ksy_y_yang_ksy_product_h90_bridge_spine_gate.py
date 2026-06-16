#!/usr/bin/env python3
"""Bridge spine from KSY atoms to the sparse Yang Hilbert-90 product.

This gate prevents two opposite mistakes:

* treating the 75 normalized-y atoms as 75 independent search candidates;
* treating the canonical 78-over-78 Hilbert-90 product as an unrelated target.

The verified bridge is a one-way spine:

    75 fixed atoms -> 300 Siegel terms -> 12-term Y_507
    -> 312-cell period norm -> 156-cell Hilbert-90 potential.

The last object is a theorem/value target downstream of the same KSY/Yang
source, not a brute-force shortlist.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_atom_terminology_guardrail_gate import (
    profile_atom_terminology_guardrail,
)
from p25_ksy_y_yang_quotient_normalized_y_descent_gate import (
    profile_yang_quotient_normalized_y_descent,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    profile_normalized_y_product_source_law,
)


@dataclass(frozen=True)
class BridgeStage:
    name: str
    input_count: int
    output_count: int
    verified_payload: str
    still_missing: str
    ok: bool


@dataclass(frozen=True)
class KsyYangH90BridgeSpine:
    atom_count: int
    raw_siegel_term_count: int
    quotient_y507_support: int
    period_norm_support: int
    h90_potential_support: int
    h90_positive_factor_count: int
    h90_negative_factor_count: int
    legal_h90_product_orbit_count: int
    legal_h90_product_stabilizer_size: int
    stages: tuple[BridgeStage, ...]
    u_primitive_word: tuple[tuple[int, int], ...]
    y507_primitive_word: tuple[tuple[int, int], ...]
    canonical_h90_positive_residues_mod39: tuple[int, ...]
    canonical_h90_negative_residues_mod39: tuple[int, ...]
    atoms_are_independent_search_candidates: bool
    h90_is_plain_75_atom_product: bool
    ksy_to_yang_descent_ok: bool
    period_norm_distribution_ok: bool
    h90_boundary_ok: bool
    direct_closer: bool
    recommendation: str
    row_ok: bool


def profile_ksy_yang_h90_bridge_spine() -> KsyYangH90BridgeSpine:
    atoms = profile_atom_terminology_guardrail()
    source_law = profile_normalized_y_product_source_law()
    descent = profile_yang_quotient_normalized_y_descent()
    primitive = profile_yang_y507_primitive_factor_word()
    distribution = profile_yang_y507_conductor39_distribution_lift()
    h90 = profile_sparse_h90_product_normal_form()
    canonical_h90 = h90.legal_rows[0]

    atom_count = atoms.atom_count
    raw_count = descent.raw_footprint_support
    quotient_count = descent.quotient_footprint_support
    period_norm_count = distribution.period_norm_support
    h90_support = canonical_h90.lifted_support
    h90_positive = canonical_h90.lifted_positive_count
    h90_negative = canonical_h90.lifted_negative_count

    atoms_are_search = atoms.atoms_are_search_candidates
    h90_is_plain_75 = (
        h90_support == atom_count
        or h90_positive == atom_count
        or h90_negative == atom_count
    )

    stages = (
        BridgeStage(
            name="fixed_atoms_to_raw_siegel_footprint",
            input_count=atom_count,
            output_count=raw_count,
            verified_payload=(
                "75 fixed normalized-y atoms expand by y(Q)=-g(2Q)/g(Q)^4 "
                "to the 300-term theta2 footprint"
            ),
            still_missing="arithmetic theorem selecting the whole fixed product",
            ok=(
                atoms.row_ok
                and source_law.row_ok
                and atom_count == 75
                and raw_count == 300
                and source_law.target_support == 300
            ),
        ),
        BridgeStage(
            name="raw_footprint_to_quotient_y507",
            input_count=raw_count,
            output_count=quotient_count,
            verified_payload=(
                "the raw K-trace footprint is constant on 25-cycles and "
                "descends to Y_507=[2]^*U_507/U_507^4"
            ),
            still_missing="finite-field value/divisor theorem for Y_507",
            ok=(
                descent.row_ok
                and primitive.row_ok
                and raw_count == 300
                and quotient_count == 12
                and descent.all_raw_orbits_constant
                and descent.quotient_equals_doubled_u_over_u4
                and primitive.y507_equals_doubled_u_minus_four_u
            ),
        ),
        BridgeStage(
            name="quotient_y507_to_period_norm_character",
            input_count=quotient_count,
            output_count=period_norm_count,
            verified_payload=(
                "Norm_156(Y_507) is the 13-fiber Yang distribution lift of "
                "the conductor-39 quadratic character source"
            ),
            still_missing="value-side theorem explaining the period norm in F_p",
            ok=(
                distribution.row_ok
                and quotient_count == 12
                and period_norm_count == 312
                and distribution.lifted_equals_period_norm
                and distribution.period_norm_equals_six_lifted_primitive
            ),
        ),
        BridgeStage(
            name="period_norm_to_sparse_hilbert90_product",
            input_count=period_norm_count,
            output_count=h90_support,
            verified_payload=(
                "a legal sparse Hilbert-90 preimage is a canonical 78-over-78 "
                "Yang-fiber product, up to the conductor-39 doubling orbit"
            ),
            still_missing="finite-field value/divisor identity and DANGER3 extraction",
            ok=(
                h90.row_ok
                and period_norm_count == 312
                and h90_support == 156
                and h90_positive == 78
                and h90_negative == 78
                and canonical_h90.boundary_equals_period_norm
                and h90.legal_rows_form_one_doubling_orbit
            ),
        ),
    )

    direct_closer = False
    row_ok = (
        all(stage.ok for stage in stages)
        and atoms.row_ok
        and source_law.row_ok
        and descent.row_ok
        and primitive.row_ok
        and distribution.row_ok
        and h90.row_ok
        and primitive.u_primitive_word
        == (
            (121, 1),
            (122, 1),
            (123, 1),
            (384, -1),
            (385, -1),
            (386, -1),
        )
        and primitive.y507_primitive_word
        == (
            (121, -4),
            (122, -4),
            (123, -4),
            (242, 1),
            (244, 1),
            (246, 1),
            (261, -1),
            (263, -1),
            (265, -1),
            (384, 4),
            (385, 4),
            (386, 4),
        )
        and h90.canonical_positive_residues == (7, 17, 23, 34, 37, 38)
        and h90.canonical_negative_residues == (4, 8, 10, 11, 20, 25)
        and len(h90.legal_rows) == 4
        and len(h90.canonical_stabilizer) == 3
        and not atoms_are_search
        and not h90_is_plain_75
        and not direct_closer
    )

    return KsyYangH90BridgeSpine(
        atom_count=atom_count,
        raw_siegel_term_count=raw_count,
        quotient_y507_support=quotient_count,
        period_norm_support=period_norm_count,
        h90_potential_support=h90_support,
        h90_positive_factor_count=h90_positive,
        h90_negative_factor_count=h90_negative,
        legal_h90_product_orbit_count=len(h90.legal_rows),
        legal_h90_product_stabilizer_size=len(h90.canonical_stabilizer),
        stages=stages,
        u_primitive_word=primitive.u_primitive_word,
        y507_primitive_word=primitive.y507_primitive_word,
        canonical_h90_positive_residues_mod39=h90.canonical_positive_residues,
        canonical_h90_negative_residues_mod39=h90.canonical_negative_residues,
        atoms_are_independent_search_candidates=atoms_are_search,
        h90_is_plain_75_atom_product=h90_is_plain_75,
        ksy_to_yang_descent_ok=descent.row_ok and primitive.row_ok,
        period_norm_distribution_ok=distribution.row_ok,
        h90_boundary_ok=canonical_h90.boundary_equals_period_norm,
        direct_closer=direct_closer,
        recommendation=(
            "treat the moonshot as one structured theorem/value spine: exact "
            "KSY product or Y_507/Hilbert-90 value identity, then DANGER3 "
            "framing and extraction; do not split the 75 atoms into candidate "
            "tries or identify the 78-over-78 product as a bare 75-atom object"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_ksy_yang_h90_bridge_spine()
    print("p25 KSY-y Yang/H90 bridge-spine gate")
    print("counts")
    print(f"  atom_count={profile.atom_count}")
    print(f"  raw_siegel_term_count={profile.raw_siegel_term_count}")
    print(f"  quotient_y507_support={profile.quotient_y507_support}")
    print(f"  period_norm_support={profile.period_norm_support}")
    print(f"  h90_potential_support={profile.h90_potential_support}")
    print(f"  h90_positive_factor_count={profile.h90_positive_factor_count}")
    print(f"  h90_negative_factor_count={profile.h90_negative_factor_count}")
    print(f"  legal_h90_product_orbit_count={profile.legal_h90_product_orbit_count}")
    print(f"  legal_h90_product_stabilizer_size={profile.legal_h90_product_stabilizer_size}")
    print("stages")
    for stage in profile.stages:
        print(
            "  "
            f"{stage.name}: {stage.input_count}->{stage.output_count} "
            f"ok={int(stage.ok)}"
        )
        print(f"    payload={stage.verified_payload}")
        print(f"    missing={stage.still_missing}")
    print("primitive_words")
    print(f"  U_507={profile.u_primitive_word}")
    print(f"  Y_507={profile.y507_primitive_word}")
    print("canonical_h90")
    print(f"  positive_residues_mod39={profile.canonical_h90_positive_residues_mod39}")
    print(f"  negative_residues_mod39={profile.canonical_h90_negative_residues_mod39}")
    print("checks")
    print(
        "  atoms_are_independent_search_candidates="
        f"{int(profile.atoms_are_independent_search_candidates)}"
    )
    print(f"  h90_is_plain_75_atom_product={int(profile.h90_is_plain_75_atom_product)}")
    print(f"  ksy_to_yang_descent_ok={int(profile.ksy_to_yang_descent_ok)}")
    print(f"  period_norm_distribution_ok={int(profile.period_norm_distribution_ok)}")
    print(f"  h90_boundary_ok={int(profile.h90_boundary_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  count_ladder_is_75_to_300_to_12_to_312_to_156=1")
    print("  seventy_five_atoms_are_fixed_factors_not_candidate_tries=1")
    print("  canonical_78_over_78_product_is_hilbert90_preimage_not_competing_search=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(f"ksy_y_yang_ksy_product_h90_bridge_spine_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("KSY-y Yang/H90 bridge-spine regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
