# Trace-GCD Borcherds / Local-Intersection Boundary

Date: 2026-06-05

This note records what the Borcherds/Gross-Zagier style literature can and
cannot supply for the current trace-GCD Schubert/operator-norm target.

## Current Target

The mixed representative theorem is now:

```text
Norm_{F[Y]/(Y^211-1)/F}(det_Q(P V_univ A)) is a p-unit.
```

Equivalently, the actual CM trace-GCD 16-plane:

```text
W_trace = A(K) subset R = F_p(mu_211)
```

avoids the 211 translated Schubert divisors:

```text
W_trace cap V_t^{-1} C = {0},      t mod 211.
```

This is a local-intersection statement for a determinant-line section on a
Grassmannian attached to the mixed CM trace data.

## Relevant Existing Machinery

Known CM-value formulas are relevant in shape:

```text
Gross-Zagier / Borcherds product formulas:
  factor norms of differences of modular functions or Borcherds CM values;

Schofer / Bruinier-Kudla-Yang style formulas:
  compute averages or values of Borcherds products over CM cycles;

p-adic theta / p-adic Gross-Zagier variants:
  compute p-adic valuations of special CM-value ratios in favorable modular
  settings.
```

Concrete references checked:

```text
Yang-Yin, "Difference of modular functions and their CM value factorization"
https://arxiv.org/abs/1711.02983

Daas, "CM-values of p-adic Theta-functions"
https://arxiv.org/abs/2309.17251

Schofer, "Borcherds Forms and Generalizations of Singular Moduli"
https://arxiv.org/abs/math/0603714
```

These support a plausible proof strategy only after the trace-GCD determinant
section is identified as a modular/Borcherds value or a quotient of such
values.

## Missing Bridge

The current determinant:

```text
f_trace = det_Q(P V_univ A)
```

is not yet a modular function on a standard modular curve.  It is a
determinant-line section built from:

```text
1. four relative trace maps defining K;
2. a selected 16-coordinate Lang projection;
3. a 211-cycle of right-origin translates.
```

Therefore known CM-value formulas do not apply directly.  They would apply if
we could construct a modular or automorphic product `Psi_trace` such that:

```text
Psi_trace(CM point)
  = unit * Norm(f_trace)
```

with the unit p-integral at the selected p24 prime.

The origin-norm power bridge sharpens this route.  It is enough to construct
`Psi_trace` for the full-origin determinant product, because that product is
a p-unit multiple of a power of the 211-term right norm.  The accounting and
boundary are recorded in:

```text
p24/lang_trace_gcd_origin_norm_power_theorem.md
p24/trace_gcd_full_origin_norm_boundary.md
p24/trace_gcd_full_origin_borcherds_gate.md
```

This does not permit computing the full-origin product by enumerating the
class set; it only says a closed product formula would descend to the right
finite certificate.

## Divisor Form Of The Needed Theorem

The exact divisor target is:

```text
D_trace = sum_{t mod 211} {W : W cap V_t^{-1} C != {0}}
```

on the relevant Grassmannian/period image.  The desired p-unit theorem is:

```text
the p24 CM point W_trace has zero local intersection with D_trace
at every prime above p = 10^24 + 7.
```

The p-local arithmetic is now pinned in:

```text
p24/trace_gcd_p24_local_invariants.py
p24/trace_gcd_p24_local_intersection_invariants.md
```

For the current trace, `t^2 - 4p = 4D_K` and
`Norm(t/2 + sqrt(D_K)) = p`, so the two ordinary primes above `p` are
explicitly oriented by `sqrt(D_K) = +/- t/2 mod p`.  The prime is split,
unramified, and prime to all `2`, `157`, `211`, `66254`, and `3107441`
certificate levels.  Thus a local-intersection proof has friendly p-local
denominator data; the missing part is still identifying the determinant
divisor.

A Borcherds proof would need to show that `D_trace`, pulled back along the
mixed-CM period map, is the divisor of a computable automorphic product.

The intrinsic determinant-line name for each summand is now recorded in:

```text
p24/trace_gcd_chow_norm_theorem_candidate.md
```

Each local equation is the Chow/Schubert hyperplane evaluation of the
translated complementary 19-plane against the CM 16-plane.  Thus a Borcherds
or local-intersection proof should target the pullback of this Chow divisor,
not a basis-dependent row-reduced determinant.

The bounded special-divisor tests are summarized in:

```text
p24/trace_gcd_chow_special_divisor_frontier.md
```

They rule out the easiest recognition patterns, including scalar-only global
matches and a broader dictionary of small phase units.  A positive proof must
therefore construct the determinant divisor itself.

## Boundary

The literature gives a method for p-adic unit proofs once the determinant is
a recognized CM value of a modular/Borcherds product.  It does not construct
that product for the current Schubert determinant.

So the current status is:

```text
productive theorem target:
  construct a modular/Borcherds product whose CM value is Norm(f_trace);

not yet justified:
  assuming existing Gross-Zagier/Borcherds formulas directly prove
  Norm(f_trace) is a p-unit.
```

This keeps the local-intersection route alive, but makes the missing bridge
explicit.
