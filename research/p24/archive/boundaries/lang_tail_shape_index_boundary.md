# Lang Tail Shape Index Boundary

Date: 2026-06-05

This note records the cheap prefilter added for p24-style Lang tail analogues.

## Tool

Added:

```text
p24/lang_tail_shape_index.py
```

Unlike the full pivot miner, this script does not build Hilbert roots, full CM
cycles, packet factors, DFT matrices, or Lang coordinates.  It uses only:

```text
qfbclassno(D);
quotient shapes h=m*n;
Kronecker(D,q)=1 as a necessary local split condition;
Frobenius orbit lengths modulo CRT components;
Hermitian packet degree ord_n(q).
```

It reports cheap shape candidates with:

```text
left orbit length;
right Frobenius orbit count and lengths;
kept capacity after deleting one right orbit;
full-block prefix count;
tail length range.
```

Rows from this tool are only candidates.  They still need full verification by
`p24/lang_pivot_order_miner.py`.

## Validation

Pinned known non-tail shape:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_tail_shape_index.py \
  --only-D -13319 --max-rows 4 --max-h 300 --q-stop 300 \
  --max-q-tests-per-D 200 --max-prime-quotients 32 \
  --max-composite-quotients 96 --min-n 3 --max-n 100 \
  --max-axis-dim 80 --max-m 80 --min-left-orbit-len 3 \
  --max-left-orbit-len 8 --min-right-orbits 2 \
  --min-right-orbit-len 2 --min-full-blocks 0
```

reported:

```text
D=-13319 h=140 q=163 m=28 n=5
components=[4,7]
left=7[1]:L3 and left=7[3]:L3
right=7:orbits[3,3]
tails=0/2
full_blocks=1..1
packet_degree=4.
```

The corresponding heavy pinned row can now be tested directly with `--only-q`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_pivot_order_miner.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 7 --only-right 7 --include-linear \
  --max-orderings 24
```

which verified the exact leading pivots and residual products as before.

## Tail Search Result

The intended p24 shape has a genuine tail:

```text
left_len=156, right_orbit_len=35,
4 full blocks + 16 tail coordinates.
```

Bounded shape-only searches for analogous small rows found none:

```text
max_h=700, max_abs_D=120000, q_stop=400000,
max_q_tests_per_D=2000,
min_left_orbit_len=3, min_right_orbits=3,
min_right_orbit_len=2, require_tail=1
=> candidates=0.

max_h=1000, max_abs_D=180000, q_stop=600000,
max_q_tests_per_D=3000,
min_left_orbit_len=3, min_right_orbits=2,
min_right_orbit_len=2, require_tail=1,
min_full_blocks=0
=> candidates=0.
```

A larger shape-only search was capped by:

```text
timeout 25s ...
max_discriminants=2000, max_h=5000, max_abs_D=900000,
q_stop=1200000, max_q_tests_per_D=5000,
min_left_orbit_len=4, min_right_orbits=3,
min_right_orbit_len=2, require_tail=1
```

and produced no candidate before timeout.

On 2026-06-06, a more permissive shape-only pass did find small formal
nonzero-prefix tail shapes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_tail_shape_index.py \
  --max-abs-D 120000 --max-h 900 --max-m 240 --max-n 600 \
  --q-stop 400000 --max-q-tests-per-D 120 \
  --min-left-orbit-len 4 --max-left-orbit-len 16 \
  --min-right-orbits 2 --max-right-orbits 8 \
  --min-right-orbit-len 2 --min-full-blocks 1 \
  --require-tail --min-tail-len 1
```

reported rows of the form:

```text
D=-80471 h=455 q=523 m=65 n=7 components=[5,13]
left=5[1]:L4 right=13:orbits[3,3,3,3]
tails=4/4 tail_range=1..1 full_blocks=1..1.
```

A second pass found:

```text
D=-169991 h=693 q=719 m=99 n=7 components=[9,11]
left=11[1]:L5 right=9:orbits[2,2,2,2]
tails=4/4 tail_range=1..1 full_blocks=2..2.
```

These are only necessary-shape candidates.  Pinned actual-CM checks with
`lang_trace_gcd_kernel_audit.py` for the listed `D,q,m,left,right` rows
returned `rows=0`, because the shape-only Kronecker split condition did not
survive the full Hilbert splitting / full-cycle / packet construction.

The practical rule is therefore:

```text
shape-only hits are cheap theorem-test leads;
they are not actual-CM calibration rows until a full audit returns profiles.
```

## Consequence

The Lang pivot miner is now connected to a cheap candidate prefilter, but
small p24-shaped tail analogues appear scarce.  The absence of such rows is
not a theorem; it is a search boundary that changes the workflow:

```text
do not run broad Hilbert/packet scans to find tail analogues;
first find a shape row with lang_tail_shape_index.py;
then run lang_pivot_order_miner.py with --only-D/--only-q/--only-m.
```

The current p24 arithmetic theorem remains:

```text
L_rep = B_rep * T_rep != 0 mod p,
```

where the `T_rep` factor is the true `16`-coordinate quotient-tail p-unit.
