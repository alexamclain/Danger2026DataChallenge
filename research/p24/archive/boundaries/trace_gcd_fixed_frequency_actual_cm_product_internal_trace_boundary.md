# Actual-CM Product/Internal-Trace Boundary

This is the sharper actual-CM boundary for the product-coboundary route.

The p24 packet has weighted product shape:

```text
sum_a T_left(a) * R_right(a).
```

The pinned calibration uses:

```text
D = -13319
q = 13463
h = 140
m = 28 = 4 * 7
n = 5
```

The relative `n=5` layer has two `E`-internal Frobenius orbits for
`q^ord_m`, and one recombined `<q>` orbit.  For the actual weighted product
analogue, both internal traces and the recombined trace are nonzero:

```text
internal_q_order=2
product_terms_all_nonzero=2/2
product_internal_trace_zeroes=0/2
recombined_q_order=4
recombined_product_trace_zeroes=0/1
product_full_projection_zero=0
```

So the theorem cannot be:

```text
weighted product packet shape
  => internal trace zero.
```

Nor can it be the recombined/decomposition-field variant:

```text
weighted product packet shape
  => Tr_{K_n/K_n^<q>}(packet) = 0.
```

The p24 proof must use the specific weighted `G_chi` packet, the 211-axis
H-coset equality, or an explicit CM/Lang potential for that packet.
