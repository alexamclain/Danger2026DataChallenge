#!/usr/bin/env python3
"""Audit whether the L1 partial-moment scalar reopens the zero-lemma route.

The finite-field divisor lemma compares two quantities after the same
Frobenius-packet multiplier has been applied:

* how many ordinary CM points are forced zeros;
* the pole degree of a nonzero modular/correspondence realization.

For exact harmful content, one character trace vanishes on all K origins, so
the forced zero count is m*n.  For a selected-origin scalar such as L1, a zero
propagates only around the relative H orbit, so the forced zero count is n.
The latter would require correspondence pole degree strictly below n, i.e. a
relative step degree delta < 1.
"""

from __future__ import annotations

from dataclasses import dataclass


P = 10**24 + 7
M = 66_254
N = 3_107_441
H = M * N
ORD_N_P = 388_430

# Best balanced p24 split row: 2 * 463 * 223^(-1).
CURRENT_DELTA = 311_808

# L1 = M0 + P2 + P157 + P211 has four scalar pieces, but they vanish on the
# same H orbit if the selected scalar vanishes; they do not create disjoint K
# translates.  Counting multiplicity in a product gives both zeros and poles a
# factor of the number of scalar pieces, so the strict average-delta test is
# unchanged.
L1_SCALAR_PIECES = 4
L1_AXIS_SUPPORT = 368


@dataclass(frozen=True)
class Scenario:
    name: str
    forced_orbit_units: int
    pole_delta_units: int
    explanation: str

    @property
    def strict_window(self) -> bool:
        return self.pole_delta_units < self.forced_orbit_units

    @property
    def ratio(self) -> float:
        return self.pole_delta_units / self.forced_orbit_units


def main() -> None:
    scenarios = [
        Scenario(
            name="exact_harmful_content_current_correspondence",
            forced_orbit_units=M,
            pole_delta_units=CURRENT_DELTA,
            explanation="all K origins vanish; criterion delta < m",
        ),
        Scenario(
            name="selected_L1_scalar_current_correspondence",
            forced_orbit_units=1,
            pole_delta_units=CURRENT_DELTA,
            explanation="one selected K origin; criterion delta < 1",
        ),
        Scenario(
            name="selected_L1_scalar_ideal_nonconstant_minimum",
            forced_orbit_units=1,
            pole_delta_units=1,
            explanation="even a degree-one nonconstant realization gives equality, not strict",
        ),
        Scenario(
            name="four_projection_family_product_ideal_minimum",
            forced_orbit_units=L1_SCALAR_PIECES,
            pole_delta_units=L1_SCALAR_PIECES,
            explanation="multiplicity from four scalar pieces cancels; still needs average delta < 1",
        ),
        Scenario(
            name="axis_support_misread_as_disjoint_orbits",
            forced_orbit_units=1,
            pole_delta_units=L1_AXIS_SUPPORT,
            explanation="368 K-character support frequencies are not 368 forced K-translates",
        ),
    ]

    print("p24 L1 zero-lemma window audit")
    print(f"p={P}")
    print(f"h=m*n={H}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_n(p)={ORD_N_P}")
    print(f"frobenius_scalar_zero_count=n*ord={N * ORD_N_P}")
    print(f"harmful_content_zero_count=h*ord={H * ORD_N_P}")
    print(f"current_delta={CURRENT_DELTA}")
    print(f"current_delta_over_m={CURRENT_DELTA / M:.6f}")
    print()

    print("scenarios")
    print("  name forced_units pole_units ratio strict_window explanation")
    for row in scenarios:
        print(
            f"  {row.name} {row.forced_orbit_units} {row.pole_delta_units} "
            f"{row.ratio:.6f} {int(row.strict_window)} {row.explanation}"
        )

    print()
    print("interpretation")
    print("  frobenius_multiplier_cancels=1")
    print("  l1_selected_zero_forces_full_K_orbit=0")
    print("  l1_axis_support_is_zero_count=0")
    print("  l1_reopens_zero_lemma_route=0")
    print("  remaining_l1_target=selected_origin_p_unit_or_finite_field_identity")


if __name__ == "__main__":
    main()
