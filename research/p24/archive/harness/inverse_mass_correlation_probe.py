#!/usr/bin/env python3
"""Small-field probe for inverse-tree mass as a predictor of full success.

For fixed A, the DANGER3 x-map can be inverted exactly.  A tempting idea is to
rank A values by the size of a shallow inverse tree from the final Z=0 target.
This script checks, on a full small field, whether that ranking is more than a
partial-depth 2-adic filter.

The output is a calibration only.  It does not search p24.
"""

from __future__ import annotations

import argparse
from collections import Counter
from math import isqrt


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def sqrt_mod_prime(a: int, p: int) -> tuple[int, ...]:
    a %= p
    if a == 0:
        return (0,)
    if legendre(a, p) != 1:
        return ()
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return tuple(sorted({r, (-r) % p}))

    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        probe = t * t % p
        while probe != 1:
            probe = probe * probe % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return tuple(sorted({r, (-r) % p}))


def verifier_k(p: int) -> int:
    q = isqrt(p)
    return (q + 1 + isqrt(4 * q)).bit_length()


def final_targets(p: int, A: int) -> set[int]:
    roots = {0}
    inv2 = (p + 1) // 2
    for r in sqrt_mod_prime(A * A - 4, p):
        roots.add((-A + r) * inv2 % p)
        roots.add((-A - r) * inv2 % p)
    return roots


def inverse_preimages(p: int, A: int, t: int) -> set[int]:
    out: set[int] = set()
    inv2 = (p + 1) // 2
    for s in sqrt_mod_prime(t * t + A * t + 1, p):
        for y in {(2 * (t + s)) % p, (2 * (t - s)) % p}:
            for r in sqrt_mod_prime(y * y - 4, p):
                for x in {((y + r) * inv2) % p, ((y - r) * inv2) % p}:
                    if x != 0 and (x * x + A * x + 1) % p != 0:
                        out.add(x)
    return out


def inverse_tree_size(p: int, A: int, depth: int) -> int:
    states = final_targets(p, A)
    for _ in range(depth):
        nxt: set[int] = set()
        for t in states:
            nxt.update(inverse_preimages(p, A, t))
        states = nxt
        if not states:
            break
    return len(states)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=10007)
    ap.add_argument("--rank-depth", type=int, default=0)
    args = ap.parse_args()

    p = args.p
    k = verifier_k(p)
    full_depth = k - 1
    rank_depth = args.rank_depth or max(1, full_depth // 2)

    rows = []
    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        mass = inverse_tree_size(p, A, rank_depth)
        full = inverse_tree_size(p, A, full_depth) > 0
        rows.append((mass, full, A))

    total = len(rows)
    hits = sum(1 for _, full, _ in rows if full)
    base = hits / total if total else 0.0
    hist = Counter(mass for mass, _, _ in rows)
    rows.sort(key=lambda row: (row[0], row[2]), reverse=True)

    print("inverse-mass correlation probe")
    print(f"p={p}")
    print(f"k={k}")
    print(f"rank_depth={rank_depth}")
    print(f"full_depth={full_depth}")
    print(f"nonsingular_A={total}")
    print(f"full_hits={hits}")
    print(f"base_hit_rate={base:.8f}")
    print("mass_hist=" + ",".join(f"{m}:{hist[m]}" for m in sorted(hist)))
    for frac in (0.01, 0.02, 0.05, 0.10, 0.25):
        n = max(1, int(total * frac))
        prefix_hits = sum(1 for _, full, _ in rows[:n] if full)
        rate = prefix_hits / n
        lift = rate / base if base else 0.0
        capture = prefix_hits / hits if hits else 0.0
        print(
            f"prefix={frac:.2f} n={n} hits={prefix_hits} "
            f"rate={rate:.8f} lift={lift:.3f} capture={capture:.3f}"
        )


if __name__ == "__main__":
    main()
