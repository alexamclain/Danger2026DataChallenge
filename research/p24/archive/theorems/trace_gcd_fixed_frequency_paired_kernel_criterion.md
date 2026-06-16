# Paired-Kernel Criterion

Date: 2026-06-06

## Statement

Let `B_s` be the right-resolvent packet before pairing and let `A` be the
selected trace-GCD left functional.  For each right H-coset `Q`, define the
right leakage vector

```text
L_Q = sum_{s in Q} B_s.
```

The paired profile is

```text
G_s = A(B_s).
```

Then the H-coset trace condition is exactly:

```text
sum_{s in Q} G_s = 0
iff
A(L_Q) = 0.
```

So the full right-resolvent theorem `L_Q=0` is sufficient but stronger than
needed.  The exact paired theorem is:

```text
L_Q lies in ker(A) for all seven H-cosets Q.
```

## p24 Covariant Form

Under the p24 `rho=p^780` covariance, the seven leakage cosets are generated
from one anchor leakage `L_0`.  The six nontrivial projector equations are:

```text
A(Pi_k L_0) = 0,       k = 1,...,6,
Pi_k = (1/7) * sum_{j=0}^6 omega^(-k*j) rho^j.
```

These six equations are the compressed paired-kernel interface behind the
`1092 = 156 * 7` scalar H-coset verifier.  They are not automatically implied
by covariance, Gauss normalization, DANGER trace congruence, or ordinary
nontrivial left-character pairing; the actual-CM left-paired boundary rules
out that last shortcut.

## Lean Gate

The formal equivalence is recorded in:

```text
p24/lean/TraceGcdPairedKernelCriterionGate.lean
```

This does not prove the arithmetic kernel membership.  It pins the remaining
theorem: construct the trace-GCD weighted product/section so that the six
projected leakage vectors land in the selected left kernel.
