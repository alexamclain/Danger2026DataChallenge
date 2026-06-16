# Tower Kummer Phase Complexity Boundary

Date: 2026-06-05

This note tests whether the relative Kummer normal form gives a real
coefficient collapse for embedded tower phases.

## Question

For a prime child layer:

```text
h = a * r * n
```

with parent periods `Z_u` and child periods `y_{u+a*v}`, define:

```text
T_s(u) = sum_v zeta_r^(s*v) y_{u+a*v}
K_s(u) = T_s(u)^r.
```

The Kummer powers `K_s` are equivalent phase payloads for the unordered child
polynomial.  The question is whether their coordinates are simpler functions
of the parent period `Z_u` than the child-polynomial coefficients were.

## Script

I added:

```text
p24/tower_kummer_phase_complexity_scan.py
```

The scan:

```text
1. builds small complete embedded CM cycles;
2. chooses quotient slices with prime child degree r;
3. adjoins mu_r when needed using a finite extension;
4. computes coordinate functions of K_s(u)=T_s(u)^r;
5. interpolates those coordinates as functions of the parent period Z_u;
6. measures Berlekamp-Massey complexity across parent order.
```

## Results

Small pinned run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_kummer_phase_complexity_scan.py \
  --max-cases 8 --min-h 12 --max-h 90 --max-abs-D 12000 \
  --q-stop 150000 --min-quotient 6 --max-quotient 60 \
  --min-parent 3 --max-parent 20 --max-child 11 \
  --max-zeta-degree 10 --min-recovery 2 \
  --max-rows-per-case 8 --summary-only
```

reported:

```text
rows=12
good_distinct_rows=12
kummer_coordinate_slots=25
full_degree_coordinates=25
low_degree_coordinates=0
low_bm_coordinates=0
```

Broader seconds-scale run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_kummer_phase_complexity_scan.py \
  --max-cases 20 --min-h 12 --max-h 140 --max-abs-D 25000 \
  --q-stop 350000 --min-quotient 6 --max-quotient 100 \
  --min-parent 3 --max-parent 36 --max-child 13 \
  --max-zeta-degree 12 --min-recovery 2 \
  --max-rows-per-case 12 --summary-only
```

reported:

```text
rows=30
good_distinct_rows=29
kummer_coordinate_slots=55
full_degree_coordinates=55
low_degree_coordinates=0
low_bm_coordinates=0
```

## Consequence

The Kummer normal form is still valuable in a one-Frobenius-orbit relative
layer:

```text
relative child polynomial
  <=> parent trace + relative Kummer powers T_s^r.
```

The multi-orbit case needs an extra caveat.  The finite ambiguity gate

```text
p24/relative_kummer_multi_orbit_ambiguity_gate.py
p24/relative_kummer_multi_orbit_ambiguity_gate.md
```

shows that if Frobenius has `g>1` primitive-character orbits, independent
root-of-unity phases on those orbits still descend to `F_q` child fibers.
Thus the unordered child polynomial is not selected by the Kummer powers alone.
For p24 this affects the `211` layer:

```text
ord_211(p)=35, primitive-character_orbits=6,
cross_orbit_phase_ambiguity_after_global_shift=211^5.
```

But small CM data does not support a further low-degree formula:

```text
K_s as a simple function of parent period Z_u.
```

So the current positive theorem should not hope for a tiny interpolation
identity in parent periods.  It should target the Kummer powers directly as
class-field/Lagrange-resolvent objects.

For p24 this means:

```text
157 layer: construct one Frobenius orbit of 156 Kummer powers;
211 layer: construct six Frobenius orbits of 35 Kummer powers plus
           cross-orbit phase glue, or construct the selected child polynomial;
then construct one selected degree-3107441 recovery polynomial.
```

This is still sub-sqrt as a certificate payload, but it remains a genuine
embedded class-field phase theorem.
