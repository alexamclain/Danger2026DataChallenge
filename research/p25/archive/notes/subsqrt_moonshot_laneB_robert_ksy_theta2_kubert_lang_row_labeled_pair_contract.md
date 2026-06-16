# P25 Lane B: Robert KSY Kubert-Lang Row-Labeled Pair Contract

Updated: 2026-06-13 17:44 PDT

## Purpose

The graph-separability gate leaves a concrete theorem interface.  A surviving
Kubert-Lang/Siegel/Robert source should not merely reproduce the `C_169`
projection or a row mask.  It should emit the exact six quotient triples, or
equivalently the exact three row-labeled signed pairs.

## Accepted Payload

```text
row 0: c31 - c138
row 1: c25 - c141
row 2: c28 - c144
```

The accepted packet has:

```text
support                  = 6
coefficient counts       = (-1,3),(1,3)
C-axis projection        = 1,1,1,-1,-1,-1
primitive K lift support = 150
source contract          = pass
```

## Rejected Controls

The gate records three important false positives:

```text
wrong fixed-T row translates:
  support 6, same C-axis projection, fail source contract

row-only projection shortcuts:
  support 6/18, rank-one/separable, fail source contract

wrong pairings with same C-axis projection:
  support 6, one signed pair per row, fail source contract
```

Thus even the shape "one signed pair per row" is not enough.  The row labels
and pair matching are part of the finite theorem payload.

## Candidate Intake

The checker accepts optional quotient triples:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate.py \
  --packet PATH
```

Input format:

```text
right_row c_log coefficient
```

Candidate pass conditions:

```text
exact row-labeled signed pairs
exact C-axis projection
primitive-K source packet lift
```

Expected default marker:

```text
robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_rows=1/1
```

## Interpretation

This is now the finite landing pad for targeted literature or formula hits.  A
candidate theorem can be useful if it naturally emits the three row-labeled
signed pairs, or if it emits a stronger object that reduces to this packet
before the existing primitive-K lift.
