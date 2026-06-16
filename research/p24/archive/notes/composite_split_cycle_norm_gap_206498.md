# Composite Split-Cycle Norm Gap To 206498

Date: 2026-06-07

Question: could the known order-`3107441` recovery representative

```text
2 * 463 * 223^(-1)
```

with norm `206498` have a smaller signed split-prime-power representative
that was missed by the earlier `norm <= 66254` zero-lemma audit?

I ran the bounded p24-real search:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/composite_split_cycle_audit.py \
  --prime-bound 206497 --max-factors 0 --max-norm 1 \
  --exhaustive-norm 206497 --show 8
```

This computes class logs for all split rational primes below `206498`, then
enumerates signed split-prime-power products of norm at most `206497`.

Output summary:

```text
split_prime_logs=9265
exhaustive_signed_prime_power_products_norm_le_206497
  index_314:   hits exist
  index_422:   hits exist
  index_66254: none
```

Conclusion:

```text
no_signed_split_prime_power_recovery_representative_below_206498=1
known_representative_2_463_223inv_is_first_visible_in_this_model=1
```

This still does not construct the selected p24 root.  It closes the remaining
bounded split-prime-power gap below the known recovery representative, so the
split-correspondence shortcut is not hiding just above the `66254` threshold.

Ramified follow-up:

```text
p24/composite_split_cycle_ramified_norm_gap_206498.md
```

Including the ramified prime `599` still gives no order-`3107441`
representative below norm `206498`.
