# P27 B-Line No-R Hidden_Mixed Next-Gate Probe

Date: 2026-06-22

## Claim

`hidden_mixed_fixedB` is not a direct multi-gate source.

It has two different gamma-positive regimes:

```text
chi(B) = -1, gamma = +1:
  Unext + 2 is square, but Unext = x6 + 1/x6 does not materialize.

chi(B) = +1, gamma = +1:
  x6 materializes, but f4 is mixed inside every active base B row.
```

So hidden_mixed gives useful CAS routing data, but no GPU-production sampler.

Relation to beta_U:
[P27 B-Line No-R Fixed-B Norm Relation](p27_b_line_noR_fixedB_norm_relation_20260622.md)
shows that on the common square-`B` support, `gamma_hidden = gamma_beta` in
all tested fields.  The square-`B` materialized hidden_mixed rows are therefore
a related model of beta_U's first selected class, not an independent first-sign
source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_hidden_mixed_next_gate_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_hidden_mixed_next_gate_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_hidden_mixed_next_gate_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_hidden_mixed_next_gate_probe_20260622.txt
```

## Result

Fields:

```text
23^2, 71^2, 103^2, 167^2, 199^2, 263^2, 311^2
```

Setup checks:

```text
bad_curve_a = 0
B_gamma_conflicts = 0
vplus2_x7_chi_mismatch = 0
x7_pair_product_formula_mismatch = 0
```

Gamma-positive hidden_mixed rows over nonsquare `B` do not materialize:

```text
field    gamma+ nonsquare-B rows    x7 roots
23^2     1                          0
71^2     4                          0
103^2    6                          0
167^2    10                         0
199^2    12                         0
263^2    16                         0
311^2    19                         0
```

Gamma-positive hidden_mixed rows over square `B` materialize but have mixed f4:

```text
field    gamma+ square-B rows    x6 roots per B    x7 roots per B    mixed-f4 B rows
71^2     8                       64                128              8
167^2    6                       64                128              6
199^2    16                      64                128              16
263^2    12                      64                128              12
311^2    16                      64                128              16
```

Aggregate f4 signs on materialized hidden_mixed rows:

```text
field    f4+    f4-
71^2     490    534
167^2    370    398
199^2    1024   1024
263^2    746    790
311^2    1034   1014
```

Pair-level structure matches the ordinary halving norm, as in beta_U:

```text
x7_plus * x7_minus = -4 * (A*x6 + 1)
```

but this only separates same-sign from mixed x7 pairs.  It does not select the
next sign.

## Interpretation

Positive:

```text
hidden_mixed has a sharper materialization boundary than before:
gamma-positive nonsquare-B rows are not x6-materialized continuation rows.
The square-B materialized rows obey the expected f4/v+2 semantics.
```

Negative:

```text
The materialized square-B hidden_mixed rows all have mixed f4.
The nonsquare-B gamma-positive rows are dead for x6 materialization.
The x7-pair norm is ordinary orientation data, not a sampler.
No hidden_mixed GPU production mode follows.
```

## CAS Consequence

Revise the hidden_mixed subtest:

```text
separate gamma-positive nonsquare-B non-materialized rows from square-B rows;
carry x7_plus*x7_minus = -4*(A*x6+1) as orientation data on the square-B side;
compare f4 only after normalization, as a possible quotient/Prym relation or
fresh half-cover.
```

Promote hidden_mixed only if normalized CAS finds a non-visible class relation
that carries f4 or couples to beta_U/f3.  Otherwise kill hidden_mixed as a
sqrt-beating route.

## Continue / Kill

```text
continue = hidden_mixed divisor/Kummer extraction only as second-pass CAS
continue = compare hidden_mixed square-B materialized class with beta_U after normalization
continue = record nonsquare-B gamma+ rows as non-materialized boundary data
continue = enforce gamma_hidden = gamma_beta on square-B rows as a regression

kill = hidden_mixed gamma=+1 as a continuation sampler
kill = hidden_mixed chi(B) split as an f4 selector
kill = hidden_mixed x7-pair buckets as production filters
kill = hidden_mixed as an independent square-B first-sign source
```

```text
p27_b_line_noR_hidden_mixed_next_gate_rows=1/1
```
