#!/usr/bin/env python3
"""Extension-field counts for the p27 B-line gamma cover.

The prime-field reduced-cover count is a useful guard, but the remaining
question is geometric: does the staged selector

    gamma^2 = U_next + 2

look like a sourceable low-genus class, or like another fresh half-cover after
the legal/core source cut?  This probe repeats the reduced-cover point count
over small extension fields GF(p^n), using the same eta=+1 source chart as the
prime-field probe.

This is not a substitute for Magma/Sage normalization.  It is a denominator
audit and a falsifier: if the selector/materialization layers keep behaving
like ordinary half-covers over extensions, GPU production remains unjustified
until a real quotient, coboundary, or recurrence is extracted.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import product

import sympy as sp


def parse_field_specs(raw: str) -> list[tuple[int, int]]:
    specs: list[tuple[int, int]] = []
    for part in raw.split(","):
        part = part.strip().lower()
        if not part:
            continue
        if "^" in part:
            p_raw, n_raw = part.split("^", 1)
            specs.append((int(p_raw), int(n_raw)))
        else:
            specs.append((int(part), 1))
    return specs


def factor_int(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


@lru_cache(maxsize=None)
def irreducible_modulus(p: int, n: int) -> tuple[int, ...]:
    """Return low-to-high coefficients c0..c_{n-1} for x^n + sum c_i x^i."""

    if n == 1:
        return (0,)
    x = sp.Symbol("x")
    for coeffs in product(range(p), repeat=n):
        poly = sp.Poly(x**n + sum(coeffs[i] * x**i for i in range(n)), x, modulus=p)
        if poly.is_irreducible:
            return tuple(int(c) % p for c in coeffs)
    raise RuntimeError(f"no irreducible polynomial found for GF({p}^{n})")


@dataclass(frozen=True)
class GF:
    p: int
    n: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "q", self.p**self.n)
        object.__setattr__(self, "modulus", irreducible_modulus(self.p, self.n))
        coeffs = [self._decode_raw(a) for a in range(self.q)]
        object.__setattr__(self, "coeffs", coeffs)
        neg = [self._encode_raw([(-c) % self.p for c in row]) for row in coeffs]
        object.__setattr__(self, "neg_table", neg)
        if self.q > 1:
            primitive = self._find_primitive()
            exp: list[int] = []
            log = [-1] * self.q
            cur = 1
            for i in range(self.q - 1):
                exp.append(cur)
                log[cur] = i
                cur = self._mul_poly(cur, primitive)
            object.__setattr__(self, "primitive", primitive)
            object.__setattr__(self, "exp_table", exp)
            object.__setattr__(self, "log_table", log)

    def _decode_raw(self, a: int) -> tuple[int, ...]:
        out = []
        for _ in range(self.n):
            out.append(a % self.p)
            a //= self.p
        return tuple(out)

    def _encode_raw(self, coeffs: list[int] | tuple[int, ...]) -> int:
        value = 0
        scale = 1
        for coeff in coeffs:
            value += (coeff % self.p) * scale
            scale *= self.p
        return value

    def _add_raw(self, a: int, b: int) -> int:
        ac = self.coeffs[a]
        bc = self.coeffs[b]
        return self._encode_raw([(ac[i] + bc[i]) % self.p for i in range(self.n)])

    def _sub_raw(self, a: int, b: int) -> int:
        ac = self.coeffs[a]
        bc = self.coeffs[b]
        return self._encode_raw([(ac[i] - bc[i]) % self.p for i in range(self.n)])

    def _mul_poly(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        ac = self.coeffs[a]
        bc = self.coeffs[b]
        tmp = [0] * (2 * self.n - 1)
        for i, av in enumerate(ac):
            if av:
                for j, bv in enumerate(bc):
                    if bv:
                        tmp[i + j] = (tmp[i + j] + av * bv) % self.p

        # x^n = -sum modulus[i] x^i.
        for deg in range(2 * self.n - 2, self.n - 1, -1):
            coeff = tmp[deg] % self.p
            if not coeff:
                continue
            tmp[deg] = 0
            offset = deg - self.n
            for i, mod_coeff in enumerate(self.modulus):
                tmp[offset + i] = (tmp[offset + i] - coeff * mod_coeff) % self.p
        return self._encode_raw(tmp[: self.n])

    def _find_primitive(self) -> int:
        order = self.q - 1
        primes = factor_int(order)
        for candidate in range(2, self.q):
            if all(self.pow_poly(candidate, order // prime) != 1 for prime in primes):
                return candidate
        raise RuntimeError(f"no primitive element found for GF({self.p}^{self.n})")

    def pow_poly(self, a: int, exponent: int) -> int:
        result = 1
        base = a
        while exponent:
            if exponent & 1:
                result = self._mul_poly(result, base)
            base = self._mul_poly(base, base)
            exponent >>= 1
        return result

    def elt(self, value: int) -> int:
        return value % self.p

    def add(self, a: int, b: int) -> int:
        return self._add_raw(a, b)

    def sub(self, a: int, b: int) -> int:
        return self._sub_raw(a, b)

    def neg(self, a: int) -> int:
        return self.neg_table[a]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp_table[(self.log_table[a] + self.log_table[b]) % (self.q - 1)]

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("field inverse of zero")
        return self.exp_table[(-self.log_table[a]) % (self.q - 1)]

    def div(self, a: int, b: int) -> int:
        return self.mul(a, self.inv(b))

    def pow(self, a: int, exponent: int) -> int:
        if exponent == 0:
            return 1
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] * exponent) % (self.q - 1)]

    def sq(self, a: int) -> int:
        return self.mul(a, a)

    def legendre(self, a: int) -> int:
        if a == 0:
            return 0
        return 1 if self.log_table[a] % 2 == 0 else -1

    def roots_square(self, a: int) -> list[int]:
        if a == 0:
            return [0]
        loga = self.log_table[a]
        if loga % 2:
            return []
        r = self.exp_table[(loga // 2) % (self.q - 1)]
        nr = self.neg(r)
        if nr == r:
            return [r]
        return [r, nr]

    def add_int(self, a: int, c: int) -> int:
        return self.add(a, self.elt(c))

    def sub_int(self, a: int, c: int) -> int:
        return self.sub(a, self.elt(c))

    def mul_int(self, a: int, c: int) -> int:
        return self.mul(a, self.elt(c))


def roots_x_plus_inv(field: GF, unext: int) -> list[int]:
    disc = field.sub(field.sq(unext), field.elt(4))
    roots = field.roots_square(disc)
    if not roots:
        return []
    inv2 = field.inv(field.elt(2))
    out = {
        field.mul(field.add(unext, root), inv2)
        for root in roots
    }
    return sorted(out)


def source_b_plus(field: GF, x: int) -> int | None:
    x2 = field.sq(x)
    den = field.sub_int(x2, 1)
    if den == 0:
        return None
    return field.div(field.mul_int(x2, 8), field.sq(den))


def count_field(field: GF) -> tuple[Counter, dict[int, Counter]]:
    F = field
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    eta = F.elt(1)

    for x in range(F.q):
        x2 = F.sq(x)
        x3 = F.mul(x2, x)
        x4 = F.sq(x2)
        x5_pow = F.mul(x4, x)
        x6_pow = F.mul(x5_pow, x)
        x8 = F.sq(x4)

        if x == 0 or x == F.elt(1) or x == F.neg(F.elt(1)) or F.add_int(x2, 1) == 0:
            stats["bad_X_denominator"] += 1
            continue

        bline = source_b_plus(F, x)
        if bline is None:
            stats["bad_Bline"] += 1
            continue

        a_den = F.mul(F.pow(F.sub_int(x, 1), 4), F.pow(F.add_int(x, 1), 4))
        if a_den == 0:
            stats["bad_A_den"] += 1
            continue
        poly = F.add(
            F.add(F.sub(x8, F.mul_int(x6_pow, 4)), F.sub(F.neg(F.mul_int(x4, 26)), F.mul_int(x2, 4))),
            F.elt(1),
        )
        a_num = F.neg(F.mul_int(poly, 2))
        a = F.div(a_num, a_den)

        t2 = F.mul(F.mul(x, F.add_int(x2, 1)), F.sub(F.add(x2, F.mul_int(x, 2)), F.elt(1)))
        for w in F.roots_square(F.sub(x3, x)):
            for t in F.roots_square(t2):
                u_den = F.mul(
                    F.mul(F.sub(t, F.mul_int(x2, 2)), F.sub_int(x, 1)),
                    F.pow(F.add_int(x, 1), 2),
                )
                if u_den == 0:
                    stats["bad_U_den"] += 1
                    continue

                mt = F.sub_int(
                    F.add(
                        F.add(F.mul_int(F.mul(w, x2), 2), F.mul_int(F.mul(w, x), 2)),
                        F.add(F.add(x4, F.mul_int(x3, 2)), F.neg(F.mul_int(x, 2))),
                    ),
                    1,
                )
                m0 = F.add(
                    F.add(
                        F.add(
                            F.add(F.mul(w, x5_pow), F.mul_int(F.mul(w, x4), 3)),
                            F.add(F.mul_int(F.mul(w, x3), 2), F.mul_int(F.mul(w, x2), 2)),
                        ),
                        F.add(F.sub(F.mul(w, x), w), F.mul_int(x6_pow, 2)),
                    ),
                    F.add(F.add(F.mul_int(x5_pow, 4), F.mul_int(x3, 4)), F.neg(F.mul_int(x2, 2))),
                )
                criterion_num = F.mul(F.mul(w, F.add_int(x2, 1)), F.add(m0, F.mul(mt, t)))
                r_roots = F.roots_square(F.div(criterion_num, x))
                if not r_roots:
                    stats["compactD_not_square"] += 1
                    continue

                u_core = F.add(
                    F.add(
                        F.add(F.mul_int(F.mul(F.mul(F.mul(eta, t), w), x), 4), F.mul(t, x3)),
                        F.add(F.mul(t, x2), F.neg(F.mul(t, x))),
                    ),
                    F.add(
                        F.add(F.neg(t), F.mul_int(x5_pow, 2)),
                        F.add(F.add(F.mul_int(x4, 2), F.neg(F.mul_int(x3, 2))), F.neg(F.mul_int(x2, 2))),
                    ),
                )
                u_num = F.mul_int(u_core, 2)
                beta_rhs = F.div(F.sub(F.sq(u_num), F.mul_int(F.sq(u_den), 4)), F.sq(u_den))
                beta_roots = F.roots_square(beta_rhs)
                if not beta_roots:
                    stats["first_half_beta_not_square"] += 1
                    continue

                for _r in r_roots:
                    stats["legal_R_points"] += 1
                    by_b[bline]["legal_R_points"] += 1
                    for beta in beta_roots:
                        stats["legal_chart_points"] += 1
                        by_b[bline]["legal_chart_points"] += 1
                        x5_num = F.add(u_num, F.mul(beta, u_den))
                        x5 = F.div(x5_num, F.mul_int(u_den, 2))
                        d_next = F.add(F.add(F.sq(x5), F.mul(a, x5)), F.elt(1))
                        sd_roots = F.roots_square(d_next)
                        if not sd_roots:
                            stats["reduced_U_no_root"] += 1
                            by_b[bline]["reduced_U_no_root"] += 1
                            continue
                        for sd in sd_roots:
                            unext = F.add(F.mul_int(x5, 2), F.mul_int(sd, 2))
                            stats["reduced_U_points"] += 1
                            by_b[bline]["reduced_U_points"] += 1
                            x6_roots = roots_x_plus_inv(F, unext)
                            stats[f"U_materialization_roots_{len(x6_roots)}"] += 1
                            by_b[bline][f"U_materialization_roots_{len(x6_roots)}"] += 1
                            selector = F.add_int(unext, 2)
                            selector_chi = F.legendre(selector)
                            stats[f"selector_chi_{selector_chi}"] += 1
                            by_b[bline][f"selector_chi_{selector_chi}"] += 1
                            gamma_roots = F.roots_square(selector)
                            stats["selector_gamma_points"] += len(gamma_roots)
                            by_b[bline]["selector_gamma_points"] += len(gamma_roots)
                            stats["materialized_x6_points"] += len(x6_roots)
                            by_b[bline]["materialized_x6_points"] += len(x6_roots)
                            if selector_chi == 1:
                                stats["materialized_x6_from_selector_plus_U"] += len(x6_roots)
                                by_b[bline]["materialized_x6_from_selector_plus_U"] += len(x6_roots)
                            elif selector_chi == -1:
                                stats["materialized_x6_from_selector_minus_U"] += len(x6_roots)
                                by_b[bline]["materialized_x6_from_selector_minus_U"] += len(x6_roots)
                            for x6 in x6_roots:
                                x6_chi = F.legendre(x6)
                                stats[f"x6_chi_{x6_chi}"] += 1
                                if x6_chi != selector_chi:
                                    stats["selector_x6_mismatch"] += 1

    for key in (
        "bad_A_den",
        "bad_Bline",
        "bad_U_den",
        "compactD_not_square",
        "first_half_beta_not_square",
        "reduced_U_no_root",
        "selector_x6_mismatch",
    ):
        stats.setdefault(key, 0)
    return stats, dict(by_b)


def ratio(stats: Counter, num: str, den: str) -> float:
    return stats[num] / stats[den] if stats[den] else 0.0


def summarize_fibers(by_b: dict[int, Counter]) -> Counter:
    out: Counter = Counter()
    for row in by_b.values():
        pair = (row["selector_chi_1"], row["selector_chi_-1"])
        out[f"selector_pm_fiber_pair_{pair}"] += 1
        lift_pair = (row["reduced_U_points"], row["materialized_x6_points"])
        out[f"U_x6_fiber_pair_{lift_pair}"] += 1
        gamma_pair = (row["reduced_U_points"], row["selector_gamma_points"])
        out[f"U_gamma_fiber_pair_{gamma_pair}"] += 1
    return out


def print_top(counter: Counter, prefix: str, limit: int) -> None:
    print(f"  {prefix}:")
    for key, value in counter.most_common(limit):
        print(f"    {key} = {value}")
    omitted = len(counter) - min(len(counter), limit)
    if omitted:
        print(f"    omitted_distinct_keys = {omitted}")


def run_field(p: int, n: int, fiber_limit: int) -> None:
    F = GF(p, n)
    stats, by_b = count_field(F)
    fiber_stats = summarize_fibers(by_b)
    stats["B_fibers"] = len(by_b)

    print(f"GF({p}^{n}) q={F.q}:")
    terms = " + ".join(f"{c}*x^{i}" for i, c in enumerate(F.modulus) if c)
    print(f"  modulus = x^{n}" + (f" + {terms}" if terms else ""))
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for num, den in [
        ("reduced_U_points", "legal_chart_points"),
        ("materialized_x6_points", "legal_chart_points"),
        ("materialized_x6_points", "reduced_U_points"),
        ("selector_gamma_points", "reduced_U_points"),
        ("selector_chi_1", "reduced_U_points"),
        ("selector_chi_-1", "reduced_U_points"),
    ]:
        print(f"  {num}_per_{den} = {ratio(stats, num, den):.9f}")
    print_top(fiber_stats, "fiber_summary_top", fiber_limit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="7,7^2,7^3,23,23^2")
    parser.add_argument("--fiber-limit", type=int, default=16)
    args = parser.parse_args()

    print("p27 B-line gamma extension-count probe")
    print("chart = eta_plus")
    print(f"fields = {args.fields}")
    print("question = does gamma^2=U_next+2 look sourceable over extensions?")
    for p, n in parse_field_specs(args.fields):
        run_field(p, n, args.fiber_limit)
    print("p27_b_line_gamma_extension_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
