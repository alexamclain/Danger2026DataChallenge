# P25 Lane B: Robert KSY / Kato-Siegel dlog Chain Gate

Updated: 2026-06-13 14:11 PDT

## Purpose

The normalized-y projection gate showed:

```text
y-footprint = double_pushforward(bridge) - 4*bridge
```

For a logarithmic derivative in the source variable, the `g(2Q)` term receives
the chain-rule factor `2`:

```text
dlog-footprint = 2*double_pushforward(bridge) - 4*bridge
```

This gate checks whether that chain-rule factor cancels the doubled layer.

## Result

It does not cancel it.

```text
dlog footprint support = 300
coefficient counts = (-4,75), (-2,75), (2,75), (4,75)
abs(coeff)=4 layer, scaled by -1/4 -> exact bridge
abs(coeff)=2 layer, scaled by 1/2  -> doubled bridge, wrong trace
```

For combinations

```text
dlog_footprint + lambda*doubled, -6 <= lambda <= 6
```

only `lambda=-2` reduces support to `150`, giving `-4*bridge`; exact division
by `-4` then recovers the bridge.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_dlog_chain_gate.py
```

Expected marker:

```text
robert_ksy_dlog_chain_rows=1/1
```

## Interpretation

The Kato-Siegel `dlog` route is still live, but the ordinary chain-rule factor
alone does not solve it.  A theorem candidate must provide exact doubled-layer
cancellation, or an equivalent identity that prevents the `g(2Q)` contribution
from surviving as payload.
