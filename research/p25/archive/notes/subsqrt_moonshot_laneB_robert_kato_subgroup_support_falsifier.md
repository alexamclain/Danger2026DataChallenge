# Subsqrt Moonshot Lane B Robert/Kato Subgroup-Support Falsifier

Date: 2026-06-13

## Result

The literature scout found the right translated-odd quotient shape:

```text
rho_H(P + T) / rho_H(P - T)
```

where a Kato/Robert function `rho_H` has divisor `|H|[0] - [H]` for a finite
subgroup `H`.  This matches the odd orientation we need, but the literal
finite-subgroup support does not match the p25 bridge.

The p25 bridge requires:

```text
base * K_trace * D_segment * (1 - T)
visible D = (1,3) in C_3 x C_169
raw D = (22,3) in C_75 x C_169
raw K = (57,0)
```

The `D_segment = 1 + D + D^2` is not a subgroup/coset support:

```text
visible order(D) = 507
3D = (0,9), not 0
raw order(D) = 12675
raw K_trace * D_segment has C-support (25,28,31)
any raw subgroup of order 75 has trivial C-projection because gcd(75,169)=1
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_kato_subgroup_support_falsifier_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_kato_subgroup_support_falsifier_gate.py
```

Observed:

```text
robert_kato_subgroup_support_falsifier_rows=1/1
conclusion=reported_p25_laneB_robert_kato_subgroup_support_falsifier_gate
```

## Consequence

The literal Kato/Robert subgroup-divisor quotient is killed as a complete
producer for the p25 bridge.  The useful part of the scout result is the
translated odd quotient architecture, not a direct subgroup `H`.

Continue only with a weighted or non-subgroup source:

```text
y(P+T)/y(P-T)
wp'/differential quotient
Klein/Siegel quotient with Bernoulli/divisor weights
finite-difference quotient that actually emits the D_segment
```

The first falsifier for those candidates is now the sparse-source harness:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py \
  --sparse-source PATH
```
