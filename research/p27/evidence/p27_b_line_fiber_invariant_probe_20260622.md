# P27 B-Line Fiber Invariant Probe

Date: 2026-06-22

## Claim

The coordinated A/B/K/Sroot class now has a smaller finite-field fiber model,
but the obvious symmetric invariants of that fiber do not expose a low-cost
selector for `f3(B)`.

For each legal B in q1607/q1847/q2087, the next-root fiber has:

```text
32 root occurrences
8 distinct next x-values
closure under x -> 1/x
4 distinct u-values, where u = x + 1/x
chi(u + 2) = f3(B) for all four u-values
```

This confirms the expected `u+2` gate structure inside the B-line fiber.  The
negative result is that norm, trace, power-sum, and low-degree coefficient
views do not turn that structure into a source-normalized shrink.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_fiber_invariant_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_fiber_invariant_probe_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_fiber_invariant_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_fiber_invariant_probe_20260622.txt
```

## Results

Fiber shape:

```text
q1607: B groups 49, occurrences 32 each, unique x roots 8 each, unique u roots 4 each
q1847: B groups 63, occurrences 32 each, unique x roots 8 each, unique u roots 4 each
q2087: B groups 57, occurrences 32 each, unique x roots 8 each, unique u roots 4 each
```

Symmetries:

```text
reciprocal_closed_True = all B groups
negation_closed_False = all B groups
occurrence_product_chi_1 = all B groups
unique_product_chi_1 = all B groups
u_plus_2_matches_f3 = all B groups
```

Power-sum selectors:

```text
x_power_sum_exact_hits = none       for exponents 1..64
reciprocal_power_sum_exact_hits = none
x_power_sum_near_75pct = none
reciprocal_power_sum_near_75pct = none
```

Coefficient interpolation on the legal-B set:

```text
q1607:
  x polynomial degree 8, coefficient degrees [0,48,48,48,48,48,48,48]
  u polynomial degree 4, coefficient degrees [48,48,48,48]

q1847:
  x polynomial degree 8, coefficient degrees [0,62,62,62,62,62,62,62]
  u polynomial degree 4, coefficient degrees [62,62,62,62]

q2087:
  x polynomial degree 8, coefficient degrees [0,56,56,56,56,56,56,56]
  u polynomial degree 4, coefficient degrees [56,56,56,56]
```

Only the constant term of the 8-root x-polynomial is low-degree on legal B;
it has squareclass `+1` and is not the selector.  The four-u polynomial has no
coefficient of degree `<= 8` on the legal-B set in any guard field.

## Interpretation

Positive:

```text
The d3 fiber over B has a concrete smaller model: an 8-root reciprocal x-cover
or a 4-root u-cover.
The equality f3=chi(u+2) holds uniformly on the reduced fiber.
This is a better CAS target than the full 32-occurrence source fiber.
```

Negative:

```text
The full norm/product is a square in every tested B fiber.
Power sums through exponent 64 do not recover f3, even up to global polarity.
The four-u cover coefficients look maximally varying on the legal-B set.
There is no new GPU sampler or one-line recurrence from these symmetric
invariants.
```

## Continue / Kill

```text
continue = normalize the 4-u / 8-x fiber cover over legal B
continue = compute genus, components, and quotient maps for this reduced cover
continue = compare f4/f3 only after the reduced f3 cover is understood

kill = norm/trace/power-sum selector for the B-line d3 fiber
kill = GPU B-fiber production from symmetric invariants alone
kill = low-degree coefficient interpolation on legal B as the next shortcut
```

```text
p27_b_line_fiber_invariant_probe_rows=1/1
```
