# Complement Trace Resolvent Boundary

This note sharpens the complement-section moment from
`relative_moment_projection_theorem.md`.

## Algebraic Identification

For the third p24 target,

```text
h = m*n,
m = 66254,
n = 3107441,
gcd(m,n) = 1.
```

Let

```text
G = <g> ~= C_h,
H = <g^m>,       |H| = n,
K = <g^n>,       |K| = m.
```

The complement section writes every class as

```text
i = n*r + m*k,       0 <= r < m, 0 <= k < n.
```

The complement trace polynomial is

```text
T(X) = sum_k Y_k X^k,
Y_k = sum_r j_{n*r + m*k}.
```

For a nontrivial `H`-character `a`, choose the unique full character index
`s mod h` satisfying

```text
s == 0 mod m,
s == a mod n.
```

Equivalently,

```text
s = m * (a * m^(-1) mod n).
```

Then

```text
T(zeta_n^a)
  = sum_{r,k} zeta_n^(a*k) j_{n*r+m*k}
  = sum_i zeta_h^(s*i) j_i
  = R_s.
```

So complement `M_0` is not merely a moment projection.  It is one full
class-character/Lagrange resolvent in the harmful dual coset, namely the one
whose character is trivial on the complement subgroup `K`.

## Why It Certifies Relative Content

The harmful dual-coset lemma says that a packet is harmful iff every full
resolvent in the coset

```text
a + Q_H
```

vanishes.  Since `R_s` is one member of that coset, a single nonzero
complement trace resolvent rules out the harmful packet.

Thus the scalar certificate

```text
Res(Phi_n, T) != 0 mod p
```

is sufficient for all eight nontrivial p24 relative packets.

This is weaker than full reduced normality and weaker than prime augmentation
normality:

```text
full reduced normality:         every class-character resolvent nonzero
prime augmentation normality:   every fiber J_u has all primitive H-resolvents nonzero
complement trace:               one K-trivial resolvent per H-character packet nonzero
exact content:                  at least one resolvent in each harmful coset nonzero
```

The complement trace is still stronger than exact content, because exact
content allows all K-trivial resolvents to vanish as long as some other
resolvent in the same dual coset survives.

## Characteristic-Zero Dominance

The complement resolvent contains the principal singular modulus with
coefficient `1`.  Every other singular modulus has reduced-form denominator
at least `2`.  The audit

```text
p24/complement_trace_height_boundary.py
```

reports:

```text
log_principal=5.076699e+12
log_all_other_crude=2.538350e+12
dominance_margin=2.538350e+12
dominance_margin_over_log_p=4.593297e+10
```

Therefore the complement resolvent is nonzero in characteristic zero for
every nontrivial `H`-character.

## p-Adic Propagation

Because the character is trivial on `K`, the resolvent lies in the degree-`n`
fixed field `L^K` after adjoining `mu_n`.  Under `H`, it is an eigenvector:

```text
g^m(R_s) = zeta_n^(-a) R_s.
```

So if the selected finite-field value of `R_s` is zero at one prime over the
chosen cyclotomic prime, then all `n` conjugate primes over that cyclotomic
prime also see zero.  Over one Frobenius packet of `mu_n`, the selected zero
propagates to

```text
n * ord_n(p) = 3107441 * 388430 = 1207023307630
```

split prime factors.

The same audit reports:

```text
one_embedding_pdiv_log=n*log_p=1.717235e+08
packet_pdiv_log=n*ord_n_p*log_p=6.670257e+13
```

This is a real strengthening compared with a scalar that does not propagate
through the recovery subgroup.

## Why Height Still Does Not Prove p-Unitness

The archimedean norm room is still much larger:

```text
one_embedding_norm_upper_log=n*log_principal=1.577554e+19
packet_norm_upper_log=n*ord_n_p*log_principal=6.127695e+24
one_embedding_room_ratio=9.186594e+10
packet_room_ratio=9.186594e+10
```

Thus even the `n`-fold and Frobenius-packet divisibility forced by a selected
zero is not contradictory.  The gap is essentially

```text
log(|j_principal|) / log(p).
```

So the complement trace improves the algebraic packaging, but it does not
turn principal dominance into a p-unit proof.

## Multi-Splitting-Prime Experiments

I extended

```text
p24/relative_moment_projection_scan.py
```

with

```text
--max-splitting-primes
--section complement
```

to test more than the first splitting prime for each small CM discriminant.

Three splitting primes per case, no origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 20 --min-h 12 --max-h 90 --max-abs-D 12000 \
  --max-prime-quotients 4 --max-composite-quotients 4 \
  --min-n 3 --max-n 80 --q-stop 200000 \
  --max-splitting-primes 3 --include-linear \
  --max-moment-degree 1 --section complement --summary-only
```

Output:

```text
packet_rows=175
content_failures=0
moment_histogram={'0': 175}
moment0_failures=0
expected_moment0_failures_random=0.142331
```

The matched contiguous-section run had:

```text
packet_rows=231
moment_histogram={'0': 230, '1': 1}
moment0_failures=1
expected_moment0_failures_random=0.187433
```

Three splitting primes plus origin rotations:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --max-cases 12 --min-h 12 --max-h 80 --max-abs-D 8000 \
  --max-prime-quotients 4 --max-composite-quotients 4 \
  --min-n 3 --max-n 60 --q-stop 120000 \
  --max-splitting-primes 3 --include-linear \
  --max-moment-degree 1 --section complement --scan-origins --summary-only
```

Output:

```text
packet_rows=1967
content_failures=0
moment_histogram={'0': 1967}
moment0_failures=0
expected_moment0_failures_random=0.959426
```

The matched contiguous-section run had:

```text
packet_rows=2483
moment_histogram={'0': 2480, '1': 3}
moment0_failures=3
expected_moment0_failures_random=1.455270
```

The complement trace remains cleaner than an arbitrary section in these
bounded tests.  The sample is still small; the point is not a statistical
proof, but that the clean behavior now aligns with a genuine class-field
resolvent.

## Counterexamples to a Universal `M0` Theorem

A wider bounded scan found that the single complement trace scalar is not
universally nonzero, even for prime recovery length.  I pinned one observed
failure in:

```text
p24/complement_m0_failure_toy.py
```

It reports:

```text
D=-899
q=281
h=14
m=2
n=7
factor=X + 32
residues=['-69', '69']
content_zero=0
M0=0
M1=69
```

So the exact relative-content vector is nonzero, but the K-trivial complement
resolvent cancels.  The next moment `M1` detects the packet.

An even smaller row reproduces the same failure mode:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_moment_projection_scan.py \
  --only-D -216 --min-h 1 --max-h 10 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 2 --max-n 6 --q-start 103 --q-stop 104 \
  --include-linear --max-moment-degree 1 --section complement
```

Output summary:

```text
D=-216 q=103 h=6 m=2 n=3 n_prime=1 deg=1
first_nonzero_moment=1
content_failures=0
moment0_failures=1
moment01_failures=0
```

Thus a broad theorem of the form

```text
Tr_K(j) has all nontrivial H-character resolvents nonzero modulo every split p
```

is false.  The clean p24 theorem, if true, must use the special high-order
selected prime and target packet, or the exact content vector rather than only
the `K`-trivial scalar.

## Current Boundary

The best single-scalar theorem target is now p24-specific:

```text
For the p24 third trace, the K-trivial order-n class-character resolvent
R_s = Tr_K(j) evaluated at every nontrivial H-character Frobenius packet is a
p-unit at the selected split prime.
```

Equivalently:

```text
Res(Phi_3107441, T) != 0 mod p.
```

If proved, this rules out every harmful relative packet with one resultant.

What remains is still substantial:

```text
1. prove the selected-prime p-unit theorem for this resolvent;
2. construct the degree-3107441 quotient trace polynomial without enumerating
   the full class set;
3. construct the relative degree-66254 recovery relation from Tr_K(j) to j.
```

The end-to-end algebra and the dense-relation boundary are recorded in:

```text
p24/complement_trace_recovery_relation.md
p24/complement_trace_recovery_toy.py
p24/complement_trace_recovery_complexity_scan.py
```

The toy construction verifies the quotient/recovery degrees, but the
interpolated recovery relation is dense of size `m*n=h` in small CM data.
Thus a successful p24 proof must construct the embedded relation in compressed
or tower form, not by dense interpolation.

This is a sharper embedded class-field tower target, not yet the final
certificate.
