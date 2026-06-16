# Reduced-Anchor Kernel Section-Pairing Guardrail

The kernel-generator-invariance gate collapses generator choices **inside an
already selected subgroup/fiber**.  It does not choose the selected embedded
fiber or pair that fiber with the correct parent section.

This matters for the p24 producer theorem.  The conditional kernel surface is:

```text
fixed selected auxiliary CM/Lang subgroup kernel polynomial
  -> two anchor signs
  -> finite verifier
```

It is not:

```text
abstract quotient roots
  -> generator collapse
  -> selected embedded section for free
```

The gate checks the existing `D=-5000` tower toy and a random subset-sum
control.  In the tiny embedded tower, the true child subset above each top
period is unique by sum.  In a modest random control (`20 choose 10` over
`F_101`), many subsets have the same sum.  At p24 scale, a trace/sum constraint
alone has far too little entropy:

```text
first layer: choose 157 roots from 314
second layer: choose 211 roots locally from 66254
```

So the remaining producer must still supply section pairing, relative
class-character traces, an embedded relative morphism, or an equivalent
phase-aware CM/Lang identity.
