# Hermitian Axis Autocorrelation Formula

This note makes the Hermitian axis determinant explicit in quotient
autocorrelation terms.

## Formula

For an axis basis function `w_i in W_axis`, define

```text
Y_i(X) = sum_k (sum_r w_i(r) j_{n*r + m*k}) X^k.
```

For a packet factor `f_a | Phi_n`, the Hermitian Gram entry is

```text
H_a(i,j)
  = Tr_{F_p[X]/(f_a)/F_p}(Y_i(X) * Y_j(X^{-1})).
```

This agrees with the middle-Frobenius definition because in the p24 packet

```text
X^(p^(d/2)) = X^-1
```

on primitive `n`th roots.

Thus the determinant is a phase-aware matrix of packet traces of explicit
axis autocorrelation polynomials.

## Verification

I added:

```text
p24/hermitian_axis_autocorrelation_formula.py
```

Default row:

```text
D=-5000
q=1259
h=30
m=2
n=15
factor_degree=2
axis_dim=2
formula_equal=1
```

Composite row:

```text
D=-1431
q=1447
h=30
m=6
n=5
factor_degree=4
axis_dim=4
formula_equal=1
```

Both direct Hermitian middle-Frobenius Gram and the autocorrelation formula
gave the same matrix rank.

## Proof Relevance

This formula is the concrete object a p-adic/divisor proof would have to
control.  It separates three layers:

```text
axis construction:
  build Y_i from the CRT axis sums of CM roots;

packet trace:
  apply Tr over the selected H-character packet to Y_i(X)Y_j(X^-1);

packet norm:
  take the determinant and multiply over the eight p24 packets.
```

The formula also explains the origin-invariance theorem: shifting the origin
multiplies every `Y_i` by a common monomial and translates the axis basis; the
autocorrelation `Y_i(X)Y_j(X^-1)` cancels the monomial.

The remaining theorem is:

```text
p does not divide the degree-8 norm of det(Tr_packet(Y_i Y_j^*)).
```

Known symmetric difference-norm and class-polynomial discriminant formulas do
not directly compute this matrix-valued non-genus autocorrelation determinant.
They would need a phase-aware refinement that keeps the order-`3107441`
packet data.
