# P27 B-Line Gamma Norm/Coboundary Boundary

Date: 2026-06-22

## Claim

The staged `f4/f3` class

```text
gamma^2 = v + 2
```

is norm-trivial in the expected sense, but the tested visible pair invariants
do not predict the remaining `f4` squareclass.

On the generic four-root transition

```text
F_A(u,v) = (v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A) + 16*(v + A)^2,
```

the full norm is the tautological square:

```text
Norm_4(v + 2) = F_A(u,-2) = 16*(A - 2)^2.
```

On the actual materialized two-root half and on the discarded two-root half,
the gamma norm is also always square in q1607/q1847/q2087.  However, the
naive stronger formula

```text
Norm_2(v + 2) / (4*(2-A)) = one of the parent x6 roots
```

is false in every row.  The quotient is square, but it is not the parent
`x6` root.

So the norm data supports a Hilbert-90/coboundary framing, but not a visible
source formula.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_gamma_norm_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_norm_probe_20260622.txt
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_norm_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_norm_probe_20260622.txt
```

## Norm Results

The generic four-root norm formula held with zero failures:

```text
q1607: generic_gamma_norm_formula_bad = 0
q1847: generic_gamma_norm_formula_bad = 0
q2087: generic_gamma_norm_formula_bad = 0
```

The actual and missing materialized two-root gamma norms were always squares:

```text
q1607: actual_or_missing_gamma_norm_nonsquare = 0
q1847: actual_or_missing_gamma_norm_nonsquare = 0
q2087: actual_or_missing_gamma_norm_nonsquare = 0
```

After dividing by `4*(2-A)`, the resulting scale was also always square:

```text
q1607: actual_or_missing_scale_nonsquare = 0
q1847: actual_or_missing_scale_nonsquare = 0
q2087: actual_or_missing_scale_nonsquare = 0
```

But that scale was never one of the parent `x6` roots:

```text
q1607: actual_or_missing_scale_not_xroot = 224
q1847: actual_or_missing_scale_not_xroot = 360
q2087: actual_or_missing_scale_not_xroot = 200
```

The row counts were:

```text
q1607: norm_rows = 112, f4 plus/minus = 76/36
q1847: norm_rows = 180, f4 plus/minus = 76/104
q2087: norm_rows = 100, f4 plus/minus = 72/28
```

## Pair-Invariant Screen

The probe also tested low-weight products of natural pair invariants, including:

```text
B, A, u,
sum/product/discriminant of the actual v-pair,
sum/product of the missing v-pair,
actual/missing/full gamma norms,
actual/missing norm scales,
small shifts of these quantities.
```

No exact product through weight `4` predicts `f4`:

```text
q1607: pair_exact_products = 0, best = 84/112 = 0.750
q1847: pair_exact_products = 0, best = 132/180 = 0.733
q2087: pair_exact_products = 0, best = 80/100 = 0.800
```

The best products are not stable across fields; they are treated as
field/tail fits, not a source law.

## Interpretation

Positive:

```text
The norm of gamma over the transition is square at the generic four-root level
and at the materialized two-root level.

This is exactly the shape where a Hilbert-90 quotient/coboundary computation
could matter.
```

Negative:

```text
The naive parent-x6 norm formula is false.
No visible pair invariant through the screened atom/product family predicts f4.
This does not produce a GPU bucket or direct sampler.
```

## Continue / Kill

```text
continue = compute an explicit H90 quotient for gamma on the staged cover
continue = ask whether that quotient telescopes or recurs in the next gate
continue = offline CAS on F_A(u,v), rho^2=v^2-4, gamma^2=v+2

kill = naive Norm_2(v+2)=4*x6*(2-A) as the missing formula
kill = visible pair-invariant products through weight 4 as f4 predictors
kill = GPU production from gamma norm-triviality alone
```

```text
p27_b_line_gamma_norm_coboundary_rows=1/1
```
