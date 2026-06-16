# Hermitian Internal-Character Boundary

This note records a boundary for the preferred Hermitian scalar certificate.

## Question

Could the Hermitian packet scalar be computed from the quotient period vector

```text
y_u = sum_k j_{u+m*k} = J_u(1),
```

or from the quotient period polynomial

```text
prod_u (Y-y_u)?
```

If yes, one might bypass the order-`n` recovery subgroup and work only with
the degree-`m` quotient data.

## Answer

No.  The Hermitian packet scalar depends on

```text
J_u(zeta_n^a),
```

for nontrivial relative characters `a`, not just on `J_u(1)`.

The toy

```text
p24/hermitian_not_quotient_period_invariant_toy.py
```

constructs two datasets over `F_101` with

```text
h=10, m=2, n=5.
```

They have identical quotient periods:

```text
quotient_periods_a=[1,1]
quotient_periods_b=[1,1]
```

but different nontrivial relative fibers and different Hermitian packets:

```text
relative_fibers_a=[1,1]
relative_fibers_b=[1,95]
hermitian_packet_a=96
hermitian_packet_b=88
```

Thus:

```text
same quotient period polynomial does not determine Hermitian packet scalar.
```

## Consequence For p24

The Hermitian scalar is a strong scalar certificate and is the preferred
energy target, but it has not removed the internal `H`-character primitive.
For the third p24 target this internal group has order

```text
n = 3107441.
```

Any proof or construction of the Hermitian packet norm must still access the
nontrivial relative character data inside each quotient fiber, or prove a
selected-prime p-adic unit theorem for the resulting scalar.  The degree-`m`
quotient period polynomial alone is insufficient.
