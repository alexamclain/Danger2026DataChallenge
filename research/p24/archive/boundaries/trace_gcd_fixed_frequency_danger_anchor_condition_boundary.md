# DANGER Anchor-Condition Boundary

Date: 2026-06-06

## Point

The p24 trace is special because the target curve order has very large
2-adic valuation.  A tempting source for the missing anchor theorem is:

```text
strict DANGER 2-adic order condition
  => relative trace-defect H-coset equality.
```

This boundary tests that idea on Sutherland's local `pp10` all-triples data.
For each small Pomerance triple, it computes the Montgomery trace, chooses the
sign satisfying the DANGER order congruence, materializes the corresponding
small CM root cycle, and tests every global child section for every coprime
decomposition with a nontrivial right quotient character.

## Result

Executable:

```text
p24/trace_gcd_fixed_frequency_danger_anchor_condition_boundary.py
```

Default scan:

```text
testable_danger_cm_cases=10
danger_anchor_decompositions_with_any_passing_section=0/19
danger_anchor_global_section_passes=0/385
```

The ten testable rows are:

```text
p=359,  trace=-24, h=14
p=443,  trace=-4,  h=15
p=491,  trace=-20, h=14
p=587,  trace=12,  h=26
p=643,  trace=4,   h=14
p=653,  trace=14,  h=14
p=773,  trace=6,   h=26
p=887,  trace=-8,  h=22
p=907,  trace=12,  h=22
p=983,  trace=24,  h=33
```

Each row comes from an actual Pomerance triple and satisfies the appropriate
small DANGER x-only order congruence.

## Consequence

The strict 2-adic curve-order condition is not enough to force the anchor
descent identity.  For p24, the proof must use more than:

```text
target trace congruence;
large 2-power order;
generic CM root-cycle structure.
```

The remaining theorem still has to explain the section-aware trace-defect
H-coset equality for the specific weighted `G_chi`/trace-GCD packet, or move
to a different p-unit producer surface.
