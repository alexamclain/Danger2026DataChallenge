# Smooth Torsor Search Boundary

This note separates what the smooth third-trace class group genuinely buys
from what it does not buy.

## Target Data

For the three strict p24 traces, the relevant maximal-order class sizes are:

```text
first:   h = 278733727154 = 0.278734 * sqrt(p)
middle:  h = 833035208344 = 0.833035 * sqrt(p)
third:   h = 205880396014 = 0.205880 * sqrt(p)
```

For the third trace,

```text
h = 2 * 157 * 211 * 3107441,
best formal split = 66254 * 3107441.
```

If the embedded quotient equations were known, this would be excellent:

```text
quotient degree = 66254,
recovery degree = 3107441,
quotient + recovery = 3173695 << sqrt(p).
```

The audit script is:

```text
p24/smooth_torsor_search_tradeoff_audit.py
```

## What Smoothness Buys

Once a target CM root or an embedded quotient period is known, smoothness is
real leverage:

```text
class navigation after a seed: cheap;
Pohlig-Hellman-style indexing after known vertices: cheap;
tower factors: 2, 157, 211, 3107441;
final recovery degree from the best quotient: 3107441.
```

This is why the third trace remains the best formal CM route.

## What Smoothness Does Not Buy

Smoothness does not increase the density of target traces in the whole
Montgomery or `j` line.  The total strict CM root count is still
`Theta(sqrt(p))`, so random discovery is still square-root scale.

The audit prints:

```text
sum_h_one_order_per_trace = 1317649331512 = 1.317649 * sqrt(p)
random_j_expected_trials_over_sqrt_using_sum_h = 0.758927
two_order_proxy_expected_trials_over_sqrt = 0.379464
generous_montgomery_A_degree_bound_expected_trials_over_sqrt = 0.063244
```

These are good constants under generous modeling assumptions, but they are
still exponent `1/2`.

The exact small-field post-trace calibration agrees.  In small
`p=n^2+7`, `n == 0 mod 8` rows, once a target-trace Montgomery `A` is known,
finding an accepted `x0` is constant expected work:

```text
projected_group_point_expected_trials_per_known_good_side <= 2.
```

But constructing the target-trace `A` remains square-root density.  A sample
run gives:

```text
target_A_over_sum_sqrt = 8.500883
strict_A_over_sum_sqrt = 6.005442
avg_x_per_strict_A = 97.802029
```

The script is:

```text
p24/post_trace_construction_audit.py
```

## BSGS Boundary

Baby-step/giant-step or smooth discrete-log methods help only on an already
defined torsor.

```text
given one target CM vertex:
  walk/split/index the class group cheaply;

given two target CM vertices:
  solve class-position problems cheaply because h is smooth;

given an embedded quotient root:
  recover j through degree 3107441;

given only p and the trace:
  no starting vertex, no embedded quotient equations, no group action domain.
```

A membership oracle such as SEA point counting can recognize a target trace,
but sampling candidates for it remains `Theta(sqrt(p))`.  Conversely, the
class action by split primes is defined only inside the hidden CM isogeny
class; it cannot be used to navigate from a random curve into that class
without already solving the trace/root-selection problem.

## Decomposed-CM Boundary

Sutherland-style decomposed CM is exactly the right formal shape once embedded
equations are available.  For p24 the degree split is excellent:

```text
best_degrees = 66254 * 3107441,
best_sum_degrees = 3173695.
```

But known ways to construct those embedded equations either:

```text
1. start from a seed target CM curve and enumerate class orbits; or
2. use CRT/complex/p-adic class-object computation at large-discriminant
   scale over auxiliary fields.
```

The abstract class-field quotient exists, but it is unpaired with `j`; see:

```text
p24/prime_torsor_obstruction_theorem.md
```

## Boundary

The smooth class group turns the third trace into the best formal target, but
it does not by itself beat square-root scaling.

To become a certificate-scale algorithm, the smooth route still needs the same
missing object:

```text
an embedded quotient period / relative class-character trace formula for the
odd 157 and 211 layers, paired back to j, without class enumeration.
```

Without that object, the choices are:

```text
random trace discovery:       Theta(sqrt(p));
known decomposed-CM methods:  class-object / orbit cost;
post-trace x0 construction:   cheap, but only after target A is known.
```
