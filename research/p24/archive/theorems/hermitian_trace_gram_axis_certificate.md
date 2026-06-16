# Hermitian Trace-Gram Axis Certificate

This is the current sharper determinant surface for the p24 axis theorem.

## Why Hermitian

For p24,

```text
n = 3107441
d = ord_n(p) = 388430
```

is even.  Since `n` is prime, the middle Frobenius power satisfies

```text
p^(d/2) == -1 mod n.
```

Thus the involution on the packet field

```text
x -> x^(p^(d/2))
```

sends an `H`-character packet to the inverse `H`-character packet.  This is
the finite-field analogue of the complex Hermitian pairing on character
resolvents.

## Certificate Statement

For each packet factor

```text
A_a = F_p[X]/(f_a),       deg(f_a)=d=388430,
```

let

```text
Y_0, ..., Y_367
```

be the images of the standard axis basis of `W_axis` under

```text
T_a : W_axis -> A_a.
```

Define the Hermitian trace-Gram matrix

```text
H_a(i,j) = Tr_{A_a/F_p}(Y_i * Y_j^(p^(d/2))).
```

If

```text
det(H_a) != 0 mod p
```

for all eight packet factors, then the Hermitian trace pairing separates the
axis image.  Therefore `T_a` is injective on `W_axis` for every packet, and
the existing Lean gate gives:

```text
Hermitian trace-Gram nonzero
  => axis injectivity
  => L1 packet nonvanishing
  => harmful all-zero packets ruled out.
```

The finite implication uses the same abstract pairing-separates-kernel gate in

```text
p24/lean/AxisInjectivityGate.lean
```

as the ordinary trace-Gram note.

## Why This Improves the Ordinary Trace Gram

The ordinary trace Gram

```text
Tr(Y_i Y_j)
```

is only a sufficient certificate and can fail on a proper independent
subspace.  The finite-field toy in

```text
p24/trace_pairing_axis_boundary.py
```

shows that formally, and the structure scan found an actual tiny CM axis row:

```text
D=-524, q=167, h=15, m=3, n=5, deg=4
axis_rank=3
ordinary_trace_gram_rank=2
```

I added:

```text
p24/hermitian_trace_gram_scan.py
```

Pinned on that same row, the Hermitian pairing gives:

```text
ordinary_gram=2
hermitian_gram=3
ordinary_failed_hermitian_rescued_rows=1
```

So the Hermitian pairing is not just cosmetic; it fixes the first CM
counter-signal to the ordinary trace-Gram determinant.

## Small CM Evidence

Broader even-degree window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_trace_gram_scan.py \
  --max-cases 24 --min-h 12 --max-h 180 --max-abs-D 70000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 700000 \
  --max-splitting-primes 2 --max-axis-dim 75 \
  --include-linear --summary-only
```

reported:

```text
packet_rows=48
full_axis_rank_rows=48
ordinary_gram_failure_rows=1
hermitian_possible_rows=30
hermitian_gram_failure_rows=0
ordinary_failed_hermitian_rescued_rows=1
```

Composite-`m` slice:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_trace_gram_scan.py \
  --max-cases 16 --min-h 12 --max-h 180 --max-abs-D 80000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --max-axis-dim 75 \
  --include-linear --require-composite-m --summary-only
```

reported:

```text
packet_rows=14
full_axis_rank_rows=14
ordinary_gram_failure_rows=0
hermitian_possible_rows=14
hermitian_gram_failure_rows=0
```

This is still toy-scale evidence, but it better matches the p24 packet
geometry than the ordinary trace pairing.

## Structure Boundary

I tested whether the Hermitian determinant factors for free through complement
characters or CRT component blocks.  The scan is:

```text
p24/hermitian_trace_gram_structure_scan.py
```

It checks:

```text
1. whether K_{r,s}=<F_r,F_s> depends only on r-s;
2. whether the trace-zero CRT blocks U_c are mutually orthogonal;
3. whether the constant block is orthogonal to every U_c.
```

Composite-`m` eligible window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_trace_gram_structure_scan.py \
  --max-cases 16 --min-h 12 --max-h 180 --max-abs-D 80000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --max-axis-dim 75 --max-m 90 \
  --include-linear --require-composite-m --summary-only
```

reported:

```text
packet_rows=14
full_hermitian_gram_rows=14
kernel_diff_circulant_rows=0
constant_orthogonal_to_all_component_rows=0
all_cross_component_blocks_zero_rows=0
max_cross_block_rank_seen=1
```

Broader eligible window:

```text
packet_rows=30
full_hermitian_gram_rows=30
kernel_diff_circulant_rows=0
constant_orthogonal_to_all_component_rows=0
all_cross_component_blocks_zero_rows=0
```

The first `max_cross_block_rank_seen=1` signal looked like it might support a
low-rank CRT coupling theorem.  A focused audit ruled this out:

```text
p24/hermitian_cross_block_rank_audit.py
p24/hermitian_cross_block_rank_boundary.md
```

On rows with genuinely multidimensional component pairs, for example

```text
D=-8711, h=132, m=12=4*3, n=11
D=-10919, h=156, m=12=4*3, n=13
```

the nontrivial `(4,3)` cross block has rank `2` while the Hermitian Gram remains
full rank.  Thus the earlier rank-one behavior was caused by easy examples
with a component `2`, not by a general pairwise rank-one coupling law.

The diagonal-block/Schur product version is recorded in:

```text
p24/hermitian_component_schur_audit.py
p24/hermitian_component_schur_boundary.md
```

On pinned `(4,3)` rows the constant, `4`, and `3` diagonal blocks are
nonsingular, but

```text
det(full Gram) / product(det(diagonal blocks))
```

is nontrivial and varies with the split prime.  A broader bounded window found
no singular diagonal block inside a full-nonsingular row, so component p-units
remain plausible sublemmas.  But the Schur correction is a real coupled
selected-prime unit, not a free constant.

Thus the Hermitian Gram target does not appear to factor automatically into
full `K`-character, CRT-component determinants, or component determinants plus
rank-one Schur corrections.  The reason is structural: the trace is taken in
the selected H-character packet field, while complement translation of the CM
class coordinate is not an automorphism of that packet field.  So the
determinant is a genuinely coupled inverse-character autocorrelation invariant.

## Arithmetic Meaning

`H_a(i,j)` is an inverse-character autocorrelation of the axis packet.  It is
therefore the matrix version of the Hermitian/energy route:

```text
scalar Hermitian energy:
  one packet autocorrelation scalar is a p-unit;

Hermitian axis Gram:
  the 368-dimensional axis autocorrelation matrix has p-unit determinant.
```

Over characteristic zero, the analogous complex Hermitian Gram is positive
definite whenever the axis images are independent.  The selected-prime problem
is local:

```text
prove this Hermitian Gram determinant is a p-unit at primes above p.
```

Equivalently, prove that the axis images form a nondegenerate local lattice
inside the selected packet algebra.

The local-lattice formulation is recorded in:

```text
p24/hermitian_axis_lattice_primitivity.md
p24/hermitian_origin_invariance_theorem.md
p24/hermitian_axis_packet_norm_theorem.md
```

It also records the warning that unramifiedness alone does not force
Hermitian-unimodularity of a chosen sublattice, via
`p24/hermitian_trace_isotropic_toy.py`.

The origin-invariance note proves that rotating the embedded CM origin
conjugates the Hermitian Gram matrix by a unimodular axis-basis change.  Thus
the determinant's p-unit status is independent of origin; the remaining
arithmetic theorem is packetwise.  The packet-norm note packages all eight p24
packet determinants as one degree-8 decomposition-field p-unit statement.

## Missing Lemma

The new missing lemma is:

```text
For every p24 packet factor f_a, det(H_a) is nonzero modulo p.
```

A stronger number-field version would prove that the algebraic Hermitian
determinant is a p-unit before reduction.  Existing local normal-basis
theorems prove some normal generator exists; they do not prove this selected
level-1 `j` axis lattice is unimodular at the p24 split prime.
