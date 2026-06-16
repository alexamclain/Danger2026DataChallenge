# Reduced Resolvent Normality Boundary

This note records the remaining finite-field faithfulness gap in the additive
projector obstruction, and the current toy evidence around it.

## Setup

Let a cyclic embedded CM torsor be written

```text
j_i = g^i(j_0),       0 <= i < h.
```

Form the group-algebra element

```text
J(T) = sum_i j_i T^i in F_q[T]/(T^h - 1).
```

Evaluating `J(T)` at `h`-th roots of unity gives the class-character
resolvents

```text
T_chi = sum_i chi(g)^i j_i.
```

Thus

```text
gcd(J(T), T^h - 1)
```

records exactly which class-character packets vanish after reduction.  If the
gcd has degree `0`, then the translates of `j` are a normal basis for the
reduced torsor and any additive group-algebra identity

```text
L*j = e_H*j
```

forces `L=e_H`.  This is the reduced normality hypothesis used by

```text
p24/structural_lifting_support_lemma.md
p24/finite_field_selector_degree_theorem.md
```

## New Toy Scan

I added:

```text
p24/reduced_resolvent_vanishing_scan.py
```

It scans complete small CM torsors, finds a splitting prime `q`, finds a split
prime ideal whose horizontal isogeny graph is a full cycle, and computes:

```text
gcd(J(T), T^h - 1) over F_q
```

as well as explicit quotient DFT support when `F_q` contains the required
roots of unity.

Runs:

```text
python3 p24/reduced_resolvent_vanishing_scan.py \
  --max-cases 12 --min-h 12 --max-h 96 --max-abs-D 12000

python3 p24/reduced_resolvent_vanishing_scan.py \
  --max-cases 40 --min-h 12 --max-h 140 --max-abs-D 24000
```

Results:

```text
12-row scan:
  normal_rows=12
  nonnormal_rows=0
  quotient_dft_rows_with_roots=15
  quotient_dft_full_support_rows=15

40-row scan:
  normal_rows=40
  nonnormal_rows=0
  quotient_dft_rows_with_roots=46
  quotient_dft_full_support_rows=46
```

So in these complete toy cycles, p-specific reduced character vanishing did
not occur.  Whenever the quotient roots of unity lived in the base field, all
quotient-character traces were nonzero.

The older normal-basis support toy agrees:

```text
python3 p24/normal_basis_support_toy.py --max-cases 8 --min-h 12 --max-h 96
```

Every reported row had `gcd_degree=0`, so the support lower bound was faithful
in those examples.

## Actual small CM failures

Reduced normality is not automatic for every split ordinary CM row.  The
focused audit

```text
p24/reduced_normality_failure_audit.py
```

found:

```text
D=-216 q=103 ell=5 h=6 gcd_degree=1 zero_order=3 quotient_failure=3/2/2
D=-300 q=139 ell=7 h=6 gcd_degree=1 zero_order=2 quotient_failure=2/3/1
```

So the clean theorem cannot be a broad statement about all split CM
reductions.  These failures are low-order degree-1 packet accidents; the
larger scans with `h >= 12` still found no failures.  For p24, the hard
unproved part remains the high-order non-genus `157` and `211` packet
nonvanishing, or an equivalent cyclic-code support lower bound.

The failure rows also do not produce sparse additive projectors.  The audit

```text
p24/failure_projector_weight_audit.py
```

computes `min wt(e_H+Ann(J))` exactly in the two failure rows.  For every
nontrivial quotient of the `h=6` class cycle, the minimum equals the original
projector support.  Thus the additive no-go theorem can target the weaker
minimum-weight condition rather than full normality.

## What This Means For p24

For the third p24 target, reduced normality would imply that any additive
oriented Hecke formula producing the desired subgroup period has support at
least

```text
|H| = 3107441.
```

For the first-trace order-19 toy target, the support lower bound would be

```text
14670196166.
```

The characteristic-zero singular modulus is already normal by the
dominant-conjugate estimate in

```text
p24/singular_moduli_normality_bound.py
```

but proving reduced normality modulo the single p24 split prime would require
showing

```text
p does not divide Norm(T_chi)
```

for every relevant high-order class character.

## Boundary

The toy evidence points away from a helpful p-specific collapse: reduced
normality appears generic in small split CM cycles, including non-genus
quotient rows.  But it does not prove the p24 case.

Known easy lifting is insufficient.  The height audit

```text
p24/finite_field_lifting_height_audit.py
```

shows that the complex singular-modulus heights are astronomically larger
than `log p`, so a naive norm-divisibility argument cannot rule out one-prime
vanishing.

Known explicit norm/valuation formulas are also not enough as currently
available.  Gross-Zagier style formulas control norms of differences of
singular moduli, and related arithmetic intersection formulas control certain
global products or toric period norms.  They do not presently give a
sub-sqrt way to certify all high-order non-genus linear resolvents

```text
T_chi = sum_g chi(g) j_g
```

modulo this one split prime.  Inserting the character `chi` is exactly the
same odd `157`/`211` period primitive.

So the reduced-normality status is:

```text
toy evidence: strong normality for h>=12 rows tested;
small counterexamples: low-order h=6 CM packet vanishings exist;
target proof: still missing for p24 high-order non-genus packets;
constructive shortcut from vanishing: no evidence;
negative theorem: projector support bound conditional on this nonvanishing.
```
