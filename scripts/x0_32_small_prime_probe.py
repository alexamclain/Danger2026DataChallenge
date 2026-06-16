#!/usr/bin/env python3
"""Small-prime X0(32) sampler probe.

This is a research helper, not a p23 production sampler. It tests the
second-round X0(32) route:

    X0(32): v^4 = 1 - u^2
    u -> j(u)
    j -> Montgomery A by solving a cubic in B = A^2
    x=0 -> order-32 x-only state by four inverse doublings

The goal is to check whether the algebraic lift can produce validated
order-32 Montgomery x-states and to get rough small-prime acceptance/timing
numbers before considering a C implementation.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter

import sympy as sp

try:
    import x16_trace_residue_calibration as trace_cal
except ImportError:  # pragma: no cover - optional research mode only
    trace_cal = None


def inv(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError
    return pow(a, p - 2, p)


def sqrt_mod_roots(a: int, p: int) -> list[int]:
    return sorted(int(r) % p for r in sp.sqrt_mod(a % p, p, all_roots=True))


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def cheap_feature_values(p: int, v: int, u: int, A: int) -> dict[str, int]:
    """Low-cost symbols available before or immediately after the X0(32)->A map."""
    v %= p
    u %= p
    A %= p
    u2 = u * u % p
    v2 = v * v % p
    return {
        "u": u,
        "u-1": u - 1,
        "u+1": u + 1,
        "u^2+1": u2 + 1,
        "u^2+u+1": u2 + u + 1,
        "u^2-u+1": u2 - u + 1,
        "v": v,
        "v^2-1": v2 - 1,
        "v^2+1": v2 + 1,
        "A": A,
        "A^2-4": A * A - 4,
    }


def feature_signs(p: int, v: int, u: int, A: int) -> dict[str, int]:
    return {name: legendre(value, p) for name, value in cheap_feature_values(p, v, u, A).items()}


def state_feature_values(p: int, A: int, x: int) -> dict[str, int]:
    """Cheap symbols attached to a produced order-32 x-only state."""
    A %= p
    x %= p
    x2 = x * x % p
    x3 = x2 * x % p
    dbl_den = (x2 + A * x + 1) % p
    curve_rhs = (x3 + A * x2 + x) % p
    return {
        "state_x": x,
        "state_x-1": x - 1,
        "state_x+1": x + 1,
        "state_dbl_den": dbl_den,
        "state_curve_rhs": curve_rhs,
        "state_Ax+1": A * x + 1,
    }


def state_feature_signs(p: int, A: int, x: int) -> dict[str, int]:
    return {name: legendre(value, p) for name, value in state_feature_values(p, A, x).items()}


def j_x0_32(u: int, p: int) -> int | None:
    u %= p
    den = u * pow((1 - u) % p, 8, p) % p * pow((1 + u) % p, 2, p) % p
    if den == 0:
        return None
    poly = (pow(u, 4, p) + 60 * pow(u, 3, p) + 134 * u * u + 60 * u + 1) % p
    return 4 * pow(poly, 3, p) % p * inv(den, p) % p


def cubic_B_roots_from_j(j: int, p: int, root_method: str) -> list[int]:
    """Solve 256*(B-3)^3 - j*(B-4) = 0."""
    if root_method == "auto":
        root_method = "brute" if p <= 200_000 else "sympy"

    if root_method == "brute":
        return [
            B
            for B in range(p)
            if (256 * pow((B - 3) % p, 3, p) - j * ((B - 4) % p)) % p == 0
        ]

    B = sp.symbols("B")
    poly = sp.Poly(256 * (B - 3) ** 3 - j * (B - 4), B, modulus=p)
    return sorted({int(root) % p for root in poly.ground_roots()})


def montgomery_As_from_j(j: int, p: int, root_method: str) -> list[int]:
    """Solve 256*(B-3)^3 - j*(B-4) = 0, then A^2 = B."""
    As: set[int] = set()
    for B in cubic_B_roots_from_j(j, p, root_method):
        for A in sqrt_mod_roots(B, p):
            if (A * A - 4) % p != 0:
                As.add(A)
    return sorted(As)


def inverse_halves(p: int, A: int, t: int) -> list[int]:
    """All affine x with Montgomery x-doubling equal to t."""
    out: set[int] = set()
    inv2 = (p + 1) // 2
    d = (t * t + A * t + 1) % p
    for sd in sqrt_mod_roots(d, p):
        for uu in {(2 * t + 2 * sd) % p, (2 * t - 2 * sd) % p}:
            w = (uu * uu - 4) % p
            for sw in sqrt_mod_roots(w, p):
                out.add(((uu + sw) * inv2) % p)
                out.add(((uu - sw) * inv2) % p)
    out.discard(0)
    return sorted(out)


def lift_from_two_torsion(p: int, A: int, levels: int = 4) -> list[int]:
    frontier = {0}
    for _ in range(levels):
        nxt: set[int] = set()
        for t in frontier:
            nxt.update(inverse_halves(p, A, t))
        frontier = nxt
        if not frontier:
            break
    return sorted(frontier)


def mong_dbl(p: int, A: int, X: int, Z: int) -> tuple[int, int]:
    X2 = X * X % p
    Z2 = Z * Z % p
    XZ = X * Z % p
    Xn = (X2 - Z2) ** 2 % p
    Zn = 4 * XZ * (X2 + A * XZ + Z2) % p
    return Xn, Zn


def xonly_zero_step(p: int, A: int, x0: int, max_steps: int = 16) -> int | None:
    X, Z = x0 % p, 1
    for step in range(1, max_steps + 1):
        X, Z = mong_dbl(p, A, X, Z)
        if Z == 0:
            return step
    return None


def halve_once_first(p: int, A: int, x: int) -> int | None:
    halves = inverse_halves(p, A, x)
    return halves[0] if halves else None


def current_k(p: int) -> int:
    q = int(sp.integer_nthroot(p, 2)[0])
    return (q + 1 + int(sp.integer_nthroot(4 * q, 2)[0])).bit_length()


def v2(n: int) -> int:
    if n == 0:
        return 0
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def first_branch_depth(p: int, A: int, x: int, start_depth: int, target_depth: int) -> int:
    depth = start_depth
    while depth < target_depth:
        nx = halve_once_first(p, A, x)
        if nx is None:
            break
        x = nx
        depth += 1
    return depth


def all_branch_reaches(
    p: int,
    A: int,
    x: int,
    start_depth: int,
    target_depth: int,
    frontier_limit: int,
) -> tuple[bool, int]:
    frontier = {x}
    max_frontier = len(frontier)
    for _depth in range(start_depth, target_depth):
        nxt: set[int] = set()
        for t in frontier:
            nxt.update(inverse_halves(p, A, t))
            if frontier_limit and len(nxt) > frontier_limit:
                return True, len(nxt)
        frontier = nxt
        max_frontier = max(max_frontier, len(frontier))
        if not frontier:
            return False, max_frontier
    return True, max_frontier


def sample_x0_32_order32_states(
    p: int,
    rng: random.Random,
    samples: int,
    root_method: str,
    target_depth_override: int,
    all_depth: int,
    all_max_states: int,
    all_frontier_limit: int,
    feature_scan: bool,
    trace_scan: bool,
) -> dict[str, object]:
    counters: Counter[str] = Counter()
    zero_steps: Counter[int] = Counter()
    depth_hist: Counter[int] = Counter()
    class_counts: Counter[str] = Counter()
    class_depth_hist: Counter[str] = Counter()
    all_depth_hist: Counter[str] = Counter()
    feature_totals: Counter[str] = Counter()
    feature_depth_hits: dict[int, Counter[str]] = {
        8: Counter(),
        9: Counter(),
        10: Counter(),
        11: Counter(),
        12: Counter(),
    }
    examples: list[tuple[int, int, int, int, int]] = []
    unique_pairs: set[tuple[int, int]] = set()
    unique_As: set[int] = set()
    per_A_state_counts: Counter[int] = Counter()
    per_A_max_depth: dict[int, int] = {}
    per_A_class: dict[int, str] = {}
    per_A_all_reached: set[int] = set()
    trace_cache: dict[int, tuple[int, int]] = {}
    trace_v2_depth_hist: Counter[str] = Counter()
    per_A_trace_v2_depth_hist: Counter[str] = Counter()
    target_depth = target_depth_override or current_k(p)

    if trace_scan and trace_cal is None:
        raise RuntimeError("trace scan requested but x16_trace_residue_calibration could not be imported")

    start = time.perf_counter()
    for _ in range(samples):
        counters["v_samples"] += 1
        v = rng.randrange(0, p)
        rhs = (1 - pow(v, 4, p)) % p
        u_roots = sqrt_mod_roots(rhs, p)
        if not u_roots:
            continue
        counters["x0_points"] += len(u_roots)
        for u in u_roots:
            if u in (0, 1, p - 1):
                continue
            j = j_x0_32(u, p)
            if j is None:
                continue
            counters["j_values"] += 1
            As = montgomery_As_from_j(j, p, root_method)
            counters["montgomery_A_values"] += len(As)
            for A in As:
                unique_As.add(A)
                states = lift_from_two_torsion(p, A, levels=4)
                counters["lifted_states"] += len(states)
                cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
                per_A_class.setdefault(A, cls)
                signs = feature_signs(p, v, u, A) if feature_scan else {}
                if trace_scan and A not in trace_cache:
                    assert trace_cal is not None
                    trace = trace_cal.trace_for_montgomery_A(p, A)
                    group_order = p + 1 - trace
                    trace_cache[A] = (trace, v2(group_order))
                for x in states:
                    step = xonly_zero_step(p, A, x, max_steps=8)
                    zero_steps[step if step is not None else -1] += 1
                    if step != 5:
                        continue
                    counters["order32_states"] += 1
                    unique_pairs.add((A, x))
                    class_counts[cls] += 1
                    depth = first_branch_depth(p, A, x, 5, target_depth)
                    depth_hist[depth] += 1
                    class_depth_hist[f"{cls}:{depth}"] += 1
                    if trace_scan:
                        trace_v2_depth_hist[f"v2N={trace_cache[A][1]}:depth={depth}"] += 1
                    per_A_state_counts[A] += 1
                    per_A_max_depth[A] = max(per_A_max_depth.get(A, 0), depth)
                    if feature_scan:
                        state_signs = state_feature_signs(p, A, x)
                        for name, sign in signs.items():
                            key = f"{name}:{sign:+d}"
                            feature_totals[key] += 1
                            for threshold, hits in feature_depth_hits.items():
                                if depth >= threshold:
                                    hits[key] += 1
                        for name, sign in state_signs.items():
                            key = f"{name}:{sign:+d}"
                            feature_totals[key] += 1
                            for threshold, hits in feature_depth_hits.items():
                                if depth >= threshold:
                                    hits[key] += 1
                    if all_depth and (not all_max_states or counters["all_checked"] < all_max_states):
                        counters["all_checked"] += 1
                        reached, max_frontier = all_branch_reaches(
                            p, A, x, 5, all_depth, all_frontier_limit
                        )
                        if reached:
                            counters["all_reached"] += 1
                            per_A_all_reached.add(A)
                        counters["all_max_frontier_sum"] += max_frontier
                        all_depth_hist[f"{'reached' if reached else 'failed'}:{max_frontier}"] += 1
                    if len(examples) < 5:
                        examples.append((v, u, A, x, depth))

    elapsed = time.perf_counter() - start
    counters["unique_order32_pairs"] = len(unique_pairs)
    counters["unique_A_values"] = len(unique_As)
    counters["unique_order32_A_values"] = len(per_A_state_counts)
    per_A_depth_hist = Counter(per_A_max_depth.values())
    per_A_class_depth_hist = Counter(
        f"{per_A_class.get(A, 'unknown')}:{depth}" for A, depth in per_A_max_depth.items()
    )
    per_A_state_hist = Counter(per_A_state_counts.values())
    per_A_all_reached_hist = Counter(
        "reached" if A in per_A_all_reached else "failed" for A in per_A_state_counts
    )
    if trace_scan:
        for A, depth in per_A_max_depth.items():
            per_A_trace_v2_depth_hist[f"v2N={trace_cache[A][1]}:depth={depth}"] += 1
    return {
        "elapsed": elapsed,
        "target_depth": target_depth,
        "counters": counters,
        "zero_steps": zero_steps,
        "depth_hist": depth_hist,
        "class_counts": class_counts,
        "class_depth_hist": class_depth_hist,
        "all_depth_hist": all_depth_hist,
        "per_A_depth_hist": per_A_depth_hist,
        "per_A_class_depth_hist": per_A_class_depth_hist,
        "per_A_state_hist": per_A_state_hist,
        "per_A_all_reached_hist": per_A_all_reached_hist,
        "trace_v2_depth_hist": trace_v2_depth_hist,
        "per_A_trace_v2_depth_hist": per_A_trace_v2_depth_hist,
        "feature_totals": feature_totals,
        "feature_depth_hits": feature_depth_hits,
        "examples": examples,
    }


def top_feature_rows(
    feature_totals: Counter[str],
    feature_depth_hits: dict[int, Counter[str]],
    threshold: int,
    base_hits: int,
    total: int,
    top: int,
) -> list[str]:
    if not top or threshold not in feature_depth_hits or not total:
        return []
    base_rate = base_hits / total if total else 0.0
    rows: list[tuple[float, str]] = []
    hits_for_threshold = feature_depth_hits[threshold]
    for key, selected in feature_totals.items():
        if not selected:
            continue
        hits = hits_for_threshold[key]
        precision = hits / selected
        coverage = selected / total
        capture = hits / base_hits if base_hits else 0.0
        lift = precision / base_rate if base_rate else 0.0
        score = lift * capture
        rows.append((
            score,
            (
                f"depth>={threshold} feature={key} selected={selected} hits={hits} "
                f"coverage={coverage:.4f} capture={capture:.4f} "
                f"precision={precision:.4f} lift={lift:.3f}"
            ),
        ))
    return [row for _score, row in sorted(rows, reverse=True)[:top]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=1009)
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260601)
    ap.add_argument("--root-method", choices=("auto", "brute", "sympy"), default="auto")
    ap.add_argument("--target-depth", type=int, default=0, help="override first-branch target depth")
    ap.add_argument("--all-depth", type=int, default=0, help="optional bounded all-branch target depth")
    ap.add_argument("--all-max-states", type=int, default=0, help="cap order32 states checked by all-branch")
    ap.add_argument("--all-frontier-limit", type=int, default=4096, help="soft frontier cap for all-branch")
    ap.add_argument("--feature-scan", action="store_true", help="scan cheap Legendre features against depth tails")
    ap.add_argument("--feature-top", type=int, default=8, help="rows to print per feature threshold")
    ap.add_argument(
        "--trace-scan",
        action="store_true",
        help="small-prime only: brute-force point count each unique A and correlate v2(#E) with depth",
    )
    args = ap.parse_args()

    if args.p <= 3 or not sp.isprime(args.p):
        raise SystemExit("--p must be an odd prime")

    rng = random.Random(args.seed)
    root_method = args.root_method
    if root_method == "auto":
        root_method = "brute" if args.p <= 200_000 else "sympy"
    result = sample_x0_32_order32_states(
        args.p,
        rng,
        args.samples,
        root_method,
        args.target_depth,
        args.all_depth,
        args.all_max_states,
        args.all_frontier_limit,
        args.feature_scan,
        args.trace_scan,
    )
    counters: Counter[str] = result["counters"]  # type: ignore[assignment]
    zero_steps: Counter[int] = result["zero_steps"]  # type: ignore[assignment]
    depth_hist: Counter[int] = result["depth_hist"]  # type: ignore[assignment]
    class_counts: Counter[str] = result["class_counts"]  # type: ignore[assignment]
    class_depth_hist: Counter[str] = result["class_depth_hist"]  # type: ignore[assignment]
    all_depth_hist: Counter[str] = result["all_depth_hist"]  # type: ignore[assignment]
    per_A_depth_hist: Counter[int] = result["per_A_depth_hist"]  # type: ignore[assignment]
    per_A_class_depth_hist: Counter[str] = result["per_A_class_depth_hist"]  # type: ignore[assignment]
    per_A_state_hist: Counter[int] = result["per_A_state_hist"]  # type: ignore[assignment]
    per_A_all_reached_hist: Counter[str] = result["per_A_all_reached_hist"]  # type: ignore[assignment]
    trace_v2_depth_hist: Counter[str] = result["trace_v2_depth_hist"]  # type: ignore[assignment]
    per_A_trace_v2_depth_hist: Counter[str] = result["per_A_trace_v2_depth_hist"]  # type: ignore[assignment]
    feature_totals: Counter[str] = result["feature_totals"]  # type: ignore[assignment]
    feature_depth_hits: dict[int, Counter[str]] = result["feature_depth_hits"]  # type: ignore[assignment]

    elapsed = float(result["elapsed"])
    print("X0(32) small-prime sampler probe")
    print(f"p={args.p}")
    print(f"samples={args.samples}")
    print(f"seed={args.seed}")
    print(f"root_method={root_method}")
    print(f"target_depth={result['target_depth']}")
    if args.all_depth:
        print(f"all_depth={args.all_depth}")
        print(f"all_max_states={args.all_max_states}")
        print(f"all_frontier_limit={args.all_frontier_limit}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"v_samples_per_second={args.samples / elapsed:.3f}" if elapsed else "v_samples_per_second=inf")
    if counters["order32_states"]:
        print(f"order32_states_per_second={counters['order32_states'] / elapsed:.3f}")
    else:
        print("order32_states_per_second=0.000")
    print()
    for key in [
        "v_samples",
        "x0_points",
        "j_values",
        "montgomery_A_values",
        "lifted_states",
        "order32_states",
        "unique_order32_pairs",
        "unique_A_values",
        "unique_order32_A_values",
    ]:
        print(f"{key}={counters[key]}")
    print("zero_step_hist=" + ",".join(f"{k}:{zero_steps[k]}" for k in sorted(zero_steps)))
    print("first_branch_depth_hist=" + ",".join(f"{k}:{depth_hist[k]}" for k in sorted(depth_hist)))
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print("split_class_depth_hist=" + ",".join(f"{k}:{class_depth_hist[k]}" for k in sorted(class_depth_hist)))
    print("per_A_max_first_depth_hist=" + ",".join(f"{k}:{per_A_depth_hist[k]}" for k in sorted(per_A_depth_hist)))
    print("per_A_split_class_depth_hist=" + ",".join(f"{k}:{per_A_class_depth_hist[k]}" for k in sorted(per_A_class_depth_hist)))
    print("per_A_order32_state_count_hist=" + ",".join(f"{k}:{per_A_state_hist[k]}" for k in sorted(per_A_state_hist)))
    if args.all_depth:
        all_checked = counters["all_checked"]
        all_avg_frontier = (
            counters["all_max_frontier_sum"] / all_checked if all_checked else 0.0
        )
        print(f"all_checked={all_checked}")
        print(f"all_reached={counters['all_reached']}")
        print(f"all_avg_max_frontier={all_avg_frontier:.3f}")
        print("all_depth_hist=" + ",".join(f"{k}:{all_depth_hist[k]}" for k in sorted(all_depth_hist)))
        print("per_A_all_reached_hist=" + ",".join(f"{k}:{per_A_all_reached_hist[k]}" for k in sorted(per_A_all_reached_hist)))
    if args.feature_scan:
        total = counters["order32_states"]
        print("feature_scan=enabled")
        for threshold in sorted(feature_depth_hits):
            base_hits = sum(count for depth, count in depth_hist.items() if depth >= threshold)
            print(f"feature_threshold depth>={threshold} base_hits={base_hits} total={total}")
            for row in top_feature_rows(
                feature_totals,
                feature_depth_hits,
                threshold,
                base_hits,
                total,
                args.feature_top,
            ):
                print(row)
    if args.trace_scan:
        print("trace_scan=enabled")
        print(
            "trace_v2_depth_hist="
            + ",".join(f"{k}:{trace_v2_depth_hist[k]}" for k in sorted(trace_v2_depth_hist))
        )
        print(
            "per_A_trace_v2_depth_hist="
            + ",".join(f"{k}:{per_A_trace_v2_depth_hist[k]}" for k in sorted(per_A_trace_v2_depth_hist))
        )
    print("examples=v,u,A,x,first_branch_depth")
    for row in result["examples"]:  # type: ignore[index]
        print(",".join(str(x) for x in row))


if __name__ == "__main__":
    main()
