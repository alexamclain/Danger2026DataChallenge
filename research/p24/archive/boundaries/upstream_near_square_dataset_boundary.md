# Upstream Near-Square Dataset Boundary

This note records what the uploaded Sutherland one-witness datasets say about
the p24-style near-square family.

## Command

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/upstream_near_square_signal_audit.py
```

The source is the local copy:

```text
p24/upstream_DANGER3/pp24.txt.gz
```

which contains one Pomerance triple for each prime below `2^24`.

## Main Signal

The exact p24 shape is

```text
p = n^2 + 7,      n == 0 mod 8.
```

In the small uploaded analogue, there are `142` such primes.  The retained
witnesses all lie in the same cheap verifier branch:

```text
p24_analog_c7_n0mod8_rows=142
p24_analog_c7_n0mod8_terminal_counts={'zero_root': 142}
p24_analog_c7_n0mod8_feature_counts
  A+2:   {1: 142}
  A-2:   {-1: 142}
  A2-4:  {-1: 142}
```

This is useful calibration: the near-square p24 analogue prefers the nonsplit
zero-terminal branch, exactly the branch already used by the p23 `X1(16)`
nonsplit search and by the conductor-2/nonsplit gate.

## What Does Not Appear

The same slice does not show a visible growing selector for `A` or `x`.
The normalized size statistics are still broad and close to the whole-file
one-witness distribution:

```text
p24_analog_c7_n0mod8_min_A_mean = 0.234522
p24_analog_c7_n0mod8_min_x_mean = 0.248044
```

The low-degree Legendre labels beyond the known branch are split rather than
constant:

```text
curve_rhs: {-1: 70, 1: 72}
x:         {-1: 68, 1: 74}
x+1:       {-1: 69, 1: 73}
x-1:       {-1: 64, 1: 78}
```

Thus the uploaded data reinforces a constant-factor branch choice, not an
asymptotic selector.  It does not reveal an algebraic rule that maps
`p = n^2 + 7` directly to the target Montgomery parameter.

## Consequence

The data can justify carrying the nonsplit branch as a verifier-side
constraint, but the remaining p24 bottleneck is still the same horizontal
class-field selector:

```text
construct the target trace / CM j root / embedded packet without enumerating
the class set.
```

The smaller-prime witnesses do not contradict the current theorem boundary:
they expose the same branch symmetries and near-uniform residual inverse-ray
entropy already seen in the full small-triple audit.

## Holdout Character-Gate Check

I also reran the greedy low-degree Legendre gate scan on exact small fields in
the family `p=n^2+7`, `n==0 mod 8`:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/character_gate_stack_scan.py \
  --min-p 10000 --max-p 120000 --max-rows 12 \
  --coeff-bound 2 --max-gates 6 --min-train-coverage 0.02 \
  --n-modulus 8 --n-residue 0
```

The first two selected gates are the expected first-branch conditions:

```text
A + 2 square,     A - 2 nonsquare.
```

They generalize to holdout and give only a constant lift:

```text
base_holdout precision=0.018765
after gate 1 precision=0.028648, lift=1.527, coverage=0.500
after gate 2 precision=0.039529, lift=2.106, coverage=0.250
```

Subsequent selected atoms do not improve the holdout counts; they are
redundant quadratic rewritings of the same branch.  This is useful
statistical evidence against a productively liftable tower of cheap Legendre
gates in the near-square family.
