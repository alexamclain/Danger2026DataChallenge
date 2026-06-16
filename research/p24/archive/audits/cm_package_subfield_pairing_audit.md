# CM Package Subfield Pairing Audit

This note implements the small audit suggested by the CM-subfield side pass:
compare abstract class-field/subfield roots with embedded subgroup-period
roots in small cyclic CM examples.

## Degree-2 genus toy

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_vs_embedded_quotient_toy.py
```

Output:

```text
D=-87
q=103
split_cycle_ell=7
abstract_bnrclassfield_degree_2=x^2 + 3
abstract_quotient_roots_mod_q=[10, 93]
embedded_cycle_sum_roots_mod_q=[4, 29]
possible_affine_pairings_alpha_to_Y=[(76, 68), (27, 68)]
```

Both the abstract quotient and the embedded cycle-sum quotient split over the
same finite field.  The abstract polynomial alone does not choose which root
corresponds to which embedded period root.  In degree `2`, this leaves only
two possible pairings, but it already shows that splitting is not pairing.

## Degree-5 non-genus toy

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_pairing_non_genus_toy.py
```

Output:

```text
D=-2239
q=2243
ell=5
class_number=35
quotient_size=5
subgroup_size=7
abstract_roots=[709, 834, 913, 987, 1043]
embedded_period_sums=[9, 106, 587, 812, 1142]
affine_set_maps_found=0
mobius_set_maps_found=0
```

Again, both quotient objects split.  But in this non-genus example there is no
affine or Mobius set map between the abstract roots and the embedded period
roots.  The pairing behaves like genuine extra embedded data.

I also added a small wrapper:

```text
p24/abstract_embedded_rational_pairing_scan.py
```

Its default run repeats the known non-genus case and searches for rational
degree-1 maps from an abstract quotient root set to the embedded period set:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_rational_pairing_scan.py
```

Output summary:

```text
rows=1
rows_with_low_degree_map=0
all_no_low_degree_map=1
```

The broader search mode is opt-in (`--scan`) because unconstrained
`bnrclassfield` discovery can become a CPU wait rather than a focused
mathematical test.

## Plain `j` selector degree

The direct finite-field selector identity toy gives a stronger calibration:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/embedded_selector_identity_toy.py
```

For `D=-5000`, `h=30`, quotient size `6`, and subgroup size `5`, the first
rational function of the plain `j` coordinate that recovers the quotient label
has degree exactly the generic interpolation threshold:

```text
data_pairs=30
generic_rational_interpolation_threshold=15
first_selector_degree=15
first_degree_equals_generic_threshold=1
```

So the embedded quotient label exists, but it does not appear as a special
low-degree identity in `j`.  This reinforces the finite-field degree theorem:
a selector constant on an `H`-coset must pay degree at least `|H|` somewhere.

## p24 consequence

For p24, a CM package subfield/tower output would be useful only if it
includes an explicit relation

```text
R(alpha, j) = 0
```

or equivalent tower relations that pair each abstract quotient root with the
correct embedded recovery factor in `j`.  A defining polynomial for the
degree-`66254` quotient, or a tower of abstract defining polynomials of
relative degrees `2,157,211`, is not enough by itself.

The small toys therefore support the same boundary as
`cm_subfield_tower_boundary.md`: subfield degrees are visible abstractly, but
the DANGER3 construction needs the embedded phase/recovery pairing.

The current selected-chain frontier uses this scan as a required falsifier for
future quotient-scale producer claims:

```text
p24/phase_chain_executable_frontier.md
```
