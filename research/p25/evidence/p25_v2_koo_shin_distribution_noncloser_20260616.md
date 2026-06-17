# P25 v2 Koo-Shin Distribution Noncloser

Updated: 2026-06-16

## Purpose

Recheck Koo-Shin 2010 after the conductor-39 target became selector-rigid.  The
question is whether Theorem 5.2, Lemma 6.1, or Theorem 6.2 can now close source
stage for one of the four legal minimal Hilbert-90 preimages.

This is a bounded pass.  It does not broadly reread the paper.

## Pages Read

- `sources/koo-shin-2010.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_koo_shin_distribution_noncloser_gate.py
```

The gate returned `p25_v2_koo_shin_distribution_noncloser_rows=1/1`.

## Source Clauses

The live cockpit has the Koo-Shin 2010 extract available at:

```text
incoming/extracted/s00209-008-0456-9.pdf.extract.txt
```

The pass checks these source roles:

```text
Theorem 5.2 = prime-level constant-product rigidity / root-descent context
Lemma 6.1  = full-fiber distribution relation for Siegel functions
Theorem 6.2 = sufficient condition and order formula for X_1(N) products
```

These are useful helper clauses, but none emits:

```text
one legal minimal H90 preimage
+ support-156 Yang product
+ finite divisor/additive theorem, or period-156 value theorem
+ Norm_156(Y_507) boundary
```

## Legal Row Check

The four selector-rigid rows have quotient-`C4` constants:

```text
( 3,  3, -3, -3)
(-3,  3,  3, -3)
(-3, -3,  3,  3)
( 3, -3, -3,  3)
```

Each row has two positive and two negative quotient-`C4` cosets.  None is a
constant exponent row, so Theorem 5.2's constant-product rigidity is not a
direct p25 collapse theorem for the current target.

The rows are also mod-13 rectangle edges:

```text
m=1: 7H against 4H
m=2: 7H against H
m=4: 2H against H
m=8: 2H against 4H
```

That rectangle structure is exactly why prime-axis or one-coset projection
answers lose the mixed conductor-39 source.

## Routing

```text
Theorem 5.2 alone:
  decision = helper_not_closer
  reason   = constant-product/root-descent context, not mixed finite theorem

Lemma 6.1 distribution alone:
  decision = helper_not_closer
  reason   = relates the fiber lift to source words, but supplies no value

Theorem 6.2 alone:
  decision = source_legality_not_closer
  reason   = sufficient condition/order formula, not p25 finite theorem
```

## Verdict

```text
helper_rows = 3
direct_source_closer_rows = 0
current_source_theorem_rows = 0
distribution_can_police_future_theorem = yes
distribution_emits_current_theorem = no
next = source theorem or expert falsifier for a finite value/divisor theorem
       on one of the four legal minimal H90 preimages
```
