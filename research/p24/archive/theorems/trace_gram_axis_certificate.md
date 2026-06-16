# Trace-Gram Axis Certificate

This note records a new sufficient certificate surface for the live p24 axis
theorem.

## Setup

For each p24 packet factor

```text
f_a | Phi_3107441
A_a = F_p[X]/(f_a)
deg(f_a)=388430
```

the axis map is

```text
T_a : W_axis -> A_a
T_a(w) = sum_r w(r) F_r(X) mod f_a,
```

where

```text
F_r(X) = sum_k j_{n*r + m*k} X^k,
m=66254,
n=3107441,
dim_Fp(W_axis)=368.
```

Choose the standard axis basis

```text
1,
1_{r == t mod 2}      for 1 <= t < 2,
1_{r == t mod 157}    for 1 <= t < 157,
1_{r == t mod 211}    for 1 <= t < 211.
```

Let the corresponding packet elements be

```text
Y_0, Y_1, ..., Y_367 in A_a.
```

## Sufficient Certificate

Define the ordinary finite-field trace Gram matrix

```text
G_a(i,j) = Tr_{A_a/F_p}(Y_i * Y_j).
```

If

```text
det(G_a) != 0 mod p,
```

then the restricted trace pairing is nondegenerate on `T_a(W_axis)`, hence the
`Y_i` are linearly independent over `F_p`.  Therefore `T_a` is injective on
`W_axis`, and the existing Lean gate gives:

```text
trace-Gram nondegenerate for every packet
  => axis injectivity for every packet
  => L1 nonzero in every packet
  => harmful all-zero packets ruled out.
```

This is lower-dimensional than full relative `K`-normality and more concrete
than the abstract Moore determinant, but it is not in a formal implication
chain with full Moore rank:

```text
full K Moore determinant, size 66254
  => axis injectivity, size 368

trace-Gram determinant, size 368
  => axis injectivity, size 368
```

The trace-Gram determinant is only sufficient, not equivalent.  A proper
subspace of a finite field can be independent and still isotropic for the
ordinary trace form.  Thus full Moore rank does not automatically imply
trace-Gram nondegeneracy on the axis subspace, and trace-Gram nondegeneracy
does not imply full `K`-normality.

The finite implication is Lean-checked in:

```text
p24/lean/AxisInjectivityGate.lean
```

under the abstract gate:

```text
pairing separates the kernel of T_a
  => kernel(T_a)=0
  => T_a is injective.
```

## Boundary Toy and CM Data

I added:

```text
p24/trace_pairing_axis_boundary.py
```

It first checks two finite-field toys:

```text
F4/F2 full basis:
  vector rank = 2
  trace Gram rank = 2

F9/F3 proper subspace span{1+alpha}:
  vector rank = 1
  trace Gram rank = 0
  Trace((1+alpha)^2)=0
```

So a trace discriminant is rank-equivalent for a full basis, but not for a
proper subspace.

Small CM axis scan with all origins:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_pairing_axis_boundary.py \
  --max-cases 8 --min-h 12 --max-h 120 --max-abs-D 20000 \
  --max-prime-quotients 6 --max-composite-quotients 6 \
  --min-n 3 --max-n 120 --q-stop 200000 \
  --max-splitting-primes 1 --max-axis-dim 45 \
  --include-linear --scan-origins --summary-only
```

reported:

```text
packet_rows=223
full_axis_rank_rows=223
full_axis_rank_but_trace_gram_degenerate_rows=0
```

Slightly wider non-origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_pairing_axis_boundary.py \
  --max-cases 16 --min-h 12 --max-h 180 --max-abs-D 60000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 180 --q-stop 500000 \
  --max-splitting-primes 2 --max-axis-dim 70 \
  --include-linear --summary-only
```

reported:

```text
packet_rows=33
full_axis_rank_rows=33
full_axis_rank_but_trace_gram_degenerate_rows=0
```

The next structure scan found the expected failure inside CM data:

```text
p24/trace_gram_structure_scan.py
```

In a broader window it reported:

```text
packet_rows=48
full_axis_rank_rows=48
full_trace_gram_rank_rows=47
```

with the failing row

```text
D=-524, q=167, h=15, m=3, n=5, deg=4
axis_dim=3, axis_rank=3, trace_gram_rank=2.
```

So ordinary trace-Gram nondegeneracy is not a plausible universal CM theorem.
It remains a sufficient p24-specific target, but the Hermitian trace-Gram
variant is now the better live determinant:

```text
p24/hermitian_trace_gram_axis_certificate.md
```

## Class-Field Meaning

The entries

```text
Tr_{A_a/F_p}(Y_i Y_j)
```

are packet traces of products of relative H-character period sums.  Summing
over all H-character packets would give an ordinary cyclic autocorrelation in
the CM class group.  One packet keeps only the Frobenius orbit of the selected
nontrivial H-character.

This makes the determinant a phase-aware autocorrelation invariant.  It is
closer to the Hermitian/energy route than to a plain class polynomial
discriminant, but it keeps the exact axis-support theorem rather than
collapsing to one scalar.

## Relation to Normal-Basis Literature

Normal-basis results for ray class fields are adjacent but do not transfer
directly.  For example, Jung-Koo-Shin prove that certain Siegel-function
singular values form normal bases of ray class fields:

```text
https://arxiv.org/abs/1007.2312
```

The obstruction is the same as in the earlier Siegel/Ramachandra notes:

```text
normality of a ray-class Siegel generator
  does not give normality of the level-1 j axis packet;

ray-kernel distribution relations
  are vertical over level-1 j and do not select a Hilbert class subgroup;

an explicit ray generator
  still needs a phase-preserving transfer to the embedded j-period packet.
```

So the trace-Gram determinant should be treated as a new p-unit target, not as
a corollary of existing Siegel normal-basis theorems.

## Missing Lemma

The first missing lemma is:

```text
For every p24 H-character packet a, the 368 x 368 matrix

  G_a(i,j)=Tr_{A_a/F_p}(Y_i Y_j)

has nonzero determinant modulo p.
```

A stronger algebraic version would prove this determinant is a p-unit in the
corresponding number-field packet before reduction at `p`.

This lemma would imply the desired axis injectivity, but it is still a
selected-prime p-unit theorem.  The advantage is that its entries are packet
autocorrelations, so Gross-Zagier/Borcherds-style divisor or local
intersection formulas may have a more concrete target than the raw Moore
determinant.
