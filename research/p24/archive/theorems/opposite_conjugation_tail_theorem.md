# Opposite-Conjugation Tail Theorem

This note isolates the finite algebra behind the opposite-pair refinement of
the p24 mixed Hermitian certificate.

## Statement

Work in the full cyclotomic product algebra for the mixed block, not in one
chosen irreducible right factor:

```text
F_p[mu_157, mu_211].
```

Let

```text
H(u,v) = H_{157,211}(u,v)
```

be the mixed Hermitian DFT entry.  Since the kernel entries lie in `F_p`, the
inversion map

```text
iota(mu_157)=mu_157^-1,
iota(mu_211)=mu_211^-1
```

satisfies

```text
iota(H(u,v)) = H(-u,-v).
```

For p24,

```text
-1 = p^78 mod 157,
```

so the left inversion is already a Frobenius automorphism of the left field

```text
L = F_p(mu_157).
```

On the right side, `-1` is not in the `p`-Frobenius orbit modulo `211`, so
inversion swaps the six right factors:

```text
O1 <-> O4,
O2 <-> O5,
O3 <-> O6.
```

Choose opposite-pair tail windows in Lang coordinates so that the window in
`O_{-v}` is the direct negation of the chosen window in `O_v`.

Then each opposite pair has equivalent tail injectivity:

```text
tail(O_v) injective on the shared prefix kernel
  <=> tail(O_{-v}) injective on the same shared prefix kernel.
```

The finite implication is formalized in:

```text
p24/lean/ConjugateTailGate.lean
```

## Why the Lang Window Matters

Raw DFT seed inversion gives

```text
H(1,p^k v) -> H(-1,-p^k v).
```

Because `-1 = p^78 mod 157`, the raw seed row contains the semilinear right
shift `T^78`.  For a right orbit of length `35`, this is an index shift by

```text
78 mod 35 = 8.
```

But the Lang trivialization writes a seed row as

```text
seed = U*w,
```

where `T U = U sigma`.  Hence

```text
T^a(seed) = U*sigma^a(w).
```

The shift becomes coordinatewise Frobenius on Lang coordinates; it does not
move the coordinate index.  This is why the correct tail windows are the
direct negation windows in Lang coordinates, not the raw shifted seed
positions.

The convention is audited by:

```text
p24/opposite_conjugation_window_audit.py
```

with p24 output:

```text
left_neg_shift=78
left_neg_shift_mod_right_orbit=8
pair=O1/O4 direct_negation_positions=[9,...,24]
pair=O1/O4 raw_seed_after_left_positions=[1,...,16]
lang_shift_coordinate_mismatches=0
```

## Certificate Consequence

The opposite-pair manifest is:

```text
deleted O1/O4 share B={O2,O3,O5,O6}, tails O4/O1
deleted O2/O5 share B={O1,O3,O4,O6}, tails O5/O2
deleted O3/O6 share B={O1,O2,O4,O5}, tails O6/O3
```

Each prefix set is stable under `iota`.  Therefore the six tail conditions
fall into three opposite-conjugate pairs once compatible Lang windows are
used.

The finite certificate surface can therefore be stated as:

```text
3 opposite-prefix p-units B,
3 representative opposite-tail p-units T,
the inversion/Lang compatibility theorem above.
```

This is a genuine compression of the arithmetic proof surface from `3B+6T`
to `3B+3T`, but it does not prove those six representative p-units.

## Remaining Arithmetic Theorem

After also applying right-unit equivariance, recorded in

```text
p24/right_unit_equivariance_theorem.md
```

the remaining p24-specific theorem is:

```text
For the actual embedded p24 mixed Hermitian periods, one representative
leading Moore determinant L=B*T is nonzero modulo p = 10^24 + 7.
```

Equivalently, all named leading residual products are p-units in the full
cyclotomic product algebra, after quotienting by the inversion and right-unit
symmetries.

That is still a class-field p-unit theorem for named CM periods.  It is the
next object that must be proved to finish the strict sub-sqrt certificate.

The opposite-stable prefixes also suggest a Hermitian Gram determinant
certificate for the three `B` factors.  This is recorded in:

```text
p24/opposite_prefix_gram_boundary.md
```

The boundary is important: over finite fields, a full-rank prefix row space
can have singular restricted Hermitian Gram form.  Thus a Gram p-unit would be
a stronger sufficient certificate for `B`, not an equivalent restatement.
