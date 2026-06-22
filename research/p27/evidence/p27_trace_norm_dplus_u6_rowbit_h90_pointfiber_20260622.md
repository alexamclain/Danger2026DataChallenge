# P27 Trace/Norm Dplus U6 Row-Bit H90 Point-Fiber Probe

Date: 2026-06-22

## Claim

The Dplus `U6` row bit has a positive H90 point-fiber compatibility signal.

Although the row-bit lift remains irreducible over the H90 elliptic function
field in the `q=607` factor test, direct small-field enumeration shows:

```text
over t alone, fibers can be mixed;
over rational E_h90, domain-spin, and A_eta points, tested fibers are uniform.
```

In the fields where `t` has mixed row-bit fibers, every mixed `t` group has no
rational `E_h90` point.  Thus the H90 quotient is still the right structure to
explain the row bit, but the explanation is not a simple function-field
factorization of the bare lift.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe.py \
  --fields 71,167,199,263,607 \
  --include-bare \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe_20260622.txt
```

## Materialized Tower Result

With the materialization filters:

```text
chi(U5^2-4)=+1
chi(U5+A)=+1
chi(U6^2-4)=+1
chi(U6+A)=+1
```

the point-fiber summary is:

```text
field   t mixed   t mixed with E point   E mixed   Z mixed   Aeta+ mixed   Aeta- mixed
71      0/8       0                      0/16      0/32      0/64         0/64
167     0/6       0                      0/12      0/24      0/48         0/48
199     0/16      0                      0/32      0/64      0/128        0/128
263     12/24     0                      0/24      0/48      0/96         0/96
607     32/96     0                      0/128     0/256     0/512        0/512
```

For `q=263` and `q=607`, all mixed `t` fibers have no rational `E_h90` point:

```text
q263:
  t_mixed = 12
  t_mixed_with_E_point = 0
  t_mixed_without_E_point = 12

q607:
  t_mixed = 32
  t_mixed_with_E_point = 0
  t_mixed_without_E_point = 32
```

## Bare Tower Result

Without materialization filters, the same pattern persists:

```text
field   t mixed   t mixed with E point   E mixed   Z mixed   Aeta+ mixed   Aeta- mixed
71      8/18      0                      0/20      0/40      0/73         0/73
167     6/14      0                      0/16      0/32      0/57         0/57
199     16/34     0                      0/36      0/72      0/137        0/137
263     12/26     0                      0/28      0/56      0/105        0/105
607     64/132    0                      0/134     0/268     0/529        0/529
```

This says the H90 rational-point compatibility is not caused only by the
materialization side conditions.

## Interpretation

Positive:

```text
The H90 elliptic quotient exactly separates the tested rational point fibers:
mixed t fibers occur only where E_h90 has no rational point.
After passing to rational E_h90 points, no tested row-bit fiber is mixed.
The same remains true over domain-spin and A_eta rational points.
```

Negative:

```text
This is not a proof that the row-bit cover factors over E_h90.
The q607 function-field factorization over E_h90 remains irreducible degree 32.
The Aeta/domain-spin factor-degree question still requires offline CAS.
```

## Consequence

The Dplus row-bit lane should not be killed as generic merely because the bare
function-field lift is irreducible over `E_h90`.  The better ask is:

```text
explain why rational E_h90 point fibers are uniform;
then decide whether that uniformity comes from local solvability, a Prym/theta
relation, or a hidden selected-source condition.
```

For GPU, this still does not promote a production bucket.  It does justify
including the row bit and H90 rational-point coordinates in fused/native
`Dplus` telemetry.

Follow-up
[P27 Trace/Norm Dplus U6 Row-Bit H90 Visible Character](p27_trace_norm_dplus_u6_rowbit_h90_visible_character_20260622.md)
screens the cheap explanation: visible product characters through weight `4`
on `E_h90`, domain-spin, and `A_eta` coordinates.  It finds no exact products.
The best filtered products are equivalent to weak `A` bias, and the best bare
products are weak `-A*B` bias.  Thus the point-fiber uniformity remains real
but non-visible in the tested coordinate family.

## Continue / Kill

```text
continue = offline factorization with side conditions over domain-spin/Aeta covers
continue = explain H90 rational-point uniformity of the row bit
continue = fused/native Dplus telemetry with E_h90/Z/Aeta coordinates and row bit

kill = pointwise descent to t alone
kill = treating irreducibility over bare E_h90 as a complete independence proof
kill = visible E_h90/Z/Aeta product characters through weight 4 as the source
kill = GPU production before a source or quotient relation is named
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_rows=1/1
```
