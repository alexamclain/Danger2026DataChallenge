# Probability Lift Sidecar For Relative Content

Date: 2026-06-04

Scope: probability/statistical techniques only for the current p24
relative-content / Hermitian nonvanishing target.

## Target

For the third p24 CM target:

```text
p = 10^24 + 7
h = 205880396014 = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
real Hermitian packet degree = 194215
nontrivial Frobenius packets = 8
```

For each nontrivial relative-character Frobenius orbit, the exact certificate
is:

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1.
```

The preferred scalar sufficient certificate is the carry-adjusted Hermitian
packet:

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{-u mod m}(a).
```

Over C this is a positive sum of squares and is nonzero by principal-term
dominance.  The missing issue is selected-prime nonvanishing modulo the
chosen prime over `p`.

## Can Probability Upgrade To A Certificate?

Current answer: not with the available inputs.

Chebotarev can explain why a nonzero algebraic integer should avoid almost all
rational primes, but the p24 task is a fixed rational prime and a selected
prime above it.  To use Chebotarev as a certificate one would still need to
prove:

```text
p does not divide the relevant packet norm, or
the selected prime above p is not one of the divisor primes.
```

That is exactly the p-adic unit problem.

Second moment, concentration, anti-concentration, random-matrix, Weil, or
Deligne style bounds can bound averages over primes, characters, or CM
translates.  They do not name the selected finite-field embedding.  A zero
set can be tiny on average and still contain the selected prime.  The existing
modular zero-lemma route would upgrade averages to a proof only if the
relative packet were realized by a low-pole function with pole degree below
the CM orbit window.  Natural `X0` / correspondence / Atkin-Lehner proxies
miss this window for p24.

Schwartz-Zippel has the same issue: it certifies random evaluations of a
nonzero polynomial, not this fixed evaluation, unless paired with an explicit
evaluation oracle or an independent random seed that produces a checkable
Bezout certificate.

The random Hermitian form model is extremely favorable but still heuristic for
the fixed target.  One p24 packet behaves like a Hermitian form over
`F_{Q^2}` with:

```text
Q = p^194215
Pr[H_a = 0] ~= Q^-1
log10 Pr[H_a = 0] ~= -4661160
```

That says failure is fantastically unlikely for a random packet.  It is not a
proof that the CM packet attached to the selected p24 prime avoids the
isotropic cone.

## Exact Missing Independence / Equidistribution Theorem

A probability route would become a proof if it supplied a p24-specific
selected-prime anti-concentration theorem of the following strength.

Let `L` be the ring class field with the needed `n`th roots of unity, and let
`P | p` be the prime corresponding to the selected finite-field embedding.
For each of the eight nontrivial Frobenius packets `a`, define:

```text
V_a(P) = (J_0 mod f_a, ..., J_{m-1} mod f_a)
       in (F_p[X]/f_a)^m.
```

Strong exact form:

```text
V_a(P) != 0
```

for the selected `P`.

Probability-flavored sufficient form:

```text
#{sigma in Gal(L/Q(zeta_n)) : V_a(sigma P) = 0} = 0
```

or, for the scalar route,

```text
#{sigma : H_a(sigma P) = 0} = 0.
```

A merely asymptotic or average statement is not enough.  To force the integer
zero count to be zero, the theorem needs a pointwise anti-concentration bound
for this exact CM packet and this exact split prime, for example:

```text
#{sigma : H_a(sigma P) = 0} <= C * h / Q < 1
```

with `Q=p^194215` and an explicit constant/conductor factor `C < Q/h`.
Standard square-root cancellation over the `h` CM translates would not be
strong enough by itself, because `Q` is enormous and the selected value could
still be one of the rare zeros.

Equivalently, this theorem is a selected-prime p-unit theorem:

```text
H_a is a p-unit at every prime above p in the chosen decomposition packet
```

or the corresponding exact content ideal is not contained in the selected
prime.

## Small Evidence

Fast reruns on 2026-06-04:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_isotropy_probability_audit.py

log10_zero_probability ~= -4.661160e+06
log10_union_bound_8_packets ~= -4.661159e+06
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 30 --min-h 12 --max-h 80 --max-abs-D 12000 \
  --max-quotients 3 --min-n 5 --q-stop 150000 --summary-only

rows=30
packet_rows=66
nonlinear_packets=44
content_failures=0
energy_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/natural_relative_resolvent_scan.py \
  --max-cases 40 --min-h 12 --max-h 80 --max-abs-D 12000 \
  --max-quotients 5 --q-stop 180000 --summary-only

rows=40
quotient_rows=115
relative_characters_tested=433
relative_fibers_tested=1382
harmful_a_total=0
individual_zero_fiber_total=0
expected_random_zero_fibers=0.764109
all_equivalences_verified=1
```

Earlier broader runs remain more informative:

```text
packetized scans:
  126 + 70 + 272 packet rows
  content_failures = 0
  hermitian_zero_packets = 0
  ordinary energy zero packets = 2 in the low-order regime

natural relative scan:
  rows=160
  quotient_rows=520
  relative_characters_tested=2150
  relative_fibers_tested=7337
  harmful_a_total=0
  individual_zero_fiber_total=1
  expected_random_zero_fibers=2.908526
```

Interpretation:

```text
1. exact harmful all-fiber collapse has not appeared in natural CM packets;
2. the stronger product/nonzero-individual-fiber theorem is false in small
   natural data;
3. ordinary energy can vanish by cancellation;
4. Hermitian energy is the best scalar statistic seen so far, but its
   nonvanishing still needs arithmetic input beyond random linear algebra.
```

Upstream DANGER3 data is useful as a negative control.  It supports
`Theta(sqrt(p))` good-prefix density and only constant-factor character gates
for the Montgomery search problem.  It does not expose a growing statistical
selector for the p24 CM packet.

## Concrete Next Proof Statement

The most useful probability-shaped theorem to try to prove is:

```text
For the p24 third target and every nontrivial relative-character Frobenius
packet a, the Hermitian packet scalar H_a is a p-unit at the selected
decomposition prime over p.
```

If aiming to retain statistical language, prove the stronger uniform form:

```text
For every prime P above p in the selected decomposition packet,
H_a mod P != 0.
```

or the exact vector form:

```text
For every such P,
(J_0 mod f_a, ..., J_{m-1} mod f_a) != 0.
```

This is the only probability-lift statement identified here that would
actually certify the fixed p24 target.  Proving only density, expectation,
Chebotarev genericity, or random Hermitian anti-concentration would remain
evidence rather than a certificate.
