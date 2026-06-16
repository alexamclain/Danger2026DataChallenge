# Composite Split-Cycle Ramified Norm Gap To 206498

Date: 2026-06-07

This is the ramified-prime follow-up to:

```text
p24/composite_split_cycle_norm_gap_206498.md
```

The split-only gap closure found no signed split-prime-power representative
of the order-`3107441` recovery class below the known norm `206498`.  The
earlier `norm <= 66254` audit had separately checked the ramified prime
`599`, but the widened `66254..206498` window had not.

Script:

```text
p24/composite_split_cycle_ramified_norm_gap_206498.py
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 \
  p24/composite_split_cycle_ramified_norm_gap_206498.py \
  --norm-bound 206497 --show 8
```

Output summary:

```text
split_prime_logs=9265
ramified_prime=599 log=102940198007 index=102940198007 order=2
rows_with_ramified=9266

exhaustive_signed_split_or_ramified_prime_power_products_norm_le_206497
  index_314:   hits exist
  index_422:   hits exist
  index_66254: none
```

Conclusion:

```text
ramified_prime_599_included=1
no_order_3107441_representative_below_known_norm_with_599=1
```

Thus the small-correspondence recovery shortcut is closed below the known
representative `2 * 463 * 223^(-1)` of norm `206498`, even after adding the
ramified genus class.
