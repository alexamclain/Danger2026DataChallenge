# P27 Label-2 Residual E[3] Coset Screen

Date: 2026-06-21

## Claim

The residual elliptic `[3]` coset source does not currently give a stable
sqrt-beating or production-worthy lift for p27.

This was worth testing because `3 | #E(F_p)` for the residual curve
`E: W^2=X^3-X` at p27, so fixed `[3]` cosets are a real low-degree quotient
of the cyclic-quartic source curve.  A true coset lift would have been a
concrete structure to hand to the GPU agent.

The result is not strong enough: one 2M seed showed a tail lift for coset `0`,
but an independent 2M seed did not confirm it.  Combined over the two 2M pairs,
coset `0` is only about `1.02x` at depth 16 and about `1.12x` at depths 18-20,
with deeper tails unstable.

## Commands

Full 500k screen:

```bash
./src/pomerance 1000000000000000000000000103 \
  143 500000 x16halvestatsnonsplitecoverlabel2 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed143_500k_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  143 500000 x16halvestatsnonsplitecoverlabel2coset3 0 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed143_500k_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  143 500000 x16halvestatsnonsplitecoverlabel2coset3 1 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_coset1_seed143_500k_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  143 500000 x16halvestatsnonsplitecoverlabel2coset3 2 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_coset2_seed143_500k_20260621.txt 2>&1
```

Focused 2M replications:

```bash
./src/pomerance 1000000000000000000000000103 \
  144 2000000 x16halvestatsnonsplitecoverlabel2 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed144_2M_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  144 2000000 x16halvestatsnonsplitecoverlabel2coset3 0 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed144_2M_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  145 2000000 x16halvestatsnonsplitecoverlabel2 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed145_2M_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  145 2000000 x16halvestatsnonsplitecoverlabel2coset3 0 \
  > research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed145_2M_20260621.txt 2>&1
```

## 500k Screen

Rates were essentially identical:

```text
baseline rate_Mps = 0.106013
coset0   rate_Mps = 0.105965
coset1   rate_Mps = 0.105839
coset2   rate_Mps = 0.105789
```

The first 500k screen gave a possible tail lift for coset `0`, but counts were
small:

```text
depth  baseline  coset0  coset0/base
16     260       274     1.054
18     46        78      1.696
20     10        18      1.800
```

Cosets `1` and `2` were mixed and did not show a stable early-depth lift.

## 2M Replications

Seed 144 kept the coset0 tail alive:

```text
depth  baseline  coset0  coset0/base
16     978       982     1.004
18     202       270     1.337
20     60        88      1.467
22     18        28      1.556
24     6         6       1.000
```

Seed 145 did not replicate:

```text
depth  baseline  coset0  coset0/base
16     916       946     1.033
18     250       234     0.936
20     76        64      0.842
22     30        18      0.600
24     8         2       0.250
```

Combined over both 2M pairs:

```text
depth  baseline  coset0  coset0/base
12     31080     31062   0.999
14     7782      7694    0.989
16     1894      1928    1.018
18     452       504     1.115
20     136       152     1.118
22     48        46      0.958
24     14        8       0.571
```

## Interpretation

Positive:

```text
The residual [3] coset is a valid low-degree quotient/source test.
There is no throughput penalty in the current CPU implementation.
```

Negative:

```text
The apparent coset0 tail lift did not replicate.
The combined lift is small and unstable.
This is not a sqrt-beating source law.
```

## Continue / Kill

```text
continue = alpha/cyclic-quartic decomposition over E
continue = GPU compactD=-1 with d3/d4 telemetry

kill = residual E[3] coset source as an active moonshot lane
kill = promoting coset0 from current CPU data
```

If a GPU implementation already exposes residual `[3]` cosets almost for free,
coset0 can be logged as a low-priority telemetry column.  It should not
displace compactD/d3/d4 telemetry.

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed143_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed143_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset1_seed143_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset2_seed143_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed144_2M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed144_2M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_baseline_seed145_2M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed145_2M_20260621.txt`
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)

```text
p27_label2_residual_e3_coset_screen_rows=1/1
```
