# Centered Marginal Origin-Norm Power Theorem

Date: 2026-06-06

This note records the centered-marginal version of the origin-norm power
bridge.

The reduced centered target is the right-window product

```text
Pi_C,right = prod_{t mod d} F(t),
```

where for p24:

```text
d = 211,
F(t) = Delta_C(t),
m = 66254 = 2 * 157 * 211,
n = 3107441,
h = m*n.
```

The full origin action writes an origin shift as

```text
shift = n*alpha + m*beta mod h.
```

## Power Theorem

For the centered Hermitian marginal, the beta direction cancels exactly:

```text
Delta_origin(alpha,beta) = Delta_origin(alpha,0).
```

The alpha direction splits into a left translation determinant and the right
cyclic window:

```text
Delta_origin(alpha,0)
  = epsilon_left(alpha) * F(alpha mod d),
```

where

```text
epsilon_left(alpha) = det(translation by alpha on the zero-sum hyperplane).
```

For a left cyclic component of size `c`,

```text
epsilon_c(alpha) = (-1)^(c - gcd(c,alpha)).
```

After this p-unit sign normalization,

```text
prod_{alpha mod m} Delta_origin(alpha,beta)
  = p-unit * Pi_C,right^(m/d),
```

and

```text
prod_{all origins} Delta_origin
  = p-unit * Pi_C,right^(n*m/d).
```

For p24, `c=157` is odd prime.  Hence `epsilon_157(alpha)=1` for every
`alpha`, so the displayed p-unit sign is actually trivial in the selected
mixed block.  The exponents are:

```text
m/d = 66254/211 = 314,
n*m/d = 3107441 * 314 = 975736474.
```

Thus a closed p-unit formula for the full-origin centered Chow product would
prove `Pi_C,right != 0`, and therefore every one of the 211 centered cyclic
right windows is nonzero.

## Proof Skeleton

Let

```text
pi_d : Z/mZ -> Z/dZ
Pi_C,right = prod_{t mod d} F(t).
```

Assume the centered origin covariance identity:

```text
Delta_origin(alpha,beta)
  = u(alpha,beta) * F(pi_d(alpha)),
```

with `u(alpha,beta)` a p-unit and with p-unit fiber products.  Since `d | m`,
each residue `t mod d` has exactly `m/d` lifts to `Z/mZ`.  Therefore

```text
prod_{alpha mod m} F(pi_d(alpha))
  = prod_{t mod d} F(t)^(m/d)
  = Pi_C,right^(m/d).
```

Multiplying over the `n` beta fibers gives the full-origin exponent
`n*m/d`.  In a field, and with p-unit normalizing factors, the larger
origin products are nonzero if and only if the reduced right product is
nonzero.

## Small Actual-CM Audit

The executable audit is:

```text
p24/centered_marginal_origin_norm_power_audit.py
```

Pinned rows:

```text
D=-6719, q=6863, h=105, m=21, n=5, pair=(3,7):
  right=7
  m/right=3
  n*m/right=15
  beta_mismatch_count=0
  left_sign_product=1
  right_product=2424
  normalized_alpha_product=1042
  normalized_alpha_power_match=1
  raw_alpha_power_match=1
  normalized_full_origin_power_match=1
  raw_full_origin_power_match=1

D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7):
  right=7
  m/right=4
  n*m/right=20
  beta_mismatch_count=0
  left_sign_product=1
  right_product=7674
  normalized_alpha_product=3636
  normalized_alpha_power_match=1
  raw_alpha_power_match=1
  normalized_full_origin_power_match=1
  raw_full_origin_power_match=1

D=-10919, q=11243, h=156, m=39, n=4, pair=(3,13):
  right=13
  m/right=3
  n*m/right=12
  beta_mismatch_count=0
  left_sign_product=1
  right_product=6266
  normalized_alpha_product=1282
  normalized_alpha_power_match=1
  raw_alpha_power_match=1
  normalized_full_origin_power_match=1
  raw_full_origin_power_match=1
```

These rows test both right factor `7` and right factor `13`, including
different factor degrees and left sizes.  The result supports the conclusion
that the larger full-origin norm introduces no new phase selector once the
centered covariance identity is fixed.

## Consequence For The Certificate Search

This theorem does not by itself produce the p24 certificate.  It is a
producer-side bridge:

```text
closed full-origin p-unit theorem
  => Pi_C,right is a p-unit
  => rank_Fp C_{157,211} = 156
  => selected centered profile certificate succeeds.
```

The remaining theorem is arithmetic, not finite:

```text
construct a p-integral phase-aware Borcherds/Fitting/class-field section
Psi_C,full whose selected CM value equals the full-origin centered Chow
product up to p-units, and prove v_p(Psi_C,full)=0 at p=10^24+7.
```

The finite implication from such a full-origin p-unit theorem is recorded in:

```text
p24/lean/CenteredFullOriginBorcherdsGate.lean
p24/centered_marginal_full_origin_borcherds_gate.md
```
