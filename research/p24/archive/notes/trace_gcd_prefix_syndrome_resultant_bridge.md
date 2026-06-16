# Trace-GCD Prefix Syndrome / Resultant Bridge

Date: 2026-06-06

## Point

The newest prefix-only certificate and the two-resultant certificate are the
same determinant-line story with one extra tail test.

The prefix syndrome/Moore theorem proves that the four full prefix blocks have
rank `140`.  Since

```text
L = F_p(mu_157),       dim_Fp L = 156,
```

this is equivalent to a `16`-dimensional residual kernel.  The representative
two-resultant theorem then asks whether the selected `16` tail coordinates are
nonsingular on that kernel.

## Finite Linear Algebra

Let

```text
C_prefix = c_1,...,c_140 in L
T_tail   = t_1,...,t_16 in L.
```

Write

```text
A_prefix : L -> F_p^140,
lambda |-> (Tr_{L/F_p}(lambda c_i))_i.
```

By trace-pairing nondegeneracy:

```text
A_prefix is surjective
  <=> dim_Fp span(C_prefix) = 140.
```

When this holds,

```text
K_prefix = ker(A_prefix)
```

has dimension `16`.  The selected representative `140+16` determinant is
nonzero exactly when

```text
lambda |-> (Tr_{L/F_p}(lambda t_i))_i
```

is injective on `K_prefix`.

Equivalently:

```text
span(C_prefix, T_tail) = L
  <=> span(C_prefix) has dimension 140
      and T_tail separates ker(A_prefix).
```

## Resultant Language

Let `P_prefix` be the monic p-linearized annihilator of
`span(C_prefix)`.  For each tail coordinate, the quotient-tail element is

```text
P_prefix(t_i).
```

The representative tail resultant is the Moore determinant

```text
Delta_16(P_prefix(t_1),...,P_prefix(t_16)).
```

Thus the p24 representative theorem can be stated as the conjunction:

```text
1. Norm(Delta_140(C_prefix)) is a p-unit;
2. Norm(Delta_16(P_prefix(T_tail))) is a p-unit.
```

The first item is exactly the prefix syndrome/Moore certificate.  The second is
the fixed-orbit linearized trace-GCD resultant on the `16`-dimensional residual
kernel.

## Why This Matters

This bridge keeps two nearby proof obligations separate:

```text
prefix syndrome surjectivity
  => residual kernel has the expected dimension 16;

tail resultant p-unit
  => the selected tail window kills no nonzero residual vector.
```

The prefix theorem alone is not enough for the full `140+16` representative
determinant.  Conversely, a full representative determinant p-unit implies both
the prefix and quotient-tail p-units through the Moore/Chow split.

This is the correct handoff to the two-resultant surface:

```text
Xi_O0 = Res_p-lin(P_K0,T_0),
Xi_O1 = Norm_O1(Res_p-lin(P_Kt,T_t)).
```

## Cheap Gate

The finite equivalences and failure modes are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_syndrome_resultant_bridge_toy.py
```

The finite handoff is also Lean-checked in:

```text
p24/lean/TraceGcdPrefixSyndromeResultantBridgeGate.lean
```

The toy has forced controls for:

```text
good prefix and good tail;
dependent prefix;
good prefix but bad tail;
good prefix with only one tail direction.
```
