# p25 Lane B Square-Axis Bridge Primitive Product Rigidity

Updated: 2026-06-12

## Result

The primitive `D`-coordinate bridge word is rigid as a trace-times-product
object.

In `C_12675`, the accepted bridge is exactly six full cosets of the unique
order-`25` subgroup.  Collapsing that `C_25` trace gives the signed quotient
word on `C_507`

```text
++: 121, 122, 123
---: 384, 385, 386
```

Enumerating every normalized signed `2 x 3` product on the collapsed quotient
finds only the two known presentations:

```text
forward = C25_trace * (1 - z^263) * z^121*(1 + z + z^2)
reverse = C25_trace * (1 - z^244) * -z^384*(1 + z + z^2)
```

There are `20` order-`25` trace generators in `C_12675`, but they all generate
the same subgroup.  Counting generator choices gives `40` raw trace-product
presentations, all the same forward/reverse bridge geometry.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_primitive_product_rigidity_gate.py
```

Expected row:

```text
square_axis_bridge_primitive_product_rigidity_rows=1/1
```

## Continue / Kill

Continue using the primitive coordinate as a positive producer target, but do
not treat it as opening a new family of short products.  A candidate arithmetic
producer still has to realize the same `C_25` trace, the same three-term
primitive `D` segment, and the same primitive bridge edge, up to reversal.

Kill proposed shortcuts that explain the word by changing the order-`25` trace
generator, by using a different signed `2 x 3` product on the collapsed
quotient, or by presenting the six quotient classes as an unrelated short
geometric product.
