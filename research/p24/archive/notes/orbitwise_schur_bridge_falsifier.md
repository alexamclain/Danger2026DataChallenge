# Orbitwise Schur Bridge Falsifier

Date: 2026-06-05

This note records a bounded side experiment suggested by a synthesis sidecar:
can the trace-GCD tail-on-kernel determinant be moved into Hermitian/Gram
packet-norm objects orbitwise?

## Finite Identity

For a prefix matrix `A`, selected tail matrix `B`, and kernel basis `N` for
`ker A`, the finite Schur identity is:

```text
det([A;B][A;B]^T) det(N^T N)
  = det(A A^T) det(BN)^2.
```

If the three Gram determinants are p-units, then the trace-GCD determinant
`det(BN)` is a p-unit.  This is a stronger route than the direct trace-GCD
determinant theorem, because a full-rank finite-field subspace can have
singular Gram form.

## Tool

Added:

```text
p24/orbitwise_schur_bridge_falsifier.py
```

It uses actual small-CM trace-GCD rows.  In metric-aware mode it computes:

```text
Pi_t = det(B_t | ker A_t),
P_t  = det(A_t G^{-1} A_t^T),
L_t  = det([A_t;B_t] G^{-1} [A_t;B_t]^T),
K_t  = det(N_t^T G N_t),
```

where `G` is the trace-pairing matrix in the selected subfield basis.  Without
`--metric-aware`, the script uses ordinary coordinate dot products, which are
useful for finite plumbing checks but not the invariant arithmetic payload.

then checks both pointwise and Frobenius-orbit product forms:

```text
L_t K_t = P_t Pi_t^2,
prod_O L_t * prod_O K_t = prod_O P_t * (prod_O Pi_t)^2.
```

## Pinned Trace-GCD Row

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail --max-origin-shifts 140
```

Output summary:

```text
D=-13319 q=13463 h=140 m=28 n=5 pair=(4,7) right_lengths=[3,3]
records=280

omitted=0:
  tail_zero=0 schur_fail=0
  prefixGram0=0 fullGram0=0 kernelGram0=0
  tailNonzeroButSomeGram0=0
  all right_class_mismatches=0
  orbitSchur=1 for [0], [1,2,4], [3,6,5]

omitted=1:
  tail_zero=0 schur_fail=0
  prefixGram0=0 fullGram0=0 kernelGram0=0
  tailNonzeroButSomeGram0=0
  all right_class_mismatches=0
  orbitSchur=1 for [0], [1,2,4], [3,6,5]
```

This supports the finite Schur bridge and the reduced right-orbit descent on
the known actual-CM row.  However, this pinned row has `prefix_len=0`, so it
is a tail-only stress test, not a genuine prefix-Gram p-unit test.

## Nonzero-Prefix Calibration

A bounded nonzero-prefix run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --include-linear --max-factor-degree 12 --max-extension-degree 12 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 3 --max-cases 20 --max-abs-D 90000 \
  --q-stop 600000 --max-origin-shifts 80
```

found three tiny `L=2` rows, all with:

```text
tail_zero=0
schur_fail=0
right_class_mismatches=0
orbitSchur=1
```

These rows check the plumbing but are still too small to justify a p24-scale
Hermitian theorem.

The latest small bounded run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 1 --max-cases 8 --max-abs-D 30000 \
  --q-stop 120000 --max-origin-shifts 40
```

found:

```text
D=-2159 q=3923 h=60 m=20 n=3
pair=(4,4) left=1:L2 right_lengths=[2,1]
tail_zero=0
schur_fail=0
prefixGram0=0
fullGram0=0
kernelGram0=0
right_class_mismatches=0
orbitSchur=1
```

The metric-aware orbit products differ from the ordinary-dot run, as they
should, but the Schur identity and nonzero factors remain clean.  This is
another positive finite-plumbing check with nonzero prefix, not a large-shape
arithmetic proof.

An expanded metric-aware run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 4 --max-cases 30 --max-abs-D 60000 \
  --q-stop 250000 --max-origin-shifts 60
```

found four actual small-CM rows, again all with:

```text
tail_zero=0
schur_fail=0
prefixGram0=0
fullGram0=0
kernelGram0=0
tailNonzeroButSomeGram0=0
right_class_mismatches=0
orbitSchur=1
```

The rows were small (`D=-2159`, `h=60`, with `L=2` left-orbit blocks), so the
run is still a falsifier/consistency check rather than p24 evidence at scale.
Its value is that the metric-aware identity and right-class descent continue
to survive actual-CM rows with nonzero prefix.

A slightly harder search with:

```text
--min-left-orbit-len 3 --min-prefix-len 1
```

was again stopped after about 35 seconds with no output.  That is a
row-discovery boundary, not mathematical evidence.

## Consequence

The orbitwise Schur bridge remains alive but stronger than necessary.

The finite implication is now Lean-checked in:

```text
p24/lean/TraceGcdSchurBridgeGate.lean
```

It records:

```text
Schur zero-detection:
  Pi_O = 0 => L_O = 0 or K_O = 0

prefix Gram p-unit gives K_O != 0
full Gram p-unit gives L_O != 0
  => Pi_O != 0 for every orbit O
  => every local Delta(t) != 0
```

So the natural minimal Gram-product payload is:

```text
P_O, P_O_inv, L_O, L_O_inv for seven orbits
```

for `28` base-field elements.  The conservative payload also carries the
kernel Gram products:

```text
P_O, P_O_inv, L_O, L_O_inv, K_O, K_O_inv for seven orbits
```

for `42` base-field elements.  Both are far below `sqrt(p)`.

Useful theorem candidate:

```text
prove orbit products of metric prefix Gram and metric full Gram determinants are p-units
for the actual p24 trace-GCD row, with kernel Gram p-unit deduced from the
prefix Gram/nondegenerate-complement theorem;
then use the Schur identity to prove the seven trace-GCD orbit products.
```

Risk:

```text
the Gram p-unit theorem may be strictly harder than the direct Fitting-unit
theorem, because Gram nondegeneracy is not implied by trace-GCD rank.
```

So this is a proof-facing bridge to Hermitian packet/autocorrelation norms,
not a replacement for the current crossed-product/Fitting unit target.
