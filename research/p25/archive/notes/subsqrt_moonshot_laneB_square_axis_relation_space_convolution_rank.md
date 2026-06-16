# Subsqrt Moonshot Lane B Square-Axis Relation-Space Convolution Rank

Date: 2026-06-12

## Result

After imposing the raw relation `D^3 = Y`, the square-axis producer target
lives on the `507`-dimensional relation space.  The residual word acts there
as a cyclic convolution kernel.

That kernel is not low rank.  Over a split field for `C_507`, convolution by
the residual has rank `505 / 507`; its only null characters are the two
`S = 1 + D + D^2` factor characters.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_relation_space_convolution_rank_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_relation_space_convolution_rank_gate.py
```

Observed:

```text
relation_space_dimension = 507

S:
  point_count = 3
  rank = 505 / 507
  nullity = 2
  zeros = [169, 338]

seed:
  point_count = 6
  rank = 507 / 507
  nullity = 0

rectangle_seed:
  point_count = 9
  rank = 505 / 507
  nullity = 2
  zeros = [169, 338]

borrow_seed:
  point_count = 3
  rank = 507 / 507
  nullity = 0

residual:
  point_count = 18
  rank = 505 / 507
  nullity = 2
  zeros = [169, 338]

rectangle:
  point_count = 27
  rank = 505 / 507
  nullity = 2
  zeros = [169, 338]

borrow:
  point_count = 9
  rank = 505 / 507
  nullity = 2
  zeros = [169, 338]

square_axis_relation_space_convolution_rank_rows = 1 / 1
```

## Consequence

The residual is sparse as a set, but not low rank as a `D`-equivariant
operator on the relation space.  After quotienting by the two `S`-null
characters, the residual, rectangle, and borrow convolution kernels are all
invertible.

This rules out another class of easy producer explanations:

```text
reject D-equivariant low-rank filters as the source of the residual;
reject hidden quotient-compression stories beyond the two S-factor characters;
keep only producers that build the no-borrow word itself, not a small image filter.
```

The preceding relation-space checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_relation_kernel_equivalence.md
```
