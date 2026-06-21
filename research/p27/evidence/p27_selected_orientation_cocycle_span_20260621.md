# P27 Selected Orientation/Cocycle Span Screen

Date: 2026-06-21

## Claim

The selected-branch orientation characters from the successful halving prefix
do not give an exact GF(2) product formula for the next selected `u+2` bit.

This kills the simplest finite-field version of the H90/cocycle hope:

```text
chi(u_j+2) = product of visible local characters and selected s-branch
orientation characters from the prefix.
```

The remaining H90 route must be a more structural quotient/source on the
iterated cover, not another small character-span scan.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_selected_orientation_cocycle_probe.py \
  --target 30000 \
  --max-draws 6000000 \
  --max-target-gate 6 \
  | tee research/p27/archive/probe_outputs/p27_selected_orientation_cocycle_probe_20260621.txt
```

Replication command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_selected_orientation_cocycle_probe.py \
  --target 30000 \
  --seed 20260622 \
  --max-draws 6000000 \
  --max-target-gate 6 \
  | tee research/p27/archive/probe_outputs/p27_selected_orientation_cocycle_probe_seed20260622_20260621.txt
```

At each selected halving step, the probe records local characters:

```text
x, x-1, x+1, A-2, A+2, 2-A, -A-2,
x*(2-A), -x*(A+2), A^2-4
```

and selected-branch orientation characters:

```text
s_sel, s_other, u_sel, u_other,
x+s_sel, x-s_sel, A+s_sel, A-s_sel,
s_sel+1, s_sel-1, u_sel+A, u_sel-A, u_other+A, u_other-A.
```

It intentionally excludes `u_sel+2` and `u_sel-2`, since those are the target
character on the successful `w` branch.

For gate `g`, the screen allows the whole successful prefix up to `g` in the
GF(2) span.  Thus the gate-4 target may use gate-3 orientation data plus
gate-4 local/orientation data, and so on.

## Main Result

Seed `20260621`:

```text
gate  rows   plus_rate   exact_combo   best_weight<=3
3     30000  0.500133333 none          15400/30000 = 0.513333333
4     15004  0.497467342 none           7848/15004 = 0.523060517
5      7464  0.496516613 none           3942/7464  = 0.528135048
6      3706  0.500269833 none           2018/3706  = 0.544522396
```

Independent seed `20260622`:

```text
gate  rows   plus_rate   exact_combo   best_weight<=3
3     30000  0.505466667 none          15302/30000 = 0.510066667
4     15164  0.497230282 none           7932/15164 = 0.523080981
5      7540  0.507161804 none           3980/7540  = 0.527851459
6      3824  0.486401674 none           2088/3824  = 0.546025105
```

No anomalies appeared on either run.

The small best low-weight lifts are not promoted:

```text
the exact GF(2) solver found no product relation
the named best products do not replicate as the same product across seeds
the later-gate best scores are in small conditioned samples after many tests
```

## Interpretation

Positive:

```text
The selected branch orientation is now tested directly, not only through
visible A,x norm characters.
```

Negative:

```text
The next u+2 bit is not a small product of local characters plus selected
s-branch orientation characters from the prefix.
```

## Reverse-Doubling Source Target

The next concrete source test should reverse the x-square gate through the
Montgomery doubling map.

For one Montgomery halving step, if

```text
x_next + 1/x_next = u
```

then the previous x-coordinate is the double of `x_next`:

```text
x = (x_next^2 - 1)^2 / (4*x_next*(x_next^2 + A*x_next + 1)).
```

Therefore the all-plus condition `chi(x_next)=+1` can be sourced by writing

```text
x_next = z^2
x = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1)).
```

This reframes the next moonshot test:

```text
intersect the label-2 / compactD source with the reverse-doubled square source
and ask whether the resulting all-plus cover has a low-genus quotient or cheap
walk.
```

This is a better next target than more finite products of visible characters.

## Concrete Next Tests

1. Sage/Magma source-cover test:

```text
Substitute x_next=z^2 into the Montgomery doubling formula and intersect with
the label-2 compactD=-1 equations.  Compute genus, components, and low-degree
quotients for the resulting d3 all-plus source.
```

2. Finite-field source-density test:

```text
Over several split small primes, count points on the reverse-doubled
compactD/d3 source and compare with the random 1/2 cover expectation.  Promote
only if the counts suggest a low-genus quotient or decomposed source.
```

3. GPU telemetry only if algebra names a source:

```text
Do not implement the low-weight orientation products as filters.  If GPU logs
orientation columns, use them only as diagnostics unless a product relation
replicates out-of-sample.
```

## Continue / Kill

```text
continue = reverse-doubling all-plus source construction
continue = Sage/Magma genus and quotient test for the d3 square-source cover
continue = non-visible H90/theta quotient on the iterated 2-cover

kill = small GF(2) product of selected orientation characters as the next bit
kill = promoting the weak low-weight in-sample lifts without a named theorem
kill = more local selected-s character scans at the same feature depth
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_selected_orientation_cocycle_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_selected_orientation_cocycle_probe_20260621.txt`
- Replication output: `research/p27/archive/probe_outputs/p27_selected_orientation_cocycle_probe_seed20260622_20260621.txt`
- Related: [P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md)
- Related: [P27 U+2 Sequence Recurrence Screen](p27_usquare_sequence_recurrence_20260621.md)
- Related: [P27 X-Square / 2-Descent Gate](p27_xsquare_2descent_gate_20260621.md)

```text
p27_selected_orientation_cocycle_span_rows=1/1
```
