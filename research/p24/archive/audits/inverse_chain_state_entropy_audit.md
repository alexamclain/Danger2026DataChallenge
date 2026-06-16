# Inverse-Chain State Entropy Audit

Date: 2026-06-04

Purpose: close the tempting meet-in-the-middle route for the strict x-only
halving chain.

The verifier asks for a rational x-only state whose `2^40` multiple is the
point at infinity.  A natural idea is to construct or rank curves by a
half-depth inverse tree, then finish the remaining depth by a residual search.

## Exact Small-Field Calibration

Run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 p24/inverse_chain_mitm_tradeoff_audit.py --min-p 10000 --max-p 80000 --max-rows 4 --depths 2 3 4 5 6 7 8 10 12
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 p24/inverse_mitm_scaling_audit.py --min-p 2000 --max-p 30000 --max-rows 4 --prefix-fracs 0.005 0.01 0.02 0.05 0.10 0.25
python3 p24/inverse_tower_intersection_degree_audit.py
```

Representative aggregate output:

```text
h total full x1_partial x1_residual x1_product x0_partial x0_residual x0_product
2 84628 3026 84628 0.03575649 27.966953 84628 0.03575649 27.966953
3 84628 3026 42308 0.07152312 27.966953 63468 0.04767757 27.966953
4 84628 3026 31728 0.09537317 27.966953 63468 0.04767757 27.966953
5 84628 3026 20740 0.14590164 27.966953 63468 0.04767757 27.966953
6 84628 3026 10242 0.29545011 27.966953 63468 0.04767757 27.966953
7 84628 3026 5392 0.56120178 27.966953 63468 0.04767757 27.966953
8 84628 3026 3026 1.00000000 27.966953 63468 0.04767757 27.966953
```

The partial-depth filter and the residual rarity are reciprocal.  The product
is the full-depth cost for every split.

Ranking by shallow inverse-tree mass gives only constant lifts.  For example,
in the exact `p=14407` row:

```text
rank_depth=3 full_depth=7 A=14405 full_hits=496 base=0.034432
max_rank_mass=8 A_at_max_mass=5400 full_hits_at_max_mass=496
prefix=0.250 hits=333 lift=2.686 capture=0.671
```

The full hits concentrate inside the partial-depth bucket because that bucket
is exactly the partial 2-adic condition; within it they remain spread at the
expected residual rate.

## p24 Degree Accounting

For `p=10^24+7`, `k=40`:

```text
split_depth degree_C degree_D bezout_product product_over_sqrt
4+36        16       68719476736 1099511627776 1.099512
8+32        256      4294967296  1099511627776 1.099512
12+28       4096     268435456   1099511627776 1.099512
16+24       65536    16777216    1099511627776 1.099512
20+20       1048576  1048576     1099511627776 1.099512
```

So a balanced split reduces the largest single polynomial degree to `2^20`,
but eliminating the middle x-coordinate has Bezout/product degree `2^40`.

## Conclusion

Inverse-chain MITM is a useful representation change, not an asymptotic
selector.  It moves the 40 bits of orientation entropy between stages unless a
new structure supplies a finite collision key or a growing-depth section of
`X1(2^d)`.

```text
conclusion=partial_inverse_halving_MITM_does_not_beat_sqrt_scaling_without_extra_structure
```
