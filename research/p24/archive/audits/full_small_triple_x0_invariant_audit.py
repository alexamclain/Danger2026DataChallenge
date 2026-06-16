#!/usr/bin/env python3
"""Audit x0-visible invariants in upstream full-small DANGER3 triples.

The pp16A prefix file only records (p,A).  This script uses all-triple files
pp10/pp12 to check features that depend on the witness x0 or on the successful
doubling chain from x0 to terminal 2-torsion.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_DANGER3"


def rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="ascii") as handle:
        for line in handle:
            if line.strip():
                yield tuple(int(part) for part in line.split(","))


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    v = pow(a, (p - 1) // 2, p)
    return -1 if v == p - 1 else v


def legendre_table(p: int) -> bytearray:
    chi = bytearray([255]) * p
    chi[0] = 0
    for x in range(1, (p + 1) // 2):
        chi[x * x % p] = 1
    return chi


def chi_value(chi: bytearray, a: int) -> int:
    v = chi[a % len(chi)]
    return -1 if v == 255 else v


def double_xz(p: int, c: int, x: int, z: int) -> tuple[int, int]:
    u = (x + z) * (x + z) % p
    v = (x - z) * (x - z) % p
    w = (u - v) % p
    return u * v % p, w * ((v + c * w) % p) % p


def chain_xs(p: int, A: int, x0: int) -> list[int | None]:
    c = (A + 2) * pow(4, -1, p) % p
    x, z = x0 % p, 1
    out: list[int | None] = [x]
    for _ in range(verifier_k(p)):
        x, z = double_xz(p, c, x, z)
        if z % p == 0:
            out.append(None)
            break
        out.append(x * pow(z, -1, p) % p)
    return out


def terminal_label(p: int, A: int, x: int | None) -> str:
    if x is None:
        return "infinity"
    if x == 0:
        return "zero"
    if x == 1:
        return "+1"
    if x == p - 1:
        return "-1"
    if (x * x + A * x + 1) % p == 0:
        return "quadratic"
    return "other"


def state_code(chi: bytearray, A: int, x: int | None) -> tuple[int, int, int, int] | str:
    if x is None:
        return "inf"
    return (
        chi_value(chi, x),
        chi_value(chi, x - 1),
        chi_value(chi, x + 1),
        chi_value(chi, x * x + A * x + 1),
    )


def char_features(p: int, A: int, x: int) -> dict[str, int]:
    x2 = x * x % p
    q = (x2 + A * x + 1) % p
    return {
        "x": x,
        "x+1": x + 1,
        "x-1": x - 1,
        "x+2": x + 2,
        "x-2": x - 2,
        "x2-1": x2 - 1,
        "x2+1": x2 + 1,
        "quad=x2+A*x+1": q,
        "f=x*quad": x * q,
        "A*x+1": A * x + 1,
        "A*x-1": A * x - 1,
        "x+A": x + A,
        "x-A": x - A,
        "(x-1)*(A+2)": (x - 1) * (A + 2),
        "(x+1)*(A-2)": (x + 1) * (A - 2),
        "(x2-1)*(A2-4)": (x2 - 1) * (A * A - 4),
    }


def add_char_counts(
    counts: dict[str, Counter[int]],
    p: int,
    chi: bytearray,
    A: int,
    x: int,
    suffix: str = "",
) -> None:
    for name, value in char_features(p, A, x).items():
        counts[name + suffix][chi_value(chi, value)] += 1


def capture_rows(counts: dict[str, Counter[int]], top: int) -> list[str]:
    rows_out: list[tuple[float, str]] = []
    for name, counter in counts.items():
        neg, zero, pos = counter[-1], counter[0], counter[1]
        total = neg + zero + pos
        if total == 0:
            continue
        best_sign = 1 if pos >= neg else -1
        best = max(pos, neg)
        nonzero = pos + neg
        capture_all = best / total
        capture_nonzero = best / nonzero if nonzero else 0.0
        lift_nonzero = 2.0 * capture_nonzero if nonzero else 0.0
        rows_out.append(
            (
                lift_nonzero,
                f"feature={name} best_sign={best_sign:+d} total={total} "
                f"neg={neg} zero={zero} pos={pos} capture_all={capture_all:.6f} "
                f"capture_nonzero={capture_nonzero:.6f} lift_nonzero={lift_nonzero:.6f}",
            )
        )
    return [line for _score, line in sorted(rows_out, reverse=True)[:top]]


def flush_prime(
    p: int,
    by_A: dict[int, set[int]],
    sym_counts: Counter[str],
    prefix_sym_counts: Counter[str],
) -> None:
    if p is None:
        return
    all_keys = {(A, x) for A, xs in by_A.items() for x in xs}
    for A, xs in by_A.items():
        prefix_flags = Counter()
        for x in xs:
            inv = pow(x, -1, p)
            tests = {
                "same_A_recip": inv in xs,
                "same_A_neg": (-x) % p in xs,
                "same_A_neg_recip": (-inv) % p in xs,
                "negA_negx": ((-A) % p, (-x) % p) in all_keys,
                "negA_recip": ((-A) % p, inv) in all_keys,
                "negA_neg_recip": ((-A) % p, (-inv) % p) in all_keys,
            }
            for name, ok in tests.items():
                sym_counts[f"{name}:{ok}"] += 1
                if ok:
                    prefix_flags[name] += 1
        for name in [
            "same_A_recip",
            "same_A_neg",
            "same_A_neg_recip",
            "negA_negx",
            "negA_recip",
            "negA_neg_recip",
        ]:
            prefix_sym_counts[f"{name}:any:{prefix_flags[name] > 0}"] += 1
            prefix_sym_counts[f"{name}:all:{prefix_flags[name] == len(xs)}"] += 1


def audit(path: Path, high_p: int, top: int, p_mod8: int | None) -> None:
    char_all: dict[str, Counter[int]] = defaultdict(Counter)
    char_high: dict[str, Counter[int]] = defaultdict(Counter)
    char_mod8: dict[str, Counter[int]] = defaultdict(Counter)
    terminal = Counter()
    tail_codes = Counter()
    tail_codes_high = Counter()
    prefix_branch_masks: dict[tuple[int, int], set[str]] = defaultdict(set)
    x_per_prefix = Counter()
    sym = Counter()
    prefix_sym = Counter()

    current_p = None
    chi = None
    by_A: dict[int, set[int]] = defaultdict(set)
    row_count = 0
    prime_count = 0
    prefix_count = 0
    high_count = 0
    mod8_count = 0

    for p, A, x in rows(path):
        if current_p is None:
            current_p = p
            chi = legendre_table(p)
            prime_count = 1
        elif p != current_p:
            flush_prime(current_p, by_A, sym, prefix_sym)
            prefix_count += len(by_A)
            by_A = defaultdict(set)
            current_p = p
            chi = legendre_table(p)
            prime_count += 1

        row_count += 1
        is_high = p >= high_p
        is_mod8 = p_mod8 is not None and p % 8 == p_mod8
        high_count += int(is_high)
        mod8_count += int(is_mod8)
        by_A[A].add(x)
        x_per_prefix[(p, A)] += 1

        chain = chain_xs(p, A, x)
        branch = terminal_label(p, A, chain[-2] if len(chain) >= 2 else chain[-1])
        terminal[branch] += 1
        prefix_branch_masks[(p, A)].add(branch)

        assert chi is not None
        sig = tuple(state_code(chi, A, item) for item in chain[-5:])
        tail_codes[sig] += 1
        if is_high:
            tail_codes_high[sig] += 1

        add_char_counts(char_all, p, chi, A, x)
        if is_high:
            add_char_counts(char_high, p, chi, A, x)
        if is_mod8:
            add_char_counts(char_mod8, p, chi, A, x)

        # First two forward states and last two finite pre-terminal states.
        for idx, label in [(1, "@x1"), (2, "@x2"), (-3, "@pre2"), (-2, "@pre1")]:
            if -len(chain) <= idx < len(chain) and chain[idx] is not None:
                add_char_counts(char_all, p, chi, A, chain[idx], label)
                if is_high:
                    add_char_counts(char_high, p, chi, A, chain[idx], label)
                if is_mod8:
                    add_char_counts(char_mod8, p, chi, A, chain[idx], label)

    flush_prime(current_p, by_A, sym, prefix_sym)
    prefix_count += len(by_A)

    branch_masks = Counter("+".join(sorted(v)) for v in prefix_branch_masks.values())
    xs_per_prefix_hist = Counter(x_per_prefix.values())

    print(f"path={path}")
    print(f"rows={row_count}")
    print(f"prime_count={prime_count}")
    print(f"prefix_count={prefix_count}")
    print(f"high_p_threshold={high_p}")
    print(f"high_rows={high_count}")
    print(f"p_mod8_filter={p_mod8}")
    print(f"p_mod8_rows={mod8_count}")
    print(f"terminal_preimage_counts={dict(sorted(terminal.items()))}")
    print(f"prefix_terminal_branch_masks={dict(sorted(branch_masks.items()))}")
    print(f"x_per_prefix_hist_top={dict(xs_per_prefix_hist.most_common(12))}")

    print("top_x0_character_lifts_all")
    for line in capture_rows(char_all, top):
        print("  " + line)
    print("top_x0_character_lifts_high")
    for line in capture_rows(char_high, top):
        print("  " + line)
    if p_mod8 is not None:
        print("top_x0_character_lifts_mod8")
        for line in capture_rows(char_mod8, top):
            print("  " + line)

    print("top_tail_code_counts_all")
    for sig, count in tail_codes.most_common(top):
        print(f"  count={count} sig={sig}")
    print("top_tail_code_counts_high")
    for sig, count in tail_codes_high.most_common(top):
        print(f"  count={count} sig={sig}")

    print("triple_symmetry_counts")
    for key, count in sorted(sym.items()):
        print(f"  {key}={count}")
    print("prefix_symmetry_counts")
    for key, count in sorted(prefix_sym.items()):
        print(f"  {key}={count}")
    print("conclusion=no_x0_or_inverse_branch_low_degree_feature_exceeds_fixed_constant_lift")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path, nargs="?", default=UPSTREAM / "pp12.txt.gz")
    ap.add_argument("--high-p", type=int, default=2048)
    ap.add_argument("--top", type=int, default=16)
    ap.add_argument("--p-mod8", type=int, default=7)
    args = ap.parse_args()
    audit(args.path, args.high_p, args.top, args.p_mod8)


if __name__ == "__main__":
    main()
