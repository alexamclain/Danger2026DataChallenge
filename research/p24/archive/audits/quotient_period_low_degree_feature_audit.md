# Quotient Period Low-Degree Feature Audit

Date: 2026-06-05

This audit tests whether the first-trace order-19 shortcut might come from a
bounded local formula rather than a global class-field identity.

The p24 motivation is:

```text
t = 1020608380936
ell = 19
index(<ell>) = 19
recovery degree = 14670196166
```

If the `ell=index` coincidence created a local selector, small analogues
should show the quotient period

```text
y(j) = sum of j-roots in the horizontal ell-cycle component of j
```

as a low-degree expression in local `Phi_ell` features.

## Script

```text
p24/quotient_period_low_degree_feature_audit.py
```

Reproducible run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/quotient_period_low_degree_feature_audit.py \
  --max-abs-d 50000 --min-h 60 --max-h 160 \
  --min-ell 3 --max-ell 31 --max-cases 2 --max-degree 4
```

The local feature vector is deliberately generous:

```text
1,
j,
total Phi_ell neighbor sum,
horizontal neighbor sum,
descending neighbor sum,
horizontal neighbor product.
```

So failure here is stronger than failure using only raw local
`Phi_ell(j,Y)` coefficients.

## Results

The run audited two `ell=index` examples:

```text
D=-12279, h=60, ell=5, order=12, index=5, q=12343
D=-18199, h=91, ell=7, order=13, index=7, q=18523
```

For both examples:

```text
degree 1: no formula
degree 2: no formula
degree 3: no formula
```

At degree 4 a formula appears, but only because the feature matrix reaches
full row rank:

```text
D=-12279: feature_rank = rows = 60
D=-18199: feature_rank = rows = 91
```

That is interpolation, not an asymptotic selector.

## Boundary

This does not disprove every possible identity.  It rules out the useful easy
version:

```text
bounded local Phi_ell feature formula
```

even after including the horizontal pair data.  The surviving order-19 theorem
must therefore be genuinely global:

```text
embedded class-field period identity,
relative content/norm theorem,
or a determinant/Fitting p-unit statement.
```

This keeps computation useful as a falsifier, but it does not move the
certificate engine toward local feature regression or ML-style selectors.
