#!/usr/bin/env python3
"""Multiplicative coset selector for the conductor-39 primitive unit.

The mixed tensor gate writes U_chi=-chi_3*chi_13 as a 24-entry signed word.
This gate compresses the same source object into a 12-pair cyclic coset
quotient in (Z/39Z)^*:

    kernel = <2>,
    U_chi = 1_{7<2>} - 1_{<2>}.

This is a theorem-facing selector: a source may emit the quotient over the
cyclic subgroup <2> and its 7-coset, rather than listing all 24 residues.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25
from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    primitive_word,
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR


GENERATOR = 2
COSET_REPRESENTATIVE = 7


@dataclass(frozen=True)
class Conductor39CosetSelector:
    level: int
    generator: int
    generator_order: int
    coset_representative: int
    kernel_residues: tuple[int, ...]
    coset_residues: tuple[int, ...]
    kernel_size: int
    coset_size: int
    quotient_order: int
    primitive_support: int
    negative_layer_residues: tuple[int, ...]
    positive_layer_residues: tuple[int, ...]
    kernel_equals_negative_layer: bool
    coset_equals_positive_layer: bool
    coset_quotient_word_equals_primitive: bool
    p_mod_39: int
    p_in_coset: bool
    p_swaps_cosets: bool
    p_squared_preserves_cosets: bool
    compact_pair_count: int
    mixed_tensor_ok: bool
    primitive_unit_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def multiplicative_order(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise ValueError("value is not a unit")
    current = 1
    for order in range(1, modulus + 1):
        current = (current * value) % modulus
        if current == 1:
            return order
    raise AssertionError("order search exceeded modulus")


def cyclic_subgroup(generator: int, modulus: int) -> tuple[int, ...]:
    order = multiplicative_order(generator, modulus)
    return tuple(sorted(pow(generator, exponent, modulus) for exponent in range(order)))


def multiply_residue_set(residue: int, source: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple(sorted((residue * item) % modulus for item in source))


def coset_quotient_word(kernel: tuple[int, ...], coset: tuple[int, ...]) -> dict[int, int]:
    word = {residue: -1 for residue in kernel}
    for residue in coset:
        word[residue] = word.get(residue, 0) + 1
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def profile_yang_y507_conductor39_coset_selector() -> Conductor39CosetSelector:
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()
    word = primitive_word()
    kernel = cyclic_subgroup(GENERATOR, CONDUCTOR)
    coset = multiply_residue_set(COSET_REPRESENTATIVE, kernel, CONDUCTOR)
    negative = tuple(sorted(residue for residue, coefficient in word.items() if coefficient == -1))
    positive = tuple(sorted(residue for residue, coefficient in word.items() if coefficient == 1))
    quotient_word = coset_quotient_word(kernel, coset)
    p_mod = P25 % CONDUCTOR
    p_kernel_image = multiply_residue_set(p_mod, kernel, CONDUCTOR)
    p_coset_image = multiply_residue_set(p_mod, coset, CONDUCTOR)
    p2_kernel_image = multiply_residue_set((p_mod * p_mod) % CONDUCTOR, kernel, CONDUCTOR)
    p2_coset_image = multiply_residue_set((p_mod * p_mod) % CONDUCTOR, coset, CONDUCTOR)
    units = tuple(residue for residue in range(CONDUCTOR) if gcd(residue, CONDUCTOR) == 1)
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and mixed.row_ok
        and CONDUCTOR == 39
        and GENERATOR == 2
        and COSET_REPRESENTATIVE == 7
        and multiplicative_order(GENERATOR, CONDUCTOR) == 12
        and len(kernel) == 12
        and len(coset) == 12
        and set(kernel).isdisjoint(coset)
        and tuple(sorted(kernel + coset)) == units
        and kernel == negative
        and coset == positive
        and quotient_word == word
        and p_mod == 23
        and p_mod in coset
        and p_kernel_image == coset
        and p_coset_image == kernel
        and p2_kernel_image == kernel
        and p2_coset_image == coset
        and not direct_closer
    )
    return Conductor39CosetSelector(
        level=CONDUCTOR,
        generator=GENERATOR,
        generator_order=multiplicative_order(GENERATOR, CONDUCTOR),
        coset_representative=COSET_REPRESENTATIVE,
        kernel_residues=kernel,
        coset_residues=coset,
        kernel_size=len(kernel),
        coset_size=len(coset),
        quotient_order=2,
        primitive_support=len(word),
        negative_layer_residues=negative,
        positive_layer_residues=positive,
        kernel_equals_negative_layer=kernel == negative,
        coset_equals_positive_layer=coset == positive,
        coset_quotient_word_equals_primitive=quotient_word == word,
        p_mod_39=p_mod,
        p_in_coset=p_mod in coset,
        p_swaps_cosets=p_kernel_image == coset and p_coset_image == kernel,
        p_squared_preserves_cosets=p2_kernel_image == kernel and p2_coset_image == coset,
        compact_pair_count=len(kernel),
        mixed_tensor_ok=mixed.row_ok,
        primitive_unit_ok=primitive.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "U_chi is the 12-pair coset quotient 1_{7<2>} - 1_{<2>} in "
            "(Z/39Z)^*."
        ),
        first_missing_clause=(
            "coset selection is a compact source descriptor, not the finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask source theorems for the cyclic quotient product over <2> and "
            "7<2>; reject claims that lose the quotient character or only project "
            "to a prime axis"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_coset_selector()
    print("p25 KSY-y Yang Y_507 conductor-39 coset-selector gate")
    print(f"level={profile.level}")
    print(f"generator={profile.generator}")
    print(f"generator_order={profile.generator_order}")
    print(f"coset_representative={profile.coset_representative}")
    print(f"kernel_residues={profile.kernel_residues}")
    print(f"coset_residues={profile.coset_residues}")
    print("layers")
    print(f"  negative_layer_residues={profile.negative_layer_residues}")
    print(f"  positive_layer_residues={profile.positive_layer_residues}")
    print(f"  kernel_equals_negative_layer={int(profile.kernel_equals_negative_layer)}")
    print(f"  coset_equals_positive_layer={int(profile.coset_equals_positive_layer)}")
    print(f"  coset_quotient_word_equals_primitive={int(profile.coset_quotient_word_equals_primitive)}")
    print("frobenius")
    print(f"  p_mod_39={profile.p_mod_39}")
    print(f"  p_in_coset={int(profile.p_in_coset)}")
    print(f"  p_swaps_cosets={int(profile.p_swaps_cosets)}")
    print(f"  p_squared_preserves_cosets={int(profile.p_squared_preserves_cosets)}")
    print("checks")
    print(f"  kernel_size={profile.kernel_size}")
    print(f"  coset_size={profile.coset_size}")
    print(f"  quotient_order={profile.quotient_order}")
    print(f"  primitive_support={profile.primitive_support}")
    print(f"  compact_pair_count={profile.compact_pair_count}")
    print(f"  mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print(f"  primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  U_chi_is_12_pair_coset_quotient_7_times_subgroup_2_over_subgroup_2=1")
    print("  frobenius_p_swaps_the_two_cosets=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_coset_selector_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 coset-selector regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
