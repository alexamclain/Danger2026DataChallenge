# Representative CS-Theory Candidate Boundary

Date: 2026-06-05

This note records what can be imported from CS/ML theory for the current
one-punit representative surface.

## Live Object

The representative p24 theorem is:

```text
L_rep != 0,
```

equivalently:

```text
K = ker(a_2,a_3,a_5,a_6) has dimension 16,
pi_16(a_1)|_K is injective.
```

This is exactly a rank-metric/subspace-polynomial statement.  The four prefix
right packets define a shortening kernel `K`, and the first 16 Lang tail
coordinates must be an erasure-decoding check on that kernel.

## Useful Imports

The imports that still touch the theorem are:

```text
rank-metric tuple span;
linearized subspace polynomials;
Moore residual products;
erasure/shortening language for interleaved Gabidulin-like codes;
PIT only after arithmetic p-unit lifting;
ML only as exact norm/resultant conjecture mining.
```

The theorem shape to prove is not generic Gabidulin MRD.  It is:

```text
the actual mixed CM trace-dual coordinates have representative
Moore residual product L_rep a p-unit at p = 10^24 + 7.
```

## Boundary On "K Is Special" Proofs

The most tempting structural shortcut would be:

```text
K is a subfield or canonical class-field layer.
```

That exact statement is impossible for p24:

```text
[L:F_p] = 156,
dim_Fp K = 16,
subfield dimensions of L are divisors of 156:
1,2,3,4,6,12,13,26,39,52,78,156.
```

So `K` cannot be `F_{p^16}` or a scalar multiple of a subfield of that
dimension.

A weaker Frobenius-module theorem is not ruled out.  Since `p mod d` has
orders:

```text
x^156 - 1 over F_p has irreducible degree histogram {1:2, 2:5, 4:36}.
```

There are many formal Frobenius-invariant 16-dimensional sums of irreducible
components:

```text
175491 component choices.
```

Thus a Frobenius-invariance proof would need to identify the exact component
or a norm formula.  Dimension alone does not force it.

## Random-Control Audit

Added:

```text
p24/representative_kernel_cs_boundary_audit.py
```

Small control:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 3 --right-degree 8 --tail-dim 4 --trials 200
```

reported:

```text
prefix_full=198/200
determinant_full=119/200
tail_injective_given_prefix=119/200
prefix_full_tail_fail=79/200
shift_stable_counts={1:0, 2:0, 4:0}
```

Tiny p24-shaped random control:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 3 --right-degree 35 --tail-dim 16 --trials 8 --max-enumerate 1000
```

reported:

```text
prefix_full=8/8
determinant_full=2/8
tail_injective_given_prefix=2/8
prefix_full_tail_fail=6/8
kernel_dim_hist={16:8}
shift_stable_counts={1:0, 2:0, 4:0}
```

Interpretation:

```text
prefix full rank does not imply tail injectivity;
random prefix kernels do not carry obvious Frobenius-shift invariance;
therefore any such invariance in the actual CM K would be a strong
arithmetic theorem, not a formal CS consequence.
```

## Fourier-Uncertainty Import

Finite Fourier uncertainty remains useful as a falsification language:

```text
no nonzero trace word should have right support inside
O4 plus the unused 19-coordinate slice of O1.
```

But standard Chebotarev/minor uncertainty does not directly imply the
representative theorem, because the bad space is not a simple time-frequency
support rectangle.  It is the intersection of the fixed 156-plane `Phi(L)`
with a 54-dimensional erasure subspace after Lang coordinates.

The Fourier route becomes viable only if the actual CM trace words can be
identified with a known cyclic/MDS code whose relevant puncturing minors are
provably nonzero.

## ML Import

ML/statistical search should be constrained to equivariant, certifiable
outputs:

```text
stable residual pivot sets;
low-height norm/resultant identities for L_rep, B_rep, or T_rep;
factor patterns invariant under unit-2 and inversion;
failure clusters in small-CM rows that identify a genuine divisor.
```

Non-equivariant features of orbit labels are likely coordinate artifacts.
Anything learned must graduate to an exact finite-field identity or p-unit
theorem.

## Current Best Theorem Candidate

The proof target after this audit is:

```text
Prove the representative Moore residual product L_rep is a selected p-unit
by expressing it as a class-field norm/resultant of the mixed periods S_j,
or equivalently prove that the actual K is transverse to the 16-coordinate
tail map by an arithmetic intersection theorem.
```

This keeps the CS import where it is strongest: it gives the right determinant,
the right erasure-code interpretation, and the right toy falsification tests.
It does not replace the missing class-field p-unit theorem.
