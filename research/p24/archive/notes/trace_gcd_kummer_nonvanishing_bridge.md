# Trace-GCD Kummer Nonvanishing Bridge

Date: 2026-06-05

This note records the finite Kummer bridge that could support the direct
`f_trace` construction route, and the exact missing determinant theorem.

## Linear Cyclic Layer

For a prime cyclic relative layer of degree `r`, child periods above one
parent are:

```text
y_u,       u in Z/rZ.
```

Their relative character traces are the DFT values:

```text
T_s = sum_u zeta_r^(s*u) y_u.
```

Equivalently, for:

```text
F(Y) = sum_u y_u Y^u,
```

one has:

```text
F(zeta_r^s) = T_s.
```

For primitive `s`, the Kummer powers:

```text
K_s = T_s^r
```

are invariant under cyclic relabeling of the child periods.  Thus:

```text
K_s != 0  =>  T_s != 0  =>  F(zeta_r^s) != 0.
```

This is useful for p-unit/nonvanishing even though Kummer orbit norms are not
enough to reconstruct a selected child chain.

## Toy

Added:

```text
p24/relative_kummer_nonvanishing_bridge_toy.py
p24/lean/KummerNonvanishingGate.lean
```

The toy uses the `D=-5000`, `h=30=2*3*5` calibration tower with relative
degree `3`.  It reports:

```text
parent=0:
  direct_values_match_traces=1
  all_traces_nonzero=1
  all_kummer_powers_nonzero=1
  nonvanishing_bridge_ok=1

parent=1:
  direct_values_match_traces=1
  all_traces_nonzero=1
  all_kummer_powers_nonzero=1
  nonvanishing_bridge_ok=1

synthetic_zero_control:
  children=[1,1,1]
  primitive_kummer_zero_detected=1
```

The Lean gate checks only the finite implication:

```text
trace_i = 0 => K_i = 0,
K_i != 0 for all i
  => trace_i != 0 for all i.
```

## p24 Use If the Determinant Factors

The p24 trace-GCD finite object is:

```text
f_trace(Y) = det_Q(P V_univ A),
Pi_right = prod_{t mod 211} f_trace(zeta_211^t).
```

If the producer theorem can express each evaluation

```text
f_trace(zeta_211^t)
```

as a p-unit multiple of a relative character trace, or as a determinant whose
zero is detected by finitely many relative Kummer powers, then Kummer p-units
would imply the 211-term trace-GCD certificate.

This gives a precise theorem shape:

```text
determinantal Kummer zero-detection theorem:
  f_trace(zeta_211^t)=0
    => at least one named primitive relative Kummer power
       in the 157/211 tower data is zero.
```

Together with p-unitness of those Kummer powers, this would prove
`Pi_right != 0`.

## Caveat: Kummer Data Does Not Automatically Kill Determinants

The current mixed trace-GCD determinant is not a raw child-period DFT.  It is
a `16 x 16` tail-on-kernel determinant built from mixed Hermitian resolvent
pairings:

```text
S_j = H_{157,211}(1,v_j) = <A_1, B_{v_j}>.
```

The determinant can vanish by cancellation even when all visible primitive
resolvent traces are nonzero.  Therefore the Kummer nonvanishing bridge is
not yet a p24 proof.  It becomes a proof only after one proves a structural
factorization or zero-detection statement for the determinant section itself.

The finite insufficiency of coordinatewise Kummer nonzero is recorded in:

```text
p24/kummer_coordinate_nonzero_det_boundary_toy.py
p24/trace_gcd_kummer_determinant_boundary.md
```

The missing theorem is now sharper:

```text
Express f_trace, or its Fitting ideal, in relative Kummer/resolvent
coordinates so that determinant failure forces a Kummer p-unit failure.
```

Without this theorem, relative Kummer powers remain selected-chain phase data
and linear-layer p-unit witnesses, not a certificate for the trace-GCD
Schubert determinant.

## Next Experiment

The right small-scale experiment is not a broad search.  It is to take an
actual small trace-GCD row, compute:

```text
1. the reduced determinant sequence Delta(t);
2. the relative right-character/Kummer coordinates B_v for the same row;
3. the ideal or rank relation between Delta(t)=0 and those Kummer coordinates.
```

A successful pattern would be an exact zero-detection identity.  Merely seeing
all quantities nonzero is only evidence, not a certificate theorem.
