# Trace-Frame Selected-Tail Resultant Theorem

Date: 2026-06-06

This note sharpens the current p24 trace-frame proof target after the
selected-leading correction.  The named certificate is not the intrinsic
full-top-three statement alone.  It is the selected Schubert-tail map:

```text
K_sel,Omega = {0}.
```

## Setup

Work orbitwise over the beta factor `A_Omega`.  Let:

```text
K_2,Omega = ker(Top_2|W_axis(A_Omega))
dim K_2,Omega = 10
```

and write:

```text
g'(theta) * x =
  b_0(x) + b_1(x) theta + ... + b_30(x) theta^30.
```

Let `nu_0,...,nu_178` be the fixed normal `E`-basis of `C/E`, and set:

```text
H = span_E{nu_0,...,nu_9}
T = span_E{nu_10,...,nu_178}
P_H : C -> H
```

where `P_H` is the trace-dual projection onto the first ten normal coordinates.
The selected certificate is:

```text
P_H o b_28 : K_2,Omega -> H
```

is injective, hence an isomorphism.

## Direct Operator Theorem

Let `A_T` be the monic `E`-linearized annihilator of the normal-basis tail:

```text
ker(A_T : C -> C) = T,
qdeg_E(A_T) = 169.
```

Since `ker(A_T)=ker(P_H)=T`, the direct selected-tail theorem is:

```text
rank_E { A_T(b_28(k_j)) : 0 <= j < 10 } = 10
```

for any `E`-basis `k_0,...,k_9` of `K_2,Omega`.  Equivalently:

```text
M_tail,Omega =
  det( A_T(b_28(k_j))^(Q^i) )_{0 <= i,j < 10}
  != 0,       Q = |E|.
```

This is the safest finite-field identity to prove as a p-unit.  It proves
`K_sel,Omega={0}` directly and does not require first proving the intrinsic
`W_axis cap F_27={0}` theorem.

## Subspace-Resultant Face

If the residual image has full dimension,

```text
U_Omega = b_28(K_2,Omega),   dim_E U_Omega = 10,
```

then the same zero test can be phrased as:

```text
U_Omega cap T = {0}
```

or, with monic `E`-linearized subspace polynomials `A_U,Omega` and `A_T`:

```text
gcd_q(A_U,Omega, A_T) = X
Res_q(A_U,Omega, A_T) != 0.
```

The dimension hypothesis is important: `U cap T={0}` alone is not a complete
selected-leading proof if `b_28` drops rank on `K_2`.  The direct Moore
determinant of `A_T o b_28` packages both rank and tail avoidance at once.

## P-Unit Certificate Surface

The missing arithmetic theorem can now be stated as:

```text
For every beta orbit Omega, M_tail,Omega is a p-unit at the selected
prime over p = 10^24 + 7.
```

Equivalently, in the denominator-safe global algebra:

```text
A_all = O_E[Y]/(Y^3107441 - 1),
M_tail,all in A_all^*.
```

Proving this gives the selected-leading determinant p-unit, hence the
trace-frame certificate.  Its verifier is sub-sqrt because the payload is a
fixed tower/linearized-resultant identity in the `n=3107441` quotient algebra,
not enumeration over the size-`sqrt(p)` class set.

## Finite Gates

The finite handoff is checked in:

```text
p24/lean/TraceFrameResidualTailGate.lean
```

The new gate records two routes:

```text
selected-tail operator p-unit
  => residual-tail avoidance
  => selected leading coordinate injective
```

and, with the extra full-image hypothesis:

```text
linearized resultant p-unit for A_U and A_T
  => U cap T = {0}
  => residual-tail avoidance.
```

The selected-leading/F_27 implication boundary remains recorded in:

```text
p24/lean/TraceFrameSelectedLeadFailureGate.lean
```

The beta-orbit crossed-product version of the same selected-tail target is:

```text
p24/trace_frame_selected_tail_crossed_product_target.md
p24/lean/TraceFrameSelectedTailCrossedProductGate.lean
```

## Toy Verification

A tiny normal-basis toy checks the equivalences over small finite fields:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/selected_tail_resultant_equivalence_toy.py \
  --m 6 --head-dim 3 --trials 200

Selected-tail resultant equivalence toy
field=GF(2^6)
tail_annihilator_qdegree=3
tail_kernel_matches_tail=1
equivalence_mismatches=0
```

and:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/selected_tail_resultant_equivalence_toy.py \
  --m 7 --head-dim 2 --trials 200

Selected-tail resultant equivalence toy
field=GF(2^7)
tail_annihilator_qdegree=5
tail_kernel_matches_tail=1
equivalence_mismatches=0
```

These tests do not prove the CM p-unit theorem.  They only verify that the
finite-field identity being handed to the arithmetic proof is the right one.
