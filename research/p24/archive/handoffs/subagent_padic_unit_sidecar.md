# p-adic Unit Sidecar For Hermitian Packets

This sidecar focuses only on the question:

```text
Can divisor, valuation, norm, or principal-ideal arguments prove the p24
Hermitian packet scalar is a p-unit at the selected split prime?
```

The short answer is: not with the currently identified structure.  There is
a clean p-unit theorem to aim at, but ordinary principal-dominance, splitting,
global norm, and divisor arguments do not currently distinguish the selected
prime above `p`.

## Exact Candidate Theorem

For the third p24 target:

```text
p = 10^24 + 7
h = 205880396014 = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
(n-1)/ord_n(p) = 8
```

For a representative `a` of a nontrivial relative-character Frobenius packet,
write

```text
P_u(a) = sum_k zeta_n^(a*k) j_{u+m*k}
u* = -u mod m
c(u) = (u+u*)/m
H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{u*}(a).
```

Let `E^+ = Q(zeta_n + zeta_n^-1)` and let

```text
M^+ = (E^+)^<p>.
```

For p24, `[E^+ : M^+] = 194215` and `[M^+ : Q] = 8`.  The sharp scalar
unit theorem is:

```text
Xi_a := Norm_{E^+/M^+}(H_a) is a p-unit at every prime of M^+ above p.
```

Equivalently:

```text
p does not divide Norm_{M^+/Q}(Xi_a).
```

Equivalently in finite-field packet language:

```text
H_a mod f_a != 0
```

for each of the eight real Frobenius packets.  This is a sufficient
certificate for the exact relative-content statement

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1.
```

This theorem is plausible as a target because the Hermitian scalar is
positive over `C`, survives all small packet scans so far, and has random
failure probability around `p^(-194215)` per packet.  It is not currently
proved by any divisor, norm, or principal-ideal argument we have.

## Why Principal Dominance Does Not Convert

The characteristic-zero principal-dominance theorem proves:

```text
H_a != 0 over C
```

with an enormous margin.  The audit gives:

```text
log_principal_lower = 5.076699e12
log_Hermitian_embedding_lower = 1.015340e13
```

But the certificate asks for:

```text
v_P(H_a) = 0
```

at a selected prime `P | p` in the class-field/cyclotomic compositum.

These are different questions.  The complex embedding where the principal
singular modulus dominates does not select a prime above a completely split
rational prime.  Choosing the reduction of the principal singular modulus
modulo `p` is already equivalent to choosing one embedded CM root modulo `p`.

The norm-height route also fails by scale.  For the Hermitian scalar:

```text
log_one_decomposition_prime_norm_bound = 1.971942e18
one_prime_bound_over_log_p = 3.568349e16
required_one_prime_height_reduction = 2.802417e-17
```

Thus even the norm to one degree-8 decomposition prime is far too large for a
"nonzero and smaller than p" argument.

The principal-ideal origin of Frobenius does not help either.  For each
target trace, the CM Frobenius element has norm `p`, so `p` splits completely
in the ring class field.  This makes Frobenius act as the identity on the
whole CM torsor.  It fixes every root; it does not choose an origin.

## Norm Versus Selected Prime Toy

The small split CM example `D=-87`, `q=103` gives a concrete warning.
PARI gives:

```text
H_D(x) = x^6 + 5321761711875*x^5 + ... + 549806430204864490157810211181640625
roots mod 103 = [5, 29, 32, 43, 60, 70]
```

Take the algebraic integer:

```text
alpha = j - 5.
```

Then:

```text
Norm_Q(alpha) = H_D(5)
              = 551979779199636057280288463250015625
```

This is a nonzero integer, but it is divisible by `103`.  At the selected
prime corresponding to the root `5`,

```text
alpha mod P_5 = 0.
```

At the selected prime corresponding to the root `29`,

```text
alpha mod P_29 = 24 != 0.
```

So the same global norm divisibility by `q` says only that some split prime
above `q` sees a zero.  It does not identify the selected prime.  Conversely,
nonzero characteristic-zero norm does not prevent a selected split-prime
zero.

For the exact finite-field packet norm, this ambiguity disappears inside one
packet:

```text
selected packet value zero  =>  packet norm zero.
```

But that is precisely why the useful theorem must be the decomposition-field
packet p-unit theorem above, not a full class norm or a principal-root
argument.

## Divisor Route Boundary

A divisor proof would need to identify `H_a` or `Xi_a` as the value of a
function whose divisor is controlled well enough to exclude the selected
ordinary CM point modulo `p`.

The current obstruction is structural:

```text
H_a is an additive Hermitian combination of high-order non-genus relative
periods, not a known modular unit or Borcherds product with explicit divisor.
```

Known product/intersection formulas control symmetric norms or divisors of
differences of singular moduli.  They erase the high-order relative phase.
The p24 scalar needs the phase retained through the order-`3107441` relative
characters and then through the degree-8 decomposition packet.

Thus a divisor proof would have to supply a new phase-aware divisor formula.
That would be essentially the missing theorem, not a consequence of existing
principal or norm data.

## Next Bounded Experiment

The next useful bounded experiment is not a larger p24 computation.  It is a
small split-CM valuation-distribution scan:

```text
For small cyclic split CM torsors and quotients h=m*n:
  compute Hermitian packet scalars H_a for every embedded root choice;
  compute packet norms and full class norms;
  record:
    selected_zero
    same_packet_norm_zero
    full_class_norm_zero
    zero_count_across_class_translates
```

Expected finite-field identities:

```text
selected_zero iff same_packet_norm_zero
full_class_norm_zero iff some class translate has selected_zero
```

The point is to measure whether Hermitian zeros, when they occur in toy
regimes, distribute like isolated selected-prime events or come in structural
suborbits.  A structural suborbit would suggest a divisor theorem.  Isolated
events would support the current conclusion: full norms are too coarse, and
the only serious certificate target is the packet p-unit theorem itself.

The bounded theorem statement to test against those rows is:

```text
For split ordinary CM rows with primitive odd relative quotient n and
Frobenius packet degree > 1, the Hermitian packet scalar has no zeros in any
selected packet.
```

This theorem is intentionally false if made too broad, but a counterexample
or a surviving range would tell us whether p24's high-order Hermitian
nonvanishing is behaving like a real arithmetic phenomenon or only a random
rarity.
