# Trace-Frame Sum-Rank Erasure Theorem

Date: 2026-06-05

This note records the coding-theory strengthening suggested by the
trace-frame flag formulation.

## Code View

Use the notation:

```text
E = F_p(mu_m)
C/E has degree 179
B/C has degree 31
B = C(theta)
```

Multiplication by `g'(theta)` and expansion in the `C`-basis

```text
1, theta, ..., theta^30
```

identifies `B` with `C^31` as an `E`-vector space.  The p24 axis image

```text
W_axis(B) subset B
```

therefore becomes an `E`-linear code:

```text
W_axis(B) subset C^31,
dim_E W_axis(B) = 368.
```

Each coordinate block has `E`-dimension `179`.

The trace-frame theorem keeps the top three blocks.  It says that the
projection:

```text
pi_top3 : W_axis(B) -> C^3
```

is injective.

## Stronger Erasure Theorem

The natural sum-rank strengthening is:

```text
for every 3-subset I of {0,...,30},
pi_I : W_axis(B) -> C^I is injective.
```

Equivalently, no nonzero codeword of `W_axis(B)` is supported on any `28`
relative coefficient blocks.

In rank-support terms, this would follow from:

```text
d_sumrank(W_axis) > 28 * 179 = 5012.
```

The Singleton bound for an `E`-linear code in the ambient space `C^31` is:

```text
d <= 31*179 - 368 + 1 = 5182.
```

So the needed distance `5013` is below the MSRD maximum but close enough that
an LRS/MSRD-style proof would be more than sufficient.

The exact accounting is recorded in:

```text
p24/trace_frame_sum_rank_erasure_accounting.py
p24/trace_frame_sum_rank_erasure_accounting.md
```

It reports:

```text
three_block_subset_count=4495
singleton_distance=5182
needed_distance=5013
distance_slack=169
```

The random-subspace union bound over all `4495` projections still has
logarithm about:

```text
log10(failure) ~= -2.227680e7.
```

So this theorem is useful as a structural proof import, not as evidence from
generic rank behavior.

This is stronger than the current p24 certificate, which only needs the
specific top-three projection.  But it is a cleaner imported theorem:

```text
W_axis(B) is a high-distance sum-rank code in the relative coefficient
decomposition B ~= C^31.
```

## Small Audit

I added:

```text
p24/tensor_factor_relative_block_erasure_audit.py
```

It tests all dimension-sufficient relative coefficient block subsets in small
tensor rows.

Pinned targeted run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_relative_block_erasure_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-subsets 1000
```

reported:

```text
rows=5
targets=44
subset_tests=102
subset_failures=0
top_failures=0
```

The useful nontrivial toy cases include:

```text
m=4, axis raw_rank=4, subdegree=2, relative_degree=3:
  all 2-of-3 relative coefficient block projections have rank 4.

m=12, constant_plus_4 raw_rank=4, subdegree=2, relative_degree=3:
  all 2-of-3 projections have rank 4.
```

Thus in the pinned tensor analogue, the top blocks are not visibly special:
every dimension-sufficient block set recovers.

## Random Baseline

I added a matching random-shape calibration:

```text
p24/tensor_factor_relative_block_erasure_random_baseline.py
```

For the small `D=-10919` shapes over the same `q=11243`, degree-2 extension,
`200` random trials per shape reported:

```text
raw_rank=6, relative_degree=3, subdegree=2: failures=0/200
raw_rank=4, relative_degree=3, subdegree=2: failures=0/200
raw_rank=3, relative_degree=3, subdegree=2: failures=0/200
raw_rank=6, relative_degree=2, subdegree=3: failures=0/200
raw_rank=4, relative_degree=2, subdegree=3: failures=0/200
raw_rank=3, relative_degree=2, subdegree=3: failures=0/200
```

So the small block-erasure audit is a consistency check, not evidence of a
hidden low-complexity identity.  The productive theorem remains arithmetic:
prove the p24 relative coefficient code is genuinely high-distance, or prove
the selected top-three erasure coordinate is a p-unit.

## LRS Signature Boundary

I also checked whether the natural relative coefficient generator matrix has
an obvious LRS/MSRD signature:

```text
p24/tensor_factor_relative_block_structure_audit.py
p24/trace_frame_lrs_signature_boundary.md
```

For the pinned `D=-10919, m=12` axis analogue, both `subdegree=2` and
`subdegree=3` cases matched random controls exactly for:

```text
block rank histograms,
pair block rank histograms,
Toeplitz/Hankel/cyclic displacement ranks.
```

In particular, the flattened displacement ranks were maximal:

```text
toeplitz=hankel=cyclic_toeplitz=cyclic_hankel=6.
```

So the natural coefficient matrix is not visibly Toeplitz, Hankel, cyclic, or
LRS-like in a simple basis.  A sum-rank proof would need a non-obvious
class-field block equivalence, not an off-the-shelf low-displacement
identification.

## p24 Meaning

For p24, the top-three theorem is:

```text
W_axis(B) cap span_C{e_0,...,e_27} = {0}
```

after ordering coefficient blocks from low to high degree.  The sum-rank
strengthening would instead say:

```text
W_axis(B) cap C^J = {0}
```

for every `28`-block coordinate subset `J`.

This converts the trace-frame problem from one Schubert coordinate into a
minimum-distance theorem for a 31-block `E`-linear code.

## Boundary

This does not by itself prove p24.  Existing random-rank and CS audits warn
that small-field erasure success is often generic.  To become a certificate,
one still needs one of:

```text
1. an explicit block-equivalence between W_axis(B) and a known LRS/MSRD code;
2. a selected-prime p-unit proof for the required erasure Plucker coordinate;
3. a class-field identity proving the relative coefficient code has
   distance at least 5013.
```

The existing Lean file:

```text
p24/lean/MSRDSupportGate.lean
```

is metric-agnostic and can carry the finite implication once the arithmetic
work supplies a genuine sum-rank support model.  The hard part is proving
that the actual p24 CM axis code has the required distance or selected
erasure p-unit.
