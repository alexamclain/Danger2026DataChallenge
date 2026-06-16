# Pluecker Trace-Form Boundary

This note checks whether the leading coefficient-minor route can be promoted
into a proof of the Hermitian axis determinant by Cauchy-Binet.

## Setup

Let `V` be the axis coefficient matrix in the packet power basis, and let `B`
be the Hermitian trace form in that same basis:

```text
H_axis = V B V^t.
```

Then

```text
det(H_axis)
  = sum_{|S|=|T|=r} det(V_S) det(B_{S,T}) det(V_T),
```

where `r = dim(W_axis)`.  The leading coefficient-minor theorem controls only
one Pluecker coordinate, `det(V_{0..r-1})`.

I added:

```text
p24/plucker_trace_form_audit.py
```

## Tiny Degenerate Case

For the first composite row,

```text
D=-671, q=2693, h=30, m=6, n=5
factor_degree=4, axis_dim=4
```

there is no room outside the leading coordinate set:

```text
pluecker_nonzero=1
pluecker_total=1
off_diagonal_nonzero_terms=0
leading_term=gram_det=1300
```

Here the leading minor and Hermitian determinant coincide for dimension
reasons only.

## First Extra-Dimension Test

On the targeted multidimensional row:

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
factor_degree=10, axis_dim=6
```

the Cauchy-Binet expansion is dense:

```text
leading_v_det=7618
leading_b_det=531
leading_term=258
diagonal_sum=2008
gram_det=6814
cb_sum=6814

pluecker_nonzero=210
pluecker_total=210
nonzero_b_minors_on_pluecker_support=5250
off_diagonal_nonzero_terms=5040
```

Thus all `C(10,6)=210` Pluecker coordinates of the axis subspace are nonzero,
and thousands of off-diagonal trace-form minors contribute.

## Consequence

The leading coefficient minor is a valid finite rank certificate:

```text
leading Pluecker coordinate nonzero => axis injectivity.
```

But it does not presently prove the Hermitian determinant p-unit theorem.
There is no observed triangular Cauchy-Binet collapse once the packet has
extra coordinate room.

To connect the two routes, one would need a new p-adic filtration/dominance
theorem showing that the dense Pluecker sum cannot cancel modulo the selected
prime.  Small data gives the opposite structural signal: the Hermitian
determinant is a genuinely coupled exterior trace-form value.
