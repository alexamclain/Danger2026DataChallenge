#!/usr/bin/env python3
"""Audit full small DANGER3 triples with x-coordinate and halving-word data.

The upstream pp16A prefix file hides the actual verifier x0 values.  This
streaming audit uses full-triple files (local pp10/pp12, optionally remote
pp14/pp16 streams) to look for structure that could reduce the inverse
halving entropy: reciprocal/sign closures, fiber-size laws, terminal branches,
low-degree characters involving x0, and canonical inverse-halving words.

The branch-word labels are deterministic only as data-analysis labels.  They
use the least square-root representative modulo p to distinguish the two
quadratic choices at each inverse-halving layer; a theorem useful at p=10^24+7
would need an invariant version of any observed bias.
"""

from __future__ import annotations

import argparse
import gzip
import io
import math
import sys
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Iterable, TextIO


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_DANGER3"
PP12 = UPSTREAM / "pp12.txt.gz"


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def open_source(source: str, timeout: int) -> TextIO:
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "p24-full-triple-audit/1"})
        response = urllib.request.urlopen(req, timeout=timeout)
        if source.endswith(".gz"):
            return io.TextIOWrapper(gzip.GzipFile(fileobj=response), encoding="ascii")
        return io.TextIOWrapper(response, encoding="ascii")
    path = Path(source)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii")
    return path.open("rt", encoding="ascii")


def row_stream(
    source: str,
    *,
    timeout: int,
    min_p: int,
    max_p: int,
    mod: int,
    residue: int | None,
    limit: int | None,
) -> Iterable[tuple[int, int, int]]:
    seen = 0
    with open_source(source, timeout) as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            p_s, A_s, x_s = line.split(",")
            p = int(p_s)
            if p > max_p:
                break
            if p < min_p:
                continue
            if residue is not None and p % mod != residue:
                continue
            yield p, int(A_s), int(x_s)
            seen += 1
            if limit is not None and seen >= limit:
                break


def build_tables(p: int) -> tuple[list[int], list[int]]:
    inv = [0] * p
    inv[1] = 1
    for a in range(2, p):
        inv[a] = (p - (p // a) * inv[p % a] % p) % p

    sqrt = [-1] * p
    for r in range((p + 1) // 2):
        v = r * r % p
        if sqrt[v] < 0 or r < sqrt[v]:
            sqrt[v] = r
    return inv, sqrt


def chi_from_table(a: int, p: int, sqrt: list[int]) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if sqrt[a] >= 0 else -1


def double_x(p: int, A: int, x: int, inv: list[int]) -> int | None:
    den = 4 * x * (x * x + A * x + 1)
    den %= p
    if den == 0:
        return None
    num = (x * x - 1) % p
    return (num * num * inv[den]) % p


def terminal_name(p: int, A: int, x: int) -> str:
    if x == 0:
        return "zero"
    if (x * x + A * x + 1) % p == 0:
        return "quadratic"
    return "other"


def chain_and_words(
    p: int,
    A: int,
    x0: int,
    inv: list[int],
    sqrt: list[int],
    max_depth: int,
) -> tuple[str, str, str, str]:
    """Return terminal, forward s-word, forward x-word, and four-symbol word."""
    k = verifier_k(p)
    depth = k - 1
    if max_depth >= 0:
        depth = min(depth, max_depth)

    chain = [x0 % p]
    for _ in range(depth):
        nxt = double_x(p, A, chain[-1], inv)
        if nxt is None:
            break
        chain.append(nxt)

    full_terminal = "truncated"
    if len(chain) == k:
        full_terminal = terminal_name(p, A, chain[-1])
    elif chain:
        full_terminal = terminal_name(p, A, chain[-1])

    s_bits: list[str] = []
    x_bits: list[str] = []
    four_bits: list[str] = []
    inv2 = (p + 1) // 2

    for pre, nxt in zip(chain, chain[1:]):
        if pre == 0:
            s_bits.append("?")
            x_bits.append("?")
            four_bits.append("??")
            continue
        s = (pre + inv[pre]) % p

        # First inverse choice: the two possible s=x+1/x values over nxt.
        d_s = (nxt * nxt + A * nxt + 1) % p
        r_s = sqrt[d_s]
        if r_s < 0:
            s_bit = "?"
        elif r_s == 0:
            s_bit = "0"
        else:
            plus = (2 * nxt + 2 * r_s) % p
            minus = (2 * nxt - 2 * r_s) % p
            if s == plus:
                s_bit = "+"
            elif s == minus:
                s_bit = "-"
            else:
                s_bit = "?"

        # Second inverse choice: the reciprocal pair with fixed s.
        d_x = (s * s - 4) % p
        r_x = sqrt[d_x]
        if r_x < 0:
            x_bit = "?"
        elif r_x == 0:
            x_bit = "0"
        else:
            plus_x = (s + r_x) * inv2 % p
            minus_x = (s - r_x) * inv2 % p
            if pre == plus_x:
                x_bit = "+"
            elif pre == minus_x:
                x_bit = "-"
            else:
                x_bit = "?"

        s_bits.append(s_bit)
        x_bits.append(x_bit)
        four_bits.append(s_bit + x_bit)

    return full_terminal, "".join(s_bits), "".join(x_bits), ".".join(four_bits)


def quantiles(values: list[float], qs: tuple[float, ...]) -> list[float]:
    if not values:
        return [0.0 for _ in qs]
    ordered = sorted(values)
    out = []
    for q in qs:
        idx = min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))
        out.append(ordered[idx])
    return out


def loglog_exponent(points: list[tuple[int, int]]) -> float:
    pts = [(math.log(p), math.log(c)) for p, c in points if c > 0]
    if len(pts) < 2:
        return 0.0
    mx = mean(x for x, _y in pts)
    my = mean(y for _x, y in pts)
    var = sum((x - mx) ** 2 for x, _y in pts)
    if var == 0:
        return 0.0
    cov = sum((x - mx) * (y - my) for x, y in pts)
    return cov / var


@dataclass
class Summary:
    source: str
    rows: int = 0
    primes: int = 0
    prefixes: int = 0
    branch_rows: int = 0
    row_terminal: Counter[str] = field(default_factory=Counter)
    row_split: Counter[int] = field(default_factory=Counter)
    prefix_terminal_masks: Counter[str] = field(default_factory=Counter)
    fiber_hist: Counter[int] = field(default_factory=Counter)
    fiber_by_split: Counter[tuple[int, int]] = field(default_factory=Counter)
    branch_symbol_by_depth: dict[int, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    s_symbol_by_depth: dict[int, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    x_symbol_by_depth: dict[int, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    inv_prefix_counts: dict[int, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    s_inv_prefix_counts: dict[int, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    char_counts: dict[str, Counter[int]] = field(default_factory=lambda: defaultdict(Counter))
    triple_counts: Counter[int] = field(default_factory=Counter)
    prefix_counts: Counter[int] = field(default_factory=Counter)
    x_per_A_values: list[float] = field(default_factory=list)
    min_x_ratios: list[float] = field(default_factory=list)
    min_A_ratios: list[float] = field(default_factory=list)
    reciprocal_closed: int = 0
    reciprocal_total: int = 0
    neg_closed: int = 0
    neg_total: int = 0
    orbit4_closed: int = 0
    orbit4_total: int = 0
    branch_by_terminal: Counter[tuple[str, str]] = field(default_factory=Counter)


def add_chars(summary: Summary, p: int, A: int, x: int, inv: list[int], sqrt: list[int]) -> None:
    f = x * (x * x + A * x + 1)
    values = {
        "A+2": A + 2,
        "A-2": A - 2,
        "A2-4": A * A - 4,
        "x": x,
        "x+1": x + 1,
        "x-1": x - 1,
        "x2-1": x * x - 1,
        "curve_rhs": f,
        "A*x+1": A * x + 1,
        "A+x": A + x,
    }
    if x % p:
        s = (x + inv[x % p]) % p
        values.update(
            {
                "s=x+1/x": s,
                "s+2": s + 2,
                "s-2": s - 2,
                "s+A": s + A,
            }
        )
    for name, value in values.items():
        summary.char_counts[name][chi_from_table(value, p, sqrt)] += 1


def process_prime_block(
    p: int,
    rows: list[tuple[int, int]],
    summary: Summary,
    *,
    branch_depth: int,
    max_prefix: int,
    branch_sample_mod: int,
    branch_sample_residue: int,
) -> None:
    if not rows:
        return
    inv, sqrt = build_tables(p)
    summary.primes += 1
    summary.rows += len(rows)
    summary.triple_counts[p] += len(rows)

    by_A: dict[int, list[int]] = defaultdict(list)
    row_set = set(rows)
    for A, x in rows:
        by_A[A].append(x)
        summary.min_x_ratios.append(min(x, p - x) / p)
        summary.min_A_ratios.append(min(A, p - A) / p)
        split = chi_from_table(A * A - 4, p, sqrt)
        summary.row_split[split] += 1
        add_chars(summary, p, A, x, inv, sqrt)

        if x:
            summary.reciprocal_total += 1
            if (A, inv[x]) in row_set:
                summary.reciprocal_closed += 1
        A_neg = (-A) % p
        x_neg = (-x) % p
        summary.neg_total += 1
        if (A_neg, x_neg) in row_set:
            summary.neg_closed += 1
        summary.orbit4_total += 1
        inv_x = inv[x] if x else 0
        orbit = {
            (A, x),
            (A, inv_x),
            (A_neg, x_neg),
            (A_neg, (-inv_x) % p),
        }
        if orbit <= row_set:
            summary.orbit4_closed += 1

        if (hash((p, A, x)) - branch_sample_residue) % branch_sample_mod == 0:
            terminal, s_word, x_word, four_word = chain_and_words(p, A, x, inv, sqrt, branch_depth)
            summary.branch_rows += 1
            summary.row_terminal[terminal] += 1
            inv_four_symbols = list(reversed(four_word.split("."))) if four_word else []
            inv_s_symbols = list(reversed(s_word))
            for depth, symbol in enumerate(inv_four_symbols):
                summary.branch_symbol_by_depth[depth][symbol] += 1
            for depth, symbol in enumerate(inv_s_symbols):
                summary.s_symbol_by_depth[depth][symbol] += 1
            for depth, symbol in enumerate(reversed(x_word)):
                summary.x_symbol_by_depth[depth][symbol] += 1
            for length in range(1, min(max_prefix, len(inv_four_symbols)) + 1):
                summary.inv_prefix_counts[length][".".join(inv_four_symbols[:length])] += 1
            for length in range(1, min(max_prefix, len(inv_s_symbols)) + 1):
                summary.s_inv_prefix_counts[length]["".join(inv_s_symbols[:length])] += 1
            if inv_four_symbols:
                summary.branch_by_terminal[(terminal, inv_four_symbols[0])] += 1

    summary.prefixes += len(by_A)
    summary.prefix_counts[p] += len(by_A)
    for A, xs in by_A.items():
        size = len(xs)
        split = chi_from_table(A * A - 4, p, sqrt)
        summary.fiber_hist[size] += 1
        summary.fiber_by_split[(split, size)] += 1
        summary.x_per_A_values.append(size)

        terminals = set()
        for x in xs:
            if (hash((p, A, x)) - branch_sample_residue) % branch_sample_mod != 0:
                continue
            terminal, _s_word, _x_word, _four_word = chain_and_words(p, A, x, inv, sqrt, branch_depth)
            terminals.add(terminal)
        if terminals:
            summary.prefix_terminal_masks["+".join(sorted(terminals))] += 1


def counter_capture(counter: Counter[str] | Counter[int]) -> tuple[str, int, int, float]:
    total = sum(counter.values())
    if total == 0:
        return "", 0, 0, 0.0
    key, count = max(counter.items(), key=lambda item: (item[1], str(item[0])))
    return str(key), count, total, count / total


def format_counter(counter: Counter, top: int = 12) -> str:
    if not counter:
        return "{}"
    parts = []
    for key, count in counter.most_common(top):
        parts.append(f"{key}:{count}")
    if len(counter) > top:
        parts.append(f"...(+{len(counter) - top})")
    return "{" + ", ".join(parts) + "}"


def build_report(summary: Summary, args: argparse.Namespace) -> str:
    out: list[str] = []
    out.append("full small-triple halving audit")
    out.append(f"source={summary.source}")
    out.append(f"filters=min_p={args.min_p} max_p={args.max_p} mod={args.mod} residue={args.residue} limit={args.limit}")
    out.append(
        f"branch_depth={args.branch_depth} branch_sample_mod={args.branch_sample_mod} "
        f"branch_sample_residue={args.branch_sample_residue} max_prefix={args.max_prefix}"
    )
    out.append(f"rows={summary.rows}")
    out.append(f"primes={summary.primes}")
    out.append(f"distinct_prefixes={summary.prefixes}")
    out.append(f"branch_rows={summary.branch_rows}")
    if summary.primes:
        out.append(f"triple_loglog_exponent={loglog_exponent(sorted(summary.triple_counts.items())):.6f}")
        out.append(f"prefix_loglog_exponent={loglog_exponent(sorted(summary.prefix_counts.items())):.6f}")
    if summary.x_per_A_values:
        q = quantiles(summary.x_per_A_values, (0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
        out.append("x_per_A_quantiles_10_25_50_75_90_99=" + ",".join(f"{v:.3f}" for v in q))
    if summary.min_x_ratios:
        qx = quantiles(summary.min_x_ratios, (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
        qa = quantiles(summary.min_A_ratios, (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
        out.append("min_x_over_p_quantiles_1_10_25_50_75_90_99=" + ",".join(f"{v:.6f}" for v in qx))
        out.append("min_A_over_p_quantiles_1_10_25_50_75_90_99=" + ",".join(f"{v:.6f}" for v in qa))

    out.append(f"row_split_counts={dict(sorted(summary.row_split.items()))}")
    out.append(f"sampled_terminal_counts={dict(sorted(summary.row_terminal.items()))}")
    out.append(f"sampled_prefix_terminal_masks={format_counter(summary.prefix_terminal_masks)}")
    out.append(f"fiber_size_hist_top={format_counter(summary.fiber_hist)}")
    out.append(f"fiber_by_split_top={format_counter(summary.fiber_by_split)}")

    rec_rate = summary.reciprocal_closed / summary.reciprocal_total if summary.reciprocal_total else 0.0
    neg_rate = summary.neg_closed / summary.neg_total if summary.neg_total else 0.0
    orbit_rate = summary.orbit4_closed / summary.orbit4_total if summary.orbit4_total else 0.0
    out.append(
        "symmetry_closure_rates="
        f"reciprocal:{summary.reciprocal_closed}/{summary.reciprocal_total}={rec_rate:.6f} "
        f"negA_negx:{summary.neg_closed}/{summary.neg_total}={neg_rate:.6f} "
        f"orbit4:{summary.orbit4_closed}/{summary.orbit4_total}={orbit_rate:.6f}"
    )

    out.append("low_degree_character_captures")
    char_rows = []
    for name, counter in summary.char_counts.items():
        key, count, total, capture = counter_capture(counter)
        nonzero = counter[-1] + counter[1]
        bias = abs(counter[1] - counter[-1]) / nonzero if nonzero else 0.0
        char_rows.append((capture, name, key, count, total, bias, dict(sorted(counter.items()))))
    for capture, name, key, count, total, bias, counts in sorted(char_rows, reverse=True)[: args.top]:
        out.append(
            f"  feature={name} best={key} count={count}/{total} capture={capture:.6f} "
            f"signed_bias={bias:.6f} counts={counts}"
        )

    if summary.branch_rows:
        out.append("inverse_depth_four_symbol_captures")
        for depth in sorted(summary.branch_symbol_by_depth)[: args.depth_top]:
            counter = summary.branch_symbol_by_depth[depth]
            key, count, total, capture = counter_capture(counter)
            out.append(f"  depth={depth} best={key} count={count}/{total} capture={capture:.6f} counts={dict(counter)}")
        out.append("inverse_depth_s_symbol_captures")
        for depth in sorted(summary.s_symbol_by_depth)[: args.depth_top]:
            counter = summary.s_symbol_by_depth[depth]
            key, count, total, capture = counter_capture(counter)
            out.append(f"  depth={depth} best={key} count={count}/{total} capture={capture:.6f} counts={dict(counter)}")
        out.append("inverse_depth_x_symbol_captures")
        for depth in sorted(summary.x_symbol_by_depth)[: args.depth_top]:
            counter = summary.x_symbol_by_depth[depth]
            key, count, total, capture = counter_capture(counter)
            out.append(f"  depth={depth} best={key} count={count}/{total} capture={capture:.6f} counts={dict(counter)}")
        out.append("inverse_four_prefix_captures")
        for length in sorted(summary.inv_prefix_counts):
            counter = summary.inv_prefix_counts[length]
            key, count, total, capture = counter_capture(counter)
            expected = 4.0 ** (-length)
            out.append(
                f"  length={length} best={key} count={count}/{total} capture={capture:.6f} "
                f"uniform4_expected={expected:.6f}"
            )
        out.append("inverse_s_prefix_captures")
        for length in sorted(summary.s_inv_prefix_counts):
            counter = summary.s_inv_prefix_counts[length]
            key, count, total, capture = counter_capture(counter)
            expected = 2.0 ** (-length)
            out.append(
                f"  length={length} best={key} count={count}/{total} capture={capture:.6f} "
                f"uniform2_expected={expected:.6f}"
            )
        out.append(f"terminal_by_first_inverse_symbol={format_counter(summary.branch_by_terminal)}")

    out.append(
        "conclusion="
        "x0_data_shows_exact_constant_symmetries_and_near_uniform_inverse_branch_entropy; "
        "no growing statistical_or_algebraic_selector_was_detected"
    )
    return "\n".join(out)


def run(args: argparse.Namespace) -> Summary:
    summary = Summary(source=args.source)
    current_p: int | None = None
    block: list[tuple[int, int]] = []

    for p, A, x in row_stream(
        args.source,
        timeout=args.timeout,
        min_p=args.min_p,
        max_p=args.max_p,
        mod=args.mod,
        residue=args.residue,
        limit=args.limit,
    ):
        if current_p is None:
            current_p = p
        if p != current_p:
            process_prime_block(
                current_p,
                block,
                summary,
                branch_depth=args.branch_depth,
                max_prefix=args.max_prefix,
                branch_sample_mod=args.branch_sample_mod,
                branch_sample_residue=args.branch_sample_residue,
            )
            current_p = p
            block = []
        block.append((A, x))

    if current_p is not None:
        process_prime_block(
            current_p,
            block,
            summary,
            branch_depth=args.branch_depth,
            max_prefix=args.max_prefix,
            branch_sample_mod=args.branch_sample_mod,
            branch_sample_residue=args.branch_sample_residue,
        )
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(PP12), help="local path or http(s) URL")
    ap.add_argument("--min-p", type=int, default=0)
    ap.add_argument("--max-p", type=int, default=1 << 63)
    ap.add_argument("--mod", type=int, default=8)
    ap.add_argument("--residue", type=int, default=None)
    ap.add_argument("--limit", type=int, default=None, help="included row limit after filters")
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--branch-depth", type=int, default=-1, help="-1 means full verifier depth")
    ap.add_argument("--branch-sample-mod", type=int, default=1)
    ap.add_argument("--branch-sample-residue", type=int, default=0)
    ap.add_argument("--max-prefix", type=int, default=6)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--depth-top", type=int, default=12)
    ap.add_argument("--output-md", type=Path, default=None)
    args = ap.parse_args()

    if args.branch_sample_mod <= 0:
        raise SystemExit("--branch-sample-mod must be positive")
    args.branch_sample_residue %= args.branch_sample_mod

    summary = run(args)
    report = build_report(summary, args)
    print(report)
    if args.output_md:
        args.output_md.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
