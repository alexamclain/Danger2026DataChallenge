# Centered Marginal Global-Product Mining Boundary

Date: 2026-06-06

This note tests a scalar variant of the cyclic-resultant route.

## Question

The orbit-product target asks for seven factors:

```text
Pi_O = prod_{t in O} Delta_C(t).
```

A global Borcherds product might instead construct one scalar:

```text
Pi_C,right = prod_{t mod right} Delta_C(t).
```

If this scalar had a tiny elementary right-phase product formula, it could be
a smaller proof surface than seven separate orbit products.  However,
scalar-only matches are dangerous: they can occur by accidental discrete-log
coincidence without giving a divisor identity or orbit-wise zero detection.

## Audit

Added:

```text
p24/centered_marginal_global_product_miner.py
```

The miner:

```text
1. computes the centered determinant sequence in small actual-CM rows;
2. excludes constants by default, since gcd(right,q-1)=1 makes constants
   scalar-log-trivial in the pinned rows;
3. searches low-weight products of elementary right-binomial norm units;
4. reports both scalar matches and full vector matches.
```

## Results

Bounded search:

```text
max_binomial_constant=20,
max_combo_terms=2,
exponent_bound=4.
```

Rows:

```text
D=-6719, q=6863, pair=(3,7):
  scalar_match_count=5,
  vector_match_count=0.

D=-13319, q=13463, pair=(4,7):
  scalar_match_count=0,
  vector_match_count=0.

D=-10919, q=11243, pair=(3,13):
  scalar_match_count=0,
  vector_match_count=0.
```

The first row has scalar coincidences, but they do not lift to the phase
vector.  The next two rows have no low-weight scalar match in the same
dictionary.

## Consequence

This demotes the elementary global-product explanation:

```text
Pi_C,right is not consistently recognized as a tiny product of elementary
right-binomial norm units in the first actual-CM rows.
```

A scalar global product may still be viable if it is produced by an honest
divisor/local-intersection theorem.  But scalar discrete-log coincidences are
not enough; the proof must compare divisors or Fitting sections, not merely
match one value in `F_q^*`.

This reinforces the target in:

```text
p24/centered_marginal_phase_borcherds_target.md
```

The missing `Psi` must be a genuine centered Schubert/Fitting object, not an
ad hoc low-weight unit product.
