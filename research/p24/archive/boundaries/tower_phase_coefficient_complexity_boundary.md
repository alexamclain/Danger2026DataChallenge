# Tower Phase Coefficient Complexity Boundary

Date: 2026-06-05

This note records a new small-data test for the embedded class-field tower
route.  It does not finish the p24 certificate, but it rules out one tempting
compression theorem for the odd non-genus phase.

## Target Analogy

The third p24 trace has

```text
h = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
```

The formal quotient tower is:

```text
degree 2 genus split
degree 157 non-genus refinement
degree 211 non-genus refinement
degree 3107441 recovery
```

The positive route still allows quotient-scale objects.  What would be even
better is a formula saying that each relative child polynomial has
low-complexity coefficients as a function of the parent period.

For a small cyclic CM cycle with

```text
h = a * b * r,
```

let `r` be the recovery subgroup size, let `a*b` be the fine quotient size,
and group the fine periods into `a` parent periods.  Above parent `Z_u`, the
relative child polynomial is

```text
C_u(Y) = prod_{v=0}^{b-1} (Y - y_{u+a*v}).
```

The coefficient of `Y^(b-1)` is forced:

```text
coeff_{b-1}(C_u) = -sum_v y_{u+a*v} = -Z_u.
```

So the only informative question is whether the lower coefficients

```text
coeff_0, ..., coeff_{b-2}
```

are low-degree functions of `Z_u`, or have low linear complexity in the
ordered parent cycle.

For p24's second odd step, the direct generic table has size

```text
a * (b-1) = 314 * 210 = 65940
```

which is still quotient-scale and below `sqrt(p)`.  A collapse below this
would be useful, but it is not required by the formal asymptotic split.

## New Scan

I added:

```text
p24/tower_phase_coefficient_complexity_scan.py
```

Small pinned run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_phase_coefficient_complexity_scan.py \
  --max-cases 8 --min-h 12 --max-h 90 --max-abs-D 12000 \
  --q-stop 150000 --min-quotient 6 --max-quotient 60 \
  --min-parent 3 --max-parent 20 --max-child 2 --max-child 11 \
  --min-recovery 2 --max-rows-per-case 8 --summary-only
```

Output:

```text
rows=12
good_distinct_rows=12
coeff_slots=29
full_degree_coeffs=17
informative_coeff_slots=17
informative_full_degree_coeffs=17
informative_low_degree_coeffs=0
low_degree_coeffs=12
low_bm_coeffs=0
```

The `12` low-degree coefficients are exactly the forced `-Z_u` coefficient.
After removing that tautology, every informative coefficient in the sample has
full interpolation degree.

Modestly broader seconds-scale run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_phase_coefficient_complexity_scan.py \
  --max-cases 20 --min-h 12 --max-h 140 --max-abs-D 25000 \
  --q-stop 350000 --min-quotient 6 --max-quotient 100 \
  --min-parent 3 --max-parent 36 --max-child 13 \
  --min-recovery 2 --max-rows-per-case 12 --summary-only
```

Output:

```text
rows=30
good_distinct_rows=29
coeff_slots=70
full_degree_coeffs=41
informative_coeff_slots=41
informative_full_degree_coeffs=41
informative_low_degree_coeffs=0
low_degree_coeffs=29
low_bm_coeffs=0
```

Again, all informative coefficient functions have full interpolation degree.

## Guardrail Experiments

I also reran the sidecar-recommended small checks.

Abstract non-genus quotient pairing:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_pairing_non_genus_toy.py
```

Key output:

```text
D=-2239
q=2243
quotient_size=5
abstract_roots=[709, 834, 913, 987, 1043]
embedded_period_sums=[9, 106, 587, 812, 1142]
affine_set_maps_found=0
mobius_set_maps_found=0
```

So even when both the abstract quotient and embedded period quotient split,
the root sets are not paired by a simple affine or Mobius transform.

Low-degree plain-`j` selector:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/embedded_selector_identity_toy.py
```

Key output:

```text
D=-5000
h=30
generic_rational_interpolation_threshold=15
first_selector_degree=15
first_degree_equals_generic_threshold=1
```

So the embedded subgroup quotient exists, but the plain `j` coordinate does
not expose it below generic interpolation degree.

Projector support stress:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/quotient_spectrum_support_toy.py --max-h 18 --max-q 100
```

Key output:

```text
rows=283
nonquotient_reduced_rows=0
quotient_reduced_rows=0
```

This supports the existing additive support boundary.

## Upstream DANGER3 Data Boundary

The local `p24/upstream_DANGER3/` corpus and the sibling
`danger3-short-certificate-experiments/external/DANGER3/` corpus are
Montgomery verifier triples or successful `(p,A)` prefixes.  The official
upstream repository is:

```text
https://github.com/AndrewVSutherland/DANGER3
```

Its README lists the same local resources plus larger linked one-witness
archives `pp28`, `pp30`, and `pp32`.  Those datasets are useful for
verifier-visible statistics and branch filters, but they do not contain:

```text
embedded CM j-cycles,
relative class-character traces,
period quotient roots paired to j-recovery factors.
```

Thus they cannot directly test the p24 non-genus tower theorem.  Existing
audits in

```text
p24/upstream_dataset_experiment_audit.md
p24/upstream_large_one_witness_audit.md
p24/upstream_near_square_dataset_boundary.md
```

show only constant-factor branch signals, especially in the near-square
`p=n^2+7` family.  They do not reveal a growing selector.

## Consequence

The theorem candidate

```text
relative child-polynomial coefficients have a small low-degree formula in the
parent period
```

is now disfavored by small CM data.  The only low-degree coefficient is the
forced trace coefficient `-Z`.

The surviving positive theorem is narrower:

```text
construct the embedded non-genus relative class-character traces, or
equivalently the quotient-scale relative child-polynomial tables, for the
157 and 211 tower layers without enumerating the full h-class orbit.
```

This is still compatible with the desired asymptotic speedup because the
largest formal degree remains

```text
max(66254, 3107441) << sqrt(p).
```

But the producer cannot be a tiny parent-period interpolation identity.  It
has to be a genuine embedded class-field/tower formula, a p-unit norm
certificate, or an equivalent finite-field split-cycle identity.
