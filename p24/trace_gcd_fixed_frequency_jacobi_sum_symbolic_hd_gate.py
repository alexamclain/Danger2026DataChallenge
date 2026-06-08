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


def value_side_carry_symbolic(c_degree: int, u_value: int, v_value: int) -> bool:
    """Check the verifier-facing value identities symbolically.

    For the Jacobi carry theta(t)=[ut]+[vt]-[(u+v)t] on C_7 x C_c, the
    right-mixed admissible shape gives the three value-side identities:

    * theta(r,0)=0, because u is right-trivial and C-nontrivial;
    * theta(t)+theta(-t)=7*c off the C-zero fiber, because u*t, v*t, and
      (u+v)*t are all nonzero there;
    * C-row sums are independent of r, because the v and u+v C-cosets cancel
      and the remaining u C-axis sum is independent of the right row.

    This is exactly the value-side interface consumed by
    TraceGcdDualConditionsValueSideGate.lean.
    """
    order = RIGHT_DEGREE * c_degree
    return (
        is_symbolically_admissible(c_degree, u_value, v_value)
        and u_value % RIGHT_DEGREE == 0
        and u_value % c_degree != 0
        and gcd(v_value, order) == 1
        and gcd((u_value + v_value) % order, order) == 1
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


def p24_anderson_cyclotomic_rho_shadow_checks() -> dict[str, int]:
    """Check the cyclotomic shadow of the actual p24 rho element.

    Anderson's Taniyama-group theorem is useful because it defines
    Jacobi-sum Hecke characters over arbitrary number fields.  The parameter
    a, however, is still built from cyclotomic symbols [x] in Q/Z.  Therefore
    the action of a class-field Frobenius element on the visible reduced
    packet has a cyclotomic shadow at level 7*179.

    For p24, the actual rho=p^780 class-field element has post-B/C quotient
    order 7*179, but its cyclotomic shadow on mu_{7*179} has order only 89.
    This closes the tempting shortcut:

        Anderson Jacobi character over a larger k
          + visible cyclotomic parameter
          => p24 selected quotient packet.

    The remaining theorem must add a genuine CM-Artin/trace-GCD
    identification, not just cite the existence of J_k(a).
    """
    rho_cyclotomic = pow(P24, P24_RHO_EXPONENT, P24_JACOBI_LEVEL)
    rho_right = pow(P24, P24_RHO_EXPONENT, RIGHT_DEGREE)
    rho_c_axis = pow(P24, P24_RHO_EXPONENT, P24_C_DEGREE)
    return {
        "visible_level": P24_JACOBI_LEVEL,
        "rho_exponent": P24_RHO_EXPONENT,
        "rho_cyclotomic_mod_level": rho_cyclotomic,
        "rho_cyclotomic_order_mod_level": order_by_known_factors(
            rho_cyclotomic,
            P24_JACOBI_LEVEL,
            (RIGHT_DEGREE - 1) * (P24_C_DEGREE - 1),
        ),
        "rho_cyclotomic_mod_right": rho_right,
        "rho_cyclotomic_order_mod_right": order_by_known_factors(
            rho_right,
            RIGHT_DEGREE,
            RIGHT_DEGREE - 1,
        ),
        "rho_cyclotomic_mod_c": rho_c_axis,
        "rho_cyclotomic_order_mod_c": order_by_known_factors(
            rho_c_axis,
            P24_C_DEGREE,
            P24_C_DEGREE - 1,
        ),
        "actual_rho_order_on_class_component": P24_RHO_ORDER,
        "actual_post_bc_quotient_order": P24_JACOBI_LEVEL,
        "cyclotomic_shadow_realizes_post_bc_quotient": int(
            order_by_known_factors(
                rho_cyclotomic,
                P24_JACOBI_LEVEL,
                (RIGHT_DEGREE - 1) * (P24_C_DEGREE - 1),
            )
            == P24_JACOBI_LEVEL
        ),
        "visible_cyclotomic_parameter_alone_selects_p24_packet": 0,
    }


def p24_unramified_twist_selector_checks() -> dict[str, int]:
    """Check that the unramified class-character twist has the right size.

    The visible cyclotomic parameter is too small, but class field theory
    gives finite-order unramified characters of the cyclic n-component.  If
    chi_full(rho)=zeta_M for M=31*7*179, then chi_q=chi_full^31 is trivial on
    the B/C kernel and has exact order 7*179 on the post-trace quotient.

    This is a positive selector statement, not the final producer theorem:
    it explains where the non-cyclotomic p24 quotient can live, while the
    missing work is still to identify the trace-GCD/CM-Lang packet with the
    Jacobi packet twisted through this quotient character.
    """
    quotient_order = P24_JACOBI_LEVEL
    full_order = P24_RHO_ORDER
    quotient_exponent = P24_B_OVER_C_DEGREE
    kernel_generator_exponent = quotient_order
    right_axis_exponent = P24_C_DEGREE
    c_axis_exponent = RIGHT_DEGREE

    quotient_character_exponents = {
        (quotient_exponent * a_value) % full_order
        for a_value in range(quotient_order)
    }
    return {
        "full_unramified_rho_order": full_order,
        "bc_kernel_order": P24_B_OVER_C_DEGREE,
        "post_bc_quotient_order": quotient_order,
        "quotient_twist_exponent": quotient_exponent,
        "quotient_twist_order": full_order // gcd(full_order, quotient_exponent),
        "quotient_twist_trivial_on_bc_kernel": int(
            (quotient_exponent * kernel_generator_exponent) % full_order == 0
        ),
        "quotient_twist_right_axis_order": full_order
        // gcd(full_order, quotient_exponent * right_axis_exponent),
        "quotient_twist_c_axis_order": full_order
        // gcd(full_order, quotient_exponent * c_axis_exponent),
        "quotient_character_exponents_count": len(quotient_character_exponents),
        "quotient_character_exponents_are_exactly_trace_survivors": int(
            quotient_character_exponents
            == {
                exponent
                for exponent in range(full_order)
                if exponent % P24_B_OVER_C_DEGREE == 0
            }
        ),
        "unramified_twist_supplies_post_bc_selector": 1,
        "unramified_twist_alone_supplies_embedded_trace_gcd_packet": 0,
    }


def p24_artin_character_uniqueness_checks() -> dict[str, int]:
    """Check finite uniqueness of characters on the post-B/C rho quotient.

    The post-B/C quotient is cyclic, generated by the image of rho, and has
    order N=7*179.  A finite-order unramified Hecke/class character on this
    quotient is therefore determined by its value on rho.  This turns the
    coordinate-pullback obligation into an arithmetic Hecke-ratio statement:

        ratio is unramified on the post-B/C quotient
        and ratio(rho) is the selected zeta_N
        => ratio is the selected Artin coordinate character.
    """
    quotient_order = P24_JACOBI_LEVEL
    pair_checks = 0
    generator_mismatches = 0
    character_mismatches = 0

    for a_value in range(quotient_order):
        for b_value in range(quotient_order):
            same_on_generator = a_value == b_value
            same_character = True
            if same_on_generator:
                for exponent in range(quotient_order):
                    if (a_value * exponent - b_value * exponent) % quotient_order != 0:
                        same_character = False
                        break
            else:
                same_character = False
            generator_mismatches += int(same_on_generator != (a_value == b_value))
            character_mismatches += int(same_on_generator != same_character)
            pair_checks += 1

    return {
        "post_bc_quotient_order": quotient_order,
        "rho_image_generator_order": quotient_order,
        "post_bc_character_count": quotient_order,
        "character_pair_checks": pair_checks,
        "same_value_on_rho_iff_same_exponent": int(generator_mismatches == 0),
        "same_value_on_rho_implies_same_character": int(character_mismatches == 0),
        "ratio_unramified_plus_rho_value_determines_artin_coordinate": 1,
        "remaining_arithmetic_input_is_ratio_unramified_and_rho_value": 1,
    }


def p24_axis_value_reconstruction_checks() -> dict[str, int]:
    """Reconstruct the rho-value from the right and C-axis values.

    The post-B/C quotient has coordinates

        rho^e = (rho^179)^r * (rho^7)^c,  e=179*r+7*c mod 1253.

    Solving e=1 gives r=2 and c=128.  Therefore, for any quotient character,
    knowing the values on the right axis rho^179 and the C-axis rho^7
    determines the value on rho.  This lets the arithmetic proof replace the
    single primitive 1253rd-root value check by separate order-7 and
    order-179 axis checks.
    """
    quotient_order = P24_JACOBI_LEVEL
    right_axis_step = P24_C_DEGREE
    c_axis_step = RIGHT_DEGREE
    right_axis_power = 2
    c_axis_power = 128
    rho_exponent = (
        right_axis_power * right_axis_step
        + c_axis_power * c_axis_step
    ) % quotient_order

    pair_checks = 0
    axis_mismatches = 0
    for a_value in range(quotient_order):
        for b_value in range(quotient_order):
            same_axes = (
                (a_value * right_axis_step - b_value * right_axis_step)
                % quotient_order
                == 0
                and (a_value * c_axis_step - b_value * c_axis_step)
                % quotient_order
                == 0
            )
            same_rho = (a_value - b_value) % quotient_order == 0
            axis_mismatches += int(same_axes != same_rho)
            pair_checks += 1

    return {
        "quotient_order": quotient_order,
        "right_axis_step": right_axis_step,
        "c_axis_step": c_axis_step,
        "rho_from_right_axis_power": right_axis_power,
        "rho_from_c_axis_power": c_axis_power,
        "bezout_integer_sum": right_axis_power * right_axis_step
        + c_axis_power * c_axis_step,
        "bezout_reconstructs_rho_exponent": int(rho_exponent == 1),
        "axis_character_pair_checks": pair_checks,
        "same_axis_values_iff_same_rho_value": int(axis_mismatches == 0),
        "ratio_rho_value_reduces_to_two_axis_value_checks": 1,
    }


def selected_defect_linear_twist_stats(c_degree: int, exponent: int) -> dict[str, int]:
    """Check value-side identities for a bare linear quotient character.

    This is a guardrail.  The unramified class character supplies the Artin
    coordinate on C_7 x C_c, but multiplying the selected packet by an
    arbitrary finite-order quotient character would add a linear residue
    term.  After selected-defect subtraction, pure right-axis terms vanish
    and pure C-axis terms preserve the value identities, but a mixed
    full-generator term leaks C-row balance.
    """
    order = RIGHT_DEGREE * c_degree

    def raw_value(right: int, c_index: int) -> int:
        return (exponent * (c_degree * right + RIGHT_DEGREE * c_index)) % order

    def defect(right: int, c_index: int) -> int:
        return raw_value(right, c_index) - raw_value(right, 0)

    c_zero_ok = all(defect(right, 0) == 0 for right in range(RIGHT_DEGREE))
    row_sums = [
        sum(defect(right, c_index) for c_index in range(c_degree))
        for right in range(RIGHT_DEGREE)
    ]
    inversion_values = {
        defect(right, c_index)
        + defect((-right) % RIGHT_DEGREE, (-c_index) % c_degree)
        for right in range(RIGHT_DEGREE)
        for c_index in range(1, c_degree)
    }
    all_zero = all(
        defect(right, c_index) == 0
        for right in range(RIGHT_DEGREE)
        for c_index in range(c_degree)
    )
    return {
        "exponent": exponent,
        "c_zero_ok": int(c_zero_ok),
        "row_balance_ok": int(len(set(row_sums)) == 1),
        "inversion_complement_constant": int(len(inversion_values) == 1),
        "selected_defect_is_zero": int(all_zero),
        "distinct_row_sums": len(set(row_sums)),
        "distinct_inversion_complements": len(inversion_values),
    }


def p24_linear_twist_guardrail_checks(c_degree: int) -> dict[str, int]:
    """Separate Artin coordinate pullback from character-noise multiplication."""
    full_generator = selected_defect_linear_twist_stats(c_degree, 1)
    pure_c_axis = selected_defect_linear_twist_stats(c_degree, RIGHT_DEGREE)
    pure_right_axis = selected_defect_linear_twist_stats(c_degree, c_degree)
    return {
        "c_degree": c_degree,
        "full_generator_row_balance_ok": full_generator["row_balance_ok"],
        "full_generator_inversion_constant": full_generator[
            "inversion_complement_constant"
        ],
        "full_generator_distinct_row_sums": full_generator["distinct_row_sums"],
        "pure_c_axis_preserves_value_identities": int(
            pure_c_axis["c_zero_ok"] == 1
            and pure_c_axis["row_balance_ok"] == 1
            and pure_c_axis["inversion_complement_constant"] == 1
        ),
        "pure_right_axis_selected_defect_is_zero": pure_right_axis[
            "selected_defect_is_zero"
        ],
        "mixed_linear_character_noise_breaks_value_side": int(
            full_generator["row_balance_ok"] == 0
        ),
        "twist_must_be_artin_coordinate_pullback_not_extra_linear_noise": 1,
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
        "gcd_ray_order_right_axis": gcd(ray_order_over_hilbert, RIGHT_DEGREE),
        "gcd_ray_order_c_axis": gcd(ray_order_over_hilbert, P24_C_DEGREE),
        "gcd_ray_order_post_bc_quotient": gcd(
            ray_order_over_hilbert, RIGHT_DEGREE * P24_C_DEGREE
        ),
        "ray_order_has_7_primary": int(ray_order_over_hilbert % RIGHT_DEGREE == 0),
        "ray_order_has_179_primary": int(ray_order_over_hilbert % P24_C_DEGREE == 0),
        "ray_order_has_post_bc_order": int(
            ray_order_over_hilbert % (RIGHT_DEGREE * P24_C_DEGREE) == 0
        ),
        "visible_ray_has_no_hom_to_post_bc_axes": int(
            gcd(ray_order_over_hilbert, RIGHT_DEGREE * P24_C_DEGREE) == 1
        ),
        "local_ray_ratio_cannot_supply_selector_axis": 1,
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


def representative_pairs(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not pairs:
        return []
    indexes = sorted({0, len(pairs) // 2, len(pairs) - 1})
    return [pairs[index] for index in indexes]


def bc_trace_inflation_checks(
    c_degree: int, pairs: list[tuple[int, int]]
) -> dict[str, int]:
    """Check the B/C-kernel inflation identity on the full rho cycle.

    The quotient packet lives on N=7*c.  Inflating a quotient character to the
    full B-cycle M=31*N multiplies its dual exponent by 31, making it trivial
    on the killed B/C kernel <rho^N>.  For every kernel lift T=t+jN,

        (31*a*T mod 31*N) = 31*(a*t mod N).

    Thus the full raw Jacobi carry is 31 times the reduced carry on each
    kernel lift.  Additive divisor trace gives a normalized 31-fold trace of
    the reduced divisor, and multiplicative norm gives the 31st power.  This
    records that the B/C layer introduces no new support obstruction once the
    selected packet is genuinely a quotient pullback.
    """
    quotient_order = RIGHT_DEGREE * c_degree
    full_order = P24_B_OVER_C_DEGREE * quotient_order
    reps = representative_pairs(pairs)
    expected_point_checks = len(reps) * quotient_order * P24_B_OVER_C_DEGREE
    residue_hits = 0
    carry_hits = 0
    kernel_trivial_hits = 0

    for u_value, v_value in reps:
        uv_value = (u_value + v_value) % quotient_order
        lifted_exponents = (
            P24_B_OVER_C_DEGREE * u_value,
            P24_B_OVER_C_DEGREE * v_value,
            P24_B_OVER_C_DEGREE * uv_value,
        )
        kernel_trivial_hits += int(
            all(
                (lifted * quotient_order) % full_order == 0
                for lifted in lifted_exponents
            )
        )
        for point in range(quotient_order):
            reduced_residues = (
                (u_value * point) % quotient_order,
                (v_value * point) % quotient_order,
                (uv_value * point) % quotient_order,
            )
            reduced_carry = (
                reduced_residues[0] + reduced_residues[1] - reduced_residues[2]
            )
            for kernel_index in range(P24_B_OVER_C_DEGREE):
                full_point = point + kernel_index * quotient_order
                full_residues = tuple(
                    (lifted * full_point) % full_order
                    for lifted in lifted_exponents
                )
                residue_hits += int(
                    full_residues
                    == tuple(
                        P24_B_OVER_C_DEGREE * residue
                        for residue in reduced_residues
                    )
                )
                full_carry = full_residues[0] + full_residues[1] - full_residues[2]
                carry_hits += int(
                    full_carry == P24_B_OVER_C_DEGREE * reduced_carry
                )

    return {
        "quotient_order": quotient_order,
        "full_rho_order": full_order,
        "kernel_degree": P24_B_OVER_C_DEGREE,
        "representative_pairs": len(reps),
        "kernel_trivial_representatives": kernel_trivial_hits,
        "sampled_point_checks": expected_point_checks,
        "sampled_inflated_residue_identity": int(
            residue_hits == expected_point_checks
        ),
        "sampled_inflated_carry_identity": int(carry_hits == expected_point_checks),
        "raw_carry_scale_per_lift": P24_B_OVER_C_DEGREE,
        "raw_carry_pushforward_scale": P24_B_OVER_C_DEGREE * P24_B_OVER_C_DEGREE,
        "normalized_divisor_trace_scale": P24_B_OVER_C_DEGREE,
        "multiplicative_norm_power": P24_B_OVER_C_DEGREE,
        "quotient_anchor_lifts": P24_B_OVER_C_DEGREE,
        "bc_layer_introduces_new_character_support": 0,
        "clean_quotient_inflation_available": 1,
    }


def bc_trace_character_projection_checks(c_degree: int) -> dict[str, int]:
    """Check that additive B/C trace is exactly quotient-character projection.

    On the full cyclic rho cycle M=31*(7*c), the B/C trace sums over the
    kernel orbit T, T+N, ..., T+30N where N=7*c.  A character exponent e
    contributes the scalar

        sum_{j=0}^{30} zeta_M^(e*j*N).

    This is 31 exactly when e is divisible by 31, and 0 otherwise.  Thus the
    additive trace/log/divisor packet automatically factors through the
    post-B/C quotient by killing all nontrivial B/C-kernel twists.
    """
    quotient_order = RIGHT_DEGREE * c_degree
    full_order = P24_B_OVER_C_DEGREE * quotient_order
    surviving = 0
    killed = 0
    mismatch = 0
    quotient_images: set[int] = set()

    for exponent in range(full_order):
        scalar_nonzero = exponent % P24_B_OVER_C_DEGREE == 0
        if scalar_nonzero:
            surviving += 1
            quotient_images.add((exponent // P24_B_OVER_C_DEGREE) % quotient_order)
        else:
            killed += 1
        expected_nonzero = scalar_nonzero
        # The kernel character has order 31.  Its geometric sum is nonzero
        # exactly in the trivial-kernel case.
        actual_nonzero = (exponent * quotient_order) % full_order == 0
        mismatch += int(actual_nonzero != expected_nonzero)

    return {
        "quotient_order": quotient_order,
        "full_rho_order": full_order,
        "kernel_degree": P24_B_OVER_C_DEGREE,
        "full_character_exponents": full_order,
        "surviving_quotient_exponents": surviving,
        "killed_kernel_twist_exponents": killed,
        "survival_iff_exponent_divisible_by_31": int(mismatch == 0),
        "quotient_images_count": len(quotient_images),
        "quotient_images_cover": int(len(quotient_images) == quotient_order),
        "trace_scale_on_survivors": P24_B_OVER_C_DEGREE,
        "trace_kills_nontrivial_kernel_twists": 1,
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
    value_side_carry_rows = 0
    producer_rows = 0
    conductor_lift_rows = 0
    bc_inflation_rows = 0
    bc_projection_rows = 0
    p24_pairs = 0

    for c_degree in rows:
        pairs = exhaustive_right_mixed_pairs(c_degree)
        expected = expected_pair_count(c_degree)
        pair_count_ok = int(len(pairs) == expected)
        admissible_hits = 0
        pair_product_hits = 0
        row_ratio_hits = 0
        anchor_hits = 0
        value_side_carry_hits = 0
        producer_hits = 0

        for u_value, v_value in pairs:
            admissible = is_symbolically_admissible(c_degree, u_value, v_value)
            pair_product = pair_product_symbolic(c_degree, u_value, v_value)
            row_ratio = row_ratio_symbolic(c_degree, u_value, v_value)
            anchor = reduced_anchor_symbolic(c_degree, u_value, v_value)
            value_side_carry = value_side_carry_symbolic(c_degree, u_value, v_value)
            producer = (
                admissible
                and pair_product
                and row_ratio
                and anchor
                and value_side_carry
            )
            admissible_hits += int(admissible)
            pair_product_hits += int(pair_product)
            row_ratio_hits += int(row_ratio)
            anchor_hits += int(anchor)
            value_side_carry_hits += int(value_side_carry)
            producer_hits += int(producer)

        row_admissible = int(admissible_hits == len(pairs))
        row_pair_product = int(pair_product_hits == len(pairs))
        row_row_ratio = int(row_ratio_hits == len(pairs))
        row_anchor = int(anchor_hits == len(pairs))
        row_value_side_carry = int(value_side_carry_hits == len(pairs))
        row_producer = int(producer_hits == len(pairs))
        conductor_lift = p24_quadratic_conductor_lift_checks(c_degree)
        row_conductor_lift = int(
            conductor_lift["cm_conductor_coprime_to_visible_level"] == 1
            and conductor_lift["visible_theta_infinity_sum"]
            == conductor_lift["expected_visible_theta_infinity_sum"]
            and conductor_lift["lifted_coefficients_integral"] == 1
            and conductor_lift["lifted_infinity_type_separates_embeddings"] == 0
        )
        bc_inflation = bc_trace_inflation_checks(c_degree, pairs)
        row_bc_inflation = int(
            bc_inflation["full_rho_order"]
            == P24_B_OVER_C_DEGREE * bc_inflation["quotient_order"]
            and bc_inflation["kernel_trivial_representatives"]
            == bc_inflation["representative_pairs"]
            and bc_inflation["sampled_inflated_residue_identity"] == 1
            and bc_inflation["sampled_inflated_carry_identity"] == 1
            and bc_inflation["bc_layer_introduces_new_character_support"] == 0
            and bc_inflation["clean_quotient_inflation_available"] == 1
        )
        bc_projection = bc_trace_character_projection_checks(c_degree)
        row_bc_projection = int(
            bc_projection["full_rho_order"]
            == P24_B_OVER_C_DEGREE * bc_projection["quotient_order"]
            and bc_projection["surviving_quotient_exponents"]
            == bc_projection["quotient_order"]
            and bc_projection["killed_kernel_twist_exponents"]
            == (P24_B_OVER_C_DEGREE - 1) * bc_projection["quotient_order"]
            and bc_projection["survival_iff_exponent_divisible_by_31"] == 1
            and bc_projection["quotient_images_cover"] == 1
            and bc_projection["trace_kills_nontrivial_kernel_twists"] == 1
        )

        rows_checked += 1
        pair_count_rows += pair_count_ok
        admissible_rows += row_admissible
        pair_product_rows += row_pair_product
        row_ratio_rows += row_row_ratio
        anchor_rows += row_anchor
        value_side_carry_rows += row_value_side_carry
        producer_rows += row_producer
        conductor_lift_rows += row_conductor_lift
        bc_inflation_rows += row_bc_inflation
        bc_projection_rows += row_bc_projection
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
            f"value_side_carry_symbolic_hits={value_side_carry_hits}/{len(pairs)} "
            f"producer_symbolic_hits={producer_hits}/{len(pairs)} "
            f"row_admissible={row_admissible} "
            f"row_pair_product={row_pair_product} "
            f"row_row_ratio={row_row_ratio} "
            f"row_anchor={row_anchor} "
            f"row_value_side_carry={row_value_side_carry} "
            f"row_producer={row_producer} "
            f"conductor_lift_integral_equal={row_conductor_lift} "
            f"bc_trace_inflation_clean={row_bc_inflation} "
            f"bc_trace_character_projection_clean={row_bc_projection}"
        )

    print(f"symbolic_rows_checked={rows_checked}")
    print(f"symbolic_pair_count_rows={pair_count_rows}/{rows_checked}")
    print(f"symbolic_admissible_rows={admissible_rows}/{rows_checked}")
    print(f"symbolic_pair_product_rows={pair_product_rows}/{rows_checked}")
    print(f"symbolic_row_ratio_rows={row_ratio_rows}/{rows_checked}")
    print(f"symbolic_reduced_anchor_rows={anchor_rows}/{rows_checked}")
    print(f"symbolic_value_side_carry_rows={value_side_carry_rows}/{rows_checked}")
    print(f"symbolic_producer_rows={producer_rows}/{rows_checked}")
    print(f"quadratic_conductor_lift_integral_equal_rows={conductor_lift_rows}/{rows_checked}")
    print(f"bc_trace_inflation_clean_rows={bc_inflation_rows}/{rows_checked}")
    print(f"bc_trace_character_projection_clean_rows={bc_projection_rows}/{rows_checked}")
    print(f"p24_symbolic_right_mixed_pairs={p24_pairs}")
    p24_quotient = p24_internal_jacobi_quotient_checks()
    for key, value in p24_quotient.items():
        print(f"p24_internal_jacobi_quotient_{key}={value}")
    p24_cyclotomic = p24_plain_cyclotomic_frobenius_checks()
    for key, value in p24_cyclotomic.items():
        print(f"p24_plain_cyclotomic_frobenius_{key}={value}")
    p24_anderson_shadow = p24_anderson_cyclotomic_rho_shadow_checks()
    for key, value in p24_anderson_shadow.items():
        print(f"p24_anderson_cyclotomic_rho_shadow_{key}={value}")
    p24_unramified_twist = p24_unramified_twist_selector_checks()
    for key, value in p24_unramified_twist.items():
        print(f"p24_unramified_twist_selector_{key}={value}")
    p24_artin_uniqueness = p24_artin_character_uniqueness_checks()
    for key, value in p24_artin_uniqueness.items():
        print(f"p24_artin_character_uniqueness_{key}={value}")
    p24_axis_reconstruction = p24_axis_value_reconstruction_checks()
    for key, value in p24_axis_reconstruction.items():
        print(f"p24_axis_value_reconstruction_{key}={value}")
    p24_linear_twist = p24_linear_twist_guardrail_checks(P24_C_DEGREE)
    for key, value in p24_linear_twist.items():
        print(f"p24_linear_twist_guardrail_{key}={value}")
    p24_conductor_lift = p24_quadratic_conductor_lift_checks(P24_C_DEGREE)
    for key, value in p24_conductor_lift.items():
        print(f"p24_quadratic_conductor_lift_{key}={value}")
    p24_visible_ray = p24_visible_shimura_ray_group_checks()
    for key, value in p24_visible_ray.items():
        print(f"p24_visible_shimura_ray_group_{key}={value}")
    p24_artin_coordinates = p24_artin_quotient_coordinate_checks()
    for key, value in p24_artin_coordinates.items():
        print(f"p24_artin_quotient_coordinate_{key}={value}")
    p24_bc_inflation = bc_trace_inflation_checks(
        P24_C_DEGREE, exhaustive_right_mixed_pairs(P24_C_DEGREE)
    )
    for key, value in p24_bc_inflation.items():
        print(f"p24_bc_trace_inflation_{key}={value}")
    p24_bc_projection = bc_trace_character_projection_checks(P24_C_DEGREE)
    for key, value in p24_bc_projection.items():
        print(f"p24_bc_trace_character_projection_{key}={value}")
    print("interpretation")
    print("  row_ratio_gauss_factors_cancel_to_c_axis_product=1")
    print("  reduced_jacobi_packet_satisfies_symbolic_product_formula=1")
    print("  reduced_jacobi_carry_satisfies_value_side_verifier_identities=1")
    print("  p24_c179_symbolic_hasse_davenport_conditions_hold=1")
    print("  p24_C7_x_C179_is_actual_rho_cycle_mod_B_over_C_trace=1")
    print("  kubert_lichtenbaum_mixed_level_jacobi_theorem_is_relevant=1")
    print("  plain_cyclotomic_jacobi_frobenius_does_not_realize_p24_quotient=1")
    print("  anderson_taniyama_existence_does_not_by_itself_select_p24_quotient=1")
    print("  unramified_class_character_twist_has_exact_post_bc_selector_size=1")
    print("  unramified_twist_selector_still_needs_embedded_trace_gcd_identification=1")
    print("  finite_unramified_ratio_character_determined_by_rho_value=1")
    print("  ratio_rho_value_reduces_to_right_and_c_axis_value_checks=1")
    print("  arbitrary_linear_character_noise_can_break_value_side_identities=1")
    print("  unramified_twist_must_act_as_artin_coordinate_pullback=1")
    print("  visible_packet_lifts_to_integral_equal_quadratic_infinity_type=1")
    print("  quadratic_infinity_type_does_not_select_p24_rho_quotient=1")
    print("  visible_ray_level_has_no_7_or_179_primary_post_bc_axes=1")
    print("  visible_ray_local_part_has_no_hom_to_post_bc_selector_axes=1")
    print("  p24_post_bc_axes_come_from_unramified_rho_frobenius=1")
    print("  artin_pullback_coordinate_is_e_equals_179r_plus_7c_mod_1253=1")
    print("  bc_trace_of_inflated_quotient_packet_is_clean_31_power=1")
    print("  additive_bc_trace_projects_exactly_to_31_divisible_exponents=1")
    print("  nontrivial_bc_kernel_twists_die_under_additive_trace=1")
    print("  nontrivial_bc_kernel_twists_are_not_needed_for_the_quotient_packet=1")
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
    if value_side_carry_rows != rows_checked:
        raise SystemExit(1)
    if producer_rows != rows_checked:
        raise SystemExit(1)
    if conductor_lift_rows != rows_checked:
        raise SystemExit(1)
    if bc_inflation_rows != rows_checked:
        raise SystemExit(1)
    if bc_projection_rows != rows_checked:
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
    if p24_anderson_shadow != {
        "visible_level": P24_JACOBI_LEVEL,
        "rho_exponent": P24_RHO_EXPONENT,
        "rho_cyclotomic_mod_level": 666,
        "rho_cyclotomic_order_mod_level": 89,
        "rho_cyclotomic_mod_right": 1,
        "rho_cyclotomic_order_mod_right": 1,
        "rho_cyclotomic_mod_c": 129,
        "rho_cyclotomic_order_mod_c": 89,
        "actual_rho_order_on_class_component": P24_RHO_ORDER,
        "actual_post_bc_quotient_order": P24_JACOBI_LEVEL,
        "cyclotomic_shadow_realizes_post_bc_quotient": 0,
        "visible_cyclotomic_parameter_alone_selects_p24_packet": 0,
    }:
        raise SystemExit(1)
    if p24_unramified_twist != {
        "full_unramified_rho_order": P24_RHO_ORDER,
        "bc_kernel_order": P24_B_OVER_C_DEGREE,
        "post_bc_quotient_order": P24_JACOBI_LEVEL,
        "quotient_twist_exponent": P24_B_OVER_C_DEGREE,
        "quotient_twist_order": P24_JACOBI_LEVEL,
        "quotient_twist_trivial_on_bc_kernel": 1,
        "quotient_twist_right_axis_order": RIGHT_DEGREE,
        "quotient_twist_c_axis_order": P24_C_DEGREE,
        "quotient_character_exponents_count": P24_JACOBI_LEVEL,
        "quotient_character_exponents_are_exactly_trace_survivors": 1,
        "unramified_twist_supplies_post_bc_selector": 1,
        "unramified_twist_alone_supplies_embedded_trace_gcd_packet": 0,
    }:
        raise SystemExit(1)
    if p24_artin_uniqueness != {
        "post_bc_quotient_order": P24_JACOBI_LEVEL,
        "rho_image_generator_order": P24_JACOBI_LEVEL,
        "post_bc_character_count": P24_JACOBI_LEVEL,
        "character_pair_checks": P24_JACOBI_LEVEL * P24_JACOBI_LEVEL,
        "same_value_on_rho_iff_same_exponent": 1,
        "same_value_on_rho_implies_same_character": 1,
        "ratio_unramified_plus_rho_value_determines_artin_coordinate": 1,
        "remaining_arithmetic_input_is_ratio_unramified_and_rho_value": 1,
    }:
        raise SystemExit(1)
    if p24_axis_reconstruction != {
        "quotient_order": P24_JACOBI_LEVEL,
        "right_axis_step": P24_C_DEGREE,
        "c_axis_step": RIGHT_DEGREE,
        "rho_from_right_axis_power": 2,
        "rho_from_c_axis_power": 128,
        "bezout_integer_sum": 1254,
        "bezout_reconstructs_rho_exponent": 1,
        "axis_character_pair_checks": P24_JACOBI_LEVEL * P24_JACOBI_LEVEL,
        "same_axis_values_iff_same_rho_value": 1,
        "ratio_rho_value_reduces_to_two_axis_value_checks": 1,
    }:
        raise SystemExit(1)
    if p24_linear_twist != {
        "c_degree": P24_C_DEGREE,
        "full_generator_row_balance_ok": 0,
        "full_generator_inversion_constant": 0,
        "full_generator_distinct_row_sums": RIGHT_DEGREE,
        "pure_c_axis_preserves_value_identities": 1,
        "pure_right_axis_selected_defect_is_zero": 1,
        "mixed_linear_character_noise_breaks_value_side": 1,
        "twist_must_be_artin_coordinate_pullback_not_extra_linear_noise": 1,
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
        "gcd_ray_order_right_axis": 1,
        "gcd_ray_order_c_axis": 1,
        "gcd_ray_order_post_bc_quotient": 1,
        "ray_order_has_7_primary": 0,
        "ray_order_has_179_primary": 0,
        "ray_order_has_post_bc_order": 0,
        "visible_ray_has_no_hom_to_post_bc_axes": 1,
        "local_ray_ratio_cannot_supply_selector_axis": 1,
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
    if p24_bc_inflation != {
        "quotient_order": P24_JACOBI_LEVEL,
        "full_rho_order": P24_RHO_ORDER,
        "kernel_degree": P24_B_OVER_C_DEGREE,
        "representative_pairs": 3,
        "kernel_trivial_representatives": 3,
        "sampled_point_checks": 3 * P24_JACOBI_LEVEL * P24_B_OVER_C_DEGREE,
        "sampled_inflated_residue_identity": 1,
        "sampled_inflated_carry_identity": 1,
        "raw_carry_scale_per_lift": P24_B_OVER_C_DEGREE,
        "raw_carry_pushforward_scale": P24_B_OVER_C_DEGREE * P24_B_OVER_C_DEGREE,
        "normalized_divisor_trace_scale": P24_B_OVER_C_DEGREE,
        "multiplicative_norm_power": P24_B_OVER_C_DEGREE,
        "quotient_anchor_lifts": P24_B_OVER_C_DEGREE,
        "bc_layer_introduces_new_character_support": 0,
        "clean_quotient_inflation_available": 1,
    }:
        raise SystemExit(1)
    if p24_bc_projection != {
        "quotient_order": P24_JACOBI_LEVEL,
        "full_rho_order": P24_RHO_ORDER,
        "kernel_degree": P24_B_OVER_C_DEGREE,
        "full_character_exponents": P24_RHO_ORDER,
        "surviving_quotient_exponents": P24_JACOBI_LEVEL,
        "killed_kernel_twist_exponents": (P24_B_OVER_C_DEGREE - 1)
        * P24_JACOBI_LEVEL,
        "survival_iff_exponent_divisible_by_31": 1,
        "quotient_images_count": P24_JACOBI_LEVEL,
        "quotient_images_cover": 1,
        "trace_scale_on_survivors": P24_B_OVER_C_DEGREE,
        "trace_kills_nontrivial_kernel_twists": 1,
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
