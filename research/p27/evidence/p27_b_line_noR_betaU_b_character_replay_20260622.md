# P27 B-Line No-R Beta_U B-Character Replay

Date: 2026-06-22

## Claim

The new beta_U norm-support split does not come from a cheap visible
base-`B` character in the tested heldout fields.

The replay over:

```text
199^2, 263^2, 311^2
```

confirms the old support law:

```text
beta_U_fixedB support = chi(B) = +1
```

but finds no exact atom, linear, or irreducible-quadratic `B` character for
the selected `gamma` side.  Since the norm-fiber profile proves that `gamma=+1`
is exactly the low-support norm side, this also kills the closest cheap
pre-enumeration explanation of that profile.

## Probe

Gate:

```text
research/p27/archive/gates/p27_b_line_noR_fixedB_character_screen.py
```

New output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_character_screen_q199_q263_q311_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_fixedB_character_screen.py \
  --fields 199^2,263^2,311^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_character_screen_q199_q263_q311_20260622.txt
```

## Result

For `beta_U_fixedB` support:

```text
q=199: exact B
q=263: exact B
q=311: exact B
```

For `beta_U_fixedB gamma_plus`:

```text
q=199:
  atoms exact = none
  linear exact = none
  irreducible quadratic exact = none

q=263:
  atoms exact = none
  linear exact = none
  irreducible quadratic exact = none

q=311:
  atoms exact = none
  linear exact = none
  irreducible quadratic exact = none
```

Best distances remain far from exact:

```text
q=199: best atom/linear distance 8; best irreducible quadratic distance 10
q=263: best atom/linear distance 16; best irreducible quadratic distance 16
q=311: best atom/linear distance 19; best irreducible quadratic distance 20
```

The same replay also keeps `hidden_mixed_fixedB` from becoming a shortcut:
presence is trivial, but gamma polarity has no exact atom, linear, or
irreducible-quadratic character in q199/q263/q311.

## Interpretation

Positive:

```text
The beta_U support gate chi(B)=+1 is stable through larger heldout fields.
The norm-support profile is still real and remains a CAS branch target.
```

Negative:

```text
The selected gamma / low-norm-support side is not a cheap B-line character
from named atoms, linear factors, or irreducible quadratic factors.
No GPU B-bucket source follows from the norm-support profile.
```

## Consequence

The beta_U lane remains:

```text
normalize the chi(B)=+1 beta_U support;
extract the norm map N_B = Norm(Unext+2);
explain the 1/8 versus 9/12/14/16 norm-support split as branch/ramification;
compare that class with f4/f3.
```

Do not spend GPU time on:

```text
chi(B) support alone;
B +/- c buckets;
irreducible quadratic B-buckets;
the low norm-support profile unless CAS turns it into a direct source map.
```

## Linked Artifacts

- [P27 B-Line No-R Fixed-B Character Screen](p27_b_line_noR_fixedB_character_screen_20260622.md)
- [P27 B-Line No-R Beta_U Norm-Fiber Profile](p27_b_line_noR_betaU_norm_fiber_profile_20260622.md)
- [P27 B-Line No-R Beta_U Norm Descent](p27_b_line_noR_betaU_norm_descent_20260622.md)
- [P27 No-R Quotient/Prym Test Packet](p27_noR_quotient_prym_test_packet_20260622.md)

```text
p27_b_line_noR_betaU_b_character_replay_rows=1/1
```
