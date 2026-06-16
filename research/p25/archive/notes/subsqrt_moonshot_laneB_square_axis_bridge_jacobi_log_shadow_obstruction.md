# p25 Lane B Square-Axis Bridge Jacobi-Log Shadow Obstruction

Updated: 2026-06-12

## Result

The natural p24-style Jacobi-log shortcut still fails on the actual p25
square-axis bridge target.

The bridge target on `C_3 x C_169` has:

```text
direct support = 6 signed points
row/column mixed support = 18 cells
mixed rank = 2
diamond/inversion conjugacy = true
nontrivial C169 Fourier support = 168/168
```

For the raw and single-anchor-corrected Jacobi packets at order `507`, the log
transforms:

```text
log mod 2029
log mod 507
log mod 169
507 * log mod 2029
```

all fail the bridge contract.  They have rank two and full C-axis Fourier
mass, but:

```text
direct scalar to bridge = none
mixed scalar to bridge = none
mixed support = 506 or 507 cells
mixed C support = all 169 C coordinates
diamond/inversion conjugacy = false
```

Thus full Fourier support and rank two are not enough.  The primitive bridge
requires an additional genuinely mixed correction, not a plain discrete-log
shadow of the Hasse-Davenport/Jacobi packet.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_jacobi_log_shadow_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_jacobi_log_shadow_obstruction_rows=1/1
```

## Continue / Kill

Continue looking for an arithmetic producer that realizes the primitive
`C_169` bridge directly.  Kill the natural square-axis Jacobi-log shortcut:
anchor correction does not recover the six-point bridge, and the resulting
log shadows are dense and violate the bridge inversion relation.
