# Tensor Factor Marginal Origin Product

This note records the origin-action test for the new marginal exterior
products.

## Origin Action

For `h=m*n` and an origin shift `s`, write:

```text
s == n*alpha + m*beta mod h.
```

The quotient fibers transform as:

```text
J'_r(theta) = theta^(-beta) J_{r+alpha}(theta).
```

The `alpha` part translates CRT residue classes.  On marginal-difference
bases `M_a-M_0`, this is a unimodular change of basis in the relevant root
lattice.  Thus a chosen exterior coordinate can change by a unit, but its
zero/nonzero status is unchanged by pure `alpha`.

The `beta` part is different.  It multiplies in the tensor factor before
applying the top-coefficient map:

```text
x |-> Top_k(theta^(-beta) x).
```

Since `Top_k` is not an invertible map on `B` for the p24 windows, beta can
move a chosen Plucker coordinate through genuinely different values.

## Product Packaging

For one chosen Plucker coordinate `P` of one marginal exterior vector
`Omega`, define:

```text
Pi_{P,Omega} = prod_{beta mod n} P(Omega_beta),
```

where `Omega_beta` is formed after the beta-shifted multiplication
`theta^(-beta)`.

Changing the embedded origin's beta coordinate permutes the factors.  Changing
alpha changes the marginal bases by unimodular matrices.  Therefore the
zero/nonzero status of `Pi_{P,Omega}` is origin-stable.

This is the marginal analogue of the older sliding-window product for leading
axis coordinate minors.  It is stronger than the selected-origin theorem:
`Pi_{P,Omega} != 0` proves that this same Plucker coordinate works for every
beta shift, while the actual certificate only needs nonzero exterior vector
for the selected origin.

## Audit

The audit script is:

```text
p24/tensor_factor_marginal_origin_action_audit.py
```

Pinned full-axis square toy:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_marginal_origin_action_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 2 --target full
```

reported:

```text
all_shifts count=156 distinct=2 zeros=0
pure_alpha_beta0 count=12 distinct=2 zeros=0
pure_beta_alpha0 count=13 distinct=1 zeros=0
alpha_beta_products count=12 distinct=2 zeros=0
```

For the one-window `4`-component marginal determinant:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_marginal_origin_action_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1 \
  --target 4 --without-constant
```

reported:

```text
all_shifts count=156 distinct=26 zeros=0
pure_alpha_beta0 count=12 distinct=2 zeros=0
pure_beta_alpha0 count=13 distinct=13 zeros=0
alpha_beta_products count=12 distinct=2 zeros=0
```

For the one-window `constant+3` determinant:

```text
all_shifts count=156 distinct=13 zeros=0
pure_alpha_beta0 count=12 distinct=1 zeros=0
pure_beta_alpha0 count=13 distinct=13 zeros=0
alpha_beta_products count=12 distinct=1 zeros=0
```

This confirms the expected pattern: alpha is a basis-unit effect, beta is a
real top-coefficient coordinate motion, and the beta product packages an
origin-stable p-unit target.

The beta-sequence complexity audit is:

```text
p24/tensor_factor_marginal_beta_complexity.py
p24/tensor_factor_marginal_beta_complexity.md
p24/tensor_factor_beta_recurrence_audit.py
p24/tensor_factor_beta_recurrence_resultant.md
```

It found that the full two-window toy determinant is beta-constant only
because the coordinate target equals the entire tensor factor.  The projected
one-window component determinants have all `13` beta values, no Frobenius
descent, and Berlekamp-Massey complexity `7`.

The recurrence audit sharpens this: the projected determinant has a degree-7
characteristic polynomial dividing `T^13-1`, and this recurrence regenerates
the doubled beta sequence with zero failures.  So the product can be expressed
as a norm/resultant over the spectral-support factor.  This is useful only
when the support factor degree is asymptotically small.

For p24, the companion support audit:

```text
p24/tensor_factor_beta_support_audit.py
p24/tensor_factor_beta_support_boundary.md
```

shows that the tensor-factor orbit `O=<p^5460>` has `O+O+O=Z/nZ`.  Thus
large exterior coordinates have full beta-character support available; the
origin-stable product is not low-order merely by representation support.

## Consequence

The p24 marginal theorem now has two nested deterministic surfaces:

```text
weaker/intrinsic:
  Omega_1, Omega_211, Omega_3 are nonzero exterior vectors;

stronger/origin-stable coordinate package:
  chosen beta-products Pi_{P,Omega_1}, Pi_{P,Omega_211}, Pi_{P,Omega_3}
  are p-units.
```

The stronger package is more certificate-like, but also more coordinate
dependent.  Small data says nonvanishing looks generic; it does not yet supply
the class-field identity needed to prove the p-unit status without enumerating
the class set.
