# P27 X-Square / 2-Descent Gate

Date: 2026-06-21

## Claim

On nonsplit Montgomery rows, the selected halving gate can be stated even more
simply:

```text
P_j is divisible by 2  <=>  x(P_j) is a square
```

for the nondegenerate points in this search path.

Equivalently, the tower bits are:

```text
chi(d_j) = chi(x_j)
d_j = x_j^2 + A*x_j + 1
```

This identifies the p27 moonshot as an iterated 2-descent / Kummer problem:
find a way to force many successive selected x-coordinates to be squares.

## Reason

For

```text
E_A: y^2 = x^3 + A*x^2 + x = x*(x^2 + A*x + 1) = x*d
```

an `F_p` point with nonzero `x` and nonzero `d` satisfies:

```text
chi(x*d) = +1
```

therefore:

```text
chi(d) = chi(x).
```

The earlier nonsplit identity then says that once `d` is square, exactly one
`w` branch is available.  So in this nonsplit path, the halving gate is exactly
the squareclass of the current x-coordinate.

The branch-twin identity adds that the two x-coordinates obtained from the
successful `w` branch multiply to `1`, hence have the same squareclass.  So
choosing the other half-branch cannot alter the next `chi(d)` bit.

Equivalently, for the successful halving equation:

```text
x_next + 1/x_next = u
```

the next x-square bit is:

```text
chi(x_next) = chi(u + 2) = chi(u - 2).
```

This was checked directly on the p27 compactD stream in
[P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md).

## Factor Telemetry

The follow-up telemetry used:

```text
x_{j+1} + 1/x_{j+1} = u_j
d_{j+1} = x_{j+1}(u_j + A)
```

and recorded the two factors:

```text
chi(x_{j+1})
chi(u_j + A)
```

Run:

```bash
./src/pomerance 1000000000000000000000000103 \
  132 100000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_nextd_factor_seed132_100k_20260621.txt
```

Observed for every reported selected pass:

```text
chi(u_j + A) = +1
chi(d_{j+1}) = chi(x_{j+1})
```

Example, `domain_plus_Tline_minus`:

```text
gate 1 output_depth=5:
  x_next=-1, u_plus_A=+1: 12676
  x_next=+1, u_plus_A=+1: 12514

gate 2 output_depth=6:
  x_next=-1, u_plus_A=+1: 6188
  x_next=+1, u_plus_A=+1: 6326
```

The `x_next` squareclass remains balanced.  The factor split does not reveal a
selector, but it gives the right mathematical language.

## Interpretation

Positive:

```text
The d_j tower is the classical 2-descent x-square character in this nonsplit
Montgomery model.
The expert ask is now very crisp: iterated divisibility by 2 with a prescribed
X1(16) starting point.
```

Negative:

```text
The measured x_j squareclasses still look random.
This does not by itself beat sqrt scaling.
It kills the idea that a separate u_j+A or w_j predictor is the missing piece.
```

## Concrete Next Tests

1. GPU prefix filters:

```text
require x_4 square
require x_4,x_5 square
require x_4,x_5,x_6 square
```

This is equivalent to the `d_1,d_2,d_3` prefix tests but cheaper to describe
and easier to cross-check.

2. Math/literature/expert ask:

```text
For a nonsplit Montgomery curve with one rational 2-torsion point, the map
P -> x(P) mod squares is the 2-descent character.  Is there a useful
description of the iterated condition
  x(P), x(Q_1), ..., x(Q_m) all squares
where 2Q_1=P and the selected branch is fixed by the X1(16) sampler?
```

3. Tower-source ask:

```text
Can the X1(16) source parameter be lifted to an iterated 2-cover source that
produces x_4,...,x_m squares with less than 2^m random loss?
```

This is the current best formulation of a possible sqrt-beating route.

4. Branch-choice falsifier:

```text
After compactD=-1 on p27, d3 and d4 are invariant across the paired T roots
and the available half-branches in the 5,000-pair recurrence probe.
Do not look for sqrt-beating by choosing among those branches; look for a
source or recurrence for the x-square bits themselves.
```

See [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md).

5. U+2 prefix formula:

```text
After identifying the successful w branch, test chi(u+2) before materializing
x_next.  This exactly predicts the next x-square gate in the p27 compactD
d3/d4 probe.
```

This is useful only if it wins per GPU-second; independent `u+2` gates remain
constant-factor filters.

Follow-up norm/coboundary screen:
[P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md).
The local branch norms are exact, but the selected branch's `u+2` character is
not in the small `A,x` norm/branch span.  The best 30k-row scores were
`0.5018` for d3 and `0.5025` for d4.  That moved the next check to selected
branch orientation/cocycle products.

Follow-up selected-orientation screen:
[P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md).
Allowing selected `s`-branch orientation characters from the successful prefix
still gives no exact GF(2) product for the next `u+2` bit.  The surviving
source formulation is reverse doubling:

```text
x = (x_next^2 - 1)^2 / (4*x_next*(x_next^2 + A*x_next + 1)),
x_next = z^2.
```

## P26 GPU Seed-Law Check

A separate p26 GPU stratum probe landed negative:

```text
identity depth-26: 216 / 1B
splitmix depth-26: 248 / 1B
mixed depth-26:    260 / 1B
```

The p26 hit bucket `16` was not elevated in the hit chunk, and no compact
bucket cleared the held-out promotion bar.  This argues against spending p27
effort on seed-order laws unless a new mathematical invariant is proposed.

## Continue / Kill

```text
continue = iterated 2-descent / x-square tower
continue = GPU prefix x-square tests
continue = GPU u+2 precheck before sqrt(w) for d3/d4 prefix filters
continue = Sage/Magma quotient/genus test for the reverse-doubling source
continue = expert ask about lifting X1(16) into an iterated 2-cover source

kill = branch-choice selector for the next x-square bit
kill = treating independent u+2 checks as sqrt-beating
kill = local A,x norm-character selector for selected u+2
kill = small selected-orientation product span for selected u+2
kill = expecting reverse-doubling density alone to beat random half-loss
kill = independent w_j predictor
kill = u_j+A as a selector, since it is square on observed selected points
kill = seed-order/bucket law without a mathematical invariant
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_trace_norm_nextd_factor_seed132_100k_20260621.txt`
- Related: [P27 Nonsplit W-Obstruction Identity](p27_nonsplit_w_obstruction_identity_20260621.md)
- Related: [P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md)
- Related: [P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md)
- Related: [P27 Reverse-Doubling Source Screen](p27_reverse_doubling_source_screen_20260621.md)
- Related: [P27 Selected Halving Tower Profile](p27_halving_tower_profile_20260621.md)
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)
- Related: [P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md)
- External p26 GPU note: `/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/research/p26/gpu-stratum-probe_20260621.md`

```text
p27_xsquare_2descent_gate_rows=1/1
```
