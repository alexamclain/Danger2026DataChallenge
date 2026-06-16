# RS-Tail Fixed-Frequency Ordinary Gate

Date: 2026-06-06

## Point

The support accounting leaves a precise fork.  For p24, Frobenius-stable
defect supports of size `16` are either:

```text
0 fixed frequencies + 4 length-4 moving orbits:   35 choices;
4 fixed frequencies + 3 length-4 moving orbits:   1225 choices.
```

The frequency-resultant route becomes much cleaner if the second type is
impossible.  The missing input is not another global rank computation; it is a
fixed-frequency local theorem.

## Local Theorem

Let `a in 5Z/35Z` be one of the seven fixed frequencies.  Let `P_a` be the
local prefix projection at frequency `a`, and let `tau_a` be the tail local
value modulo the prefix image.

The fixed-frequency ordinary statement is:

```text
rank(P_a, tau_a) = rank(P_a)
```

for every fixed frequency `a`.  Equivalently, the tail value lies in the
prefix image at every fixed frequency, so no fixed frequency contributes a
defect line.

Together with:

```text
defect support is Frobenius-stable;
defect support has size 16;
```

this forces the defect support to be a union of four length-4 moving orbits.
The selector choices then drop from `1260` to `35`.

## Why This Is The Right Extra Lemma

The mixed case is not rejected by descent, and it is not rejected by the tail
Vandermonde factor.  A mixed support with four fixed frequencies and three
moving orbits is Frobenius-stable, has size `16`, and still has a nonzero
Fourier/Vandermonde determinant because the sixteen selected `35`th roots are
distinct and `p` does not divide `35`.

So the extra theorem must use arithmetic of the fixed-frequency prefix/tail
local values.  It cannot be replaced by support bookkeeping alone.

## Check

The finite gate is:

```text
p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.py
```

It checks:

```text
pure moving support:
  fixed ordinary + descent => one of 35 pure length-4 supports;

mixed fixed support control:
  descent and Vandermonde still pass, but fixed ordinary fails;

nonstable support control:
  rejected by the descent/support condition.
```

## Next Arithmetic Target

Prove, from the CM/Lang construction of the fixed RS-tail map, that for all
fixed frequencies:

```text
tau_a in image(P_a).
```

In the existing notation this should be a fixed-frequency Hilbert-90/trace
adjoint identity, not a numerical rank scan over the class set.

The trace-adjoint form is isolated in:

```text
p24/trace_gcd_fixed_frequency_annihilator_bridge.md
```

It rewrites the same target as
`Ann(V_{a,2},V_{a,3},V_{a,5},V_{a,6}) subset Ann(V_{a,1})`.
