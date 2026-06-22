# P27 Trace/Norm Dplus U6 Row-Bit H90 Factor Test

Date: 2026-06-22

## Claim

The descended Dplus `U6` row-bit cover does not split after adjoining the H90
elliptic quotient coordinate, at least in the `q=607` function-field test.

This is the nearest quotient explanation after the row-bit/resultant result:

```text
R(t,S) = Res_U5(F_A(X(t),U5), F_A(U5,S^2-2))
```

was irreducible over `Q(t)`.  The natural next question was whether it factors
over:

```text
E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1).
```

Online Magma says no over `F_607(t,w)`: the lift remains one irreducible
degree-32 factor.

## Artifacts

Magma fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_h90_factor_q607_magma.m
```

Online Magma output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_factor_q607_magma_20260622.xml
```

Command:

```bash
curl -L -sS -A 'Mozilla/5.0 Codex p27 research' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode input@research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_h90_factor_q607_magma.m \
  --max-time 120 \
  https://magma.maths.usyd.edu.au/xml/calculator.xml \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_h90_factor_q607_magma_20260622.xml
```

## Result

Magma output:

```text
RESULT u6_rowbit_factor_base 607 32 1
RESULT u6_rowbit_factor_K 32 1
RESULT u6_rowbit_factor_h90 607 1 2 32 1
RESULT u6_rowbit_factor_E 32 1
RESULT p27_trace_norm_dplus_u6_rowbit_h90_factor_q607 done
```

Interpretation:

```text
over F_607(t):         one degree-32 factor
over E_h90/F_607(t):   one degree-32 factor
E_h90 genus:           1
degree(E_h90 / F(t)):  2
```

So the H90 elliptic base does not split the `S^2=U6+2` row-bit cover in this
test.

## Consequence

This kills the nearest low-genus quotient shortcut:

```text
not only irreducible over Q(t),
but still irreducible after adjoining the named H90 elliptic quotient.
```

The remaining Dplus route is therefore not "factor the row bit over E_h90";
it is one of:

```text
1. find a non-obvious Prym/theta relation between the row bit and A_eta;
2. prove the row-bit Kummer class is generic/high-cost over the selected base;
3. use GPU only for fused/native Dplus pricing plus row-bit telemetry.
```

## Continue / Kill

```text
continue = Prym/theta comparison of row bit with A_eta
continue = second-layer branch-class obstruction or decomposition
continue = fused/native Dplus pricing with one row-bit column

kill = H90 elliptic-base factorization as the easy row-bit source
kill = branch-choice buckets after Dplus
kill = visible t/A/X branch atoms as row-bit sources
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_factor_rows=1/1
```
