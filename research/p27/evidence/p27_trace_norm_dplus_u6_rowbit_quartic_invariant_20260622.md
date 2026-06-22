# P27 Trace/Norm Dplus U6 Row-Bit Quartic Invariant

Date: 2026-06-22

## Claim

The Dplus `U6` row-bit quartic label has a visible A-line resolvent root.

For the Aeta quartic factor in

```text
Y = S^2 = U6 + 2
```

the quartic is irreducible over the Aeta field, its discriminant is nonsquare,
but its cubic resolvent factors as:

```text
linear * irreducible quadratic
```

and the linear resolvent root is exactly:

```text
16 - 8*A
```

where the Dplus A-coordinate is:

```text
A = (t - 1/t)^4/4 - 2.
```

Thus the quartic-label pairing is not arbitrary: the first resolvent is already
the A-line bridge.  The remaining obstruction is the nonsquare quadratic
resolvent discriminant over the Aeta field.

## Artifacts

Fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q607_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q1607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q1847_local_magma_20260622.txt
```

Command:

```bash
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q607_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_quartic_invariant_q607_local_magma_20260622.txt
```

The q1607 and q1847 guards used the same fixture with the field constant
substituted.

## Results

The invariant profile is stable in q607, q1607, and q1847:

```text
quartic in Y factorization:                 irreducible degree 4
quartic discriminant square:                false
quartic discriminant rho-norm square:       true
cubic resolvent factorization:              degree 1 + degree 2
linear resolvent root:                      16 - 8*A
quadratic resolvent discriminant square:    false
cubic resolvent discriminant square:        false
```

Degree/complexity profile:

```text
quartic discriminant:                 nonzero basis 8, max deg 68/33
quartic discriminant rho-norm:         nonzero basis 4, max deg 136/66
linear resolvent root:                 nonzero basis 1, max deg 8/4
quadratic resolvent discriminant:      nonzero basis 8, max deg 24/12
cubic resolvent discriminant:          nonzero basis 8, max deg 68/33
```

The root check is explicit in all three fields:

```text
RESULT cubic_resolvent_linear_root_matches_16_minus_8A true
```

## Interpretation

Positive:

```text
The first resolvent of the row-bit quartic label descends all the way to the
A-line coordinate.
This directly bridges the Dplus/H90 row-bit lane to the A-level Kummer lane.
The residual obstruction is now a named quadratic resolvent discriminant,
not an opaque quartic factor.
```

Negative:

```text
The quartic itself is still irreducible over Aeta.
The quartic discriminant and residual quadratic resolvent discriminant are
nonsquares in q607/q1607/q1847.
This is not yet a sampler or a production GPU mode.
```

## Consequence

The next concrete test is:

```text
extract the residual quadratic resolvent discriminant Delta_res;
normalize it as a Kummer class over the Aeta/domain-spin tower;
compare chi(Delta_res) to pulled-back A-level d3=chi(x6), d4, d5 on
same-stream Dplus rows;
promote only if Delta_res is the same class, a coboundary, or a recurrent
later-gate class.
```

If `Delta_res` is independent of the A-level selected gates, this row-bit
factor lane becomes a structural obstruction rather than a sqrt-beating source.
If it equals or recurs with an A-level gate, it becomes the first serious
candidate for compounding beyond independent half-loss.

## Continue / Kill

```text
continue = derive/export the residual quadratic resolvent discriminant formula
continue = compare Delta_res with pulled-back A-level d3/d4/d5
continue = if cheap, ask GPU for same-stream Delta_res telemetry
continue = keep 16-8*A as the exact A-line bridge for the row-bit quartic

kill = treating the quartic factor as generic S4
kill = treating the Aeta quartic label as sourceable before Delta_res comparison
kill = visible-coordinate product bucket scans in place of Delta_res extraction
```

```text
p27_trace_norm_dplus_u6_rowbit_quartic_invariant_rows=1/1
```
