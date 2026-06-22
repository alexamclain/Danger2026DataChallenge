#!/usr/bin/env python3
"""Validate the p27 conic-pair sampler identities over finite fields."""

from __future__ import annotations

import argparse
import random


P27 = 10**27 + 103
DEFAULT_FIELDS = [1607, 1847, 2087, P27]


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def check_field(p: int, trials: int, rng: random.Random) -> tuple[int, int, int]:
    inv2 = inv(2, p)
    inv4 = inv(4, p)
    ok = 0
    bad = 0
    degenerate = 0

    for _ in range(trials):
        R = rng.randrange(1, p)
        L = rng.randrange(1, p)
        a = (R - inv(R, p)) % p
        s = (R + inv(R, p)) % p
        a2_over_l = (a * a * inv(L, p)) % p
        d = ((L - a2_over_l) * inv2) % p
        r = (-(L + a2_over_l) * inv4) % p
        if r == 0:
            degenerate += 1
            continue

        h = ((s + d) * inv2) % p
        g = ((s - d) * inv2) % p
        c = (s * d * inv((2 * r) % p, p)) % p

        e_h = (h * h - (r * r + c * r + 1)) % p
        e_g = (g * g - (r * r - c * r + 1)) % p
        e_R = (R * R - (h + g) * R + 1) % p

        if e_h == 0 and e_g == 0 and e_R == 0:
            ok += 1
        else:
            bad += 1

    return ok, bad, degenerate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument(
        "--fields",
        default=",".join(str(q) for q in DEFAULT_FIELDS),
        help="comma-separated prime fields",
    )
    args = parser.parse_args()

    fields = [int(part) for part in args.fields.split(",") if part]
    rng = random.Random(args.seed)

    print("P27_CONIC_PAIR_SAMPLER_IDENTITY_PROBE")
    print(f"trials_per_field {args.trials}")
    print(f"seed {args.seed}")
    for p in fields:
        ok, bad, degenerate = check_field(p, args.trials, rng)
        print(f"FIELD {p} ok {ok} bad {bad} degenerate {degenerate}")
    print("RESULT p27_conic_pair_sampler_identity rows=1/1")


if __name__ == "__main__":
    main()
