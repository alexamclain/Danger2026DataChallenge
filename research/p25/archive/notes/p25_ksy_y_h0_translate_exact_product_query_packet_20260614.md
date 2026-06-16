# P25 KSY-y H0 Translate Exact-Product Query Packet

Updated: 2026-06-14 15:20 PDT

## Purpose

This packet gives the exact product targets for the H0-translate theorem hunt.
The previous query packet says what answer shape closes the source stage; this
one says which four products a theorem may hit.

## Four Legal Products

Each row is a level-507 Yang-fiber product:

```text
prod_{a in P, k=0..12} E_{a+39k}^6 /
prod_{b in N, k=0..12} E_{b+39k}^6
```

All four have `78` positive and `78` negative factors, support `156`, and
boundary `(1-Frob_p)H0 = Norm_156(Y_507)`.

```text
multiplier 1, canonical_H0
  constants = (3, 3, -3, -3)
  P = (7, 17, 23, 34, 37, 38)
  N = (4, 8, 10, 11, 20, 25)

multiplier 2, H0_translate
  constants = (-3, 3, 3, -3)
  P = (7, 14, 29, 34, 35, 37)
  N = (1, 8, 11, 16, 20, 22)

multiplier 4, H0_translate
  constants = (-3, -3, 3, 3)
  P = (14, 19, 28, 29, 31, 35)
  N = (1, 2, 5, 16, 22, 32)

multiplier 8, H0_translate
  constants = (3, -3, -3, 3)
  P = (17, 19, 23, 28, 31, 38)
  N = (2, 4, 5, 10, 25, 32)
```

## Source-Closing Answers

For any one of the four products, either answer shape closes the source stage:

```text
exact finite-field value identity with period-156 branch/root/telescoping context
exact divisor/additive identity with the Hilbert-90 boundary to Norm_156(Y_507)
```

First falsifier:

```text
wrong residue sets
nonlegal sparse gauge
formal one-coset H
missing boundary
missing period-156 context for value claims
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_exact_product_query_packet_gate.py
```

Expected marker:

```text
ksy_y_h0_translate_exact_product_query_packet_rows=1/1
```

## Interpretation

This is the object-level matching sheet.  If an expert answer or paper
contains a theorem that emits one of these four products with either accepted
answer shape, route it immediately to DANGER3 framing and the `X_1(8112)` /
`X_1(16)` extraction ladder.
