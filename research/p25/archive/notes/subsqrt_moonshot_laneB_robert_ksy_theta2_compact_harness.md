# P25 Lane B: theta2 Compact Parameter Harness

Updated: 2026-06-13 14:43 PDT

## Purpose

The sparse theta2 harness accepts `300` source triples.  A KSY/Kato-Siegel
theorem may naturally emit a much smaller recipe:

```text
center_base
half_shift
optional inversion
```

This harness expands the compact recipe through the normalized-y footprint,
then reuses the sparse theta2 resolvent and final bridge contract.

## Result

Accepted compact recipe:

```text
center_base = (44,166) = base + H
half_shift  = (56,28)  = -H
H           = (19,141), with 2H = T
T           = (38,113)
```

With no inversion, the recipe emits `theta2^-1`; with `--invert`, it emits
`theta2`.

```text
theta2^-1 support       = 300
theta2 support          = 300
coefficient counts      = (-4,75), (-1,75), (1,75), (4,75)
resolvent(theta2^-1)    = -bridge
resolvent(theta2)       = bridge
shifted union support   = 11700
shifted term budget     = 46800
```

Controls rejected:

```text
wrong half orientation
using full bridge edge as the half shift
using the half edge without the center shift
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_compact_harness.py
```

Candidate mode:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_compact_harness.py \
  --center-right 44 --center-c 166 --half-right 56 --half-c 28
```

Use `--invert` for the theta2 orientation instead of theta2-inverse.

Expected markers:

```text
robert_ksy_theta2_compact_harness_rows=1/1
robert_ksy_theta2_compact_harness_candidate_rows=1/1
```

## Interpretation

The active theorem target can now be even smaller than sparse theta2 triples:
identify the compact KSY center/half-edge recipe.  The harness expands it,
resolvents it, and applies the unchanged bridge audit.
