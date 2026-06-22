# P27 Trace/Norm Dplus U6 Row-Bit Local Magma Factor Split

Date: 2026-06-22

## Claim

Local Magma resolves the Dplus `U6` row-bit factorization tier that online
Magma could not run.  The row-bit lift is irreducible over the bare H90
elliptic base, but it splits after adjoining the H90 domain-spin layer and
splits again after adjoining either `A_eta` second-layer cover.

Across the guard fields

```text
q = 607, 1607, 1847, 2087
```

the factor degrees are stable:

```text
over E_h90:              32
over domain-spin z:      16 + 16
over A_eta, eta = +1:     8 + 8 + 8 + 8
over A_eta, eta = -1:     8 + 8 + 8 + 8
```

This is a positive structural result.  It does not yet give a production
sampler, but it turns the row-bit lane from "generic hidden sign" into a
specific factor-action / Kummer-class extraction problem over the
domain-spin/Aeta tower.

## Artifacts

Local Magma binary used:

```text
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma
```

Fixtures:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_magma.m
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_magma.m
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_aeta_factor_eta1_q607_magma.m
research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_eta1_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q1607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q1847_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q2087_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_action_q607_local_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_action_q1607_local_magma_20260622.txt
```

## Commands

Smoke:

```bash
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q31_local_magma_20260622.txt
```

q607 domain-spin and Aeta:

```bash
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_domainspin_factor_q607_local_magma_20260622.txt

/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607_local_magma_20260622.txt
```

The q1607/q1847/q2087 guard runs used the same `botheta` fixture with the
field constant substituted:

```bash
perl -pe 's/q := 607;/q := <q>;/' \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q607_magma.m \
  > /tmp/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q<q>_magma.m

/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  /tmp/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q<q>_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_aeta_factor_botheta_q<q>_local_magma_20260622.txt
```

Factor-action probe:

```bash
/Users/agent/Documents/Codex/t24-search/private/magma-local/install/magma \
  research/p27/archive/fixtures/p27_trace_norm_dplus_u6_rowbit_factor_action_q607_magma.m \
  2>&1 | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_factor_action_q607_local_magma_20260622.txt
```

The q1607 action guard used the same fixture with `q := 1607`.

## Results

Tiny smoke:

```text
q31 domain-spin setup: E genus 1, degree 2; L genus 5, degree 2 over E
q31 domain-spin factor degrees: 16, 16
```

Guard fields:

```text
field   domain-spin factors   Aeta eta=+1 factors   Aeta eta=-1 factors
607     16 + 16               8 + 8 + 8 + 8          8 + 8 + 8 + 8
1607    16 + 16               8 + 8 + 8 + 8          8 + 8 + 8 + 8
1847    16 + 16               8 + 8 + 8 + 8          8 + 8 + 8 + 8
2087    16 + 16               8 + 8 + 8 + 8          8 + 8 + 8 + 8
```

Magma setup also reports:

```text
E_h90 genus = 1, degree(E/Fq(t)) = 2
domain-spin L genus = 5, degree(L/E_h90) = 2
Aeta cover degree(N/L) = 2
```

Factor action:

```text
field   domain z->-z   domain S->-S   Aeta rho->-rho   Aeta S->-S
607     [2,1]          [1,2]          [2,1,4,3]        [1,2,3,4]
1607    [2,1]          [1,2]          [2,1,4,3]        [1,2,3,4]
```

Thus the domain-spin deck involution swaps the two degree-16 factors; the
Aeta deck involution swaps the degree-8 factors in pairs; and the row-bit
sheet involution `S -> -S` fixes each tested factor.

## Interpretation

Positive:

```text
The row-bit cover is not generic over the full H90/domain-spin/Aeta tower.
The domain-spin layer halves the degree of the row-bit lift.
Each Aeta sign halves it again, producing four degree-8 factors.
The pattern is stable across q607/q1607/q1847/q2087.
```

Negative:

```text
This is not yet a direct source or GPU production rule.
The visible H90/domain-spin/Aeta product-character screen still has no exact
coordinate product through weight 4.
The q1847 visible u-line cubic/quartic route is still dead.
```

## Consequence

The row-bit lane should now focus on factor action, not blind buckets:

```text
1. compute the remaining eta/z cross-action between the two Aeta signs;
2. identify whether a factor orbit is the pulled-back A-level d3/x6 Kummer class,
   a coboundary of A_eta, or a fresh Prym factor;
3. if a cheap factor identifier exists, ask GPU for same-stream telemetry of
   that identifier versus d3/d4/d5;
4. if the degree-8 factors remain high/non-sourceable, record that as the
   obstruction.
```

Follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit Factor Label Probe](p27_trace_norm_dplus_u6_rowbit_factor_label_20260622.md)
shows that the four Aeta degree-8 factors are all even in `S`, hence quartics
in `Y=S^2=U6+2`; rho-paired factor products multiply exactly back to the two
domain-spin degree-16 factors; and the quartic coefficient profile is stable
in q607/q1607.  The next extraction target is therefore a quartic-label
Kummer class over the Aeta function field, not an arbitrary degree-8 factor.

Promotion:

```text
a named low-complexity factor label or Kummer class that recurs across later
selected gates, or a cheap same-stream identifier whose lift compounds beyond
independent half-loss
```

Kill:

```text
treating the row bit as generic over domain-spin/Aeta
treating visible H90/Aeta coordinate products as the explanation
treating the split alone as a sampler without factor-label extraction
```

```text
p27_trace_norm_dplus_u6_rowbit_local_magma_factor_split_rows=1/1
```
