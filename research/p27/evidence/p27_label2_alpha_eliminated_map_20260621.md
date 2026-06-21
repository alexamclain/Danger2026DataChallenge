# P27 Label-2 Alpha Eliminated-Map Probe

Date: 2026-06-21

## Claim

The label-2/order-4 lane now has an explicit rational `alpha` action on the
eliminated cyclic-quartic model over the residual elliptic curve.  This turns
the next CAS ask from "find the automorphism" into:

```text
use this explicit order-4 map to compute the quotient/Prym decomposition
```

The eliminated model over `E: W^2=X^3-X` is:

```text
R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*S^2 = 0
pref = W*(X^2+1)/X
```

Using the original identity

```text
R^2 = pref*(m0 + mt*T),
```

the order-4 lift

```text
T -> -T
R -> R*(m0 - mt*T)/(2*T*S)
```

descends to the eliminated rational map:

```text
alpha_R = R*mt*(2*pref*m0 - R^2)/(2*S*(R^2 - pref*m0)).
```

## Probe

Gate:

```text
research/p27/archive/gates/p27_label2_alpha_eliminated_map_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_label2_alpha_eliminated_map_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_label2_alpha_eliminated_map_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_label2_alpha_eliminated_map_probe_20260621.txt
```

The probe enumerates affine points on the eliminated quartic over p27-signature
fields, applies the rational `alpha_R` map, and checks:

```text
alpha maps the curve to itself
alpha^2 is the R-deck involution R -> -R
alpha^4 is identity
```

## Results

For `q=1607`:

```text
quartic_affine_points = 1604
quartic_fiber_0 = 1203
quartic_fiber_1 = 4
quartic_fiber_4 = 400
alpha_defined = 1600
alpha_undefined = 4
```

For `q=1847`:

```text
quartic_affine_points = 1948
quartic_fiber_0 = 1357
quartic_fiber_1 = 4
quartic_fiber_4 = 486
alpha_defined = 1944
alpha_undefined = 4
```

For `q=2087`:

```text
quartic_affine_points = 1956
quartic_fiber_0 = 1595
quartic_fiber_1 = 4
quartic_fiber_4 = 488
alpha_defined = 1952
alpha_undefined = 4
```

The failure counters are absent, i.e. zero:

```text
alpha_image_not_on_curve = 0
alpha2_not_rdeck = 0
alpha4_not_identity = 0
quartic_root_mismatch = 0
```

The four undefined affine points are the expected exceptional branch/degenerate
points where the rational formula denominator vanishes.

## Interpretation

Positive:

```text
The order-4 action is now explicit on the eliminated genus-17 model.
It validates over three q = 7 mod 16 fields.
The next Magma/Sage quotient ask can use a concrete rational map.
```

Negative:

```text
The quotient by alpha is still the residual elliptic curve E.
This does not by itself give a sampler or d3/d4 recurrence.
The quartic fibers are mostly 0-or-4 over E, so compactD remains a real cover
rather than a trivial rational parameter.
```

## Continue / Kill

```text
continue = Magma/Sage quotient/Prym decomposition using explicit alpha_R
continue = derive a cyclic-quartic character over E only if the Prym splits usefully
continue = test any extracted character against d3/d4 on q=1607/q1847/q2087 and p27

kill = treating compactD=-1 as a direct low-genus source
kill = more visible H90 norm-one squareclass products
kill = GPU production promotion without quotient-derived recurrence or rate lift
```

## Linked Artifacts

- Parent: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Component check: [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md)
- Gate: `research/p27/archive/gates/p27_label2_alpha_eliminated_map_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_alpha_eliminated_map_probe_20260621.txt`

```text
p27_label2_alpha_eliminated_map_probe_rows=1/1
```
