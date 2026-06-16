# Lang Trace-GCD Origin-Action Boundary

Date: 2026-06-05

This note packages the representative trace-gcd determinant under a change of
CM cycle origin.

## Origin Coordinates

For `h=m*n`, write an origin shift as:

```text
shift == n*alpha + m*beta mod h.
```

The quotient fibers transform as:

```text
F'_r(X) = X^(-beta) F_{r+alpha}(X).
```

The trace-gcd determinant is attached to:

```text
K_alpha,beta = common kernel of the selected prefix trace blocks,
Delta_i(alpha,beta) = det(tail_i on K_alpha,beta),
```

where `i` is the omitted right block.  Nonvanishing of this determinant is
equivalent to:

```text
gcd_p-lin(P_K, tail_i) = X.
```

## Audit

Added:

```text
p24/lang_trace_gcd_origin_action_audit.py
```

Pinned actual-CM row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_origin_action_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail
```

reported:

```text
D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7)
records=280
det_zero_count=0
det_distinct_count=14
gcd_failure_count=0
```

For each omitted block separately:

```text
omitted=0:
  zeros=0, distinct=7, product_all_mod_q=3871
  alpha_fixed_product_distinct=7, period=7
  beta_fixed_product_distinct=1, period=1
  alpha_value_period=7, beta_value_period=1

omitted=1:
  zeros=0, distinct=7, product_all_mod_q=4697
  alpha_fixed_product_distinct=7, period=7
  beta_fixed_product_distinct=1, period=1
  alpha_value_period=7, beta_value_period=1
```

Thus, in this actual-CM row:

```text
Delta_i(alpha,beta) is independent of beta,
Delta_i(alpha,beta) has alpha-period 7.
```

This matches the Hermitian origin-action heuristic: multiplication by the
common packet monomial `X^(-beta)` cancels inside the relative trace pairing,
while the quotient-axis translation `alpha` moves the selected right window.

The exact finite algebra behind this heuristic is recorded in:

```text
p24/lang_origin_covariance_theorem.md
p24/lang_origin_covariance_toy.py
```

At the trace-map level:

```text
T_j^(alpha,beta) = V_{j,t} o T_j o U_alpha,   t=alpha mod right,
```

with `U_alpha` and `V_{j,t}` invertible.  Hence the prefix kernel transports
as:

```text
K_(alpha,beta)=U_alpha^(-1)K_0,
```

and the transported tail determinant depends only on the right component
`t`, up to a nonzero determinant unit.

## Product Target

The audit suggests the stronger origin-stable package:

```text
Pi_i = prod_t Delta_i(t,0),
```

where `t` runs over the reduced right-component alpha cycle.  In the toy row,
the reduced cycle has length `7`, not `m=28` and not `h=140`.

For p24:

```text
m = 66254 = 2*157*211.
```

The analogous reduced target is expected to be the `211`-term product:

```text
Pi_trace,i = prod_{t mod 211} Delta_i(t,0).
```

A proof of:

```text
Pi_trace,i != 0 mod p
```

would prove every reduced alpha translate is nonsingular, hence the selected
representative determinant is nonzero.  Together with the right-unit
equivariance theorem, this would propagate to the full six-orbit
representative certificate.

Equivalently, if `f_i(Y)` interpolates the right-translation determinant
sequence, then:

```text
Pi_trace,i = Res_Y(Y^211 - 1, f_i(Y)).
```

Since `ord_211(p)=35`, the nonzero right translations split into six
Frobenius orbits of length `35`, plus the fixed `0` translation.  The product
therefore has a seven-factor orbit-product form over `F_p`.

## Missing Theorem

The missing theorem is not just generic nonvanishing.  It should prove the
following arithmetic identity for the embedded CM trace blocks:

```text
Delta_i(alpha,beta)
  = u_i(alpha,beta) * F_i(alpha mod 211),
```

with `u_i(alpha,beta)` a p-unit coming from the left/beta basis action, and:

```text
prod_{t mod 211} F_i(t) != 0 mod p.
```

This would replace class-set enumeration by a fixed-size cyclic resultant in
the right component.  The audit gives small actual-CM evidence for the
invariance and period statement, but the p24 proof still needs a class-field
divisor/norm identity for this determinant sequence.
