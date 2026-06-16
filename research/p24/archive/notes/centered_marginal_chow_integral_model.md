# Centered Marginal Chow Integral Model

Date: 2026-06-06

This note isolates the p-integral determinant-line object behind the centered
cyclic consecutive-arc theorem.  It is not the p-unit theorem; it identifies
the exact Schubert/Chow section whose orbit norm a phase-aware proof must
construct.

## Ambient Hyperplane

Let

```text
H = {w in F_p^211 : w_0 = 0}.
```

The centered point columns have `P_0=0`, so the dual centered row space

```text
W_C = {lambda(P_b)}_{b mod 211}
```

lies in `H`.  For p24:

```text
dim H = 210,
dim W_C = 156.
```

For a cyclic window

```text
I_t = {t, t+1, ..., t+156} mod 211,
```

define the centered plateau subspace:

```text
B_t = {w in H : w is constant on I_t}.
```

Since the condition `w_0=0` is already imposed, one checks:

```text
dim B_t = 54,
dim W_C + dim B_t = 210 = dim H.
```

The window determinant

```text
Delta_C(t) = det(P_{t+1}-P_t, ..., P_{t+156}-P_t)
```

is nonzero if and only if:

```text
W_C cap B_t = {0}.
```

Thus `Delta_C(t)` is a complementary Schubert/Chow determinant on
`Gr(156,H)`.

## Integral Lattice

Let `O_p` be the localization of the relevant ring-class/cyclotomic integer
ring at the selected ordinary prime above:

```text
p = 10^24 + 7.
```

The levels `2`, `157`, `211`, `66254`, and `3107441` are all p-units, so the
coordinate hyperplane `H`, the cyclic translations, and the plateau quotient
lattices have p-integral models.

Let:

```text
Lambda_C subset H_{O_p}
```

be the p-integral lift of the centered row space.  For each `t`, let
`Lambda_{B,t}` be the p-integral lattice in the plateau subspace `B_t`.

## Chow Section

Choose p-integral bases:

```text
w_1,...,w_156 of Lambda_C,
b_1,...,b_54 of Lambda_{B,t},
e_1,...,e_210 of H_{O_p}.
```

Define:

```text
Chow_t(W_C,B_t)
  = det(w_1,...,w_156,b_1,...,b_54) / det(e_1,...,e_210).
```

Equivalently, this is the determinant-line pairing:

```text
det(Lambda_C) tensor det(Lambda_{B,t}) -> det(H_{O_p}).
```

Changing any compatible basis multiplies this scalar by:

```text
det(GL_156(O_p)) * det(GL_54(O_p)) * det(GL_210(O_p))^{-1},
```

hence by a p-unit.  Therefore:

```text
Chow_t is a p-unit
```

is independent of basis and volume-form choices.

## Relation To Delta_C(t)

The usual determinant `Delta_C(t)` is the same Schubert pairing after using
the quotient basis of:

```text
H / B_t
```

given by the 156 window differences:

```text
e_{t+i} - e_t,       1 <= i <= 156.
```

The transition from this quotient basis to any p-integral determinant-line
basis has p-unit determinant because all entries are `0`, `1`, and `-1`.
Thus:

```text
Delta_C(t) = u_t * Chow_t(W_C,B_t),
u_t in O_p^*.
```

For a right Frobenius orbit `O`:

```text
Pi_O = prod_{t in O} Delta_C(t)
     = u_O * prod_{t in O} Chow_t(W_C,B_t),
u_O in O_p^*.
```

So the seven centered orbit-product payloads are equivalently seven
Schubert/Chow orbit norms.

## What Remains

This model proves denominator hygiene only.  The missing arithmetic theorem
is still:

```text
prod_{t in O} Chow_t(W_C,B_t) is a p-unit at the selected ordinary prime
above p, for all seven right Frobenius orbits O.
```

Equivalently:

```text
the p24 centered CM row space avoids every translated plateau Schubert
divisor modulo p.
```

The finite handoff is checked in:

```text
p24/lean/CenteredBorcherdsPUnitGate.lean
p24/lean/CenteredArcProductGate.lean
```

The phase-aware target is:

```text
p24/centered_marginal_phase_borcherds_target.md
```

The current negative audits show that this Chow norm is not explained by the
easy dictionaries:

```text
p24/centered_marginal_phase_unit_span_boundary.md
p24/centered_marginal_global_product_mining_boundary.md
p24/centered_plateau_lang_support_boundary.md
```

Therefore the remaining proof must construct this exact centered
Schubert/Fitting determinant section, or prove its seven orbit norms are
p-units by another selected-prime arithmetic argument.
