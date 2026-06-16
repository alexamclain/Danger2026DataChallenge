# Relative Kummer Orbit-Norm Boundary

Date: 2026-06-05

This note separates two uses of Kummer phase data:

```text
selected-chain reconstruction;
p-unit / nonzero orbit-norm certification.
```

## Question

For a prime child layer, relative Kummer powers

```text
K_s = T_s^r
```

come in Frobenius orbits.  For p24:

```text
157 layer: one orbit of size 156
211 layer: six orbits of size 35.
```

Can a norm over one Frobenius orbit replace the whole orbit in the
selected-chain certificate?

## Toy Audit

The script:

```text
p24/relative_kummer_orbit_norm_toy.py
```

uses the `D=-5000`, `h=30=2*3*5` calibration tower.  The child degree is
`3`, and the primitive Kummer power `K=T_1^3` lies in `F_{1259^2}`.

For each parent, the script fixes:

```text
T_0 = parent trace,
Norm_{F_{q^2}/F_q}(K),
```

then enumerates every `K'` with that norm and checks whether some cube root
of `K'` descends by inverse DFT to an `F_q` child polynomial.

Results:

```text
parent=0:
  norm_candidate_count=1260
  norm_descending_polynomial_count=210
  trace_norm_candidate_count=2
  trace_norm_descending_polynomial_count=1

parent=1:
  norm_candidate_count=1260
  norm_descending_polynomial_count=210
  trace_norm_candidate_count=2
  trace_norm_descending_polynomial_count=1
```

So the orbit norm alone leaves many fake selected-child polynomials.  In the
quadratic orbit toy, trace plus norm identifies the Frobenius pair and hence
the child polynomial; norm alone does not.

## Consequence

For selected-chain reconstruction, one must carry enough orbit data to
identify the Kummer powers, e.g. the orbit/minimal-polynomial data or explicit
Frobenius representatives.  A single norm value per orbit is not enough.  In a
multi-orbit layer such as p24's `211` layer, even the independent Kummer
orbits need cross-orbit phase glue before they select a child polynomial.

For p-unit routes, orbit norms remain useful:

```text
Norm(K_s) != 0
```

proves that every conjugate in that orbit is nonzero.  But this is a
nonvanishing certificate surface, not an embedded child-polynomial producer.

Thus:

```text
selected-chain producer:
  needs Kummer orbit data;

p-unit producer:
  may use Kummer orbit norms if nonzero Kummer powers imply the required
  determinant/content condition.
```

The second implication is arithmetic and route-specific; it is not automatic
from the Kummer normal form alone.
