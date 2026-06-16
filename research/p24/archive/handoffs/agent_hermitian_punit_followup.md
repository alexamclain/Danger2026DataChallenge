# Hermitian p-unit follow-up

Date: 2026-06-05

Question: find a non-random route to the p24 selected-prime Hermitian packet
nonvanishing theorem, especially using p-adic valuation/product-formula inputs
in the Gross-Zagier / Schofer / Lauter-Viray neighborhood.

## Current scalar target

For the third p24 target

```text
p = 10^24 + 7
h = 205880396014 = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
real packet degree = 194215
packet count = 8
```

the preferred scalar certificate is

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{-u mod m}(a).
```

It is positive over the chosen complex embedding, but the needed finite-field
statement is

```text
H_a mod f_a != 0
```

for each of the eight real Frobenius packets.  Equivalently, with

```text
E^+ = Q(zeta_n + zeta_n^-1),
M^+ = (E^+)^<p>,
Xi_a = Norm_{E^+/M^+}(H_a),
```

the theorem is that `Xi_a` is a p-unit at every prime of `M^+` above `p`.

## New product-formula theorem candidate

The only genuinely new-looking non-random route is a phase-aware Borcherds
divisor certificate.

Candidate theorem:

```text
For each p24 Hermitian packet a, there exists a weakly holomorphic
vector-valued modular form F_a, or an equivalent explicit Borcherds input,
whose Borcherds product Psi_a satisfies

  Psi_a(CM(O)) = Xi_a * U_a

where U_a is a p-unit in M^+.

Moreover the principal part of F_a has no local p-intersection with the p24
ordinary CM cycle at the selected split prime p.
```

Then the Schofer / Lauter-Viray local valuation formula would give

```text
ord_p(Psi_a(CM(O))) = 0,
```

because p is split ordinary for the p24 CM order and the chosen principal part
has empty p-local representation/intersection contribution.  Since `U_a` is a
p-unit, this implies

```text
ord_p(Xi_a) = 0,
```

hence every Hermitian packet residue is nonzero.

This is not the previous random-bound framing.  It would be a deterministic
local-intersection computation: prove p-unitness by proving that the divisor
whose CM value is the packet norm does not meet the p24 CM cycle in
characteristic p.

## Proof skeleton if the Borcherds input exists

1. Construct a divisor/product object.

   Build `Psi_a` so that its CM value is the degree-8 decomposition-field
   packet norm `Xi_a`, up to explicitly listed cyclotomic or CM unit factors.
   The construction must retain the order-`3107441` relative character packet;
   a genus or full-class norm is not enough.

2. Check integrality and unit factors.

   Show `Psi_a(CM(O)) / Xi_a` is integral and a p-unit at all primes above
   `p`.  Any eta, discriminant, root-of-unity, or denominator factors must be
   visibly prime to `p`.

3. Apply the p-local valuation formula.

   Use the Schofer/Lauter-Viray style formula for the p-adic valuation of a
   Borcherds CM value.  The local term at p is a finite representation or
   intersection number attached to the principal part of `F_a`.

4. Prove the p-local term vanishes.

   Because `p` is split ordinary and not a bad prime for the CM order or the
   cyclotomic packet, choose/support the principal part so that no represented
   local norm contributes at p.  Then the formula gives `ord_p(Psi_a)=0`.

5. Descend to the finite-field packet.

   Since packet norms are exactly the residues of `Xi_a` at the eight primes
   of `M^+` above `p`, p-unitness of `Xi_a` gives `H_a mod f_a != 0` for all
   packets, which implies the relative-content gcd certificate.

## Sharp obstruction

The obstruction is step 1.  Existing product formulas do not currently supply
such a `Psi_a`.

Gross-Zagier difference norms control products of pairwise differences of
singular moduli.  Schofer and Lauter-Viray control CM values of Borcherds
products or intersection multiplicities with explicitly given divisors.  These
are symmetric enough to compute global norms or divisor intersections, but the
p24 scalar is an order-`3107441` non-genus Hermitian autocorrelation packet.

In concrete terms,

```text
H_a = sum_d zeta_n^(a*d) C_d
```

is a high-order Fourier coefficient of the CM pair-correlation sequence, not a
known modular unit value.  A product formula that averages over all `d`, over
all classes, over genus characters, or over all CM pairs has already discarded
the phase indexed by `a`.

Thus the required input is very precise:

```text
Construct a modular/Borcherds divisor whose CM value is the packet norm Xi_a
and whose principal part is known without summing the order-3107441 relative
subgroup.
```

Without this construction, p-adic product formulas only repackage the missing
p-unit theorem.  If such a construction exists, the p-local valuation formula
is exactly the right tool: it could prove p-unitness by showing the selected
ordinary CM reduction is disjoint from the packet divisor.

## Small discriminating experiment

Do not run this at p24 scale.  In a small split CM row with prime relative
length `n`, build the exact rational function `R_a(X)` modulo the class
polynomial such that

```text
R_a(j_0) = Xi_a
```

or the corresponding packet scalar.  Factor the divisor of `R_a` on the small
`j`-line and classify its zeros:

```text
CM/Heegner-supported zeros?
cuspidal/modular-unit-supported zeros?
generic non-CM zeros?
```

If the zeros are Heegner/cuspidal in the tested prime-`n` cases, the
Borcherds-divisor route is credible.  If generic non-CM zeros appear, then
Gross-Zagier/Schofer/Lauter-Viray inputs cannot directly specialize to the
Hermitian packet; the packet norm is not living in the divisor class these
formulas compute.

## Follow-up Divisor-Shape Diagnostic

The small test is now implemented in:

```text
p24/packet_scalar_divisor_shape_toy.py
p24/packet_scalar_divisor_shape_boundary.md
```

For the Hermitian packet norm on the `D=-5000` and `D=-2239` toy torsors, the
minimal interpolation degrees in the plain `j` coordinate are generic:

```text
D=-5000 h=30:
  polynomial degree 29, rational degree 15, matching random controls

D=-2239 h=35:
  polynomial degree 34, rational degree 17 or 18, matching random controls
```

The ordinary autocorrelation control has degree `0` because it is invariant
under rotating the CM cycle.  Thus the Hermitian scalar remains the stronger
finite-field certificate, but it does not look like a simple one-variable
modular function of `j`.  A Borcherds proof would need to construct a
phase-aware divisor directly, not find a low-degree `j`-function hiding in the
data.

## Verdict

The best new theorem candidate is:

```text
Phase-aware Borcherds p-unit theorem for the p24 Hermitian packet norm Xi_a.
```

The easy Heegner-support version of this route is now tested in:

```text
p24/phase_divisor_heegner_support_scan.py
p24/phase_divisor_heegner_support_boundary.md
```

On the non-genus row `D=-2239, q=2243`, the Hermitian packet interpolant has
generic rational degree and its numerator roots are not target CM roots and
have no small-Heegner hits in the bounded scan.  The `D=-5000` calibration has
at most an isolated small-Heegner collision, not full Heegner support.

So the Borcherds route, if true, must construct a genuinely phase-aware
divisor rather than recognize the tautological plain-`j` interpolant as a
simple Heegner-supported function.

Its proof would be deterministic and p-adic: realize `Xi_a` as a Borcherds CM
value and use the local valuation formula to prove no contribution at the
selected split prime.

The sharp obstruction is equally clear:

```text
Known Gross-Zagier/Schofer/Lauter-Viray formulas do not construct the
order-3107441 phase-aware divisor.  Producing that divisor without class
enumeration is essentially the missing new input.
```
