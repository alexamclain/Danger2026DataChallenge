# Relative Moment Projection Theorem Target

This note records a new aggregate scalar route between exact relative content
and the stronger prime augmentation-normality theorem.

## Setup

For the third p24 target,

```text
h = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
(n-1)/ord_n(p) = 8
```

write

```text
J_u(X) = sum_k j_{u+m*k} X^k,      0 <= u < m.
```

For a Frobenius packet factor `f_a | Phi_n`, the exact harmful-packet
certificate is

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1.
```

Equivalently, not all residues `J_u mod f_a` vanish.

## Moment Projections

Define quotient-coordinate moments

```text
M_e(X) = sum_{u=0}^{m-1} u^e J_u(X).
```

If all `J_u` vanish modulo `f_a`, then every `M_e` vanishes modulo `f_a`.
Therefore

```text
M_e mod f_a != 0
```

for any one `e` proves the exact content condition for that packet.

Globally, for a bounded set of moments `E`, the sufficient aggregate
certificate is

```text
gcd(Phi_n, {M_e : e in E}) = 1.
```

For `E={0,1}` this is a two-scalar certificate:

```text
gcd(Phi_n, M_0, M_1) = 1.
```

It is strictly weaker than prime augmentation normality, which asks for

```text
gcd(Phi_n, J_u) = 1      for every u.
```

It is also weaker than the product certificate: individual coordinates may
vanish while the low moments still certify that the packet vector is nonzero.

## Complement Section

There is a more structured version when `gcd(m,n)=1`, as in p24.  Since

```text
G = <g> ~= C_(mn),
H = <g^m>,        |H| = n,
K = <g^n>,        |K| = m,
G = H x K,
```

use the complement representatives

```text
i = n*r + m*k,       0 <= r < m, 0 <= k < n.
```

The zeroth complement moment is

```text
T(X) = sum_{k=0}^{n-1} Y_k X^k,
Y_k = sum_{r=0}^{m-1} j_{n*r + m*k}.
```

This is not an arbitrary transverse slice: `Y_0` is the trace of `j` over the
order-`m` complement subgroup `K`, and the `Y_k` are its conjugates under
`H`.  Thus

```text
T(zeta_n^a)
```

is an ordinary `H`-character resolvent of the quotient trace element
`Tr_K(j)` in the degree-`n` field fixed by `K`.

This gives a cleaner theorem target:

```text
Res(Phi_n, T) != 0 mod p.
```

If true, it proves exact relative content for every nontrivial `H` packet
with a single scalar resultant.  It is still a sufficient certificate, not an
equivalence: a nonzero content vector can have zero complement trace.

For p24 this would expose the degree-`3107441` recovery object first, then
one would still need a relative degree-`66254` relation from `Tr_K(j)` back to
one `j` root.  Both degrees are far below `sqrt(p)`, but constructing the
embedded trace polynomial and recovery relation remains the missing class-field
theorem.

## Single-Scalar Variant

If `gcd(Phi_n,M_0,M_1)=1`, then a generic linear projection

```text
L_lambda = M_0 + lambda M_1
```

is nonzero in every packet.  Packetwise, a bad `lambda` must equal
`-M_0/M_1` when this ratio lies in `F_p`; otherwise no base-field `lambda`
kills that packet.  Thus at most one `lambda` is forbidden per packet where
`M_1` is nonzero.

For p24 there are only eight nontrivial packets, so this suggests an
equivalent one-resultant certificate after choosing a small `lambda`:

```text
Res(Phi_n, M_0 + lambda M_1) != 0 mod p.
```

This is a certificate packaging trick, not yet an arithmetic proof.

## Experiments

I added:

```text
p24/relative_moment_projection_scan.py
```

Pinned composite coordinate-zero case:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --only-D -1336 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 1777 --q-stop 1778 \
  --include-linear --max-moment-degree 4 --scan-origins
```

Output summary:

```text
packet_rows=72
content_failures=0
nonzero_content_missed_by_moments=0
moment_histogram={'0': 72}
```

So the moment scalar survives exactly where the product/coordinate theorem
fails.

Moderate origin-rotated scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 80 --min-h 12 --max-h 120 --max-abs-D 30000 \
  --max-prime-quotients 6 --max-composite-quotients 6 \
  --min-n 3 --max-n 120 --q-stop 300000 \
  --include-linear --max-moment-degree 1 --scan-origins --summary-only
```

Output:

```text
packet_rows=5861
prime_packet_rows=2751
composite_packet_rows=3110
content_failures=0
nonzero_content_missed_by_moments=0
moment_histogram={'0': 5856, '1': 5}
moment0_failures=5
moment01_failures=0
expected_moment0_failures_random=3.512963
expected_moment01_failures_random=0.009254
```

Wider non-origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 160 --min-h 12 --max-h 150 --max-abs-D 60000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 150 --q-stop 600000 \
  --include-linear --max-moment-degree 3 --summary-only
```

Output:

```text
packet_rows=651
prime_packet_rows=301
composite_packet_rows=350
content_failures=0
nonzero_content_missed_by_moments=0
moment_histogram={'0': 650, '1': 1}
moment0_failures=1
moment01_failures=0
expected_moment0_failures_random=0.442249
expected_moment01_failures_random=0.001260
```

The only repeated `M_0` failure was:

```text
D=-824 q=431 ell=3 h=20 m=4 n=5 deg=1
origins 0,4,8,12,16
first_nonzero_moment=1
```

Complement-section scans were cleaner:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 60 --min-h 12 --max-h 120 --max-abs-D 25000 \
  --max-prime-quotients 6 --max-composite-quotients 6 \
  --min-n 3 --max-n 120 --q-stop 250000 \
  --include-linear --max-moment-degree 1 \
  --section complement --scan-origins --summary-only
```

Output:

```text
packet_rows=2727
prime_packet_rows=1667
composite_packet_rows=1060
content_failures=0
nonzero_content_missed_by_moments=0
moment_histogram={'0': 2727}
moment0_failures=0
expected_moment0_failures_random=1.596667
```

and

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 160 --min-h 12 --max-h 150 --max-abs-D 60000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 150 --q-stop 600000 \
  --include-linear --max-moment-degree 2 \
  --section complement --summary-only
```

gave

```text
packet_rows=423
content_failures=0
moment_histogram={'0': 423}
moment0_failures=0
expected_moment0_failures_random=0.275300
```

A wider complement scan finally found `M_0` failures, while `{M_0,M_1}` still
certified every observed nonzero packet:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 120 --min-h 12 --max-h 180 --max-abs-D 90000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --include-linear \
  --max-moment-degree 1 --section complement --summary-only
```

Output:

```text
packet_rows=650
content_failures=0
nonzero_content_missed_by_moments=0
moment_histogram={'0': 649, '1': 1}
moment0_failures=1
moment01_failures=0
```

Pinned failures:

```text
p24/complement_m0_failure_toy.py

D=-899 q=281 h=14 m=2 n=7
residues at factor X+32: [-69, 69]
M0=0, M1=69, content_zero=0
```

and

```text
D=-216 q=103 h=6 m=2 n=3
first_nonzero_moment=1
content_failures=0
moment0_failures=1
moment01_failures=0
```

I added an early-exit falsifier:

```text
p24/moment_pair_failure_search.py
```

It stops as soon as it finds a nonzero content packet with both `M_0` and
`M_1` zero.  Bounded non-origin runs:

```text
section=complement: tested_packets=545, m0_failures=1, pair_failures=0
section=contiguous: tested_packets=810, m0_failures=2, pair_failures=0
```

Bounded origin-rotated runs:

```text
section=complement: tested_packets=1204, m0_failures=0, pair_failures=0
section=contiguous: tested_packets=1565, m0_failures=0, pair_failures=0
```

## Interpretation

The experiments support this hierarchy:

```text
exact content:                 no failures observed
moments {M_0,M_1}:             no failures observed
complement trace M_0:           rare random-rate failures, even for prime n
moment M_0 alone:              rare random-rate failures
coordinate/product theorem:    false for composite n
```

The random baseline is important.  The observed `M_0` failures are close to
the random expectation `sum q^(-deg f)`, so the moment scan is not by itself
evidence of a special CM unit theorem.  It is evidence that a two-moment
scalar certificate is a very efficient way to package exact content.

The two-moment condition is not a linear-algebra consequence of nonzero
content.  For `m >= 3`, nonzero residue vectors can have both zero sum and
zero first moment.  The point of the scan is that the actual CM packet vectors
have not shown this failure in the tested windows.

For p24 the random model predicts

```text
Pr[M_0 packet zero]  ~= p^(-388430)
Pr[M_0 and M_1 zero] ~= p^(-776860)
```

per packet.  This is effectively zero heuristically, but a certificate still
needs a selected-prime p-unit proof.

## Arithmetic Boundary

The surviving theorem target is now sharper:

```text
prove gcd(Phi_3107441, M_0, M_1) = 1 mod p
```

or, after choosing a safe `lambda`,

```text
prove Res(Phi_3107441, M_0 + lambda M_1) != 0 mod p.
```

This would imply the exact relative-content certificate for all eight p24
packets without requiring 66,254 coordinate resultants.

The one-lambda packaging boundary is recorded in:

```text
p24/moment_lambda_bad_values_scan.py
p24/moment_lambda_packaging_boundary.md
```

The finite conclusion is:

```text
if {M0,M1} is nonzero in a packet, then at most one base-field lambda makes
M0 + lambda*M1 vanish in that packet.
```

Small selected-prime scans found no `{M0,M1}` pair failures, but did find
small bad lambdas for individual rows.  Thus a one-resultant certificate is
available only after choosing a lambda outside the finite bad set; the robust
arithmetic target remains `gcd(Phi_n,M0,M1)=1`.

What is still missing is a structural way to prove the p-unit statement for
these transverse quotient moments.  They are low-degree projections of the
relative content vector, but the coefficients depend on a chosen quotient
section.  Characteristic-zero nonvanishing follows the same principal
dominance philosophy as ordinary class-character resolvents when the
principal coefficient is nonzero; it does not imply selected-prime unitness.

The first derivative has a new construction boundary:

```text
p24/crt_partial_moment_tower_boundary.md
```

For composite `m`, the literal integer-representative moment

```text
M_1 = sum_r r J_r
```

does not equal the CRT sum of prime-factor partial moments.  It differs by a
carry term:

```text
M_1 = sum_i e_i P_i - m*C.
```

The carry is joint in the CRT components, so the actual Hasse derivative is
not automatically a smooth tower object.  The tower-native replacement is a
finite projection family:

```text
M_0, P_2, P_157, P_211.
```

The finite logic for such a projection family is now checked in
`p24/lean/GlobalContentGate.lean`; the arithmetic target is:

```text
gcd(Phi_3107441, M_0, P_2, P_157, P_211) = 1 mod p.
```

The refined formulation is now:

```text
p24/relative_augmentation_order_theorem.md
p24/relative_augmentation_order_scan.py
```

For each packet factor `f_a`, set

```text
V_a(Y) = sum_u (J_u mod f_a) Y^u.
```

Then `{M_0,M_1}` is exactly the first-order augmentation-jet certificate:
nonzero `V_a` must not lie in `(Y-1)^2`.  The complement `M_0` term is the
constructive `K`-trivial class-character resolvent; `M_1` is the first
augmentation derivative in the `K` direction.

Thus this is a better scalar theorem target, not yet the final speedup.

## Complement Generator Audit

The complement trace would be especially constructive if the order-`m`
subgroup `K` had a very small split-prime correspondence generator.  I checked
the simplest version with class logs relative to the norm-23 generator.

Single split primes up to `20000`:

```text
single_split_prime_order_66254_audit
prime_bound=20000
split_prime_logs=1091
target_index=3107441
hits=0
```

Signed split-prime-power products of norm at most `66254`:

```text
exhaustive_signed_prime_power_order_66254_audit
prime_bound=66254
norm_bound=66254
split_prime_logs=3270
visited_products=32080
target_index=3107441
hits=0
```

So the complement trace is not unlocked by a single tiny cycle or by a
norm-`<=m` split-prime-power word.  A constructive version would need to build
`K` through the known smooth tower factors, or prove a direct trace formula
for `Tr_K(j)`.

## Lean Gate

The finite implication is now checked in:

```text
p24/lean/GlobalContentGate.lean
```

It proves abstractly that a nonzero scalar projection of each packet, or a
Bezout/content certificate, rules out every harmful all-zero packet.  The
Lean file deliberately leaves the arithmetic p-unit theorem as an input.

## Refined Complement Boundary

The complement trace is sharpened further in:

```text
p24/complement_trace_resolvent_boundary.md
p24/complement_trace_height_boundary.py
```

There `T(zeta_n^a)` is identified with the unique full class-character
resolvent in the harmful dual coset whose character is trivial on the
order-`m` complement subgroup.  This explains why complement `M_0` is cleaner
than arbitrary quotient moments in the small scans, and why selected-prime
zero would propagate through all `n` recovery conjugates.

The same note records the remaining boundary: even this `n`-fold propagation
does not make principal-dominance/height estimates strong enough to prove
p-unitness.
