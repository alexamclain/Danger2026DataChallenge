# Tensor Factor Plucker Norm Miner

This note records the first bounded search for stable Plucker norm identities
after the CS/statistics side pass.

## Question

For a maximal minor `P` of a marginal matrix, form the beta product:

```text
Pi_P = prod_{beta mod n} P(Omega_beta).
```

If `Pi_P` has unusually low subfield degree, small/factorable base norm, or
stable nonzero behavior not shared by random tensor-factor controls, then it
could be the visible edge of a class-field norm identity.

## Script

Added:

```text
p24/tensor_factor_plucker_norm_miner.py
```

The script:

```text
1. builds the top-coordinate marginal matrix for one small tensor row;
2. enumerates or samples maximal Plucker minors;
3. computes beta products for each minor;
4. computes product subfield degree and norm down to the base field;
5. compares best CM minors with random tensor-factor controls of the same
   matrix shape.
```

It caches beta-shifted matrices so rectangular Plucker scans stay small.

## Pinned Full-Axis Square Sanity Check

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_plucker_norm_miner.py \
  --only-D -10919 --only-m 12 --max-h 200 --max-abs-D 12000 \
  --max-n 80 --q-stop 200000 --max-extension-degree 8 \
  --max-factor-degree 20 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 2 --subdegree 3 --windows 2 \
  --target full --random-trials 40 --max-minors 200 --top 10 \
  --include-alpha-products
```

Result:

```text
matrix_shape=6x6
minors_tested=1
cm_best:
  zeros=0 distinct=1 prod_deg=2 norm_height=2544
  alpha_products_distinct=2
random_controls:
  best_height_min=56
  best_height_max=5598
  best_subfield_degree_hist={2:40}
```

No special CM norm structure appears in the square determinant.

## Rectangular Component Plucker Scan

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_plucker_norm_miner.py \
  --only-D -10919 --only-m 12 --max-h 200 --max-abs-D 12000 \
  --max-n 80 --q-stop 200000 --max-extension-degree 8 \
  --max-factor-degree 20 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 2 --subdegree 3 --windows 2 \
  --target 4 --without-constant --random-trials 30 \
  --max-minors 200 --top 12 --include-alpha-products
```

Result:

```text
matrix_shape=3x6
minors_tested=20
cm_aggregate:
  zero_free_minors=20
  product_subfield_degree_hist={2:20}
  beta_zero_count_hist={0:20}
cm_best:
  cols:0,1,3 zeros=0 distinct=13 prod_deg=2 norm_height=331
random_controls:
  nonzero_minor_count_min=20
  nonzero_minor_count_max=20
  best_height_min=5
  best_height_max=857
  best_subfield_degree_hist={2:30}
```

Again the CM products are robustly nonzero, but their subfield degree and norm
height look random-generic.

## Rectangular Constant-Plus Component Scan

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_plucker_norm_miner.py \
  --only-D -10919 --only-m 12 --max-h 200 --max-abs-D 12000 \
  --max-n 80 --q-stop 200000 --max-extension-degree 8 \
  --max-factor-degree 20 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 2 --subdegree 3 --windows 2 \
  --target 3 --random-trials 30 --max-minors 200 --top 12 \
  --include-alpha-products
```

Result:

```text
matrix_shape=3x6
minors_tested=20
cm_aggregate:
  zero_free_minors=20
  product_subfield_degree_hist={2:20}
  beta_zero_count_hist={0:20}
cm_best:
  cols:1,2,4 zeros=0 distinct=13 prod_deg=2 norm_height=342
random_controls:
  best_height_min=2
  best_height_max=735
  best_subfield_degree_hist={2:30}
```

Adding the constant row does not reveal an obvious low-degree or low-height
norm identity.

## Neighboring Row Check

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_plucker_norm_miner.py \
  --only-D -8711 --only-m 12 --max-h 200 --max-abs-D 12000 \
  --max-n 80 --q-stop 200000 --max-extension-degree 8 \
  --max-factor-degree 20 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 2 --subdegree 1 --windows 3 \
  --target 4 --without-constant --random-trials 25 \
  --max-minors 20 --top 10 --include-alpha-products
```

Result:

```text
matrix_shape=3x3
minors_tested=1
cm_best:
  zeros=0 distinct=11 prod_deg=2 norm_height=3347
random_controls:
  best_height_min=219
  best_height_max=4099
  best_subfield_degree_hist={2:25}
```

This also looks generic.

## Conclusion

The first stable-coordinate-product search is negative:

```text
ordinary trace-coordinate Plucker beta-products are nonzero,
but full-degree and random-looking in the tested small rows.
```

This does not rule out a Plucker p-unit theorem.  It does rule out the easiest
data-mined version:

```text
a natural coordinate minor has a visibly small/factorable norm product.
```

The remaining norm route needs either:

```text
1. a more intrinsic exterior norm, not an ordinary coordinate Plucker product;
2. a special CM-derived coordinate/basis change before taking minors;
3. an exact class-field identity whose norm is full-support but still a p-unit.
```
