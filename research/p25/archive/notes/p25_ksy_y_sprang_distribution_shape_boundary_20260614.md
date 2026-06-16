# P25 KSY-y: Sprang Distribution-Shape Boundary

Updated: 2026-06-14 08:11 PDT

## Purpose

After the post-Koo-Shin reroute, Sprang/Kronecker `D=2` is the first theorem
front door.  This checkpoint narrows what counts as progress there.

The p25 target is:

```text
base * K_trace * (1 + D + D^2) * (1 - T)
base=(1,25), D=(1,3), T=(2,113) on C_3 x C_169
```

## Boundary

The visible `D` step has order `507`, and:

```text
3D = (0,9)
```

So the three `D` points are a short arithmetic segment, not an order-3 subgroup
or coset.  This kills literal distribution shapes that only supply subgroup
kernels or full torsion sums.

Rejected shadows:

```text
kernel/base edge only       support 2
literal order-3 row kernel  wrong C coordinates
literal C13 kernel          support 26
literal C169 axis           support 338
C169 projection             loses C3 row graph and T edge
literal D=2 torsion selector killed on odd p25 source quotient
```

Accepted front door:

```text
exact mixed row-labeled specialization
```

That is, an even-D Kronecker/Sprang theorem must emit exact `P` or
theta2/theta2-inverse divisor data with the mixed row graph, equal weights, and
orientation.

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_distribution_shape_boundary_gate.py
```

Marker:

```text
ksy_y_sprang_distribution_shape_boundary_rows=1/1
```
