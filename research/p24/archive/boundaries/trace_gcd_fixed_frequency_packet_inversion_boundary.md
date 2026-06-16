# Fixed-Frequency Packet-Inversion Boundary

Date: 2026-06-06

## Point

The class-character expansion reduces the order-7 target to

```text
sum_a L_a R_{-a} = 0,
L_a = T_{1,0,a},
R_{-a} = R_{chi,-a}.
```

The relative packet is stable under inversion `a -> -a`, so a tempting proof
is that Hermitian packet symmetry cancels the sum.  Finite algebra says this
is not automatic.

Pairing the terms gives

```text
L_a R_{-a} + L_{-a} R_a.
```

If the inversion symmetries have multipliers

```text
L_{-a} = alpha_a L_a,
R_a    = beta_a R_{-a},
```

then the paired contribution is

```text
(1 + alpha_a beta_a) L_a R_{-a}.
```

Ordinary Hermitian/inversion stability gives a paired structure, but
cancellation requires the extra anti-invariance

```text
alpha_a beta_a = -1.
```

If `alpha_a beta_a=1`, the contribution doubles instead of vanishing.

## Check

The finite boundary is:

```text
p24/trace_gcd_fixed_frequency_packet_inversion_boundary.py
```

It checks:

```text
random nonzero packets:
  all product terms nonzero and the sum nonzero;

inversion-even packets:
  all product terms nonzero and the sum still nonzero;

paired multiplier packets with alpha*beta=1:
  all product terms nonzero and the sum still nonzero;

anti-inversion packets with alpha*beta=-1:
  product terms nonzero but the paired sum vanishes;

termwise right-combo vanishing:
  the sum vanishes for the stronger obvious reason.
```

## Consequence

The p24 proof cannot stop at saying "the relative packet is inversion-stable"
or "the Hermitian pairing pairs `a` with `-a`."  The remaining theorem must
prove one of:

```text
1. an actual anti-invariance sign in the product packet;
2. termwise right-combo vanishing R_{chi,-a}=0;
3. a genuine packet cancellation not explained by inversion alone.
```

This keeps the target on the paired packet-cancellation theorem, not on a
generic Hermitian packet symmetry.
