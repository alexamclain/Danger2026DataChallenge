# Targeted Ask Memo For Drew Sutherland

Date: 2026-06-08

Purpose: ask for a focused expert sanity check on the missing CM/class-field
producer theorem for the `p = 10^24 + 7` certificate route.  This is not a
request to solve the full challenge; it is a request to identify whether the
remaining selector theorem is known, impossible as stated, or missing one
standard ingredient.

## One-Sentence Ask

For the p24 CM field below, is there a known explicit CM / Shimura reciprocity
/ elliptic-unit / Lang construction that selects one embedded unramified
`157/211` Hilbert-class phase, or an obstruction showing that such a
class-set-free selector cannot exist without carrying a degree-about-`3107441`
recovery object?

## Fixed Data

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441

E = F_p(mu_m),          [E:F_p] = 5460
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7
rho = p^780 fixes the left 157-frequency and shifts the right C_7 quotient by 6
```

The class group is cyclic in this case.  The genus quotient accounts for the
order-2 layer; the odd `157`, `211`, and `3107441` layers are the relevant
unramified class-field structure.

## What We Have Reduced The Problem To

The current best certificate surface is conditional on two p-unit producers:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

That is a four-field-element payload once the p-unit nonvanishing theorems are
proved.  The downstream finite algebra is strongly checked locally.  The live
arithmetic producer target is a selected CM/Lang/Jacobi packet after
`Tr_{B/C}` on

```text
C_7 x C_179.
```

For a raw packet `g(r,c)` and selected defect
`f(r,c)=g(r,c)-g(r,0)`, the value-side theorem we want is:

```text
g(r,0)+g(-r,0)=A_0,
g(r,c)+g(-r,-c)=A_1 for c != 0,
sum_c g(r,c)-179*g(r,0)=B independent of r.
```

Equivalently, `f` lies in a rank-621 admissible C-axis Jacobi-carry span.  The
formal chain from this to forbidden bidegree vanishing, internal trace zero,
right/product coboundaries, and the fixed-frequency verifier is already
gated by small finite tests and Lean handoffs.

## Why The Remaining Question Is Specific

The finite Jacobi algebra is no longer the mystery.  Punctured
Hasse-Davenport plus one degenerate-anchor correction gives the exact local
shape.  The selected correction has footprint

```text
h(r,c)=1 if r=0 and c != 0, else 0.
```

For p24, the residual is the principal cyclotomic/diamond divisor

```text
R_179(X) = Phi_179(X)/(X-1)^178.
```

Equivalently, on the elliptic/subgroup side, the target is the whole
`179`-subgroup kernel polynomial

```text
K_H(x)=prod_{Q in (H\{O})/{+-1}} (x-x(Q)),
deg K_H = 89,
div(K_H)=sum_{Q in H, Q != O}[Q]-178[O].
```

Once a selected auxiliary coordinate or subgroup polynomial is produced, the
p-unit check is tiny:

```text
Res(M(T), X(T)^179 - 1) != 0
```

or equivalently a Bezout identity modulo the selected algebra
`F_q[T]/(M(T))`.

The hard step is before this: construct the selected p-integral
CM/Lang coordinate or selected auxiliary `179`-kernel object inside the
unramified `157/211` Hilbert-class layers without enumerating the class set.

## Negative Evidence So Far

Classical ray/Siegel/Ramachandra/Robert-unit distribution looks relevant for
certifying a unit once a ray/fiber is selected, but it does not appear to
select the conductor-one unramified `157/211` phase in this p24 case.

Local audit:

```text
ell=157: ell_divides_mod_ell_kernel=0
ell=211: ell_divides_mod_ell_kernel=0

squarefree levels 157*211, 2*157*211, 223*463, 2*223*463:
  local unit parts contain neither 157 nor 211
```

Small actual-CM calibration rows also show that generic embedded CM packets,
generic right-character packets, and generic covariance/telescope identities
do not satisfy the required Jacobi/admissible-span conditions.  The producer
has to use the specific selected trace-GCD / CM-Lang packet, not ordinary
period covariance alone.

The final curve over `F_p` is also not the right place to search for a
rational `179`-isogeny: for the selected trace, `179` is Atkin and does not
divide `#E(F_p)`.  The `179`-kernel object must live in the auxiliary
CM/Lang/cyclotomic layer.

## Current Non-Enumerative Selector Candidate

The only plausible selector route we have besides a direct CM/Lang producer is
a low-moment phase selector.

```text
first layer:  P_1..P_4  with P_1 automatic from the parent
second layer: P_1..P_26 with P_1 automatic from the parent

new producer values:
  first layer  e_2..e_4      = 3
  second layer e_2..e_26     = 25
  total                         28

selector constraints including P_1:
  4 + 26 = 30
```

The needed theorem would be a sparse moment-curve anti-collision statement
for the embedded CM quotient roots:

```text
first layer:  no collisions for sizes 5..157 with 4 moments
second layer: no collisions for sizes 27..211 with 26 moments
```

Random entropy and small CM controls are encouraging, but this still needs an
arithmetic construction of the 28 higher relative traces / truncated
coefficients and a proof that the embedded CM roots avoid the sparse signed
relations.

## Questions For Drew

1. Is there a known explicit class-field / CM method that selects a single
   embedded Hilbert-class root or auxiliary subgroup object over `F_p` from
   the unramified odd layers, without computing the full class set?

2. Does Shimura reciprocity, an elliptic/Siegel/Ramachandra unit norm, or a
   Lang-style construction naturally produce the selected `R_179` /
   `K_H` object above once the `157/211` phase is fixed?

3. Is there a Galois-equivariance obstruction that explains why the selector
   must carry a growing-degree recovery object, roughly the `3107441` layer,
   rather than a bounded ray/class invariant?

4. Does the low-moment selector theorem above sound like a viable way to
   select the embedded child fibers, or is there a standard reason such moment
   data cannot be constructed/proved without class enumeration?

5. Are there references or standard tools we should be using here, especially
   from accelerated CM, CRT class polynomial decomposition, class invariants,
   or explicit CM class-field generators?

## Useful Pointers In The Local Folder

```text
p24/00_CURRENT_CONTEXT.md
p24/00_HANDOFF_INDEX_20260607.md
p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
p24/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md
p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate.md
p24/trace_gcd_low_moment_sparse_relation_gate.md
p24/trace_gcd_low_moment_relative_trace_gate.md
p24/ray_kernel_distribution_audit.py
```

Relevant Sutherland-adjacent context:

```text
Andrew V. Sutherland, "Accelerating the CM method"
https://arxiv.org/abs/1009.1082

Andreas Enge and Andrew V. Sutherland, "Class invariants by the CRT method"
https://arxiv.org/abs/1001.3394
```

## Desired Outcome

A short expert answer would be enough:

```text
known construction: look at X/Y/Z;
known obstruction: selector cannot be bounded because X;
or promising new theorem: formulate it as X and prove via Y.
```

Any of those would materially reduce the search space for the p24 certificate.
