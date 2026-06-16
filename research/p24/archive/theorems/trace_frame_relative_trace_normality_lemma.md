# Trace-Frame Relative Trace Normality Lemma

Date: 2026-06-06

This note isolates a formal normal-basis fact behind the decimated trace-frame
target:

```text
p24/trace_frame_decimated_period_certificate_target.md
```

It is not the missing CM p-unit theorem.  It says that the 31-term trace
periods themselves should not be the source of rank loss once the underlying
degree-5549 tensor factor has a normal generator.

## Formal Lemma

Let `B/E` be a cyclic Galois extension of degree:

```text
h*c
```

with generator `sigma`, and let `C = B^{<sigma^c>}` so:

```text
[B:C] = h
[C:E] = c.
```

If `theta` is normal in `B/E`, then:

```text
eta = Tr_{B/C}(theta)
    = sum_{j=0}^{h-1} sigma^(c*j)(theta)
```

is normal in `C/E`.

Indeed, if:

```text
sum_{t=0}^{c-1} a_t sigma^t(eta) = 0,
```

then after expanding `eta` this is a coset-constant relation among the
`h*c` conjugates of `theta`.  Normality of `theta` forces every coset
coefficient `a_t` to vanish.

## p24 Instantiation

For the current p24 tensor factor:

```text
E = F_p(mu_66254)
[B:E] = 5549 = 31*179
[B:C] = 31
[C:E] = 179
```

and:

```text
eta_t = Tr_{B/C}(theta^(a^t))
      = sum_{j=0}^{30} theta^(a^t * h_31^j),
0 <= t < 179.
```

So, conditional on `theta` being normal in `B/E`, the `179` periods
`eta_t` form an `E`-normal basis of `C`.

This turns each trace-frame coordinate:

```text
Tr_{B/C}(theta^i x_w)
```

into honest normal-basis coordinates in `C/E`; no extra rank loss is hidden in
the period trace basis.

## What Remains

The actual theorem is still the CM/axis statement:

```text
for every nonzero CRT-axis weight w,
  (Tr_{B/C}(x_w), Tr_{B/C}(theta*x_w), Tr_{B/C}(theta^2*x_w))
  != (0,0,0).
```

Equivalently:

```text
W_axis(B) cap span_C{1,theta,theta^2}^perp = {0}.
```

The normality lemma only says the target `C^3` coordinates are safe.  It does
not prove the smooth-axis CM periods avoid the trace annihilator.

## Toy Gate

The toy:

```text
p24/trace_frame_relative_trace_normal_basis_toy.py
```

checks two positive finite-field examples and two nonnormal controls:

```text
theta normal in B/E => Tr_{B/C}(theta) normal in C/E
nonnormal theta can give nonnormal relative traces
```

The p24 proof can use this lemma in either of two ways:

```text
1. prove or import normality of the selected n-root theta in the
   degree-5549 tensor factor over E;

2. bypass theta-normality and prove directly that the 179 relative Gaussian
   periods eta_t are normal over E.
```

Either route only clears the coordinate system.  The certificate still needs
the selected-prime Plucker/Schubert p-unit for the `368`-dimensional
CRT-axis image.
