# p25 Lane C W_axis Pilot

Updated: 2026-06-12

## Result

Lane C remains a theorem microscope, not a producer, but the first finite
falsifier did not kill it.

The exact p25 accounting is:

```text
positive trace: n=505027, dim(W_axis)=336, ord_n(p)=252513, surface=169688736
middle trace:   n=13620867859, dim(W_axis)=15, ord_n(p)=6810433929, surface=204313017870
negative trace: n=2031=3*677, dim(W_axis)=298, ord_n(p)=338, surface=402896
```

All three rank surfaces are below:

```text
sqrt_floor = 3162277660168
```

The negative trace is the smallest surface.  Its largest-prime-only shortcut is
killed:

```text
n=677: ord_677(p)=169 < dim(W_axis)=298
```

So the bundled axis `n=2031` is necessary for the first p25-native Lane C
target.

## First Falsifier Run

Command run from `/Users/agent/Documents/Codex`:

```sh
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  python3 Danger2026DataChallenge/p24/l1_axis_injectivity_scan.py \
  --max-cases 40 --min-h 20 --max-h 1200 --max-abs-D 200000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 2031 --q-stop 500000 \
  --include-linear --require-deg-ge-axis-dim --summary-only
```

Observed summary:

```text
packet_rows=126
nonzero_rows=126
dimension_bound_rows=0
injective_possible_rows=126
injective_rows=126
injective_failures=0
full_k_injective_possible_rows=124
full_k_injective_rows=124
full_k_injective_failure_rows=0
rank_defect_histogram={0: 126}
```

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneC_w_axis_pilot_gate.py
```

Expected row:

```text
laneC_w_axis_pilot_rows=1/1
```

## Continue / Kill

Continue Lane C only as a low-priority theorem microscope.  The first finite
analogue scan did not find axis-injectivity failures, and the p25 negative
trace surface is tiny.  Kill the `n=677` shortcut and any claim that counts
alone are a certificate; the missing ingredient is still a p25 Moore-rank or
p-unit nonvanishing theorem, or an actual selected relative-trace producer.
