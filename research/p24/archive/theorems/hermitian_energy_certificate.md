# Hermitian Energy Certificate

The relative-energy scalar

```text
E_a = sum_u P_u(a)P_u(-a)
```

is useful, but it is not the positive complex norm of the content vector.  A
closely related scalar is.

## Setup

Let

```text
h = m*n,
P_u(a) = sum_k zeta_n^(a*k) j_{u+m*k}.
```

Assume the CM origin is chosen so complex conjugation acts on the class group
by inversion:

```text
conj(j_i) = j_-i.
```

For `0 <= u < m`, define

```text
u* = -u mod m,
c(u) = (u + u*) / m.
```

Then

```text
conj(P_u(a)) = zeta_n^(a*c(u)) P_{u*}(a).
```

Therefore the Hermitian scalar

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{u*}(a)
```

satisfies

```text
H_a = sum_u |P_u(a)|^2
```

under the chosen complex embedding.  In particular, in characteristic zero:

```text
H_a = 0  iff  every P_u(a)=0.
```

Modulo the selected p24 prime, `H_a != 0` is a sufficient certificate against
harmful vanishing, just like `E_a != 0`.

## Polynomial Form

With

```text
J_u(X) = sum_k j_{u+m*k} X^k,
```

the Hermitian packet polynomial is

```text
H(X) = sum_u X^c(u) J_u(X) J_{u*}(X).
```

Reducing modulo a Frobenius packet factor `f_a` gives the finite-field scalar
for the orbit of `a`.

This is now checked in:

```text
p24/packetized_relative_content_scan.py
```

The scan computes exact content, ordinary energy, and Hermitian energy on the
same packet rows.

## Toy Checks

The indexing and positivity distinction are checked in:

```text
p24/complex_energy_positivity_boundary_toy.py
```

The run reports:

```text
max_conjugation_error=3.797e-15
finite_field_energy_pairing=48.9910204082
hermitian_positive_pairing=86.8376961849
sum_abs_square=86.8376961849
energy_equals_positive=0
positive_equals_abs_square=1
```

So the old energy is not the positive pairing, while the carry-adjusted
Hermitian scalar is.

The packetized CM scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 50 --min-h 12 --max-h 96 --max-abs-D 20000 \
  --max-quotients 3 --min-n 5 --q-stop 200000 --summary-only
```

found:

```text
packet_rows=126
nonlinear_packets=82
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

I also ran the scan in the known low-order failure regime:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 40 --min-h 2 --max-h 30 --max-abs-D 2000 \
  --max-quotients 4 --min-n 2 --q-stop 50000 --summary-only
```

It found ordinary energy failures but no Hermitian failures:

```text
packet_rows=70
nonlinear_packets=36
content_failures=0
energy_zero_packets=2
packet_norm_zero_packets=2
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

The exact random-model scale is recorded in:

```text
p24/hermitian_isotropy_probability_audit.py
p24/hermitian_isotropy_probability_audit.md
```

For one p24 packet, the Hermitian scalar is modeled by a nondegenerate
Hermitian form on `F_{Q^2}^m` with

```text
Q = p^194215,
m = 66254.
```

The exact zero count is

```text
Q^(2m-1) + (-1)^m (Q-1)Q^(m-1),
```

so a random packet failure has probability about `Q^-1`.  Numerically:

```text
log10_zero_probability≈-4.661160e6
log10_union_bound_8_packets≈-4.661159e6
```

The scalar does not factor through quotient periods alone.  The boundary note

```text
p24/hermitian_internal_character_boundary.md
```

and toy

```text
p24/hermitian_not_quotient_period_invariant_toy.py
```

construct two datasets with the same quotient period vector `J_u(1)` but
different Hermitian packet values.  Thus computing the degree-`m` quotient
period polynomial is not enough; the scalar still depends on nontrivial
relative `H`-characters.

## p24 Relevance

For the third p24 target,

```text
m = 66254,
n = 3107441,
ord_n(p) = 388430,
(n-1)/ord_n(p) = 8.
```

The Hermitian packet certificates have the same Frobenius packet structure as
the ordinary energy certificates.  Since the scalar is invariant under
complex conjugation by construction, it should again live in the real
cyclotomic packet field, with degree `194215` over the degree-8 decomposition
field.

The possible theorem target is:

```text
prove the degree-8 decomposition-field norm of the p24 Hermitian energy is a
p-unit.
```

This target has a better characteristic-zero property than the old energy:
it is strictly positive whenever the content vector is nonzero.

For p24, this positivity can be made completely explicit by principal-term
dominance:

```text
p24/hermitian_principal_dominance_audit.py
p24/hermitian_principal_dominance_theorem.md
```

The `u=0` fiber contains the principal singular modulus with coefficient `1`,
and every other term has reduced-form denominator at least `2`.  The audit
reports:

```text
p0_dominance_margin=2.538350e12
log_Hermitian_embedding_lower=1.015340e13
```

So every p24 Hermitian packet is nonzero in characteristic zero by an
overwhelming archimedean margin.

## Boundary

This still does not prove the p24 certificate.  A positive algebraic integer
can vanish modulo a selected split prime, and the singular-modulus heights are
far too large for the crude norm-height argument to rule out p-divisibility.

Also, over finite fields a Hermitian form in at least two variables can be
isotropic.  The artificial obstruction in

```text
p24/energy_isotropy_obstruction_toy.py
```

therefore still applies to this positive scalar after reduction: nonzero
content does not formally imply nonzero Hermitian packet value modulo `p`.

The scale is recorded in:

```text
p24/hermitian_energy_height_gap_audit.py
```

For the third p24 target it reports:

```text
log_p = 55.262042
log_Hermitian_energy_bound = 1.015340e13
log_one_decomposition_prime_norm_bound = 1.971942e18
one_prime_bound_over_log_p = 3.568349e16
required_one_prime_height_reduction = 2.802417e-17
```

So even at the level of one prime of the degree-8 decomposition field, a
naive "positive and norm smaller than p" argument is off by more than sixteen
orders of magnitude in the exponent.

So the Hermitian scalar improves the shape of the arithmetic target, but the
missing input remains a selected-prime p-adic unit theorem or an explicit
embedded finite-field identity.
