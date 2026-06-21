# P27 U+2 Norm/Coboundary Screen

Date: 2026-06-21

## Claim

The `u+2` gate has exact norm identities across the two `s^2=d` branches, but
the selected `w`-square branch's `u+2` bit is not visible in the small
norm/branch character span.

This sharpens the remaining moonshot: the obstruction is an orientation or
Hilbert-90 class on the halving double cover, not a missing visible norm
factor.

## Identities

For one Montgomery halving step:

```text
d = x^2 + A*x + 1
s^2 = d
u_+ = 2(x+s)
u_- = 2(x-s)
```

The next x-square gate is:

```text
chi(u + 2)
```

The two `s` branches satisfy:

```text
Norm_s(u+2) = 4*x*(2-A)
Norm_s(u-2) = -4*x*(A+2)
Norm_s(u^2-4) = 16*x^2*(A^2-4)
```

On nonsplit rows, `chi(A^2-4)=-1`, so exactly one `s` branch has
`w=u^2-4` square.  The question is whether the selected branch's
`chi(u+2)` is visible from the norm data.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_usquare_norm_coboundary_probe.py \
  --target 30000 \
  --max-draws 6000000 \
  | tee research/p27/archive/probe_outputs/p27_usquare_norm_coboundary_probe_20260621.txt
```

Screened features:

```text
x, x-1, x+1,
A-2, A+2, 2-A, -A-2,
x*(2-A), -x*(A+2), A2-4
```

These are the natural local branch and norm characters from the identities
above.

## Result

Input sample:

```text
sampled_pairs = 30000
x_draws = 235889
candidate_invalid_not_nonsplit = 59140
compact_not_target = 58926
pair_incomplete = 29570
```

All norm identities and selected-branch consistency checks passed:

```text
norm_identity_stats = none
```

d2-to-d3 selected `u+2` span:

```text
rows = 30000
exact_combo = none
best = 15054/30000 = 0.501800000
```

d3-to-d4 selected `u+2` span:

```text
rows = 15004
exact_combo = none
best = 7540/15004 = 0.502532658
```

The best combinations are indistinguishable from noise at this scale.

## Interpretation

Positive:

```text
The norm identities are exact and explain why exactly one w branch exists.
The correct object is now sharply identified: the selected branch orientation
of chi(u+2), not the norm of u+2.
```

Negative:

```text
The selected u+2 bit is not a product of the local norm/branch characters.
The visible A,x norm data does not give a cheap selector for d3 or d4.
```

## Consequence

The immediate route:

```text
derive chi(u_j+2) from local norm characters of A and x_j
```

is killed.

The remaining route must use orientation data:

```text
Hilbert-90/cocycle class selecting the w-square branch
theta/Kummer relation coupling several selected orientations
low-genus source for the all-plus orientation locus
```

Follow-up selected-orientation span screen:
[P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md).
That screen allowed selected `s`-branch orientation characters from the whole
successful prefix through gates 3-6.  It also found no exact GF(2) product for
the next `u+2` bit on two 30,000-row seeds.  Thus the surviving orientation
route is not a small visible product; it must be a source/quotient on the
iterated cover.

## Concrete Next Tests

1. Symbolic H90 orientation test:

```text
Express selected chi(u+2) as a cocycle on the d-cover with deck s -> -s.
The first small GF(2) selected-orientation product screen is now negative;
continue only with a non-visible quotient/source, not another similar product
scan.
```

2. Low-genus all-plus source test:

```text
Use the reverse-doubling source equations already screened for density, and
compute whether any quotient stays low-genus.
```

3. GPU test remains practical:

```text
Use chi(u+2) only as a possible pre-sqrt(w) fixed-prefix cost optimization.
Do not expect norm factors to remove the 1/2 loss.
```

## Continue / Kill

```text
continue = non-visible H90/theta quotient on the iterated cover
continue = Sage/Magma quotient/genus test for the reverse-doubling source
continue = low-genus quotient/source for all-plus iterated 2-cover

kill = local A,x norm-character selector for selected u+2
kill = small selected-orientation GF(2) product at the screened feature depth
kill = expecting reverse-doubling density alone to beat random half-loss
kill = expecting compactD to bias the visible norm span
kill = fixed-prefix u+2 filtering as sqrt-beating
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_usquare_norm_coboundary_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_usquare_norm_coboundary_probe_20260621.txt`
- Related: [P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md)
- Related: [P27 U+2 Sequence Recurrence Screen](p27_usquare_sequence_recurrence_20260621.md)
- Related: [P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md)
- Related: [P27 Reverse-Doubling Source Screen](p27_reverse_doubling_source_screen_20260621.md)
- Related: [P27 Nonsplit W-Obstruction Identity](p27_nonsplit_w_obstruction_identity_20260621.md)

```text
p27_usquare_norm_coboundary_rows=1/1
```
