# Near-singular window audit

This tests a verifier-native route distinct from CM root selection.

The singular Montgomery parameters

```text
A = +/-2
```

degenerate to rational torus power maps.  They are rejected by the verifier
and for p24 have only

```text
v2(p-1)=1, v2(p+1)=3.
```

Still, a possible asymptotic speedup would be concentration near the singular
points: if strict DANGER parameters for `p=n^2+7` lived in a window

```text
min(|A-2|, |A+2|) <= W
```

with `W=o(sqrt(p))` and non-negligible capture, then scanning that window
would beat generic trace search.

## Exact calibration

I added:

```text
p24/near_singular_window_audit.py
```

Run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_singular_window_audit.py \
  --min-p 10000 --max-p 180000 --max-rows 10 \
  --betas 0.10 0.20 0.25 0.30 0.40 0.50 \
  --fixed 4 8 16 32 64 128
```

Aggregate output:

```text
good=10482/360626
base_rate=0.02906612

p^0.10     hits=    0/      72 capture=0.000000 lift=0.000 coverage=0.000200
fixed_4    hits=    2/     110 capture=0.000191 lift=0.626 coverage=0.000305
fixed_8    hits=    4/     190 capture=0.000382 lift=0.724 coverage=0.000527
p^0.20     hits=    4/      87 capture=0.000382 lift=1.582 coverage=0.000241
p^0.25     hits=    6/     290 capture=0.000572 lift=0.712 coverage=0.000804
fixed_16   hits=   12/     350 capture=0.001145 lift=1.180 coverage=0.000971
p^0.30     hits=   12/     478 capture=0.001145 lift=0.864 coverage=0.001325
fixed_32   hits=   16/     670 capture=0.001526 lift=0.822 coverage=0.001858
fixed_64   hits=   30/    1310 capture=0.002862 lift=0.788 coverage=0.003633
p^0.40     hits=   30/    1191 capture=0.002862 lift=0.867 coverage=0.003303
fixed_128  hits=   72/    2590 capture=0.006869 lift=0.956 coverage=0.007182
p^0.50     hits=  108/    3742 capture=0.010303 lift=0.993 coverage=0.010376
```

## Interpretation

The windows behave like random slices of the `A`-line.  By `W ~= sqrt(p)`,
capture is essentially the same as coverage and lift is about `1`.  Smaller
windows sometimes show noisy row-level lifts, but aggregate capture is tiny
and there is no growth pattern.

Thus the singular torus does not appear to perturb into a sub-sqrt scan
window for the strict verifier.

```text
conclusion=near_singular_windows_show_no_subsqrt_capture_concentration
```

This complements:

```text
p24/torus_degeneration_audit.py
p24/torus_lft_parameter_probe.py
```

The first rules out the exact singular torus; the second rules out simple
torus-coordinate formulas.  This audit rules out the remaining window-scan
version at exact small scale.
