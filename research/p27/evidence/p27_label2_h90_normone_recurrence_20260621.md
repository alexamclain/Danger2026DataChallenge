# P27 Label-2 H90 Norm-One Recurrence Screen

Date: 2026-06-21

## Claim

The natural Hilbert-90 norm-one element from the order-4 lift does not give a
cheap visible recurrence or selector for `d3` or `d4`.

For

```text
u = (m0 + mt*T)/(2*T*Salpha),
```

the probe screened compact H90-derived squareclasses on independent p27
train/heldout samples.  The best train lifts collapse on heldout, and the
features that are genuinely invariant under `T -> -T` stay at raw-bias level.

This kills the cheap "H90 norm-one character product" route.  It does not kill
the larger alpha/Prym lane, because a non-visible quotient or Jacobian factor
could still exist.

## Probe

Gate:

```text
research/p27/archive/gates/p27_label2_h90_normone_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_label2_h90_normone_recurrence_probe_20260621.txt
```

Command:

```bash
PYTHONPATH=research/p27/archive/gates PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_label2_h90_normone_recurrence_probe.py \
  --target 8000 \
  --heldout-target 8000 \
  --max-draws 1200000 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_label2_h90_normone_recurrence_probe_20260621.txt
```

## Feature Set

The screened H90 features were:

```text
u
u+1
u-1
u^2+1
u^2-1
u+u^-1
u-u^-1
mplus = m0 + mt*T
denom = 2*T*Salpha
mt*T
m0
Salpha
prefactor = W*(X^2+1)/X
L
```

Only seven squareclasses were invariant under the actual `T -> -T` sign
change on both train and heldout:

```text
u^2+1
u-u^-1
mplus
m0
Salpha
prefactor
L
```

The non-invariant features were still screened separately as
implementation/canonical-`T` diagnostics, but they are weaker mathematically.

## Train / Heldout Result

Train sample:

```text
usable_rows = 8000
d3_plus/minus = 4036/3964
d4_rows = 4036
d4_plus/minus = 2048/1988
```

Heldout sample:

```text
usable_rows = 8000
d3_plus/minus = 4096/3904
d4_rows = 4096
d4_plus/minus = 2016/2080
```

Best `d3` all-H90 train score:

```text
train = 4100/8000 = 0.512500
heldout = 3928/8000 = 0.491000
```

Best `d3` `T`-sign-invariant score:

```text
train = 4100/8000 = 0.512500
heldout = 3928/8000 = 0.491000
```

Best `d4` all-H90 train score:

```text
train = 2126/4036 = 0.526759
heldout = 2023/4096 = 0.493896
```

Best `d4` `T`-sign-invariant score:

```text
train = 2048/4036 = 0.507433
heldout = 2016/4096 = 0.492188
```

The heldout rates track the raw heldout biases, not a stable structural lift.

## Interpretation

Positive:

```text
The H90 lift gives a small, explicit, testable feature family.
The T-sign-invariant subset is now known and should be reused if needed.
```

Negative:

```text
No screened H90 norm-one product predicts d3 or d4.
Canonical-T train lifts are overfit.
T-sign-invariant H90 products do not beat the raw heldout bias.
```

## Continue / Kill

```text
continue = alpha-equivariant Prym/Jacobian decomposition of the genus-17 component
continue = explicit non-visible cyclic-quartic character if CAS produces one
continue = GPU telemetry only for a new named stratum or recurrence

kill = H90 norm-one squareclass products listed here as d3/d4 selectors
kill = canonical-T feature products without heldout lift
kill = treating compactD/order-4 as sufficient for later-gate recurrence
```

## Linked Artifacts

- Parent: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Component check: [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md)
- Probe: `research/p27/archive/gates/p27_label2_h90_normone_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_h90_normone_recurrence_probe_20260621.txt`

```text
p27_label2_h90_normone_recurrence_rows=1/1
```
