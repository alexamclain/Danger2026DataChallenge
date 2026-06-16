# p24 Right/C Bidegree Support Gate

Date: 2026-06-07

## Point

After the `B/C` trace, the surviving packet lives on two quotient axes:

```text
right quotient: C_7
internal C/E:   C_179
```

The final `C/E` trace of a nontrivial right projector is exactly the
`C/E`-trivial bidegree in that right channel.  Thus the remaining theorem is:

```text
for k=1,...,6, the bidegree (right character k, C-character 0) vanishes.
```

This is the same as the projector/internal-character target, but it names the
precise forbidden Fourier slots.

## Important Warning

Since

```text
gcd(7,179)=1,
```

there is no nontrivial group homomorphism from the right quotient `C_7` to the
internal `C_179` character group.  So a proof cannot be mere quotient graph
bookkeeping.  If the actual packet avoids the trivial `C/E` character in
nontrivial right channels, that separation must come from the selected
trace-GCD weighted/section-aware CM packet.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_c_bidegree_support_gate.py
```

Key markers:

```text
bidegree_projector_commutation_failures=0
final_trace_iff_no_trivial_C_bidegree_failures=0
random_packets_with_trivial_C_leakage=48/48
forced_no_trivial_C_bidegree_passes=48/48
graph_nontrivial_C_support_final_trace_zero=1
trivial_C_support_leaks=1
trivial_C_forbidden_bidegrees_nonzero=6/6
p24_has_no_nontrivial_group_hom_from_C7_to_C179=1
remaining_theorem_is_vanishing_of_right_nontrivial_C_trivial_bidegrees=1
```

## Consequence

The proof frontier is now an exact bidegree support theorem:

```text
The selected weighted CM/Lang packet has no Fourier support in
  C_7^nontrivial x {trivial C/E character}
after the B/C trace.
```

That is the arithmetic identity that would feed the projector-trace pipeline
and hence the sub-sqrt H-coset verifier.
