# Post-CM-Root Projection Boundary

Date: 2026-06-05

This note isolates the part of the DANGER3 certificate after a target-trace
Montgomery parameter `A` is known.

## Statement

For p24, the third strict trace has:

```text
p = 10^24 + 7
t = -1178414874616
p + 1 - t = 2^41 * 454747350887
verifier depth k = 40
```

So if the embedded CM/root-selection theorem supplies a nonsingular
Montgomery `A` on the correct strict branch, then the remaining `x0` is found
by x-only projection:

```text
take an x-coordinate seed,
apply the Montgomery ladder by the odd part,
double down to exact depth k,
verify Z_k = 0 and Z_{k-1} != 0.
```

This is logarithmic/constant-expected work after `A` is known.  It should not
be folded into the class-field construction as a marked `2^40` ray; doing so
would reintroduce the huge `X1(2^40)` orientation cover.

## Toy

I added:

```text
p24/post_cm_root_projection_toy.py
p24/post_j_root_to_triple_toy.py
p24/post_j_root_to_triple_boundary.md
```

It uses pure Python x-only Montgomery arithmetic:

```text
xMUL by the odd part,
exact-depth trimming by xDBL,
literal DANGER3 replay check.
```

On the small conductor-2 analogue:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/post_cm_root_projection_toy.py \
  --p 103 --trace 8 --trials 200 --scan-target-trace
```

reported:

```text
candidates=36
found=12
conclusion=post_cm_root_projection_constructs_x0_for_strict_target_trace_A
```

The successful rows are exactly the strict verifier branch in this toy.  For
example:

```text
A=12 trace=8 split=-1 found=1 side=curve seed_x=5 odd=3 x0=75 verify=1
A=44 trace=-8 split=-1 found=1 side=twist seed_x=4 odd=3 x0=100 verify=1
```

The split target-trace rows with no accepted `x0` are the small-field analogue
of the branch caveat already recorded in the conductor-2/nonsplit gate.

## Consequence

The p24 work should remain split:

```text
hard:
  construct a strict target-trace Montgomery A by the embedded CM quotient /
  recovery theorem;

easy:
  project to x0 afterward with the odd part of the known curve/twist order.
```

Thus the missing asymptotic speedup is entirely in the unmarked embedded
CM-root selector.  The verifier point is not an additional class-field or
sqrt-scale obstacle once `A` is supplied.
