# Trace-Frame Toeplitz Support Boundary

Date: 2026-06-05

This note measures the symbol support of the selected cyclic Toeplitz minor:

```text
det(c_{r-s})_{r in R, s in S_axis}
```

where:

```text
R = {0,...,367}
S_axis subset Z/66254Z
```

is the smooth-axis frequency set.

## Audit

I added:

```text
p24/trace_frame_toeplitz_support_audit.py
```

It reports:

```text
rows=368
cols=368
entries=135424
distinct_offsets=66254
offset_density=66254/66254
max_offset_multiplicity=3
```

So the selected matrix touches every symbol position in `Z/66254Z`, and no
symbol value appears more than three times:

```text
no symbol value appears more than 3 times in the selected matrix.
```

Componentwise, the `211` block is the only block with systematic adjacent
overlap at this window size, because:

```text
66254/211 = 314 < 368,
66254/157 = 422 > 368.
```

The audit also builds the column interval-overlap graph.  It records many
small overlaps and, crucially:

```text
column_overlap_component_count=1
column_overlap_component_sizes=[368]
```

so the overlap graph is connected.  There is no disjoint support product
decomposition.

## Consequence

The selected Toeplitz minor is not close to a small repeated-symbol determinant
or an obvious block product.  It uses the full `m`-periodic symbol, with only
low-multiplicity repetitions coming from nearby CRT-axis frequencies.

This closes another structural shortcut:

```text
exploit heavy symbol repetition or clean support block factorization.
```

The determinant remains a high-dimensional selected skew-Schur/Toeplitz
noncancellation theorem for the actual CM symbol.  Any proof must use
arithmetic p-unit structure, not just combinatorial sparsity of the selected
matrix.

The finite verifier surface exposed by this support audit is recorded in:

```text
p24/trace_frame_selected_minor_certificate_spec.md
p24/trace_frame_selected_minor_certificate_accounting.py
```

It uses the full length-`66254` symbol to reconstruct the selected matrix.
This is useful for selected-origin verification, but literal beta-orbit
symbols are too large; beta coverage still needs a reduced-norm or
class-field identity.
