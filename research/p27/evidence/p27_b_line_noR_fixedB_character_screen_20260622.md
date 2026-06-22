# P27 B-Line No-R Fixed-B Character Screen

Date: 2026-06-22

## Claim

The surviving quadratic fixed-`B` no-R subcovers have one visible support law
but no stable selected-gamma law.

Positive structural fact:

```text
beta_U_fixedB support = chi(B) = +1
```

on the tested fixed-`B` domain over `GF(q^2)` for
`q = 23, 71, 103, 167`.

Negative structural fact:

```text
gamma polarity on beta_U_fixedB is not stable across guard fields
hidden_mixed_fixedB gamma has no stable visible base-B character law
```

So `beta_U_fixedB` has a real base-`B` support gate, but it is not yet a
sqrt-beating source.  The selected class still needs divisor/Kummer extraction.

Norm-descent follow-up:
[P27 B-Line No-R Beta_U Norm Descent](p27_b_line_noR_betaU_norm_descent_20260622.md).
On the `chi(B)=+1` support, `gamma = chi(Unext+2)` descends exactly as
`chi_base(Norm(Unext+2))` across `q = 23, 71, 103, 167, 199, 263`.  The sign
is uniform on each active base `B`, and `gamma=+1` is exactly the half-size
`16`-point beta_U fiber case while `gamma=-1` is the full-size `32`-point
case.  This promotes beta_U from a bucket to a named norm/Kummer extraction
target, but still not to GPU production.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_fixedB_character_screen.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_character_screen_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_fixedB_character_screen.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_fixedB_character_screen_20260622.txt
```

## Method

For the two surviving fixed-`B` classes:

```text
beta_U_fixedB
hidden_mixed_fixedB
```

the probe tests exact pullback to visible base-`B` quadratic characters:

```text
named B-line atoms
all linear B-a characters
all monic irreducible quadratic B^2+uB+v characters
```

Targets:

```text
presence
gamma_plus
gamma_minus
plus_majority
```

## Result

`beta_U_fixedB` support:

```text
q=23:  exact B
q=71:  exact B
q=103: exact B
q=167: exact B
```

Equivalently, the fixed-`B` beta/U subcover appears exactly on the
`chi(B)=+1` half of the tested fixed-`B` domain.

`beta_U_fixedB` gamma polarity:

```text
q=23:  all gamma -
q=71:  all gamma +
q=103: all gamma -
q=167: mixed; no atom/linear/quadratic exact rule
```

`hidden_mixed_fixedB` presence:

```text
present on every fixed-B row in the tested target domain
```

`hidden_mixed_fixedB` gamma polarity:

```text
q=23:  gamma plus exact -chi(B-2)
q=71:  gamma plus exact  chi(B+2)
q=103: gamma plus exact -chi(B+2)
q=167: no atom/linear/quadratic exact rule
```

The small-field `B +/- 2` pattern is therefore not promoted.

## Interpretation

Positive:

```text
beta_U_fixedB has a real visible support gate: chi(B)=+1.
This is the first clean base-B law inside the surviving fixed-B subcovers.
The law is useful for CAS routing: beta_U lives over the square-B half.
```

Negative:

```text
The support gate does not select gamma.
beta_U gamma polarity is guard-field dependent.
hidden_mixed gamma has no stable visible atom/linear/quadratic law.
No direct GPU sampler follows from chi(B)=+1 unless CAS proves gamma descends there.
```

## CAS Consequence

Revise the fixed-`B` subtests:

```text
beta_U_fixedB:
  impose chi(B)=+1 as a support gate, then extract div(Unext+2) modulo squares.
  Promote only if gamma descends on this square-B quotient or couples f3/f4.

hidden_mixed_fixedB:
  treat as a fresh-looking fixed-B quadratic subcover.
  Do not promote B+/-2 atom patterns without a divisor proof.
```

GPU should not prefilter on `chi(B)=+1` alone.  It is a support shrink for one
diagnostic subcover, not a verified continuation source.

## Continue / Kill

```text
continue = beta_U_fixedB Kummer/divisor extraction on chi(B)=+1 support
continue = extract the beta_U norm class Norm(Unext+2)
continue = hidden_mixed_fixedB Kummer/divisor extraction without visible atom shortcut
continue = compare beta_U gamma class against f4/f3 after quotient extraction

kill = hidden_mixed B+/-2 atom shortcut after q167 failure
kill = beta_U gamma polarity as a visible base-B law
kill = treating beta_U norm descent alone as sqrt-beating
kill = GPU production from chi(B)=+1 support alone
```

```text
p27_b_line_noR_fixedB_character_screen_rows=1/1
```
