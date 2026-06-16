# P25 KSY-y Yang Y507 Affine/Level Rigidity

Updated: 2026-06-14 09:05 PDT

## Purpose

The compact primitive word

```text
Y_507 = [2]^*U_507 / U_507^4
U_507 = z^121(1+z+z^2)(1-z^263)
```

has only 12 nonzero exponent residues.  This checkpoint asks whether that
compactness hides a lower-level pullback or affine symmetry that would make the
source theorem target cheaper.

## Affine Scan

All affine maps

```text
x -> u*x + b mod 507,  gcd(u,507)=1
```

were scanned.

Results:

```text
exact affine stabilizers      = {(1,0)}
negative affine stabilizers   = {(506,0)}
support affine stabilizers    = {(1,0), (506,0)}
translation stabilizers       = {0}
multiplicative support maps   = {1, -1}
```

So the exact word has trivial affine stabilizer.  The only nontrivial support
symmetry is inversion, and inversion sends the word to its negative.

## Lower Levels

Every proper divisor level fails the pullback test:

```text
level 1     pushforward support 0
level 3     pushforward support 0
level 13    pushforward support 10
level 39    pushforward support 12
level 169   pushforward support 12
```

The level `1` and level `3` pushforwards vanish.  The `13`, `39`, and `169`
pushforwards retain nonzero shadows, but none reconstructs the original word as
a lower-level pullback.

## Verdict

Positive payload:

```text
Y_507 is a genuine level-507 primitive word with trivial exact affine
stabilizer and inversion anti-invariance.
```

First missing clause:

```text
affine/level rigidity is structural data, not the finite-field value/divisor
theorem or DANGER3 extraction
```

Practical effect:

```text
source queries should preserve level 507 and inversion anti-invariance; do not
chase a lower-level pullback shortcut for this compact word
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_affine_level_rigidity_gate.py
```

Marker:

```text
ksy_y_yang_y507_affine_level_rigidity_rows=1/1
```
