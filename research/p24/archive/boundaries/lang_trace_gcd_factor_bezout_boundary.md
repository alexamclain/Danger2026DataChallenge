# Lang Trace-GCD Factor-Bezout Boundary

Date: 2026-06-05

## Purpose

The orbit-norm frontier can be packaged in two nearby ways:

```text
small norm payload:
  Pi_O = prod_{t in O} Delta(t), plus inverse;

factorwise Bezout payload:
  actual descended/twisted residue in the correct orbit algebra,
  plus inverse residue.
```

The first is smaller.  The second is closer to an explicit algebra element if
the arithmetic producer naturally constructs such a residue.  Both require
honesty: the supplied object must be tied to the actual trace-GCD determinant
section.

## Audit

Added:

```text
p24/lang_trace_gcd_factor_bezout_audit.py
p24/lean/TraceGcdCyclicFactorGate.lean
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_factor_bezout_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140
```

Small actual-CM row:

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7
q mod 7 = 2
factor degrees of Y^7-1 over F_q: [1,3,3]
Frobenius orbits: [0], [1,2,4], [3,6,5]
```

For both omitted rows:

```text
right_mismatches=0
frobenius_compatibility_mismatches=6/7
split_interpolation_eval_mismatches=0
base_polynomial_possible=0
base_factor_residue_possible_by_orbit=[1,0,0]
ordinary_base_factor_residues_possible=0
orbit_products_nonzero=1
product_matches_orbit_products=1
```

The split-field DFT interpolant exists and evaluates correctly, but it does
not have base-field coefficients:

```text
omitted=0:
  split_interpolant_base_coefficients=4/7
  nonbase positions=[3,5,6]

omitted=1:
  split_interpolant_base_coefficients=4/7
  nonbase positions=[1,2,4]
```

## Consequence

This concretely rules out the unsafe shortcut:

```text
take the printed F_q determinant values,
interpolate a polynomial in F_q[Y],
then check gcd with Y^d-1.
```

The values are not Frobenius-compatible, so the honest split interpolant lives
outside `F_q[Y]`.

It also rules out the only-slightly-less-naive factor shortcut:

```text
for each orbit O, take a residue in F_q[Y]/Phi_O(Y)
whose evaluations are the printed base-field values on O.
```

If an ordinary base residue produced base-field values on a Frobenius orbit,
those values would be Frobenius-compatible.  Since the values already lie in
`F_q`, this would force them to be equal along the orbit.  The pinned row
fails that condition on every nontrivial orbit.

For p24 the verifier/producer must use either:

```text
1. pointwise values with inverses;
2. split/twisted factor residues with Bezout/unit witnesses in the actual
   descended orbit algebra, not raw F_p[Y]/Phi_O residues;
3. orbit norm scalars, plus an arithmetic theorem proving they are actual
   norms of the actual determinant section.
```

## Payload Accounting

For the small right-7 row:

```text
norm scalar payload = 2 * 3 = 6 field elements;
factor residue + inverse coefficients = 2 * 7 = 14 field coefficients.
```

For p24:

```text
right = 211,
orbit/factor degrees = 1 + 6*35,
norm scalar payload = 2 * 7 = 14 field elements;
raw split value + inverse payload = 2 * 211 = 422 field elements.
```

Thus raw split values or explicit split residues are safe but not smaller than
pointwise values at the finite payload level.  Ordinary base factor residues
are not valid for the raw determinant sequence.  The asymptotically best
surface is still the seven orbit norms, provided the producer theorem proves
soundness.

## Lean Gate

`p24/lean/TraceGcdCyclicFactorGate.lean` records the abstract finite
implication:

```text
actual factor residue has a unit/Bezout witness
+ any zero Delta(t) would make its factor residue nonunit
=> every Delta(t) is nonzero.
```

The second premise is exactly the arithmetic honesty theorem.  The Lean gate
prevents replacing it with an unrelated unit in the same quotient factor.
This gate does not assert that the quotient is the ordinary base algebra
`F_p[Y]/Phi_O`; the audit shows that assertion would be false for the raw
printed determinant values.
