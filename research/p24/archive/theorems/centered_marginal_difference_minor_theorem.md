# Centered Marginal Difference-Minor Theorem Candidate

Date: 2026-06-05

This note records a cleaner sufficient base-field certificate for the p24
mixed Hermitian block.

## Object

Let

```text
M(a,b) = sum_{r == a mod 157, s == b mod 211} K(r,s)
```

be the Hermitian CRT double marginal of the packet autocorrelation kernel.
Define the doubly-centered difference marginal

```text
C(a,b) = M(a,b) - M(a,0) - M(0,b) + M(0,0),
1 <= a < 157, 1 <= b < 211.
```

This is the `156 x 210` base-field matrix whose rank is equivalent to the
centered-profile span theorem.

## New Sufficient Scalar

Define

```text
Delta_C_leading =
  det(C(a,b))_{1 <= a <= 156, 1 <= b <= 156}.
```

Then

```text
Delta_C_leading != 0 mod p
  => rank_Fp C = 156
  => rank_Fp C_{157,211} = 156.
```

This is not the same scalar as `D_profile_leading` from
`p24/centered_profile_trace_gram_basefield_formula.md`.  The older
`D_profile_leading` is equivalent to the Moore determinant of one absolute
centered-profile window.  `Delta_C_leading` instead uses the first `156`
right-difference columns `G_b-G_0`, `1 <= b <= 156`, and proves the mixed
rank directly.

The advantage is that `Delta_C_leading` is just an ordinary visible minor of
the centered marginal already used by the small-CM audits:

```text
rows:    a = 1,...,156
columns: b = 1,...,156
```

No extension-field coordinates, trace pairing, or inversion Gram are needed
to state the arithmetic p-unit target.

## CS Interpretation

Dualizing, `Delta_C_leading != 0` says that the cyclic code

```text
lambda |-> (Tr_{L/Fp}(lambda * (G_b-G_0)))_{b=1}^{210}
```

has no nonzero word vanishing on the first `156` right-difference positions.
In CS language this is a deterministic rank-condenser / superregular
projection theorem for the actual CM marginal generator.

The useful imported theorem shape is therefore:

```text
the p24 centered Hermitian marginal avoids the leading consecutive-minor
divisor modulo p = 10^24+7.
```

Generic random-subspace heuristics predict success, but they are not a
certificate.  The missing step is a class-field or finite-field identity
showing that this selected determinant is a p-unit.

## Exterior Trace-Form Identity

There is an exact Cauchy-Binet form.  If `A` is the coefficient matrix of the
left differences and `R` is the coefficient matrix of the first `156` right
differences in a packet power basis, then:

```text
C_lead = A * B * R^t,
```

where `B` is the Hermitian packet trace-form matrix.  Thus:

```text
Delta_C_leading =
  <L_1 wedge ... wedge L_156,
   R_1 wedge ... wedge R_156>_{wedge B}.
```

This is the current best class-field identity surface: prove that two
explicit decomposable exterior class-field vectors are not orthogonal modulo
`p`.

The boundary audit is:

```text
p24/centered_marginal_cauchy_binet_boundary.md
p24/centered_marginal_cauchy_binet_audit.py
p24/centered_marginal_padic_filtration_boundary.md
p24/centered_marginal_padic_filtration_audit.py
```

Small actual-CM rows show that the natural power-basis Cauchy-Binet expansion
is dense once the packet degree exceeds the window dimension, so this does
not immediately factor into separate left and right leading minors.  The
structured-basis audit further shows that power, Frobenius normal, and
middle-Frobenius bases do not collapse the Pluecker support in the hard row.
Hermitian orthogonal bases reduce the expansion to a single diagonal Pluecker
dot product `sum_S u_S v_S`, but all matched Pluecker coordinates remain
nonzero in the nondegenerate small rows.

## Origin-Stable Product

The Hermitian origin action gives a useful package for the selected minor.  If

```text
shift == n*alpha + m*beta mod h,
```

then the packet monomial shift `beta` cancels in the Hermitian pairing, while
`alpha` translates the CRT-axis residues.  Therefore define:

```text
Pi_C = prod_{alpha mod m} Delta_C(alpha).
```

If `Pi_C` is a p-unit, the selected origin's `Delta_C_leading` is a p-unit.
This is recorded in:

```text
p24/centered_marginal_origin_product_theorem.md
p24/centered_marginal_origin_product_audit.py
```

Small actual-CM rows verified exact beta invariance and nonzero alpha
products in the dimension-eligible cases tested.

For p24, the left component is the odd prime `157`, so the left translation
determinant is always `+1`.  Consequently the `66254`-factor alpha product
collapses to the `314`th power of a 211-factor right-translation product:

```text
Pi_C = (prod_{t mod 211} F(t))^314.
```

The compact p24 target is therefore the p-unitness of the 211 cyclic right
translates of the leading `156 x 156` difference minor.

## Actual-CM Leading-Minor Audit

Added:

```text
p24/centered_marginal_leading_minor_audit.py
```

It computes ranks and leading determinants of the centered marginal `C` on
bounded actual-CM rows.  The first checks were:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py \
  --only-D -13319 --max-rows 8 --max-cases 1 --max-h 200 \
  --max-abs-D 14000 --max-composite-quotients 20 \
  --max-axis-dim 50 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py \
  --only-D -6719 --max-rows 8 --max-cases 1 --max-h 200 \
  --max-abs-D 8000 --max-composite-quotients 20 \
  --max-axis-dim 50 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py \
  --only-D -10919 --max-rows 8 --max-cases 1 --max-h 200 \
  --max-abs-D 12000 --max-composite-quotients 20 \
  --max-axis-dim 50 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear
```

The summaries were:

```text
D=-13319: full_rank_applicable_pairs=9,
          leading_full_pairs=9,
          full_rank_but_leading_zero_pairs=0.

D=-6719:  full_rank_applicable_pairs=12,
          leading_full_pairs=12,
          full_rank_but_leading_zero_pairs=0.

D=-10919: full_rank_applicable_pairs=12,
          leading_full_pairs=12,
          full_rank_but_leading_zero_pairs=0.
```

Origin shifts `1` and `2` for `D=-13319`, and shift `1` for `D=-6719`,
preserved:

```text
full_rank_but_leading_zero_pairs=0.
```

This supports the leading-difference minor as a stable theorem candidate.  It
does not prove p24, because small-row success is consistent with generic
random-subspace behavior.

## Current p24 Target

The sharpened sufficient arithmetic theorem is:

```text
For p = 10^24+7, the determinant Delta_C_leading of the actual
156 x 156 leading right-difference minor of the centered Hermitian
157 x 211 marginal is nonzero modulo p.
```

If proved, this gives the needed mixed Schur rank with sub-sqrt verification
cost: the verifier checks one finite determinant certificate instead of
enumerating the class set or running a sqrt(p) Montgomery search.
