# Lang Trace-GCD Origin-Norm Power Theorem

Date: 2026-06-05

This note records a producer-side clarification for the trace-GCD route.

The reduced theorem target is the right product

```text
Pi_right = prod_{t mod 211} Delta(t),
Delta(t)=det(P V_t A).
```

The full origin action has more coordinates.  Write

```text
h = m*n,
shift = n*alpha + m*beta mod h,
right = d | m.
```

For p24:

```text
m = 2 * 157 * 211,
n = 3107441,
d = 211.
```

## Conditional Power Theorem

After p-integral trace-coordinate choices, origin covariance has the form

```text
Delta_origin(alpha,beta)
  = u(alpha,beta) * F(alpha mod d),
```

with `u(alpha,beta)` a p-unit and with p-unit product over every irrelevant
fiber.  Consequently

```text
prod_{alpha mod m : fixed beta} Delta_origin(alpha,beta)
  = unit(beta) * Pi_right^(m/d),
```

and

```text
prod_{all origins} Delta_origin
  = unit * Pi_right^(n*m/d).
```

Because the ambient residue field is a field, nonvanishing of either larger
norm is equivalent to nonvanishing of `Pi_right`, provided the unit factors
are known p-units.

For p24 the exponents are:

```text
m/d = 2 * 157 = 314,
n*m/d = 3107441 * 314 = 975736474.
```

This is not a new finite payload.  It is a bridge: a full-origin
Borcherds/class-field norm formula would imply the 211-term right product if
the formula can be proved without enumerating the class set.

## Proof Under Covariance

Let:

```text
pi_d: Z/mZ -> Z/dZ
F(t) = reduced right determinant
Pi_right = prod_{t mod d} F(t).
```

Assume:

```text
Delta_origin(alpha,beta)
  = u(alpha,beta) * F(pi_d(alpha)),
```

and assume the unit factors have fiber products:

```text
U_beta = prod_{alpha mod m} u(alpha,beta)       is a p-unit,
U_all  = prod_{alpha,beta} u(alpha,beta)        is a p-unit.
```

Then, for fixed `beta`,

```text
prod_{alpha mod m} Delta_origin(alpha,beta)
  = U_beta * prod_{alpha mod m} F(pi_d(alpha)).
```

Because `d | m`, every residue `t mod d` has exactly `m/d` lifts
`alpha mod m`, so:

```text
prod_{alpha mod m} F(pi_d(alpha))
  = prod_{t mod d} F(t)^(m/d)
  = Pi_right^(m/d).
```

Multiplying over all `beta mod n` gives:

```text
prod_{alpha,beta} Delta_origin(alpha,beta)
  = U_all * Pi_right^(n*m/d).
```

Since the residue algebra is a field and `U_beta`, `U_all` are p-units, each
larger norm is nonzero if and only if `Pi_right` is nonzero.  The only
arithmetic input in this proof is the covariance identity and p-unitness of
the unit-factor products.

## Small Actual-CM Audit

Added:

```text
p24/lang_trace_gcd_origin_norm_power_audit.py
```

Pinned row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_origin_norm_power_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

Output:

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7
m/right=4
n*m/right=20

omitted=0:
  pi_right=6352
  pi_right^4=1718
  beta_products all equal 1718
  pi_right^20=3871
  all_origin_product=3871

omitted=1:
  pi_right=6639
  pi_right^4=5193
  beta_products all equal 5193
  pi_right^20=4697
  all_origin_product=4697
```

This matches the earlier origin-action audit:

```text
p24/lang_trace_gcd_origin_action_boundary.md
```

## Consequence for the Missing Theorem

The operator-norm target remains the small, honest finite object:

```text
Pi_right = Norm_{F[Y]/(Y^211-1)/F}(f_trace).
```

A larger full-origin norm is useful only if it has an independent closed
formula, for example a Borcherds/local-intersection product formula for the
same determinant section.  If such a formula exists, the power theorem
removes the remaining origin phase: proving the full-origin norm p-unit
proves the 211-term right norm p-unit.

The current boundary is therefore:

```text
find a modular/class-field product formula for the trace-GCD determinant
section, or construct f_trace directly in the degree-211 cyclic algebra.
```

The power relation is not itself the final certificate.  It only says that
lifting from the right norm to a full-origin norm does not introduce a new
selector problem; it introduces the need for a closed norm formula.

The finite implication is Lean-checked in:

```text
p24/lean/OriginNormPowerGate.lean
```
