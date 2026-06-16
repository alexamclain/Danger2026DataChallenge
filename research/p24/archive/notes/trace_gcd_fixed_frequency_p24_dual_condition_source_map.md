# p24 Dual Fourier Condition Source Map

Date: 2026-06-07

## Point

The current admissible Jacobi target is the four-family Fourier system on
`C_7 x C_179`.  This note maps each family to possible arithmetic sources and
known failed shortcuts, so the next proof attempt does not rediscover old
false implications.

Write the post-`Tr_{B/C}` Fourier coefficients as:

```text
F(a,b),  a in C_7, b in C_179.
```

## Family 1: Forbidden C/E-Trivial Vanishing

Equation:

```text
F(a,0) = 0,  a = 1,...,6.
```

Meaning:

```text
no C_7^nontrivial x {C/E trivial} bidegrees.
```

This is equivalent to final internal trace zero in the nontrivial right
projector channels.

Known trap:

```text
trace-defect anchor zero does not imply this.
```

The anchor-vs-`C/E`-centering boundary constructs exact quotient models where
the anchor passes and this bidegree still leaks, and conversely.

Likely source:

```text
direct C/E-centering of the selected weighted obstruction after Tr_{B/C},
or an affine profile theorem tying that centering to the selected child.
```

Jacobi-carry source:

```text
For an admissible C-axis carry, u=7*s has no right-nontrivial support, and
the v and u+v sawtooth terms have the same right component when b=0, so
their Fourier coefficients cancel.
```

## Family 2: Nontrivial-Right Conjugate Skew

Equation:

```text
F(a,b) + F(-a,-b) = 0,
  a != 0, b up to conjugate C/E pairs.
```

This is the most visible conjugate-pair compatibility condition.

Known trap:

```text
ordinary inversion/Hermitian packet stability only pairs terms;
it does not cancel them.
```

The packet-inversion boundary shows that if paired multipliers satisfy

```text
L_{-a} = alpha_a L_a,
R_a    = beta_a R_{-a},
```

then cancellation requires the extra sign

```text
alpha_a * beta_a = -1.
```

If the product is `+1`, the paired contribution doubles.  Therefore a proof
of this family needs an actual anti-invariance sign, termwise right-combo
vanishing, or a genuine selected-packet cancellation.

Likely source:

```text
Gauss-normalized anti-Hermitian CM/Lang involution on the selected weighted
packet, not bare inversion symmetry.
```

Jacobi-carry source:

```text
For one sawtooth term, hat g_m(k)+hat g_m(-k)=-d*N.  In an admissible carry,
the right-nontrivial slice is the difference of the v and u+v terms with the
same divisor d, so these constants cancel and give true conjugate skew.
```

## Family 3: Right-Trivial Pair-Sum Normalization

Equation:

```text
F(0,b) + F(0,-b) = lambda_179 * F(0,0).
```

The scalar depends on the Fourier-root normalization.

For admissible C-axis carries the scalar is explicit:

```text
lambda_c = -2/(c-1).
```

For p24:

```text
lambda_179 = -2/178 = -1/89.
```

Known trap:

```text
ordinary centering controls only the trivial right quotient profile;
it does not determine all right-trivial C/E conjugate pair sums.
```

Likely source:

```text
degree/augmentation normalization of the C-axis Jacobi-carry divisor, or a
principal-divisor/product-formula identity after Tr_{B/C}.
```

This family is a good place to look for a clean class-field/Jacobi-sum
normalization constant, because it is the only family involving `F(0,0)`.

## Family 4: Three Global Pair Balances

Equations:

```text
sum_{b>0}(F(-a,b) - F(a,b)) = 0,
  a = 1,2,3.
```

These are the terminal compatibility equations in the spectral fingerprint:
after `88` conjugate C/E pairs each add a full right rank `7`, the final pair
adds rank `4` rather than `7`.

Known trap:

```text
pairwise conjugate skew by itself is not enough to identify the admissible
Jacobi-carry span.
```

Likely source:

```text
a global residue/product-formula relation among the C-axis Jacobi carries,
or the same relation seen through the right-difference trace telescope.
```

Jacobi-carry source:

```text
Every admissible carry vanishes on the C-zero fiber.  Fourier inversion along
the C coordinate gives sum_b F(a,b)=0; using the conjugate-pair skew, this is
equivalent to the three independent global balances.
```

This is the most plausible place for the right-difference route to compose
with the admissible-Jacobi route.

## Proof Architecture To Try Next

The current clean theorem can be attacked dually:

```text
prove Families 1-4 directly for the selected weighted packet after Tr_{B/C}.
```

Or constructively:

```text
write the packet as an admissible C-axis Jacobi-carry combination.
```

The dual route is currently more testable.  A useful next computation should
materialize a faithful selected weighted analogue and report the four family
residuals separately:

```text
family1_forbidden_residuals
family2_conjugate_skew_residuals
family3_pair_sum_residuals
family4_global_balance_residuals
```

This avoids another support-only test.  Positive evidence is only useful if
it explains which family is being supplied by which arithmetic identity.

## Current Honest Status

The finite plumbing is now strong:

```text
four families => admissible span => verifier pipeline.
```

The missing theorem is still arithmetic:

```text
why does the selected weighted trace-GCD packet satisfy Families 1-4?
```

Generic CM rows, generic inversion symmetry, left pairing, covariance, and
anchor zero have all failed as standalone explanations.

The Jacobi-carry Fourier formula gate now proves:

```text
admissible C-axis Jacobi carries satisfy Families 1-4 symbolically.
```

So the preferred arithmetic theorem is even sharper:

```text
construct the selected weighted packet as a p-integral combination of
admissible C-axis Jacobi carries, or prove that the selected packet obeys the
same sawtooth identities directly.
```
