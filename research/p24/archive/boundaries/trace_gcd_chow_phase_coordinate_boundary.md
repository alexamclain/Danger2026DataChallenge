# Trace-GCD Chow Phase-Coordinate Boundary

Date: 2026-06-06

This note records the phase-aware follow-up to the plain-`j` divisor scan.

The plain scan showed that the selected trace-GCD Chow determinant is not a
low-degree function of `j_i` or of the one-edge coordinate `(j_i,j_{i+1})`.
The next question is whether keeping the hidden right phase coordinate
actually buys structure.

## Audit

The diagnostic is:

```text
p24/trace_gcd_chow_phase_coordinate_scan.py
```

It checks:

```text
1. whether determinant values factor through alpha mod right;
2. the Berlekamp-Massey order of the resulting right-phase sequence;
3. DFT/Frobenius support over the right roots of unity;
4. the p24 exterior-support comparison for right=211, tail=16.
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_chow_phase_coordinate_scan.py \
  --max-factor-degree 8 \
  --max-extension-degree 8 \
  --min-left-orbit-len 2 \
  --max-origin-shifts 140 \
  --skip-plain-degree
```

## Small Actual-CM Result

For the pinned row:

```text
D=-13319
q=13463
h=140
m=28
n=5
pair=(4,7)
right_order=3
frobenius_orbits=[[0], [1,2,4], [3,6,5]]
```

both omitted blocks satisfy:

```text
right_class_mismatches=0
phase_compression_factor=20
right_zero_count=0
bm_order=3
connection_divides_xn_minus_1=1
```

The DFT support is exactly one nonzero Frobenius orbit:

```text
omitted=0:
  dft_support=[3,5,6]
  dft_support_full_orbits=[2]
  one_full_nonzero_orbit_support=1

omitted=1:
  dft_support=[1,2,4]
  dft_support_full_orbits=[1]
  one_full_nonzero_orbit_support=1
```

The orbit products are nonzero:

```text
omitted=0:
  right_orbit_products=[(0,1,2125), (1,3,2515), (2,3,603)]

omitted=1:
  right_orbit_products=[(0,1,11423), (1,3,9495), (2,3,6085)]
```

So in this row the phase coordinate explains the determinant cleanly:
`140` origin values compress to a right-phase function of length `7`, and
that function has one-orbit DFT support.

## p24 Warning

The same script prints the p24 exterior support comparison:

```text
p24_right=211
p24_p_mod_right=114
p24_orbit_len=35
p24_tail=16
distinct_subset_sum_size_k1=35
distinct_subset_sum_size_k2=210
distinct_subset_sum_size_k3=211
distinct_subset_sum_size_k16=211
full_support_by_k3=1
```

Thus p24 has full possible right-frequency support already by subset size
`3`, far before the actual tail size `16`.  A p24 one-orbit phase theorem
would need special arithmetic cancellation among the CM Plucker coefficients.
It is not forced by the right action.

A bounded right-`11` row-discovery probe:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_spectral_scan.py \
  --only-right 11 \
  --include-linear \
  --require-square-tail \
  --require-prime-right \
  --min-tail-len 1 \
  --max-rows 4 \
  --max-cases 8 \
  --max-abs-D 70000 \
  --q-stop 200000 \
  --max-factor-degree 10 \
  --max-extension-degree 10 \
  --min-left-orbit-len 2
```

returned `rows=0`; it gives no additional evidence either way.

## Consequence

The phase-aware direction is real, but the safe p24 theorem remains the
seven-orbit Chow/Fitting norm theorem:

```text
construct Pi_O = prod_{t in O} Delta(t)
and prove each Pi_O is a p-unit.
```

The stronger theorem

```text
f_trace has support on a single degree-35 right Frobenius orbit
```

would further simplify the producer, but it now has to be treated as a new
arithmetic cancellation theorem.  The current evidence does not justify
assuming it.
