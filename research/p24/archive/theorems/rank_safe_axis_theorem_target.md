# Rank-Safe Axis Theorem Target

This note restates the live p24 theorem target after the packet-field DFT rank
caveat.

## Certificate Interface

For the third p24 trace,

```text
p = 10^24 + 7
h = m*n = 66254 * 3107441
deg(f_a) = ord_n(p) = 388430
```

and for each of the eight Frobenius packet factors `f_a | Phi_n`, define

```text
F_r(X) = sum_k j_{n*r + m*k} X^k mod f_a,      0 <= r < m.
```

Let

```text
T_a(w) = sum_r w(r) F_r(X) mod f_a.
```

The rank-safe axis theorem is:

```text
T_a restricted to W_axis is injective over F_p for every packet a,
```

where

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}.
dim_Fp(W_axis)=368.
```

This is the smallest theorem currently known to imply the `L1` certificate
path.  The Lean-checked finite implication is:

```text
axis injectivity
  + L1 weight nonzero
  => L1 packet value nonzero
  => packet content nonzero
  => harmful all-zero packet ruled out.
```

The checked gate is in:

```text
p24/lean/AxisInjectivityGate.lean
```

## Stronger Parent

A stronger sufficient theorem is full relative `K`-normality:

```text
T_a : F_p^m -> F_p[X]/(f_a) is injective for every packet a.
```

Equivalently, with `beta_r = F_r(zeta_a)` in the packet field,

```text
det(beta_r^(p^s))_{0 <= r,s < m} != 0.
```

This Moore determinant statement is rank-safe because it lives over the base
field packet algebra.  After adjoining `mu_m`, it can be translated to
character resolvent rank only through tensor scalar extension.

## What Is Not Enough

The following are useful diagnostics but are not formal certificates:

```text
every individual K-character resolvent is nonzero;
the 211-axis diagonalizes inside the packet field;
small CM packets show no dimension-possible rank defects.
```

Character support is weaker than rank.  Packet-field diagonalization is an
invertible coordinate chart over the packet field, but it can change the
`F_p`-span of coordinate entries.  The two warning toys are:

```text
p24/scalar_extension_rank_pitfall_toy.py
p24/packet_field_dft_rank_warning_toy.py
```

## First Missing Lemma

The first genuinely missing arithmetic lemma is a selected-prime
anti-annihilator statement:

```text
For every packet a and every nonzero w in W_axis,
f_a does not divide sum_r w(r) F_r(X).
```

The parent version replaces `W_axis` by all of `F_p^m`.

A proof has to explain why the reduced CM packet vector avoids the annihilator
subspaces coming from the selected prime `p`, not merely why a random vector
would avoid them.  Equivalently, it should prove that the relevant Moore
determinant, or its 368-dimensional axis minor, is a p-unit.

## Plausible Proof Routes

The current plausible routes are:

```text
1. group-determinant/p-unit route:
   express the axis or K-normality determinant as a product of CM resolvents
   and prove p does not divide it using a Gross-Zagier-style valuation formula
   or a selected-prime local embedding criterion;

2. class-field normality route:
   lift the packet vector to the H-character component of the ring-class field
   and prove that reduction at the p24 Frobenius prime preserves normality for
   the smooth complement layers;

3. finite-field trace route:
   prove a fixed-packet anti-concentration theorem for the CM trace vector,
   strong enough to rule out the 368-dimensional axis annihilator space.
```

The first route is the most concrete because it asks for a p-adic valuation of
one determinant.  The second is conceptually closest to the Moore determinant.
The third matches the small-data statistics but needs a new pointwise theorem,
not an average equidistribution result.

There is now a more concrete lower-dimensional sufficient determinant adjacent
to the Moore parent:

```text
p24/trace_gram_axis_certificate.md
p24/hermitian_trace_gram_axis_certificate.md
```

The ordinary version asks for nonvanishing of the `368 x 368` trace Gram matrix

```text
G_a(i,j)=Tr_{F_p[X]/(f_a)/F_p}(Y_i Y_j)
```

for the axis basis images `Y_i`.  This is not equivalent to axis injectivity
for an arbitrary proper subspace, but it is sufficient.  A broader scan found
one tiny CM full-rank axis row with degenerate ordinary trace Gram.  The
Hermitian variant

```text
H_a(i,j)=Tr(Y_i * Y_j^(p^(d/2)))
```

rescued that row and is better aligned with p24 because `d=ord_n(p)` is even
and the middle Frobenius sends the H-character to its inverse.

The Hermitian determinant does not seem to split for free.  The structure scan
in

```text
p24/hermitian_trace_gram_structure_scan.py
p24/hermitian_cross_block_rank_boundary.md
```

found no eligible rows with a difference-circulant Hermitian kernel and no
composite rows with all CRT trace-zero blocks orthogonal.  Thus this remains a
coupled p-unit determinant, not a product of independent 2-, 157-, and
211-axis determinants.

A coordinate-minor variant is recorded in:

```text
p24/axis_coefficient_minor_audit.py
p24/axis_coefficient_minor_boundary.md
```

It asks for a fixed `368 x 368` coordinate minor of the packet-reduced axis
images to be nonzero.  This would imply axis injectivity by the Lean theorem
`injective_from_projected_eval`, and small CM scans show strong leading-minor
rank.  The caveat is that these are packet-basis coordinates after reduction
modulo `f_a`, not raw short CM prefixes, and the determinant is not
origin-invariant.  So it is a finite certificate shape, but currently less
natural than the Hermitian decomposition-field norm.

## Small-Scale Falsifiers

The theorem would be falsified by any CM packet row with:

```text
deg(f) >= 368
rank(T_f | W_axis) < 368.
```

The parent theorem would be falsified by:

```text
deg(f) >= m
rank(T_f) < m.
```

Existing scans have found no dimension-possible failures in either sense.  The
next useful experiments should therefore search for a structured first failure
near the boundary, not for more random confirmation.

One fresh cheap falsifier run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 5 --min-h 24 --max-h 120 --max-abs-D 20000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 120 --q-stop 150000 \
  --max-splitting-primes 1 --include-linear --scan-origins \
  --require-deg-ge-axis-dim --random-trials 0 --summary-only
```

reported:

```text
packet_rows=386
injective_rows=386
injective_failures=0
block_internal_failure_rows=0
pair_directness_failure_rows=0
cross_directness_failure_rows=0
full_k_injective_possible_rows=386
full_k_injective_rows=386
full_k_injective_failure_rows=0
l1_zero_rows=0
rank_defect_histogram={0: 386}
```
