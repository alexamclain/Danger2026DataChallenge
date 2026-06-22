# P27 A-Line Combined Prefix Support Screen

Date: 2026-06-22

## Claim

The nearest A-line source-shrink shortcut is negative: a single visible
low-degree character on `P1_A` does not select the all-plus `d3&d4` prefix in
the three guard fields.

This matters because a positive result would have fused two independent
half-losses into one source condition.  The negative result keeps the live
A-line route on normalized Kummer/divisor-class extraction, not GPU
A-prefix bucket production.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_prefix_support_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_a_line_prefix_support_probe_q1607_q1847_q2087_deg4_prefix2_3_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_prefix_support_probe.py \
  --small-primes 1607,1847,2087 \
  --selected-depth 6 \
  --prefix-depths 2,3,4 \
  --min-rows 40 \
  --max-weight 4 \
  --quadratic-prefixes 2,3 \
  | tee research/p27/archive/probe_outputs/p27_a_line_prefix_support_probe_q1607_q1847_q2087_deg4_prefix2_3_20260622.txt
```

## Screen

For each legal A-row, define the prefix bit:

```text
prefix2 = d3=+1 and d4=+1
prefix3 = d3=+1 and d4=+1 and d5=+1
prefix4 = d3=+1 and d4=+1 and d5=+1 and d6=+1
```

The probe asks whether that combined prefix bit is:

```text
prefix_m(A) = chi(f_m(A))
```

for visible branch support of degree `<= 4` on `P1_A`.

Families tested where enabled:

```text
split support: product of up to 4 rational linear factors
quadratic + linears: one irreducible quadratic times up to 2 rational factors
two quadratics: product of up to two irreducible quadratics
```

## Results

The two-gate prefix is the important source-shrink test.  It is negative
through visible degree `<= 4` in every guard field:

```text
q1607 prefix2 rows=49, plus/fail=19/30:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none

q1847 prefix2 rows=63, plus/fail=19/44:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none

q2087 prefix2 rows=57, plus/fail=18/39:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none
```

The three-gate prefix does not give a stable new selector:

```text
q1607 prefix3 rows=49, plus/fail=19/30:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none

q1847 prefix3 rows=63:
  skipped_one_sided; no A row survives the three-gate prefix

q2087 prefix3 rows=57, plus/fail=18/39:
  split degree <=4: none
  irreducible quadratic + <=2 linears: none
  two irreducible quadratics: none
```

The four-gate prefix is field-local tail behavior, not promotion evidence:

```text
q1607 prefix4: skipped_one_sided; all fail
q1847 prefix4: skipped_one_sided; all fail
q2087 prefix4 rows=57, plus/fail=18/39:
  split degree <=4: none
```

## Interpretation

Positive:

```text
The combined-prefix question is now explicitly tested, not inferred from
individual gate screens.
The two-gate all-plus prefix descends cleanly to A rows in all guard fields.
```

Negative:

```text
No visible degree <=4 A-line character selects d3&d4.
No stable deeper-prefix shortcut appears in q1607/q1847/q2087.
The prefix route does not justify GPU A-bucket production.
```

## Continue / Kill

```text
continue = normalized A/B/K/Sroot Kummer-class extraction
continue = B-line phase GPU telemetry with raw-source denominators
continue = CAS/expert work on class comparison, coboundaries, or sourced quotients

kill = low-degree visible A-character as a multi-gate source selector
kill = GPU A-prefix bucket production from finite-field prefix descent alone
kill = more blind A-prefix polynomial scans without a named divisor reason
```

```text
p27_a_line_prefix_support_rows=1/1
```
