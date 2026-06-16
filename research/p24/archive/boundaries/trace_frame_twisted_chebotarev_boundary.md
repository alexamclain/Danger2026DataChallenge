# Trace-Frame Twisted Chebotarev Boundary

Date: 2026-06-05

This note isolates the exact point where finite Fourier uncertainty almost,
but not quite, proves the trace-frame local-unit theorem.

## Temptation

For the p24 tensor factor:

```text
n = 3107441 is prime
axis support size = 368
bad relative flag size = 28*179 = 5012
368 + 5012 = 5380 << n+1
368 * 5012 = 1844416 < n
```

If the axis characters and the bad flag were an ordinary prime-cyclic Fourier
support pair, Chebotarev/Tao uncertainty would rule out every nonzero
intersection immediately.

That would prove:

```text
W_axis cap F_27 = {0}
```

namely the intrinsic full-top-three avoidance theorem.  The selected
`179+179+10` leading local-unit theorem is stronger: it needs the residual
Schubert-tail condition

```text
K_sel =
  { x in W_axis cap F_28 : pi_10(b_28(x)) = 0 }
  = {0}.
```

So even the untwisted Chebotarev analogy is only a guide to the larger
transversality picture, not a sufficient proof of the actual selected minor.
The selected-vs-full distinction is recorded in:

```text
p24/trace_frame_selected_lead_failure_module.md
```

## The Missing Identification

The actual map is not an untwisted Fourier projection.  After inserting the
embedded CM period sequence, the relevant linear maps have a twisted shape:

```text
F_T * diag(Lambda_CM) * F^{-1}_S
```

or one of its relative/crossed-product variants.  Here:

```text
S = selected smooth-axis character set,
T = selected relative coefficient / Schubert flag coordinates,
Lambda_CM = singular-moduli class-character resolvents.
```

Prime-cyclic Chebotarev controls minors of:

```text
F_T,S
```

and it survives row or column scaling by p-units.  It does not control an
interior diagonal twist by arbitrary nonzero `Lambda_CM`.

## Toy Boundary

I added:

```text
p24/twisted_chebotarev_minor_toy.py
p24/weighted_fourier_cauchy_binet_toy.py
p24/trace_frame_weighted_fourier_expansion.md
```

It works over `F_11` with prime length `5`.  The ordinary Fourier matrix has
no zero `2 x 2` minors, and column-scaled Fourier matrices still have no zero
`2 x 2` minors.  But an invertible interior spectral twist already has a zero
selected minor:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/twisted_chebotarev_minor_toy.py
```

Output:

```text
fourier_zero_2x2_minors=0
column_scaled_fourier_zero_2x2_minors=0
nonzero_spectral_twist=[1, 1, 1, 1, 2]
twisted_zero_rows=[0, 1]
twisted_zero_cols=[2, 3]
twisted_minor_det=0
```

Thus:

```text
all spectral weights nonzero
```

is too weak.  This matches the reduced-normality boundary:

```text
p24/reduced_normality_proof_frontier.md
```

Reduced normality says the class-character resolvents are nonzero.  The
trace-frame theorem needs the stronger selected-minor/nonincidence statement.

The Cauchy-Binet toy makes the failure mechanism sharper.  The same zero
minor has the full expansion:

```text
sum_{U, |U|=2}
  det(F_{T,U}) det((F^-1)_{U,S}) prod_{u in U} lambda_u,
```

with:

```text
cauchy_binet_subset_count=10
zero_coefficient_count=0
nonzero_term_count=10
actual_minor=0
```

So the failure is full-support cancellation, not missing spectral support.

## Productive Theorem Form

The CS import that would genuinely finish the current route is therefore a
weighted Chebotarev theorem for the actual CM twist:

```text
For the p24 singular-moduli twist Lambda_CM, the selected
Schubert/trace-frame minor of F_T * diag(Lambda_CM) * F^{-1}_S is a p-unit.
```

In the existing local-unit notation this is exactly:

```text
for every beta orbit Omega,
  K_sel,Omega =
    { x in W_axis(A_Omega) cap F_28(A_Omega) :
        pi_10(b_28(x)) = 0 }
    = {0};
```

equivalently:

```text
R_lead,Omega is a p-unit,
and D_0 is a p-unit.
```

So the Fourier/CS route has not disappeared.  It has become precise: prove a
CM-weighted Chebotarev minor theorem, not an ordinary uncertainty theorem.

## Consequence For Next Proof Attempts

This boundary rules out the following shortcuts:

```text
prime cyclic uncertainty alone;
nonzero class-character resolvents alone;
ordinary reduced normality alone;
full Cauchy-Binet coefficient support alone;
generic random-rank heuristics.
```

It leaves two viable imported theorem shapes:

```text
1. Hidden block equivalence:
   find p-unit source/target changes that move the CM twist to row/column
   scalings of an LRS/MSRD/Fourier-superregular matrix.

2. Direct weighted minor:
   prove the selected Schubert determinant for the actual singular-moduli
   twist is a p-unit by a class-field norm, divisor, or p-adic identity.
```

The first is the exact strengthened version of the MSRD/LRS route.  The second
is the current determinant-line/local-unit theorem.
