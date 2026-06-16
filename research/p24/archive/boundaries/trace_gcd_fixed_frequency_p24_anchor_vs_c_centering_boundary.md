# p24 Anchor Versus C/E-Centering Boundary

Date: 2026-06-07

## Point

There are two nearby but distinct conditions in the current fixed-frequency
route.

The recombined anchor says the nontrivial right spectrum of the trace defect
vanishes:

```text
D_q = Tr_relative(packet)_q - |internal| * selected_q.
```

The bidegree/internal-trace target says that, after `Tr_{B/C}`, the nontrivial
right channels have no trivial `C/E` component.  In quotient coordinates this
means the full internal trace profile itself has no nontrivial right
component.

The tempting proof shortcut is:

```text
trace-defect anchor zero
  => C/E-trivial bidegree zero.
```

This is false.

## Finite Boundary

The gate uses the exact p24 quotient dimensions:

```text
right quotient: C_7
C/E quotient:   C_179
B/C quotient:   C_31
internal size:  5549
```

It constructs packets with prescribed full internal trace and selected child
profile.  The output is:

```text
forced_anchor_pass_bidegree_fail=32/32
forced_bidegree_pass_anchor_fail=32/32
forced_anchor_and_bidegree_both_pass=32/32
```

So selected-section subtraction can make the trace defect anchor pass while
the forbidden `C/E`-trivial bidegree still leaks.  Conversely, `C/E`-centering
can hold while the section-aware anchor fails if the selected child has
nontrivial right profile.

## Consequence

Do not try to prove the bidegree theorem merely from the relative trace defect
identity:

```text
Tr_relative(j_{r+m*bullet}) - n*j_r.
```

The proof needs one of the following stronger ingredients:

```text
1. direct C/E-centering of the weighted obstruction after Tr_{B/C}; or
2. C/E-centering plus a theorem controlling the selected child right profile;
3. the full affine profile identity
   M_i(D)-388430*b_i independent of i.
```

This makes the current target slightly cleaner: the anchor and the
`C/E`-centering are distinct arithmetic inputs unless a new CM/Lang identity
ties them together.

## Check

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_anchor_vs_c_centering_boundary.py
```

The check is a small finite quotient model.  It does not enumerate CM roots.
