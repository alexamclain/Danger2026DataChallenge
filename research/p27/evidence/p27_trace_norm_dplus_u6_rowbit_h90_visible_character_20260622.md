# P27 Trace/Norm Dplus U6 Row-Bit H90 Visible Character

Date: 2026-06-22

## Claim

The H90 rational point-fiber row-bit uniformity is not explained by a visible
product character on the tested `E_h90`, domain-spin, or `A_eta` coordinates.

This keeps the Dplus row bit alive as real structure, but moves it out of the
cheap GPU bucket/sign-product lane and into Prym/theta, local-solubility, or
offline CAS class-comparison territory.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_visible_character_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_visible_character_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_visible_character_probe.py \
  --fields 71,167,199,263,607 \
  --max-weight 4 \
  --top 12 \
  --include-bare \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_visible_character_probe_20260622.txt
```

## Screened Levels

```text
E_h90:      (t,w)
Z:          (t,w,z), z^2 = domain-spin polynomial
Aeta_plus:  (t,w,z,rho), rho^2 = A_eta for eta=+1
Aeta_minus: (t,w,z,rho), rho^2 = A_eta for eta=-1
```

The probe screens product characters through weight `4` on the visible atoms
available at each level.

## Materialized Tower Result

With the materialization filters enabled, there are no exact visible
characters:

```text
level       rows   exact products   best product        best matches
E           212    0                A                   136/212 = 0.641509
Z           424    0                A                   272/424 = 0.641509
Aeta_plus   848    0                A                   544/848 = 0.641509
Aeta_minus  848    0                A                   544/848 = 0.641509
```

The best products are equivalent to weak `A` bias and are not exact.

## Bare Tower Result

Without the materialization filters, there are still no exact visible
characters:

```text
level       rows   exact products   best product        best matches
E           234    0                -A*B                154/234 = 0.658119
Z           468    0                -A*B                308/468 = 0.658119
Aeta_plus   901    0                -A*B                581/901 = 0.644839
Aeta_minus  901    0                -A*B                581/901 = 0.644839
```

The best bare products are weak, field-dependent `A/B` bias, not a source law.

## Interpretation

Positive:

```text
The H90 point-fiber uniformity is still real.
The screen covered visible E_h90, domain-spin, and A_eta point coordinates.
```

Negative:

```text
No exact product character through weight 4 explains the uniform row bit.
The H90 point-fiber signal should not be converted into a GPU sign-bucket run.
```

## Consequence

The next Dplus row-bit work should focus on:

```text
offline factorization with side conditions over domain-spin/Aeta covers;
Prym/theta or local-solubility explanation of H90 rational-point uniformity;
GPU telemetry columns that expose row bit, H90 coordinates, and later gates.
```

Do not spend GPU time retrying visible H90 coordinate products unless a divisor
or source theorem names a new atom family.

## Continue / Kill

```text
continue = offline domain-spin/Aeta factorization with selected side conditions
continue = explain H90 rational-point uniformity by Prym/theta/local solvability
continue = fused/native Dplus telemetry with row-bit/H90/Aeta columns

kill = visible E_h90/Z/Aeta product characters through weight 4 as the source
kill = GPU sign-bucket scans based on the current H90 visible atoms
kill = interpreting A or A*B bias as a promotion signal
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_visible_character_rows=1/1
```
