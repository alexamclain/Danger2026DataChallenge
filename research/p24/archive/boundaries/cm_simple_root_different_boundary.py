#!/usr/bin/env python3
"""Simple-root/different units do not certify the Fitting determinant.

For an ordinary split prime, the Hilbert class polynomial can be squarefree
modulo q; equivalently the CM algebra is etale and the derivative at every
CM root is nonzero.  This is a useful local fact, but it does not say that a
separate Schubert/Fitting determinant-line section is a unit at the selected
CM point.

This pinned small actual-CM row checks the simple-root fact and contrasts it
with two zero-section controls:

* the elementary section X-j_0 vanishes at one simple CM root;
* a forced singular determinant-line control has all coordinate entries
  nonzero while its determinant is zero.
"""

from __future__ import annotations

import argparse

from cypari2 import Pari

from trace_gcd_phase_divisor_identity_holdout import determinant_control


def hilbert_simple_root_data(D: int, q: int) -> dict[str, object]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    H = pari.polclass(D)
    degree = int(pari.poldegree(H))
    roots = sorted(int(root) for root in pari.polrootsmod(H, q))
    derivative = pari.deriv(H)
    derivative_values = [
        int(pari.subst(derivative, "x", root)) % q
        for root in roots
    ]
    zero_derivative_roots = [
        root
        for root, value in zip(roots, derivative_values)
        if value == 0
    ]
    return {
        "degree": degree,
        "root_count": len(roots),
        "roots": roots,
        "derivative_values": derivative_values,
        "zero_derivative_roots": zero_derivative_roots,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=13463)
    parser.add_argument("--q-stop", type=int, default=13464)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=8)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int, default=140)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    simple = hilbert_simple_root_data(args.only_D, args.only_q)
    roots = simple["roots"]
    derivative_values = simple["derivative_values"]
    zero_root = roots[0]
    section_values = [(root - zero_root) % args.only_q for root in roots]
    section_zero_count = sum(value == 0 for value in section_values)
    derivative_at_zero_root = derivative_values[0]
    control = determinant_control(args)

    print("CM simple-root/different boundary")
    print(f"D={args.only_D}")
    print(f"q={args.only_q}")
    print(f"class_polynomial_degree={simple['degree']}")
    print(f"root_count_mod_q={simple['root_count']}")
    print(
        "class_polynomial_split_squarefree="
        f"{int(simple['root_count'] == simple['degree'] and not simple['zero_derivative_roots'])}"
    )
    print(f"zero_derivative_count={len(simple['zero_derivative_roots'])}")
    print(f"sample_roots={roots[:12]}")
    print(f"sample_derivative_values={derivative_values[:12]}")
    print("simple_vanishing_section")
    print(f"  section=X-{zero_root}")
    print(f"  section_zero_count={section_zero_count}")
    print(f"  derivative_unit_at_zero_root={int(derivative_at_zero_root != 0)}")
    print("determinant_zero_control")
    for key, value in control.items():
        print(f"  {key}={value}")
    print("interpretation")
    print("  split_squarefree_Hilbert_roots_certify_the_CM_algebra_is_etale=1")
    print("  an_etale_CM_point_can_still_lie_on_an_unrelated_section_divisor=1")
    print("  simple_root_derivative_units_do_not_detect_Fitting_determinant_units=1")
    print("  p24_needs_the_selected_tail_determinant_line_itself_not_only_the_CM_different=1")
    print("conclusion=reported_cm_simple_root_different_boundary")


if __name__ == "__main__":
    main()
