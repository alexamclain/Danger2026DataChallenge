# Lang Trace-GCD Crossed-Product Orbit Boundary

Date: 2026-06-05

## Point

The raw trace-GCD determinant values on a nontrivial Frobenius orbit are not
ordinary base-factor evaluations.  They are, however, packaged exactly by a
crossed-product weighted-cycle norm.

For an orbit:

```text
O = {t_0, q*t_0, ..., q^(r-1)*t_0}
T_i = Delta(q^i*t_0)
```

define the weighted cyclic shift:

```text
M_O e_i = T_i e_{i+1},
M_O e_{r-1} = T_{r-1} e_0.
```

Then:

```text
det(M_O) = (-1)^(r-1) prod_i T_i.
```

For p24 the nonzero right-orbit length is:

```text
r = ord_211(p) = 35,
(-1)^(r-1) = +1.
```

So the seven trace-GCD orbit products are exactly seven crossed-product
weighted-cycle determinants.

## Audit

Added:

```text
p24/lang_trace_gcd_crossed_product_orbit_audit.py
p24/lean/TraceGcdCrossedProductGate.lean
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_crossed_product_orbit_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

Output summary:

```text
omitted=0:
  orbit [1,2,4]: product=2515, weighted_shift_match=1,
                 ordinary_power_match=0
  orbit [3,6,5]: product=603,  weighted_shift_match=1,
                 ordinary_power_match=0

omitted=1:
  orbit [1,2,4]: product=9495, weighted_shift_match=1,
                 ordinary_power_match=0
  orbit [3,6,5]: product=6085, weighted_shift_match=1,
                 ordinary_power_match=0

failures=0
```

Thus the crossed-product norm identity is exact, while the ordinary norm
collapse:

```text
prod_{t in O} Delta(t) = Delta(t_0)^|O|
```

is false on every nonconstant orbit.

## Consequence

This is the finite algebra that replaces the invalid ordinary base quotient
residue:

```text
not: f_O in F_p[Y]/Phi_O with base-field orbit values;
yes: crossed-product weighted-cycle/reduced norm for the orbit values.
```

The small payload is unchanged:

```text
seven crossed-product norm scalars + inverses = 14 field elements.
```

But the arithmetic producer theorem is now sharper:

```text
Construct, for each right Frobenius orbit O, the actual trace-GCD
crossed-product determinant-line element whose reduced norm is
prod_{t in O} det(P V_t A), and prove that reduced norm is a p-unit.
```

This is the trace-GCD analogue of the trace-frame crossed-product package:

```text
p24/trace_frame_trace_sum_crossed_product_boundary.md
p24/trace_frame_lead_crossed_product_norm.md
```

## What It Does Not Prove

The weighted-cycle identity alone is tautological once the actual values are
known.  It does not construct the values without class-set enumeration.

Its value is theorem-shaping:

```text
ordinary factor residues are wrong;
ordinary-power Hilbert-90 collapse is wrong;
crossed-product reduced norms are the correct descended orbit objects.
```

This is the object the embedded class-field/Fitting theorem should construct.

## Spectral Caveat

The companion audit:

```text
p24/lang_trace_gcd_crossed_weight_spectral_boundary.md
```

shows that the pinned right-7 row has one-orbit Fourier support, but p24
right-211 exterior support is full by `k=3`.  Therefore a further collapse
from seven crossed-product norms to one degree-35 norm would require a new
CM/Plucker cancellation theorem.  It is not a consequence of the
crossed-product packaging itself.
