# P27 Trace/Norm Post-Dplus Screen

Date: 2026-06-21

## Claim

The production C-style trace/norm `D_plus` predicate is confirmed again as an
exact two-gate prefix, but the named trace/norm signs tested here do not
predict the next selected halving gates.

This closes the immediate interpretation of the GPU `4x` result:

```text
Dplus = exact first-two-gate prefix
post-Dplus d3/d4 = random-looking half-loss
low-weight named trace/norm products = no exact post-Dplus selector
```

So `D_plus` remains a valuable algebraic description of the first two selected
gates, but it is not yet a sqrt-beating recurrence or a production source.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_post_dplus_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_post_dplus_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p27/archive/gates/p27_trace_norm_post_dplus_probe.py \
  --seeds 121,122 \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-rows 20000 \
  --top 12
```

The probe mirrors the production `x16_y_trace_norm_d_class128` predicate from
`src/pomerance.c`, reconstructs C-ordered X1(16) candidates, applies the
selected first-branch halving path, and then scores low-weight products of
named trace/norm characters against `d3` and `d4`.

## Counts

```text
raw_y_draws = 131,072
nonsplit_y = 65,766
D_zero = 32,965
D_+1 = 16,485
D_-1 = 16,316
Dplus_y = 16,485
Dplus_no_valid_candidate = 8,286
Dplus_candidates = 16,398
Dplus_prefix_failure = 0
d1_+1 = 16,398
d2_+1 = 16,398
d3_+1 = 8,298
d3_-1 = 8,100
d4_+1 = 4,062
d4_-1 = 4,236
```

Rates:

```text
d3_plus_after_Dplus = 8298 / 16398 = 0.506037322
d4_plus_after_Dplus_and_d3 = 4062 / 8298 = 0.489515546
```

There were zero `Dplus` prefix failures: every usable `Dplus` candidate passed
the first two selected halving gates.

## Character Screen

Pre-root feature atoms:

```text
H, VQ, X_pref, chi_y, chi_t, chi_y_minus_2,
chi_B, chi_C, chi_R, chi_F, chi_root_disc
```

Root-level extension:

```text
root_index, chi_root, chi_root_minus_y, chi_A,
chi_A_minus_2, chi_A_plus_2, chi_xP, chi_xP_minus_1,
chi_xP_plus_1, chi_a, chi_b, T_line
```

The screen tested all products of weight `<= 4` in both feature sets.

Results:

```text
pre-root d3 exact_combo_weight_le_4 = none
root-level d3 exact_combo_weight_le_4 = none
pre-root d4 exact_combo_weight_le_4 = none
root-level d4 exact_combo_weight_le_4 = none
```

The best apparent train lifts did not replicate:

```text
pre-root d3 best train = 0.513965118, heldout = 0.496645932
root-level d3 best train = 0.515062813, heldout = 0.490669594
pre-root d4 best train = 0.533140516, heldout = 0.498915401
root-level d4 best train = 0.533140516, heldout = 0.498915401
```

This is the expected signature of noise rather than a reusable trace/norm
selector.

## Orientation Follow-up

Follow-up:
[P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md).

The exact cover orientation signs were then tested directly:

```text
eps_h = chi(t)
eps_v = chi((t+1)C)
```

On seed groups `121,122` and `123,124`, the `d3` and `d4` rates by
`eps_h/eps_v`, `H/VQ`, `eps_h/eps_v/T_line`, and
`hcore_chi/vcore_chi` stayed near half.  Apparent high `d4` states did not
replicate as the same named bucket.  This kills the simple orientation-bucket
version of a post-Dplus recurrence.

## Interpretation

Positive:

```text
Dplus is an exact, scalable algebraic two-gate prefix.
The production C predicate and the Python reconstruction agree on the prefix.
```

Negative:

```text
Dplus does not visibly couple to the next selected gate.
The tested H/VQ/X/T_line/root squareclasses do not explain d3 or d4.
The GPU 4x result should not be treated as a late-depth law.
```

## Next Test

The next sqrt-beating test is not another low-weight sign scan.  The surviving
question is to extract the actual quotient/function-field double covers for
the descended `d3` and `d4` bits on the residual elliptic quotient or its
2-isogenous quotient:

```text
E:  W^2 = X^3 - X
E': V^2 = U^3 + 4U,  U = X - 1/X
```

Concrete ask:

```text
Use Magma/Sage to compute the divisor/Kummer classes of the d3 and d4 double
covers on E or E', then compare them for a sourceable relation, quotient, Prym
factor, or recurrence.
```

GPU-worthy follow-up:

```text
Only implement a new GPU filter if the function-field extraction produces a
named class or sampler.  Dplus by itself is a two-gate prefix, not a raw
source-space shrink.
```

## Continue / Kill

```text
continue = Dplus as the named trace/norm model of the first two gates
continue = E/E' function-field extraction for d3 and d4
continue = online Magma small-field validation for named formulas

kill = low-weight post-Dplus products from H,VQ,X,T_line/root atoms
kill = eps_h/eps_v or H/VQ/T_line buckets as post-Dplus GPU filters
kill = interpreting the Dplus 4x GPU lift as a recurrence
kill = spending GPU production time on Dplus unless its implementation beats
       other ways to impose the same two gates
```

```text
p27_trace_norm_post_dplus_screen_rows=1/1
```
