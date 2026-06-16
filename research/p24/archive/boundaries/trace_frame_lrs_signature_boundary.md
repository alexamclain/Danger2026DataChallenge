# Trace-Frame LRS Signature Boundary

Date: 2026-06-05

This note records a bounded check for visible LRS/MSRD structure in the
relative coefficient code from the trace-frame route.

## Question

The sum-rank strengthening views the p24 axis image as:

```text
W_axis(B) subset C^31
```

over `E=F_p(mu_m)`, with block size `dim_E C = 179`.

If this code were visibly LRS/MSRD in the natural relative coefficient basis,
small analogues might show:

```text
low Toeplitz/Hankel/cyclic displacement rank,
special block rank patterns,
non-random pair-block behavior,
or another rigid generator-matrix signature.
```

## Audit

I added:

```text
p24/tensor_factor_relative_block_structure_audit.py
```

It builds the small relative coefficient generator matrix and compares:

```text
individual block ranks,
pair block ranks,
flattened Toeplitz/Hankel/cyclic displacement ranks,
random matrices with the same shape over E.
```

Pinned `D=-10919, m=12` axis analogue, `subdegree=2`:

```text
rows=6
cols=6
block_rank_hist={2: 3}
pair_rank_hist={4: 3}
displacement={toeplitz:6,hankel:6,cyclic_toeplitz:6,cyclic_hankel:6}

random_controls:
  rank_hist={6:80}
  block_rank_hists={((2,3),):80}
  pair_rank_hists={((4,3),):80}
  all displacement histograms {6:80}
```

For the other intermediate subfield, `subdegree=3`:

```text
rows=6
cols=6
block_rank_hist={3: 2}
pair_rank_hist={6: 1}
displacement={toeplitz:6,hankel:6,cyclic_toeplitz:6,cyclic_hankel:6}

random_controls:
  rank_hist={6:80}
  block_rank_hists={((3,2),):80}
  pair_rank_hists={((6,1),):80}
  all displacement histograms {6:80}
```

## Interpretation

The natural relative coefficient generator matrix looks random under these
simple LRS/MSRD signatures.  This demotes the off-the-shelf route:

```text
identify obvious low-displacement / Toeplitz / Hankel / cyclic structure
```

as a proof strategy.

It does **not** rule out a hidden LRS/MSRD equivalence.  Such an equivalence
could require class-field-dependent block transformations.  But that is now
the right burden:

```text
prove an explicit p-unit block equivalence to an LRS/MSRD code,
or prove the selected top-three Schubert/Plucker coordinate is a p-unit.
```

The second target remains the smaller certificate surface.
