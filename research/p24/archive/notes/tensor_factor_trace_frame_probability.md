# Tensor Factor Trace Frame Probability

The trace-frame target has a strong random-subspace sanity check.

The script is:

```text
p24/tensor_factor_trace_frame_probability.py
```

For p24:

```text
Q = |E| = p^5460
axis_dim = 368
trace_frame_dim = 3*179 = 537
```

If the 368-dimensional axis image behaved like a random `E`-subspace against
a fixed rank-537 trace frame, the failure probability would be:

```text
1 - product_{i=0}^{367} (1 - Q^(i-537))
  ~= Q^-170.
```

Since:

```text
log10(Q) ~= 131040
```

the leading log-probability is about:

```text
log10(failure) ~= -2.23e7.
```

This is not a proof.  It says that if the p24 CM axis image fails the
trace-frame theorem, it is not a mild random accident; it must come from a
structured CM annihilator forcing:

```text
W_axis(B) ∩ span_C{1,theta,theta^2}^perp ≠ {0}.
```

That is why the annihilator formulation is now the right proof target.
