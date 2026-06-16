#!/usr/bin/env python3
"""p23 Hasse trace-lattice model for high-v2 and odd residue conditioning.

This enumerates the p23 trace lattice:

    |t| <= floor(2*sqrt(p))
    p + 1 - t is divisible by 2^d

and measures how the p23 target odd trace residues modulo small primes cut
that lattice.  It is a probability-model helper, not a sampler and not a
verifier.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from x16_trace_residue_calibration import P23, P23_TRACES


@dataclass
class Accum:
    count: int = 0
    mass: float = 0.0

    def add(self, weight: float) -> None:
        self.count += 1
        self.mass += weight


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def trace_weight(t: int, p: int) -> float:
    root_p = math.sqrt(p)
    u = t / (2.0 * root_p)
    if abs(u) > 1.0:
        return 0.0
    return math.sqrt(max(0.0, 1.0 - u * u)) / (math.pi * root_p)


def lattice_traces(p: int, d: int, bound: int):
    modulus = 1 << d
    residue = (p + 1) % modulus
    lo = -bound
    hi = bound
    first = lo + ((residue - lo) % modulus)
    t = first
    while t <= hi:
        yield t
        t += modulus


def fmt(acc: Accum, total: Accum) -> str:
    count_rate = acc.count / total.count if total.count else 0.0
    mass_rate = acc.mass / total.mass if total.mass else 0.0
    return f"{acc.count}/{total.count}:{count_rate:.6f} mass={mass_rate:.6f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=P23)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19])
    ap.add_argument("--d-min", type=int, default=16)
    ap.add_argument("--d-max", type=int, default=40)
    args = ap.parse_args()

    p = args.p
    if p != P23:
        raise SystemExit("this helper is currently parameterized by the fixed p23 target residues")

    bound = math.isqrt(4 * p)
    residues = {ell: {t % ell for t in P23_TRACES} for ell in args.ells}

    print("p23 trace-lattice high-v2 / odd-residue model")
    print(f"p={p}")
    print(f"hasse_trace_bound=floor(2sqrt(p))={bound}")
    print(f"ells={args.ells}")
    print("target_traces=" + ",".join(str(t) for t in P23_TRACES))
    for t in P23_TRACES:
        n = p + 1 - t
        print(f"target_trace_detail t={t} v2_p_plus_1_minus_t={v2(n)} oddpart={n >> v2(n)}")
    print("target_residues=" + ",".join(f"ell{ell}:{sorted(residues[ell])}" for ell in args.ells))
    print()

    print("d total_count total_mass prefix conditional_count_rate conditional_mass_rate ideal_independent")
    for d in range(args.d_min, args.d_max + 1):
        total = Accum()
        prefix_acc = [Accum() for _ in args.ells]
        for t in lattice_traces(p, d, bound):
            w = trace_weight(t, p)
            total.add(w)
            ok = True
            for i, ell in enumerate(args.ells):
                ok = ok and (t % ell in residues[ell])
                if ok:
                    prefix_acc[i].add(w)

        ideal = 1.0
        for i, ell in enumerate(args.ells):
            ideal *= len(residues[ell]) / ell
            acc = prefix_acc[i]
            print(
                f"{d:2d} {total.count:7d} {total.mass:.12e} "
                f"through_ell={ell:2d} {fmt(acc, total)} ideal={ideal:.6e}"
            )
        print()


if __name__ == "__main__":
    main()
