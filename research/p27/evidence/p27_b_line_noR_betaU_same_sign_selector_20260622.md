# P27 B-Line No-R Beta_U Same-Sign Selector Screen

Date: 2026-06-22

## Claim

The remaining same-plus versus same-minus choice in beta_U f4 is not explained
by natural low-weight x6-level squareclass products.

This screen starts only after the exact pair norm

```text
x7_plus * x7_minus = -4*(A*x6 + 1)
```

has already separated mixed x7 pairs from same-sign x7 pairs.  On the
same-sign pairs, it tests whether natural x6-level characters can choose:

```text
same-plus  vs  same-minus.
```

No exact selector appears through product weight `3`, and the best labels are
not stable across guard fields.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_same_sign_selector_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_same_sign_selector_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_same_sign_selector_probe_q359_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_same_sign_selector_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_same_sign_selector_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_same_sign_selector_probe.py \
  --fields 359^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_same_sign_selector_probe_q359_20260622.txt
```

## Method

Rows:

```text
beta_U_fixedB
gamma = +1
x6 materialized
x7 pair has same f4 sign
```

Targets:

```text
same-plus  -> +1
same-minus -> -1
```

Atom family:

```text
x6, x6 +/- 1, x6 +/- 2,
A*x6 +/- 1,
x6 +/- A,
u=x6+1/x6, u +/- 2,
x6-1/x6,
B, A, d_next,
x6*(A*x6+1),
(x6+/-1)*(A*x6+1)
```

Screen:

```text
all squarefree products through weight 3
```

## Result

Guard and heldout fields:

```text
71^2, 167^2, 199^2, 263^2, 311^2, 359^2
```

Same-sign pair counts:

```text
field    same pairs    plus    minus
71^2     118           70      48
167^2    92            48      44
199^2    250           114     136
263^2    208           104     104
311^2    272           148     124
359^2    456           220     236
```

Best low-weight products:

```text
field    best weight-1       best weight-2/3 quality
71^2     80 / 118            80 / 118
167^2    56 / 92             68 / 92
199^2    142 / 250           146 / 250
263^2    122 / 208           130 / 208
311^2    154 / 272           164 / 272
359^2    244 / 456           276 / 456
```

The best label changes across fields.  The larger `359^2` heldout has best
weight-3 quality `276/456`, about `60.5%`, not a promotion signal.

## Interpretation

Positive:

```text
The test is now focused on the actual remaining beta_U f4 choice, after the
known x7-pair norm has been factored out.
```

Negative:

```text
No natural atom or low-weight atom product selects same-plus vs same-minus.
Best in-field products are weak and field-dependent.
No visible x6-level beta_U f4 selector should be sent to GPU.
```

## CAS Consequence

The remaining beta_U/f4 question is genuinely normalized Kummer/Prym work:

```text
extract the beta_U f3/materialization class;
include x7_plus*x7_minus=-4*(A*x6+1) as known branch norm;
then decide whether the same-plus/same-minus class is pullback, coboundary,
quotient/Prym, recurrence, or fresh half-cover.
```

Promote only a named quotient/class relation.  Kill visible x6-atom product
searches unless a theorem gives a specific new coordinate.

## Continue / Kill

```text
continue = beta_U normalized Kummer/Prym extraction
continue = compare same-sign f4 choice after normalization
continue = keep this screen as a regression against visible x6 atom claims

kill = natural x6-level products through weight 3 as f4 selectors
kill = GPU beta_U same-sign buckets
kill = more blind x6 atom-product scans without a named theorem
```

```text
p27_b_line_noR_betaU_same_sign_selector_rows=1/1
```
