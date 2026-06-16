# Larger Upstream One-Witness Dataset Audit

Date: 2026-06-04

Purpose: independently audit the `pp28`, `pp30`, and `pp32` one-witness
datasets linked from Sutherland's upstream DANGER3 README for statistical or
probabilistic structure that could help find a strict certificate for
`p = 10^24 + 7`.

No remote archive was saved locally.  The audit used HEAD requests, bounded
prefix streams for all three URLs, and one sparse full stream of `pp28`.

## Commands

```text
python3 -m py_compile p24/upstream_large_one_witness_audit.py
python3 p24/upstream_large_one_witness_audit.py --heads
python3 p24/upstream_large_one_witness_audit.py --prefixes --prefix-rows 1300000
python3 p24/upstream_large_one_witness_audit.py --pp28-sparse --stride 997 --tail-keep 20000 --near-delta 32
python3 - <<'PY'
from p24.upstream_large_one_witness_audit import LOCAL_PP24, URLS, open_local_rows, open_url_rows, row_hash
local_count, local_last, local_digest = row_hash(open_local_rows(LOCAL_PP24), None)
print(f"local_pp24 rows={local_count} last_p={local_last} sha256={local_digest}")
for label, url in URLS.items():
    count, last_p, digest = row_hash(open_url_rows(url), local_count)
    print(f"{label}_first_{local_count} rows={count} last_p={last_p} sha256={digest} equal_local={digest == local_digest}")
PY
```

## Remote Metadata

```text
pp28 content-length=174789799  accept-ranges=bytes
pp30 content-length=684123983  accept-ranges=bytes
pp32 content-length=2702673797 accept-ranges=bytes
```

The files are gzip streams, so byte ranges are useful for prefixes and
metadata, but not for cheap random access to high-prime rows without building
an index or decompressing from the beginning.

## Witness Selection

The local `pp24` file is exactly the prefix of each larger one-witness file:

```text
local_pp24 rows=1077869 last_p=16777213 sha256=c85fad4afb36898ff43e0e6094534c56f92bdabc2316d6e7243dc8fcfde755c1
pp28_first_1077869 equal_local=True
pp30_first_1077869 equal_local=True
pp32_first_1077869 equal_local=True
```

The first 1,300,000 rows, which extend past `pp24`, are also identical across
`pp28`, `pp30`, and `pp32`:

```text
rows=1300000 last_p=20495869 sha256=395865c9803c994dcdf40f16abfded94f831f1e3225e76482fa5d68c8e558196
remote_prefix_hashes_equal=True
```

This supports treating the files as ordered extensions from the same
one-witness generator.  It does not reveal a new selected-witness rank rule
beyond the earlier all-triple overlap audit.

## Prefix Statistics

For the 1,300,000-row remote prefix:

```text
split_counts={-1: 1296845, 1: 3155}
terminal_counts={'quadratic_root': 1584, 'zero_root': 1298416}
top_sign_pairs=[((1, -1, -1), 973236), ((-1, 1, -1), 323609), ((1, 1, 1), 1997), ((-1, -1, 1), 1158)]
A_over_p_quantiles=0.009859,0.100189,0.250584,0.500461,0.750864,0.900251,0.990079
x_over_p_quantiles=0.009896,0.099680,0.249836,0.499699,0.749986,0.899903,0.990008
```

The selected witnesses are overwhelmingly in the nonsplit/zero-terminal
generator branch, but within that branch `A/p` and `x0/p` look uniform.  The
`p` residue slices are balanced in prime count and show no special enhancement
for the target residues `p % 16 = 7` and `p % 12 = 11`.

## Full pp28 Sparse Pass

Streaming all of `pp28` gave:

```text
rows_seen=14630841
last_p=268435399
p_mod8_counts={1: 3657088, 3: 3657723, 5: 3658133, 7: 3657897}
target_order_count_full_hist={1: 14366, 2: 3603724, 3: 7293053, 4: 3719698}
```

Stride sample, one row every 997:

```text
rows=14675
split_counts={-1: 14663, 1: 12}
terminal_counts={'quadratic_root': 5, 'zero_root': 14670}
A_over_p_quantiles=0.009257,0.101528,0.255201,0.507093,0.751111,0.900274,0.990517
x_over_p_quantiles=0.011335,0.103125,0.251906,0.507437,0.752559,0.901342,0.989084
```

Final 20,000 rows near `2^28`:

```text
split_counts={-1: 19993, 1: 7}
terminal_counts={'quadratic_root': 3, 'zero_root': 19997}
A_over_p_quantiles=0.010640,0.100718,0.247023,0.498234,0.753186,0.903636,0.990372
x_over_p_quantiles=0.010085,0.102423,0.252943,0.506476,0.750575,0.900764,0.988906
```

The high end of `pp28` has the same behavior as the smaller prefix: fixed
branch bias, no visible compression of `A` or `x0`.

## Near-Square Family

The target prime is in the family `p = n^2 + 7`.  In `pp28`:

```text
near_square_delta_7 rows=1888
split_counts={-1: 1883, 1: 5}
terminal_counts={'quadratic_root': 2, 'zero_root': 1886}
top_sign_pairs=[((1, -1, -1), 1883), ((-1, -1, 1), 3), ((1, 1, 1), 2)]
A_over_p_quantiles=0.011422,0.099891,0.246694,0.504224,0.751163,0.895337,0.985807
x_over_p_quantiles=0.014297,0.095120,0.248278,0.500551,0.739196,0.893563,0.989969
```

For `p = n^2 + delta` with `delta <= 32`:

```text
rows=30979
split_counts={-1: 30882, 1: 97}
terminal_counts={'quadratic_root': 57, 'zero_root': 30922}
A_over_p_quantiles=0.009606,0.099723,0.249118,0.500655,0.751639,0.898252,0.989315
x_over_p_quantiles=0.010378,0.096083,0.248906,0.495854,0.746735,0.899263,0.989809
```

The `n^2+7` slice does make the selected nonsplit sign pair almost constant
at `(chi(A+2), chi(A-2), chi(A^2-4)) = (1, -1, -1)`, but the actual selected
`A` and `x0` remain uniform-looking.  This is at most a constant branch filter,
not an asymptotic selector.

## Conclusion

The larger one-witness files do not expose a predictive rule for `A`, `x0`,
split class, terminal branch, residue class, near-square primes, or selected
witness rank that would beat sqrt scaling.

The useful information is negative but clarifying:

```text
one-witness data = same generator extensions + strong fixed branch bias
selected A,x0 within branch = uniform-looking
near-square n^2+7 = fixed sign-pair constant only
```

So the data reinforces the current frontier: a p24 speedup still needs a
growing-depth mathematical selector, not another fixed residue or terminal
branch statistic.
