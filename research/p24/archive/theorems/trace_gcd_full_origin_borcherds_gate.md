# Trace-GCD Full-Origin Borcherds Gate

Date: 2026-06-06

This note records the checked finite handoff for the full-origin version of
the trace-GCD Chow/Borcherds route.

## Why This Gate Exists

The reduced trace-GCD target is still:

```text
Pi_right = product_{t mod 211} Delta(t),
Delta(t) = det(P V_t A).
```

The origin-norm power theorem says that, after p-integral covariance choices,
a full-origin determinant product satisfies:

```text
prod_all_origins Delta_origin
  = p-unit * Pi_right^(n*m/211).
```

For p24:

```text
n*m/211 = 3107441 * 314 = 975736474.
```

So a closed p-unit formula for the full-origin product would imply
`Pi_right != 0`, and hence all 211 translated Chow/Schubert tests are good.

The finite implication is now Lean-checked in:

```text
p24/lean/TraceGcdFullOriginBorcherdsGate.lean
```

## Lean Interface

The checked route is:

```text
zero local intersection for psiFull
=> psiFull is a p-unit

p-unit comparison:
  psiFull -> actual full-origin norm

full-origin norm detects right-product zero:
  Pi_right = 0 => fullNorm = 0

right product detects Chow zeros:
  Chow_t(W,C) = 0 => Pi_right = 0

Chow zero detects translated Schubert bad event
=> selected row good.
```

The final theorem is:

```text
selected_good_from_full_origin_borcherds
```

and the payload bound is:

```text
p24_full_origin_borcherds_payload_subsqrt:
  2 < sqrt(p)
```

using the conservative integer bound `sqrt(p) = 10^12`.

## Arithmetic Theorem Still Missing

The gate deliberately does not prove the hard part.  A successful arithmetic
producer must construct a phase-aware full-origin section `psiFull` such that:

```text
div(psiFull)
  = pulled-back full-origin trace-GCD Chow divisor
    + harmless boundary/vertical terms,
```

and:

```text
psiFull(CM_p24) = p-unit * prod_all_origins Delta_origin.
```

Then a local-intersection or Borcherds valuation formula must prove that
`psiFull(CM_p24)` is a p-unit at every prime above `p = 10^24 + 7`.

## Boundary From Small Computation

The small scalar miner:

```text
p24/trace_gcd_global_product_miner.py
p24/trace_gcd_global_product_mining_boundary.md
```

shows why the theorem must be divisor-honest.  In the pinned small row,
low-weight formulas for the isolated scalar `Pi_all` appear, but they do not
match the right-phase vector.  The full-origin product is even more symmetric,
so a scalar identity alone is not evidence that the trace-GCD determinant
section has been recognized.

The full-origin route is therefore viable only as a closed
divisor/local-intersection theorem.  Computing the product by enumerating the
class torsor, or recognizing the final scalar after the fact, does not give
the requested asymptotic speedup.
