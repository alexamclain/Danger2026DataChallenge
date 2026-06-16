# Lang Trace-GCD Plucker-Kummer Descent Boundary

Date: 2026-06-05

## Question

Can the determinant-level Kummer payload descend as individual values

```text
Theta(t) = unit(t) * Delta(t)^r,
```

or does the cyclic labeling force us to use Frobenius orbit products/norms?

## Actual-CM Audit

Added:

```text
p24/lang_trace_gcd_plucker_kummer_descent_audit.py
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_plucker_kummer_descent_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

The row has:

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7
q mod 7 = 2
Frobenius orbits on Z/7Z: [0], [1,2,4], [3,6,5]
```

For both omitted rows, the reduced right sequence has no mismatches and all
orbit products are nonzero:

```text
omitted=0:
  right_values=[2125, 6973, 11434, 2597, 12105, 2133, 3022]
  orbit products: 2125, 2515, 603
  full right product: 6352

omitted=1:
  right_values=[11423, 4693, 4157, 13397, 8480, 3228, 8474]
  orbit products: 11423, 9495, 6085
  full right product: 6639
```

But individual values do not descend on the nontrivial orbits:

```text
raw_descended_orbits=1/3
nontrivial_power_descended_orbits_any_tested=1/3
orbit_product_nonzero_count=3/3
```

The only power that descends on all nonzero orbits is the tautological
`q-1` power, which sends every nonzero value to `1`; it carries no determinant
information.

## Consequence

The over-strong theorem

```text
Delta(t)^r descends orbitwise as an individual scalar
```

is not supported by the actual-CM row unless one proves an additional
semi-invariant Plucker-line condition.

The robust theorem target is instead:

```text
Pi_O = prod_{t in O} Delta(t)
```

or the corresponding determinant-level Kummer norm

```text
Theta_O = prod_{t in O} unit(t) * Delta(t)^r.
```

This matches the seven-orbit payload in the certificate manifest.  It also
keeps the producer theorem honest: the class-field construction must output
the actual orbit product/norm, not an unrelated nonzero scalar.

## Updated Frontier

The finite verifier is still tiny:

```text
seven orbit products + inverses = 14 base-field elements.
```

The missing arithmetic theorem is now sharper:

```text
Construct the determinant/Plucker orbit norms of the trace-GCD section inside
the embedded class-field tower and prove each is a p-unit at the selected
prime over p.
```

The individual Plucker-Kummer payload remains possible only as a special
case:

```text
chosen Plucker coordinate is semi-invariant under the hidden cyclic action.
```

The actual-CM audit says not to assume that special case.
