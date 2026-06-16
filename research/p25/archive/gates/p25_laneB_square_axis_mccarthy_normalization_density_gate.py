#!/usr/bin/env python3
"""McCarthy parameter-normalization density gate for the p25 square axis.

The numeric McCarthy gate proves that Theorem 1.7 produces the exact
q_exp=138 singleton after subtracting the transformed main sum.  This gate
checks the next normalization question:

* the parameter q_exp=43*(h+1)+9*t is genuinely the p25 square-axis anomaly
  cell (h,t)=(2,1);
* the full S-layer still has to be supplied explicitly;
* the McCarthy singleton is not a standalone sparse hypergeometric value.

In the actual finite-field evaluation, both hypergeometric sides are dense in
q_exp and dense in Fourier space.  The singleton appears only as the theorem
difference LHS-main_sum.  After normalizing the singleton coefficient to 1,
forcing degree zero by scalar balance would also make all 507 q_exp entries
nonzero.  Thus a certificate-shaped continuation must realize the transformed
difference or an equivalent identity before raw lift, not just point at one
McCarthy value and call it the p25 unit vector.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    BASE_FIELD_Q,
    CHARACTER_ORDER,
    ORDER_507_STEP,
    TARGET_Q_EXP,
    VALUE_FIELD,
    X_VALUE,
    McCarthyContext,
)


@dataclass(frozen=True)
class SeedCell:
    h_value: int
    t_value: int
    q_exp: int
    exact_delta: bool
    order3_shadow_delta: bool
    order169_shadow_delta: bool


@dataclass(frozen=True)
class McCarthyNormalizationDensityProfile:
    target_q_exp: int
    target_cell: tuple[int, int]
    a0_exponent: int
    a1_exponent: int
    x_value: int
    seed_cells: tuple[SeedCell, ...]
    exact_seed_delta_cells: tuple[tuple[int, int], ...]
    order3_shadow_cells: tuple[tuple[int, int], ...]
    order169_shadow_cells: tuple[tuple[int, int], ...]
    outer_s_image: tuple[int, ...]
    outer_s_mod169_values: tuple[int, ...]
    outer_s_is_single_order169_delta: bool
    lower_1f0_value: int
    lhs_support_count: int
    main_support_count: int
    transformed_difference_support: tuple[int, ...]
    exceptional_support: tuple[int, ...]
    lhs_fourier_support_count: int
    main_fourier_support_count: int
    transformed_difference_fourier_support_count: int
    exceptional_value_at_target: int
    normalized_delta_degree: int
    degree_zero_scalar_balance: int
    degree_zero_balanced_support_count: int
    sides_are_coordinate_dense: bool
    sides_are_fourier_dense: bool
    point_delta_requires_theorem_cancellation: bool
    scalar_balancing_is_dense: bool


def support(vector: list[int]) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(vector) if value % VALUE_FIELD)


def dft_support_count(ctx: McCarthyContext, vector: list[int]) -> int:
    root_507 = pow(ctx.zeta, ORDER_507_STEP, VALUE_FIELD)
    nonzero = 0
    for frequency in range(QUOTIENT_ORDER):
        ratio = pow(root_507, frequency, VALUE_FIELD)
        power = 1
        total = 0
        for value in vector:
            total = (total + value * power) % VALUE_FIELD
            power = power * ratio % VALUE_FIELD
        nonzero += int(total != 0)
    return nonzero


def seed_cell(h_value: int, t_value: int) -> SeedCell:
    q_exp = (X_STEP * (h_value + 1) + Y_STEP * t_value) % QUOTIENT_ORDER
    return SeedCell(
        h_value=h_value,
        t_value=t_value,
        q_exp=q_exp,
        exact_delta=q_exp == TARGET_Q_EXP,
        order3_shadow_delta=q_exp % 3 == TARGET_Q_EXP % 3,
        order169_shadow_delta=q_exp % 169 == TARGET_Q_EXP % 169,
    )


def mccarthy_vectors() -> tuple[McCarthyContext, int, list[int], list[int], list[int], list[int]]:
    ctx = McCarthyContext()
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    a1_exp = 0
    lower_1f0 = ctx.hypergeo_star((a0_exp,), (), X_VALUE)
    inner_2f1 = tuple(
        ctx.hypergeo_star(
            (a0_exp, (-psi_exp) % CHARACTER_ORDER),
            ((a0_exp + psi_exp) % CHARACTER_ORDER,),
            (-X_VALUE) % BASE_FIELD_Q,
        )
        for psi_exp in range(CHARACTER_ORDER)
    )

    lhs_vector: list[int] = []
    main_vector: list[int] = []
    difference_vector: list[int] = []
    exceptional_vector: list[int] = []

    for q_exp in range(QUOTIENT_ORDER):
        a2_exp = ORDER_507_STEP * q_exp
        lhs = ctx.hypergeo_star(
            (a0_exp, a1_exp, a2_exp),
            (
                (a0_exp - a1_exp) % CHARACTER_ORDER,
                (a0_exp - a2_exp) % CHARACTER_ORDER,
            ),
            X_VALUE,
        )
        denominator = (
            ctx.gauss[a1_exp]
            * ctx.gauss[a2_exp]
            % VALUE_FIELD
            * ctx.gauss[(-a0_exp + a1_exp) % CHARACTER_ORDER]
            % VALUE_FIELD
            * ctx.gauss[(-a0_exp + a2_exp) % CHARACTER_ORDER]
            % VALUE_FIELD
        )
        prefactor = (
            ctx.gauss[(-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER]
            * ctx.inverse(denominator)
            % VALUE_FIELD
        )
        main_sum = 0
        for psi_exp in range(CHARACTER_ORDER):
            term = (
                ctx.gauss[(a1_exp + psi_exp) % CHARACTER_ORDER]
                * ctx.gauss[(a2_exp + psi_exp) % CHARACTER_ORDER]
                % VALUE_FIELD
                * ctx.gauss[-psi_exp % CHARACTER_ORDER]
                % VALUE_FIELD
                * ctx.gauss[(-a0_exp - psi_exp) % CHARACTER_ORDER]
                % VALUE_FIELD
                * inner_2f1[psi_exp]
                % VALUE_FIELD
            )
            main_sum = (main_sum + term) % VALUE_FIELD
        main_term = prefactor * main_sum % VALUE_FIELD * ctx.inv_character_order % VALUE_FIELD

        delta_active = (-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER == 0
        exceptional = (
            BASE_FIELD_Q
            * CHARACTER_ORDER
            % VALUE_FIELD
            * ctx.character_value((a2_exp + a1_exp) % CHARACTER_ORDER, -1)
            % VALUE_FIELD
            * int(delta_active)
            % VALUE_FIELD
            * ctx.inverse(denominator)
            % VALUE_FIELD
            * lower_1f0
            % VALUE_FIELD
        )
        lhs_vector.append(lhs)
        main_vector.append(main_term)
        difference_vector.append((lhs - main_term) % VALUE_FIELD)
        exceptional_vector.append(exceptional)

    return ctx, lower_1f0, lhs_vector, main_vector, difference_vector, exceptional_vector


def mccarthy_normalization_density_profile() -> McCarthyNormalizationDensityProfile:
    cells = tuple(seed_cell(h_value, t_value) for h_value in range(3) for t_value in range(3))
    ctx, lower_1f0, lhs_vector, main_vector, difference_vector, exceptional_vector = mccarthy_vectors()
    diff_support = support(difference_vector)
    exceptional_support = support(exceptional_vector)
    exceptional_value = exceptional_vector[TARGET_Q_EXP]
    normalized_delta = [
        value * ctx.inverse(exceptional_value) % VALUE_FIELD for value in difference_vector
    ]
    scalar_balance = (-ctx.inverse(QUOTIENT_ORDER)) % VALUE_FIELD
    degree_zero_balanced = [
        (value + scalar_balance) % VALUE_FIELD for value in normalized_delta
    ]
    outer_s_image = tuple(
        sorted((TARGET_Q_EXP + layer * S_STEP) % QUOTIENT_ORDER for layer in range(3))
    )
    lhs_fourier = dft_support_count(ctx, lhs_vector)
    main_fourier = dft_support_count(ctx, main_vector)
    diff_fourier = dft_support_count(ctx, difference_vector)

    return McCarthyNormalizationDensityProfile(
        target_q_exp=TARGET_Q_EXP,
        target_cell=(2, 1),
        a0_exponent=ORDER_507_STEP * TARGET_Q_EXP,
        a1_exponent=0,
        x_value=X_VALUE,
        seed_cells=cells,
        exact_seed_delta_cells=tuple(
            (cell.h_value, cell.t_value) for cell in cells if cell.exact_delta
        ),
        order3_shadow_cells=tuple(
            (cell.h_value, cell.t_value) for cell in cells if cell.order3_shadow_delta
        ),
        order169_shadow_cells=tuple(
            (cell.h_value, cell.t_value) for cell in cells if cell.order169_shadow_delta
        ),
        outer_s_image=outer_s_image,
        outer_s_mod169_values=tuple(q_exp % 169 for q_exp in outer_s_image),
        outer_s_is_single_order169_delta=len({q_exp % 169 for q_exp in outer_s_image}) == 1,
        lower_1f0_value=lower_1f0,
        lhs_support_count=len(support(lhs_vector)),
        main_support_count=len(support(main_vector)),
        transformed_difference_support=diff_support,
        exceptional_support=exceptional_support,
        lhs_fourier_support_count=lhs_fourier,
        main_fourier_support_count=main_fourier,
        transformed_difference_fourier_support_count=diff_fourier,
        exceptional_value_at_target=exceptional_value,
        normalized_delta_degree=sum(normalized_delta) % VALUE_FIELD,
        degree_zero_scalar_balance=scalar_balance,
        degree_zero_balanced_support_count=len(support(degree_zero_balanced)),
        sides_are_coordinate_dense=(
            len(support(lhs_vector)) == QUOTIENT_ORDER
            and len(support(main_vector)) == QUOTIENT_ORDER
        ),
        sides_are_fourier_dense=(
            lhs_fourier == QUOTIENT_ORDER
            and main_fourier == QUOTIENT_ORDER
            and diff_fourier == QUOTIENT_ORDER
        ),
        point_delta_requires_theorem_cancellation=(
            len(support(lhs_vector)) == QUOTIENT_ORDER
            and len(support(main_vector)) == QUOTIENT_ORDER
            and diff_support == (TARGET_Q_EXP,)
            and exceptional_support == (TARGET_Q_EXP,)
        ),
        scalar_balancing_is_dense=len(support(degree_zero_balanced)) == QUOTIENT_ORDER,
    )


def main() -> int:
    print("p25 Lane B McCarthy parameter-normalization density gate")
    profile = mccarthy_normalization_density_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.target_cell == (2, 1)
        and profile.a0_exponent == 552
        and profile.a1_exponent == 0
        and profile.x_value == 2
        and profile.exact_seed_delta_cells == ((2, 1),)
        and profile.order3_shadow_cells == ((2, 0), (2, 1), (2, 2))
        and profile.order169_shadow_cells == ((2, 1),)
        and profile.outer_s_image == (138, 310, 482)
        and profile.outer_s_mod169_values == (138, 141, 144)
        and not profile.outer_s_is_single_order169_delta
        and profile.lower_1f0_value == 1
        and profile.lhs_support_count == 507
        and profile.main_support_count == 507
        and profile.transformed_difference_support == (138,)
        and profile.exceptional_support == (138,)
        and profile.lhs_fourier_support_count == 507
        and profile.main_fourier_support_count == 507
        and profile.transformed_difference_fourier_support_count == 507
        and profile.exceptional_value_at_target == 2028
        and profile.normalized_delta_degree == 1
        and profile.degree_zero_scalar_balance == 40580
        and profile.degree_zero_balanced_support_count == 507
        and profile.sides_are_coordinate_dense
        and profile.sides_are_fourier_dense
        and profile.point_delta_requires_theorem_cancellation
        and profile.scalar_balancing_is_dense
    )

    print(f"mccarthy_normalization_density_profile={profile}")
    print("seed_cell_q_exponents")
    for cell in profile.seed_cells:
        print(
            f"  h={cell.h_value} t={cell.t_value}: q={cell.q_exp} "
            f"exact={int(cell.exact_delta)} "
            f"mod3={int(cell.order3_shadow_delta)} "
            f"mod169={int(cell.order169_shadow_delta)}"
        )
    print("normalization_density_laws")
    print("  q=43*(h+1)+9*t selects exactly the anomaly cell (2,1)")
    print("  order_3_shadow_selects_the_whole_h=2_row=1")
    print("  outer_S_image_requires_an_explicit_S_trace_not_one_C169_delta=1")
    print("  mccarthy_LHS_and_main_sum_are_coordinate_dense=1")
    print("  mccarthy_LHS_main_sum_and_delta_are_fourier_dense=1")
    print("  singleton_appears_only_after_theorem_difference_LHS_minus_main_sum=1")
    print("  degree_zero_scalar_balance_of_normalized_delta_is_dense=1")
    print("interpretation")
    print("  positive_parameter_alignment_with_the_p25_seed_grid=1")
    print("  standalone_sparse_mccarthy_unit_vector_is_killed=1")
    print("  continue_only_with_theorem_level_cancellation_or_equivalent_unit_identity=1")
    print(f"square_axis_mccarthy_normalization_density_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_normalization_density_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
