# Order-19 Relative Content Boundary

The first strict p24 trace remains the cleanest theorem toy:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 278733727154 = 19 * 14670196166
quotient degree = 19
recovery degree = 14670196166
p == -1 mod 19
```

Because `p == -1 mod 19`, the order-19 Fourier/Kummer layer lives over
`F_{p^2}`.  This makes the finite-field normal form unusually small.

## What The Quadratic Descent Buys

Once the embedded quotient periods

```text
y_r = sum_k j_{r+19*k}
```

are known, the order-19 twisted traces are just a length-19 DFT over
`F_{p^2}`.  Frobenius pairs `T_s` with `T_{19-s}`.  The Kummer constant
`T_1^19` is invariant under cyclic rotation of the oriented quotient ordering,
up to the Frobenius ambiguity.

This is a good normal form for a certificate:

```text
small quotient field,
quadratic roots of unity,
degree-19 quotient polynomial.
```

## What It Does Not Buy

The local audits still close the obvious escapes:

```text
p24/order19_kummer_shortcut_audit.py
p24/order19_ring_ray_sequence_audit.py
p24/order19_power2_level_audit.py
p24/order_l_kummer_phase_toy.py
p24/quotient_period_low_degree_feature_audit.py
```

Their conclusions are:

```text
zeta_19 in F_p^2:
  diagonalizes the period vector after it is known;

ring/ray conductor 19:
  gives ramified local kernels of size 18, 9, 162, ...,
  not the unramified degree-19 Hilbert quotient;

level 2^19:
  has small X0 degree 786432, but the horizontal edge still has full
  class orbit h and is not the coset projector;

Kummer phase toy:
  unordered quotient periods have multiple possible Kummer constants.
  The true constant is selected only after an oriented quotient action is
  supplied.

low-degree local feature audit:
  degree <= 3 formulas in generous local Phi_ell features fail on
  ell=index examples with h=60 and h=91;
  degree 4 succeeds only by full row-rank interpolation.
```

Thus the order-19 target is a small version of the same embedded phase
problem.  The quadratic cyclotomic field reduces arithmetic after the
orientation is known; it does not choose the orientation.

## Content-Certificate Version

For the order-19 toy, the exact relative-content target from
`relative_resolvent_content_certificate.md` has only one nontrivial Frobenius
orbit up to sign:

```text
Frobenius: a -> -a mod 19.
```

For a representative `a`, define

```text
J_u(X) = sum_k j_{u+19*k} X^k,
f_a(X) = minimal polynomial of zeta_19^a over F_p.
```

The exact certificate is:

```text
(J_0 mod f_a, ..., J_18 mod f_a) is nonzero.
```

The stronger product certificate is:

```text
prod_{u=0}^{18} (J_u mod f_a) != 0.
```

This is a cleaner proving ground for a future norm formula, but it is not the
best p24 certificate route because its recovery degree is
`14670196166`, much larger than the third trace's `3107441`.

## Transfer Lesson

Any successful order-19 identity must identify the unramified class-group
quotient, not a small conductor or small level substitute.  If such an
identity is phase-aware, the same kind of identity might transfer to the
third trace's order-157 and order-211 quotient phases.  If it only works after
the quotient ordering is supplied, it is a normal form rather than a
selector.
