#!/usr/bin/env python3
"""Empirical hazard calibration for generic search versus X1(16)+halving.

This script runs the local pomerance binary in fixed-budget batches on smaller
primes. It is meant to estimate whether the p23 model's lift/bias factor is
plausible; it does not touch the active p23 production run.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


P23 = 10**23 + 117


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in [2, 3, 5, 7, 11, 13, 17]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime_mod8_5(start: int) -> int:
    n = start + ((5 - start) % 8)
    while not is_prime(n):
        n += 8
    return n


def compute_k(p: int) -> int:
    q = math.isqrt(p)
    sq = math.isqrt(q)
    bound = q + 1 + 2 * sq
    k = 0
    v = 1
    while v <= bound:
        k += 1
        v <<= 1
    return k


def odd_parts(p: int, k: int) -> list[int]:
    twok = 1 << k
    pp1 = p + 1
    r = pp1 % twok
    sqrtp = math.isqrt(p)
    two_sqrtp = 2 * sqrtp + 4
    out: list[int] = []
    for ri, res in enumerate([r, (-r) % twok]):
        for sign in (-1, 1):
            j = 0
            while True:
                if sign > 0:
                    tv = res + j * twok
                else:
                    tv = res - (j + 1) * twok
                if tv > two_sqrtp or tv < -two_sqrtp:
                    break
                if tv != 0:
                    if ri == 0:
                        n = pp1 - tv
                    else:
                        n = pp1 + tv
                    if n > 0 and n % twok == 0:
                        out.append(n // twok)
                j += 1
    return sorted(set(out))


def trace_mass(p: int, k: int) -> float:
    twok = 1 << k
    pp1 = p + 1
    total = 0.0
    for m in odd_parts(p, k):
        n = twok * m
        t = pp1 - n
        u = t / (2.0 * math.sqrt(p))
        if abs(u) <= 1:
            total += math.sqrt(max(0.0, 1.0 - u * u)) / (math.pi * math.sqrt(p))
    return total


@dataclass
class RunResult:
    p: int
    k: int
    n_odd_parts: int
    trace_mass: float
    mode: str
    seed: int
    budget: int
    hit: bool
    trials_to_hit: int | None
    elapsed: float
    returncode: int


FOUND_RE = re.compile(r"Found after ([0-9.]+)s \(~([0-9]+) (?:X1\(16\) curves|trials)\)")
ELAPSED_RE = re.compile(r"(?:Verified: PASS|Not found) .*\(([0-9.]+)s\)|Not found in ([0-9.]+)s")


def run_one(binary: Path, p: int, mode: str, seed: int, budget: int, timeout: float) -> RunResult:
    k = compute_k(p)
    ops = odd_parts(p, k)
    cmd = [str(binary), str(p), str(seed), str(budget)]
    if mode != "generic":
        cmd.append(mode)
    t0 = time.monotonic()
    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    wall = time.monotonic() - t0
    out = proc.stdout
    hit = "Verified: PASS" in out
    trials_to_hit: int | None = None
    m = FOUND_RE.search(out)
    if m:
        trials_to_hit = int(m.group(2))
    elapsed = wall
    em = ELAPSED_RE.search(out)
    if em:
        elapsed = float(em.group(1) or em.group(2))
    return RunResult(
        p=p,
        k=k,
        n_odd_parts=len(ops),
        trace_mass=trace_mass(p, k),
        mode=mode,
        seed=seed,
        budget=budget,
        hit=hit,
        trials_to_hit=trials_to_hit,
        elapsed=elapsed,
        returncode=proc.returncode,
    )


def summarize(rows: list[RunResult]) -> str:
    lines = []
    groups: dict[tuple[int, str], list[RunResult]] = {}
    for r in rows:
        groups.setdefault((r.p, r.mode), []).append(r)
    for (p, mode), rs in sorted(groups.items()):
        hits = [r for r in rs if r.hit]
        total_budget = sum(r.trials_to_hit if r.hit and r.trials_to_hit else r.budget for r in rs)
        total_elapsed = sum(r.elapsed for r in rs)
        hazard_mle = len(hits) / total_budget if total_budget else 0.0
        rate = total_budget / total_elapsed if total_elapsed else 0.0
        tm = rs[0].trace_mass
        x16_gain = hazard_mle / (16.0 * tm) if mode.startswith("x16") and tm else 0.0
        gen_gain = hazard_mle / tm if mode == "generic" and tm else 0.0
        lines.append(
            "p={p} mode={mode} runs={runs} hits={hits} "
            "hazard_mle={hazard:.6e} rate={rate:.3f}/s "
            "effective_hits_per_s={ehps:.6e} trace_mass={tm:.6e} "
            "generic_hazard_over_mass={gen:.3f} x16_LB={x16:.3f}".format(
                p=p,
                mode=mode,
                runs=len(rs),
                hits=len(hits),
                hazard=hazard_mle,
                rate=rate,
                ehps=hazard_mle * rate,
                tm=tm,
                gen=gen_gain,
                x16=x16_gain,
            )
        )
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", type=Path, default=Path("./pomerance_calib"))
    ap.add_argument("--starts", type=int, nargs="+", default=[10**10, 3 * 10**10, 10**11])
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--budget", type=int, default=2_000_000)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument(
        "--modes",
        nargs="+",
        default=["generic", "x16halve"],
        help="Search modes to pass to the binary; use generic for the default random-A search.",
    )
    ap.add_argument("--out", type=Path, default=Path("runs/small_p_calibration/latest.csv"))
    args = ap.parse_args()

    args.binary = args.binary.resolve()
    if not args.binary.exists():
        raise SystemExit(f"binary not found: {args.binary}")

    primes = [next_prime_mod8_5(s) for s in args.starts]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    rows: list[RunResult] = []
    base_seed = 910000
    for p in primes:
        for mode in args.modes:
            for i in range(args.seeds):
                mode_offset = 0 if mode == "generic" else 5000000 + 1000003 * args.modes.index(mode)
                seed = base_seed + i * 104729 + mode_offset + (p % 100000)
                print(f"run p={p} mode={mode} seed={seed} budget={args.budget}", flush=True)
                try:
                    rows.append(run_one(args.binary, p, mode, seed, args.budget, args.timeout))
                except subprocess.TimeoutExpired:
                    print(f"timeout p={p} mode={mode} seed={seed}", file=sys.stderr, flush=True)

    with args.out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(RunResult.__dataclass_fields__.keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r.__dict__)

    print()
    print(summarize(rows))
    print(f"csv={args.out}")


if __name__ == "__main__":
    main()
