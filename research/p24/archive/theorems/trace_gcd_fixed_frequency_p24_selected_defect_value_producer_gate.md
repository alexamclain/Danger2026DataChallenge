# p24 Selected-Defect Value Producer Gate

Date: 2026-06-07

## Point

The value-side target can be stated one layer closer to the actual selected
packet.

Let `g(r,c)` be a raw post-`Tr_{B/C}` packet on:

```text
C_7 x C_179
```

and let the selected-child defect be:

```text
f(r,c) = g(r,c) - g(r,0).
```

Then:

```text
f(r,0)=0
```

is automatic.  The remaining value-side identities for `f` are equivalent to
two raw identities for `g`.

## Raw Producer Identities

### 1. Two-Level Inversion Complement

There are constants `A_0` and `A_1` such that:

```text
g(r,0) + g(-r,0) = A_0
g(r,c) + g(-r,-c) = A_1,  c != 0.
```

Then:

```text
f(r,c)+f(-r,-c)=A_1-A_0,  c != 0.
```

### 2. Selected Affine Row Balance

There is a constant `B` such that:

```text
sum_c g(r,c) - 179*g(r,0) = B
```

for every `r in C_7`.

This is exactly row-sum independence for the selected defect:

```text
sum_c f(r,c) = B.
```

## Consequence

The selected-packet theorem can now be targeted as:

```text
raw two-level inversion complement
+ selected affine row balance
=> selected defect satisfies the three value-side identities
=> admissible Jacobi span
=> verifier pipeline.
```

Controls show each piece is necessary:

```text
selected defect alone forces only f(r,0)=0;
raw inversion without affine balance leaks row sums;
raw affine balance without inversion leaks structural symmetry.
```

This is a more precise arithmetic target than "prove admissible span
membership."  It asks for a complement/product-formula law and an affine
selected-child row balance for the actual weighted raw packet.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.py
```

Observed:

```text
selected_defect_producer_equivalence=3/3
forced_raw_producer_hits=3/3
selected_defect_only_controls=3/3
inversion_only_controls=3/3
affine_only_controls=3/3
```

No p24 class set or CM root enumeration is used.
