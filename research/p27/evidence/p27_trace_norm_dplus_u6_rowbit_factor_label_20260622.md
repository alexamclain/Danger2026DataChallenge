# P27 Trace/Norm Dplus U6 Row-Bit Factor Label Probe

Date: 2026-06-22

## Claim

The Dplus `U6` row-bit factor split has a more concrete label structure than
the raw degree counts show.

Over the `eta=+1` `A_eta` cover, each degree-8 factor is fixed by
`S -> -S`, so it is a quartic in:

```text
Y = S^2 = U6 + 2.
```

The `rho -> -rho` paired products multiply exactly back to the two
domain-spin degree-16 factors.  Thus the row-bit split is a two-stage Kummer
split:

```text
domain-spin: 32 -> 16 + 16
Aeta:        each 16 -> 8 + 8
```

This gives a concrete next test: extract the quartic factor label and compare
that label to pulled-back A-level `d3=chi(x6)` and later selected gates.

## Artifacts

Fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_factor_label_q607_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_label_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_label_q1607_local_magma_20260622.txt
```

Command:

```bash
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_factor_label_q607_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_label_q607_local_magma_20260622.txt
```

The q1607 guard used the same fixture with `q := 1607`.

## Results

Both q607 and q1607 agree:

```text
domain factors:        2 factors, degrees [16,16]
Aeta factors:          4 factors, degrees [8,8,8,8]
domain factors even:   [true,true]
Aeta factors even:     [true,true,true,true]
rho permutation:       [2,1,4,3]
pair [1,2] -> domain factor 1
pair [3,4] -> domain factor 2
each Aeta factor:      quartic in Y=S^2
```

Coefficient profile for the four Aeta quartics is also stable in q607/q1607.
Flattening coefficients in the basis

```text
1, w, z, w*z, rho, rho*w, rho*z, rho*w*z
```

gives:

```text
factor  coeff Y^0   nonzero basis 1   max numerator degree 16   max denominator degree 8
factor  coeff Y^1   nonzero basis 6   max numerator degree 12   max denominator degree 8 or 10
factor  coeff Y^2   nonzero basis 7   max numerator degree 10   max denominator degree 6 or 8
factor  coeff Y^3   nonzero basis 6   max numerator degree 4    max denominator degree 6 or 8
factor  coeff Y^4   nonzero basis 1   max numerator degree 0    max denominator degree 0
```

The two rho-paired factor pairs have the slightly lower denominator profile;
the other pair has the `+2` denominator-degree shift.  The shape is otherwise
identical across q607 and q1607.

## Interpretation

Positive:

```text
The Aeta split is not an opaque degree-8-in-S split.
It descends to a quartic label in Y=U6+2.
The factor pairs are exactly the domain-spin factors, so the split tower is
structured and reproducible.
The coefficient degrees are moderate and field-stable in q607/q1607.
```

Negative:

```text
The quartic coefficients still live in the Aeta function field, not on a
visible base coordinate.
This is not yet a direct GPU sampler or a sqrt-beating source.
The visible H90/domain-spin/Aeta product-character and visible u-line divisor
routes remain killed.
```

## Next Concrete Tests

CAS extraction:

```text
derive the field-independent quartic factor formula in Y over
F(t,w,z,rho), preferably normalized as G(Y) + rho*H(Y);
compute the remaining w/eta cross-action between eta=+1 and eta=-1 labels;
compute discriminant/resolvent/norm classes of the quartic label;
compare the resulting Kummer class with pulled-back A-level d3=chi(x6).
```

GPU/telemetry test, only after a cheap label formula exists:

```text
on same-stream Dplus rows, emit the domain factor label, Aeta quartic label,
d3,d4,d5, and raw source denominators;
promote only if factor labels predict a later selected gate or recur with
source-normalized lift beyond independent half-loss;
kill if the factor labels split d3/d4/d5 flat after heldout normalization.
```

## Continue / Kill

```text
continue = exact quartic-label formula over the Aeta cover
continue = resolvent/discriminant/norm class of the quartic label
continue = compare factor labels to A-level d3/x6 and later gates
continue = bounded GPU telemetry only after CAS supplies a cheap label

kill = treating the factor label as visible on t,u,A without extraction
kill = treating the degree split alone as a sampler
kill = retrying low-weight visible H90/Aeta product buckets
```

```text
p27_trace_norm_dplus_u6_rowbit_factor_label_rows=1/1
```
