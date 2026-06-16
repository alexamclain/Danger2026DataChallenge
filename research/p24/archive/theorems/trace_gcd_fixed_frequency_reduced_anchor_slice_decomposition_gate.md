# Reduced Anchor C-Slice Decomposition

Date: 2026-06-07

## Point

The reduced-anchor fingerprint is:

```text
h(r,k)=1  if r=0 and k != 0,
h(r,k)=0  otherwise.
```

The adjacent-anchor bridge accounts for only the `C/E`-trivial row-sum slice.
This note splits:

```text
h = h_triv + h_nontriv
```

where `h_triv` is constant in the `C/E` coordinate on each right row, and
`h_nontriv` has row sums zero.

## Exact Profiles

For `C_7 x C_c`:

```text
h_triv Fourier:
  H(a,0)=c-1
  H(a,b)=0      for b != 0

h_nontriv Fourier:
  H(a,0)=0
  H(a,b)=-1     for b != 0
```

Spatially, on the right-zero row:

```text
h_nontriv(0,0)=-(c-1)/c
h_nontriv(0,k)=1/c       for k != 0
h_nontriv(r,k)=0         for r != 0
```

Thus `h_nontriv` is invisible to the old adjacent-anchor theorem: its row sums
and all `b=0` Fourier coefficients vanish.  The old bridge handles the
`b=0` leak; it does not realize the full punctured row.

## p24 Consequence

For p24, `c=179`.

```text
old adjacent bridge:
  handles 6 nonfixed right b=0 projector channels

remaining full-anchor realization:
  7*(179-1)=1246 C/E-nontrivial Fourier channels
```

This is the exact shape of the next CM/Lang unit theorem:

```text
construct a p-integral selected degenerate-anchor unit whose selected defect
has both the b=0 row-sum slice and this C/E-nontrivial residual slice.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.py
```

Expected markers:

```text
slice_reconstruction_rows=6/6
c_trivial_slice_profile_rows=6/6
c_nontrivial_slice_profile_rows=6/6
c_nontrivial_rowsum_zero_rows=6/6
c_nontrivial_spatial_formula_rows=6/6
old_adjacent_anchor_invisible_c_nontrivial_rows=6/6
full_remaining_nontrivial_channel_rows=6/6
p24_remaining_c_nontrivial_fourier_channels=1246
```
