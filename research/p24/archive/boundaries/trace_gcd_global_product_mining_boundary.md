# Trace-GCD Global Product Mining Boundary

Date: 2026-06-06

This note records the first small actual-CM test of the global Chow/Borcherds
product target.

## Question

The global handoff replaces seven orbit products by one scalar:

```text
Pi_all = product_{t mod right} Delta(t).
```

For a Borcherds/local-intersection proof this is attractive, but it creates a
recognition hazard: matching one element of `F_q^*` is far easier than matching
the actual Chow divisor.

The falsifier is:

```text
p24/trace_gcd_global_product_miner.py
```

It uses the pinned actual-CM row:

```text
D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7).
```

For each omitted target it compares:

```text
phase vector:
  (log Delta(t))_{t mod 7}

global scalar:
  sum_t log Delta(t) = log Pi_all.
```

against the bounded phase-unit dictionary from
`trace_gcd_chow_phase_divisor_span_scan.py`, plus small constant units.

## Run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_global_product_miner.py \
  --max-formula-features 32 \
  --max-combo-terms 3 \
  --exponent-bound 3 \
  --match-limit 8
```

reported:

```text
unit_dictionary_size=160
distinct_global_products=152
right_binomial_global_formula_mismatches=0
```

The right-binomial global products satisfy the expected identity:

```text
product_t Norm(1 - c*zeta^(k*t))
  = (1 - c^right)^ord_q(right).
```

So their global products collapse to ordinary small cyclotomic units, even
though their phase vectors are nonconstant.

## Results

For omitted `0`:

```text
right_values=[2125, 6973, 11434, 2597, 12105, 2133, 3022]
Pi_all=6352
low_weight_scalar_matches: found
low_weight_vector_matches: none
```

For omitted `1`:

```text
right_values=[11423, 4693, 4157, 13397, 8480, 3228, 8474]
Pi_all=6639
low_weight_scalar_matches: found
low_weight_vector_matches: none
```

The linear-span diagnostic says the same thing:

```text
mod 2:
  scalar_dictionary_rank=1/1, scalar_target_in_span=1
  vector_dictionary_rank=3/7, vector_target_in_span=0

mod 53 and mod 127:
  scalar rank is full for the one-dimensional scalar problem;
  vector rank is 7/7, so containment is just interpolation.
```

## Interpretation

The global scalar is too easy to fit in small finite fields.  Low-weight
scalar formulas appeared for both omitted targets, but none lifted to the
phase vector, and the mod-`2` phase-vector obstruction from the earlier
unit-span scan remains.

Therefore a useful global `Psi_all` theorem must be divisor/local-intersection
honest:

```text
div(Psi_all) = pulled-back full Chow divisor + harmless boundary/vertical terms
```

or equivalently it must compare to the actual trace-GCD Fitting/Chow section
up to a p-unit.  Merely recognizing the isolated value `Pi_all` as a product
of simple units is not evidence of a certificate.

This does not kill the global Borcherds route.  It sharpens it: the proof
must construct the global divisor, not just the global scalar.
