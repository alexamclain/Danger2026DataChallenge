#!/usr/bin/env python3
"""Toy verifier for a phase-lifted decomposed CM tower certificate.

This is a certificate-shape experiment, not a producer.  It uses the familiar
small CM cycle

    D = -5000, h = 30 = 2 * 3 * 5 over F_1259

and treats it as the p24 analogue

    h = 2 * 157 * 211 * 3107441.

The generated artifact is:

* a top quotient polynomial of degree 2;
* a relative child relation of degree 3 above the top root;
* one selected recovery polynomial of degree 5 in j.

The verifier checks only the supplied root chain and the selected recovery
root.  It does not need the full 30-root class polynomial or the dense
quotient/recovery relation.  In p24 terms, the same finite surface would have
about

    2 + 2*157 + 314*211 + 3107441 = 3174011

field coefficients, far below sqrt(10^24+7).  The unsolved theorem is how to
produce the embedded relative relations and the selected recovery polynomial
without first enumerating the class orbit.
"""

from __future__ import annotations

from dataclasses import dataclass

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)


QUOTIENT_FACTORS = [2, 3]
RECOVERY_SIZE = H // (QUOTIENT_FACTORS[0] * QUOTIENT_FACTORS[1])


@dataclass(frozen=True)
class LevelRelation:
    parent_count: int
    child_factor: int
    child_count: int
    parent_values: list[int]
    child_values: list[int]
    coefficient_polys: list[list[int]]
    cross_zero_count: int


@dataclass(frozen=True)
class TowerCertificate:
    cycle: list[int]
    top_poly: list[int]
    relations: list[LevelRelation]
    selected_chain_indices: list[int]
    selected_chain_values: list[int]
    selected_recovery_poly: list[int]
    selected_j: int


def eval_poly(poly: list[int], x: int, q: int = Q) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % q
    return value


def interpolate(xs: list[int], ys: list[int], q: int = Q) -> list[int]:
    """Interpolate the unique polynomial of degree < len(xs)."""
    if len(xs) != len(ys):
        raise ValueError("xs/ys length mismatch")
    if len(set(xs)) != len(xs):
        raise ValueError("interpolation points not distinct")
    coeffs = [0] * len(xs)
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        numerator = [1]
        denominator = 1
        for j, xj in enumerate(xs):
            if i == j:
                continue
            new = [0] * (len(numerator) + 1)
            for k, coeff in enumerate(numerator):
                new[k] = (new[k] - coeff * xj) % q
                new[k + 1] = (new[k + 1] + coeff) % q
            numerator = new
            denominator = denominator * ((xi - xj) % q) % q
        scale = yi * pow(denominator, -1, q) % q
        for k, coeff in enumerate(numerator):
            coeffs[k] = (coeffs[k] + scale * coeff) % q
    return coeffs


def quotient_periods(cycle: list[int], quotient_size: int, q: int = Q) -> list[int]:
    h = len(cycle)
    subgroup_size = h // quotient_size
    return [
        sum(cycle[(r + quotient_size * k) % h] for k in range(subgroup_size)) % q
        for r in range(quotient_size)
    ]


def specialize_relation(relation: LevelRelation, parent_value: int, q: int = Q) -> list[int]:
    coeffs = [eval_poly(poly, parent_value, q) for poly in relation.coefficient_polys]
    coeffs.append(1)
    return coeffs


def build_relation(
    parent_values: list[int],
    child_values: list[int],
    parent_count: int,
    child_factor: int,
    q: int = Q,
) -> LevelRelation:
    child_polys: list[list[int]] = []
    for parent in range(parent_count):
        children = [child_values[parent + parent_count * v] for v in range(child_factor)]
        child_polys.append(monic_poly_from_roots(children, q))

    coefficient_polys = [
        interpolate(parent_values, [poly[i] for poly in child_polys], q)
        for i in range(child_factor)
    ]

    cross_zero_count = 0
    for parent, z in enumerate(parent_values):
        specialized = specialize_relation(
            LevelRelation(
                parent_count=parent_count,
                child_factor=child_factor,
                child_count=parent_count * child_factor,
                parent_values=parent_values,
                child_values=child_values,
                coefficient_polys=coefficient_polys,
                cross_zero_count=0,
            ),
            z,
            q,
        )
        for other_parent in range(parent_count):
            if other_parent == parent:
                continue
            for v in range(child_factor):
                y = child_values[other_parent + parent_count * v]
                if eval_poly(specialized, y, q) == 0:
                    cross_zero_count += 1

    return LevelRelation(
        parent_count=parent_count,
        child_factor=child_factor,
        child_count=parent_count * child_factor,
        parent_values=parent_values,
        child_values=child_values,
        coefficient_polys=coefficient_polys,
        cross_zero_count=cross_zero_count,
    )


def build_certificate(cycle: list[int]) -> TowerCertificate:
    quotient_sizes: list[int] = []
    size = 1
    for factor in QUOTIENT_FACTORS:
        size *= factor
        quotient_sizes.append(size)

    level_values = [quotient_periods(cycle, size, Q) for size in quotient_sizes]
    top_poly = monic_poly_from_roots(level_values[0], Q)

    relations = [
        build_relation(
            parent_values=level_values[i - 1],
            child_values=level_values[i],
            parent_count=quotient_sizes[i - 1],
            child_factor=QUOTIENT_FACTORS[i],
            q=Q,
        )
        for i in range(1, len(quotient_sizes))
    ]

    selected_fine_index = 0
    fine_quotient = quotient_sizes[-1]
    selected_roots = [
        cycle[(selected_fine_index + fine_quotient * k) % H]
        for k in range(RECOVERY_SIZE)
    ]
    selected_recovery_poly = monic_poly_from_roots(selected_roots, Q)
    selected_chain_indices = [0 for _ in quotient_sizes]
    selected_chain_values = [values[0] for values in level_values]
    selected_j = selected_roots[0]
    return TowerCertificate(
        cycle=cycle,
        top_poly=top_poly,
        relations=relations,
        selected_chain_indices=selected_chain_indices,
        selected_chain_values=selected_chain_values,
        selected_recovery_poly=selected_recovery_poly,
        selected_j=selected_j,
    )


def verify_certificate(cert: TowerCertificate, q: int = Q) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True
    if eval_poly(cert.top_poly, cert.selected_chain_values[0], q) != 0:
        ok = False
        messages.append("top root failed")
    parent_value = cert.selected_chain_values[0]
    for level, relation in enumerate(cert.relations, start=1):
        child_value = cert.selected_chain_values[level]
        specialized = specialize_relation(relation, parent_value, q)
        if eval_poly(specialized, child_value, q) != 0:
            ok = False
            messages.append(f"relation level {level} failed")
        parent_value = child_value
    if eval_poly(cert.selected_recovery_poly, cert.selected_j, q) != 0:
        ok = False
        messages.append("selected recovery root failed")
    return ok, messages


def selected_child_polys(cert: TowerCertificate, q: int = Q) -> list[list[int]]:
    out: list[list[int]] = []
    parent_value = cert.selected_chain_values[0]
    for relation in cert.relations:
        out.append(specialize_relation(relation, parent_value, q))
        parent_index = len(out)
        parent_value = cert.selected_chain_values[parent_index]
    return out


def verify_selected_chain_artifact(
    top_poly: list[int],
    child_polys: list[list[int]],
    recovery_poly: list[int],
    chain_values: list[int],
    selected_j: int,
    q: int = Q,
) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True
    if eval_poly(top_poly, chain_values[0], q) != 0:
        ok = False
        messages.append("top root failed")
    for idx, child_poly in enumerate(child_polys):
        if eval_poly(child_poly, chain_values[idx + 1], q) != 0:
            ok = False
            messages.append(f"selected child level {idx + 1} failed")
    if eval_poly(recovery_poly, selected_j, q) != 0:
        ok = False
        messages.append("selected recovery root failed")
    return ok, messages


def coefficient_slots(cert: TowerCertificate) -> int:
    # Exclude monic leading coefficients.
    relation_slots = sum(
        len(poly)
        for relation in cert.relations
        for poly in relation.coefficient_polys
    )
    return (len(cert.top_poly) - 1) + relation_slots + (len(cert.selected_recovery_poly) - 1)


def selected_chain_slots(cert: TowerCertificate) -> int:
    # Exclude monic leading coefficients in the selected specialized child
    # polynomials and in the selected recovery polynomial.
    child_slots = sum(relation.child_factor for relation in cert.relations)
    return (len(cert.top_poly) - 1) + child_slots + (len(cert.selected_recovery_poly) - 1)


def p24_slot_accounting() -> tuple[int, int, int, int]:
    f1, f2, f3 = 2, 157, 211
    recovery = 3107441
    top = f1
    first_refine = f1 * f2
    second_refine = f1 * f2 * f3
    total = top + first_refine + second_refine + recovery
    return top, first_refine, second_refine, total


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    cert = build_certificate(cycle)
    verified, messages = verify_certificate(cert, Q)
    selected_polys = selected_child_polys(cert, Q)
    selected_verified, selected_messages = verify_selected_chain_artifact(
        cert.top_poly,
        selected_polys,
        cert.selected_recovery_poly,
        cert.selected_chain_values,
        cert.selected_j,
        Q,
    )
    hilbert_check = int(pari(f"subst({hilbert}, x, Mod({cert.selected_j},{Q}))")) == 0

    print("phase-lifted tower certificate toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"quotient_factors={QUOTIENT_FACTORS}")
    print(f"recovery_size={RECOVERY_SIZE}")
    print()

    print("certificate")
    print(f"  top_poly_degree={len(cert.top_poly)-1}")
    print(f"  top_poly_coeffs_ascending={cert.top_poly}")
    for idx, relation in enumerate(cert.relations, start=1):
        degrees = [len(poly) - 1 for poly in relation.coefficient_polys]
        print(
            f"  relation_level={idx} parent_count={relation.parent_count} "
            f"child_factor={relation.child_factor} child_count={relation.child_count} "
            f"coefficient_poly_degrees={degrees} "
            f"cross_zero_count={relation.cross_zero_count}"
        )
        for coeff_index, poly in enumerate(relation.coefficient_polys):
            print(f"    coeff_Y^{coeff_index}_as_parent_poly={poly}")
    for idx, poly in enumerate(selected_polys, start=1):
        print(f"  selected_child_level={idx}_coeffs_ascending={poly}")
    print(f"  selected_chain_values={cert.selected_chain_values}")
    print(f"  selected_recovery_degree={len(cert.selected_recovery_poly)-1}")
    print(f"  selected_recovery_coeffs_ascending={cert.selected_recovery_poly}")
    print(f"  selected_j={cert.selected_j}")
    print()

    print("verification")
    print(f"  chain_and_recovery_verify={int(verified)}")
    print(f"  verification_messages={messages}")
    print(f"  selected_chain_artifact_verify={int(selected_verified)}")
    print(f"  selected_chain_messages={selected_messages}")
    print(f"  selected_j_satisfies_full_H_D_sanity_check={int(hilbert_check)}")
    print()

    top, first_refine, second_refine, p24_total = p24_slot_accounting()
    print("accounting")
    print(f"  toy_certificate_slots_excluding_monic={coefficient_slots(cert)}")
    print(f"  toy_selected_chain_slots_excluding_monic={selected_chain_slots(cert)}")
    print(f"  toy_full_h={H}")
    print(f"  toy_slots_over_h={coefficient_slots(cert) / H:.6f}")
    print(f"  toy_selected_chain_slots_over_h={selected_chain_slots(cert) / H:.6f}")
    print(f"  p24_top_slots={top}")
    print(f"  p24_first_refinement_slots={first_refine}")
    print(f"  p24_second_refinement_slots={second_refine}")
    print("  p24_selected_recovery_slots=3107441")
    print(f"  p24_total_slots={p24_total}")
    p24_selected_chain_total = 2 + 157 + 211 + 3107441
    print(f"  p24_selected_chain_slots={p24_selected_chain_total}")
    print("  p24_sqrt=1000000000000")
    print(f"  p24_total_over_sqrt={p24_total / 10**12:.12f}")
    print(f"  p24_selected_chain_over_sqrt={p24_selected_chain_total / 10**12:.12f}")
    print()

    print("interpretation")
    print("  verifier_uses_selected_root_chain_not_full_class_set=1")
    print("  selected_recovery_polynomial_avoids_dense_h_sized_recovery_table=1")
    print("  artifact_is_sub_sqrt_if_produced_by_class_field_theorem=1")
    print("  toy_generation_still_used_full_embedded_cycle=1")
    print(
        "conclusion=phase_lifted_tower_certificate_surface_is_sub_sqrt_but_"
        "producer_theorem_remains_the_missing_step"
    )


if __name__ == "__main__":
    main()
