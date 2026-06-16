# Subsqrt Moonshot Lane B Jacobi-Log Shadow Obstruction

Date: 2026-06-12

## Result

The natural discrete-log shadows of the punctured Hasse-Davenport Jacobi packet
are not the missing ray-local producer.

This gate checks the first `C_3 x C_13` lab.  It takes:

```text
raw Jacobi packet
single-anchor-corrected Jacobi packet
```

then discrete-logs them in the Jacobi value field and tests the natural
projections:

```text
log mod 79
log mod 39
log mod 13
39 * log mod 79
```

Every direct shadow fails the `theta_{3,1}` quotient contract:

```text
direct_scale = None
direct_selected_defect_ok = 0
direct_raw_product_ok = 0
```

Even after removing all row-plus-column additive normalizations, the mixed
payload is still wrong:

```text
mixed_rank = 2
zero_mean = 1
Fourier support = 12 / 12
but:
  support = (0, 12, 13), not the half-arc (4, 9, 6)
  diamond_conjugacy = 0
  scalar_multiple_of_canonical = 0
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_jacobi_log_shadow_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_jacobi_log_shadow_obstruction_gate.py
```

Observed:

```text
jacobi_log_shadow_obstruction_rows = 8 / 8
conclusion = reported_p25_laneB_jacobi_log_shadow_obstruction_gate
```

## Consequence

This rules out a tempting shortcut:

```text
take logs of the raw or anchor-corrected Jacobi sums;
reduce them modulo an obvious quotient;
remove scalar / row / column terms;
call the result the ray-local theta_{3,1} producer.
```

The obstruction is not lack of mixed payload.  The log shadows have rank `2`
and full nontrivial `C_13` Fourier support.  The failure is geometric: the
payload is spread across the full C-axis and does not obey the required
negative-inversion diamond relation.

The missing producer must therefore do something more selective than the naive
Jacobi-log shadow: it must realize the middle half-arc vector itself, not just
the Hasse-Davenport multiplicative packet up to row/column normalization.
