# P27 BSM Halving-Cover Identity

Date: 2026-06-22

## Claim

The staged BSM surface is not an independent source surface.  It is exactly the
ordinary selected halving cover written in different coordinates.

Starting from the BSM equation:

```text
m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
```

set:

```text
A = B^2 - 2
x = m^2 / 16
z = s^2
```

Then the BSM equation becomes:

```text
z^2 - 4*(x+1)*z - 4*x*(B^2-4) = 0.
```

The discriminant in `z` is:

```text
16*(x^2 + A*x + 1).
```

Thus a nondegenerate BSM point is exactly:

```text
x is square
x^2 + A*x + 1 is square
```

with extra sign choices.  This is the same one-step selected halving condition
already recorded in the B-line/Kummer lane, not a new multi-gate coupling.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_bsm_halving_cover_identity_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_bsm_halving_cover_identity_probe_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_bsm_halving_cover_identity_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_bsm_halving_cover_identity_probe_20260622.txt
```

## Guard-Field Results

The identities have zero failures:

```text
q1607: quadratic_identity_fail=0, z_discriminant_identity_fail=0
q1847: quadratic_identity_fail=0, z_discriminant_identity_fail=0
q2087: quadratic_identity_fail=0, z_discriminant_identity_fail=0
```

Every nondegenerate BSM point has square `x` and square halving discriminant:

```text
q1607: x_not_square=0, d_not_square=0, discriminant_not_square=0
q1847: x_not_square=0, d_not_square=0, discriminant_not_square=0
q2087: x_not_square=0, d_not_square=0, discriminant_not_square=0
```

The legal target incidence is exactly the d3-plus side:

```text
q1607: d3plus_bax_points=896, d3minus_bax_points=0, d3plus lifts per row=8
q1847: d3plus_bax_points=1440, d3minus_bax_points=0, d3plus lifts per row=8
q2087: d3plus_bax_points=800, d3minus_bax_points=0, d3plus lifts per row=8
```

## Interpretation

Positive:

```text
BSM is now algebraically identified with a known selected-halving cover.
The equation is still a compact coordinate for CAS notes.
The eightfold lift explains the uniform target fibers seen in earlier BSM screens.
```

Negative:

```text
BSM does not add a new source denominator.
BSM does not couple two selected gates.
BSM cannot be promoted as a separate GPU/source lane unless a new quotient is
named after adding additional Kummer classes.
```

This explains the earlier observations:

```text
raw BSM surface size ~= q^2
legal-B-restricted BSM keeps the legal-B denominator
next-selector low-degree screens see only the inherited surface equation
```

## Continue / Kill

```text
continue = use BSM only as notation for the known x-square plus d-square cover
continue = compare any future BSM quotient directly against the B-line Kummer class
continue = only revive BSM if an added selector creates a genuinely new low-genus quotient

kill = BSM as an independent first-class moonshot lane
kill = GPU sampling of raw or legal-B-restricted BSM
kill = interpreting the BSM equation as multi-gate coupling
kill = further BSM low-degree screens without an added non-inherited selector
```

```text
p27_bsm_halving_cover_identity_rows=1/1
```
