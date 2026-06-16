# Hybrid Trace-Verifier Boundary

This note checks the hybrid route:

```text
use trace-residue / fixed-trace information to get close to a strict
Montgomery A, then use the DANGER x-only verifier equation for x0.
```

## What Would Be Enough

For p24, once a nonsingular Montgomery parameter `A` is known whose curve or
twist has one of the strict signed traces, the remaining `x0` step is cheap:
the relevant side has a large rational 2-primary subgroup, and sampling or
projecting to a point of exact x-only order `2^40` is constant expected work.

The small exact calibration

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/post_trace_construction_audit.py \
  --min-p 10000 --max-p 120000 --max-rows 8 --details
```

reported:

```text
target_trace_A=12048
strict_good_A=8424
accepted_x_total=821248
target_A_over_sum_sqrt=8.754736
strict_A_over_sum_sqrt=6.121340
avg_x_per_strict_A=97.489079
```

So the verifier point is not the hard part after `A` is known.

The x-only projection tail is now packaged explicitly in:

```text
p24/post_cm_root_projection_toy.py
p24/post_cm_root_projection_boundary.md
```

The toy confirms the caveat: projection constructs `x0` for the strict branch
of a target-trace `A`; target-trace `A` values on the wrong split branch may
still fail the literal verifier.

## Exact Trace-Residue Oracle

The strongest optimistic trace-residue model grants an oracle that imposes
exactly the target trace residues modulo a level `N`, and prices the
construction only by `Gamma0(N)` index.  This is stronger than ordinary
unoriented `X0(N)` data, because exact trace residues also know eigenvalue
information.

The rerun

```text
python3 p24/exact_trace_residue_oracle_tradeoff.py
```

again found pure `2^40` best among sampled levels:

```text
best_sampled_level:
  label=2^40
  level=1099511627776
  survivors=6
  gamma0_over_sqrt=1.649267
  oracle_proxy_over_sqrt=1.649267
```

Shallower levels have lower modular degree but leave proportionally more Hasse
trace lifts.  Odd or mixed levels reduce the residual trace count but increase
the modular index by the same square-root-scale amount.

## Wider Mixed Search Attempt

I also tried to widen

```text
p24/mixed_crt_trace_residue_optimizer.py
```

to `prime_bound=211`, `max_odd_part=1000000`, and `depth=16..42`.  That
combinatorial enumeration did not finish within a useful interactive window
and was stopped.  The completed exact oracle above is the cleaner evidence:
even a much stronger sampled oracle remains constant times `sqrt(p)`.

The earlier finished mixed optimizer remains the best broad search record:

```text
levels_tested=80940
best depth=40, odd_part=1
proxy_over_sqrt=1.649267
```

## Why The Hybrid Does Not Beat Sqrt

The verifier equation

```text
Z_40(A,x)=0
```

is a marked `X1(2^40)/{+-1}` condition.  Eliminating `x` forgets the marked
ray and mostly projects to the whole Montgomery line over an algebraic
closure.  Over `F_p`, it enforces only the `2^40` Frobenius eigenvalue residue.

Adding odd trace residues gives a CRT condition on the Hasse trace:

```text
t mod N in target residues.
```

To isolate a constant number of Hasse traces, `N` must be on the order of
`sqrt(p)`.  Pricing that residue condition by even the optimistic `Gamma0(N)`
index keeps the total at square-root scale.

Therefore the hybrid route reduces to one of two already-known bottlenecks:

```text
construct target trace A:
  large-discriminant CM / fixed isogeny class selector;

construct marked 2^40 ray directly:
  X1 orientation selector.
```

No current trace-residue/verifier combination supplies the requested
asymptotic speedup.

## Do Not Mark The CM Quotient By The Ray

The explicit CM-plus-ray degree audit is:

```text
p24/cm_ray_class_orientation_degree_audit.py
```

It prices the honest marked object: a CM `j` root together with an x-only
`2^40` ray orientation.  The x-only orientation cover has degree

```text
phi(2^40)/2 = 2^38.
```

For the best third trace:

```text
h = 205880396014,
h * 2^38 = 56591972337130160521216
            = 5.659197e10 * sqrt(p).
```

Even if the dream unmarked quotient of degree `66254` were already available,
marking it by the verifier ray would have degree

```text
66254 * 2^38 = 18211760846667776
              = 1.821176e4 * sqrt(p).
```

So the class-field construction should not include `Z_k` or the `2^40` ray.
The only viable split is:

```text
1. construct a target-trace Montgomery A by an unmarked embedded CM quotient;
2. find x0 afterward by the constant-expected post-trace projection.
```

This leaves the same live constructive target as before: the third trace's
unmarked embedded quotient/recovery object of degrees `66254` and `3107441`.
