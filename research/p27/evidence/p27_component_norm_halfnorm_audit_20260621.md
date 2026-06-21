# P27 Component Norm / Half-Norm Audit

Date: 2026-06-21

## Claim

The visible norm squareclasses inside the `h` and `vq` components do not
explain the remaining `T_line` selector.  After simplification, the new norm
factors collapse to already-known branch squareclasses.  A small named-product
screen gives no exact selector, and its best in-sample lift fails on held-out
seed streams.

This sharpens the theorem target: the remaining object is not a branch-divisor
or norm-squareclass lookup.  It would need a non-visible theta/additive/Hilbert
90 coupling identity for the phases of the two half-norm sections.

## Setup

Use:

```text
t = y - 1
B = t^2 + 1 = y^2 - 2y + 2
C = t^2 + 2t - 1 = y^2 - 2
R = t^2 - 2t - 1 = y^2 - 4y + 2
F = t C B
K = -C R
a = t - 1/t
b = w B / t^2
```

The component split from the previous audit is:

```text
T = chi(y - 2) * h * vq
T_line = T                  if chi(a)=+1
       = T * chi(b)         if chi(a)=-1
```

## Norm Reductions

For the `h` argument:

```text
H = 4 C B + 8 t z
z^2 = F
Norm_z(H) = 16 C B (C B - 4t^3)
C B - 4t^3 = (t - 1)^3 (t + 1)
```

So the non-square part of the `h` norm is only the already-visible branch
squareclass `chi(t^2 - 1)`, equivalently `-chi(1 - t^2)` for this p27 prime.

For the `vq` argument:

```text
V = 8 y C t^2 + 4 y z w
w^2 = K
Norm(V) = 16 y^2 C^2 t (4t^3 + B R)
4t^3 + B R = (t + 1)^3 (t - 1)
```

So the non-square part of the `vq` norm is again only the same branch class,
with the extra `chi(t)` factor.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_component_norm_gate.py
```

Run:

```bash
python3 research/p27/archive/gates/p27_component_norm_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --top 20 \
  --max-product-degree 4 \
  | tee research/p27/archive/probe_outputs/p27_component_norm_64tid_2chunk_256draw_20260621.txt
```

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
component_rows = 16096
component_unusable = 16768
```

Formula checks:

```text
h_recompute_mismatch = 0
vq_recompute_mismatch = 0
h_norm_factor_mismatch = 0
v_norm_factor_agree = 16096
h_inner_anti_xpref = 16096
v_inner_anti_xpref = 16096
B_equals_a_plus_2 = 16096
B_anti_a_minus_2 = 16096
C_anti_R = 16096
pref_formula_mismatch = 0
q2_non_square = 0
```

Named atoms against `T_line`:

```text
best single usable atom lift ~= 1.011
exact single atoms = 0
```

Named product span:

```text
usable_atoms = 13
product_count = 1092
exact_products = 0
best in-sample product lift ~= 1.039
```

The best in-sample product was:

```text
chi_B * chi(y - 2) * chi(1 - t^2)
```

Held-out check:

```text
seed=121 lift=1.038952575
seed=122 lift=1.005353567
seed=123 lift=1.005343337
seed=124 lift=1.002737207
```

The lift is therefore not promoted as a filter.

## Interpretation

Positive:

```text
The h and vq square-root arguments have now been reduced to explicit norm
forms.
The norm reductions explain why another branch-divisor scan was unlikely to
work: the new factors collapse to existing branch classes.
```

Negative:

```text
No visible branch divisor, h/vq norm class, or degree <= 4 product of the named
line atoms explains T_line.
The only apparent product lift disappears on held-out seed streams.
```

## Continue / Kill

```text
continue = ask for a theta/additive/Hilbert-90 identity that controls the phase
           of H and V together, not just their norms
continue = GPU same-stream line telemetry for practical survivor lift
continue = test only named non-visible identities from an expert/source

kill = more visible branch-divisor product screens
kill = treating h_norm or vq_norm as the missing selector
kill = promoting the 1.039 in-sample product without held-out lift
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_component_norm_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_component_norm_64tid_2chunk_256draw_20260621.txt`
- Held-out output: `research/p27/archive/probe_outputs/p27_component_norm_top_product_heldout_20260621.txt`
- Prior component split: [P27 T-Line Component Descent](p27_tline_component_descent_20260621.md)

```text
p27_component_norm_halfnorm_audit_rows=1/1
```
