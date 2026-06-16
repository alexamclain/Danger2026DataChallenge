# Reduced Anchor Fingerprint Gate

Date: 2026-06-07

## Point

The reduced Jacobi packet changes only the raw value:

```text
U(0,0)=J(1,1)=q-2
```

by multiplying it by `(q-2)^(-1)`.  In additive/logarithmic notation this is
the raw correction:

```text
-e_(0,0).
```

The selected defect is:

```text
f(r,k)=g(r,k)-g(r,0).
```

Therefore the selected-defect contribution of the reduced anchor is exactly:

```text
h(r,k) = 1  if r=0 and k != 0,
h(r,k) = 0  otherwise.
```

This is the punctured right-zero row.

## Fingerprints

For `C_7 x C_c`, the anchor fingerprint has:

```text
support size = c-1;
row sums = (c-1,0,0,0,0,0,0);
Fourier profile H(a,0)=c-1 for every a;
Fourier profile H(a,b)=-1 for every a and b != 0.
```

So the anchor fingerprint alone leaks the forbidden
`C_7^nontrivial x {C/E trivial}` bidegrees.  It is not an admissible packet by
itself; it must cancel the matching degenerate leak of the raw punctured
Jacobi packet.

Its cyclic right difference has only two nonzero rows:

```text
Delta_0 = -punctured_C_row,
Delta_6 =  punctured_C_row,
Delta_i = 0 otherwise.
```

This is the exact additive shape that should be compared with the older
right-difference/adjacent-anchor descent route.

## p24 Consequence

For p24, `c=179`, so the selected CM/Lang anchor unit must supply:

```text
178 nonzero selected-defect entries,
Fourier values H(a,0)=178 and H(a,b)=-1,
two adjacent right-difference punctured rows.
```

The remaining theorem is no longer just "find an anchor."  It is:

```text
show that the selected trace-GCD/CM-Lang anchor contributes this exact
punctured right-zero row after Tr_{B/C} and selected-child subtraction.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.py
```

Observed:

```text
anchor_selected_defect_rows=6/6
anchor_fourier_profile_rows=6/6
anchor_forbidden_c_trivial_leak_rows=6/6
anchor_right_difference_profile_rows=6/6
p24_anchor_nonzero_entries=178
```

No finite-field Jacobi sums, p24 class-set enumeration, or CM roots are used.
