# Hermitian Mixed Right-Orbit Support Theorem Candidate

This note records a stronger dual-trace theorem candidate suggested by the
current trace-intersection formulation.

## Dual Trace Support

For

```text
L = F_p(mu_157),   R = F_p(mu_211),   E = L R,
S_j = H_{157,211}(1,v_j),
```

the current theorem is:

```text
for every nonzero lambda in L,
some Tr_{E/R}(lambda*S_j) is nonzero.
```

Equivalently, the six right orbit packets separate all nonzero left
characters.

## Stronger Candidate

A stronger statement is:

```text
for every nonzero lambda in L,
at least two of the six values Tr_{E/R}(lambda*S_j) are nonzero.
```

If true, then any five of the six right orbit packets already separate `L`.
In the centered-profile language, a failure of the original theorem is a
nonzero left twist whose nontrivial right Fourier spectrum disappears
entirely.  The stronger theorem also rules out support contained in a single
right orbit.

## Cyclic-Code Form

For each `lambda in L`, define the base-field scalar sequence

```text
f_lambda(s) = Tr_{L/F_p}(lambda * G_s^0),      s mod 211.
```

Its nonzero right Fourier coefficients are exactly the six orbit traces
`Tr_{E/R}(lambda*S_j)` unpacked over Frobenius.  Therefore:

```text
original theorem:
  f_lambda is not the zero word for lambda != 0;

support >= 2 theorem:
  f_lambda is not contained in any single irreducible right-orbit cyclic code.
```

So the stronger theorem is a cyclic-code avoidance statement for the
156-dimensional left-twist family:

```text
{ f_lambda : lambda in L } avoids 0 and avoids each of the six
35-dimensional nontrivial right-orbit code components.
```

This is potentially proof-friendly because it converts the target into an
incidence theorem between a class-field trace family and seven explicit
cyclic-code subspaces of functions on `Z/211Z`.

## Delsarte/Delete-One Dictionary

Let `O_j={p^b v_j mod 211 : 0 <= b < 35}` be the six nonzero right
Frobenius orbits and define

```text
a_j(lambda) = Tr_{E/R}(lambda*S_j).
```

Delsarte's trace-code decomposition gives the exact Fourier dictionary:

```text
hat f_lambda(p^b v_j) = a_j(lambda)^(p^b),
```

and

```text
f_lambda(s) =
  211^(-1) * sum_j Tr_{R/F_p}(a_j(lambda)*zeta_211^(-v_j*s)).
```

Thus the six nontrivial irreducible cyclic-code components are standard; the
new arithmetic input is the delete-one rank theorem

```text
for every j,
rank_Fp(lambda |-> (a_k(lambda))_{k != j}) = 156.
```

This is equivalent to the support-`>=2` strengthening.  It is a better proof
target than generic cyclic-code minimum distance: BCH/Delsarte identify the
six ideals, but they do not by themselves prove that the CM trace family
avoids any one of them.

In Moore-certificate form, this asks for six p-units.  For each deleted right
orbit `j`, take the `175` Lang/trace-dual coordinates from the remaining five
orbits.  The sharp current candidate is:

```text
the leading 156 of those 175 coordinates already have nonzero Moore
determinant over F_p.
```

This would make the certificate deterministic: six named Moore minors, not an
existential minor search.

The corresponding erasure-incidence statement is recorded in:

```text
p24/hermitian_mixed_leading_erasure_theorem.md
```

## Toy Audit

Added:

```text
p24/hermitian_mixed_orbit_support_toy.py
```

Six-right-orbit miniature:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_orbit_support_toy.py \
  --q 2 --left 7 --right 31 --trials 40 --summary-only
```

reported:

```text
support_tests=80
full_rank_tests=80
delete_one_full_rank_tests=80
delete_one_leading_full_rank_tests=10
zero_support_failures=0
one_support_strong_failures=0
frobenius_stable_tests=80
min_lambda_support=3
min_delete_one_leading_rank=0
max_stability_defect=0
```

One-right-orbit control:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_orbit_support_toy.py \
  --q 2 --left 7 --right 5 --trials 40 --summary-only
```

reported:

```text
support_tests=80
full_rank_tests=52
delete_one_full_rank_tests=0
delete_one_leading_full_rank_tests=0
zero_support_failures=28
one_support_strong_failures=80
frobenius_stable_tests=56
min_lambda_support=0
min_delete_one_leading_rank=0
max_stability_defect=1
```

So the six-orbit shape strongly supports the delete-one theorem in the toy
model, while the one-orbit control fails exactly where it should.  The
leading-prefix condition is much stricter: it holds only `10/80` times in the
random six-orbit toy.  Therefore the leading Moore candidate is not a generic
consequence of delete-one rank; it would need a genuine CM p-unit theorem.

Larger pure-Python finite-field toys such as `q=11,left=61,right=19` and
`q=2,left=17,right=31` were intentionally stopped because finite-field
arithmetic became slower than the theorem-shaping value.  The useful output
here is the exact cyclic-code formulation and the six-orbit miniature/control
split, not a broad random-rank search.

## Actual-CM Delete-One Diagnostic

I extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

with two Delsarte-side diagnostics:

```text
delete_one_min_transformed_rank
delete_one_full_count
```

and, when `q^left_degree-1` is below the small enumeration budget:

```text
centered_trace_min_right_orbit_support
centered_trace_zero_support_count
centered_trace_one_support_count
```

Pinned positive stress row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_left_subfield_normality_audit.py \
  --only-D -13319 --max-rows 1 --max-h 200 --max-abs-D 14000 \
  --min-n 5 --max-n 5 --q-stop 20000 --max-splitting-primes 1 \
  --max-axis-dim 20 --max-m 40 --min-factor-degree 3 \
  --max-factor-degree 10 --max-extension-degree 8 --include-linear \
  --min-left-orbit-len 3 --summary-only
```

reported:

```text
full_left_span_tests=8
delete_one_full_left_span_tests=5
delete_one_annihilator_degree_mismatches=0
delete_one_annihilator_vanish_failures=0
delete_one_zero_residual_norms=0
delete_one_full_field_annihilator_all_tests=5
delete_one_leading_full_tests=5
delete_one_leading_annihilator_degree_mismatches=0
delete_one_leading_annihilator_vanish_failures=0
delete_one_leading_zero_residual_norms=0
delete_one_leading_full_field_annihilator_all_tests=5
centered_trace_support_checked_tests=2
centered_trace_zero_support_tests=0
centered_trace_one_support_tests=0
min_centered_trace_right_orbit_support=2
```

The checked exhaustive trace-support cases line up with the stronger theorem:
no nonzero left twist vanished, and none was supported on a single right orbit.
The full delete-one cases also have full-field annihilator polynomials after
deleting either orbit, and the explicit leading-prefix test matches them.

For the full `(7,7)` and `(4,7)` stress cases, the delete-one pivot prefixes
are leading:

```text
(7,7): deletepivotprefixes [[0,1,2], [0,1,2]]
(4,7): deletepivotprefixes [[0,1], [0,1]]
```

The aggregate delete-one counts are unchanged under origin shifts `1,2,3,4`
on `D=-13319`; the full cases above still have leading pivot prefixes in the
checked shifted row.  This supports the leading-delete-one-Moore-minor
candidate, although it is still small-degree evidence rather than proof.

Pinned boundary row:

```text
D=-6719:
delete_one_full_left_span_tests=0
max_delete_one_min_transformed_rank=0
```

This row has only one right orbit in the stressed components, so deleting one
orbit leaves no right packet.  It is a useful control, not a p24-like
six-orbit test.

## Galois-Stable Normal Frame Candidate

Another possible strengthening is:

```text
U = span_Fp{centered profile values}
is Frobenius-stable, and U contains one normal element of L/F_p.
```

Then `U=L`.

The actual-CM audit now records:

```text
centered_profile_stability_defect
centered_profile_max_single_normal_rank
centered_profile_normal_coordinate_count
```

Pinned `D=-10919` and `D=-8711` rows have stability defect `0`, but their
left orbit length is only `2` and the tested profile already spans the whole
left field.  This does not prove the candidate.  The one-right-orbit random
control has nonzero stability defect in failed rows, so stability is not a
formal consequence of the toy setup.

The actual-CM stress row `D=-6719` gives the sharper boundary:

```text
left orbit length=6
packet degree=4
centered_profile_max_single_normal_rank=6
centered_profile_stability_defect=2
full=0
```

Thus a normal coordinate can exist even when the centered-profile span is not
Frobenius-stable and not full.  A normal-frame proof must prove stability
first.

## Current Status

The right-orbit support theorem is a useful possible strengthening:

```text
minimum right trace support >= 2.
```

For p24 it would imply the mixed Schur theorem with slack, and it gives a
clear falsifier: find a nonzero left twist supported on one right orbit.

The finite implication is Lean-checked in:

```text
p24/lean/MixedRightOrbitSupportGate.lean
```
