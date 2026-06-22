# P27 Lambda Rational-Quotient Obstruction

Date: 2026-06-21

## Claim

The Belyi coordinate

```text
lambda = -K^2/4
```

is useful as an algebraic normalization, but it is not a rational source
quotient in the p27 sign regime.

Reason: on

```text
E': V^2 = U^3 + 4U
```

the Kummer coordinate is

```text
K = x([2]P) = (U^2 - 4)^2 / (4U(U^2+4))
            = ((U^2 - 4)/(2V))^2.
```

Thus every nondegenerate rational doubled `K` is a square.  Since p27 and all
compatible guard fields have `q mod 8 = 7`, `chi(-1)=-1`, so `-K` is a
nonsquare whenever `K` is a nonzero square.  The quotient `K ~ -K` leaves the
rational doubled stratum.

## Probe

Gate:

```text
research/p27/archive/gates/p27_lambda_rational_quotient_obstruction_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_lambda_rational_quotient_obstruction_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_lambda_rational_quotient_obstruction_probe.py \
  | tee research/p27/archive/probe_outputs/p27_lambda_rational_quotient_obstruction_probe_20260621.txt
```

## Symbolic Identity

The probe verifies:

```text
K = (U - 2)^2*(U + 2)^2/(4*U*(U^2 + 4))
K_square_form = (U - 2)^2*(U + 2)^2/(4*V^2)
difference_after_Eprime_relation = 0
```

So, away from branch points, `K` is visibly square for rational doubles.

## Guard-Field Evidence

The checked fields were:

```text
607, 863, 991, 1471, 1607, 1847,
1951, 1999, 2039, 2063, 2087, 2111, 2143, 2207, 2239
```

All have:

```text
q mod 8 = 7
chi(-1) = -1
chi(2) = +1
```

For the full doubled image on `E'`, every nonzero doubled `K` stayed in the
square stratum, and there were no nonzero `K/-K` paired doubled values:

```text
neg_nonzero_k_also_doubled = 0
```

for every guard field.  The only exceptional value is the branch value `K=0`.

For selected source rows, the same obstruction is exact:

```text
q=1471: d3 K rows 50, d3_k_plus=50, d3_neg_k_present=0
q=1607: d3 K rows 49, d3_k_plus=49, d3_neg_k_present=0
q=1847: d3 K rows 63, d3_k_plus=63, d3_neg_k_present=0
```

and similarly for `d4`.  The broader guard-field set has the same pattern.

## Interpretation

Positive:

```text
The K-square identity explains why the visible branch atoms K and K^2+4 were
already square on all selected rows.
```

Negative:

```text
lambda=-K^2/4 is not a rational p27 source quotient.
A lambda-line branch class cannot by itself become a GPU sampler over F_p.
```

The lambda coordinate can still help a symbolic branch-class computation over
the algebraic closure, but any useful p27 source must lift back to the
rational `K` square stratum.

Follow-up:
[P27 Lambda Monomial Recurrence Screen](p27_lambda_monomial_recurrence_screen_20260622.md)
tests the canonical Belyi dynamics on this normalized line,
`lambda -> lambda^m` with S3 conjugation, for `m=2..12`.  It finds no exact
`d3/d4` recurrence in q1471/q1607/q1847, so lambda remains a normalization
coordinate rather than a recurrence/source shortcut.

## Next Test

Use `lambda` only as a normalization aid.  The live source question is:

```text
recover the actual branch class over K, with the doubled-image square stratum
remembered.
```

Promotion bar:

```text
a K-level branch class or recurrence that sources d3 inside the rational
doubled image, not merely a lambda-level class modulo K -> -K.
```

Kill condition:

```text
the recovered K-level branch class is high/generic and d4 is an unrelated
fresh half-cover.
```

## Continue / Kill

```text
continue = K-level branch-class/genus extraction with K square stratum explicit
continue = use lambda only to mark Belyi branch values 0,1,infinity
kill = lambda as a standalone rational sampler/source quotient for p27
kill = GPU sampler from lambda without a K-square lift
```

## Linked Artifacts

- Parent: [P27 Kummer Belyi Structure Probe](p27_kummer_belyi_structure_probe_20260621.md)
- Related: [P27 Lambda Branch-Divisor Screen](p27_lambda_branch_divisor_screen_20260621.md)
- Probe: `research/p27/archive/gates/p27_lambda_rational_quotient_obstruction_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_lambda_rational_quotient_obstruction_probe_20260621.txt`

```text
p27_lambda_rational_quotient_obstruction_rows=1/1
```
