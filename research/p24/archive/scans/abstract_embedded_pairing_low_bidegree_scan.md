# Abstract-Embedded Low-Bidegree Pairing Scan

Date: 2026-06-07

This is a producer-facing stress test for the p24 selected-chain route.

Earlier tests showed that abstract unramified class-field quotient roots do
not map to embedded quotient period roots by affine or Mobius maps.  This scan
tests a slightly broader escape hatch:

```text
F(X,Y)=0
```

where `X` is an abstract quotient root, `Y` is an embedded period quotient
root, and the zero set on `X_roots x Y_roots` is a perfect matching.

For quotient size `n`, arbitrary interpolation becomes generic once the
monomial support exceeds `n`.  The useful signal would be a separating
relation with:

```text
support = (deg_X + 1) * (deg_Y + 1) <= n.
```

Script:

```text
p24/abstract_embedded_pairing_low_bidegree_scan.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/abstract_embedded_pairing_low_bidegree_scan.py
```

Key rows:

```text
D=-2239, q=2243, quotient n=7:
  orient=1121, support 6, bidegree (2,1): 0/5040 matchings
  orient=1121, support 6, bidegree (1,2): 0/5040 matchings
  orient=1123, support 6, bidegree (2,1): 0/5040 matchings
  orient=1123, support 6, bidegree (1,2): 0/5040 matchings
  support 9, bidegree (2,2): 5040/5040 matchings, same as random controls
```

Summary:

```text
rows=16
low_support_rows=8
actual_low_support_rows_with_pairing=0
random_low_support_control_hits=0
```

Interpretation:

```text
support_gt_quotient_size_is_generic_interpolation_not_structure=1
support_le_quotient_size_pairing_would_be_non_generic_phase_evidence=1
abstract_quotient_coordinate_did_not_show_low_support_pairing=1
```

This does not rule out a genuine class-field tower morphism.  It does rule out
another cheap producer theorem:

```text
plain abstract quotient coordinate + low-bidegree relation
  => embedded phase pairing.
```

The surviving p24 target remains stronger and more explicit:

```text
construct the embedded relative class-character traces / selected child
polynomial coefficients directly, or bypass them with a p-unit/divisor
identity.
```
