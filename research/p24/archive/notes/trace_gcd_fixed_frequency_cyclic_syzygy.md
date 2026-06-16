# Fixed-Frequency Cyclic Syzygy Gate

Date: 2026-06-06

## Point

The no-fixed-defect theorem currently asks for seven fixed-frequency
relations:

```text
V_{a,1} in span(V_{a,2}, V_{a,3}, V_{a,5}, V_{a,6}),
    a in 5Z/35Z.
```

Since

```text
p = 10^24 + 7 = 1 mod 7,
```

the seven fixed frequencies are base-rational on the `7`-part.  Therefore
the seven relations can be packaged as one cyclic module syzygy over:

```text
R_7 = F_p[y] / (y^7 - 1).
```

## Cyclic Form

Let `P_2(y), P_3(y), P_5(y), P_6(y)` be the vector-valued fixed-frequency
prefix sections, and let `T(y)` be the tail section.  The packaged theorem is:

```text
T(y)
  = C_2(y) P_2(y)
  + C_3(y) P_3(y)
  + C_5(y) P_5(y)
  + C_6(y) P_6(y)
      in R_7 tensor L.
```

Evaluating at the seven roots of `y^7-1` gives the seven primal relations.
Conversely, because `p = 1 mod 7`, any seven pointwise coefficient lists
interpolate to coefficients in `R_7`.

## Why This Helps

The finite packaging by itself is not proof: pointwise post-fit coefficients
always interpolate in this split case.  The arithmetic target is to construct
the sections `C_j(y)` intrinsically from the CM/Lang fixed map, or prove the
dual annihilator inclusion in a way that produces this cyclic syzygy.

The prefix Plucker p-unit remains a separate condition:

```text
rank(P_2(a), P_3(a), P_5(a), P_6(a)) = 4
```

at all seven fixed frequencies.  A cyclic tail-in-prefix syzygy alone only
removes fixed defect lines; it does not prove fixed frequencies are ordinary
unless the prefix ranks are also p-units.

## Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_cyclic_syzygy_toy.py
```

It checks:

```text
seven pointwise tail-in-prefix relations
  <=> one cyclic R_7 syzygy;

one failed fixed relation
  blocks the cyclic syzygy;

tail-in-prefix can hold even when a prefix Plucker gate fails;

post-fit interpolation is finite algebra, not arithmetic proof.
```

## Next Arithmetic Target

Construct the cyclic coefficients:

```text
C_2(y), C_3(y), C_5(y), C_6(y) in R_7
```

from the CM/Lang trace-adjoint identity, without enumerating the class set.
