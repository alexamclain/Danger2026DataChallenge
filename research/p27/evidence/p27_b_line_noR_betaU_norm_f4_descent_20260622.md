# P27 B-Line No-R Beta_U Norm/F4 Descent

Date: 2026-06-22

## Claim

The beta_U norm map does not carry the next selected gate.

After restricting to:

```text
beta_U_fixedB
gamma = chi_base(Norm(Unext+2)) = +1
N = Norm(Unext+2)
```

the next sign `f4` is still mixed on the finer quotient coordinate `(B,N)` in
every tested field:

```text
71^2, 167^2, 199^2, 263^2, 311^2.
```

This kills the nearest two-gate beta_U quotient shortcut.  The beta_U norm
class remains a real f3/materialization Kummer class and branch-profile target,
but the next gate is not a function of the norm-map quotient.

## Probe

Gate:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_norm_f4_descent_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_f4_descent_probe_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_f4_descent_probe.py \
  --fields 71^2,167^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_f4_descent_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_f4_descent_probe.py \
  --fields 199^2,263^2,311^2 \
  | tee -a research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_f4_descent_probe_20260622.txt
```

## Result

All active `B` groups remain mixed for f4:

```text
field   B_f4 mixed / groups
71^2    8 / 8
167^2   6 / 6
199^2   16 / 16
263^2   12 / 12
311^2   16 / 16
```

The finer `(B,N)` quotient is also mostly mixed:

```text
field   BN_f4 mixed / groups
71^2    33 / 36
167^2   21 / 27
199^2   66 / 72
263^2   50 / 54
311^2   63 / 72
```

The `N`-only quotient is similarly mixed:

```text
field   N_f4 mixed / groups
71^2    24 / 26
167^2   20 / 25
199^2   47 / 51
263^2   42 / 45
311^2   54 / 60
```

Most individual beta_U gamma-positive points already have mixed f4 among their
materialized x7 roots:

```text
field   mixed beta_U points / gamma+ beta_U points
71^2    114 / 128
167^2   80 / 96
199^2   234 / 256
263^2   158 / 192
311^2   218 / 256
```

Regression checks:

```text
bad_curve_a = 0
gamma_norm_mismatch = 0
nonbase_norm = 0
x6_roots_2 for every gamma-positive beta_U row
x7_roots_2 for every materialized x6
```

## Interpretation

Positive:

```text
The beta_U norm map is still exact for f3/materialization.
The norm-fiber profile remains a valid branch/ramification target.
The probe gives a clean regression for any future beta_U CAS model.
```

Negative:

```text
f4 does not descend to B.
f4 does not descend to N = Norm(Unext+2).
f4 does not descend to the joint quotient (B,N).
The beta_U norm map is not a two-gate source.
```

## CAS Consequence

The beta_U subtest is now bounded:

```text
extract beta_U as the f3/materialization class;
explain the norm-map branch profile;
then compare f4/f3 as a separate Kummer class after normalization.
```

Promote only if normalization finds a non-visible quotient/Prym relation
between the beta_U class and the f4 class.  Do not promote the norm map itself
as a multi-gate sampler.

## Continue / Kill

```text
continue = beta_U branch/ramification extraction as one-gate structure
continue = compare f4/f3 only after normalized beta_U quotient/Prym data
continue = carry (B,N) f4 mixed counts as a regression

kill = beta_U norm map as a two-gate source
kill = f4 as a function of B, N, or (B,N)
kill = GPU production from beta_U gamma=+1 or low norm-support rows
```

## Linked Artifacts

- [P27 B-Line No-R Beta_U Norm-Fiber Profile](p27_b_line_noR_betaU_norm_fiber_profile_20260622.md)
- [P27 B-Line No-R Beta_U B-Character Replay](p27_b_line_noR_betaU_b_character_replay_20260622.md)
- [P27 B-Line No-R Beta_U Next-Gate Probe](p27_b_line_noR_betaU_next_gate_20260622.md)
- [P27 No-R Quotient/Prym Test Packet](p27_noR_quotient_prym_test_packet_20260622.md)

```text
p27_b_line_noR_betaU_norm_f4_descent_rows=1/1
```
