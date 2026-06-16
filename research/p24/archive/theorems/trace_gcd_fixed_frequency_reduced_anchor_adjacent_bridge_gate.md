# Reduced Anchor / Adjacent Anchor Bridge

Date: 2026-06-07

## Point

The reduced Jacobi anchor fingerprint is two-dimensional:

```text
h(r,k)=1  if r=0 and k != 0,
h(r,k)=0  otherwise.
```

The older adjacent-anchor descent route sees only the `C/E`-trivial slice,
i.e. row sums over `k`.  For the reduced anchor this slice is:

```text
A=(c-1)e_0 on C_7.
```

So the correct composition is not:

```text
whole punctured row = adjacent anchor.
```

It is:

```text
adjacent anchor = invertible right difference of the reduced anchor's
C/E-trivial row-sum leak.
```

## Exact Finite Bridge

With Fourier convention:

```text
hat A(a)=sum_r A(r) zeta_7^(ar),
Delta A(r)=A(r+1)-A(r),
```

we have:

```text
hat A(a)=c-1                for every a,
hat DeltaA(a)=(zeta_7^(-a)-1) hat A(a).
```

Thus:

```text
hat A(a) != 0 for a=1,...,6;
zeta_7^(-a)-1 != 0 for a=1,...,6.
```

The adjacent-difference operator is invertible on all six nonfixed right
channels.  Therefore the old adjacent-anchor descent theorem is exactly the
requirement that this `b=0` reduced-anchor leak cancel against the raw packet's
opposite `b=0` leak.

## Consequence

This bridge splits the remaining theorem cleanly:

```text
punctured Hasse-Davenport:
  supplies the nonzero right-row product identities;

selected degenerate anchor unit:
  supplies the full punctured right-zero row;

row-sum / adjacent bridge:
  identifies the C/E-trivial part of that row with the old adjacent-anchor
  descent obstruction.
```

The bridge does not prove the CM/Lang unit exists.  It says exactly which part
of that unit the previous covariance/telescope machinery was already asking
for.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.py
```

Expected markers:

```text
b0_slice_matches_row_sum_rows=6/6
anchor_b0_forbidden_leak_rows=6/6
adjacent_difference_multiplier_rows=6/6
adjacent_difference_nonfixed_invertible_rows=6/6
anchor_diff_telescope_rows=6/6
opposite_raw_leak_cancel_rows=6/6
mismatched_anchor_leak_control_rows=6/6
p24_anchor_b0_nontrivial_projectors=6
```
