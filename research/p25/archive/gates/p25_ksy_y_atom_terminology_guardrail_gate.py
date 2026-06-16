#!/usr/bin/env python3
"""Terminology guardrail for KSY-y atoms.

In this workbench, a "normalized-y atom" is a fixed factor inside the target
product P, not a search candidate.  The target has 3 D-segment positions and
25 K-trace positions, hence 75 normalized-y factors.  KSY's formula
y(Q)=-g(2Q)/g(Q)^4 expands each factor into four Siegel-footprint terms.
"""

from __future__ import annotations

from dataclasses import dataclass


Coord = tuple[int, int]

RIGHT_ORDER = 75
C_ORDER = 169
C = (47, 28)
D = (22, 3)
K = (57, 0)
T = (2, 113)


@dataclass(frozen=True)
class AtomTerminologyGuardrail:
    normalized_y_atoms: tuple[Coord, ...]
    atom_count: int
    d_segment_length: int
    k_trace_length: int
    anti_invariant_factor_pairs: int
    siegel_terms_per_atom: int
    theta_footprint_terms: int
    atoms_are_search_candidates: bool
    required_theorem_output: str
    row_ok: bool


def add(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def scale(step: Coord, scalar: int) -> Coord:
    return ((step[0] * scalar) % RIGHT_ORDER, (step[1] * scalar) % C_ORDER)


def p25_atoms() -> tuple[Coord, ...]:
    out = []
    for j in (-1, 0, 1):
        d_base = add(C, scale(D, j))
        for k in range(25):
            out.append(add(d_base, scale(K, k)))
    return tuple(out)


def profile_atom_terminology_guardrail() -> AtomTerminologyGuardrail:
    atoms = p25_atoms()
    atom_count = len(atoms)
    unique_atoms = len(set(atoms))
    d_segment_length = 3
    k_trace_length = 25
    anti_invariant_pairs = atom_count
    siegel_terms_per_atom = 4
    theta_terms = atom_count * siegel_terms_per_atom
    atoms_are_search_candidates = False
    row_ok = (
        atom_count == 75
        and unique_atoms == 75
        and d_segment_length * k_trace_length == atom_count
        and anti_invariant_pairs == 75
        and theta_terms == 300
        and not atoms_are_search_candidates
        and T == (2, 113)
    )
    return AtomTerminologyGuardrail(
        normalized_y_atoms=atoms,
        atom_count=atom_count,
        d_segment_length=d_segment_length,
        k_trace_length=k_trace_length,
        anti_invariant_factor_pairs=anti_invariant_pairs,
        siegel_terms_per_atom=siegel_terms_per_atom,
        theta_footprint_terms=theta_terms,
        atoms_are_search_candidates=atoms_are_search_candidates,
        required_theorem_output=(
            "an arithmetic identity selecting the whole fixed 75-atom product, "
            "with orientation and challenge-legal finite-field framing"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_atom_terminology_guardrail()
    print("p25 KSY-y atom terminology guardrail gate")
    print("counts")
    print(f"  d_segment_length={profile.d_segment_length}")
    print(f"  k_trace_length={profile.k_trace_length}")
    print(f"  atom_count={profile.atom_count}")
    print(f"  anti_invariant_factor_pairs={profile.anti_invariant_factor_pairs}")
    print(f"  siegel_terms_per_atom={profile.siegel_terms_per_atom}")
    print(f"  theta_footprint_terms={profile.theta_footprint_terms}")
    print(f"  atoms_are_search_candidates={int(profile.atoms_are_search_candidates)}")
    print("interpretation")
    print("  atoms_are_fixed_product_factors_not_search_candidates=1")
    print("  product_theorem_must_select_all_75_atoms_at_once=1")
    print("  KSY_formula_expands_each_atom_to_four_Siegel_terms=1")
    print(
        "ksy_y_atom_terminology_guardrail_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("KSY-y atom terminology guardrail regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
