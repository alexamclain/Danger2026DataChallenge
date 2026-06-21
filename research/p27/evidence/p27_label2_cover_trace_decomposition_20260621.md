# P27 Label-2 Cover Trace Decomposition Probe

Date: 2026-06-21

## Claim

The small-prime point-count diagnostic supports the genus/recurrence read:
the known intermediate biquadratic cover decomposes as expected after a
common-branch correction, but the new second-gate Prym trace is not an obvious
small integer combination of the visible quotient traces.

This is a cheap diagnostic only.  It is not a substitute for a Sage/Magma
zeta-function or Jacobian/Prym decomposition.

## Objects

Intermediate cover:

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
C = (X,W,T)
```

Second-gate cover:

```text
R^2 = W(X^2 + 1)(m0 + mt_coeff*T)/X
D = (X,W,T,R)
```

The trace probe counted `W`, `T`, the third quadratic quotient `WT`, the
intermediate cover `C`, and the full double cover `D` over small prime fields.
For the intermediate `V4` cover, the raw quotient-trace identity misses by a
constant `+1` because the model has common branch at `X=0`.

## Command

```bash
python3 research/p27/archive/gates/p27_label2_cover_trace_probe.py \
  | tee research/p27/archive/probe_outputs/p27_label2_cover_trace_probe_20260621.txt
```

## Result

The common-branch offsets are constant:

```text
intermediate_raw_common_branch_offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
intermediate_trace_decomposition_common_branch_adjusted_ok = 1
```

After replacing the raw third quotient trace `aWT` by the common-branch
adjusted `aWT+1`, the intermediate trace decomposition matches on all tested
small primes.

The new trace from `D -> C`,

```text
aPrym = aD - aC
```

does not match any integer linear combination of the obvious quotient traces
`aW`, `aT`, and adjusted `aWT` with coefficients in `[-8,8]`:

```text
prym_trace_small_combo_known_factors = none_bound_8
```

## Interpretation

Positive:

```text
The intermediate cover accounting is now consistent.
The trace probe is aligned with the genus-5 intermediate picture.
```

Negative:

```text
No obvious reuse of the known W/T/WT quotient factors explains the new Prym.
This weakens the hope that compactD=-1 is secretly a low-degree visible
quotient of the already-known elliptic/genus-2 factors.
```

What remains:

```text
Run Sage/Magma for the actual L-polynomial/Jacobian/Prym decomposition.
Look for a non-obvious low-degree quotient or special isogeny factor.
Do not treat the small-prime trace screen as a proof of genericity.
```

## Continue / Kill

```text
continue = Sage/Magma zeta/Jacobian/Prym decomposition of D and D -> C
continue = GPU compactD=-1 only as same-stream telemetry with d3/d4 reporting

kill = assuming the visible W/T/WT factors already provide a sqrt-beating source
kill = broad small-character scans not tied to a named quotient or recurrence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_label2_cover_trace_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_cover_trace_probe_20260621.txt`
- Related: [P27 Label-2 Cover Genus And Recurrence Probe](p27_label2_cover_genus_recurrence_20260621.md)

```text
p27_label2_cover_trace_decomposition_rows=1/1
```
