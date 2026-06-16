# P25 Lane B: KSY-y Mixed-Graph Obligation

Updated: 2026-06-13 20:12 PDT

## Purpose

The source-parameter hygiene gate prevents notation drift.  This gate records
the next source-theorem obligation: the p25 payload really needs the mixed
`C_3 x C_169` row graph.  A source theorem cannot close the route by producing
only the `C_169` projection, ordinary Kubert-Lang congruences, or one signed
pair per row with the wrong row assignment.

## Accepted Finite Graph Shapes

Any of the following satisfies the finite mixed-graph obligation:

```text
exact row-labeled pairs:
  row 0: c31 - c138
  row 1: c25 - c141
  row 2: c28 - c144

quotient reflection center:
  C = (2,28)
  D = (1,3)
  base = C-D = (1,25)
  T = -2C = (2,113)
  T/2 = -C = (1,141)

raw equal-weight product:
  raw C = (47,28) up to K-gauge
  raw D = +/-(22,3) up to K-gauge
  K = primitive generator of (57,0)
  orientation = theta2 or theta2 inverse branch
```

These are finite payload shapes.  They still need a challenge-legal arithmetic
producer theorem before the moonshot route closes.

## Rejected Or Conditional Shadows

```text
rejected:
  C169 projection alone
  KL exponent/congruence hygiene alone
  one signed pair per row with wrong pairing

conditional:
  fixed-T cyclic translate without base-row anchor
```

The fixed `T` edge leaves three cyclic row translates.  The accepted translate
is selected only by the base-row/reflection anchor, equivalently by the exact
source-packet contract.

## Completed Gate

```text
dependency gates:
  source-parameter hygiene              = pass
  graph row law                         = pass
  graph separability                    = pass
  row-labeled pair contract             = pass
  row-pair permutation rigidity         = pass
  reflection-center contract            = pass
  anti-invariant producer contract      = pass

regression rows:
  finite obligation met                 = 4
  arithmetic closing rows               = 1
  conditional rows                      = 1
  rejected rows                         = 3
```

Local audit gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py
```

Fast candidate examples:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py \
  --candidate --name c169_only --kind c_axis --c169-projection

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py \
  --candidate --name reflection_center --kind reflection \
  --c169-projection --kl-congruences --one-pair-per-row --fixed-t-edge \
  --base-row-anchor --reflection-center

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py \
  --candidate --name raw_product_theorem --kind raw \
  --c169-projection --kl-congruences --one-pair-per-row --fixed-t-edge \
  --base-row-anchor --exact-row-labeled-pairs --reflection-center \
  --raw-product --arithmetic-producer
```

Marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_candidate_rows=1/1
```

## Consequence

The theorem target is now sharper:

- Kubert-Lang `C169` data is a necessary screen only.
- A live source must emit exact row-labeled pairs, reflection-center data, or
  the stronger raw K-traced product.
- The raw product plus an arithmetic producer theorem is the closing source
  shape; everything weaker remains finite-payload evidence, not a certificate.
