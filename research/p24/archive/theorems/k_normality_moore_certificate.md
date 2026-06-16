# K-Normality Moore Certificate Shape

This note records a basis-free certificate form for the relative `K`-normality
parent theorem.

## Packet Elements

For a packet factor `f_a | Phi_n`, write

```text
A_a = F_p[X]/(f_a),        deg(f_a)=d=388430.
```

For the p24 third trace,

```text
m = 66254 < d,
```

and the complement-section fibers give packet elements

```text
beta_r = F_r(zeta_a) in A_a,       0 <= r < m.
```

Full relative `K`-normality is:

```text
beta_0, ..., beta_{m-1}
are F_p-linearly independent in A_a.
```

## Moore Determinant

This is equivalent to nonvanishing of the Moore determinant

```text
Delta_a =
det( beta_r^(p^s) )_{0 <= r,s < m}
in A_a.
```

Since

```text
beta_r^(p^s) = F_r(zeta_a^(p^s)),
```

the determinant only uses the Frobenius packet orbit of the `H`-character.
A scalar finite-field certificate is:

```text
Norm_{A_a/F_p}(Delta_a) != 0.
```

This is the basis-free version of the coefficient-rank check in

```text
p24/l1_axis_injectivity_scan.py.
```

## Coefficient Minor

Choosing the power basis `1,X,...,X^(d-1)` of `A_a`, the same theorem can be
proved by any nonzero `m x m` coefficient minor.  The most optimistic shape is
the leading minor

```text
det( j_{n*r + m*k} )_{0 <= r,k < m} != 0 mod p,
```

because the coefficient of `X^k` in `F_r(X)` is `j_{n*r+m*k}`.

Small CM scans found that when full `K` rank is dimensionally possible, the
pivot prefix is very small:

```text
broad eligible window:   full_k_pivot_prefix_max=4
larger targeted window:  full_k_pivot_prefix_max=7
```

This does not prove the p24 leading minor is nonzero, but it suggests a
possible concrete certificate surface:

```text
provide m coefficient positions S with det(coeff_S(F_r)) != 0.
```

The leading choice `S={0,...,m-1}` would be especially clean if it can be
proved.

## Failure Consequence

A full `K`-rank failure is equivalent to the existence of a nonzero weight
vector

```text
w = (w_0,...,w_{m-1}) in F_p^m
```

such that

```text
sum_r w_r F_r(X) == 0 mod f_a.
```

Equivalently, if

```text
A_w(X) = sum_{k=0}^{n-1} (sum_r w_r j_{n*r + m*k}) X^k,
```

then

```text
f_a | A_w.
```

This is a structured low-dimensional annihilator:

```text
W_axis failure:  w lies in the 368-dimensional axis space;
full K failure:  w is arbitrary in F_p^m.
```

In Moore language, a failure gives a nonzero Frobenius-linear dependence among
the `beta_r`; equivalently the selected packet span has dimension `< m`.

## K-Character Transform

After adjoining `mu_m`, the `K`-coordinate DFT gives full class-character
resolvents

```text
G_s = sum_r zeta_m^(s*r) beta_r.
```

The DFT matrix is invertible after scalar extension.  Therefore the Moore
determinant theorem can also be phrased as:

```text
the m full K-character resolvents are linearly independent in the tensor
extension A_a tensor_{F_p} E, where E contains mu_m.
```

This is a scalar-extension statement.  It is not the same as choosing one
embedding `A_a -> E'` and viewing the `G_s` as scalars in a single field;
that would make the rank at most one.

The warning and split-character boundary are recorded in

```text
p24/scalar_extension_rank_pitfall_toy.py
p24/packet_field_dft_rank_warning_toy.py
p24/k_character_rank_split_boundary.md
```

Individual nonvanishing of every `G_s` is weaker than rank.  Small split-
character CM windows found no dimension-possible rank defects once every
character resolvent was nonzero, but dimension-bound rows show that support
alone is not a formal replacement for the Moore determinant.

There is also a coordinate-transform warning for partial character axes.  If
the relevant roots of unity lie in the packet field, the transform is
invertible over that packet field, but it need not preserve the `F_p`-span of
the coordinate entries.  The formal certificate must therefore remain a
base-field rank statement, or the equivalent tensor/Moore scalar-extension
statement.

The finite transform logic is Lean-checked in

```text
p24/lean/AxisInjectivityGate.lean
```

via `injective_iff_precompose_bijection`: precomposing an evaluation map with
an invertible transform preserves injectivity in both directions when the
source and target rank statement live over the same scalar field.  For p24
character language, that means base-field transforms or the tensor scalar
extension, not a single packet-field embedding.

## p24 Hierarchy

The proof hierarchy is now:

```text
Moore determinant Delta_a nonzero for all eight packets
  <=> full relative K-normality
  => axis injectivity on W_axis
  => L1 packet nonvanishing
  => exact packet content / harmful collapse ruled out.
```

The Moore determinant may be the cleanest arithmetic theorem statement.  The
axis theorem remains the smaller construction/certificate target.
