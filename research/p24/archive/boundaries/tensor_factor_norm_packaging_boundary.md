# Tensor Factor Norm Packaging Boundary

This note records what can and cannot be made intrinsic about the one-factor
tensor determinant.

## Coordinate Minor

A one-factor coordinate certificate chooses a flag/projection

```text
P : B_i -> E^368
```

and checks a Pluecker coordinate:

```text
delta_i = det(P(R_s)_{s in S_axis}) != 0.
```

This is a valid finite certificate, but it is not canonical.  Changing the
coordinate flag changes the Pluecker coordinate, including its zero/nonzero
status.

The norm-like package is the Frobenius orbit product

```text
Pi_a = product_{i=0}^{69} delta_i,
```

with compatible flags on the 70 tensor factors.  Squaring removes possible
sign choices.  This is a legitimate finite p-unit package for a chosen
coordinate flag, but it is still a Pluecker-coordinate certificate rather than
a canonical CM invariant.

## Moore Determinant

The one-factor Moore determinant

```text
Delta_i = det(R_s^(Q^j))_{s in S_axis, 0 <= j < 368},
Q = |E|,
```

is intrinsic to the E-vector-space rank problem in `B_i`.  Its nonvanishing is
equivalent to full one-factor axis rank.

A scalar form is:

```text
Norm_{B_i/E}(Delta_i) != 0.
```

This is more natural than an arbitrary coordinate minor, but still lives in a
chosen tensor factor.  Semilinear Frobenius transports the statement to every
factor, as recorded in:

```text
p24/tensor_factor_rank_symmetry.md
```

## Hermitian Pairing

The p24 factor accounting is:

```text
ord_n(p)=388430
ord_m(p)=5460
factor_count=70
factor_degree_over_E=5549
```

I added:

```text
p24/tensor_factor_pairing_accounting.py
```

It reports:

```text
p^(ord_n/2) == -1 mod n
inversion_shift_mod_factor_count=35
factor_degree_parity=1
```

Thus inversion does not act inside one tensor factor.  It pairs

```text
B_i with B_{i+35}.
```

So the Hermitian/trace-Gram object is more intrinsic than coordinate minors,
but it naturally lives on paired tensor factors, not on a single factor.  This
connects the one-factor tensor route back to the earlier Hermitian axis norm
target:

```text
p24/hermitian_axis_packet_norm_theorem.md
```

## Current Boundary

There are now two clean certificate surfaces:

```text
1. One-factor Moore determinant:
   det(R_s^(Q^j)) != 0 in B_i.

2. Paired-factor Hermitian determinant:
   trace/inversion Gram pairing B_i with B_{i+35}.
```

The Moore determinant is the smallest rank certificate.  The Hermitian
determinant is more canonical but uses paired factors.  Neither is currently
proved to be a p-unit for the selected p24 CM embedding.
