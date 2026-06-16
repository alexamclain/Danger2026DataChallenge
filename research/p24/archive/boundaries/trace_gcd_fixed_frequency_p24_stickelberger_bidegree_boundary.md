# p24 Stickelberger Bidegree Boundary

Date: 2026-06-07

## Point

The current fixed-frequency theorem is the bidegree support statement:

```text
after Tr_{B/C}, the six slots
  C_7^nontrivial x {trivial C/E character}
vanish.
```

This made a Stickelberger/Jacobi-sum proof look tempting.  The finite Fourier
shadow of that proof has a hard necessary shape: any proposed universal
annihilator must have zero Fourier coefficient in the six forbidden bidegrees.

The new gate tests the plain candidates on the exact p24 quotient degrees:

```text
right quotient C_7
C/E quotient C_179
```

## Result

```text
cyclic_stickelberger_forbidden_nonzero=6/6
cyclic_centered_stickelberger_forbidden_nonzero=6/6
right_axis_stickelberger_forbidden_nonzero=6/6
right_axis_centered_stickelberger_forbidden_nonzero=6/6
c_axis_centered_stickelberger_forbidden_nonzero=0/6
centered_product_forbidden_nonzero=0/6
```

So the plain cyclic Stickelberger distribution on `C_(7*179)` leaks in every
forbidden slot, even after subtracting its augmentation.  The plain right-axis
Stickelberger distribution also leaks in every forbidden slot.

The only tested toy distributions that avoid the forbidden bidegrees are
deliberately `C/E`-centered: a pure centered `C` factor, or a product with a
centered `C` factor.  That is not a proof; it is the shape a successful
Jacobi-sum/Stickelberger proof would have to explain from the selected
weighted trace-GCD packet.

## Consequence

Do not use the slogan

```text
Stickelberger/Jacobi sums kill the anchor
```

unless the construction explicitly produces the missing `C/E` centering after
`Tr_{B/C}`.  The generic cyclotomic or right-axis annihilator is not the
missing theorem.

The surviving proof target is sharper:

```text
construct a phase-aware CM/Lang determinant or Jacobi-sum product whose
divisor/support is already C/E-centered in the nontrivial right channels.
```

This aligns the Stickelberger route with the existing bidegree target rather
than replacing it with another broad heuristic.

## Check

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_stickelberger_bidegree_boundary.py
```

The gate runs entirely in a split finite Fourier model over `F_32579`, where
`32579 - 1 = 26 * 7 * 179`; it does not enumerate CM roots or use p24-scale
computation.
