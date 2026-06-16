# p25 Lane B Square-Axis Bridge Theta31 Affine Obstruction

Updated: 2026-06-12

## Result

The canonical square-axis `theta_{3,1}` near miss is not the primitive bridge
under an affine, diamond, or Frobenius-style reindexing of `C_507`.

The checked theta edge directions are the full support-`<=12` family:

```text
directions = 163, 172, 335, 344
support sizes = 12, 6, 6, 12
```

Every affine endomorphism `q -> a*q + b mod 507` was scanned.  None maps any of
these supports to the primitive bridge support.  Therefore affine automorphism
subfamilies, including diamond/Frobenius relabelings, cannot repair signs or
coefficients either.

For affine units the obstruction is already visible in the ordered-difference
profile:

```text
bridge:      gcd differences = {1: 24, 3: 6}
theta +/-D:  gcd differences = {1: 18, 3: 6, 169: 6}
theta +/-2D: gcd differences = {1: 84, 3: 36, 169: 12}
```

The theta near-miss has internal `169`-separated pairs.  The primitive bridge
has none.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_theta31_affine_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_theta31_affine_obstruction_rows=1/1
```

## Continue / Kill

Kill the affine/diamond/Frobenius reindexing escape for the canonical
`theta_{3,1}` edge family.  Continue only if the theta packet itself is
changed, or if a new arithmetic factor realizes the primitive bridge directly.
