# Prescribed-Trace Direct Route Boundary

Date: 2026-06-05

This note records the sanity check:

```text
Could Waterhouse/Rueck/Voloch/Mestre-style prescribed-trace existence or
construction bypass the embedded CM phase problem?
```

For the fixed p24 DANGER3 prime, the answer is no for the known direct route.

## Fixed Field Means Fixed Isogeny Class

For a fixed prime field `F_p`, prescribing the DANGER3 order is the same as
prescribing the trace:

```text
N = p + 1 - t.
```

By Tate's theorem, fixing `t` fixes the ordinary isogeny class over `F_p`.
Waterhouse/Rueck/Voloch-style theorems classify existence and group
structures in that class, but they do not name a curve in the class.

The constructive fixed-field route returns to CM:

```text
compute or otherwise select a root of the relevant CM class polynomial mod p.
```

For the p24 strict traces, that CM root selection is exactly the hard part.

Source anchor: Agashe-Lauter-Venkatesan's "Constructing elliptic curves with
a given number of points over a finite field" describes the Atkin-Morain CM
route as requiring calculation of a Hilbert class polynomial `H(X)` modulo
`p` for a discriminant `D`; their contribution is a better way to compute
`H(X) mod p`, not a root selector that avoids the class object.

## p24 Audit

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/prescribed_order_fixed_p_audit.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/waterhouse_mestre_fixed_trace_barrier.py
```

The three strict absolute traces are:

```text
|t| = 1020608380936
|t| = 78903246840
|t| = 1178414874616
```

All have:

```text
t^2 - 4p = 4D_K,
conductor in Z[pi] = 2,
|D_K| comparable to p.
```

The audit reports:

```text
abs_trace=1020608380936
  fundamental_D=-739589633190799177940983
  class_number_degree_H_D=278733727154
  class_number_over_sqrt=0.278734

abs_trace=78903246840
  fundamental_D=-998443569409526507503607
  class_number_degree_H_D=833035208344
  class_number_over_sqrt=0.833035

abs_trace=1178414874616
  fundamental_D=-652834595820939249713143
  class_number_degree_H_D=205880396014
  class_number_over_sqrt=0.205880
```

The third trace remains the best decomposed target because:

```text
205880396014 = 2 * 157 * 211 * 3107441.
```

But direct fixed-trace CM construction would still face a class object whose
degree is a positive constant times `sqrt(p)`.

## Near-Square Exception

The near-square identity gives a genuine cheap CM curve:

```text
p = n^2 + 7,
t = +/- 2n,
D = -7.
```

For p24:

```text
n = 10^12,
t = +/- 2000000000000.
```

That curve is easy to construct, but the DANGER3 strict depth fails:

```text
v2(p + 1 - 2n) = 3,
v2(p + 1 + 2n) = 3,
required k = 40.
```

So the only known cheap prescribed-trace-looking object is not in the strict
DANGER3 branch.

## Toy Calibration

The small fixed-trace toy:

```text
p24/fixed_trace_cm_root_toy.py
p24/fixed_trace_cm_root_toy.md
```

shows the exact finite-field shape:

```text
fixed_trace_j_set = roots(H_DK) union roots(H_4DK) mod p.
```

Thus fixed trace names the relevant volcano/isogeny class, not a seed vertex
inside it.

## Consequence

Known fixed-field prescribed-trace/order tools do not bypass the p24
certificate problem.  A successful direct route would need a genuinely new
fixed-p selector:

```text
select one conductor-2 CM j-root for the p24 strict trace
without computing a class object of degree Theta(sqrt(p)).
```

That is the same embedded non-genus phase/recovery obstruction isolated by
the selected-chain and Fitting p-unit routes.
