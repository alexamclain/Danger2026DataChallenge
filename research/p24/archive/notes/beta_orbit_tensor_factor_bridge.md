# Beta Orbit Tensor-Factor Bridge

Date: 2026-06-05

This note connects two p24 surfaces that were previously recorded separately:

```text
trace-frame beta product:
  nonzero beta powers split over E=F_p(mu_m) into 560 Frobenius orbits;

tensor-factor axis certificate:
  each of the eight F_p H-packets splits over E into 70 degree-5549 factors.
```

They are the same finite-field decomposition.

## General Lemma

Let `n` be prime, let

```text
d = ord_n(p)
e = ord_m(p)
g = gcd(d,e)
E = F_p(mu_m) = F_{p^e}.
```

For one irreducible `F_p` H-packet factor

```text
f_a(X) = product_{c in <p>} (X - zeta_n^(a*c)),
deg f_a = d,
```

scalar extension to `E` gives

```text
F_p[X]/(f_a) tensor_Fp E
  ~= product_{i=1}^g B_{a,i},
[B_{a,i}:E] = d/g.
```

Equivalently, the `<p^e>`-orbits on `(Z/nZ)^*` refine each `<p>`-orbit into
exactly `g` pieces.  The proof is just the standard finite-field tensor
factorization:

```text
F_{p^d} tensor_Fp F_{p^e}
  ~= product_{gcd(d,e)} F_{p^lcm(d,e)}.
```

## p24 Counts

For the third trace:

```text
m = 66254 = 2*157*211
n = 3107441
ord_n(p) = 388430
ord_m(p) = 5460
gcd(388430,5460) = 70
ord_n(p^5460) = 5549
(n-1)/ord_n(p) = 8
(n-1)/ord_n(p^5460) = 560
```

Thus:

```text
8 F_p H-packets
70 E-tensor factors per H-packet
560 nonzero E-Frobenius beta orbits
```

and

```text
560 = 8 * 70.
```

The beta-orbit crossed-product factors in

```text
p24/trace_frame_trace_sum_crossed_product_boundary.md
```

are therefore not free-floating orbit factors.  They are exactly the
scalar-extension factors of the eight `F_p` H-packet algebras after adjoining
the `K`-character field `E`.

## Consequence For The P-Unit Route

For a selected H-packet `a`, the stronger beta-product theorem can be stated
factorwise:

```text
for i = 1,...,70:
  the crossed-product reduced norm R_{a,i} is a p-unit in E.
```

Equivalently, the packet product

```text
Delta_a = product_{i=1}^{70} R_{a,i}
```

is the `E`-scalar extension of the corresponding `F_p` packet resultant.
The eight-packet product is the decomposition-field packet norm surface from

```text
p24/decomposition_field_packet_norm_theorem.md
```

but now with the K-character tensor factors visible.

This sharpens the missing theorem:

```text
prove p-unitness of the trace-frame crossed-product reduced norms in the
70 scalar-extension factors of each selected p24 H-packet.
```

It does not prove p-unitness by itself.  Its value is that the beta-product
resultant, the one-factor trace-frame Plucker determinant, and the
decomposition-field packet norm now have the same indexing set.  A future
proof can attack one factor and use semilinear Frobenius symmetry, or attack
the 70-factor packet product, without enumerating `n=3107441` beta shifts.

## Verification

The accounting command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_decomposition_accounting.py
```

now reports:

```text
H_packet_count_over_Fp=8
E_Frobenius_orbit_size_on_H=5549
E_Frobenius_nonzero_orbit_count_on_H=560
E_orbits_per_H_packet=70
beta_orbit_count_matches_packets_times_tensor_factors=1
```

The small crossed-product toy in:

```text
p24/trace_frame_trace_sum_crossed_product_audit.py
```

has the same shape with `n=13`, one `F_q` H-packet, two `E`-tensor factors,
and two nonzero beta orbits of length `6`.

I then added a small multi-case wrapper:

```text
p24/beta_orbit_tensor_factor_bridge_audit.py
```

Bounded determinant command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/beta_orbit_tensor_factor_bridge_audit.py \
  --max-cases 2 --max-discriminants 5000 \
  --min-h 24 --max-h 220 --max-n 200 --max-m 48 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --target constant_plus_3
```

Calibrating on the pinned trace-frame row:

```text
D=-10919, q=11243, h=156, m=12, n=13
```

gave eight summarized determinant surfaces, all with:

```text
bridge_match=1
block_match_rows=orbit_rows
block_in_E_rows=orbit_rows
zero_block_rows=0
ordinary_power_fail_nonconstant=2
```

A bounded search for two additional compact rows found:

```text
D=-1559, q=2459, h=51, m=3, n=17
  packet_deg=16, E_deg=2, tensor_count=2, tensor_deg=8
  H_packets=1, E_orbit_size=8, E_orbits=2

D=-2207, q=2243, h=39, m=3, n=13
  packet_deg=12, E_deg=2, tensor_count=2, tensor_deg=6
  H_packets=1, E_orbit_size=6, E_orbits=2
```

For both rows and both proper subdegrees tested, the same summary held:

```text
bridge_match=1
zero_block_rows=0
ordinary_power_fail_nonconstant=2
```

So the crossed-product/tensor bridge is not an artifact of the pinned
`D=-10919` row.  The caveat is that these compact trace-frame rows have one
`F_q` H-packet; they test the tensor-factor refinement and orbit norm shape,
not the p24 eight-packet product.

For a separate multi-packet arithmetic sanity check, the old `D=-5000` toy
parameters:

```text
p=1259, m=6, n=5
```

give:

```text
H_packet_count_over_Fp=2
tensor_factor_count_over_E=2
E_Frobenius_nonzero_orbit_count_on_H=4
beta_orbit_count_matches_packets_times_tensor_factors=1
```

Here the tensor factors have degree `1`, so this row is too small for the
one-factor trace-frame determinant theorem.  It only checks the same
multi-packet orbit refinement.

## Boundary

The bridge rules out a bookkeeping ambiguity, not an arithmetic obstruction.
It does not imply:

```text
individual selected determinants are nonzero;
ordinary norm collapse on a beta orbit;
sparsity of the beta interpolant;
descent of the interpolant to E[Y].
```

Those shortcuts were already closed by the residual-tail and crossed-product
audits.  The remaining input is a genuinely CM-specific p-unit theorem for
the named scalar-extension/crossed-product norm factors.
