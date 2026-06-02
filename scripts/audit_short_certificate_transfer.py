#!/usr/bin/env python3
"""Read-only audit for the DANGER3 short-certificate transfer.

This checks that the sibling short-certificate repository is present, that the
external DANGER3 verifier artifacts can be resolved, and that the X1(16)
y-character used by the p23 nonsplit fallback agrees with the direct
Montgomery split discriminant on deterministic samples.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


P23 = 100000000000000000000117
REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO_ROOT.parent
DEFAULT_EXTERNAL = CODEX_ROOT / "danger3-short-certificate-experiments"


def run_text(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else f"ERROR: {proc.stdout.strip()}"


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    v = pow(a, (p - 1) // 2, p)
    if v == 1:
        return 1
    if v == p - 1:
        return -1
    raise ValueError(f"unexpected Legendre value {v}")


def sqrt_mod_p5(a: int, p: int) -> int | None:
    """Square root for primes p == 5 mod 8, returning one root if it exists."""
    a %= p
    if a == 0:
        return 0
    if p % 8 != 5:
        raise ValueError("sqrt_mod_p5 requires p == 5 mod 8")
    root = pow(a, (p + 3) // 8, p)
    if root * root % p == a:
        return root
    sqrt_m1 = pow(2, (p - 1) // 4, p)
    root = root * sqrt_m1 % p
    if root * root % p == a:
        return root
    return None


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def x16_root_to_montgomery_A(p: int, x: int, y: int) -> tuple[int, int] | None:
    """Mirror the local C X1(16) root-to-Montgomery conversion."""
    xy = x * y % p
    x2 = x * x % p
    denr = (x2 * y - x) % p
    dens = xy
    if denr == 0 or dens == 0:
        return None

    rnum = (x2 * y - xy + y - 1) % p
    snum = (xy - y + 1) % p
    r = rnum * inv(denr, p) % p
    s = snum * inv(dens, p) % p
    if r in (0, 1) or s == 0:
        return None

    rm1 = (r - 1) % p
    bt = r * s % p * rm1 % p
    if bt == 0:
        return None
    c = s * rm1 % p
    a = (c - 1) % p
    e = (a * a - 4 * bt) % p

    rs = r * s % p
    den = (rs - 2 * r + 1) % p
    u4 = r * rm1 % p
    s2 = s * s % p
    term = (r - s2 + s - 1) % p
    denn = den * den % p

    numer8 = u4 * (r - s) % p * term % p
    x8_num = (36 * numer8 + 3 * e * denn) % p
    lam_num = 36 * (u4 * denn - numer8) % p
    if lam_num == 0:
        return None
    inv_lam = inv(lam_num, p)
    A = 3 * x8_num % p * inv_lam % p
    xP = (-36 * numer8) % p * inv_lam % p
    if A <= 2 or A >= p - 2:
        return None
    return A, xP


def x16_roots_for_y(p: int, y: int) -> list[int]:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return []
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    sd = sqrt_mod_p5(disc, p)
    if sd is None:
        return []
    inv_2qa = inv(2 * qa, p)
    return [((sd - qb) * inv_2qa) % p, ((-sd - qb) * inv_2qa) % p]


def x16_y_character(p: int, y: int) -> int:
    y2 = y * y % p
    return legendre((y2 - 2) * (y2 - 4 * y + 2), p)


def deterministic_y(seed: int, p: int) -> int:
    # SplitMix64-style step, then lift into F_p. This is deterministic and cheap.
    z = (seed + 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9 & ((1 << 64) - 1)
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB & ((1 << 64) - 1)
    z ^= z >> 31
    return (z % (p - 1)) + 1


def concordance(p: int, samples: int) -> dict[str, int]:
    attempts = 0
    accepted_y = 0
    roots_checked = 0
    mismatches = 0
    split = 0
    nonsplit = 0
    degeneracies = 0

    while accepted_y < samples and attempts < samples * 200:
        attempts += 1
        y = deterministic_y(attempts, p)
        y_chi = x16_y_character(p, y)
        if y_chi == 0:
            degeneracies += 1
            continue
        roots = x16_roots_for_y(p, y)
        if not roots:
            continue

        saw_root = False
        for x in roots:
            converted = x16_root_to_montgomery_A(p, x, y)
            if converted is None:
                continue
            A, _xP = converted
            direct_chi = legendre(A * A - 4, p)
            roots_checked += 1
            saw_root = True
            if direct_chi != y_chi:
                mismatches += 1
            if direct_chi == 1:
                split += 1
            elif direct_chi == -1:
                nonsplit += 1
        if saw_root:
            accepted_y += 1

    return {
        "p": p,
        "samples_requested": samples,
        "attempts": attempts,
        "accepted_y": accepted_y,
        "roots_checked": roots_checked,
        "mismatches": mismatches,
        "split_roots": split,
        "nonsplit_roots": nonsplit,
        "degenerate_y": degeneracies,
    }


def first_existing(candidates: list[Path]) -> Path | None:
    return next((path for path in candidates if path.exists()), None)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P23)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--external-repo", type=Path, default=DEFAULT_EXTERNAL)
    args = parser.parse_args()

    external = args.external_repo.resolve()
    vpp = first_existing([
        REPO_ROOT / "external" / "DANGER3" / "vpp.py",
        CODEX_ROOT / "open-co-mathematician" / "external" / "DANGER3" / "vpp.py",
        external / "external" / "DANGER3" / "vpp.py",
    ])
    lean_vpp = first_existing([
        REPO_ROOT / "external" / "DANGER3" / "lean_vpp.py",
        CODEX_ROOT / "open-co-mathematician" / "external" / "DANGER3" / "lean_vpp.py",
        external / "external" / "DANGER3" / "lean_vpp.py",
    ])

    print("short_certificate_transfer_audit=1")
    print(f"repo_root={REPO_ROOT}")
    print(f"external_repo={external}")
    print(f"external_exists={int(external.exists())}")
    if external.exists():
        print(f"external_head={run_text(['git', 'rev-parse', 'HEAD'], external)}")
        print(f"external_status={run_text(['git', 'status', '--short'], external) or 'clean'}")
    print(f"vpp_path={vpp if vpp else 'missing'}")
    print(f"lean_vpp_path={lean_vpp if lean_vpp else 'missing'}")
    print()
    print("formula:")
    print("split iff Legendre(A^2 - 4, p) = 1")
    print("x16 nonsplit iff Legendre((y^2 - 2)(y^2 - 4y + 2), p) = -1")
    print()

    stats = concordance(args.p, args.samples)
    print("x16_y_character_concordance:")
    for key, value in stats.items():
        print(f"  {key}={value}")
    if stats["mismatches"] == 0 and stats["accepted_y"] == args.samples:
        print("  status=PASS")
    else:
        print("  status=REVIEW")


if __name__ == "__main__":
    main()
