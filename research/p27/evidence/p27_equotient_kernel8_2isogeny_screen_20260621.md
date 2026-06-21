# P27 E-Quotient Kernel-8 / 2-Isogeny Screen

Date: 2026-06-21

## Claim

The descended `d3` and `d4` bits have a real additional symmetry: on p27 they
are invariant under the rational 2-torsion translation `(X,W) -> (-1/X,W/X^2)`
whenever both points remain in the compactD label-2 domain.

Equivalently, the active quotient problem descends from

```text
E: W^2 = X^3 - X
```

to the 2-isogenous quotient by `(0,0)`:

```text
U = X - 1/X
V = W*(X^2 + 1)/X^2
V^2 = U^3 + 4U.
```

This is positive structure, but it is not yet sqrt-beating.  After quotienting,
exact line and two-line screens over the non-degenerate fields `q=1471` and
`q=1607` are still negative.

## How We Found It

The small-field group projection screen tested whether d3/d4 are functions of
small projections of `E(F_q)`.  The standout projection was consistently
`m=(q+1)/8`, i.e. the class of `[8]P`.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_group_projection_probe.py \
  --small-primes 1087,1471,1607 \
  --max-modulus 256 \
  --top 10 \
  | tee research/p27/archive/probe_outputs/p27_equotient_group_projection_probe_20260621.txt
```

Key small-field results:

```text
q=1087, m=(q+1)/8=136:
  d3 exact on signed/unsigned projection classes
  d4 not exact

q=1471, m=(q+1)/8=184:
  d3 near-exact: 192/200, only 1 signed mixed class
  d4 not exact

q=1607, m=(q+1)/8=201:
  d3 exact on signed/unsigned projection classes
  d4 exact on signed/unsigned projection classes
```

This was too structured to ignore, but small fields alone could have been a
projection artifact.  The p27 test therefore forced actual `[8]`-fiber
collisions.

## P27 Kernel Test

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_kernel8_invariance_probe.py \
  --target 1000 \
  --max-draws 500000 \
  --kernel-max-draws 2000 \
  | tee research/p27/archive/probe_outputs/p27_equotient_kernel8_invariance_probe_20260621.txt
```

Since `#E(F_p)=p+1=8*125000000000000000000000013`, multiplying random
E-points by the odd part generated the full rational kernel killed by `[8]`:

```text
kernel_points = 8
random_points_needed = 16
```

On 1,000 p27 quotient rows:

```text
base_rows = 1000
base_d4_rows = 484
d3_orbit_domain_size_2 = 1000
translated_in_d3_domain = 2000
translated_not_in_d3_domain = 6000
mixed_d3_orbits = 0
mixed_d4_orbits = 0
```

The per-kernel counters identify the structure:

```text
kernel_0 = O        in d3 domain for all 1000 rows
kernel_1 = (0,0)    in d3 domain for all 1000 rows
kernel_2..7         never in d3 domain on this sample
```

Thus the actionable symmetry is not the whole rational `[8]` kernel.  The
compactD domain intersects each sampled `[8]` fiber in the two-point orbit
under translation by `(0,0)`, and both `d3` and `d4` are invariant on that
orbit.

## 2-Isogeny Quotient Screen

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_2isogeny_line_probe.py \
  --p27-target 1000 \
  --p27-heldout-target 1000 \
  --max-draws 300000 \
  --small-primes 1087,1471,1607 \
  --p27-line-bound 2 \
  --pair-limit 4 \
  | tee research/p27/archive/probe_outputs/p27_equotient_2isogeny_line_probe_20260621.txt
```

The quotient map is clean in p27 and in the small fields: no mixed rows appear
after mapping `(X,W)` to `(U,V)`.

P27 small-coefficient line sanity:

```text
p27 train d3 best = 560/1000 = 0.560000000
p27 heldout d3 best = 530/1000 = 0.530000000
p27 train d4 best = 270/484 = 0.557851240
p27 heldout d4 best = 294/526 = 0.558935361
exact small-coefficient lines = 0
```

The `q=1087` quotient rows are small and show accidental-looking positives:

```text
q1087 quotient d3 rows = 36
q1087 d3 exact two-line pairs = 36
q1087 quotient d4 rows = 20
q1087 d4 exact lines = 3
```

The non-degenerate guard fields kill those as promotion evidence:

```text
q1471 quotient d3 rows = 100
q1471 d3 exact lines = 0
q1471 d3 exact two-line pairs = 0

q1471 quotient d4 rows = 56
q1471 d4 exact lines = 0
q1471 d4 exact two-line pairs = 0

q1607 quotient d3 rows = 98
q1607 d3 exact lines = 0
q1607 d3 exact two-line pairs = 0

q1607 quotient d4 rows = 56
q1607 d4 exact lines = 0
q1607 d4 exact two-line pairs = 0
```

## Interpretation

Positive:

```text
d3/d4 descend through a concrete rational 2-isogeny.
The right quotient coordinates are now named: U=X-1/X, V=W(X^2+1)/X^2.
This halves the active quotient surface and gives a sharper function-field target.
The small-field [8] projection lead was not random; it reflects the (0,0) orbit.
```

Negative:

```text
The symmetry is only a factor-2 quotient by itself.
Lines and two-line products on the 2-isogenous quotient are killed by q=1471/q=1607.
The q1087 exact formulas are small-row coincidences.
No GPU sampler follows from the quotient alone.
```

Follow-up status:

```text
The first random low-pole section/product screen directly on E' is also negative.
No exact p27 or q1471/q1607 candidate appeared at pole bounds 5, 7, or 9.
Best p27 heldout lifts are weak: 0.5225 for d3 and 0.5295 for d4.
The first E' affine-walk recurrence screen is negative as well: for |m|<=8
and all Q over q=1471,1607,1847, only identity/negation have full coverage,
and they score like raw d4 bias.
```

## Concrete Next Tests

1. Function-field extraction on the quotient curve:

```text
Work over E': V^2 = U^3 + 4U instead of E.
Extract the actual d3/d4 double covers and compare divisor/Kummer classes there.
```

2. Irreducible conic / low-degree section screen on `E'`:

```text
If doing finite-field search, search on the 2-isogenous quotient coordinates.
Do not spend more time on lines or reducible two-line products.
```

3. Magma validation:

```text
Use the online Magma calculator for small-field checks of any named formula on
E'.  Validation fields should include q=1471 or q=1607, not only q=1087.
```

## Continue / Kill

```text
continue = E' function-field extraction for d3/d4
continue = divisor-class comparison on the 2-isogenous quotient
continue = exact irreducible-conic screen on E' if tractable

kill = treating [8] projection as a full p27 source by itself
kill = line/two-line source on E'
kill = promoting q1087 quotient exact lines/products without q1471/q1607 support
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_equotient_group_projection_probe.py`
- Gate: `research/p27/archive/gates/p27_equotient_kernel8_invariance_probe.py`
- Gate: `research/p27/archive/gates/p27_equotient_2isogeny_line_probe.py`
- Gate: `research/p27/archive/gates/p27_eprime_lowpole_random_probe.py`
- Gate: `research/p27/archive/gates/p27_eprime_affine_walk_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_equotient_group_projection_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_equotient_kernel8_invariance_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_equotient_2isogeny_line_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_eprime_lowpole_random_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_q1847_20260621.txt`
- Related: [P27 E-Quotient Affine-Walk Recurrence](p27_equotient_affine_walk_recurrence_20260621.md)
- Related: [P27 E-Quotient Line-Product Screen](p27_equotient_line_product_screen_20260621.md)
- Related: [P27 E-Prime Low-Pole Random Screen](p27_eprime_lowpole_random_screen_20260621.md)
- Related: [P27 E-Prime Affine-Walk Recurrence](p27_eprime_affine_walk_recurrence_20260621.md)

```text
p27_equotient_kernel8_2isogeny_screen_rows=1/1
```
