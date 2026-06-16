# Trace-Frame Flag Transversality Theorem

Date: 2026-06-05

This note sharpens the trace-frame target into a flag-transversality theorem.

## Relative Infinity Flag

Keep the tensor-factor notation:

```text
E = F_p(mu_m)
C/E has degree 179
B = C(theta)
[B:C] = 31
g = minimal polynomial of theta over C
```

For `x in B`, write:

```text
g'(theta)*x =
  b_0(x) + b_1(x) theta + ... + b_30(x) theta^30.
```

Define the flag:

```text
F_j = { x in B : b_{j+1}(x)=...=b_30(x)=0 }.
```

Thus:

```text
dim_C F_j = j+1
dim_E F_j = 179*(j+1).
```

The top-coefficient map satisfies:

```text
ker Top_k = F_{30-k}.
```

Equivalently, this is the trace-pairing annihilator flag:

```text
ker Top_k = span_C{1,theta,...,theta^(k-1)}^perp.
```

## p24 Axis Statement

Let `W = W_axis(B)` be the `E`-span of the 368 selected axis
K-character resolvents in one tensor factor.

The intrinsic full-top-three theorem target:

```text
Top_3 is injective on W
```

is exactly:

```text
W cap F_27 = {0}.
```

The stronger maximum-rank-profile theorem is:

```text
rank_E Top_k(W) = min(368, 179*k),       k=1,2,3.
```

Equivalently:

```text
dim_E(W cap F_29) = 368 - 179 = 189,
dim_E(W cap F_28) = 368 - 358 = 10,
dim_E(W cap F_27) = 0.
```

This is a clean Schubert-position statement: the CM axis subspace should lie
in the open Schubert cell relative to the rational flag produced by the
degree-31 extension `B/C`.  After the selected-leading correction, this
intrinsic statement is necessary but not sufficient for the named
`179+179+10` certificate coordinate; the live target is the selected
Schubert-tail module `K_sel=0`.

## Split Version

The component split from the trace-frame frontier becomes:

```text
W_{0,2,157} cap F_29 = {0},          dim W_{0,2,157}=158,
W_{211}     cap F_28 = {0},          dim W_{211}=210,
W_axis      cap F_27 = {0},          dim W_axis=368.
```

The first two are component-normality statements.  The third is the remaining
cross-component flag-transversality statement.

## Targeted Evidence

I extended:

```text
p24/tensor_factor_dual_basis_window_audit.py
```

to count failures of the maximum rank profile:

```text
rank Top_k(target) = min(raw_rank, k*subdegree).
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_dual_basis_window_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-windows 3
```

reported:

```text
rows=5
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=5
max_rank_profile_tests=115
max_rank_profile_failures=0
```

The main `m=12` toy analogue has:

```text
axis dim=6, subdegree=3:
  Top_1 rank=3,
  Top_2 rank=6.
```

and for the other intermediate subfield:

```text
axis dim=6, subdegree=2:
  Top_1 rank=2,
  Top_2 rank=4,
  Top_3 rank=6.
```

This exactly matches the maximum-rank-profile rule.

## Why This Helps

The previous statement:

```text
no nonzero axis weight has top three coefficients zero
```

is equivalent but blunt.  The flag version gives a hierarchy of sharper
failure consequences:

```text
Top_1 failure on W_{0,2,157}
  => a nonzero structured period lies in F_29.

Top_2 failure on W_211
  => a nonzero 211-axis period lies in F_28.

Top_3 failure on W_axis
  => a nonzero full-axis period lies in F_27.
```

In polynomial language, the last condition says:

```text
g'(theta)*x_w
```

has relative degree at most `27` over `C`.

This remains a useful intrinsic subtheorem, but it is no longer sufficient as
the preferred proof target.  A successful arithmetic proof of the selected
coordinate could still use:

```text
1. a p-unit Plucker theorem for the open Schubert cell coordinate;
2. a divisor/degree contradiction for structured CM periods lying in F_27;
3. a class-field identity for the Schubert coordinate/norm;
4. a rank-condenser proof upgraded to a selected-prime p-unit theorem.
```

## Boundary

This is not a generic Grassmannian argument.  Random subspaces have this
profile with overwhelming probability, but p24 needs the selected CM axis
subspace at the selected prime.  The required theorem is:

```text
the p24 CM axis subspace is in maximum-rank position relative to the
relative-infinity flag of B/C.
```

That theorem is necessary for the `L1` certificate route, but the selected
normal-head tail theorem is also needed to finish the named leading
coordinate without enumerating the class set.

The beta-orbit version of this statement is now isolated in:

```text
p24/trace_frame_lead_local_unit_criterion.md
```

There the current p-unit theorem for the selected leading crossed-product norm
is stronger than:

```text
W_axis(A_Omega) cap F_27(A_Omega) = {0}
```

over every nonzero beta-orbit algebra `A_Omega`; it requires
`K_sel,Omega={0}` as recorded in
`p24/trace_frame_selected_lead_failure_module.md`.

## Sum-Rank Strengthening

The same relative coefficient decomposition also gives a coding-theory
strengthening:

```text
p24/trace_frame_sum_rank_erasure_theorem.md
```

Viewing `B ~= C^31`, the axis image is an `E`-linear code of dimension `368`
with block size `179`.  The top-three theorem says one fixed `3`-block
projection is injective.  The stronger theorem says every `3`-block
projection is injective, or equivalently the code has no nonzero word
supported on `28` coefficient blocks.

For p24 this would follow from sum-rank distance:

```text
d_sumrank(W_axis) > 28*179 = 5012.
```

The Singleton bound is:

```text
d <= 31*179 - 368 + 1 = 5182.
```

So an LRS/MSRD-style proof would be more than sufficient.  A targeted
`D=-10919` tensor audit found no failures among `102` dimension-sufficient
relative-block projections, including nontrivial `2`-of-`3` tests.  This is
evidence for the stronger erasure profile, not a certificate.

## Selected Plucker Certificate

The smallest finite certificate surface is recorded in:

```text
p24/trace_frame_selected_plucker_certificate.md
p24/trace_frame_selected_plucker_accounting.py
```

The coordinate-free object is:

```text
Omega_top3 = wedge_{s in S_axis} Top_3(R_s)
             in Exterior_E^368(C^3).
```

The p24 theorem is `Omega_top3 != 0`.  A verifier-friendly certificate names
one Plucker coordinate:

```text
delta_I != 0 in E,
I subset {1,...,537}, |I|=368.
```

There are:

```text
binom(537,368) ~= 10^143.820126
```

possible coordinates, so the coordinate choice is part of the certificate or
must be produced by a class-field norm identity.  This selected Plucker p-unit
is weaker than the all-erasure theorem and remains the smallest honest
trace-frame certificate target.
