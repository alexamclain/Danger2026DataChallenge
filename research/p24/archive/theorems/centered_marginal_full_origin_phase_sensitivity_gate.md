# Centered Full-Origin Phase-Sensitivity Gate

Date: 2026-06-06

## Point

The centered full-origin Borcherds route hopes to prove a p-unit theorem for a
closed product:

```text
prod_all_origins Delta_origin.
```

The existing origin-power theorem shows this product is a p-unit multiple of
the centered right-window product to a known power.  This gate checks whether
the full-origin product is determined by unordered recovery fibers, or whether
it still depends on embedded phase/order data.

## Actual-CM Test

Pinned row:

```text
D=-13319
q=13463
h=140
m=28
n=5
pair=(4,7)
```

For each quotient residue `r mod m`, the control preserves the unordered
fiber:

```text
{j_{r+m*k} : 0 <= k < n}
```

but shuffles the child order inside those fibers.

Genuine cyclic origin shifts preserve the full-origin product in the row:

```text
cyclic_origin_shift_product_preserved=4/4
```

But unordered fiber shuffles change the product and the reduced right
sequence:

```text
fiber_multisets_preserved_by_shuffle=8/8
fiber_shuffle_alpha_product_changed=8/8
fiber_shuffle_right_sequence_changed=8/8
fiber_shuffle_zero_products=0/8
```

## Consequence

The centered full-origin product is not a symmetric function of unordered
relative recovery fibers.  A successful full-origin Borcherds/Fitting theorem
must be phase-aware:

```text
construct the Chow/Fitting divisor directly,
or retain embedded class-field phase/order data.
```

It cannot be replaced by unordered fiber data, trace-only data, or recovery
fiber multisets.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_full_origin_phase_sensitivity_gate.py
```

Key markers:

```text
cyclic_origin_shift_product_preserved=4/4
fiber_multisets_preserved_by_shuffle=8/8
fiber_shuffle_alpha_product_changed=8/8
fiber_shuffle_right_sequence_changed=8/8
fiber_shuffle_right_factorization_failed=0/8
fiber_shuffle_zero_products=0/8
cyclic_origin_shift_preserves_the_full_origin_product=1
unordered_recovery_fibers_do_not_determine_centered_full_origin_product=1
full_origin_borcherds_producer_must_be_phase_aware=1
closed_divisor_formula_cannot_be_replaced_by_unordered_fiber_data=1
```
