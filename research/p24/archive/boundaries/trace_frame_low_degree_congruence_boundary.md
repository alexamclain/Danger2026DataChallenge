# Trace-Frame Low-Degree Congruence Boundary

Date: 2026-06-05

This note spells out the concrete obstruction behind the local-unit criterion.

## Congruence Form

In one p24 tensor factor:

```text
B/E has degree 5549
C/E has degree 179
B/C has degree 31
```

Let `theta` generate `B/C`, and let `g` be its relative minimal polynomial.
For an axis-supported character combination:

```text
x_w = sum_{s in S_axis} w_s R_s,
```

the leading trace-frame theorem fails exactly when:

```text
g'(theta) * x_w
```

has relative degree at most `27` over `C`.

Equivalently, there are coefficients `c_0,...,c_27 in C`, not all coming from
the zero axis vector, such that:

```text
g'(theta) * sum_s w_s R_s
  = c_0 + c_1 theta + ... + c_27 theta^27.
```

This is the low-relative-degree congruence that must be ruled out at the
selected prime.  In orbit-algebra language it is the failure condition:

```text
W_axis(A_Omega) cap F_27(A_Omega) != {0}.
```

## Audit

I added:

```text
p24/trace_frame_low_degree_congruence_audit.py
```

It intentionally takes too few top blocks in small CM tensor rows so the
kernel is dimension-forced, then measures the resulting congruence:

```text
axis_support:
  number of nonzero axis-character coefficients;

axis_block_touches:
  number of smooth axis blocks touched;

low_nonzero_blocks:
  number of nonzero relative coefficient blocks below the killed top window;

high_zero:
  verifies that the top blocks really vanish.
```

Pinned full-axis row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_low_degree_congruence_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-top-count 3 --include-linear --only-m 12 \
  --max-cases 1 --max-kernel-basis 4
```

reported:

```text
rows=9
all high_zero=1

subdeg=2, rel=3, top=1:
  kernel_dim=4
  axis_support=3
  axis_block_touches=2 or 3
  low_nonzero_blocks=2 of 2

subdeg=2, rel=3, top=2:
  kernel_dim=2
  axis_support=5
  axis_block_touches=3
  low_nonzero_blocks=1 of 1

subdeg=3, rel=2, top=1:
  kernel_dim=3
  axis_support=4
  axis_block_touches=2 or 3
  low_nonzero_blocks=1 of 1
```

The compact beta/tensor bridge rows show the same pattern:

```text
D=-1559, q=2459, h=51, m=3, n=17:
  axis_support=3
  axis_block_touches=2
  low_nonzero_blocks=3 of 3
  high_zero=1

D=-2207, q=2243, h=39, m=3, n=13:
  axis_support=3
  axis_block_touches=2
  low_nonzero_blocks=2 of 2
  high_zero=1
```

## Consequence

The failure relation is not behaving like:

```text
a one-component annihilator,
a sparse tail polynomial,
a low-support coefficient accident.
```

In the tested rows, when a low-degree congruence is forced, it already uses
multiple smooth-axis blocks and fills the entire allowed low relative tail.

So the p24 proof should target the selected cross-axis congruence:

```text
no nonzero smooth-axis character combination can land in C[theta]_{<=28}
after multiplication by g'(theta) with its theta^28 coefficient supported
outside the first ten normal-basis coordinates.
```

This matches the determinant-line/local-unit formulation and disfavors
component-only or sparse-tail proof attempts.

The intrinsic full-top-three condition `W_axis cap F_27={0}` follows from the
selected-leading theorem but is not a sufficient replacement for it.  The
selected-vs-full distinction is recorded in:

```text
p24/trace_frame_selected_lead_failure_module.md
p24/lean/TraceFrameSelectedLeadFailureGate.lean
```

## Possible Positive Lemma

A theorem strong enough to finish the leading route would be:

```text
For the p24 CM tensor factor and every beta-orbit algebra A_Omega, the
selected residual-tail module vanishes:

  K_sel,Omega =
    { x in W_axis(A_Omega) cap F_28(A_Omega) :
        pi_10(b_28(x)) = 0 }
    = {0}.
```

In Fitting language, this says the cokernel determinant of the dual leading
map is a unit.  In divisor language, it says the selected CM prime avoids the
Schubert divisor of selected low-relative-degree smooth-axis congruences.

The small audits say this is the right-strength theorem: weaker component
normality cannot see the obstruction, and sparse low-tail formulas are not
what appears in forced kernels.
