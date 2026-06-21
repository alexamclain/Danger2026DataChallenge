# P27 Nonsplit W-Obstruction Identity

Date: 2026-06-21

## Claim

The absence of `w_j` obstructions in the selected p27 halving tower is
explained by a general nonsplit Montgomery identity.

For a Montgomery curve

```text
E_A: y^2 = x^3 + A*x^2 + x
```

write

```text
d = x^2 + A*x + 1
s^2 = d
u_+ = 2(x+s)
u_- = 2(x-s)
w_+ = u_+^2 - 4
w_- = u_-^2 - 4
```

Then

```text
w_+ * w_- = 16*x^2*(A^2 - 4).
```

Therefore on a nonsplit curve, where `chi(A^2-4)=-1`, the two `w` candidates
have opposite squareclass.  Once `d` is square, exactly one `w` branch is
available, except for degenerate zero rows.

So the p27 selected halving tower is not mysteriously avoiding `w` failures:
for nonsplit rows, the halving obstruction is exactly the next `d_j`
squareclass.

There is a second branch consequence.  On the successful `w` branch, the two
half x-coordinates are:

```text
x'_+ = (u + sqrt(w))/2
x'_- = (u - sqrt(w))/2
```

and therefore:

```text
x'_+ * x'_- = (u^2 - w)/4 = 1.
```

Thus the two available x-branches have the same squareclass.  Since
`chi(d_next)=chi(x_next)`, branch choice cannot change the next halving gate.
This was confirmed in the label-2 compactD stratum through d3 and d4:
[P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md).

## Derivation

Starting from `s^2=d=x^2+A*x+1`:

```text
w_+ * w_-
  = 16((x+s)^2 - 1)((x-s)^2 - 1)
  = 16((x^2+s^2-1)^2 - (2xs)^2)
  = 16((2x^2 + A*x)^2 - 4x^2(x^2+A*x+1))
  = 16*x^2(A^2 - 4).
```

Because `16*x^2` is a square away from degenerate `x=0`, the squareclass is
`chi(A^2-4)`.

## Consequence

The empirical tower profile:

```text
d_square_w_none = 0
pass_two_w = 0
```

is now explained, not merely observed.  It should hold throughout the nonsplit
selected path, not just through the first eight measured gates.

The branch-twin product identity also explains why lookahead branch choice did
not help in the compactD recurrence probe: both x-branches see the same next
`x` squareclass.

The practical and theoretical target becomes:

```text
find structure in chi(d_1), chi(d_2), ..., chi(d_j)
where d_j = x_j^2 + A*x_j + 1.
```

## GPU Implication

GPU prefix filters do not need to model a separate `w_j` obstruction for
nonsplit rows.  It is enough to report:

```text
d_j square?
which w branch was selected?
branch mismatch/degenerate count
```

The branch-choice telemetry is still useful for debugging, but not as a
selector for the next gate.  The expected survival probability of each
additional prefix gate remains `~1/2` unless a new recurrence couples the
descended x-square bits.

## Moonshot Implication

The sqrt-beating ask is narrower:

```text
Find a source/tower law that produces many consecutive square d_j values on
the nonsplit Montgomery halving tower.
```

Equivalently, describe the solvable locus of the iterated quadratic system:

```text
d_j = x_j^2 + A*x_j + 1 = square
x_{j+1} + 1/x_{j+1} = 2(x_j +/- sqrt(d_j))
```

The nonsplit identity removes the extra `w` condition from the obstruction
count.

## Continue / Kill

```text
continue = derive or search for relations among chi(d_j)
continue = ask experts about iterated Kummer characters for d_j
continue = GPU prefix d_j tests without separate w_j filtering

kill = treating w_j as an independent obstruction on nonsplit rows
kill = interpreting zero w failures as p27-specific luck
```

## Linked Artifacts

- Related: [P27 Selected Halving Tower Profile](p27_halving_tower_profile_20260621.md)
- Related: [P27 Second-D Gate Frontier](p27_second_d_gate_frontier_20260621.md)
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)

```text
p27_nonsplit_w_obstruction_identity_rows=1/1
```
