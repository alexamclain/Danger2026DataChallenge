# Axis Probability and Upstream Data Sidecar

This note records the side-agent synthesis after the `L1` axis-injectivity
target emerged.

## Probability Takeaway

Probability is useful only if it becomes a pointwise anti-concentration
statement for the selected CM packet.  Average equidistribution over origins,
primes, or random weights is too weak for p24.

The productive theorem shape is:

```text
T_a : W_axis -> F_p[X]/(f_a)
```

is injective for each selected packet orbit.  Equivalently,

```text
W_axis ∩ Ann(packet_a) = {0}.
```

This is a statistics-to-structure dichotomy:

```text
if selected-origin L1 vanished, then either
  a visible axis-rank defect appears, or
  the actual CM packet violates the random-subspace model in a pointwise way.
```

The current small CM data supports the first formulation: eligible packet
rows have full axis rank, and all observed rank defects are dimension-forced.

## Failure Modes to Watch

The theorem would be falsified by an eligible packet with

```text
deg(f) >= dim(W_axis)
rank(T_f) < dim(W_axis).
```

A weaker but still worrying signal would be a selected-origin `L1` zero with
full axis rank, because that would show ordinary finite-field cancellation
inside the fixed all-ones weight rather than a rank defect.  No such zero has
appeared.

Standard character-sum and small-bias tools are not directly enough because
they usually prove averaged statements.  A p24 proof needs a fixed selected
origin and a fixed selected prime.

## Upstream DANGER3 Data Takeaway

The local upstream/Sutherland clone under

```text
p24/upstream_DANGER3
```

contains Montgomery verifier triples and prefixes, not CM packet fibers.  It
is therefore a negative-control dataset for cheap verifier-side selectors, not
a direct test of `L1` p-unitness.

Existing upstream-data audits found:

```text
one-witness rows are strongly nonsplit/zero-terminal,
but all-prefix data shows this is a constant-factor branch condition;

Legendre and branch labels do not form a growing selector;

projection-compression checks under A^2, Montgomery j, A^2-4, and terminal
ratios show only constant-degree compression.
```

So the upstream data supports carrying the verifier branch constraint as a
sanity condition, but it does not materially prove or disprove axis
injectivity.

## Follow-Up Experiments

Already run after this sidecar:

```text
composite-m all-origin eligible axis scan:
packet_rows=162
injective_rows=162
injective_failures=0
l1_zero_rows=0

all-origin eligible axis scan:
packet_rows=341
injective_rows=341
injective_failures=0
l1_zero_rows=0
```

Potential next negative-control experiment:

```text
stream pp16A after the known nonsplit/zero-terminal gate and test whether any
small squarefree A mod M axis support remains.
```

This would only rule out more Montgomery-side shortcuts.  The main theorem
target remains the CM packet axis-injectivity statement.
