# P25 KSY-y Kubert-Lang Visual Theorem Boundary

Updated: 2026-06-14 08:24 PDT

## Purpose

Local OCR is not available in the current environment, but the rendered
Kubert-Lang IV/V pages are readable enough for a targeted theorem pass.  This
checkpoint records that visual pass so the active KL/KSY exact-product lane can
move forward without repeatedly reopening the same image pages.

## Visual Rows

```text
Kubert-Lang IV, Theorem 6, article page 239
image = /tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all/page-18.png
visible = multiplicative-dependence criterion for constant/modular products of
          Siegel functions
verdict = useful dependence/modularity language, not exact p25 row labels

Kubert-Lang IV, Theorem 7, article page 240
image = /tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all/page-19.png
visible = prime-power multiplicative independence modulo constants for
          g_a with a in Z(p^n)^*
verdict = useful prime-power independence control, not mixed C3 x C169 selector

Kubert-Lang IV, Theorem 8 / Lemma 6.1, article page 241
image = /tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all/page-20.png
visible = Delta/Klein-form dependence and prime-power generated-unit criterion
verdict = useful generation boundary, not finite p25 P/theta2 payload

Kubert-Lang V, Theorem 1, article page 101
image = /tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016/page-6.png
visible = G is a one-dimensional free module over the Iwasawa algebra
verdict = p-primary tower context, not finite row labels or raw product

Kubert-Lang V, Lemma 1, article page 102
image = /tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016/page-7.png
visible = factor group V_m/V_n has no torsion for m >= n
verdict = tower torsion-control context, not exact mixed product

Kubert-Lang V, Lemma 2 / conclusion, article page 103
image = /tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016/page-8.png
visible = maximal unramified p-abelian extension and Vandiver/Iwasawa
          cyclicity conclusion
verdict = class-field/Kummer analogy only for the p25 target
```

## Boundary

The visible theorem rows are theorem-shaped and relevant as source vocabulary,
but they do not emit any of the accepted p25 payloads:

```text
exact C3 x C169 row-labeled pairs
quotient reflection center
raw equal-weight K-traced product with arithmetic producer status
```

So the active KL/KSY lane remains live only through an exact product upgrade,
not through generic KL IV dependence/generation or KL V Iwasawa-freeness
language.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_visual_theorem_boundary_gate.py
```

Marker:

```text
ksy_y_kubert_lang_visual_theorem_boundary_rows=1/1
```
