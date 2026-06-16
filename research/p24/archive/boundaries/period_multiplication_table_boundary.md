# Period Multiplication-Table Boundary

This note tests a tempting Gaussian-period analogue for the embedded quotient
tower.

## Question

For classical Gaussian periods, the multiplication constants are cyclotomic
numbers with strong combinatorial structure.  If CM quotient periods had a
similarly sparse multiplication table, one might compute the unordered child
polynomial without explicitly computing all high-order class-character traces.

The diagnostic in

```text
p24/period_multiplication_table_scan.py
```

works in the split finite-field algebra.  For a quotient-period vector

```text
y = (y_0, ..., y_{m-1}),
```

use the cyclic shifts of `y` as a normal-basis candidate and solve

```text
shift_i(y) * shift_j(y) = sum_k c_{i,j,k} shift_k(y)
```

coordinatewise in `F_q^m`.

## Result

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/period_multiplication_table_scan.py --random-controls 20
```

Output:

```text
D=-5000 quotient=6:
  rank=6, avg_support=6.000, random_avg=6.000, distinct_rows=21

D=-5000 quotient=10:
  rank=10, avg_support=10.000, random_avg=9.985, distinct_rows=55

D=-2239 quotient=5 full-cycle:
  rank=5, avg_support=5.000, random_avg=5.000, distinct_rows=15

D=-2239 quotient=7 full-cycle:
  rank=7, avg_support=7.000, random_avg=6.986, distinct_rows=28

D=-2239 quotient=5 components:
  rank=5, avg_support=5.000, random_avg=5.000, distinct_rows=15
```

The support is dense and indistinguishable from random normal-basis data.
The distinct-row counts are the commutative maximum `m(m+1)/2`.

## Interpretation

No sparse Gaussian-period multiplication table is visible in these CM quotient
periods.  Multiplication-table access is essentially access to the embedded
period algebra itself; it does not compute the quotient polynomial from a
small set of universal cyclotomic numbers.

This does not rule out all trace formulas.  It rules out the simple route:

```text
CM quotient periods behave like classical Gaussian periods with cheap
combinatorial multiplication constants.
```

For p24, the first odd `157` layer still needs either the high-order
non-genus class-character traces or another explicit embedded relation.
