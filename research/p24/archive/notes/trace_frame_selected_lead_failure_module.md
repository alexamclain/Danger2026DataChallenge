# Trace-Frame Selected-Lead Failure Module

Date: 2026-06-06

This note corrects a bookkeeping compression that appeared in several
frontier notes.  The selected leading p24 certificate is not equivalent to
the full top-three annihilator statement:

```text
W_axis cap F_27 = {0}.
```

It is stronger.

## Filtration

For one tensor factor, write:

```text
g'(theta) * x =
  b_0(x) + b_1(x) theta + ... + b_30(x) theta^30,
```

with `b_i(x) in C`, `[C:E]=179`.

Define:

```text
F_j = { x : deg_C(g'(theta)*x) <= j }.
```

Then:

```text
F_27:
  b_30=b_29=b_28=0

F_28:
  b_30=b_29=0.
```

The intrinsic full top-three trace-frame theorem is:

```text
W_axis cap F_27 = {0}.
```

The selected leading coordinate uses only:

```text
all coordinates of b_30,
all coordinates of b_29,
the first 10 normal-basis coordinates of b_28.
```

Thus its failure module is:

```text
K_sel =
  { x in W_axis cap F_28 :
      pi_10(b_28(x)) = 0 }.
```

The actual selected-leading theorem is:

```text
K_sel = {0}.
```

## Direction Of Implication

Since `b_28(x)=0` implies `pi_10(b_28(x))=0`, every full top-three failure is
a selected-leading failure:

```text
W_axis cap F_27 != {0}
  => K_sel != {0}.
```

Therefore:

```text
K_sel = {0}
  => W_axis cap F_27 = {0}.
```

But the converse is false.  The full top-three theorem can hold while the
selected 10-coordinate leading minor still fails, because a nonzero element
of `W_axis cap F_28` may have `b_28` supported entirely in the normal-basis
tail:

```text
b_28(x) in span_E{nu_10,...,nu_178}.
```

This finite implication and the counterexample to the converse are
Lean-checked in:

```text
p24/lean/TraceFrameSelectedLeadFailureGate.lean
```

## Correct Fitting Target

For the selected leading map:

```text
T_lead,Omega :
  Lambda_axis tensor A_Omega
    -> O_E^368 tensor A_Omega,
```

the zeroth Fitting ideal controls:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }.
```

So the selected-leading p-unit theorem is:

```text
K_sel,Omega = {0}
```

for every beta orbit `Omega`, equivalently:

```text
det(T_lead,Omega) in A_Omega^*.
```

The often-written condition:

```text
W_axis(A_Omega) cap F_27(A_Omega) = {0}
```

is a necessary consequence and the intrinsic full top-three transversality
theorem.  It is not sufficient for the selected `179+179+10` certificate.

## Consequence

This sharpens the missing theorem.  A proof cannot stop at:

```text
no nonzero axis period lies in F_27.
```

It must prove the residual-tail Schubert statement:

```text
pi_10 o b_28 :
  W_axis cap F_28 -> E^10
```

is injective after the prefix rank theorem gives:

```text
dim_E(W_axis cap F_28)=10.
```

This is exactly why the denominator-safe global package should use:

```text
Xi_A, Xi_B, Xi_AB, Xi_lead
```

rather than replacing `Xi_lead` by a full-annihilator `F_27` condition.
