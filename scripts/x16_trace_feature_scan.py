#!/usr/bin/env python3
"""Scan cheap X1(16) y-features against tiny trace residues.

This is a small-prime research helper. It samples Sutherland's X1(16) model,
keeps the original y parameter, brute-force point-counts the resulting
Montgomery curves, and asks whether low-degree Legendre features of y enrich
the p23 target trace residues modulo small odd primes.

It is not a production filter. Its purpose is to make the "native trace
residue predicate" lane reproducible and easy to falsify.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from dataclasses import dataclass

import x16_trace_residue_calibration as cal


P23 = 10**23 + 117
P23_TRACES = (321963163766, -227792650122)


@dataclass(frozen=True)
class Sample:
    y: int
    A: int
    trace: int
    group: str


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def x16_samples_with_y(p: int, rng: random.Random, want: int) -> list[tuple[int, int]]:
    """Return (y,A) samples from the local X1(16) model."""
    out: list[tuple[int, int]] = []
    attempts = 0
    max_attempts = want * 2000 + 2000
    while len(out) < want and attempts < max_attempts:
        attempts += 1
        y = rng.randrange(1, p)
        y2 = y * y % p
        y3 = y2 * y % p
        qa = (y2 - 2 * y) % p
        if qa == 0:
            continue
        qb = (2 * y2 - y3) % p
        qc = (1 - y) % p
        disc = (qb * qb - 4 * qa * qc) % p
        sd = cal.sqrt_mod(disc, p)
        if sd is None:
            continue

        inv_2qa = cal.inv(2 * qa, p)
        for x in (((sd - qb) * inv_2qa) % p, ((-sd - qb) * inv_2qa) % p):
            xy = x * y % p
            x2 = x * x % p
            denr = (x2 * y - x) % p
            dens = xy
            if denr == 0 or dens == 0:
                continue
            rnum = (x2 * y - xy + y - 1) % p
            snum = (xy - y + 1) % p
            r = rnum * cal.inv(denr, p) % p
            s = snum * cal.inv(dens, p) % p
            if r in (0, 1) or s == 0:
                continue

            rm1 = (r - 1) % p
            bt = r * s % p * rm1 % p
            if bt == 0:
                continue
            c = s * rm1 % p
            a = (c - 1) % p
            e = (a * a - 4 * bt) % p

            rs = r * s % p
            den = (rs - 2 * r + 1) % p
            u4 = r * rm1 % p
            s2 = s * s % p
            term = (r - s2 + s - 1) % p
            denn = den * den % p
            numer8 = u4 * ((r - s) % p) % p * term % p

            x8_num = (36 * numer8 + 3 * e * denn) % p
            lam_num = 36 * ((u4 * denn - numer8) % p) % p
            if lam_num == 0:
                continue
            A = 3 * x8_num % p * cal.inv(lam_num, p) % p
            if A <= 2 or A >= p - 2:
                continue
            out.append((y, A))
            if len(out) >= want:
                break
    return out


def feature_values(y: int, p: int) -> dict[str, int]:
    y %= p
    y2 = y * y % p
    f: dict[str, int] = {
        "y": y,
        "y-1": y - 1,
        "y+1": y + 1,
        "y-2": y - 2,
        "y+2": y + 2,
        "y*(y-1)": y * (y - 1),
        "y*(y-2)": y * (y - 2),
        "(y-1)*(y-2)": (y - 1) * (y - 2),
        "y^2-2": y2 - 2,
        "y^2-2y+2": y2 - 2 * y + 2,
        "y^2-4y+2": y2 - 4 * y + 2,
        "y^2-y+1": y2 - y + 1,
        "y^2+y+1": y2 + y + 1,
        "y^2-3y+1": y2 - 3 * y + 1,
    }
    f["G_nonsplit"] = f["y^2-2"] * f["y^2-4y+2"]
    f["D16"] = y * (y - 2) * f["y^2-2"] * f["y^2-2y+2"]
    f["C3_resolvent"] = f["D16"] * (y - 1) * f["y^2-2y+2"] * f["y^2-4y+2"]
    return {k: v % p for k, v in f.items()}


def split_class_from_y(y: int, p: int) -> str:
    values = feature_values(y, p)
    chi = legendre(values["G_nonsplit"], p)
    if chi == 1:
        return "split"
    if chi == -1:
        return "nonsplit"
    return "degenerate"


def feature_sign_vectors(samples: list[Sample], p: int) -> dict[tuple[str, int], list[bool]]:
    names = sorted(feature_values(samples[0].y, p)) if samples else []
    vectors: dict[tuple[str, int], list[bool]] = {}
    for name in names:
        signs = [legendre(feature_values(sample.y, p)[name], p) for sample in samples]
        for sign in (-1, 0, 1):
            vectors[(name, sign)] = [value == sign for value in signs]
    return vectors


def summarize_filter(
    selected: list[bool],
    target_flags: list[bool],
    base: float,
    label: str,
) -> tuple[float, str] | None:
    idx = [i for i, keep in enumerate(selected) if keep]
    if not idx:
        return None
    hits = sum(target_flags[i] for i in idx)
    total_hits = sum(target_flags)
    coverage = len(idx) / len(target_flags) if target_flags else 0.0
    capture = hits / total_hits if total_hits else 0.0
    precision = hits / len(idx)
    lift = precision / base if base else 0.0
    score = lift * capture
    return (
        score,
        f"{label} coverage={coverage:.4f} capture={capture:.4f} "
        f"precision={precision:.4f} lift={lift:.3f}"
    )


def scan_features(samples: list[Sample], p: int, ell: int) -> list[tuple[float, str]]:
    targets = {t % ell for t in P23_TRACES}
    target_flags = [sample.trace % ell in targets for sample in samples]
    base = sum(target_flags) / len(samples) if samples else 0.0
    rows: list[tuple[float, str]] = []
    for (name, sign), selected in feature_sign_vectors(samples, p).items():
        row = summarize_filter(
            selected,
            target_flags,
            base,
            f"ell={ell} feature={name} sign={sign:+d}",
        )
        if row is not None:
            rows.append(row)
    return sorted(rows, reverse=True)


def scan_feature_pairs(
    samples: list[Sample],
    p: int,
    ell: int,
    min_coverage: float,
) -> list[tuple[float, str]]:
    targets = {t % ell for t in P23_TRACES}
    target_flags = [sample.trace % ell in targets for sample in samples]
    base = sum(target_flags) / len(samples) if samples else 0.0
    vectors = feature_sign_vectors(samples, p)
    atoms = [
        (name, sign, selected)
        for (name, sign), selected in vectors.items()
        if sum(selected) / len(samples) >= min_coverage
    ]
    rows: list[tuple[float, str]] = []
    for i, (name1, sign1, selected1) in enumerate(atoms):
        for name2, sign2, selected2 in atoms[i + 1 :]:
            if name1 == name2:
                continue
            selected = [a and b for a, b in zip(selected1, selected2)]
            if sum(selected) / len(samples) < min_coverage:
                continue
            row = summarize_filter(
                selected,
                target_flags,
                base,
                f"ell={ell} pair=({name1}:{sign1:+d})&({name2}:{sign2:+d})",
            )
            if row is not None:
                rows.append(row)
    return sorted(rows, reverse=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=240)
    ap.add_argument("--start", type=int, default=20_000)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--seed", type=int, default=20260601)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--pair-top", type=int, default=0)
    ap.add_argument("--pair-min-coverage", type=float, default=0.15)
    ap.add_argument("--group", choices=("all", "split", "nonsplit"), default="all")
    args = ap.parse_args()

    modulus = 8
    for ell in args.ells:
        modulus *= ell
    p = cal.find_calibration_prime(args.start, modulus, P23 % modulus)
    rng = random.Random(args.seed)
    pairs = x16_samples_with_y(p, rng, args.samples)
    all_samples = [
        Sample(y, A, cal.trace_for_montgomery_A(p, A), split_class_from_y(y, p))
        for y, A in pairs
    ]
    samples = [
        sample for sample in all_samples
        if args.group == "all" or sample.group == args.group
    ]

    print("X1(16) trace-residue y-feature scan")
    print(f"calibration_prime={p}")
    print(f"p23_mod_modulus={P23 % modulus} modulus={modulus}")
    group_counts = Counter(sample.group for sample in all_samples)
    print(f"samples={len(samples)} seed={args.seed} group={args.group}")
    print("split_class_counts=" + ",".join(f"{k}:{group_counts[k]}" for k in sorted(group_counts)))
    print()

    for ell in args.ells:
        targets = {t % ell for t in P23_TRACES}
        counts = Counter(sample.trace % ell for sample in samples)
        accepted = sum(counts[r] for r in targets)
        rate = accepted / len(samples) if samples else 0.0
        print(
            f"ell={ell} target_residues={sorted(targets)} "
            f"accepted={accepted}/{len(samples)} rate={rate:.4f} "
            f"counts={dict(sorted(counts.items()))}"
        )
        for _score, row in scan_features(samples, p, ell)[: args.top]:
            print(row)
        if args.pair_top:
            print("pair_scan")
            for _score, row in scan_feature_pairs(
                samples, p, ell, args.pair_min_coverage
            )[: args.pair_top]:
                print(row)
        print()


if __name__ == "__main__":
    main()
