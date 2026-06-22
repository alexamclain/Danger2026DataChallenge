# P27 B-Line No-R Genus Pressure

Date: 2026-06-22

## Claim

The localized no-R reduced B-line cover does not look like a simple low-genus
source in the existing extension-field counts.

This is not a normalization result.  It applies the one-component Hasse-Weil
pressure test to the already-computed affine localized counts.  If the no-R
reduced cover were a single smooth projective component after adding boundary
points, then:

```text
N_aff <= N_proj <= q + 1 + 2*g*sqrt(q).
```

Removed denominator/boundary points only decrease the affine count, so positive
excess over `q+1` gives a one-component genus lower bound.  If the
one-component interpretation is wrong, the same data points to nontrivial
component or field-of-definition behavior rather than a simple genus-0/1
source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_genus_pressure_probe.py
```

Input:

```text
research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_20260622.txt
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_genus_pressure_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_noR_genus_pressure_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_genus_pressure_probe_20260622.txt
```

## Result

```text
field  q       noR_U  noR/q      excess  g_min_if_one_component  genus1_margin
607^1  607     1044   1.719934   436     9                       386.725
7^3    343     288    0.839650   -56     0                       -93.041
7^4    2401    1688   0.703040   -714    0                       -812.000
7^5    16807   18880  1.123341   2072    8                       1812.716
7^6    117649  124808 1.060850   7158    11                      6472.000
23^2   529     648    1.224953   118     3                       72.000
23^3   12167   12768  1.049396   600     3                       379.392
```

Summary:

```text
positive_excess_fields = 5/7
genus_one_violations_if_one_component = 5/7
max_g_min_if_one_component = 11
```

Closed-point follow-up:
[P27 B-Line No-R Closed-Point Pressure](p27_b_line_noR_closed_point_pressure_20260622.md).
After adding the missing low-degree counts, the affine Mobius transform has no
degree-1 closed points but nonzero coprime degree-2 and degree-3 closed points
over both base `7` and base `23`.  Thus the next CAS pass must compare degree
`2` and `3` base changes and Frobenius component permutation; a single
extension-degree unlock is not supported.

## Interpretation

Positive:

```text
The no-R cover remains the right first normalization target after compactD_R
was demoted.
The count data gives a cheap falsifier for the simplest low-genus-source hope.
```

Negative:

```text
Under a one-component reading, genus <= 1 is incompatible with 5/7 counts.
The strongest single-field pressure gives g >= 11.
If not one component, there is nontrivial component/field-of-definition behavior.
No direct sampler or GPU mode follows from these counts.
```

## Continue / Kill

```text
continue = offline normalize the no-R reduced cover to resolve genus/components
continue = look for quotient/Prym/component decompositions, not just a genus-0/1 source
continue = compare gamma/f4 only after the no-R component structure is known

kill = expecting the localized no-R cover to be an obvious genus-0/1 source
kill = GPU production from no-R count data alone
kill = treating extension-field count oscillations as a sampler without a map
```

```text
p27_b_line_noR_genus_pressure_rows=1/1
```
