# Subsqrt Moonshot Lane B Gross-Koblitz Semiprimitive Unit Rewrite

Date: 2026-06-13

## Result

The HD/GK literature scout found a narrow rewrite for the free `U(169)` symbol
left by the gamma-reflection precheck.

Since

```text
p = 10^25 + 13
p == -1 mod 3
p^39 == -1 mod 507
f = 78 = 2 * 39
```

the cubic Gauss sum is semiprimitive/pure.  In standard Gross-Koblitz
normalization this rewrites:

```text
U(169) -> 1
U(338) -> 1
```

Applying that to the reflection residue:

```text
before:
  (1,2): +234 * U(169)
  (2,1): -234 * U(169)

after:
  (1,2): +234
  (2,1): -234
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py
```

Observed:

```text
p_mod_3 = 2
p39_mod_507 = 506
unit_rewrites = ((169,1),(338,1))
residue_after_rewrite = ((1,2): 234), ((2,1): -234)
square_axis_gross_koblitz_semiprimitive_unit_rewrite_rows=1/1
```

## Consequence

Semiprimitive purity removes the free unit symbol, but it does not by itself
produce the anomaly projector.  The false-positive `(1,2)` scalar remains.

Continue the HD/GK lane only if a further multiplication, triplication,
endpoint, or quotient relation removes `(1,2)` while preserving the selected
`(2,1)` correction.  Otherwise this route is killed at the signed two-cell
scalar residue.
