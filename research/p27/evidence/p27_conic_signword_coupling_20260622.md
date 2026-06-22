# P27 Conic Sign-Word Coupling Probe

Date: 2026-06-22

## Claim

The repeated conic-chain signs do not show a stable p27 coupling in the
bounded CPU telemetry.

The exact recurrence remains valuable:

```text
A = 2 - c^2
x_j = r_j^2
s_j = chi(r_j^2 + c*r_j + 1)
```

But the all-plus prefix profile on p27 train/heldout thins like independent
half-gates through the range with meaningful counts.  Small guard fields show
striking all-plus plateaus, but the plateau and kill gates vary by field, so
they look like finite-field artifacts rather than a transferable p27 law.

This weakens GPU sign-word bucket hunting as the next move.  GPU remains useful
for bounded confirmation at much larger scale, but the first-class moonshot
still needs a legal-pullback sampler, quotient, or CAS-normalized tower
structure.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_signword_coupling_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_signword_coupling_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_conic_signword_coupling_probe_q1607_q1847_q2087_p27_depth14_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_signword_coupling_probe.py \
  --small-primes 607 \
  --p27-target 0 \
  --p27-heldout-target 0 \
  --max-depth 6 \
  | tee research/p27/archive/probe_outputs/p27_conic_signword_coupling_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_signword_coupling_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 4000 \
  --p27-heldout-target 4000 \
  --max-draws 3000000 \
  --max-depth 14 \
  | tee research/p27/archive/probe_outputs/p27_conic_signword_coupling_probe_q1607_q1847_q2087_p27_depth14_20260622.txt
```

## P27 Results

The p27 sample uses `4000` train and `4000` heldout unique `(A,x5)` rows.

Train all-plus prefix:

```text
depth 1: 1968 / 4000, scaled = 0.984
depth 2: 1020 / 4000, scaled = 1.020
depth 3:  484 / 4000, scaled = 0.968
depth 4:  238 / 4000, scaled = 0.952
depth 5:  126 / 4000, scaled = 1.008
depth 6:   68 / 4000, scaled = 1.088
depth 7:   32 / 4000, scaled = 1.024
depth 8:   14 / 4000, scaled = 0.896
depth 9:    6 / 4000, scaled = 0.768
depth 10:   0 / 4000
```

Heldout all-plus prefix:

```text
depth 1: 2010 / 4000, scaled = 1.005
depth 2:  982 / 4000, scaled = 0.982
depth 3:  466 / 4000, scaled = 0.932
depth 4:  238 / 4000, scaled = 0.952
depth 5:  108 / 4000, scaled = 0.864
depth 6:   70 / 4000, scaled = 1.120
depth 7:   32 / 4000, scaled = 1.024
depth 8:   16 / 4000, scaled = 1.024
depth 9:    4 / 4000, scaled = 0.512
depth 10:   4 / 4000, scaled = 1.024
depth 11:   2 / 4000, scaled = 1.024
depth 12:   2 / 4000, scaled = 2.048
depth 13:   2 / 4000, scaled = 4.096
depth 14:   2 / 4000, scaled = 8.192
```

The late heldout tail has only two rows.  It is not evidence of a stable
recurrence without a named invariant or much larger heldout confirmation.

## Guard Fields

The exact small fields reproduce the familiar local-tail warning:

```text
q1607 unique_ax = 196:
  depth1/depth2/depth3 = 112/76/76
  depth4 = 0

q1847 unique_ax = 252:
  depth1/depth2 = 180/76
  depth3 = 0

q2087 unique_ax = 228:
  depth1/depth2/depth3/depth4/depth5 = 100/72/72/72/72
  depth6 = 0
```

The plateaus are real in their fields, but their stopping gates disagree.
They should not be promoted as a p27 law.

## Interpretation

Positive:

```text
The recurrence-coordinate sign telemetry is now a named, repeatable CPU probe.
It matches the B-line prefix read: small-field plateaus exist, but p27 itself
does not currently show source shrink through useful counts.
```

Negative:

```text
No stable sign-word coupling is visible in p27 train/heldout.
No GPU bucket candidate follows from short all-plus words alone.
Small-field plateaus remain finite-field artifacts unless a theorem explains
and transfers them.
```

## Continue / Kill

```text
continue = staged legal-pullback normalization of the conic-chain Kummer tower
continue = GPU recurrence telemetry only as bounded larger-scale confirmation
continue = direct legal-pullback sampler if a quotient/source map is found

kill = GPU sign-word bucket hunting from the current CPU evidence
kill = interpreting two-row p27 late tails as structure
kill = treating small-field plateau gates as transferable without an invariant
```

```text
p27_conic_signword_coupling_rows=1/1
```
