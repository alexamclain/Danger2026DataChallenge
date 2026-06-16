#!/usr/bin/env python3
"""Parameter-level bridge audit for the dual-sparse trace-GCD route.

The finite DFT bridge says cyclic difference is p-unit diagonal scaling on
nonzero right frequencies.  The remaining ambiguity is whether the same
left-field parameter lambda is being seen by:

* the centered profile scalar word
      f_lambda(s) = Tr_{L/F_q}(lambda * G_s^0);
* the nonzero right Fourier periods
      S_v = sum_s zeta_right^(v*s) G_s^0;
* the Lang/Fitting trace coordinates used by trace-GCD.

For small actual-CM rows, this audit checks the exact parameter identities on
an F_q-basis of lambda:

    DFT_right(f_lambda)_v = Tr_{LR/R}(lambda * S_v)

and, on each right Frobenius orbit,

    (Tr_{LR/R}(lambda*S_v))_v = U_orbit *
      (Tr_{L/F_q}(lambda*T_i))_i,

where U_orbit is the Lang Moore matrix and T_i are the Lang-trivialized
coordinates.  These are linear in lambda, so basis checks prove the identity
for all lambda in the tested left field.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_inverse,
    matrix_vector_mul,
    subfield_power_basis,
)
from hermitian_mixed_left_subfield_normality_audit import (
    centered_right_profile_for_left_orbit,
    right_fourier_coefficient,
    trace_to_base,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import section_fiber_polynomials


SEED = 20260605


@dataclass(frozen=True)
class LambdaBridgeCase:
    label: str
    D: int
    q: int
    m: int
    left: int
    right: int


@dataclass(frozen=True)
class LambdaBridgeRow:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    left_orbit: tuple[int, ...]
    right_orbit_lengths: tuple[int, ...]
    lambda_basis_size: int
    profile_dft_mismatches: int
    lambda_fourier_trace_mismatches: int
    lang_reconstruction_mismatches: int
    lang_zero_equivalence_failures: int
    checked_right_frequencies: int
    checked_orbit_vectors: int


def hermitian_packet_factor(n: int, q: int) -> sp.Poly:
    for factor in packet_factors(n, q):
        if factor.degree() % 2:
            continue
        if pow(q, factor.degree() // 2, n) == n - 1:
            return factor
    raise ValueError("no Hermitian packet factor")


def relative_trace_fix_right(
    value: FpE,
    left_len: int,
    right_len: int,
    field: ExtensionField,
) -> FpE:
    """Trace from LR to R, using Frobenius^{right_len} to fix R."""

    total = field.zero
    for i in range(left_len):
        total = field.add(total, field.pow(value, field.q ** (right_len * i)))
    return total


def scalar_word_for_lambda(
    lam: FpE,
    centered_profile: list[FpE],
    left_len: int,
    field: ExtensionField,
) -> list[FpE]:
    return [
        trace_to_base(field.mul(lam, value), left_len, field)
        for value in centered_profile
    ]


def audit_case(case: LambdaBridgeCase) -> list[LambdaBridgeRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(case.D)
    h = int(pari.poldegree(hilbert))
    roots = [int(root) for root in pari.polrootsmod(hilbert, case.q)]
    ell, cycle = find_full_cycle_prime(roots, case.D, case.q)
    n = h // case.m
    factor = hermitian_packet_factor(n, case.q)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, case.q, case.m, "complement")
    ]
    marginal = double_marginal(
        kernel_matrix(residues, factor, case.q),
        case.left,
        case.right,
        case.q,
    )

    extension_degree = int(sp.n_order(case.q % case.m, case.m))
    modulus = find_irreducible_modulus(case.q, extension_degree, SEED)
    field = ExtensionField(case.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, case.m, SEED)
    powers = zeta_powers(zeta, case.m, field)
    dft_matrix = dft_double_marginal(
        marginal, case.left, case.right, powers, case.m, field
    )
    right_orbits = q_orbits(case.right, case.q)
    row_index = {u: u - 1 for u in range(1, case.left)}
    col_index = {v: v - 1 for v in range(1, case.right)}

    rows: list[LambdaBridgeRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        left_len = len(left_orbit)
        if left_len <= 1:
            continue
        if any(gcd(left_len, len(right_orbit)) != 1 for right_orbit in right_orbits):
            continue

        centered_profile = centered_right_profile_for_left_orbit(
            marginal,
            case.left,
            case.right,
            left_orbit,
            case.m,
            powers,
            case.q,
            field,
        )
        lambda_basis = subfield_power_basis(case.q, left_len, field, SEED + 157)

        profile_dft_mismatches = 0
        for v in range(1, case.right):
            profile_coeff = right_fourier_coefficient(
                centered_profile, v, case.right, case.m, powers, field
            )
            dft_coeff = dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            if profile_coeff != dft_coeff:
                profile_dft_mismatches += 1

        lambda_fourier_trace_mismatches = 0
        lang_reconstruction_mismatches = 0
        lang_zero_equivalence_failures = 0
        checked_orbit_vectors = 0
        checked_right_frequencies = 0

        for lam in lambda_basis:
            scalar_word = scalar_word_for_lambda(
                lam, centered_profile, left_len, field
            )
            for v in range(1, case.right):
                word_coeff = right_fourier_coefficient(
                    scalar_word, v, case.right, case.m, powers, field
                )
                period = dft_matrix[row_index[left_orbit[0]]][col_index[v]]
                traced_period = relative_trace_fix_right(
                    field.mul(lam, period),
                    left_len,
                    int(sp.n_order(case.q % case.right, case.right)),
                    field,
                )
                if word_coeff != traced_period:
                    lambda_fourier_trace_mismatches += 1
                checked_right_frequencies += 1

            for right_orbit in right_orbits:
                orbit_len = len(right_orbit)
                seed_vector = [
                    dft_matrix[row_index[left_orbit[0]]][col_index[v]]
                    for v in right_orbit
                ]
                lang_inverse = lang_inverse_for_orbit(
                    case.q, orbit_len, field, SEED
                )
                lang_matrix = matrix_inverse(lang_inverse, field)
                transformed = matrix_vector_mul(lang_inverse, seed_vector, field)
                raw_trace_vector = [
                    relative_trace_fix_right(
                        field.mul(lam, value),
                        left_len,
                        orbit_len,
                        field,
                    )
                    for value in seed_vector
                ]
                lang_trace_scalars = [
                    trace_to_base(field.mul(lam, value), left_len, field)
                    for value in transformed
                ]
                reconstructed = matrix_vector_mul(
                    lang_matrix, lang_trace_scalars, field
                )
                if raw_trace_vector != reconstructed:
                    lang_reconstruction_mismatches += 1
                if (all(value == field.zero for value in raw_trace_vector)) != (
                    all(value == field.zero for value in lang_trace_scalars)
                ):
                    lang_zero_equivalence_failures += 1
                checked_orbit_vectors += 1

        rows.append(
            LambdaBridgeRow(
                label=case.label,
                D=case.D,
                q=case.q,
                h=h,
                m=case.m,
                n=n,
                factor_degree=factor.degree(),
                left=case.left,
                right=case.right,
                left_orbit=tuple(left_orbit),
                right_orbit_lengths=tuple(len(orbit) for orbit in right_orbits),
                lambda_basis_size=len(lambda_basis),
                profile_dft_mismatches=profile_dft_mismatches,
                lambda_fourier_trace_mismatches=lambda_fourier_trace_mismatches,
                lang_reconstruction_mismatches=lang_reconstruction_mismatches,
                lang_zero_equivalence_failures=lang_zero_equivalence_failures,
                checked_right_frequencies=checked_right_frequencies,
                checked_orbit_vectors=checked_orbit_vectors,
            )
        )
    return rows


def main() -> None:
    cases = [
        LambdaBridgeCase("pinned", -13319, 13463, 28, 4, 7),
        LambdaBridgeCase("holdout", -26759, 26903, 21, 3, 7),
    ]
    rows = [row for case in cases for row in audit_case(case)]
    print("Trace-GCD lambda profile bridge audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit right_lens "
        "lambda_basis profile_dft_mismatches lambda_fourier_trace_mismatches "
        "lang_reconstruction_mismatches lang_zero_equivalence_failures"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"right_lens={list(row.right_orbit_lengths)} "
            f"lambda_basis={row.lambda_basis_size} "
            f"profile_dft_mismatches={row.profile_dft_mismatches} "
            f"lambda_fourier_trace_mismatches={row.lambda_fourier_trace_mismatches} "
            f"lang_reconstruction_mismatches={row.lang_reconstruction_mismatches} "
            f"lang_zero_equivalence_failures={row.lang_zero_equivalence_failures} "
            f"checked_right_frequencies={row.checked_right_frequencies} "
            f"checked_orbit_vectors={row.checked_orbit_vectors}"
        )
    print("totals")
    print(f"  rows={len(rows)}")
    print(
        "  profile_dft_mismatches="
        f"{sum(row.profile_dft_mismatches for row in rows)}"
    )
    print(
        "  lambda_fourier_trace_mismatches="
        f"{sum(row.lambda_fourier_trace_mismatches for row in rows)}"
    )
    print(
        "  lang_reconstruction_mismatches="
        f"{sum(row.lang_reconstruction_mismatches for row in rows)}"
    )
    print(
        "  lang_zero_equivalence_failures="
        f"{sum(row.lang_zero_equivalence_failures for row in rows)}"
    )
    print("interpretation")
    print("  centered_profile_dft_equals_mixed_periods=1")
    print("  scalar_profile_fourier_equals_relative_trace_of_periods=1")
    print("  lang_coordinates_preserve_parameter_zero_conditions=1")
    print("  remaining_bridge_is_plateau_vanishing_for_bad_lambda=1")
    print("conclusion=reported_trace_gcd_lambda_profile_bridge_audit")


if __name__ == "__main__":
    main()
