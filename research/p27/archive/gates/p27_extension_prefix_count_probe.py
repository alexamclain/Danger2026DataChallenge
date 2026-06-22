#!/usr/bin/env python3
"""Extension-field counts for the p27 legal selected-prefix source.

This is a lightweight substitute for memory-heavy Magma normalization.  It
counts the trusted label-2 / compactD=-1 source and selected halving prefixes
over GF(7^n), using the same equations as the p27 finite-field probes.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import product


def trim(poly: list[int]) -> list[int]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mod(a: list[int], f: list[int], q: int) -> list[int]:
    a = trim([x % q for x in a])
    f = trim(f[:])
    if not f:
        raise ValueError("zero modulus")
    inv_lc = pow(f[-1], q - 2, q)
    while len(a) >= len(f):
        coeff = a[-1] * inv_lc % q
        shift = len(a) - len(f)
        if coeff:
            for i, value in enumerate(f):
                a[shift + i] = (a[shift + i] - coeff * value) % q
        trim(a)
    return a


def poly_mul(a: list[int], b: list[int], q: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % q
    return trim(out)


def poly_pow_x(exp: int, f: list[int], q: int) -> list[int]:
    result = [1]
    base = [0, 1]
    while exp:
        if exp & 1:
            result = poly_mod(poly_mul(result, base, q), f, q)
        base = poly_mod(poly_mul(base, base, q), f, q)
        exp >>= 1
    return result


def poly_sub(a: list[int], b: list[int], q: int) -> list[int]:
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % q for i in range(n)])


def poly_gcd(a: list[int], b: list[int], q: int) -> list[int]:
    a = trim(a[:])
    b = trim(b[:])
    while b:
        a, b = b, poly_mod(a, b, q)
    if not a:
        return []
    inv_lc = pow(a[-1], q - 2, q)
    return [(x * inv_lc) % q for x in a]


def is_irreducible(f: list[int], q: int) -> bool:
    n = len(f) - 1
    x_poly = [0, 1]
    for i in range(1, n // 2 + 1):
        h = poly_sub(poly_pow_x(q**i, f, q), x_poly, q)
        if len(poly_gcd(f, h, q)) > 1:
            return False
    return poly_mod(poly_sub(poly_pow_x(q**n, f, q), x_poly, q), f, q) == []


def find_irreducible(q: int, n: int) -> list[int]:
    if n == 1:
        return [0, 1]
    for coeffs in product(range(q), repeat=n):
        f = list(coeffs) + [1]
        if f[0] == 0:
            continue
        if is_irreducible(f, q):
            return f
    raise RuntimeError(f"no irreducible degree {n} over GF({q})")


@dataclass
class GF:
    q: int
    n: int
    modulus: list[int]

    def __post_init__(self) -> None:
        self.size = self.q**self.n
        self.coeffs = [self._decode(i) for i in range(self.size)]
        self.const = {i: i % self.q for i in range(-8, 33)}
        self.zero = 0
        self.one = 1
        self.neg_one = self.neg(self.one)
        self.two = self.const[2]
        self.inv2 = self.inv(self.two)
        self.excluded_A = {
            self.zero,
            self.one,
            self.two,
            self.neg(self.one),
            self.neg(self.two),
        }
        self.sqrt_table = self._sqrt_table()

    def _decode(self, value: int) -> tuple[int, ...]:
        coeffs = []
        for _ in range(self.n):
            coeffs.append(value % self.q)
            value //= self.q
        return tuple(coeffs)

    def encode(self, coeffs: list[int]) -> int:
        value = 0
        mul = 1
        for i in range(self.n):
            value += (coeffs[i] % self.q if i < len(coeffs) else 0) * mul
            mul *= self.q
        return value

    def add(self, a: int, b: int) -> int:
        ca = self.coeffs[a]
        cb = self.coeffs[b]
        return self.encode([(ca[i] + cb[i]) % self.q for i in range(self.n)])

    def neg(self, a: int) -> int:
        ca = self.coeffs[a]
        return self.encode([(-ca[i]) % self.q for i in range(self.n)])

    def sub(self, a: int, b: int) -> int:
        return self.add(a, self.neg(b))

    def mul(self, a: int, b: int) -> int:
        ca = self.coeffs[a]
        cb = self.coeffs[b]
        tmp = [0] * (2 * self.n - 1)
        for i, ai in enumerate(ca):
            if ai:
                for j, bj in enumerate(cb):
                    tmp[i + j] = (tmp[i + j] + ai * bj) % self.q
        for deg in range(2 * self.n - 2, self.n - 1, -1):
            coeff = tmp[deg] % self.q
            if coeff:
                shift = deg - self.n
                for i in range(self.n):
                    tmp[shift + i] = (tmp[shift + i] - coeff * self.modulus[i]) % self.q
        return self.encode(tmp[: self.n])

    def sqr(self, a: int) -> int:
        return self.mul(a, a)

    def pow(self, a: int, e: int) -> int:
        result = self.one
        base = a
        while e:
            if e & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            e >>= 1
        return result

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError
        return self.pow(a, self.size - 2)

    def div(self, a: int, b: int) -> int:
        return self.mul(a, self.inv(b))

    def _sqrt_table(self) -> list[list[int]]:
        roots: list[list[int]] = [[] for _ in range(self.size)]
        for a in range(self.size):
            roots[self.sqr(a)].append(a)
        return roots

    def squareclass(self, a: int) -> int:
        if a == 0:
            return 0
        return 1 if self.sqrt_table[a] else -1

    def roots(self, a: int) -> list[int]:
        return self.sqrt_table[a]

    def c(self, value: int) -> int:
        return value % self.q


def x16_a_num(F: GF, y: int) -> int:
    num = F.one
    for coeff in [-8, 24, -32, 8, 32, -48, 32, -8]:
        num = F.add(F.mul(num, y), F.c(coeff))
    return num


def halve_known_d(F: GF, x: int, sd: int) -> list[int]:
    out: set[int] = set()
    for rd in [sd, F.neg(sd)]:
        u = F.add(F.mul(F.two, x), F.mul(F.two, rd))
        w = F.sub(F.sqr(u), F.c(4))
        for sw in F.roots(w):
            out.add(F.mul(F.add(u, sw), F.inv2))
            out.add(F.mul(F.sub(u, sw), F.inv2))
    out.discard(0)
    return sorted(out)


def halve_all(F: GF, a: int, x: int) -> tuple[int, list[int]]:
    d = F.add(F.add(F.sqr(x), F.mul(a, x)), F.one)
    roots = F.roots(d)
    if not roots:
        return F.squareclass(d), []
    return 1, halve_known_d(F, x, roots[0])


def compact_class(F: GF, x: int, w: int, t: int) -> int:
    x2 = F.sqr(x)
    x3 = F.mul(x2, x)
    x4 = F.sqr(x2)
    x5 = F.mul(x4, x)
    x6 = F.mul(x5, x)
    mt = F.add(
        F.add(
            F.add(F.mul(F.c(2), F.mul(w, x2)), F.mul(F.c(2), F.mul(w, x))),
            F.add(F.add(x4, F.mul(F.c(2), x3)), F.sub(F.neg(F.mul(F.c(2), x)), F.one)),
        ),
        F.zero,
    )
    m0 = F.zero
    for term in [
        F.mul(w, x5),
        F.mul(F.c(3), F.mul(w, x4)),
        F.mul(F.c(2), F.mul(w, x3)),
        F.mul(F.c(2), F.mul(w, x2)),
        F.mul(w, x),
        F.neg(w),
        F.mul(F.c(2), x6),
        F.mul(F.c(4), x5),
        F.mul(F.c(4), x3),
        F.neg(F.mul(F.c(2), x2)),
    ]:
        m0 = F.add(m0, term)
    if x == 0:
        return 0
    v = F.mul(F.mul(w, F.add(x2, F.one)), F.inv(x2))
    criterion = F.mul(F.mul(x, v), F.add(m0, F.mul(mt, t)))
    c = F.squareclass(criterion)
    return -c if c else 0


def label2_candidate(F: GF, x: int, w: int, t: int, root_index: int) -> tuple[str, tuple[int, int] | None]:
    if x in (0, F.one):
        return "degenerate", None
    x_minus_1 = F.sub(x, F.one)
    y = F.div(F.mul(F.two, x), x_minus_1)
    y2 = F.sqr(y)
    y3 = F.mul(y2, y)
    nonsplit = F.mul(F.sub(y2, F.two), F.add(F.sub(y2, F.mul(F.c(4), y)), F.two))
    if F.squareclass(nonsplit) != -1:
        return "not_nonsplit", None
    qa = F.sub(y2, F.mul(F.two, y))
    qb = F.sub(F.mul(F.two, y2), y3)
    if qa == 0:
        return "degenerate", None
    sd = F.div(F.mul(F.c(4), t), F.pow(x_minus_1, 3))
    signed_sd = sd if root_index == 0 else F.neg(sd)
    root = F.div(F.sub(signed_sd, qb), F.mul(F.two, qa))

    ym1 = F.sub(y, F.one)
    den_a = F.mul(F.c(4), F.pow(ym1, 4))
    den_x = F.sub(root, y)
    if den_a == 0 or den_x == 0:
        return "degenerate", None
    A = F.div(x16_a_num(F, y), den_a)
    if A in F.excluded_A:
        return "degenerate_A", None
    xp = F.div(root, den_x)

    z = F.div(F.mul(w, sd), F.mul(F.two, x))
    den = F.mul(F.mul(F.two, F.sub(root, y)), F.sqr(ym1))
    if den == 0:
        return "degenerate", None
    sd1 = F.div(F.mul(y, z), den)
    d1 = F.add(F.add(F.sqr(xp), F.mul(A, xp)), F.one)
    if F.sqr(sd1) != d1:
        return "d1_sqrt_mismatch", None
    x5s = halve_known_d(F, xp, sd1)
    if not x5s:
        return "d1_no_half", None
    return "ok", (A, x5s[0])


def selected_prefix_depth(F: GF, A: int, x0: int, depth: int) -> int:
    active = [x0]
    survived = 0
    for _ in range(depth):
        branch_classes: list[int] = []
        next_active: set[int] = set()
        for x in active:
            _, branches = halve_all(F, A, x)
            for branch in branches:
                branch_classes.append(F.squareclass(branch))
                if F.squareclass(branch) == 1:
                    next_active.add(branch)
        vals = {c for c in branch_classes if c in (-1, 1)}
        if vals != {1}:
            break
        survived += 1
        active = sorted(next_active)
        if not active:
            break
    return survived


def count_field(q: int, n: int, depth: int) -> Counter:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    stats: Counter = Counter()
    source_rows = 0
    oriented_candidates: list[tuple[int, int]] = []
    for x in range(F.size):
        if x in (0, F.one):
            stats["skip_x_degenerate"] += 1
            continue
        w2 = F.sub(F.mul(F.sqr(x), x), x)
        t2 = F.mul(F.mul(x, F.add(F.sqr(x), F.one)), F.add(F.add(F.sqr(x), F.mul(F.two, x)), F.neg(F.one)))
        for w in F.roots(w2):
            for t in F.roots(t2):
                comp = compact_class(F, x, w, t)
                if comp != -1:
                    stats["compact_not_target"] += 1
                    continue
                source_rows += 1
                for ri in [0, 1]:
                    reason, cand = label2_candidate(F, x, w, t, ri)
                    if cand is None:
                        stats[f"candidate_invalid_{reason}"] += 1
                    else:
                        oriented_candidates.append(cand)

    unique_ax = set(oriented_candidates)
    unique_A = {A for A, _ in unique_ax}
    prefix_ax = [set() for _ in range(depth + 1)]
    prefix_A = [set() for _ in range(depth + 1)]
    for A, x in unique_ax:
        survived = selected_prefix_depth(F, A, x, depth)
        for d in range(survived + 1):
            prefix_ax[d].add((A, x))
            prefix_A[d].add(A)
    stats["field_size"] = F.size
    stats["source_rows"] = source_rows
    stats["oriented_candidates"] = len(oriented_candidates)
    stats["unique_ax"] = len(unique_ax)
    stats["unique_A"] = len(unique_A)
    for d in range(depth + 1):
        stats[f"depth{d}_ax"] = len(prefix_ax[d])
        stats[f"depth{d}_A"] = len(prefix_A[d])
    return stats


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def print_stats(q: int, n: int, stats: Counter, depth: int) -> None:
    N = stats["field_size"]
    print(f"GF({q}^{n}) N={N}:")
    for key in [
        "source_rows",
        "oriented_candidates",
        "unique_ax",
        "unique_A",
        "candidate_invalid_degenerate",
        "candidate_invalid_degenerate_A",
        "candidate_invalid_not_nonsplit",
        "candidate_invalid_d1_sqrt_mismatch",
        "candidate_invalid_d1_no_half",
    ]:
        if key in stats:
            print(f"  {key} = {stats[key]}")
    for d in range(depth + 1):
        ax = stats[f"depth{d}_ax"]
        A = stats[f"depth{d}_A"]
        print(
            f"  depth{d}: ax={ax} A={A} "
            f"ax/N={ax / N:.9f} A/N={A / N:.9f} "
            f"scaled_ax={(ax / stats['depth0_ax'] * (2**d)) if stats['depth0_ax'] else 0.0:.6f} "
            f"scaled_A={(A / stats['depth0_A'] * (2**d)) if stats['depth0_A'] else 0.0:.6f}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=7)
    parser.add_argument("--degrees", default="1,2,3,4")
    parser.add_argument("--depth", type=int, default=5)
    args = parser.parse_args()

    print("p27 extension-field legal selected-prefix count probe")
    print("source = residual E/T cover + compactD=-1 + label-2 candidate map")
    for n in parse_ints(args.degrees):
        print_stats(args.q, n, count_field(args.q, n, args.depth), args.depth)
    print("p27_extension_prefix_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
