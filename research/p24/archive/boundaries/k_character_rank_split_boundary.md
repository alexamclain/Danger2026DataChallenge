# K-Character Rank Split Boundary

This note records what happens when the complement `K` roots of unity are
already in the base field of a small CM packet.

## Setup

For packet elements

```text
F_r mod f,      0 <= r < m,
```

full relative `K`-normality is F_q-linear independence of these `m` elements
in `F_q[X]/(f)`.

If

```text
m | q-1,
```

choose a primitive `m`th root `zeta_m in F_q` and form the `K`-character DFT:

```text
G_s = sum_r zeta_m^(s*r) F_r,      0 <= s < m.
```

The DFT matrix is invertible, so

```text
rank{F_r} = rank{G_s}.
```

In the split-character toy, all objects live over the base field `F_q`, so
this is ordinary `F_q`-rank.  For p24, where `mu_m` is not in the base packet
field, the analogous statement must be interpreted after tensor scalar
extension.  It is not the same as embedding the packet field into one larger
field and treating the `G_s` as scalars.

The toy

```text
p24/scalar_extension_rank_pitfall_toy.py
```

shows the distinction:

```text
single_embedding_rank_over_E=1
tensor_extension_rank_over_E=2
```

This separates:

```text
character support:  every G_s is nonzero;
character rank:     the G_s are linearly independent.
```

The second is the Moore/full-rank theorem.  The first is only nonvanishing of
the individual full class-character resolvents.

A related packet-field warning is recorded in

```text
p24/packet_field_dft_rank_warning_toy.py
```

If the DFT coefficients live in the packet field rather than the base field,
the coordinate transform can be invertible over the packet field while changing
the base-field span of the coordinate entries.  Thus packet-field
diagonalization is structural evidence, not a substitute for the Moore/tensor
rank statement.

## Scan

I added:

```text
p24/k_character_rank_split_scan.py
```

Broad split-character window:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/k_character_rank_split_scan.py \
  --max-cases 40 --min-h 12 --max-h 140 --max-abs-D 40000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 140 --max-m 60 \
  --q-stop 500000 --max-splitting-primes 16 \
  --include-linear --summary-only
```

Output:

```text
packet_rows=1422
dimension_possible_rows=628
dimension_bound_rows=794
full_rank_rows=628
rank_defect_rows=794
dimension_possible_rank_defect_rows=0
zero_character_rows=0
rank_defect_with_full_character_support_rows=794
dimension_possible_rank_defect_with_full_character_support_rows=0
```

Origin-scanned split-character window:

```text
packet_rows=2894
dimension_possible_rows=1541
dimension_bound_rows=1353
full_rank_rows=1541
rank_defect_rows=1353
dimension_possible_rank_defect_rows=0
zero_character_rows=0
rank_defect_with_full_character_support_rows=1353
dimension_possible_rank_defect_with_full_character_support_rows=0
```

Known low-order reduced-normality failures:

```text
D=-216, q=103:
  packet_rows=3
  dimension_possible_rows=0
  zero_character_rows=1
  rank_defect_with_full_character_support_rows=2

D=-300, q=139:
  packet_rows=3
  dimension_possible_rows=0
  zero_character_rows=1
  rank_defect_with_full_character_support_rows=2
```

So the diagnostic does detect the old low-order character vanishings, but they
all live in dimension-bound degree-1 packet rows.

## Interpretation

Every tested `K`-character resolvent was nonzero:

```text
zero_character_rows=0.
```

When `deg(f) < m`, rank defects occur for the obvious dimension reason even
though every `G_s` is nonzero.  This proves that character nonvanishing alone
is not the same as full rank.

When `deg(f) >= m`, no rank defect appeared:

```text
dimension_possible_rank_defect_rows=0.
```

So in the tested CM rows, the only obstruction to full `K`-rank in split
character coordinates was the dimension bound.

## p24 Relevance

For the p24 target,

```text
deg(f_a)=388430 > m=66254,
```

so the dimension obstruction is absent.  But `mu_m` is not contained in the
base packet field: the p24 axis audit found

```text
ord_157(p)=156,
ord_211(p)=35,
ord_m(p)=5460.
```

Thus the split-character diagnostic is a toy model for the extension where
`K`-characters diagonalize.  The p24 proof still needs a selected-prime
statement that the full class-character resolvents are independent after
descent to the actual packet field.

The sharp proof target is therefore not merely:

```text
all full class-character resolvents are nonzero.
```

It is:

```text
the full K-character resolvents have rank m over the K-character splitting
field, equivalently the Moore determinant in the packet field is nonzero.
```
