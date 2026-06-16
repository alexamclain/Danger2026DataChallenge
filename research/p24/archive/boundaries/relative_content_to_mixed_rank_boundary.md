# Relative Content To Mixed Rank Boundary

Date: 2026-06-05

This note records the relationship between the surviving relative-content
route and the current mixed Hermitian rank target.

## Surviving Relative-Content Statement

The broad product theorem failed:

```text
Res(Phi_n, J_u) != 0 for every coordinate u
```

is false even for prime `n`; see:

```text
p24/prime_relative_normality_counterexample.md
```

The stronger exact-content and Hermitian scalar checks have survived the
selected-prime scans:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1
```

and the phase-aware Hermitian scalar is nonzero in the tested windows; see:

```text
p24/packetized_content_selected_prime_scan.md
```

## Mixed Rank Is Stronger

The live mixed target can be stated by the centered right profile:

```text
G_s^0 in L = F_p(mu_157),     s mod 211,
span_Fp{G_s^0 : s mod 211} = L.
```

Relative content is a nonzero-packet statement.  In Fourier/profile language
it can at best say that certain right-frequency packets are not identically
zero.  It does not force the values `G_s^0` to span `L`.

Added:

```text
p24/content_vs_mixed_rank_boundary_toy.py
```

The toy constructs a rank-one profile over `F_13` whose nonzero right
Fourier components are all nonzero:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/content_vs_mixed_rank_boundary_toy.py
```

Output:

```text
nonzero_right_frequency_count=5/5
profile_span_rank=1/5
all_nonzero_right_frequencies=1
mixed_full_rank=0
```

So:

```text
nonzero packet content does not imply centered-profile full span.
```

This is a theorem-shape boundary, not CM evidence.  It prevents promoting a
surviving content p-unit into the mixed rank certificate without a new
linear-independence input.

## Useful Reformulation

The content route can still help if it is strengthened to a frame theorem:

```text
the centered right profile values G_s^0 have subspace polynomial
A_G(X) = X^(p^156) - X.
```

Equivalently, some centered-profile Moore minor is a p-unit:

```text
det((G_{s_j}^0)^(p^i))_{0<=i,j<156} != 0.
```

This is a valid sufficient certificate for the mixed marginal rank
`rank_Fp C_{157,211}=156`.  It is not identical to the current representative
leading-erasure p-unit `L_rep`; the Fourier transform between centered
profile values and right-orbit Lang coordinates is invertible on the full
210-dimensional right side, but it does not preserve a chosen leading minor.

Thus there are now two finite p-unit surfaces:

```text
1. representative leading-erasure p-unit L_rep:
   stronger, proves delete-one/right-support >= 2 and hence full rank;

2. centered-profile Moore p-unit:
   enough for full mixed marginal rank, but does not by itself prove
   delete-one support.
```

Either would beat sqrt scaling if supplied with a selected p24 arithmetic
proof.  The centered-profile surface may be better for class-field/lattice
arguments because it avoids choosing a right trace-dual basis.

## Current Lesson

The exact-content scans remain useful evidence for nonvanishing of packet
scalars.  They do not close the p24 mixed rank theorem.  The missing theorem
must prove a spanning/frame statement:

```text
the 211 centered right-profile values are not contained in any proper
F_p-subspace of F_p(mu_157),
```

or the stronger representative erasure statement already encoded by
`L_rep`.
