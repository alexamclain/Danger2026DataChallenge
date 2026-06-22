# P27 B-Line No-R Quadratic Subcover Classifier

Date: 2026-06-22

## Claim

The quadratic fixed-`B` no-R behavior splits into stable named mechanisms, and
one of the tempting subtests is now dead:

```text
WT-only quadratic extension = stable zero-selector branch, not a gamma source
```

Across `GF(q^2)` for `q = 7, 23, 71, 103, 167`, the `WT_only_zero` class has
exactly `8` points and always `gamma_chi = 0`.  That makes it a
ramification/zero-selector artifact, not a selected-branch source.

The live quadratic fixed-`B` subcovers are therefore:

```text
beta_U_fixedB
hidden_mixed_fixedB
```

The degree-2 `B_orbit` class remains separate from fixed-`B` fiber splitting.

Fixed-B character follow-up:
[P27 B-Line No-R Fixed-B Character Screen](p27_b_line_noR_fixedB_character_screen_20260622.md).
The `beta_U_fixedB` support is exactly `chi(B)=+1` on the tested fixed-`B`
domain over `q = 23, 71, 103, 167`, but gamma polarity on that support is not
stable.  The `hidden_mixed_fixedB` gamma atom patterns seen in smaller fields
fail at `q=167`.  Thus `chi(B)=+1` is a real support gate for beta_U, not a
selected-gamma source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_quadratic_subcover_classifier.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_quadratic_subcover_classifier_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_quadratic_subcover_classifier.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_quadratic_subcover_classifier_20260622.txt
```

## Result

Class counts:

```text
field    B_orbit        WT_zero  base_point  beta_U_fixedB    hidden_mixed_fixedB
7^2      0              8        0           0                0
23^2     384            8        0           64               192
71^2     4352           8        128         128              768
103^2    8704           8        0           384              1152
167^2    24320          8        96          544              1920
```

Gamma splits:

```text
field    B_orbit gamma     beta_U gamma      hidden_mixed gamma
23^2     -192 / +192       -64 / +0          -128 / +64
71^2     -2176 / +2176     -0 / +128         -256 / +512
103^2    -4352 / +4352     -384 / +0         -768 / +384
167^2    -11776 / +12544   -448 / +96        -1088 / +832
```

Stable zero branch:

```text
field    WT_only_zero gamma_0
7^2      8
23^2     8
71^2     8
103^2    8
167^2    8
```

## Interpretation

Positive:

```text
The quadratic no-R mechanisms now have stable names.
WT-only can be removed from the active source search.
The remaining fixed-B quadratic subcovers are beta_U_fixedB and hidden_mixed_fixedB.
The B_orbit class is large and separate, with near-balanced gamma splits.
```

Negative:

```text
No quadratic class gives a stable selected gamma source law.
beta_U_fixedB polarity changes across guard fields.
hidden_mixed_fixedB polarity also changes across guard fields.
base_point rows are field-local and not a stable route.
WT-only is gamma=0, so it cannot produce selected gamma.
No GPU production mode follows.
```

## CAS Consequence

Revise the no-R CAS queue:

```text
keep = cubic/degree-2 B-orbit quotient/component test
keep = beta_U_fixedB quadratic fixed-B subcover test
keep = hidden_mixed_fixedB quadratic fixed-B subcover test
kill = WT-only quadratic fixed-B subcover as selected-gamma source
kill = base_point rows as a stable source route
```

For the two surviving fixed-`B` subcovers, CAS should compute whether their
Kummer classes are pullbacks, coboundaries, or fresh half-covers.  Promote only
if one carries gamma or couples f3/f4 through a sourceable quotient/Prym
factor.

## Continue / Kill

```text
continue = beta_U_fixedB divisor/class extraction
continue = hidden_mixed_fixedB divisor/class extraction
continue = B_orbit quotient/component comparison
continue = impose chi(B)=+1 only as beta_U support, not as gamma selector

kill = WT-only fixed-B subcover as a gamma source
kill = base_point rows as a stable sqrt-beating source
kill = hidden_mixed B+/-2 atom shortcut after q167 failure
kill = GPU production from any quadratic bucket without a named map
```

```text
p27_b_line_noR_quadratic_subcover_classifier_rows=1/1
```
