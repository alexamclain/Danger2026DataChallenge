# Fixed-Frequency H-Coboundary Base-Field Boundary

Date: 2026-06-06

## Base-Field Form

Let

```text
C(r,s),     1 <= r < 157, 1 <= s < 211,
```

be the `156 x 210` centered mixed Hermitian marginal matrix:

```text
C(r,s) = M(r,s) - M(r,0) - M(0,s) + M(0,0).
```

The centered right profile is:

```text
G_s = sum_r zeta_157^r C(r,s) in F_p(mu_157).
```

Since the nonzero powers of `zeta_157` are an `F_p`-basis of
`F_p(mu_157)`, the order-7 H-coboundary theorem is equivalent to the
base-field row identities:

```text
sum_{s in qH} C(r,s) = 0
```

for every left row `r` and every multiplicative coset `qH`, where:

```text
H = <2^7> <= (Z/211Z)^*,     |H| = 30.
```

So the missing p24 theorem can be stated without adjoining either `mu_157` or
`mu_211`:

```text
the seven multiplicative Gaussian-period column sums of C vanish row-wise.
```

This is exactly the additive Hilbert-90 condition:

```text
G_s = Y_s - Y_{2^7 s}.
```

## Boundary

Ordinary right centering only says the total sum over all `210` nonzero right
columns is zero.  It does not force the seven H-coset sums to vanish.

A pinned actual-CM analogue also rejects this as a generic packet symmetry:

```text
D=-13319, q=13463, h=140, m=28, n=5,
left=4, right=7.
```

For the right quotient with two cosets, the centered marginal has:

```text
h_coset_sums=[[9224,9029], [9165,1536], [3467,9584]]
h_coset_sum_zero_entries=0/6
h_coset_sum_rank=2
```

Thus the p24 theorem, if true, is a specific selected-prime Gaussian-period
marginal identity, not a consequence of ordinary centering, full rank, or
generic CM Hermitian packet structure.

## Check

The finite dictionary and pinned actual-CM boundary are checked by:

```text
p24/trace_gcd_fixed_frequency_h_coboundary_basefield_boundary.py
```

It verifies:

```text
H-coset row sums vanish
  <=> row-wise additive Hilbert-90 potential exists;

ordinary centering
  does not imply H-coset row sums vanish;

pinned actual-CM analogue
  has nonzero H-coset row sums.
```
