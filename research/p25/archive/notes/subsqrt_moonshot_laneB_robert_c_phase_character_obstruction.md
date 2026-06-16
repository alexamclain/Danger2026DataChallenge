# Subsqrt Moonshot Lane B Robert C-Phase Character Obstruction

Date: 2026-06-13

## Result

The active C-side odd phase needed by the Robert/Siegel lane cannot be a plain
character or sign tag on `C_169`.

The required active phase is:

```text
+ on C-values 25, 28, 31
- on C-values 138, 141, 144 = -31, -28, -25 mod 169
```

Since `C_169` has odd order, there is no nontrivial homomorphism

```text
C_169 -> {+1,-1}.
```

And for a 169th-root character `chi_b`, an odd phase would require

```text
chi_b(-c) = -chi_b(c)
```

on an active C-pair.  That would force `-1` to be a 169th root of unity, which
is impossible.

## Producer Consequence

The Robert/Siegel phase must come from an oriented divisor, quotient of
conjugate units, `y`/differential data, or another non-character finite
identity.  A scalar-normalized C-character, Legendre-style tag, or simple
root-of-unity phase is not enough.

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_c_phase_character_obstruction_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_c_phase_character_obstruction_gate.py
```
