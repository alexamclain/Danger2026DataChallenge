#!/usr/bin/env python3
"""Natural symmetry screen for the p27 trace/norm Dplus cover.

The direct source-orientation cover is too large to sample naively.  Before
asking for a heavier CAS decomposition, test the obvious quotient candidates:
the z/w deck flips on

    z^2 = t(t^2+2t-1)(t^2+1)
    w^2 = -(t^2+2t-1)(t^2-2t-1)

and the domain involution t -> -1/t, with the induced z,w scalings.

If the Dplus squareclass is invariant under one of these maps, it may descend
to a smaller quotient.  If every natural map mixes Dplus and Dminus, the next
route needs a non-obvious Prym/quotient rather than the visible deck group.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import product


def leg(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1


def sqrt_mod(a: int, q: int) -> int | None:
    a %= q
    if a == 0:
        return 0
    if leg(a, q) != 1:
        return None
    if q % 4 == 3:
        return pow(a, (q + 1) // 4, q)
    for x in range(1, q):
        if x * x % q == a:
            return x
    return None


def roots2(a: int, q: int) -> list[int]:
    root = sqrt_mod(a, q)
    if root is None:
        return []
    if root == 0:
        return [0]
    return [root, (-root) % q]


@dataclass(frozen=True)
class Row:
    t: int
    z: int
    w: int
    dplus: int
    eps_h: int
    eps_v: int


def parts(t: int, q: int) -> tuple[int, int, int, int, int]:
    t %= q
    y = (t + 1) % q
    b = (t * t + 1) % q
    c = (t * t + 2 * t - 1) % q
    r = (t * t - 2 * t - 1) % q
    return y, b, c, r, (-c * r) % q


def core_and_signs(t: int, z: int, w: int, q: int) -> tuple[int, int, int, int] | None:
    t %= q
    z %= q
    w %= q
    y, b, c, _r, _k = parts(t, q)
    eps_h = leg(t, q)
    eps_v = leg(y * c, q)
    if eps_h == 0 or eps_v == 0:
        return None
    hcore = (c * b + eps_h * 2 * t * z) % q
    vcore = (2 * c * t * t + eps_v * z * w) % q
    core = (1 - t * t) % q
    core = core * b % q
    core = core * c % q
    core = core * y % q
    core = core * vcore % q
    core = core * hcore % q
    dplus = leg((-core) % q, q)
    return core, dplus, eps_h, eps_v


def is_valid_base(t: int, z: int, w: int, q: int) -> bool:
    y, b, c, _r, k = parts(t, q)
    f = t * c % q * b % q
    return z * z % q == f and w * w % q == k and y is not None


def collect_rows(q: int) -> list[Row]:
    rows: list[Row] = []
    for t in range(q):
        y, b, c, _r, k = parts(t, q)
        f = t * c % q * b % q
        if t == 0 or y == 0 or b == 0 or c == 0 or k == 0 or f == 0:
            continue
        for z in roots2(f, q):
            for w in roots2(k, q):
                pack = core_and_signs(t, z, w, q)
                if pack is None:
                    continue
                _core, dplus, eps_h, eps_v = pack
                rows.append(Row(t=t, z=z, w=w, dplus=dplus, eps_h=eps_h, eps_v=eps_v))
    return rows


def transform(row: Row, name: str, q: int) -> tuple[int, int, int] | None:
    t, z, w = row.t, row.z, row.w
    if name == "zflip":
        return t, (-z) % q, w
    if name == "wflip":
        return t, z, (-w) % q
    if name == "zwflip":
        return t, (-z) % q, (-w) % q
    if name.startswith("iota"):
        if t == 0:
            return None
        inv_t = pow(t, q - 2, q)
        inv_t2 = inv_t * inv_t % q
        inv_t3 = inv_t2 * inv_t % q
        _, sz_name, sw_name = name.split("_")
        sz = 1 if sz_name == "zp" else -1
        sw = 1 if sw_name == "wp" else -1
        return (-inv_t) % q, sz * z * inv_t3 % q, sw * w * inv_t2 % q
    raise ValueError(name)


def transition_stats(rows: list[Row], q: int, name: str) -> Counter[str]:
    stats: Counter[str] = Counter()
    by_orientation: Counter[str] = Counter()
    for row in rows:
        stats["rows"] += 1
        image = transform(row, name, q)
        if image is None:
            stats["undefined"] += 1
            continue
        t2, z2, w2 = image
        if not is_valid_base(t2, z2, w2, q):
            stats["invalid_base"] += 1
            continue
        pack = core_and_signs(t2, z2, w2, q)
        if pack is None:
            stats["invalid_core"] += 1
            continue
        _core2, d2, eh2, ev2 = pack
        stats["valid"] += 1
        if d2 == row.dplus:
            stats["same"] += 1
        elif d2 == -row.dplus:
            stats["flipped"] += 1
        else:
            stats["zero"] += 1
        if row.dplus == 1:
            stats["src_dplus"] += 1
            if d2 == 1:
                stats["dplus_to_dplus"] += 1
            elif d2 == -1:
                stats["dplus_to_dminus"] += 1
        elif row.dplus == -1:
            stats["src_dminus"] += 1
            if d2 == 1:
                stats["dminus_to_dplus"] += 1
            elif d2 == -1:
                stats["dminus_to_dminus"] += 1
        label = f"{row.eps_h},{row.eps_v}->{eh2},{ev2}"
        by_orientation[label] += 1
    stats.update({f"orientation_{key}": value for key, value in by_orientation.items()})
    return stats


def print_stats(q: int, rows: list[Row], name: str, stats: Counter[str]) -> None:
    valid = stats["valid"]
    same = stats["same"]
    flipped = stats["flipped"]
    print(f"q{q}_{name}:")
    for key in (
        "rows",
        "valid",
        "invalid_base",
        "invalid_core",
        "undefined",
        "same",
        "flipped",
        "zero",
        "src_dplus",
        "dplus_to_dplus",
        "dplus_to_dminus",
        "src_dminus",
        "dminus_to_dplus",
        "dminus_to_dminus",
    ):
        print(f"  {key} = {stats[key]}")
    same_rate = same / valid if valid else 0.0
    flipped_rate = flipped / valid if valid else 0.0
    dplus_stay = stats["dplus_to_dplus"] / stats["src_dplus"] if stats["src_dplus"] else 0.0
    print(f"  same_rate = {same_rate:.9f}")
    print(f"  flipped_rate = {flipped_rate:.9f}")
    print(f"  dplus_stay_rate = {dplus_stay:.9f}")
    for key in sorted(k for k in stats if k.startswith("orientation_")):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qs", default="607,1607,1847,2087")
    args = parser.parse_args()

    qs = [int(part) for part in args.qs.split(",") if part]
    names = ["zflip", "wflip", "zwflip"]
    for sz, sw in product(("zp", "zm"), ("wp", "wm")):
        names.append(f"iota_{sz}_{sw}")

    print("p27 trace/norm Dplus natural symmetry probe")
    print("question = does Dplus descend under z/w deck flips or t -> -1/t?")
    print("transforms = " + ",".join(names))
    for q in qs:
        rows = collect_rows(q)
        counts = Counter(row.dplus for row in rows)
        orientation_counts = Counter((row.eps_h, row.eps_v) for row in rows)
        print(f"q{q}_sample:")
        print(f"  rows = {len(rows)}")
        print(f"  dplus_+1 = {counts[1]}")
        print(f"  dplus_-1 = {counts[-1]}")
        for eh, ev in product((1, -1), (1, -1)):
            print(f"  orientation_{eh}_{ev} = {orientation_counts[(eh, ev)]}")
        for name in names:
            print_stats(q, rows, name, transition_stats(rows, q, name))
    print("p27_trace_norm_dplus_symmetry_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
