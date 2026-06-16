# Gaussian-Period Followup For Degree 157

Question: can the unordered degree-157 child polynomial in the smooth
third-trace class tower be computed by a Gaussian-period/cyclotomic-period
analogue, without computing the high-order class-character traces?

## Short Answer

No existing analogue in the inspected notes avoids the high-order traces.  The
closest formal candidate is:

```text
compute the relative power sums
  P_d(Z) = sum_{r=0}^{156} y_{a+2r}^d,       1 <= d <= 157,
over a genus parent Z, then use Newton identities to recover F_157(Z,Y).
```

But the moment and correlation toys show that these `P_d` are exactly the
order-157 subgroup idempotent in another basis.  They are not determined by
genus/trivial data or by ordinary global Hecke/correlation traces unless a new
theorem supplies the same high-order projection by other means.

## Why The Gaussian Analogy Breaks

For classical Gaussian periods, multiplication has a special combinatorial
closure:

```text
eta_i eta_j = sum_k cyclotomic_number(i,j,k) eta_k + constant.
```

The constants come from additive relations among multiplicative cosets in a
finite field.  They are structural counts, not measurements of a specific
embedded class-field generator.

For CM class periods,

```text
y_r = sum_{h in H} j_{r+h},
```

there is no analogous universal rule expressing `y_i y_j` as a known
integer-linear combination of the same `y_k` using only the class group.  The
class group acts by Galois conjugation on the `j`-values; multiplication of
the numerical values `j_a j_b` is field multiplication, not the class-group
law.  So a "CM cyclotomic-number" multiplication table would have to know
extra embedded information about the `j`-vector.  That is already the missing
period data.

## What The Inspected Files Show

`class_character_period_reframing.md` gives the exact Fourier identity:

```text
y_r = (1/m) sum_s zeta_m^(-sr) T_s,
T_s = sum_i zeta_m^(si) j_i.
```

Thus the unordered child polynomial is easy once the quotient-character
twisted traces are known.  The obstruction is computing the non-genus
order-157 or order-211 traces sublinearly.

`degree157_refinement_target.md` sharpens this to the first odd layer:
construct, over each genus parent `Z`, the degree-157 polynomial whose roots
are the embedded child periods.  This intentionally avoids choosing a child;
it still requires the order-157 relative phase.

`period_moment_idempotent_toy.py` verifies:

```text
P_d = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}.
```

I reran the toy.  It reports:

```text
convolution_formula_matches=1
newton_reconstructs_true_period_polynomial=1
genus_polynomial_equals_true=0
```

So moments do recover the unordered polynomial, but only after the same
high-order character data has entered through convolution.

`period_correlation_idempotent_toy.py` verifies the Hecke/correlation version:

```text
sum_r y_r^2 = sum_{d in H} C(d),
DFT(autocorrelation)(s) = T_s T_{-s}.
```

I reran it.  It reports:

```text
square_sum_equals_projected_autocorrelation=1
autocorrelation_spectrum_matches_trace_products=1
nonzero_spectral_components=10
period_autocorrelation_bm_complexity=10
```

So correlation/Hecke bookkeeping has full quotient spectrum in the toy; it
does not collapse to low-order data.

`siegel_unit_split_cycle_theorem_attempt.md` supplies the embedded geometric
shape: split-prime cycles give the right quotient objects, and whole-cycle
symmetric sums are the correct invariants.  But the construction still needs
either an embedded CM vertex/cycle or a way to form the quotient polynomial
without enumerating the roots of the class polynomial.

## Sharp Obstruction

The obstruction is not Fourier inversion, not unorderedness, and not the
degree 157 itself.  The obstruction is:

```text
apply the order-157 subgroup idempotent to the embedded j-vector without
enumerating the class orbit or computing the order-157 class-character traces.
```

Multiplication, moments, autocorrelation, and Hecke traces all become useful
after this projection is available.  In the current evidence they do not
provide the projection.

## Viable Theorem Candidate, If Any

The only plausible theorem candidate left is a genuinely new relative trace
formula:

```text
For the p24 third-trace CM order and the degree-157 layer over the genus
parent, compute all relative power sums
  Tr_{K_314/K_2}(Y^d | Z), 1 <= d <= 157,
or equivalently the degree-157 child polynomial F_157(Z,Y),
from D_K, p, Z, and low-degree modular/Hecke data in o(sqrt(p)) work,
without first constructing H_D or the order-157 twisted traces.
```

This would be a true Gaussian-period analogue for CM class periods.  The
inspected notes provide no mechanism for it.  In particular, a theorem that
only gives abstract class-field multiplication, global norms, genus traces,
or ordinary Hecke correlations is not enough; it must retain the embedded
relative phase of the `j`-torsor over the degree-157 layer.

Conclusion: the unordered degree-157 child polynomial is the right relaxed
target, but the Gaussian/cyclotomic-period analogy currently hits the same
high-order idempotent wall.  The sharp obstruction is absence of a universal
CM period multiplication law whose structure constants are computable without
the embedded order-157 class-character data.
