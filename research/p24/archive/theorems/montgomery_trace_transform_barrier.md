# Montgomery Trace Transform Barrier

This note checks a possible hypergeometric shortcut.  The trace of the
Montgomery family

```text
E_A: y^2 = x^3 + A x^2 + x
```

has the exact convolution form

```text
t(A) = - sum_c chi(c^2 - 4) chi(A + c).
```

Thus `A -> t(A)` is a finite-field trace function.  If this sequence had a
sparse additive transform, unusually concentrated low frequencies, or a stable
low-order multiplicative structure in the near-square rows `p=n^2+7`, one
could hope to target the strict trace residue without first selecting a CM
root.

The additive transform is now identified more sharply.  For
`psi(x)=exp(2*pi*i*x/p)` and `h != 0`,

```text
T(h) = sum_A t(A) psi(-hA)
     = - chi(-h) G(chi) Kl(-4, -h^2/4),

Kl(a,b) = sum_{y != 0} psi(a*y + b/y).
```

So additive sparsity would require many exact zeros of a one-parameter
Kloosterman family, not merely a hidden short Fourier basis.

## Audit

I added:

```text
p24/montgomery_trace_transform_audit.py
```

and reran the existing bucket-spectrum probes with the bundled NumPy runtime:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/montgomery_trace_transform_audit.py \
  --min-p 10000 --max-p 120000 --max-rows 6 --n-modulus 8 --n-residue 0

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/additive_spectrum_trace_bucket.py \
  --min-p 10000 --max-p 120000 --max-rows 6 --n-modulus 8 --n-residue 0

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/multiplicative_spectrum_trace_bucket.py \
  --min-p 10000 --max-p 90000 --max-rows 4 --n-modulus 8 --n-residue 0
```

## Results

For the full trace sequence, every tested row had full additive support:

```text
nonzero_spectrum = p-1 of p-1
```

The direct Kloosterman identity check on the same six near-square rows reported
relative error below `2.8e-11`:

```text
p=14407: kloosterman_identity_max_relative_error=4.161e-12
p=18503: kloosterman_identity_max_relative_error=1.123e-11
six-row max: 2.710e-11
```

The energy was not concentrated in a small number of frequencies.  Across six
rows:

```text
top16_energy median   = 0.002556
top64_energy median   = 0.010083
top256_energy median  = 0.039016
low32_energy median   = 0.002899
low128_energy median  = 0.010744
```

The accepted strict bucket also looked random-sized in additive spectrum:

```text
max Fourier peak / sqrt(good) ~= 3.8 to 4.1
low_energy(|h|<=32) median ~= 0.0027
low_energy(|h|<=128) median ~= 0.0100
```

Low-order multiplicative cosets in `A` and in Montgomery `j` produced only
unstable constant-factor lifts.  A few rows have visible small-order `j`
cosets, but they do not persist as a growing selector across rows.

## Boundary

The convolution formula is still useful for exact small-field experiments and
constant-factor diagnostics.  It does not provide a sub-sqrt p24 construction
unless one can exploit a p-specific transform identity much stronger than the
ordinary finite-field hypergeometric representation.

In current evidence:

```text
full trace transform: full support;
strict bucket transform: random-sized peaks;
low-frequency/residue labels: constant-factor only;
low-order multiplicative labels: unstable constants.
```

So the hypergeometric/Montgomery trace-function route collapses to the same
trace oracle barrier: computing the target trace class is easy by full
convolution at small p, but no sublinear selector is visible.
