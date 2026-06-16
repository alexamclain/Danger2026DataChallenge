# Actual-CM Projector/Internal-Character Boundary

This checks a tempting but false strengthening of the current p24 target.

False strengthening:

```text
nontrivial quotient projector
  => zero trivial C/E component after B/C trace.
```

The calibration uses the small embedded CM row:

```text
D = -5000
h = 30 = 2 * 5 * 3
top quotient = 2
C/E analogue = 5
B/C analogue = 3
```

For each origin, the nontrivial top projector is the difference between the
two top packets.  Its `B/C` trace is nonzero, and its final internal trace is
usually nonzero.

Latest markers:

```text
projected_B_over_C_trace_nonzeroes=30/30
projected_final_trace_zeroes=0/30
projected_final_trace_nonzeroes=30/30
raw_top_final_trace_zeroes=0/60
```

So the p24 theorem cannot be merely:

```text
Pi_m is nontrivial, therefore its final internal trace vanishes.
```

It must use the actual weighted right/G_chi packet structure.
