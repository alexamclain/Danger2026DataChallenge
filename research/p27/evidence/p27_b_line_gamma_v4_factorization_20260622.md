# P27 B-Line Gamma V4 Factorization

Date: 2026-06-22

## Claim

The staged B-line gamma transition has a genuine V4-style algebraic
factorization, but it does not yet give a source sampler.  It explains the
gamma class as a product of two sheet-dependent half-norm phases.

With

```text
A = B^2 - 2
H^2 = u + 2
Y = v + 2
```

the transition `F_A(u,v)=0` becomes the quartic:

```text
P(Y) =
Y^4
- 4*H^2*Y^3
+ (-4*B^2*H^2 + 8*B^2 + 32*H^2 - 32)*Y^2
+ 16*H^2*(B^2 - 4)*Y
+ 16*(B^2 - 4)^2.
```

Its discriminant is a square:

```text
Disc_Y(P) =
[256*B^2*H^2*(B^2 - 4)*(H^2 - 4)*(B^2 + H^2 - 4)]^2.
```

Its cubic resolvent splits:

```text
(z + 8*B^2 - 32)
*(z - 8*B^2 - 16*H^2 + 32)
*(z + 4*B^2*H^2 - 8*B^2 - 16*H^2 + 32).
```

After adjoining

```text
R^2 = H^2 - 4
S^2 = B^2 + H^2 - 4,
```

the four roots of `P(Y)` are:

```text
Y = (H +/- R)*(H +/- S).
```

So the gamma squareclass decomposes as:

```text
chi(v+2) = chi(H + R) * chi(H + S)
```

for either choice of the `R` and `S` signs.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_gamma_v4_factor_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_v4_factor_probe_20260622.txt
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_gamma_class_handoff_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_v4_factor_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_v4_factor_probe_20260622.txt
```

## Guard-Field Results

The V4 root formula has zero failures:

```text
q1607: v4_roots_mismatch=0, alpha_beta_product_not_f4=0
q1847: v4_roots_mismatch=0, alpha_beta_product_not_f4=0
q2087: v4_roots_mismatch=0, alpha_beta_product_not_f4=0
```

The two component characters are sign-invariant in `R` and `S`, but they are
not invariant under the `H -> -H` sheet:

```text
q1607: Bu_alpha_flips=112, Bu_beta_flips=112, Bu_product_H_invariant=112
q1847: Bu_alpha_flips=180, Bu_beta_flips=180, Bu_product_H_invariant=180
q2087: Bu_alpha_flips=100, Bu_beta_flips=100, Bu_product_H_invariant=100
```

For every active B row, the product is constant while the two factors are
mixed:

```text
q1607: B_product_constant=28, B_alpha_mixed=28, B_beta_mixed=28
q1847: B_product_constant=45, B_alpha_mixed=45, B_beta_mixed=45
q2087: B_product_constant=25, B_alpha_mixed=25, B_beta_mixed=25
```

The boundary condition needed for `beta` sign-independence also holds:

```text
four_minus_B2_not_square=0
```

## Interpretation

Positive:

```text
The gamma class is not an opaque quartic anymore.
It decomposes into two explicit half-norm phases alpha=chi(H+R) and beta=chi(H+S).
The product alpha*beta is the canonical f4 bit and is constant on each active B row.
```

Negative:

```text
alpha and beta are not separately canonical on the f3/H90 base.
Both flip under H -> -H, while only alpha*beta is H-invariant.
No direct B/H/tau bucket or one-factor sampler follows from this factorization.
```

This explains why the earlier H90 quotient collapsed to the f3 layer: the
missing information is not the quotient `H^2=u+2` itself, but the coupled
sheet-dependent phase product.

## Concrete Next Test

The next meaningful GPU/CAS telemetry is not another B bucket.  It should emit
the phase sequence across successive selected gates:

```text
alpha_j = chi(H_j + R_j),  R_j^2 = H_j^2 - 4
beta_j  = chi(H_j + S_j),  S_j^2 = B^2 + H_j^2 - 4
f_{j+1} = alpha_j * beta_j
```

Promote only if the phase sequence has a recurrence, telescoping product,
sourceable sheet choice, or direct sampler that controls multiple selected
gates with raw-source accounting.  Kill this route if successive
`alpha_j/beta_j` pairs remain fresh sheet-dependent phases with geometric
half-loss.

## Continue / Kill

```text
continue = CAS compare alpha/beta phase classes across f4/f5
continue = bounded GPU telemetry emitting alpha_j,beta_j,f_j with raw source denominator
continue = look for telescoping or sheet-choice recurrence, not a one-factor bucket

kill = using alpha alone as a canonical selector
kill = using beta alone as a canonical selector
kill = treating the V4 factorization itself as a below-sqrt sampler
kill = more B/H/tau coordinate scans without phase-sequence data
```

```text
p27_b_line_gamma_v4_factorization_rows=1/1
```
