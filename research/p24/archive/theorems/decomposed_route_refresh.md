# Decomposed Route Refresh

This note refreshes the best surviving constructive shape after the ray-kernel
and dataset passes.

## p24 Degree Accounting

Running

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/decomposed_cm_tradeoff_audit.py
```

confirms the balanced split for the third strict trace:

```text
h = 205880396014 = 66254 * 3107441
sqrt(p) = 1000000000000
best_degrees = 66254 * 3107441
best_largest_degree_over_sqrt_p = 3.107441e-06
best_sum_degrees = 3173695
```

So if we had the embedded decomposed equations, the final root work would beat
the `sqrt(p)` yardstick by a huge factor.

## Calibration

The small calibration

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/embedded_decomposition_calibration.py
```

uses `D=-5000`, `q=1259`, `h=30=6*5`.  It constructs:

```text
V_degree = 6
U_selected_degree = 5
```

instead of one degree-30 Hilbert class polynomial.

But the script explicitly obtains these polynomials from:

```text
1. a seed embedded CM root;
2. the full horizontal isogeny cycle of embedded j roots;
3. sums over embedded cosets.
```

This is exactly the p24 missing primitive in miniature.

## Boundary

The decomposed route remains the cleanest positive target, but it is not
currently operational.  The known construction is:

```text
embedded CM root set / class-action cycle
  -> quotient period polynomial V of degree 66254
  -> selected recovery polynomial U of degree 3107441
  -> target j root.
```

The desired construction would need:

```text
quotient period polynomial V and recovery relation U
```

without first building the degree-`h` embedded root set.  Abstract class-field
towers, auxiliary ray generators, and the uploaded small-prime witness data do
not supply the pairing from their roots back to the embedded level-1 `j`
torsor.

Thus this route has the right asymptotic output shape but still reduces to the
same theorem:

```text
construct embedded non-genus relative traces/periods for the 157 and 211
Hilbert class layers, or prove an equivalent selected-origin finite-field
identity.
```

The tail after a successful embedded `j` root is now explicit:

```text
p24/post_j_root_to_triple_boundary.md
p24/post_j_root_to_triple_toy.py
```

In the small conductor-2 analogue, every conductor-2 `j` root lifts to
nonsplit Montgomery `A` values and then to verifier-passing `x0` values by
odd-part projection.  Thus the decomposed route's missing object is exactly
the embedded `j` root / recovery phase, not a hidden 2-adic verifier tail.

The selected-chain verifier and the seedless modular-recurrence boundary are
now consolidated in:

```text
p24/phase_chain_executable_frontier.md
p24/phase_chain_certificate_verifier.py
```

The verifier checks a `3107811`-slot selected-chain artifact.  The
seedless-cycle audit shows that modular-polynomial recurrences become small
only after an embedded subgroup projector or equivalent quotient invariant is
already supplied.

The direct prescribed-trace route is also recorded as a boundary:

```text
p24/prescribed_trace_direct_route_boundary.md
```

It confirms that Waterhouse/Rueck/Voloch/Mestre-style existence or
fixed-trace language does not name a seed curve for the strict p24 isogeny
class; the constructive route again requires a large-discriminant CM root.
