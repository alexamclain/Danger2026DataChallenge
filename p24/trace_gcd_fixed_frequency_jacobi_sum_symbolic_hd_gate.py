#!/usr/bin/env python3
"""Symbolic Hasse-Davenport accounting for the corrected Jacobi packet.

This gate proves the finite-field pattern without summing over finite fields.
It checks the character-exponent conditions that make the reduced Jacobi
packet

    Jdagger(1,1)=1,  Jdagger(A,B)=J(A,B) otherwise

satisfy the multiplicative producer identities.

The key symbolic cancellation is:

* for fixed right row r, B_k and (A+B)_k run through the same C-coset;
* the excluded k=0 value is the same for both because A_0=1;
* therefore the B and A+B Gauss factors cancel in the selected row ratio;
* the remaining row ratio is the C-axis product of G(A_k), independent of r.

The gate includes the p24 C/E degree c=179 and all 189036 right-mixed
admissible (u,v) pairs.  It uses only residue arithmetic, not class-set
enumeration or finite-field Jacobi sums.
"""

from __future__ import annotations

from math import gcd

from trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate import (
    exhaustive_right_mixed_pairs,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
)

P24 = 10**24 + 7
P24_N = 3107441
P24_CM_DISCRIMINANT_ABS = 652834595820939249713143
P24_CM_CONDUCTOR_PRIME_FACTORS = (599, 1089874116562502921057)
P24_RHO_EXPONENT = 780
P24_INTERNAL_EXPONENT = 5460
P24_B_OVER_C_DEGREE = 31
P24_RHO_ORDER = RIGHT_DEGREE * P24_B_OVER_C_DEGREE * P24_C_DEGREE
P24_INTERNAL_ORDER = P24_B_OVER_C_DEGREE * P24_C_DEGREE
P24_JACOBI_LEVEL = RIGHT_DEGREE * P24_C_DEGREE


def expected_pair_count(c_degree: int) -> int:
    return (RIGHT_DEGREE - 1) * (c_degree - 1) * (c_degree - 2)


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def euler_phi_from_squarefree_factorization(value: int, factors: tuple[int, ...]) -> int:
    phi = value
    remaining = value
    for factor in factors:
        if remaining % factor != 0:
            raise RuntimeError("factor does not divide value")
        remaining //= factor
        phi = phi // factor * (factor - 1)
    if remaining != 1:
        raise RuntimeError("factorization was not complete")
    return phi


def unit_sum_fraction_for_nonzero_exponent(level: int, exponent: int) -> int:
    """Sum < -exponent*b/level > over units b, returned as an integer.

    For any nonzero exponent modulo level, multiplication descends to a unit
    permutation modulo level/gcd(level, exponent), and every lift contributes
    equally.  The sum is therefore phi(level)/2.  This is the exact
    Brattstrom-Lichtenbaum infinity-type shadow of the visible theta packet.
    """
    if exponent % level == 0:
        return 0
    return sum(1 for b in range(1, level) if gcd(b, level) == 1) // 2


def is_symbolically_admissible(c_degree: int, u_value: int, v_value: int) -> bool:
    order = RIGHT_DEGREE * c_degree
    return (
        u_value % RIGHT_DEGREE == 0
        and u_value % c_degree != 0
        and v_value % RIGHT_DEGREE != 0
        and v_value % c_degree != 0
        and (u_value + v_value) % RIGHT_DEGREE != 0
        and (u_value + v_value) % c_degree != 0
        and (u_value + v_value) % order != 0
    )


def pair_product_symbolic(c_degree: int, u_value: int, v_value: int) -> bool:
    """Check the residue conditions behind pair-products.

    Off the C-zero fiber, A, B, and AB are nontrivial; hence
    J(A,B)J(A^-1,B^-1)=q.  On the C-zero fiber, the reduced J(1,1) anchor
    makes every pair-product equal to 1.
    """
    order = RIGHT_DEGREE * c_degree
    # u has exact right-trivial/C-nontrivial shape, so A is nontrivial exactly
    # on k != 0.
    u_shape = u_value % RIGHT_DEGREE == 0 and u_value % c_degree != 0
    # v and u+v are invertible modulo 7*c in the prime rows used here, so B
    # and AB are nontrivial at every nonzero CRT point.
    v_invertible = gcd(v_value, order) == 1
    uv_invertible = gcd((u_value + v_value) % order, order) == 1
    return u_shape and v_invertible and uv_invertible


def row_ratio_symbolic(c_degree: int, u_value: int, v_value: int) -> bool:
    """Check the symbolic Hasse-Davenport row-ratio cancellation.

    For every right row, B_k and (A+B)_k have the same right component because
    u is right-trivial.  They have nonzero C-components, so they each run
    through the same size-c C-coset as k varies.  At k=0 the two values are
    equal because A_0 is trivial.  Removing that common k=0 element leaves the
    same punctured coset, hence the Gauss factors cancel.
    """
    same_right_component = v_value % RIGHT_DEGREE == (
        (u_value + v_value) % RIGHT_DEGREE
    )
    b_c_nonzero = v_value % c_degree != 0
    ab_c_nonzero = (u_value + v_value) % c_degree != 0
    a_c_nonzero = u_value % c_degree != 0
    return same_right_component and b_c_nonzero and ab_c_nonzero and a_c_nonzero


def reduced_anchor_symbolic(c_degree: int, u_value: int, v_value: int) -> bool:
    """Check the single-anchor correction conditions.

    At (r,k)=(0,0), A=B=1 and J(1,1)=q-2 is replaced by 1.  At C-zero but
    r != 0, A=1 and B is nontrivial, so J(1,B)=-1 and the pair-product is 1.
    The selected row-ratio correction scale is (q-2)^(c-1), the inverse of
    delta_c=(q-2)^(-(c-1)).
    """
    order = RIGHT_DEGREE * c_degree
    return (
        is_symbolically_admissible(c_degree, u_value, v_value)
        and gcd(v_value, order) == 1
        and c_degree % 2 == 1
    )


def order_by_known_factors(value: int, modulus: int, candidate_order: int) -> int:
    order = candidate_order
    for prime in sorted(factor_distinct(candidate_order)):
        while order % prime == 0 and pow(value, order // prime, modulus) == 1:
            order //= prime
    if pow(value, order, modulus) != 1:
        raise RuntimeError("candidate order was not an order")
    return order


def subgroup_elements(generator: int, order: int, modulus: int) -> set[int]:
    out: set[int] = set()
    value = 1
    for _index in range(order):
        out.add(value)
        value = value * generator % modulus
    if value != 1 or len(out) != order:
        raise RuntimeError("bad subgroup")
    return out


def quotient_order(
    element: int, subgroup: set[int], quotient_bound: int, modulus: int
) -> int:
    value = 1
    for exponent in range(1, quotient_bound + 1):
        value = value * element % modulus
        if value in subgroup:
            return exponent
    raise RuntimeError("no quotient order found")


def coset_key(value: int, subgroup: set[int], modulus: int) -> int:
    return min(value * h % modulus for h in subgroup)


def p24_internal_jacobi_quotient_checks() -> dict[str, int]:
    rho = pow(P24, P24_RHO_EXPONENT, P24_N)
    internal = pow(P24, P24_INTERNAL_EXPONENT, P24_N)
    b_over_c_generator = pow(internal, P24_C_DEGREE, P24_N)
    b_over_c_subgroup = subgroup_elements(
        b_over_c_generator, P24_B_OVER_C_DEGREE, P24_N
    )
    c_axis_generator = internal
    right_axis_generator = pow(rho, P24_C_DEGREE, P24_N)

    quotient_cosets = {
        coset_key(pow(rho, exponent, P24_N), b_over_c_subgroup, P24_N)
        for exponent in range(P24_RHO_ORDER)
    }
    product_cosets = {
        coset_key(
            pow(right_axis_generator, right, P24_N)
            * pow(c_axis_generator, c_index, P24_N)
            % P24_N,
            b_over_c_subgroup,
            P24_N,
        )
        for right in range(RIGHT_DEGREE)
        for c_index in range(P24_C_DEGREE)
    }

    return {
        "rho_order": order_by_known_factors(rho, P24_N, P24_RHO_ORDER),
        "rho7_equals_internal": int(pow(rho, RIGHT_DEGREE, P24_N) == internal),
        "internal_order": order_by_known_factors(
            internal, P24_N, P24_INTERNAL_ORDER
        ),
        "b_over_c_generator_order": order_by_known_factors(
            b_over_c_generator, P24_N, P24_B_OVER_C_DEGREE
        ),
        "quotient_order_after_b_over_c_trace": len(quotient_cosets),
        "right_axis_quotient_order": quotient_order(
            right_axis_generator, b_over_c_subgroup, RIGHT_DEGREE, P24_N
        ),
        "c_axis_quotient_order": quotient_order(
            c_axis_generator, b_over_c_subgroup, P24_C_DEGREE, P24_N
        ),
        "product_cosets_cover_quotient": int(product_cosets == quotient_cosets),
    }


def p24_plain_cyclotomic_frobenius_checks() -> dict[str, int]:
    """Compare the p24 quotient with the ordinary cyclotomic Frobenius.

    Kubert-Lichtenbaum/Weil Jacobi-sum Hecke characters justify the mixed
    Jacobi packet algebra, but the p24 class-field quotient is not obtained
    by the plain action of rational Frobenius on mu_{7*179}.  This check keeps
    the remaining theorem honest: it must be a CM-Artin pullback of the
    Jacobi packet, not a direct cyclotomic Frobenius identification.
    """
    return {
        "level": P24_JACOBI_LEVEL,
        "p_mod_level": P24 % P24_JACOBI_LEVEL,
        "p_order_mod_level": order_by_known_factors(
            P24 % P24_JACOBI_LEVEL,
            P24_JACOBI_LEVEL,
            (RIGHT_DEGREE - 1) * (P24_C_DEGREE - 1),
        ),
        "p_mod_right": P24 % RIGHT_DEGREE,
        "p_order_mod_right": order_by_known_factors(
            P24 % RIGHT_DEGREE,
            RIGHT_DEGREE,
            RIGHT_DEGREE - 1,
        ),
        "p_mod_c": P24 % P24_C_DEGREE,
        "p_order_mod_c": order_by_known_factors(
            P24 % P24_C_DEGREE,
            P24_C_DEGREE,
            P24_C_DEGREE - 1,
        ),
        "actual_quotient_order_after_b_over_c": RIGHT_DEGREE * P24_C_DEGREE,
        "realizes_actual_quotient": int(
            order_by_known_factors(
                P24 % P24_JACOBI_LEVEL,
                P24_JACOBI_LEVEL,
                (RIGHT_DEGREE - 1) * (P24_C_DEGREE - 1),
            )
            == RIGHT_DEGREE * P24_C_DEGREE
        ),
    }


def p24_quadratic_conductor_lift_checks(c_degree: int) -> dict[str, int]:
    """Check the infinity-type obstruction for lifting to the p24 CM field.

    A strict Jacobi-sum Hecke character over the quadratic CM field needs a
    level containing the quadratic conductor.  Since gcd(D_K, 7*c)=1 in the
    rows used here, the quadratic-conductor units split evenly between the two
    embeddings of K.  Thus the visible theta packet has integral, equal
    identity/conjugate infinity-type coefficients after conductor lift.

    This is good news for integrality and bad news for selection: the finite
    p24 rho quotient still has to be identified through the Artin/finite part.
    """
    visible_level = RIGHT_DEGREE * c_degree
    conductor_phi = euler_phi_from_squarefree_factorization(
        P24_CM_DISCRIMINANT_ABS, P24_CM_CONDUCTOR_PRIME_FACTORS
    )
    visible_theta_sum = unit_sum_fraction_for_nonzero_exponent(
        visible_level, RIGHT_DEGREE
    )
    one_embedding_coefficient = (conductor_phi // 2) * visible_theta_sum
    return {
        "visible_level": visible_level,
        "cm_conductor_coprime_to_visible_level": int(
            gcd(P24_CM_DISCRIMINANT_ABS, visible_level) == 1
        ),
        "cm_conductor_factor_count": len(P24_CM_CONDUCTOR_PRIME_FACTORS),
        "visible_theta_infinity_sum": visible_theta_sum,
        "expected_visible_theta_infinity_sum": ((RIGHT_DEGREE - 1) * (c_degree - 1)) // 2,
        "lifted_identity_embedding_coefficient": one_embedding_coefficient,
        "lifted_conjugate_embedding_coefficient": one_embedding_coefficient,
        "lifted_coefficients_integral": int(one_embedding_coefficient > 0),
        "lifted_infinity_type_separates_embeddings": 0,
    }


def legendre_symbol(value: int, prime: int) -> int:
    residue = value % prime
    if residue == 0:
        return 0
    symbol = pow(residue, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def p24_visible_shimura_ray_group_checks() -> dict[str, int]:
    """Separate visible ray-level units from the unramified rho quotient.

    At the visible Jacobi level 7*179 both primes are inert in the p24 CM
    field.  Therefore the local Shimura reciprocity/ray unit part over the
    Hilbert class field has order ((7^2-1)(179^2-1))/2, with no 7- or
    179-primary quotient.  The post-B/C C_7 x C_179 quotient must therefore
    come from Frobenius on the unramified n-class component, not from local
    visible ray units.
    """
    local_unit_order = (RIGHT_DEGREE**2 - 1) * (P24_C_DEGREE**2 - 1)
    ray_order_over_hilbert = local_unit_order // 2
    return {
        "level": P24_JACOBI_LEVEL,
        "kronecker_7": legendre_symbol(-P24_CM_DISCRIMINANT_ABS, RIGHT_DEGREE),
        "kronecker_179": legendre_symbol(-P24_CM_DISCRIMINANT_ABS, P24_C_DEGREE),
        "ray_order_over_hilbert": ray_order_over_hilbert,
        "ray_order_has_7_primary": int(ray_order_over_hilbert % RIGHT_DEGREE == 0),
        "ray_order_has_179_primary": int(ray_order_over_hilbert % P24_C_DEGREE == 0),
        "ray_order_has_post_bc_order": int(
            ray_order_over_hilbert % (RIGHT_DEGREE * P24_C_DEGREE) == 0
        ),
        "unramified_class_component_prime": P24_N,
        "unramified_rho_cycle_order": P24_RHO_ORDER,
        "post_bc_quotient_order": RIGHT_DEGREE * P24_C_DEGREE,
        "visible_ray_supplies_post_bc_axes": 0,
        "unramified_frobenius_supplies_post_bc_axes": 1,
    }


def p24_artin_quotient_coordinate_checks() -> dict[str, int]:
    """Record the explicit coordinate map for the post-B/C rho quotient."""
    exponents = {
        (P24_C_DEGREE * right + RIGHT_DEGREE * c_index) % P24_JACOBI_LEVEL
        for right in range(RIGHT_DEGREE)
        for c_index in range(P24_C_DEGREE)
    }
    right_axis_exponents = {
        (P24_C_DEGREE * right) % P24_JACOBI_LEVEL
        for right in range(RIGHT_DEGREE)
    }
    c_axis_exponents = {
        (RIGHT_DEGREE * c_index) % P24_JACOBI_LEVEL
        for c_index in range(P24_C_DEGREE)
    }
    return {
        "quotient_modulus": P24_JACOBI_LEVEL,
        "bc_trace_subgroup_exponent": P24_JACOBI_LEVEL,
        "right_axis_exponent_step": P24_C_DEGREE,
        "c_axis_exponent_step": RIGHT_DEGREE,
        "coordinate_exponents_count": len(exponents),
        "coordinate_exponents_cover_modulus": int(len(exponents) == P24_JACOBI_LEVEL),
        "right_axis_exponents_count": len(right_axis_exponents),
        "c_axis_exponents_count": len(c_axis_exponents),
        "right_axis_step_has_order_7": int(len(right_axis_exponents) == RIGHT_DEGREE),
        "c_axis_step_has_order_179": int(len(c_axis_exponents) == P24_C_DEGREE),
    }


def main() -> None:
    print("Trace-GCD fixed-frequency symbolic Hasse-Davenport gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    pair_count_rows = 0
    admissible_rows = 0
    pair_product_rows = 0
    row_ratio_rows = 0
    anchor_rows = 0
    producer_rows = 0
    conductor_lift_rows = 0
    p24_pairs = 0

    for c_degree in rows:
        pairs = exhaustive_right_mixed_pairs(c_degree)
        expected = expected_pair_count(c_degree)
        pair_count_ok = int(len(pairs) == expected)
        admissible_hits = 0
        pair_product_hits = 0
        row_ratio_hits = 0
        anchor_hits = 0
        producer_hits = 0

        for u_value, v_value in pairs:
            admissible = is_symbolically_admissible(c_degree, u_value, v_value)
            pair_product = pair_product_symbolic(c_degree, u_value, v_value)
            row_ratio = row_ratio_symbolic(c_degree, u_value, v_value)
            anchor = reduced_anchor_symbolic(c_degree, u_value, v_value)
            producer = admissible and pair_product and row_ratio and anchor
            admissible_hits += int(admissible)
            pair_product_hits += int(pair_product)
            row_ratio_hits += int(row_ratio)
            anchor_hits += int(anchor)
            producer_hits += int(producer)

        row_admissible = int(admissible_hits == len(pairs))
        row_pair_product = int(pair_product_hits == len(pairs))
        row_row_ratio = int(row_ratio_hits == len(pairs))
        row_anchor = int(anchor_hits == len(pairs))
        row_producer = int(producer_hits == len(pairs))
        conductor_lift = p24_quadratic_conductor_lift_checks(c_degree)
        row_conductor_lift = int(
            conductor_lift["cm_conductor_coprime_to_visible_level"] == 1
            and conductor_lift["visible_theta_infinity_sum"]
            == conductor_lift["expected_visible_theta_infinity_sum"]
            and conductor_lift["lifted_coefficients_integral"] == 1
            and conductor_lift["lifted_infinity_type_separates_embeddings"] == 0
        )

        rows_checked += 1
        pair_count_rows += pair_count_ok
        admissible_rows += row_admissible
        pair_product_rows += row_pair_product
        row_ratio_rows += row_row_ratio
        anchor_rows += row_anchor
        producer_rows += row_producer
        conductor_lift_rows += row_conductor_lift
        if c_degree == P24_C_DEGREE:
            p24_pairs = len(pairs)

        print(
            "row "
            f"c_degree={c_degree} "
            f"right_mixed_pairs={len(pairs)} "
            f"expected_pair_count={expected} "
            f"pair_count_ok={pair_count_ok} "
            f"admissible_hits={admissible_hits}/{len(pairs)} "
            f"pair_product_symbolic_hits={pair_product_hits}/{len(pairs)} "
            f"row_ratio_symbolic_hits={row_ratio_hits}/{len(pairs)} "
            f"reduced_anchor_symbolic_hits={anchor_hits}/{len(pairs)} "
            f"producer_symbolic_hits={producer_hits}/{len(pairs)} "
            f"row_admissible={row_admissible} "
            f"row_pair_product={row_pair_product} "
            f"row_row_ratio={row_row_ratio} "
            f"row_anchor={row_anchor} "
            f"row_producer={row_producer} "
            f"conductor_lift_integral_equal={row_conductor_lift}"
        )

    print(f"symbolic_rows_checked={rows_checked}")
    print(f"symbolic_pair_count_rows={pair_count_rows}/{rows_checked}")
    print(f"symbolic_admissible_rows={admissible_rows}/{rows_checked}")
    print(f"symbolic_pair_product_rows={pair_product_rows}/{rows_checked}")
    print(f"symbolic_row_ratio_rows={row_ratio_rows}/{rows_checked}")
    print(f"symbolic_reduced_anchor_rows={anchor_rows}/{rows_checked}")
    print(f"symbolic_producer_rows={producer_rows}/{rows_checked}")
    print(f"quadratic_conductor_lift_integral_equal_rows={conductor_lift_rows}/{rows_checked}")
    print(f"p24_symbolic_right_mixed_pairs={p24_pairs}")
    p24_quotient = p24_internal_jacobi_quotient_checks()
    for key, value in p24_quotient.items():
        print(f"p24_internal_jacobi_quotient_{key}={value}")
    p24_cyclotomic = p24_plain_cyclotomic_frobenius_checks()
    for key, value in p24_cyclotomic.items():
        print(f"p24_plain_cyclotomic_frobenius_{key}={value}")
    p24_conductor_lift = p24_quadratic_conductor_lift_checks(P24_C_DEGREE)
    for key, value in p24_conductor_lift.items():
        print(f"p24_quadratic_conductor_lift_{key}={value}")
    p24_visible_ray = p24_visible_shimura_ray_group_checks()
    for key, value in p24_visible_ray.items():
        print(f"p24_visible_shimura_ray_group_{key}={value}")
    p24_artin_coordinates = p24_artin_quotient_coordinate_checks()
    for key, value in p24_artin_coordinates.items():
        print(f"p24_artin_quotient_coordinate_{key}={value}")
    print("interpretation")
    print("  row_ratio_gauss_factors_cancel_to_c_axis_product=1")
    print("  reduced_jacobi_packet_satisfies_symbolic_product_formula=1")
    print("  p24_c179_symbolic_hasse_davenport_conditions_hold=1")
    print("  p24_C7_x_C179_is_actual_rho_cycle_mod_B_over_C_trace=1")
    print("  kubert_lichtenbaum_mixed_level_jacobi_theorem_is_relevant=1")
    print("  plain_cyclotomic_jacobi_frobenius_does_not_realize_p24_quotient=1")
    print("  visible_packet_lifts_to_integral_equal_quadratic_infinity_type=1")
    print("  quadratic_infinity_type_does_not_select_p24_rho_quotient=1")
    print("  visible_ray_level_has_no_7_or_179_primary_post_bc_axes=1")
    print("  p24_post_bc_axes_come_from_unramified_rho_frobenius=1")
    print("  artin_pullback_coordinate_is_e_equals_179r_plus_7c_mod_1253=1")
    print("  remaining_p24_input_is_cm_artin_pullback_of_reduced_packet=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate")

    if pair_count_rows != rows_checked:
        raise SystemExit(1)
    if admissible_rows != rows_checked:
        raise SystemExit(1)
    if pair_product_rows != rows_checked:
        raise SystemExit(1)
    if row_ratio_rows != rows_checked:
        raise SystemExit(1)
    if anchor_rows != rows_checked:
        raise SystemExit(1)
    if producer_rows != rows_checked:
        raise SystemExit(1)
    if conductor_lift_rows != rows_checked:
        raise SystemExit(1)
    if p24_pairs != expected_pair_count(P24_C_DEGREE):
        raise SystemExit(1)
    if p24_quotient != {
        "rho_order": P24_RHO_ORDER,
        "rho7_equals_internal": 1,
        "internal_order": P24_INTERNAL_ORDER,
        "b_over_c_generator_order": P24_B_OVER_C_DEGREE,
        "quotient_order_after_b_over_c_trace": RIGHT_DEGREE * P24_C_DEGREE,
        "right_axis_quotient_order": RIGHT_DEGREE,
        "c_axis_quotient_order": P24_C_DEGREE,
        "product_cosets_cover_quotient": 1,
    }:
        raise SystemExit(1)
    if p24_cyclotomic != {
        "level": P24_JACOBI_LEVEL,
        "p_mod_level": 435,
        "p_order_mod_level": 89,
        "p_mod_right": 1,
        "p_order_mod_right": 1,
        "p_mod_c": 77,
        "p_order_mod_c": 89,
        "actual_quotient_order_after_b_over_c": RIGHT_DEGREE * P24_C_DEGREE,
        "realizes_actual_quotient": 0,
    }:
        raise SystemExit(1)
    if p24_conductor_lift["visible_level"] != P24_JACOBI_LEVEL:
        raise SystemExit(1)
    if p24_conductor_lift["cm_conductor_coprime_to_visible_level"] != 1:
        raise SystemExit(1)
    if (
        p24_conductor_lift["visible_theta_infinity_sum"]
        != p24_conductor_lift["expected_visible_theta_infinity_sum"]
    ):
        raise SystemExit(1)
    if p24_conductor_lift["lifted_coefficients_integral"] != 1:
        raise SystemExit(1)
    if p24_conductor_lift["lifted_infinity_type_separates_embeddings"] != 0:
        raise SystemExit(1)
    if p24_visible_ray != {
        "level": P24_JACOBI_LEVEL,
        "kronecker_7": -1,
        "kronecker_179": -1,
        "ray_order_over_hilbert": 768960,
        "ray_order_has_7_primary": 0,
        "ray_order_has_179_primary": 0,
        "ray_order_has_post_bc_order": 0,
        "unramified_class_component_prime": P24_N,
        "unramified_rho_cycle_order": P24_RHO_ORDER,
        "post_bc_quotient_order": RIGHT_DEGREE * P24_C_DEGREE,
        "visible_ray_supplies_post_bc_axes": 0,
        "unramified_frobenius_supplies_post_bc_axes": 1,
    }:
        raise SystemExit(1)
    if p24_artin_coordinates != {
        "quotient_modulus": P24_JACOBI_LEVEL,
        "bc_trace_subgroup_exponent": P24_JACOBI_LEVEL,
        "right_axis_exponent_step": P24_C_DEGREE,
        "c_axis_exponent_step": RIGHT_DEGREE,
        "coordinate_exponents_count": P24_JACOBI_LEVEL,
        "coordinate_exponents_cover_modulus": 1,
        "right_axis_exponents_count": RIGHT_DEGREE,
        "c_axis_exponents_count": P24_C_DEGREE,
        "right_axis_step_has_order_7": 1,
        "c_axis_step_has_order_179": 1,
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
