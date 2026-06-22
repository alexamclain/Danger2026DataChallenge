# P27 B-Line No-R Beta_U Norm Relation Screen

Date: 2026-06-22

## Claim

The beta_U norm class is real, but it does not collapse to a small visible
plane curve in `(B, N)` where:

```text
N = Norm_GF(q^2)/GF(q)(Unext + 2)
```

Across the main guard fields, the point sets `(B,N)`, `(B,N)|gamma+`, and
`(B,N)|gamma-` have no stable extra bidegree relation through:

```text
B degree <= 12
N degree <= 16
```

The lone extra-nullity signal appears only for `q=199`, `gamma-`,
bidegree `B8_N12`, and disappears at `q=263` and `q=311`.  Treat it as local
interpolation.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_norm_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_relation_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_relation_probe_q311_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_relation_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_relation_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_relation_probe.py \
  --fields 311^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_relation_probe_q311_20260622.txt
```

## Result

Screened fields:

```text
103^2, 167^2, 199^2, 263^2, 311^2
```

Screened systems:

```text
all beta_U norm pairs
gamma_plus beta_U norm pairs
gamma_minus beta_U norm pairs
```

Screened bidegrees:

```text
B2_N4
B4_N8
B6_N8
B8_N12
B10_N16
B12_N16
```

Stable verdict:

```text
extra_nullity = 0 for all systems and bidegrees in q=103,167,263,311
extra_nullity = 0 for all and gamma_plus in q=199
q=199 gamma_minus B8_N12 has extra=9, but q=263/q=311 kill the same signal
```

## Interpretation

Positive:

```text
The beta_U norm class remains a named divisor/Kummer target.
The finite-field norm descent and 16/32 fiber split are still the real
structure to explain.
```

Negative:

```text
No small bidegree plane curve in (B,N) is visible.
The gamma+ and gamma- subcovers do not expose a stable low-bidegree relation.
The q199 extra-nullity signal is not stable.
No GPU sampler follows from a low-degree (B,N) relation.
```

## CAS Consequence

Do not ask the CAS/expert agent to search for a small explicit plane equation
in `(B, Norm(Unext+2))` as the main route.  Ask for divisor/Kummer extraction
of the norm class on the normalized beta_U support:

```text
support: chi(B)=+1
class:   N = Norm(Unext+2)
task:    div(N) modulo squares, quotient/Prym explanation of the 16/32 split
```

Promote only a quotient, recurrence, or source map produced from the divisor
class.  Kill further blind low-bidegree `(B,N)` scans unless a theorem names a
specific coordinate change.

## Continue / Kill

```text
continue = beta_U divisor/Kummer extraction for Norm(Unext+2)
continue = quotient/Prym explanation of the 16/32 split
continue = compare beta_U norm class with f4/f3 after normalization

kill = small visible (B, Norm(Unext+2)) plane curve through B12_N16
kill = q199-only B8_N12 gamma- relation
kill = GPU production from beta_U norm data alone
```

```text
p27_b_line_noR_betaU_norm_relation_rows=1/1
```
