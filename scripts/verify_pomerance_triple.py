#!/usr/bin/env python3
"""Verify a Pomerance triple candidate.

This is an operational helper for p23 hits. It can read a triple directly or
extract the last three-integer line preceding "Verified: PASS" in a worker log.
It then runs an independent Montgomery doubling replay and, when available,
Andrew Sutherland's DANGER3 vpp.py verifier.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO_ROOT.parent


def first_existing(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


DEFAULT_VPP = first_existing([
    REPO_ROOT / "external" / "DANGER3" / "vpp.py",
    CODEX_ROOT / "open-co-mathematician" / "external" / "DANGER3" / "vpp.py",
    CODEX_ROOT / "danger3-short-certificate-experiments" / "external" / "DANGER3" / "vpp.py",
])
DEFAULT_LEAN_VPP = first_existing([
    REPO_ROOT / "external" / "DANGER3" / "lean_vpp.py",
    CODEX_ROOT / "open-co-mathematician" / "external" / "DANGER3" / "lean_vpp.py",
    CODEX_ROOT / "danger3-short-certificate-experiments" / "external" / "DANGER3" / "lean_vpp.py",
])


def parse_triple_from_log(path: Path) -> tuple[int, int, int]:
    triple: tuple[int, int, int] | None = None
    int_line = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s*$")
    for line in path.read_text().splitlines():
        m = int_line.match(line)
        if m:
            triple = tuple(int(x) for x in m.groups())  # type: ignore[assignment]
        if "Verified: PASS" in line:
            if triple is None:
                raise SystemExit(f"{path}: saw PASS but no preceding triple line")
            return triple
    raise SystemExit(f"{path}: no Verified: PASS line found")


def compute_k(p: int) -> tuple[int, int, int, int]:
    q = math.isqrt(p)
    sq = math.isqrt(q)
    bound = q + 1 + 2 * sq
    k = 0
    v = 1
    while v <= bound:
        k += 1
        v <<= 1
    return q, sq, bound, k


def mong_dbl(p: int, A: int, X: int, Z: int) -> tuple[int, int]:
    X2 = X * X % p
    Z2 = Z * Z % p
    XZ = X * Z % p
    Xn = (X2 - Z2) ** 2 % p
    Zn = (4 * XZ * (X2 + A * XZ + Z2)) % p
    return Xn, Zn


def replay(p: int, A: int, x0: int) -> dict[str, object]:
    q, sq, bound, k = compute_k(p)
    if not (0 <= A < p and 0 <= x0 < p):
        raise AssertionError("A and x0 must be reduced modulo p")
    if A % p in (2, p - 2):
        raise AssertionError("A must not be +/-2 modulo p")

    X, Z = x0 % p, 1
    zero_steps: list[int] = []
    z_prev = Z
    for i in range(1, k + 1):
        z_prev = Z
        X, Z = mong_dbl(p, A, X, Z)
        if Z == 0:
            zero_steps.append(i)

    ok = bool(zero_steps == [k])
    return {
        "p": p,
        "A": A,
        "x0": x0,
        "sqrt_floor": q,
        "sqrt_sqrt_floor": sq,
        "bound": bound,
        "k": k,
        "zero_steps": zero_steps,
        "final_X": X,
        "final_Z": Z,
        "gcd_Zprev_p": math.gcd(z_prev, p),
        "independent_replay_pass": ok,
    }


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("triple", nargs="*", help="p A x0, unless --log is used")
    ap.add_argument("--log", type=Path, help="worker log containing a Verified: PASS triple")
    ap.add_argument("--vpp", type=Path, default=DEFAULT_VPP)
    ap.add_argument("--lean-vpp", type=Path, default=DEFAULT_LEAN_VPP)
    ap.add_argument("--lean-out", type=Path, help="optional path for generated Lean certificate")
    ap.add_argument("--skip-vpp", action="store_true")
    ap.add_argument("--skip-prime", action="store_true")
    args = ap.parse_args()

    if args.log:
        p, A, x0 = parse_triple_from_log(args.log)
    else:
        if len(args.triple) != 3:
            ap.error("provide p A x0 or --log worker.log")
        p, A, x0 = (int(x) for x in args.triple)

    print("triple:")
    print(f"  p  = {p}")
    print(f"  A  = {A}")
    print(f"  x0 = {x0}")
    print()

    info = replay(p, A, x0)
    print("independent_replay:")
    for key in [
        "sqrt_floor",
        "sqrt_sqrt_floor",
        "bound",
        "k",
        "zero_steps",
        "final_X",
        "final_Z",
        "gcd_Zprev_p",
        "independent_replay_pass",
    ]:
        print(f"  {key} = {info[key]}")
    if not info["independent_replay_pass"]:
        raise SystemExit("independent replay failed")
    print()

    if not args.skip_prime:
        openssl = shutil.which("openssl")
        if openssl:
            code, out = run_cmd([openssl, "prime", "-checks", "128", str(p)])
            print("openssl_prime:")
            print(f"  returncode = {code}")
            print(f"  output = {out}")
            if code != 0 or "is prime" not in out:
                raise SystemExit("openssl prime check failed")
        else:
            print("openssl_prime: skipped (openssl not found)")
        print()

    if not args.skip_vpp:
        if args.vpp.exists():
            code, out = run_cmd([sys.executable, str(args.vpp), str(p), str(A), str(x0)])
            print("danger3_vpp:")
            print(f"  returncode = {code}")
            print(out)
            if code != 0:
                raise SystemExit("vpp.py failed")
        else:
            print(f"danger3_vpp: skipped ({args.vpp} not found)")
        print()

    if args.lean_out:
        if not args.lean_vpp.exists():
            raise SystemExit(f"lean_vpp.py not found: {args.lean_vpp}")
        code, out = run_cmd([sys.executable, str(args.lean_vpp), str(p), str(A), str(x0)])
        if code != 0:
            print(out)
            raise SystemExit("lean_vpp.py failed")
        args.lean_out.parent.mkdir(parents=True, exist_ok=True)
        args.lean_out.write_text(out + "\n")
        print(f"lean_certificate_written = {args.lean_out}")

    print("verification_status = PASS")


if __name__ == "__main__":
    main()
