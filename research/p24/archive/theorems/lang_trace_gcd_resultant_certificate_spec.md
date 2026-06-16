# Lang Trace-GCD Resultant Certificate Spec

Date: 2026-06-05

This note turns the reduced trace-gcd origin product into an explicit finite
verifier object.

The sharpened p24 payload manifest is:

```text
p24/trace_gcd_subsqrt_certificate_manifest.md
```

and its finite honesty gate is Lean-checked in:

```text
p24/lean/TraceGcdPayloadGate.lean
```

## Finite Target

After origin covariance and kernel transport, the representative row reduces
to:

```text
Delta(t) = det(P V_t A),        t mod 211.
```

Here `A` is the transported tail map from the prefix trace kernel `K_0`,
`V_t` is right multiplication by `zeta_211^t`, and `P` is the selected
first-16 Lang-coordinate projection.  The p-unit target is:

```text
Delta(t) != 0 for every t mod 211.
```

Equivalently:

```text
Pi_trace = prod_{t mod 211} Delta(t) != 0 mod p.
```

## Verifier Forms

Because the actual small trace-gcd sequences are not Frobenius-compatible as
raw base-field values, the safest verifier form is value-based rather than a
base-coefficient polynomial in `F_p[Y]`.

A finite certificate may supply:

```text
Delta_0,...,Delta_210 in F_p,
Inv_0,...,Inv_210 in F_p,
```

and the verifier checks:

```text
Delta_t * Inv_t = 1 mod p       for every t.
```

This proves every right translate is nonzero.  The data size is `422` base
field elements, independent of the class number and far below `sqrt(p)`.

Equivalently, the verifier can group by the Frobenius action:

```text
{0} plus six length-35 right orbits.
```

For each orbit `O`, supply:

```text
Pi_O = prod_{t in O} Delta_t,
Pi_O_inv,
```

and check both the product and inverse relation:

```text
Pi_O = prod_{t in O} Delta_t,
Pi_O * Pi_O_inv = 1.
```

This is a seven-p-unit check once the `Delta_t` values are trusted or
recomputed.  Equivalently, it is valid once a producer theorem proves the
zero-detection implication:

```text
Delta_t = 0  =>  Pi_orbit(t) = 0.
```

Thus seven orbit products are a compressed producer-theorem payload, not by
themselves a value certificate.  The one-scalar norm/resultant form has the
same honesty requirement:

```text
(exists t, Delta_t = 0)  =>  Norm_trace = 0.
```

## Polynomial / Resultant View

Over a splitting field, the Pluecker-Fourier polynomial satisfies:

```text
Delta(t) = f(zeta_211^t),
```

and:

```text
prod_t Delta(t) = Res(Y^211 - 1, f(Y)).
```

If a coefficient representation of `f` is supplied in the splitting algebra,
the verifier can instead check a Bezout identity:

```text
U(Y) f(Y) + V(Y)(Y^211 - 1) = 1.
```

But this should not be mistaken for a base-coefficient polynomial over `F_p`
unless the values satisfy:

```text
Delta(p*t) = Delta(t).
```

The pinned actual-CM trace-gcd row fails this compatibility:

```text
right_sequence_frobenius_compatibility_mismatches=6/7.
```

So for p24, a base-value or split-algebra verifier is the honest finite
object.

## Toy

Added:

```text
p24/lang_trace_gcd_resultant_certificate_toy.py
```

Success run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_resultant_certificate_toy.py --q 337 --right 7
```

reported:

```text
value_zero_count=0
product_mod_q=141
resultant_mod_q=141
product_resultant_match=1
gcd_degree=0
bezout_unit_certificate=1.
```

Forced zero run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_resultant_certificate_toy.py --q 337 --right 7 --force-zero
```

reported:

```text
value_zero_count=1
product_mod_q=0
resultant_mod_q=0
gcd_degree=1
bezout_unit_certificate=0.
```

## Remaining Arithmetic Producer

This finite certificate is small enough.  The missing theorem is the producer:
construct the actual `Delta_t` values, or a split-algebra `f`, from embedded
CM trace-gcd data without enumerating the class set.

Current exact identity:

```text
Delta(t)
  = sum_{I subset O, |I|=16}
      det(P_I) det(A_I) zeta_211^(t * sum(I)).
```

Thus a constructive proof must provide one of:

```text
1. the transported tail map A=T_i|K_0 from an embedded class-field formula;
2. the Pluecker-Fourier coefficients c_s with proof they come from A;
3. the value list Delta_t with a class-field identity certifying the values;
4. a direct divisor/norm theorem proving all Delta_t are p-units.
```

The finite verifier is now sub-sqrt.  The unresolved work is the embedded
arithmetic construction of its inputs.

## Spectral-Collapse Status

The first `(4,7)` trace-GCD row had degree-3 right support, but the follow-up
scan in:

```text
p24/lang_trace_gcd_spectral_scan_boundary.md
```

shows why this should not be overread.  For p24, the exterior support of the
right action with `right=211` and `tail=16` is already full by `k=3`, so a
degree-35 Gauss-period certificate would require special Pluecker
cancellations, not just representation theory.

Therefore the conservative finite certificate remains:

```text
Delta_0,...,Delta_210 plus inverses,
```

or the equivalent direct split-algebra resultant.  A one-orbit Gauss-period
norm is still a possible strengthening, but it is no longer the default
producer target.

The direct split-algebra resultant can also be read as one operator norm:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
```

It identifies:

```text
prod_t Delta(t)
  = det(m_f on F[Y]/(Y^211 - 1)),
```

where `f(Y)=det(P diag(Y^v) A)`.  This is now the preferred language for a
class-field producer theorem, even though constructing the actual p-integral
`f` remains the hard arithmetic input.

The p-integral lift conditions are recorded in:

```text
p24/lang_trace_gcd_integrality_lift.md
```

The equivalent Schubert-orbit avoidance form is recorded in:

```text
p24/lang_trace_gcd_schubert_orbit_theorem.md
```
