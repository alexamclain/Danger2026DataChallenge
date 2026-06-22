# P27 B-Line No-R Beta_U Norm-Fiber Profile

Date: 2026-06-22

## Claim

The `beta_U_fixedB` norm class has a sharper finite-field signature than just
`gamma = chi_base(Norm(Unext+2))`.

Across every tested quadratic guard field, the selected sign is exactly the
low-support profile of the norm map:

```text
gamma = +1  <=>  distinct Norm(Unext+2) values per B <= 8
gamma = -1  <=>  distinct Norm(Unext+2) values per B > 8
```

with zero mismatches in:

```text
23^2, 71^2, 103^2, 167^2, 199^2, 263^2, 311^2.
```

This is not a sampler by itself.  It is a more precise CAS target: explain the
branch/ramification profile of the norm map on the `chi(B)=+1`
`beta_U_fixedB` support.

## Probe

Gate:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_norm_fiber_profile_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_fiber_profile_probe_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_fiber_profile_probe.py \
  --fields 23^2,71^2,103^2,167^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_fiber_profile_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_fiber_profile_probe.py \
  --fields 199^2,263^2,311^2 \
  | tee -a research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_fiber_profile_probe_20260622.txt
```

## Result

Summary:

```text
field   active B   gamma+ profile                 gamma- profile             mismatches
23^2    2          none                           norm values 9,10           0
71^2    8          norm values 1,8                none                       0
103^2   12         none                           norm values 9,12,14,16     0
167^2   20         norm values 1,8                norm values 9,12,14,16     0
199^2   24         norm values 1,8                norm values 9,12,16        0
263^2   32         norm values 1,8                norm values 9,12,14,16     0
311^2   38         norm values 1,8                norm values 9,12,14,16     0
```

The multiplicity profiles are also stable:

```text
gamma+:
  16 points, 1 norm value:  16x1
  16 points, 8 norm values: 2x8

gamma-:
  32 points, 9 norm values:  2x8,16x1
  32 points, 12 norm values: 2x8,4x4
  32 points, 14 norm values: 2x12,4x2
  32 points, 16 norm values: 2x16
```

Every active base `B` has a uniform norm squareclass:

```text
B_norm_sign_conflicts = 0
```

and the cutoff test has no exceptions:

```text
norm_value_cutoff_8_mismatch = 0
```

Visible precursor replay:
[P27 B-Line No-R Beta_U B-Character Replay](p27_b_line_noR_betaU_b_character_replay_20260622.md)
checks the closest cheap explanation in the heldout fields `q=199,263,311`.
The beta_U support remains exactly `chi(B)=+1`, but the `gamma=+1`
low-support side has no exact named atom, linear, or irreducible-quadratic
`B` character.  Thus the norm-support profile is a branch/ramification target,
not a B-bucket source.

Next-gate quotient follow-up:
[P27 B-Line No-R Beta_U Norm/F4 Descent](p27_b_line_noR_betaU_norm_f4_descent_20260622.md)
shows that the norm map does not carry `f4`.  In
`71^2,167^2,199^2,263^2,311^2`, `f4` is mixed on every active `B`, and remains
mostly mixed even after grouping by the finer quotient `(B, Norm(Unext+2))`.
So beta_U is a one-gate/materialization class unless a non-visible normalized
Prym relation appears.

## Interpretation

Positive:

```text
The beta_U norm class has a visible ramification/fiber-profile signature.
The selected sign is not merely a pointwise Legendre bucket.
The 16/32 point split is refined by a stable norm-support split.
This gives CAS a branch-profile target for the beta_U quotient/Prym pass.
```

Negative:

```text
Counting distinct norm values per B is not a source sampler.
It still requires enumerating the beta_U fiber, so it does not beat sqrt.
It does not explain f4; the beta_U next-gate probe already shows f4 is mixed
inside every gamma-positive active B row.
```

## CAS Consequence

The beta_U subtest should now ask for:

```text
the norm map N_B = Norm(Unext+2) on the chi(B)=+1 beta_U support;
branch/ramification divisor explaining support degrees 1,8 versus 9,12,14,16;
whether the low-support side is a quotient/Prym factor or just ramification
of a high-genus fresh Kummer cover;
comparison of this norm-map ramification class with the f4/f3 class.
```

Promote only if the branch profile descends to a low-genus/sourceable quotient
or couples to the next Kummer class.  Otherwise this remains a good diagnostic
for a fresh half-cover, not a GPU production mode.

## Continue / Kill

```text
continue = beta_U quotient/Prym extraction using norm-support profile as a target
continue = compare beta_U norm ramification with f4/f3 after normalization
continue = include norm-value support counts in offline CAS regression
continue = include (B,N) f4 mixed counts as a next-gate regression

kill = treating distinct norm-value count as a production sampler
kill = GPU beta_U buckets without a source map
kill = atom/linear/quadratic B-character explanations for the low-support side
kill = f4 as a function of B, N, or (B,N)
kill = broad visible (B,Norm) plane-curve scans already killed through B12_N16
```

## Linked Artifacts

- [P27 B-Line No-R Beta_U Norm Descent](p27_b_line_noR_betaU_norm_descent_20260622.md)
- [P27 B-Line No-R Beta_U B-Character Replay](p27_b_line_noR_betaU_b_character_replay_20260622.md)
- [P27 B-Line No-R Beta_U Norm/F4 Descent](p27_b_line_noR_betaU_norm_f4_descent_20260622.md)
- [P27 B-Line No-R Beta_U Norm Relation Screen](p27_b_line_noR_betaU_norm_relation_20260622.md)
- [P27 B-Line No-R Beta_U Next-Gate Probe](p27_b_line_noR_betaU_next_gate_20260622.md)
- [P27 No-R Quotient/Prym Test Packet](p27_noR_quotient_prym_test_packet_20260622.md)

```text
p27_b_line_noR_betaU_norm_fiber_profile_rows=1/1
```
