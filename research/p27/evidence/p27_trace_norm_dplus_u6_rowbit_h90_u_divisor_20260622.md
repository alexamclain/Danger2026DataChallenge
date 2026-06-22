# P27 Trace/Norm Dplus U6 Row-Bit H90 U-Divisor Screen

Date: 2026-06-22

## Claim

The H90-soluble Dplus `U6` row-bit sign descends to the even elliptic quotient
coordinate

```text
u = 4/(t - 1/t)^2
```

but it is not a monic linear or quadratic divisor in `u` in the tested fields.

This is a useful narrowing.  The soluble-side sign is simpler than an arbitrary
function on `E_h90`, but not as simple as the first visible `P^1_u` divisors.
The next concrete screen is exact monic cubic/quartic support on the generated
finite-field target packet.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_probe_20260622.txt
```

Target packet:

```text
research/p27/archive/fixtures/p27_dplus_rowbit_u_divisor_targets_20260622.json
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_probe.py \
  --fields 263,607,1607,1847,2087 \
  --degree 2 \
  --include-bare \
  --json-out research/p27/archive/fixtures/p27_dplus_rowbit_u_divisor_targets_20260622.json \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_probe_20260622.txt
```

## Result

Aggregate:

```text
u_mixed = 0
degree1_exact = 0
degree2_exact = 0
```

Materialized target rows:

```text
field   rows   plus   minus   mixed u groups
263     6      6      0       0
607     32     16     16      0
1607    50     28     22      0
1847    64     45     19      0
2087    57     25     32      0
```

The bare tower gives the same meaningful conclusion: no mixed `u` groups and
no exact degree `1` or degree `2` monic divisor in any field with both signs.

The best linear scores are not exact:

```text
q607:  best 26/32
q1607: best 38/50
q1847: best 45/64, just baseline plus majority
q2087: best 43/57
```

## Exact-Support Packet

The generated fixture freezes rows for the next exact-support screen:

```text
family = dplus_h90_soluble_rowbit_u
degree 3 = u^3 + a*u^2 + b*u + c
degree 4 = u^4 + a*u^3 + b*u^2 + c*u + d
accept = chi(P(u)) = polarity * sign on every row, with no zero evaluations
```

Promotion fields:

```text
q1607: rows=50, expected monic cubic exact fits ~= 3.69e-6
q1847: rows=64, expected monic cubic exact fits ~= 3.42e-10
q1847: rows=64, expected monic quartic exact fits ~= 6.31e-7
q2087: rows=57, expected monic cubic exact fits ~= 6.31e-8
q2087: rows=57, expected monic quartic exact fits ~= 1.32e-4
```

An exact cubic/quartic in `q1847` or `q2087` would therefore be a serious
source/divisor candidate, not a routine interpolation artifact.

## Interpretation

Positive:

```text
The H90-soluble row bit descends from E_h90 to the even u-line in all tested
fields.
The next search is a small, named exact-support problem rather than a broad
feature scan.
```

Negative:

```text
No monic linear or quadratic u-divisor explains the sign.
q607 quartics are not decisive: with 32 rows, random monic quartics are
expected to produce many local exact fits.
```

## Consequence

The next concrete test is:

```text
run monic cubic exact support on q1607, q1847, q2087;
if no cubic, run monic quartic exact support on q1847 and q2087;
verify any hit on another guard field before promoting.
```

Promote only if the exact divisor survives a promotion field and gives a named
source/class to compare with later gates.  If cubic/quartic exact support is
empty in q1847/q2087, kill visible low-degree `P^1_u` support and keep the
row-bit lane in divisor/theta/Prym extraction.

## Continue / Kill

```text
continue = exact monic cubic/quartic support on the frozen u target packet
continue = if hit, verify on independent guard field and compare to d4/d5
continue = if no hit, extract non-visible theta/Prym class on the u-line cover

kill = monic degree <= 2 u-divisors as the source
kill = treating q607 quartic fits, if any, as promotion evidence by themselves
kill = GPU production from u buckets before exact support or theorem evidence
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_rows=1/1
```
