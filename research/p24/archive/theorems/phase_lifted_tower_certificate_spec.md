# Phase-Lifted Tower Certificate Spec

Date: 2026-06-05

This note states the surviving decomposed CM certificate surface as an
explicit finite verifier.  It separates the sub-sqrt artifact from the missing
producer theorem.

## p24 Target

Use the third strict trace:

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
sqrt(p) = 1000000000000
```

The H-period handoff is:

```text
H = <g^m>, |H| = n
y_r = sum_{k=0}^{n-1} j_{r+m*k}, 0 <= r < m
```

The quotient tower is:

```text
1 -> 2 -> 2*157 = 314 -> 2*157*211 = 66254.
```

## Certificate Artifact

A phase-lifted certificate may carry:

```text
1. top polynomial P_2(Z), degree 2;
2. relative relation F_157(Z,Y), monic degree 157 in Y,
   coefficients of Y^0..Y^156 polynomial in Z of degree < 2;
3. relative relation F_211(Y,W), monic degree 211 in W,
   coefficients of W^0..W^210 polynomial in Y of degree < 314;
4. one selected recovery polynomial R(W,J), specialized at the selected
   quotient root W0, monic degree 3107441 in J;
5. one root chain Z0, Y0, W0, J0;
6. a Montgomery A above J0 and an x0 for the DANGER3 verifier.
```

The finite checks are:

```text
P_2(Z0) = 0;
F_157(Z0,Y0) = 0;
F_211(Y0,W0) = 0;
R(W0,J0) = 0;
J0 = 256*(A^2-3)^3/(A^2-4) mod p;
A^2 - 4 != 0;
DANGER3 x-only replay accepts (p,A,x0).
```

This verifier never enumerates the full `h` CM roots.  The strict DANGER3
tail is already recorded in:

```text
p24/post_j_root_to_triple_boundary.md
p24/post_cm_root_projection_boundary.md
```

The payload taxonomy is now also checked in:

```text
p24/lean/PhaseLiftedTowerPayloadGate.lean
p24/phase_lifted_payload_accounting_frontier.md
```

That gate separates "below fixed `sqrt(p)`" from the stronger requirement that
the producer be class-set-free.  This matters because the literal p24 class
number is below `sqrt(p)` for this fixed instance, but an `h`-scale class table
is still the forbidden sqrt-scale behavior.

## Degree / Slot Accounting

Count field coefficients excluding monic leading coefficients:

```text
top slots:                 2
degree-157 relation:       2*157     = 314
degree-211 relation:       314*211   = 66254
selected recovery:         3107441
total:                     3174011
```

Thus:

```text
3174011 / sqrt(p) = 3.174011e-6.
```

This is only `316` slots more than the formal quotient-plus-recovery count:

```text
m+n = 3173695.
```

The extra `316` is the top polynomial plus the degree-157 relative phase.

There is an even smaller selected-chain variant.  If the arithmetic theorem
directly supplies the selected root chain rather than all parent-relative
relations, the finite artifact can carry:

```text
top polynomial:             2
selected degree-157 child:  157
selected degree-211 child:  211
selected recovery:          3107441
total:                      3107811
```

So:

```text
3107811 / sqrt(p) = 3.107811e-6.
```

This is the surface checked by the Lean gate: a selected chain plus a
producer-soundness theorem.  The full-relation artifact above is more
table-like and easier to state uniformly over all parents, but not logically
required if the producer theorem is already phase-selective.

By contrast, carrying the full recovery relation

```text
U(W,J) = prod over every quotient root W of its recovery fiber
```

would require about

```text
m*n = h = 205880396014
```

coefficients in dense form.  That is the table we must avoid.  The selected
degree-`n` recovery polynomial is the right finite object.

A cheap selected-recovery producer would exist if the order-`3107441`
recovery class had a split-prime-power representative below the quotient
degree threshold.  That shortcut is already closed in:

```text
p24/low_norm_order3107441_search.md
```

It found no signed split-prime-power word of norm at most `66254`, even after
including the ramified genus prime `599`.  The known composite representative

```text
2 * 463 * 223^(-1)
```

has norm `206498` and `X0` index proxy `311808`, so it is useful as an
oriented formal class but not as a below-threshold zero-lemma/walk producer.

## Toy Verification

I added:

```text
p24/phase_lifted_tower_certificate_toy.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/phase_lifted_tower_certificate_toy.py
```

It uses:

```text
D = -5000
q = 1259
h = 30 = 2 * 3 * 5
quotient factors = [2,3]
recovery size = 5
```

Key output:

```text
top_poly_degree=2
relation_level=1 parent_count=2 child_factor=3 child_count=6
selected_child_level=1_coeffs_ascending=[563, 777, 133, 1]
selected_chain_values=[1126, 159]
selected_recovery_degree=5
selected_j=3
chain_and_recovery_verify=1
selected_chain_artifact_verify=1
selected_j_satisfies_full_H_D_sanity_check=1
toy_certificate_slots_excluding_monic=13
toy_selected_chain_slots_excluding_monic=10
toy_full_h=30
```

The toy generation still uses the full embedded CM cycle; that is deliberate.
The point is that verification of the resulting phase-lifted artifact does
not.

## What The Missing Theorem Must Produce

The theorem must supply the embedded objects, not just abstract class-field
quotients:

```text
P_2, F_157, F_211, selected R(W0,J)
```

with the correct pairing to the embedded conductor-2 `j` torsor.

Equivalently, it must compute the embedded relative non-genus class-character
traces for the `157` and `211` layers and then the selected recovery fiber,
without enumerating all `h` CM roots.

The following are not sufficient:

```text
abstract quotient field roots;
unpaired bnrclassfield equations;
genus-only labels;
low-degree functions of the parent period;
dense h-sized recovery interpolation.
```

The recent coefficient-complexity scan shows that the informative relative
coefficients behave as full-degree functions of parent periods in small CM
data:

```text
p24/tower_phase_coefficient_complexity_boundary.md
```

So the producer must be a genuine embedded class-field/tower formula, a
p-unit norm theorem, or an equivalent finite-field split-cycle identity.

The selected-chain artifact and the alternative p-unit/content route are
compared in:

```text
p24/selected_chain_vs_punit_producer_boundary.md
```

## Lean Use

This surface is now simple enough for Lean to be productive, but only for the
finite implication:

```text
root chain + recovery root + j-to-A equation + DANGER replay
  => supplied A,x0 is a valid DANGER3 triple.
```

Lean will not prove the arithmetic producer theorem.  The arithmetic theorem
must first identify exact p24 polynomials or p-unit identities; then Lean can
check that the finite certificate format implies the verifier statement.

I added the finite gate:

```text
p24/lean/PhaseLiftedTowerGate.lean
```

Direct check:

```text
lean p24/lean/PhaseLiftedTowerGate.lean
```

## Executable p24 Verifier Skeleton

The selected-chain surface has an executable verifier skeleton:

```text
p24/phase_chain_certificate_verifier.py
```

Run without a certificate to print the JSON schema and p24 slot accounting:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/phase_chain_certificate_verifier.py --schema
```

Given a payload, it checks:

```text
top_poly(Z0) = 0,
selected degree-157 child polynomial at Y0 = 0,
selected degree-211 child polynomial at W0 = 0,
selected recovery polynomial at J0 = 0,
optional J0 = j(A),
optional DANGER3 x-only replay accepts (p,A,x0).
```

It does not prove producer honesty.  Its purpose is to make the
`3107811`-coefficient selected-chain artifact a concrete verifier target.
