# P27 B-Line No-R Beta_U Next-Gate Probe

Date: 2026-06-22

## Claim

The `beta_U_fixedB` norm class is a real one-gate structure, but it does not
directly carry the next selected gate.

On every tested `beta_U` row with

```text
gamma = chi(Unext + 2) = +1,
```

the materialization step behaves exactly as expected:

```text
Unext = x6 + 1/x6 gives 2 x6 roots,
each x6 has 2 next halves x7,
chi(v+2) = chi(x7) for v = x7 + 1/x7.
```

However, the next sign `f4 = chi(x7) = chi(v+2)` is mixed inside every active
gamma-positive base `B` row.  Thus the `beta_U` norm class does not provide a
multi-gate source law by itself.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_next_gate_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_next_gate_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_next_gate_probe_q199_q263_q311_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_next_gate_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_next_gate_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_next_gate_probe.py \
  --fields 199^2,263^2,311^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_next_gate_probe_q199_q263_q311_20260622.txt
```

## Result

Fields:

```text
23^2, 71^2, 103^2, 167^2, 199^2, 263^2, 311^2
```

Setup checks:

```text
bad_curve_a = 0 in every field
B_gamma_conflicts = 0 in every field
vplus2_x7_chi_mismatch = 0 in every field
```

For fields with gamma-positive beta_U rows:

```text
field    gamma+ B rows   x6 roots per B   x7 roots per B   B rows with mixed f4
71^2     8               32               64               8
167^2    6               32               64               6
199^2    16              32               64               16
263^2    12              32               64               12
311^2    16              32               64               16
```

Aggregate f4 signs on gamma-positive beta_U rows:

```text
field    f4+   f4-
71^2     278   234
167^2    196   188
199^2    490   534
263^2    384   384
311^2    536   488
```

Fields with only gamma-negative beta_U rows:

```text
23^2     betaU gamma- = 64, no x6 materialization
103^2    betaU gamma- = 384, no x6 materialization
```

## Interpretation

Positive:

```text
The beta_U norm class cleanly controls f3/materialization.
The materialized next-root semantics match the B-line f3/f4 interpretation:
chi(v+2) = chi(x7) with zero mismatches.
This gives a regression fixture for any CAS extraction of the beta_U class.
```

Negative:

```text
f4 is not uniform on gamma-positive beta_U fibers.
Every gamma-positive B row has both f4 signs.
The beta_U class does not by itself give a two-gate recurrence or source law.
No GPU sampler follows from beta_U gamma=+1.
```

## CAS Consequence

Refine the beta_U task:

```text
extract beta_U Norm(Unext+2) as a clean f3/materialization Kummer class;
do not expect it to carry f4 automatically;
compare f4 only after normalization, as a possible quotient/Prym relation or
fresh half-cover.
```

Promote beta_U only if CAS finds a non-visible class relation between this
f3 norm class and the mixed f4 class.  Kill beta_U as a direct sqrt-beating
route if f4 remains a fresh half-cover on every quotient carrying the beta_U
class.

## Continue / Kill

```text
continue = beta_U divisor/Kummer extraction for f3/materialization
continue = compare f4 after beta_U normalization, not before
continue = use this probe as a regression for chi(v+2)=chi(x7)

kill = beta_U gamma=+1 as a multi-gate sampler
kill = GPU production from beta_U materialized rows
kill = treating the 16/32 beta_U split as evidence for f4 coupling
```

```text
p27_b_line_noR_betaU_next_gate_rows=1/1
```
