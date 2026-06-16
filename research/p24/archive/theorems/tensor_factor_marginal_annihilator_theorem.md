# Tensor Factor Marginal-Annihilator Theorem

This is the current proof frontier after the CRT marginal-rank reduction.

## Structured Weight Spaces

Let

```text
E = F_p(mu_m),       m = 2*157*211,
C = F_{E^179},       B/C has degree 31,
```

and let

```text
A_k(r) = Top_k(J_r(theta)) in C^k.
```

For a CRT component `c`, define:

```text
M_{c,a}^{(k)} = sum_{r == a mod c} A_k(r),
Delta_c^(k) = span_E {M_{c,a}^{(k)} - M_{c,0}^{(k)} : 1 <= a < c}.
```

A rank failure is exactly a structured weight annihilator.  Namely, for a
weight

```text
w(r) = alpha + lambda_2(r mod 2)
             + lambda_157(r mod 157)
             + lambda_211(r mod 211),
```

with each `lambda_c` trace-zero on its component, define

```text
x_w = sum_r w(r) J_r(theta) in B.
```

Then:

```text
sum_r w(r) A_k(r) = Top_k(x_w).
```

So the marginal theorem is an annihilator-avoidance statement:

```text
nonzero structured w  =>  x_w not in ker Top_k.
```

Using the trace-frame description, this is:

```text
x_w not in Ann_k = span_C{1,theta,...,theta^(k-1)}^perp.
```

## p24 Split Theorem

The three target statements are:

```text
dim_E( E*S_1 + Delta_2^(1) + Delta_157^(1) ) = 158,
dim_E( Delta_211^(2) ) = 210,
dim_E( E*S_3 + Delta_2^(3) + Delta_157^(3) + Delta_211^(3) ) = 368,
```

where `S_k=sum_r A_k(r)`.

Equivalently:

```text
w in constant+2+157, w != 0
  => Top_1(x_w) != 0;

w in 211 trace-zero block, w != 0
  => Top_2(x_w) != 0;

w in full axis, w != 0
  => Top_3(x_w) != 0.
```

In dual-basis form, if

```text
g'(theta) * x_w = b_0(w) + b_1(w) theta + ... + b_30(w) theta^30,
```

then this says:

```text
constant+2+157:       b_30(w) != 0,
211 block:            (b_30(w), b_29(w)) != (0,0),
full axis:            (b_30(w), b_29(w), b_28(w)) != (0,0,0),
```

for every nonzero weight in the indicated structured space.

## Exterior Certificate Surface

The same theorem can be packaged as three nonzero exterior products:

```text
Omega_1 =
  S_1 wedge delta_2,1^(1)
      wedge delta_157,1^(1) wedge ... wedge delta_157,156^(1)
  in Exterior_E^158(C);

Omega_211 =
  delta_211,1^(2) wedge ... wedge delta_211,210^(2)
  in Exterior_E^210(C^2);

Omega_3 =
  S_3 wedge delta_2,1^(3)
      wedge delta_157,1^(3) wedge ... wedge delta_157,156^(3)
      wedge delta_211,1^(3) wedge ... wedge delta_211,210^(3)
  in Exterior_E^368(C^3).
```

Here

```text
delta_c,a^(k) = M_{c,a}^{(k)} - M_{c,0}^{(k)}.
```

The probability heuristic says a random `368`-plane in `C^3` misses the
`Top_3` annihilator with overwhelming probability.  The deterministic lift is
not a probability bound; it is a p-unit theorem saying these exterior
products, or a suitable CM norm of their Plucker coordinates, are not
divisible by the selected prime over `p`.

The origin-action/product refinement is recorded in:

```text
p24/tensor_factor_marginal_origin_action_audit.py
p24/tensor_factor_marginal_origin_product.md
```

It tests the stronger coordinate package

```text
Pi_{P,Omega} = prod_{beta mod n} P(Omega_beta),
```

where `P` is a chosen Plucker coordinate and `Omega_beta` is formed after
multiplication by `theta^(-beta)`.  This product has origin-stable zero status:
beta shifts permute factors, and alpha shifts act by marginal-basis units.
It is stronger and more coordinate-dependent than nonvanishing of the
intrinsic exterior vector for the selected origin.

## Why This Is Sharper Than the Fourier Statement

The DFT/root-of-unity layer has been removed by the formal marginal lemma.
The missing theorem is no longer about character transforms; it is about
affine independence and directness of embedded CM marginal sums.

The small coefficient-profile audit rules out the easiest triangular-support
argument: the adjusted elements `g'(theta)*R_s(theta)` have dense relative
support in the toy row.  So a proof likely needs one of:

```text
1. a p-unit/Plucker-content theorem for the three Omega products;
2. a relative top-degree noncollapse theorem for structured CRT weights;
3. an embedded class-field identity that computes these leading coefficients
   without enumerating the class set.
```

## Current Frontier Note

The current sharpened p24 target, including targeted no-failure summaries for
the CRT marginal audit, is recorded in:

```text
p24/trace_frame_split_frontier.md
```

The key finite identity is:

```text
for every nonzero axis weight w,
g'(theta)*x_w has at least one nonzero theta^30, theta^29, theta^28
coefficient over C.
```

This is equivalent to:

```text
W_axis(B) cap span_C{1,theta,theta^2}^perp = {0}
```

and is now the preferred theorem statement to attack.

## Formal Gate

The finite directness implication is Lean-checked in:

```text
p24/lean/CrtMarginalAnnihilatorGate.lean
```

It verifies that marginal directness plus trivial component kernels implies
injectivity of the combined top-coefficient map.  The open arithmetic input is
exactly the p24 noncollapse theorem above.
