# Complement Trace Recovery Relation

This note connects the complement-trace scalar target to the actual object
needed for a DANGER3 certificate: one CM `j` root, hence a Montgomery
parameter and a 2-power point.

## End-To-End Algebra

Let

```text
h = m*n,        gcd(m,n)=1,
G = <g> ~= C_h,
H = <g^m>,      |H| = n,
K = <g^n>,      |K| = m.
```

The complement trace values are

```text
Y_k = Tr_K(g^(m*k) j_0)
    = sum_{r=0}^{m-1} j_{n*r + m*k},
      0 <= k < n.
```

They form a quotient polynomial

```text
F(Y) = prod_k (Y - Y_k),       degree n.
```

Above one quotient root `Y_k`, the recovery polynomial is

```text
U_k(J) = prod_{r=0}^{m-1} (J - j_{n*r + m*k}),       degree m.
```

Equivalently, one can interpolate a bivariate relation

```text
U(Y,J) = J^m + sum_{d=0}^{m-1} c_d(Y) J^d,
deg c_d < n,
```

such that

```text
U(Y_k,J) = U_k(J).
```

For p24 with the balanced complement split:

```text
n = 3107441,
m = 66254.
```

Thus, if the quotient trace polynomial and recovery relation were available
in compressed form, root-finding degrees would be far below
`sqrt(p)=10^12`.

## Toy Construction

I added:

```text
p24/complement_trace_recovery_toy.py
```

The calibrated `D=-5000`, `q=1259`, `h=30=6*5` p24-shape toy gives:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/complement_trace_recovery_toy.py --D -5000 --m 6 --q-stop 200000
```

Output summary:

```text
D=-5000
q=1259
ell=3
h=30
m=6
n=5
quotient_values_distinct=1
all_specializations_ok=1
quotient_poly_degree=5
recovery_degree_in_J=6
relation_degree_y_max=4
```

The quotient polynomial is:

```text
Y^5 - 399*Y^4 + 608*Y^3 - 137*Y^2 - 51*Y + 228
```

and the interpolated recovery relation specializes correctly above every
quotient root.

The complementary split `m=5`, `n=6` also works:

```text
quotient_poly_degree=6
recovery_degree_in_J=5
relation_degree_y_max=5
all_specializations_ok=1
```

This verifies the exact algebraic path:

```text
embedded CM cycle
  -> complement trace quotient F(Y)
  -> degree-m recovery polynomial U(Y0,J)
  -> one CM j root.
```

Once a p24 `j` root is known, the remaining conversion to a DANGER3 triple is
the standard Montgomery/recovery step: choose a Montgomery `A` with that `j`,
then find an `x0` in the 2-primary subgroup of the curve or twist with the
target verifier depth `k=40`.

## Dense Relation Boundary

The toy also exposes a danger.  The interpolated relation has `m` coefficient
polynomials of degree `< n`, so a dense representation has about

```text
m*n = h
```

field coefficients.  For p24 this is

```text
h = 205880396014.
```

That is not the desired tower-sized object.  It is below `sqrt(p)` by a
constant for this one instance, but it is not the asymptotic speedup the goal
asks for and is far too large to materialize directly.

I added:

```text
p24/complement_trace_recovery_complexity_scan.py
```

Bounded scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/complement_trace_recovery_complexity_scan.py \
  --max-cases 80 --min-h 12 --max-h 160 --max-abs-D 60000 \
  --q-stop 600000 --summary-only
```

Output:

```text
rows=80
all_specializations_ok=1
full_y_degree_rows=80
avg_density=0.683251
min_density=0.538462
max_density=0.833333
```

Every tested recovery relation had full `Y`-degree, and the coefficient
polynomials were dense.  The small data gives no sign that naive interpolation
compresses the relation.

## Tower Decomposition Check

Because the p24 complement size is smooth,

```text
m = 66254 = 2 * 157 * 211,
```

one might hope that a tower through the factors of `K` automatically avoids
the dense degree-`m` recovery relation.  I added:

```text
p24/complement_trace_tower_toy.py
```

For the calibrated `D=-5000`, `h=30`, `m=6=2*3` toy:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/complement_trace_tower_toy.py --D -5000 --m 6 --q-stop 200000
```

Output:

```text
factor_chain=[2, 3]

level parent_size child_size factor parents deg_y_max nonzero_terms dense_slots density ok
    1           6          3      2       5         4             6          10   0.600  1
    2           3          1      3      10         9            21          30   0.700  1

total_nonzero_terms=27
total_dense_slots=40
direct_dense_slots=m*n=30
tower_slots_over_direct=1.333333
```

So a tower of dense interpolated step relations is not automatically smaller;
for this toy it is larger.  The point of a tower must be formulaic or
class-field-theoretic coefficient construction, not simply replacing one
dense table by several dense tables.

## Low-Norm K-Generator Audit

A specialized recovery fiber above one quotient root would be much more
constructive if the balanced complement subgroup

```text
K,      |K| = m = 66254
```

had small split-prime generators for its `2`, `157`, and `211` factors.  I
added:

```text
p24/complement_subgroup_generator_audit.py
```

and ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/complement_subgroup_generator_audit.py \
  --norm-bound 66254 --prime-bound 66254
```

Output:

```text
visited_products=32080
target_order=2 hits_recorded=0
target_order=157 hits_recorded=0
target_order=211 hits_recorded=0
target_order=314 hits_recorded=0
target_order=422 hits_recorded=0
target_order=33127 hits_recorded=0
target_order=66254 hits_recorded=0
```

Thus no signed split-prime-power word of norm at most `m` even lands in `K`
with one of the useful factor orders.  The balanced recovery fiber cannot be
generated by the same kind of low-norm split-prime cycle that made the
quotient candidates attractive.  It needs a nonlocal `K`-orbit construction,
a class-field formula, or a different subgroup split.

## Generated-Subgroup Tradeoff

The opposite tradeoff is to choose a subgroup that is generated by a small
split prime, and accept a larger recovery degree.  I added:

```text
p24/generated_subgroup_split_tradeoff.py
```

and ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/generated_subgroup_split_tradeoff.py --prime-bound 20000 --show 12
```

Best rows:

```text
ell=2
  K_order=102940198007
  quotient=2
  proxy/sqrt=0.308821

ell=677
  K_order=655670051 = 211 * 3107441
  quotient=314 = 2 * 157
  proxy/sqrt=0.444544

ell=7349
  K_order=487868237 = 157 * 3107441
  quotient=422 = 2 * 211
  proxy/sqrt=3.585832
```

The `ell=677` split is the most interesting generated-subgroup fallback:
it has a small walk generator and quotient degree `314`, and it contains the
target recovery subgroup `H` because its order is `211*n`.

This suggests a tower shape:

```text
G / <677>             degree 314
<677> / H             degree 211
H                     recovery degree 3107441
```

The degrees are excellent.  The obstruction is the same embedded one: a
seedless construction must compute the quotient trace and the relative
degree-211 child relation paired to `j`, not merely know that the abstract
subgroups exist.  This is why the `ell=677` component quotient is useful as a
tower target but not, by itself, a certificate.

## Current Meaning For p24

The complement trace route now has a precise positive shape:

```text
1. prove Res(Phi_3107441,T) != 0 mod p;
2. construct F(Y)=minpoly(Tr_K(j)) of degree 3107441;
3. construct a compressed recovery relation U(Y,J) of degree 66254 in J;
4. choose a root Y0 of F and recover one j root from U(Y0,J);
5. convert j to a Pomerance triple.
```

The finite algebra is sound and tested in toy examples.  The missing theorem
has shifted again:

```text
not only p-unitness of the complement resolvent,
but a sub-h, preferably tower-sized, construction of F and U.
```

This is exactly the embedded class-field tower problem in a sharper form.  An
abstract degree-`3107441` field is not enough; the construction must also give
the degree-`66254` embedded recovery map back to `j`.
