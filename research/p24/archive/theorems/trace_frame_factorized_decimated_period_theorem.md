# Trace-Frame Factorized Decimated-Period Theorem

Date: 2026-06-06

This note pins the current best p24 theorem candidate in the same coordinates
as:

```text
p24/trace_frame_decimated_period_certificate_target.md
p24/trace_frame_factorized_schubert_punit.md
p24/trace_frame_schubert_packet_norm.md
```

It is the explicit four-factor version of the decimated trace-period rank
theorem.  It is not yet proved; it is the arithmetic statement whose proof
would finish the current sub-sqrt certificate route.

## Field And Period Schedule

For:

```text
p = 10^24 + 7
m = 66254 = 2*157*211
n = 3107441
```

put:

```text
E = F_p(mu_m),              [E:F_p] = ord_m(p) = 5460
ord_n(p) = 388430
H-packet count = 8
```

In one scalar-extension tensor factor:

```text
B/E has degree 5549 = 31*179
C/E has degree 179
B/C has degree 31
theta = selected n-th root coordinate in B
```

The `E`-Frobenius multiplier on the factor is:

```text
a = p^5460 mod n = 209035,       ord_n(a) = 5549.
```

The subgroup for the relative trace `Tr_{B/C}` is:

```text
h_31 = a^179 mod n = 1293662,    ord_n(h_31) = 31.
```

For each axis frequency `s` let `R_s(X)` be the corresponding
K-character resolvent evaluated in this tensor factor.  The decimated period
coordinates are:

```text
T_{i,t}(R_s)
  = sum_{j=0}^{30}
      theta^(i*a^t*h_31^j) R_s(theta^(a^t*h_31^j)),
    0 <= i < 3, 0 <= t < 179.
```

Equivalently:

```text
T_i(R_s) = Tr_{B/C}(theta^i R_s(theta)) in C
```

and the index `t` records the fixed normal-basis coordinates of `C/E`.

The axis frequency set is:

```text
S_axis = {0} union S_2 union S_157 union S_211
|S_axis| = 368

S_2   = {33127}
S_157 = {422*j mod m : 1 <= j < 157}
S_211 = {314*j mod m : 1 <= j < 211}
```

Split:

```text
A = {0} union S_2 union S_157,        dim_E A = 158
B_axis = S_211,                       dim_E B_axis = 210
W_axis = A + B_axis,                  dim_E W_axis = 368.
```

## Four Schubert Factors

Fix the deterministic normal-basis coordinate flag of `C/E`.  For one
H-packet and one tensor factor, define four determinant-line sections:

```text
Delta_A:
  selected Top_1 Plucker coordinate proving
  rank_E(T_0 on A) = 158.

Delta_B:
  selected Top_2 Plucker coordinate proving
  rank_E((T_0,T_1) on B_axis) = 210.

Delta_AB:
  selected quotient Plucker coordinate proving
  rank_E(Top_2(B_axis) modulo Top_2(A)) = 200.

Delta_tail:
  selected residual-tail Plucker coordinate proving
  pi_10 o b_28 is injective on
  K_2 = ker(Top_2|W_axis).
```

The dimension forcing is:

```text
dim C^2 = 2*179 = 358
dim A + dim B_axis - dim C^2 = 158 + 210 - 358 = 10.
```

Thus `Delta_AB != 0` says the prefix intersection has the minimal forced
dimension:

```text
dim_E(Top_2(A) cap Top_2(B_axis)) = 10.
```

Then `Delta_tail != 0` says the third trace-coordinate head separates exactly
that ten-dimensional forced kernel.

## Finite Implication

The four p-unit statements imply:

```text
Top_2(W_axis) has rank 358;
K_2 = ker(Top_2|W_axis) has dimension 10;
pi_10 o b_28 : K_2 -> E^10 is injective;
therefore Top_3,lead : W_axis -> E^368 is injective.
```

Here:

```text
Top_3,lead = first 179 coordinates of T_0
           + first 179 coordinates of T_1
           + first 10 coordinates of T_2.
```

Since `Top_3,lead` is a selected subcoordinate of the full
`368 x 537` decimated period matrix, this proves the rank-368 trace-frame
theorem for the tensor factor.  The existing scalar-extension and
semilinear-symmetry gates then transport the result to every p24 H-packet.

The finite logic is guarded by:

```text
p24/lean/TraceFramePrefixIntersectionGate.lean
p24/lean/TraceFrameResidualTailGate.lean
p24/lean/TraceFrameAnnihilatorGate.lean
p24/lean/TraceFrameSchubertPacketNormGate.lean
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
```

## Decomposition-Field P-Unit Theorem

Let:

```text
K_m = Q(mu_m)
M   = Q(zeta_n)^<p>,        [M:Q] = 8
S   = K_m M.
```

The desired arithmetic theorem is:

```text
There are determinant-line sections

  Xi_A, Xi_B, Xi_AB, Xi_tail in S

whose residues at the eight primes over the selected prime of K_m above p
are, up to explicit E-units, the four packet determinants

  Delta_A(a), Delta_B(a), Delta_AB(a), Delta_tail(a).

Moreover,

  Norm_{S/K_m}(Xi_A),
  Norm_{S/K_m}(Xi_B),
  Norm_{S/K_m}(Xi_AB),
  Norm_{S/K_m}(Xi_tail)

all have nonzero residue modulo the selected prime over p.
```

This compresses the proof surface from:

```text
8 H-packets * 4 factors = 32 local p-unit statements
```

to:

```text
4 relative degree-8 p-unit statements over K_m.
```

With tensor-factor rank symmetry, these four statements cover the chosen
tensor-factor representative and hence the p24 axis certificate.  Without
that symmetry, the same packet-norm compression still reduces the factorwise
surface to `4*70` relative degree-8 statements.

## Denominator-Safe Variant

The tail factor is the most delicate one globally.  Packetwise computation of:

```text
K_2 = ker(Top_2|W_axis)
```

can introduce denominators from the chosen prefix chart.  A packetwise
Gaussian-elimination basis for `K_2` is therefore not automatically the
residue of one determinant-line section over `S`.

The next most provable-looking theorem is consequently:

```text
Construct denominator-safe sections

  Xi_A, Xi_B, Xi_AB, Xi_lead in S

whose packet residues are the three prefix Schubert factors and the full
leading `179+179+10` Plucker coordinate, up to p-units.

Prove

  Norm_{S/K_m}(Xi_A),
  Norm_{S/K_m}(Xi_B),
  Norm_{S/K_m}(Xi_AB),
  Norm_{S/K_m}(Xi_lead)

are p-units at the selected prime over p.
```

Then:

```text
Delta_prefix = Delta_A * Delta_B * Delta_AB
Delta_lead   = Delta_prefix * Delta_tail
```

on the open prefix chart, so the residual-tail p-unit follows without making
the packetwise kernel basis primary data.  The four-factor tail statement is
still the clearest local obstruction, but the `Xi_lead` version is safer for
class-field descent.

The finite bookkeeping for this denominator-safe package is Lean-checked in:

```text
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
```

It proves that global p-unit norms for `Xi_A`, `Xi_B`, `Xi_AB`, and
`Xi_lead`, plus the packetwise finite implication "prefix-good and lead-good
imply trace-frame-good", exclude every harmful packet.  The gate deliberately
does not assert that `Xi_tail` exists as an independent global section.

## Equivalent Failure To Exclude

For an axis weight:

```text
w(r) = alpha
     + lambda_2(r mod 2)
     + lambda_157(r mod 157)
     + lambda_211(r mod 211)
```

define:

```text
x_w = sum_r w(r) J_r(theta) in B.
```

A failure of the theorem is equivalent to a nonzero `w` such that:

```text
Tr_{B/C}(x_w) = 0
Tr_{B/C}(theta*x_w) = 0
```

and the `theta^28` coefficient of `g'(theta)*x_w` lies in the normal-basis
tail:

```text
span_E{nu_10, nu_11, ..., nu_178} subset C.
```

So the theorem is also the assertion:

```text
No nonzero CRT-axis class-period combination lands in the forced
prefix kernel with its residual coefficient supported outside the selected
10-coordinate normal head.
```

This is much sharper than asking for generic rank of a degree-388430 packet.
It is a selected Schubert-position theorem for the exact p24 CM packet.

## Why This Beats Sqrt(p)

The explicit verifier surface for the four factors is:

```text
Delta_A:       158 x 158
Delta_B:       210 x 210
Delta_AB:      200 x 200
Delta_tail:     10 x 10
```

or `109164` `E`-entries per H-packet.  For all eight H-packets, expanded over
`F_p`, this is:

```text
4,768,283,520 F_p slots = 4.76828352e-3 * sqrt(p).
```

Even expanding all 70 tensor factors remains below sqrt:

```text
333,779,846,400 F_p slots = 0.3337798464 * sqrt(p).
```

The p-unit theorem is smaller still: four relative degree-8 norms over
`K_m`.  Proving or producing those four norms is therefore an asymptotic
speed-up over any class-set or sqrt-scale enumeration.

## Current Proof Mechanisms To Try

The theorem now has three plausible proof mechanisms:

```text
1. determinant-line class-field identity:
   construct Xi_A, Xi_B, Xi_AB, Xi_tail directly over S=K_m M and prove their
   norms are p-units by an explicit finite-field/cyclotomic identity;

2. Schubert divisor contradiction:
   identify the four zero divisors as pulled-back modular/CM Schubert
   divisors and show the selected p24 packet cannot meet them modulo p;

3. low-degree exclusion:
   prove the equivalent residual failure would force a forbidden
   relative-degree <=28 congruence for a nonzero CRT-axis class period.
```

The most likely weak premise is not the finite factorization; that is now
well guarded.  The fragile step is the existence of a denominator-safe global
`Xi_tail` section, because packetwise kernel bases can introduce prefix
denominators.  The denominator-free fallback is to prove the single leading
section `Xi_lead` plus the prefix p-units, then infer the residual-tail
p-unit by:

```text
Delta_lead = Delta_prefix * Delta_tail
```

on the open prefix chart.
