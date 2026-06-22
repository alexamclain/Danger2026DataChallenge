# P27 Kummer Branch-Extraction Handoff

Date: 2026-06-21

## Claim

The K-line route is no longer a coefficient-fitting problem.  The finite-field
screens now say the right next test is to recover the actual branch class or
genus of the `d3` double cover over the Kummer line.

The current reduced coordinate is:

```text
residual E:        W^2 = X^3 - X
2-isogenous E':    V^2 = U^3 + 4U
quotient map:      U = X - 1/X, V = W*(X^2+1)/X^2
Kummer coordinate: K = x([2]P) on E'
```

In residual `X`,

```text
K = (X^2 - 2X - 1)^2*(X^2 + 2X - 1)^2
    / (4*X*(X - 1)*(X + 1)*(X^2 + 1)^2).
```

The new handoff packages this map together with the reverse-source equations
for the `d3` all-plus extraction.

## Artifact

Gate / handoff generator:

```text
research/p27/archive/gates/p27_kummer_branch_extraction_handoff.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kummer_branch_extraction_handoff_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_kummer_branch_extraction_handoff.py \
  > research/p27/archive/probe_outputs/p27_kummer_branch_extraction_handoff_20260621.txt
```

## Decisive Context

Already killed:

```text
degree 1 and 2 K-polynomial characters over q=1471,1607,1847
shared small-integer degree 3/4 K-polynomials with coefficients [-8,8]
split degree <=4 branch divisors from rational linear / irreducible quadratic factors
```

Still live:

```text
irreducible cubic/quartic branch extraction
actual Magma/Sage normalization and genus computation
comparison of d4 only after a stable d3 class is named
```

## Magma / Sage Ask

Use the handoff equations to define the function field or affine scheme over a
guard field, add

```text
K*K_den(X) - K_num(X) = 0
```

as the map to `P^1_K`, normalize the `d3` source cover over `P^1_K`, and
compute:

```text
branch divisor degree
support field degrees
genus
whether the class survives p27-signature fields q=1607, q=1847, and q=2087
```

## Promotion Bar

Promote only if the branch class is stable across guard fields and gives:

```text
genus <= 1, or
a named recurrence/sourceable walk, or
a direct sampler into the d3 all-plus source
```

## Kill Condition

Kill the K-line source route if the recovered branch divisor is high/generic
and `d4` is an unrelated fresh half-cover.

## Continue / Kill

```text
continue = Magma/Sage branch-divisor and genus extraction from the handoff
continue = exact irreducible cubic/quartic branch recovery if it avoids blind fitting
kill = broader coefficient-bound widening
kill = using q1471/q1607-only d4 local fits as recurrence evidence
```

## Linked Artifacts

- Parent: [P27 Kummer Branch-Divisor Screen](p27_kummer_branch_divisor_screen_20260621.md)
- Generator: `research/p27/archive/gates/p27_kummer_branch_extraction_handoff.py`
- Output: `research/p27/archive/probe_outputs/p27_kummer_branch_extraction_handoff_20260621.txt`

```text
p27_kummer_branch_extraction_handoff_rows=1/1
```
