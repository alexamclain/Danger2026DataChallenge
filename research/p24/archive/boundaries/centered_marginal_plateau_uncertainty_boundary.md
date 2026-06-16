# Centered Marginal Plateau/Uncertainty Boundary

Date: 2026-06-05

This note records the dual form of the right-window determinant condition and
why plain cyclic uncertainty is not enough to prove it.

## Plateau Dual

Let `P_b in F_p^156`, `b mod 211`, be the centered marginal point columns with
`P_0=0`.  The right-translation determinant factor is:

```text
F(t) = det(P_{t+1}-P_t, ..., P_{t+156}-P_t).
```

Then:

```text
F(t)=0
```

if and only if there exists a nonzero dual vector `lambda` such that the scalar
word

```text
w_lambda(b)=lambda(P_b)
```

is constant on the `157` consecutive positions:

```text
t, t+1, ..., t+156.
```

Thus `Pi_C,right != 0` is equivalent to:

```text
no nonzero dual trace word has a 157-term cyclic plateau.
```

## Why Plain Uncertainty Is Insufficient

Subtract the plateau constant.  A bad word gives a nonzero word supported on
at most:

```text
211 - 157 = 54
```

positions.  Tao's prime cyclic uncertainty gives:

```text
support_time + support_frequency >= 212.
```

So the Fourier support must have size at least:

```text
212 - 54 = 158.
```

But the centered right profile can use all `210` nonzero right frequencies.
Therefore the uncertainty bound leaves a wide feasible range:

```text
158 <= support_frequency <= 210.
```

It cannot prove the p24 plateau obstruction by itself.

## Toy Boundary

Added:

```text
p24/plateau_uncertainty_boundary_toy.py
```

Command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/plateau_uncertainty_boundary_toy.py \
  --length 13 --plateau 8 --q 53 --trials 10000
```

Output:

```text
time_support_after_subtracting_constant=5
frequency_support_after_subtracting_constant=12
uncertainty_sum=17
uncertainty_threshold=14
plateau_ok=1
zero_frequency_absent=1
nonzero_frequency_support_full=1
```

So even a zero-mean sparse difference word with a long plateau can have full
nonzero Fourier support.  The p24 proof needs more than prime cyclic
uncertainty: it needs the CM/exterior trace-form arithmetic of the actual
dual word family.

## Current Theorem Shape

The plateau formulation remains useful because it gives a crisp obstruction:

```text
For every nonzero lambda in the left dual field, the scalar centered
right-profile word w_lambda has no cyclic plateau of length 157.
```

This is equivalent to all 211 factors of `Pi_C,right` being nonzero.  The
missing theorem is still arithmetic, not a generic uncertainty theorem.

Equivalently, the centered marginal point columns form a cyclic consecutive
affine arc:

```text
p24/centered_marginal_affine_arc_theorem.md
```
