# Punctured Hasse-Davenport Jacobi Theorem Candidate

Date: 2026-06-07

## Point

The literal finite-field Jacobi route now has a precise theorem statement.
This is the theorem whose p24 CM/Lang analogue should be sought.

## Reduced Jacobi Packet

Let:

```text
N = 7*c
q = 1 mod N
chi : F_q^* -> mu_N
```

and extend characters by `chi(0)=0`.  For characters `A,B`, write:

```text
J(A,B) = sum_x A(x)B(1-x).
```

Use the reduced degenerate convention:

```text
Jdagger(1,1) = J(1,1)/(q-2) = 1,
Jdagger(A,B) = J(A,B) otherwise.
```

Let `t(r,k)` be the CRT representative of `(r,k) in C_7 x C_c`.  Take:

```text
u = 7*s,  s != 0 mod c,
v right-mixed,
v nontrivial on C_c,
u+v nontrivial on C_c,
u+v != 0 mod N.
```

Define:

```text
U(r,k) = Jdagger(chi^(u*t(r,k)), chi^(v*t(r,k))).
```

## Finite-Field Theorem

The expected Hasse-Davenport theorem is:

```text
U(r,0)U(-r,0) = 1,
U(r,k)U(-r,-k) = q      for k != 0,
prod_k U(r,k) / U(r,0)^c = beta(u,v,c),
```

where `beta(u,v,c)` is independent of the right row `r`.

Thus the reduced Jacobi packet satisfies the full multiplicative producer
target:

```text
constant pair-products + constant selected row-product ratio.
```

## Proof Skeleton

The pair-product identities are direct from the standard Gauss-sum identities:

```text
J(A,B) = G(A)G(B)/G(AB),       A,B,AB nontrivial
G(A)G(A^{-1}) = A(-1)q.
```

For `k != 0`, admissibility makes all involved characters nontrivial, so:

```text
J(A,B)J(A^{-1},B^{-1}) = q.
```

On the `k=0` fiber, `u*t(r,0)=0`.  If `r != 0`, then:

```text
J(1,lambda) = -1
```

for a nontrivial right character `lambda`, so the pair-product is `1`.  If
`r=0`, the uncorrected value is:

```text
J(1,1)=q-2.
```

The reduced convention changes only this single value to `1`, so the
right-zero C-zero pair-product also becomes `1`.

For the row-product ratio, write `A_k=chi^(u*t(r,k))` and
`B_k=chi^(v*t(r,k))`.  For `r != 0`, `B_k` and `A_kB_k` run through two
cosets of the same `C_c` character subgroup with the same nonzero right
component.  Hasse-Davenport collapses:

```text
prod_k G(A_k),  prod_k G(B_k),  prod_k G(A_kB_k)
```

to a right-row-independent ratio after dividing by `U(r,0)^c`.

For `r=0`, the same collapse has exactly the degenerate `J(1,1)=q-2` anchor.
Replacing it by `Jdagger(1,1)=1` multiplies the right-zero selected row ratio
by:

```text
(q-2)^(c-1),
```

which is the inverse of the mined defect:

```text
delta_c = (q-2)^(-(c-1)).
```

Therefore the reduced packet has the same row ratio at `r=0` as on the six
nonzero right rows.

## Exhaustive Small Checks

The exact gate:

```text
p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py
```

checks all right-mixed admissible pairs in the first three small rows:

```text
c=5:  72 pairs
c=11: 540 pairs
c=13: 792 pairs
```

Observed:

```text
corrected_pair_product_rows=3/3
corrected_row_ratio_rows=3/3
corrected_product_formula_rows=3/3
anchor_scale_formula_rows=3/3
```

No p24 class-set enumeration is used.

The symbolic gate:

```text
p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py
```

checks the residue/Gauss-factor cancellation directly for
`c=5,11,13,17,19,179`; for p24 it covers all `189036` right-mixed admissible
pairs and reports `symbolic_producer_rows=6/6`.

The reduced-anchor fingerprint gate:

```text
p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.py
```

records the additive footprint of the single anchor in selected-defect
coordinates.  For p24 it is the punctured right-zero row with `178` nonzero
entries and Fourier profile `H(a,0)=178`, `H(a,b)=-1` for `b != 0`.

## p24 Lift Obligation

The p24 theorem should now be sought in this form:

```text
selected weighted trace-GCD packet after Tr_{B/C}
  = p-integral divisor/log/specialization of a reduced Jacobi/CM-Lang packet;

the selected right-zero anchor supplies the analogue of J(1,1)/(q-2);

Hasse-Davenport/distribution along C/E degree 179 supplies the punctured
row-product theorem.
```

If this lift is proved, then the existing finite gates give:

```text
reduced product formula
  => selected-defect value identities
  => rank-621 admissible Jacobi span
  => forbidden bidegree zero
  => internal trace zero
  => product coboundary
  => 1092 H-coset verifier
  => sub-sqrt certificate surface.
```

The remaining unknown is the actual p24 CM/Lang producer of the reduced
degenerate anchor.  Generic CM packets have already failed the relevant
boundary tests, so this producer must use the selected trace-GCD weighting or
an explicit principal divisor/unit.
