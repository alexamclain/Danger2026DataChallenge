# Trace-Frame Split Frontier

Date: 2026-06-05

This note records the current sharpest version of the `L1` axis certificate
route.

## Finite Setup

For p24:

```text
p = 10^24 + 7
h = m*n
m = 66254 = 2*157*211
n = 3107441
ord_n(p) = 388430
```

After adjoining the complement roots of unity:

```text
E = F_p(mu_m),            [E:F_p] = 5460
A_a = F_p[X]/(f_a),       deg(f_a)=388430
A_a tensor E = product_{i=1}^{70} B_i
[B_i:E] = 5549 = 31*179
```

Choose one tensor factor `B/E` and its degree-179 subfield `C`, so:

```text
C/E has degree 179
B/C has degree 31
B = C(theta)
```

Let `g` be the minimal polynomial of `theta` over `C`.  For an axis weight

```text
w(r) = alpha
     + lambda_2(r mod 2)
     + lambda_157(r mod 157)
     + lambda_211(r mod 211),
```

define:

```text
x_w = sum_r w(r) J_r(theta) in B.
```

The top-coefficient map is:

```text
Top_k(x) =
  the top k C-coefficients of g'(theta)*x
  in the C-basis 1,theta,...,theta^30.
```

Equivalently:

```text
Top_k(x)=0
  iff Tr_{B/C}(theta^i*x)=0 for i=0,...,k-1.
```

## Current Theorem Target

The p24 arithmetic theorem that would finish the L1 route is:

```text
Top_3 : W_axis(B) -> C^3
is injective.
```

In annihilator form:

```text
W_axis(B) cap span_C{1,theta,theta^2}^perp = {0}
```

under the trace pairing `Tr_{B/C}(xy)`.

In dual-basis coefficient form:

```text
for every nonzero axis weight w,
g'(theta)*x_w has at least one nonzero theta^30, theta^29, theta^28
coefficient over C.
```

This is a finite-field identity, not a heuristic.  Combined with the existing
Lean gates, it implies:

```text
Top_3 injective in one tensor factor
  => axis injectivity in every p24 H-packet
  => L1 packet nonvanishing
  => harmful packet collapse is ruled out
  => sub-sqrt certificate route.
```

## Split Subgoals

Dimension accounting suggests proving a stronger structured split:

```text
Top_1 injective on constant + 2 + 157       (dimension 158 < 179)
Top_2 injective on the 211 trace-zero block (dimension 210 < 2*179)
Top_3 injective on the full axis            (dimension 368 < 3*179)
```

Using CRT marginals

```text
A_k(r) = Top_k(J_r(theta)) in C^k
M_c,a^(k) = sum_{r == a mod c} A_k(r)
Delta_c^(k) = span_E{M_c,a^(k)-M_c,0^(k)}
```

the DFT layer is formal.  The remaining arithmetic target is:

```text
dim_E( E*S_1 + Delta_2^(1) + Delta_157^(1) ) = 158
dim_E( Delta_211^(2) ) = 210
dim_E( E*S_3 + Delta_2^(3) + Delta_157^(3) + Delta_211^(3) ) = 368
```

where `S_k=sum_r A_k(r)`.

## Why This Is Progress

This moves the hard theorem from:

```text
degree-388430 packet rank
```

to:

```text
one degree-5549 tensor factor,
then three traces to a degree-179 subfield.
```

The certificate surface is now a `368`-dimensional rank statement inside
`C^3`, whose `E`-dimension is only:

```text
3*179 = 537.
```

That is still an arithmetic p-unit theorem, but it is no longer a raw
class-set computation.

## Targeted Evidence

I added summary failure counts to:

```text
p24/tensor_factor_crt_marginal_rank_audit.py
```

Pinned exact row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_crt_marginal_rank_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1 --max-rows 8
```

reported:

```text
rank_identity_mismatches=0
combined=constantplus4plus3 size=6 rank=3/3
```

With two windows:

```text
rank_identity_mismatches=0
combined=constantplus4plus3 size=6 rank=6/6
```

Targeted nearby-row summaries for `D=-10919`:

```text
windows=1:
  component_blocks_tested=10
  component_capacity_failures=0
  combined_capacity_targets=9
  combined_capacity_failures=0

windows=2:
  component_blocks_tested=10
  component_capacity_failures=0
  combined_capacity_targets=21
  combined_capacity_failures=0
```

A broader summary attempt was intentionally stopped once it became a data
generation job rather than a theorem-guided check.

## Proof Tactics To Try Next

1. Prove a selected-prime p-unit theorem for the exterior products:

```text
Omega_1 in Exterior_E^158(C)
Omega_211 in Exterior_E^210(C^2)
Omega_3 in Exterior_E^368(C^3)
```

2. Convert a hypothetical failure into a low-relative-degree congruence:

```text
g'(theta)*x_w has relative degree <= 27
```

and try to lift that to an impossible divisor/class-period relation.

3. Search for a phase-aware class-field identity for the top coefficients of
`g'(theta)*J_r(theta)`.  Ordinary symmetric norm formulas are not enough,
because the theorem keeps both the order-`3107441` H-phase and the
`2*157*211` axis phase.

The exact p24 exponent schedule and certificate-facing 31-term period matrix
are now isolated in:

```text
p24/trace_frame_decimated_period_certificate_target.md
p24/trace_frame_factorized_decimated_period_theorem.md
```

The factorized theorem note is now the most precise proof target.  It replaces
the single broad `368 x 537` rank ask by four named Schubert factors:

```text
Delta_A:     Top_1 is injective on A=constant+2+157;
Delta_B:     Top_2 is injective on B=211;
Delta_AB:    Top_2(A) and Top_2(B) meet in the forced dimension 10;
Delta_tail:  the selected 10-coordinate residual head separates ker Top_2.
```

Equivariant descent packages these as:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail in K_m Q(zeta_n)^<p>
```

and the remaining arithmetic theorem is that their relative degree-8 norms to
`K_m` are p-units at the selected prime over `p`.

## Flag Transversality Refinement

The same theorem is sharpened in:

```text
p24/trace_frame_flag_transversality_theorem.md
```

Let

```text
F_j = {x in B : deg_C(g'(theta)*x) <= j}.
```

Then:

```text
ker Top_k = F_{30-k}.
```

So the p24 `Top_3` theorem is:

```text
W_axis(B) cap F_27 = {0}.
```

The stronger maximum-rank-profile form predicts:

```text
dim_E(W_axis cap F_29) = 189,
dim_E(W_axis cap F_28) = 10,
dim_E(W_axis cap F_27) = 0.
```

This turns the missing theorem into a selected-prime Schubert-position
statement for the CM axis subspace relative to the `B/C` infinity flag.

## Status

No final p24 certificate yet.  The goal is closer because the missing theorem
is now a specific trace-annihilator avoidance statement in `B/C`, with a
small finite certificate surface and a formal implication chain back to the
original danger certificate.
