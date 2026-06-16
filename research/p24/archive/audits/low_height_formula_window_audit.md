# Low-height formula window audit

This closes a softer version of the low-height formula idea.

Earlier probes tested exact formulas such as

```text
A = f(n),    A^2 = f(n),    j = f(n)
```

for `p=n^2+7`.  A possible asymptotic shortcut would not need an exact formula:
it could scan a small moving interval

```text
|A - f(n)| <= W(p)
```

around a simple formula `f`, provided `W=o(sqrt(p))` and the window captured a
non-negligible share of strict parameters.

## Exact calibration

I added:

```text
p24/low_height_formula_window_audit.py
```

It computes the exact strict-good `A` mask for small near-square primes and
tests low-height LFT centers

```text
f(n) = (a*n+b)/(c*n+d)
```

using circular interval prefix sums.  This makes each formula/window query
constant-time after the exact trace mask is built.

Run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/low_height_formula_window_audit.py \
  --min-p 10000 --max-p 180000 --max-rows 10 \
  --coeff-bound 3 \
  --betas 0.20 0.25 0.30 0.40 0.50 \
  --fixed 8 16 32 64 128 --top 16
```

Aggregate:

```text
formula_count=1008
good=10482/360626
base_rate=0.02906612
```

Best by score:

```text
p^0.50 last_width=248 hits=147/3722
capture=0.014024 lift=1.359 coverage=0.010321
formula=(1*n+-2)/(-3*n+-1)
```

Best lift with at least one percent capture:

```text
fixed_128 last_width=128 hits=106/2570
capture=0.010113 lift=1.419 coverage=0.007126
formula=(2*n+3)/(-3*n+1)
```

## Interpretation

This is constant-factor behavior.  Even `W ~= sqrt(p)` windows capture only
about one percent of the strict-good set in this calibration range, and the
best lifts are around `1.4`.  Sub-sqrt windows do not retain enough mass to be
an exponent-changing sampler.

```text
conclusion=low_height_formula_windows_show_no_subsqrt_capture_concentration
```

This complements the exact formula probes:

```text
p24/near_square_formula_probe.py
p24/quadratic_near_square_parameter_probe.py
p24/implicit_quadratic_section_probe.py
p24/legendre_near_square_parameter_probe.py
p24/torus_lft_parameter_probe.py
```

Those rule out exact low-height sections; this audit rules out small
neighborhoods around such sections at exact small scale.
