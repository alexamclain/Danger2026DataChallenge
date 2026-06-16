# Trace-GCD Prefix Subcode Distance Boundary

Date: 2026-06-06

This note records the coding-theory translation of the metric prefix-Gram
obstruction.

## Prefix Subcode

Let `S` be one p24 four-orbit prefix on the nonzero right frequencies:

```text
S subset (Z/211Z)^*,        |S| = 4*35 = 140,
T_nonzero = (Z/211Z)^* \ S, |T_nonzero| = 70.
```

Let `G_s in L=F_p(mu_157)` denote the metric-aware trace-GCD right-coordinate
field values.  Define:

```text
U_S = span_Fp{G_s : s in S}.
```

The bad prefix-Gram event is:

```text
U_S cap U_S^perp != 0
```

under `<x,y> = Tr_{L/F_p}(xy)`.

Equivalently, there is a nonzero `lambda in U_S` such that the scalar trace
word:

```text
w_lambda(s) = Tr(lambda * G_s)
```

vanishes on every `s in S`.  Therefore the nonzero-coordinate word
`w_lambda|_(Z/211Z)^*` is supported inside `T_nonzero`, which has size `70`.

If one extends the scalar word to all of `Z/211Z` in order to use prime cyclic
uncertainty, there is one additional zero-frequency coordinate.  Then the
complement size is at most:

```text
|Z/211Z \ S| = 71.
```

The nonzero-coordinate code and the prime-cyclic uncertainty code therefore
have slightly different distance thresholds.

## Distance Theorem Equivalent

Define the prefix trace subcode:

```text
C_S^* = { (Tr(lambda * G_s))_{s in (Z/211Z)^*} : lambda in U_S }.
```

Then the prefix Gram theorem is implied by the support-specific distance
statement:

```text
For every nonzero lambda in U_S,
w_lambda|_(Z/211Z)^* is not supported inside T_nonzero.
```

A stronger sufficient theorem is:

```text
On the 210 nonzero right coordinates,
every nonzero parameter word has Hamming support at least 71.
```

This would make a self-orthogonal prefix vector impossible, because such a
vector gives a nonzero word supported on at most `70` nonzero right
coordinates.

This should be read as a parameter-level statement.  The set-theoretic slogan
`C_S cap F_p^T = {0}` is safe only if the trace-word map is injective on
`U_S`, or if the statement is formulated directly in terms of nonzero
`lambda`.  The Lean gate below uses the parameter-level version.

## Uncertainty Form

If the condition `lambda in U_S` could be upgraded to an honest cyclic Fourier
support bound:

```text
Fourier support(w_lambda) <= 140,
```

then prime cyclic uncertainty on `Z/211Z` would give:

```text
support_time(w_lambda) + support_frequency(w_lambda) >= 212.
```

A bad word would have:

```text
support_time <= 71,
support_frequency <= 140,
```

which sums to `211`, a contradiction.

The catch is exactly the missing arithmetic theorem: the tested CM row spaces
are not generic cyclic codes, and the prefix span condition is not automatically
a Fourier support condition for the scalar trace word.

## Existing Boundaries

The generic shortcuts are already demoted:

```text
p24/centered_marginal_cyclic_code_boundary.md
p24/centered_marginal_plateau_uncertainty_boundary.md
p24/cyclic_code_min_weight_counterexample.py
p24/lang_trace_gcd_crossed_weight_spectral_boundary.md
p24/opposite_prefix_gram_boundary.md
p24/kernel_tail_schur_identity_boundary.md
p24/trace_gcd_selected_erasure_vs_global_distance.md
```

They rule out ordinary cyclic-code, plain uncertainty, and prefix-rank-only
arguments.  They do not rule out the actual p24 support-specific theorem:

```text
For the actual metric trace-GCD prefix subcodes C_S,
no nonzero lambda in U_S has trace word supported inside T_nonzero.
```

But this is essentially the selected-prime p-unit theorem in coding language.
Full distance is a sufficient strengthening, not an equivalent requirement.
The selected-erasure/global-distance separation is documented in the note above.

## Lean Gate

The finite support implication is recorded in:

```text
p24/lean/PrefixSubcodeDistanceGate.lean
p24/lean/PrefixGramErasureBridgeGate.lean
```

It checks:

```text
nonzero-coordinate distance >= 71
and prefix vanishing => nonzero-coordinate support <= 70
  => no nonzero prefix parameter vanishes on the prefix;

prime-cyclic uncertainty threshold 212
and time support <= 71
and frequency support <= 140
  => no bad prefix+frequency parameter.
```

The second implication isolates the exact missing arithmetic hypothesis: prove
that `lambda in U_S` gives the promised Fourier-support bound for the actual
trace-GCD family.

The bridge gate records why this is the same finite obstruction as the metric
prefix Gram: a nonzero prefix parameter vanishing on the prefix is exactly a
self-orthogonal prefix vector.

## Bounded Test

The current smallest actual-CM falsifier should be run in metric-aware mode:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 1 --max-cases 8 --max-abs-D 30000 \
  --q-stop 120000 --max-origin-shifts 40
```

Any genuine actual-CM row with `prefixGram0>0` in this metric-aware mode would
seriously narrow or kill the Gram/support theorem.  The current bounded row has
`prefixGram0=0`, so it remains a positive plumbing check only.
