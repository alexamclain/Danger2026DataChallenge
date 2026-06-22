# P27 Trace/Norm Dplus U6 Row-Bit H90 Group-Coset Screen

Date: 2026-06-22

## Claim

The H90-soluble Dplus `U6` row-bit sign is not explained by the tested small
elliptic group quotient classes on:

```text
E: v^2 = u^3 - u.
```

This is a negative result for the nearest sourceable/coset shortcut.  It does
not kill the H90 local-solubility boundary; it says the remaining plus/minus
class is not a small visible projection of the H90 elliptic group.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_probe.py \
  --fields 263,607,1607,1847,2087 \
  --moduli 2,3,4,6,8,12,16,24 \
  --include-bare \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_probe_20260622.txt
```

## Model

The screen uses the known quotient maps:

```text
E_h90: w^2 = -t^4 + 6*t^2 - 1
a = t - 1/t
b = w*(t^2 + 1)/t^2
C: b^2 = 16 - a^4
E: v^2 = u^3 - u
u = 4/a^2
v = 2*b/a^3
```

On each field it keeps H90-soluble uniform row-bit records, folds `P` and
`-P`, and projects to small quotient classes of `E(F_q)`.

## Result

Overall:

```text
exact_nontrivial_projection_total = 0
```

The field `q=263` has only one sign in the retained records, so it is not a
promotion field for a character.  In every field with both signs present,
projected classes remain mixed.

Materialized examples:

```text
q607:
  records = 32
  target_plus/target_minus = 16/16 after folding
  m=2,4,8,16 all have mixed projected classes

q1607:
  records = 50
  target_plus/target_minus = 28/22
  m=2,3,4,6,8,12,24 all have mixed projected classes

q1847:
  records = 64
  target_plus/target_minus = 45/19
  m=2,3,4,6,8,12,24 all have mixed projected classes

q2087:
  records = 57
  target_plus/target_minus = 25/32
  m=2,3,4,6,8,12,24 all have mixed projected classes
```

The bare tower gives the same conclusion, with the same meaningful fields
mixed in every tested projection.

## Interpretation

Positive:

```text
The H90 local-solubility boundary remains intact.
The screen tests a genuinely different explanation than visible coordinate
products: small elliptic group quotient/coset classes.
```

Negative:

```text
No tested small quotient projection of E(F_q) separates the soluble-side
row-bit sign.
There is no immediate small-coset sampler for the plus row-bit half.
```

## Consequence

The remaining H90 row-bit question is now narrower:

```text
prove the Ktrace local-solubility boundary;
extract the non-visible soluble-side sign as a divisor/theta/Prym or higher
Kummer class;
compare that class with later selected gates d4,d5,...
```

Do not ask the GPU agent to test small elliptic quotient classes for this row
bit unless a new theorem names a specific projection outside the tested
moduli.

## Continue / Kill

```text
continue = divisor/theta/Prym extraction of the soluble-side sign
continue = compare this H90 class to A-level d3/d4/d5 classes
continue = include elliptic coordinates as telemetry if cheap

kill = small E(F_q) quotient projections m <= 24 as a row-bit source
kill = treating q263 one-sign exactness as a character promotion
kill = GPU production from H90 group-coset buckets
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_group_coset_rows=1/1
```
