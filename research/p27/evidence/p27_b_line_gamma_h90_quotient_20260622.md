# P27 B-Line Gamma H90 Quotient

Date: 2026-06-22

## Claim

The explicit Hilbert-90 quotient for the staged gamma class exists, but it
collapses to the already-imposed `f3` layer rather than exposing `f4`.

For the materialized two-root pair `v1,v2` over a fixed legal `(B,u)`, define:

```text
r = (v1 + 2)/(v2 + 2)
h^2 = r
```

The involution swaps `h <-> 1/h`.  In q1607/q1847/q2087, the quotient obeys:

```text
r + 1/r = u
(h + 1/h)^2 = u + 2
tau = (h - 1)/(h + 1)
tau^2 + tau^-2 = 2*(u + 6)/(u - 2)
```

with zero identity failures.  Thus the H90 quotient is a restatement of the
first reduced `f3` square-root layer `u+2`, not the missing `f4` source law.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_gamma_h90_quotient_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_h90_quotient_probe_20260622.txt
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_h90_quotient_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  --degrees 2,4,6,8,10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_h90_quotient_probe_20260622.txt
```

## Identity Results

The ratio was always a square:

```text
q1607: h90_ratio_square_fail = 0
q1847: h90_ratio_square_fail = 0
q2087: h90_ratio_square_fail = 0
```

The quotient identities all held:

```text
q1607:
  rsym_minus_u_identity_fail = 0
  hsym2_minus_uplus2_identity_fail = 0
  tau_sym_formula_fail = 0

q1847:
  rsym_minus_u_identity_fail = 0
  hsym2_minus_uplus2_identity_fail = 0
  tau_sym_formula_fail = 0

q2087:
  rsym_minus_u_identity_fail = 0
  hsym2_minus_uplus2_identity_fail = 0
  tau_sym_formula_fail = 0
```

This explains the low-rank `(u, r+1/r)`, `(u, (h+1/h)^2)`, and
`(u, tau^2+tau^-2)` relation screens: they are tautological consequences of
the first reduced cover, not new B-line structure.

## Predictor Screen

The probe also tested low-weight products of visible H90 quotient atoms
including:

```text
r, r+1/r,
h, h+1/h, (h+1/h)^2,
tau, tau^2, tau^2+tau^-2,
B, A, u, v-pair sum/product, gamma norm,
small shifts of these quantities.
```

No exact product through weight `4` predicts `f4`:

```text
q1607: h90_exact_products = 0, best = 77/112 = 0.688
q1847: h90_exact_products = 0, best = 122/180 = 0.678
q2087: h90_exact_products = 0, best = 75/100 = 0.750
```

The best products are not stable across fields.

## Relation Screen

The B-line relation screens remain negative for the quotient invariants:

```text
(B, r+1/r):        extra_nullity = 0 through degree 10
(B, (h+1/h)^2):    extra_nullity = 0 through degree 10
(B, tau^2+tau^-2): extra_nullity = 0 through degree 10
```

The low-degree relations involving `u` are exactly the identities above.
They do not couple `f4` to B or provide a sampler.

## Interpretation

Positive:

```text
The H90 quotient is explicit and checked.
It identifies the materialized gamma-pair quotient with the first reduced f3
square-root layer.
```

Negative:

```text
The H90 quotient itself does not predict f4.
No visible quotient-coordinate product through weight 4 predicts f4.
No low-degree B-relation appears for the quotient invariants through degree 10.
```

The live object is therefore narrower:

```text
gamma^2 = v + 2 as a new class over the already-known H90/f3 layer.
```

A sqrt-beating result now needs `gamma` to be a pullback, coboundary, iterate,
recurrence, or low-genus/sourceable quotient over that layer.  The basic H90
quotient is not enough.

Follow-up:
[P27 B-Line Gamma Over F3/H90 Layer Relation Screen](p27_b_line_gamma_f3_layer_relation_20260622.md)
doubles the rows by `H -> +/-H` and tests whether `gamma` becomes visible on
the explicit `H^2=u+2` layer.  Stable pair-coordinate screens in `(B,H)`,
`(B,tau)`, `(B,H^2)`, and `(B,tau^2+tau^-2)` remain negative; the triple
relations are the known layer equations.

## Continue / Kill

```text
continue = compute/divide the gamma divisor class over the h + 1/h f3 layer
continue = ask whether gamma recurs/telescopes at f5 after the same construction
continue = offline CAS on gamma over the normalized f3/H90 layer

kill = treating the explicit H90 quotient as a new source law
kill = visible H90 quotient-coordinate products through weight 4
kill = low-degree B-plane relations for r+1/r, (h+1/h)^2, or tau^2+tau^-2 through degree 10
kill = visible f3/H90-layer pair-coordinate relations as gamma source laws
```

```text
p27_b_line_gamma_h90_quotient_rows=1/1
```
