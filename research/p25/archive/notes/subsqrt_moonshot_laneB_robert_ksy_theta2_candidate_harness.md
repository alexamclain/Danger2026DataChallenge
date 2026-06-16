# P25 Lane B: theta2 Sparse Candidate Harness

Updated: 2026-06-13 14:39 PDT

## Purpose

The theta2 resolvent changed the producer contract.  A theorem hit no longer
has to emit the final `150`-cell bridge directly; it may emit the `300`-cell
theta2 divisor footprint:

```text
theta2     = 4*bridge - [2]bridge
theta2^-1  = [2]bridge - 4*bridge
```

This harness accepts sparse source triples

```text
right_log c_log coefficient
```

in `C_75 x C_169`, checks theta2/theta2-inverse exactness, applies the finite
resolvent, and audits the recovered bridge with the existing bridge contract.

## Result

Default positive controls:

```text
theta2 sparse terms         = 300
theta2 inverse sparse terms = 300
coefficient counts          = (-4,75), (-1,75), (1,75), (4,75)

resolvent(theta2)           = bridge
resolvent(theta2^-1)        = -bridge
shifted union support       = 11700
shifted term budget         = 46800
```

After global sign normalization, both orientations pass the full bridge
contract.

Negative control:

```text
plain bridge sparse terms = 150
accepted as theta2        = false
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_candidate_harness.py
```

To test a theorem output:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_candidate_harness.py \
  --sparse-source PATH
```

Expected marker:

```text
robert_ksy_theta2_candidate_harness_rows=1/1
```

## Interpretation

The active KSY/theta theorem request is now operational:

1. produce exact sparse theta2 or theta2-inverse divisor triples;
2. let the local resolvent recover the bridge;
3. use the support-period `156` resolvent;
4. keep the final bridge contract unchanged.

This lowers the arithmetic producer burden without weakening the finite
certificate target.
