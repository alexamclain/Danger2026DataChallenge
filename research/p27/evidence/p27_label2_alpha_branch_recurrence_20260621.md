# P27 Label-2 Alpha/Branch Recurrence Probe

Date: 2026-06-21

## Claim

The label-2 compactD/order-4 structure gives an exact second-gate stratum, but
the paired `T`-deck root and the two half-branches do not give a way to choose
the next gate.

On a 5,000-pair p27 sample:

```text
compactD=-1 matched d2 with zero failures
d3 was invariant across both T-deck roots and both second-half x-branches
d4, conditioned on d3, was invariant across all next branches in the same way
d3 and d4 rates were random-looking half-losses
```

So the next possible sqrt-beating route is not branch selection.  It must be a
source, formula, or recurrence for the descended sequence of x-square bits.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_label2_alpha_branch_recurrence_probe.py \
  --target 5000 \
  --max-draws 1000000 \
  | tee research/p27/archive/probe_outputs/p27_label2_alpha_branch_recurrence_probe_20260621.txt
```

The probe samples p27 residual-E label-2 rows:

```text
E: W^2 = X^3-X
y = 2X/(X-1)
T^2 = X(X^2+1)(X^2+2X-1)
compactD = -1
```

It applies the nonsplit X1(16) boundary, pairs the two `T` signs, enumerates
the two second-halving x-branches after `d2`, and then checks `d3` and `d4`.

## Result

Input sample:

```text
sampled_pairs = 5000
x_draws = 39299
candidate_invalid_not_nonsplit = 9808
compact_not_target = 9728
pair_incomplete = 4904
```

The compactD/d2 boundary is exact on the sampled nonsplit rows:

```text
total_roots = 10000
d2_fail_after_compactDneg = 0
```

The next gate is invariant across both half-branches and both paired `T`
roots, but is not biased positive:

```text
total_x6_branches = 20000
d3_plus_branches = 9864
d3_plus_branch_rate = 0.493200000
root0_d3_plus_rate = 0.493200000
root1_d3_plus_rate = 0.493200000

per_root_branch_hist:
  nbranches=2 n_d3_plus=0 count=5068
  nbranches=2 n_d3_plus=2 count=4932

paired_T_root_d3_plus_hist:
  root0_plus=0 root1_plus=0 count=2534
  root0_plus=2 root1_plus=2 count=2466
```

Conditioned on d3 passing, d4 has the same shape:

```text
total_d3plus_x6 = 9864
total_x7_branches = 19728
d4_plus_branches = 10208
d4_plus_branch_rate_after_d3 = 0.517437145

per_d3plus_x6_d4_branch_hist:
  nbranches=2 n_d4_plus=0 count=4760
  nbranches=2 n_d4_plus=2 count=5104

paired_T_orbit_d4_plus_hist:
  x7_branches=8 d4_plus=0 count=1190
  x7_branches=8 d4_plus=8 count=1276
```

The descended d3 bit is also not a visible GF(2) character in the screened
H90/order-4 factor basis:

```text
features =
  X, W, X-1, X+1, X2+1, X2+2X-1, X2-2X-1,
  S, S_conj, mt_linear, m0, mt_coeff, prefactor, L

rows = 5000
exact_combo = none
best rate = 2548/5000 = 0.509600000
```

## Identity Behind The Branch Result

For one successful halving step, write:

```text
s^2 = d = x^2 + A*x + 1
u = 2(x+s)
w = u^2 - 4
x'_+ = (u + sqrt(w))/2
x'_- = (u - sqrt(w))/2
```

Then:

```text
x'_+ * x'_- = (u^2 - w)/4 = 1.
```

Therefore the two x-branches from the same successful `w` branch have the same
squareclass.  Since

```text
chi(d_next) = chi(x_next)
```

on the nonsplit Montgomery path, the next halving gate cannot be changed by
choosing the other x-branch.  The probe confirms this at d3 and d4 in the
label-2 compactD stratum.

## Interpretation

Positive:

```text
compactD=-1 is again verified as the exact p27 d2 selector.
d3 and d4 descend cleanly through the available branch choices.
GPU telemetry can report one selected branch for d3/d4 rates; branch
enumeration is useful mainly as a consistency check.
```

Negative:

```text
The alpha/T-deck pair does not provide a hidden branch chooser.
The two x-branches after a successful halving step do not provide a chooser.
d3 and d4 still look like independent half-losses.
The natural visible residual-E factor basis does not explain d3.
```

## Concrete Next Tests

1. Formalize the branch-twin identity in the tower notes:

```text
x'_+ * x'_- = 1
therefore chi(x'_+) = chi(x'_-)
therefore branch choice cannot alter chi(d_next)
```

2. GPU compactD telemetry should still report d3/d4, but should not spend much
effort enumerating branch choices unless it is essentially free.

3. The next math lane should target a non-visible recurrence for the descended
bit sequence:

```text
compactD/d2 bit on residual E
d3 bit after compactD
d4 bit after compactD+d3
```

The local form of each descended bit is now:

```text
chi(u_j + 2)
```

where `x_{j+1}+1/x_{j+1}=u_j`; see
[P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md).

4. Promote only a source or theorem that couples several of those descended
bits at once.  A fixed-prefix filter remains constant-factor unless the bit
sequence becomes non-random.

## Continue / Kill

```text
continue = derive symbolic formula for the descended d3 bit
continue = GPU compactD+d3+d4 prefix rates with effective survivor/sec
continue = non-visible theta/Kummer/H90 recurrence for the x-square bit sequence

kill = branch-choice selector for d3/d4
kill = T-deck/alpha-pair selector for d3/d4
kill = visible residual-E character from the screened factor basis for d3
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_label2_alpha_branch_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_alpha_branch_recurrence_probe_20260621.txt`
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Related: [P27 Nonsplit W-Obstruction Identity](p27_nonsplit_w_obstruction_identity_20260621.md)
- Related: [P27 X-Square / 2-Descent Gate](p27_xsquare_2descent_gate_20260621.md)
- Related: [P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md)

```text
p27_label2_alpha_branch_recurrence_rows=1/1
```
