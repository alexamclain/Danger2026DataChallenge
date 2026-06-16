#!/usr/bin/env python3
"""Primitive-D factor word for the compact p25 Y_507 target.

Yang residues live in the one-dimensional X_1(507) coordinate a.  The earlier
Kubert-Lang primitive-D word uses q = 169*row + 3*c, so the conversion is

    q = 172*a mod 507,

because 172 is 1 mod 3 and 3 mod 169.  After applying the D inverse used by
the primitive-word gate, the compact normalized-y target becomes exactly

    Y_507 = [2]^*U_507 / U_507^4

for the same primitive bridge word U_507 = z^121(1+z+z^2)(1-z^263).
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_modular_period_certificate_gate import (
    profile_yang_y507_modular_period_certificate,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate import (
    profile_primitive_word,
)


YANG_TO_Q_MULTIPLIER = 172


@dataclass(frozen=True)
class PrimitiveFactorBlock:
    name: str
    coefficient: int
    support: tuple[int, ...]
    step_pattern: tuple[int, ...]
    ok: bool


@dataclass(frozen=True)
class YangY507PrimitiveFactorWord:
    yang_to_q_multiplier: int
    d_q_inverse: int
    yang_to_primitive_multiplier: int
    u_primitive_word: tuple[tuple[int, int], ...]
    y507_primitive_word: tuple[tuple[int, int], ...]
    doubled_u_minus_four_u_word: tuple[tuple[int, int], ...]
    y507_equals_doubled_u_minus_four_u: bool
    factor_blocks: tuple[PrimitiveFactorBlock, ...]
    primitive_word_gate_ok: bool
    y507_modular_period_certificate_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def to_primitive_exponent(yang_residue: int, d_q_inverse: int) -> int:
    return (YANG_TO_Q_MULTIPLIER * yang_residue * d_q_inverse) % QUOTIENT_LEVEL


def word_from_yang_exponents(yang_exponents: tuple[tuple[int, int], ...], d_q_inverse: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in yang_exponents:
        exponent = to_primitive_exponent(residue, d_q_inverse)
        out[exponent] = out.get(exponent, 0) + coefficient
    return dict(sorted((exponent, coefficient) for exponent, coefficient in out.items() if coefficient))


def doubled_u_minus_four_u(u_word: tuple[tuple[int, int], ...]) -> dict[int, int]:
    out: dict[int, int] = {}
    for exponent, coefficient in u_word:
        doubled = (2 * exponent) % QUOTIENT_LEVEL
        out[doubled] = out.get(doubled, 0) + coefficient
        out[exponent] = out.get(exponent, 0) - 4 * coefficient
    return dict(sorted((exponent, coefficient) for exponent, coefficient in out.items() if coefficient))


def block(name: str, coefficient: int, support: tuple[int, ...], expected: tuple[int, ...]) -> PrimitiveFactorBlock:
    steps = tuple((right - left) % QUOTIENT_LEVEL for left, right in zip(support, support[1:]))
    return PrimitiveFactorBlock(
        name=name,
        coefficient=coefficient,
        support=support,
        step_pattern=steps,
        ok=support == expected and (steps in ((), (1, 1), (2, 2))),
    )


def factor_blocks(y_word: dict[int, int]) -> tuple[PrimitiveFactorBlock, ...]:
    by_coefficient: dict[int, list[int]] = {}
    for exponent, coefficient in y_word.items():
        by_coefficient.setdefault(coefficient, []).append(exponent)
    return (
        block("minus_four_original_U_numerator", -4, tuple(by_coefficient[-4]), (121, 122, 123)),
        block("plus_one_doubled_U_numerator", 1, tuple(by_coefficient[1]), (242, 244, 246)),
        block("minus_one_doubled_U_denominator", -1, tuple(by_coefficient[-1]), (261, 263, 265)),
        block("plus_four_original_U_denominator", 4, tuple(by_coefficient[4]), (384, 385, 386)),
    )


def profile_yang_y507_primitive_factor_word() -> YangY507PrimitiveFactorWord:
    primitive = profile_primitive_word()
    y507 = profile_yang_y507_modular_period_certificate()
    y_word = word_from_yang_exponents(y507.y507_exponents, primitive.d_q_inverse)
    from_u = doubled_u_minus_four_u(primitive.quotient_word)
    blocks = factor_blocks(y_word)
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and y507.row_ok
        and YANG_TO_Q_MULTIPLIER == 172
        and primitive.d_q_inverse == 94
        and (YANG_TO_Q_MULTIPLIER * primitive.d_q_inverse) % QUOTIENT_LEVEL == 451
        and primitive.quotient_word
        == (
            (121, 1),
            (122, 1),
            (123, 1),
            (384, -1),
            (385, -1),
            (386, -1),
        )
        and y_word == from_u
        and tuple(sorted(y_word.items()))
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
        and all(item.ok for item in blocks)
        and not direct_closer
    )
    return YangY507PrimitiveFactorWord(
        yang_to_q_multiplier=YANG_TO_Q_MULTIPLIER,
        d_q_inverse=primitive.d_q_inverse,
        yang_to_primitive_multiplier=(YANG_TO_Q_MULTIPLIER * primitive.d_q_inverse) % QUOTIENT_LEVEL,
        u_primitive_word=primitive.quotient_word,
        y507_primitive_word=tuple(sorted(y_word.items())),
        doubled_u_minus_four_u_word=tuple(sorted(from_u.items())),
        y507_equals_doubled_u_minus_four_u=y_word == from_u,
        factor_blocks=blocks,
        primitive_word_gate_ok=primitive.row_ok,
        y507_modular_period_certificate_ok=y507.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Y_507 is exactly [2]^*U_507/U_507^4 in the primitive-D word "
            "coordinate, with U_507=z^121(1+z+z^2)(1-z^263)"
        ),
        first_missing_clause=(
            "the primitive factor word still needs a theorem proving its "
            "finite-field value/divisor identity and DANGER3 extraction"
        ),
        recommendation=(
            "use this primitive factor word as the compact source-query form "
            "when searching for Kubert-Lang/Sprang/KSY theorem hits"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_primitive_factor_word()
    print("p25 KSY-y Yang Y_507 primitive-factor word gate")
    print("coordinate_change")
    print(f"  yang_to_q_multiplier={profile.yang_to_q_multiplier}")
    print(f"  d_q_inverse={profile.d_q_inverse}")
    print(f"  yang_to_primitive_multiplier={profile.yang_to_primitive_multiplier}")
    print("words")
    print(f"  u_primitive_word={profile.u_primitive_word}")
    print(f"  y507_primitive_word={profile.y507_primitive_word}")
    print(f"  doubled_u_minus_four_u_word={profile.doubled_u_minus_four_u_word}")
    print(
        "  y507_equals_doubled_u_minus_four_u="
        f"{int(profile.y507_equals_doubled_u_minus_four_u)}"
    )
    print("factor_blocks")
    for item in profile.factor_blocks:
        print(
            "  "
            f"{item.name}: coeff={item.coefficient} support={item.support} "
            f"step_pattern={item.step_pattern} ok={int(item.ok)}"
        )
    print("checks")
    print(f"  primitive_word_gate_ok={int(profile.primitive_word_gate_ok)}")
    print(f"  y507_modular_period_certificate_ok={int(profile.y507_modular_period_certificate_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  Y_507_primitive_word_is_doubled_U_minus_four_U=1")
    print("  compact_source_query_form_is_z121_block_and_its_doubling=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_primitive_factor_word_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 primitive-factor word regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
