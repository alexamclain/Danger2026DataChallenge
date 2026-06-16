# Trace-GCD Global Chow/Borcherds Handoff

Date: 2026-06-06

The orbitwise Chow payload is:

```text
Pi_O = prod_{t in O} Chow_t(W,C),
O in Frobenius orbits on Z/211Z.
```

For p24 this gives seven products and seven inverses.  This is the safest
factorwise producer surface because each `Pi_O` lives over a specific
irreducible right factor.

But a Borcherds/local-intersection construction may naturally produce the
full right translate divisor:

```text
D_all = sum_{t mod 211} { W : W cap V_t^{-1}C != 0 }.
```

The corresponding scalar is:

```text
Pi_all = prod_{t mod 211} Chow_t(W,C)
       = prod_O Pi_O.
```

If `Pi_all` is honestly constructed and is a p-unit, then no individual
Chow value can vanish:

```text
Chow_t(W,C)=0  =>  Pi_all=0,
Pi_all p-unit  =>  Pi_all != 0.
```

Thus a global product formula would also finish the finite trace-GCD
certificate, with payload:

```text
Pi_all, Pi_all^{-1}
```

or only two base-field elements.

## Lean Gate

The phase-aware Chow/Borcherds gate now covers both variants:

```text
p24/lean/TraceGcdChowBorcherdsPUnitGate.lean
```

Orbitwise route:

```text
zero local intersection for Psi_O
+ p-unit comparison Psi_O -> Pi_O
+ orbit Chow zero-detection
=> selected row good.
```

Global route:

```text
zero local intersection for Psi_all
+ p-unit comparison Psi_all -> Pi_all
+ global Chow zero-detection
=> selected row good.
```

Both payload bounds are checked:

```text
2 * 7 < sqrt(p),
2     < sqrt(p).
```

## Producer Implication

This slightly changes the theorem search:

```text
factorwise Fitting/class-field producer:
  construct seven orbit norms Pi_O;

Borcherds/local-intersection producer:
  it may be enough to construct the single full divisor product Pi_all.
```

The global route is not weaker arithmetically if the product formula is
honest: p-unitness of the total product excludes every zero.  It may even be
more natural, because Borcherds products often attach to Galois-invariant
divisor sums rather than to individual right Frobenius factors.

The caveat is honesty.  A supplied scalar must be proved to be the actual
full Chow/Fitting norm of the trace-GCD determinant section.  Otherwise the
two-element payload is meaningless.

The first small actual-CM global-product miner makes this caveat concrete:

```text
p24/trace_gcd_global_product_miner.py
p24/trace_gcd_global_product_mining_boundary.md
```

On the pinned `D=-13319`, `q=13463`, `right=7` row, low-weight formulas for
the isolated scalar `Pi_all` appear quickly, but none of them match the actual
right-phase vector.  The mod-`2` phase-vector obstruction from the bounded
unit-span scan also remains.  Thus scalar recognition in `F_q^*` is too weak;
the producer theorem must compare divisors or local intersections.

## Current Status

No explicit `Psi_all` is known.  The bounded phase-unit dictionary did not
find a simple product formula:

```text
p24/trace_gcd_chow_phase_divisor_span_boundary.md
p24/trace_gcd_global_product_mining_boundary.md
```

So this is not a certificate yet.  It is a sharper target for the missing
Borcherds/Fitting theorem: construct either the seven orbit divisors or the
single full right Chow divisor, prove the selected p24 local valuation is
zero, and compare to the actual trace-GCD determinant section up to p-units.
