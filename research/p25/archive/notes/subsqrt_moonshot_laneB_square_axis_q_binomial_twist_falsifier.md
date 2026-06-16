# Subsqrt Moonshot Lane B Square-Axis q-Binomial Twist Falsifier

Date: 2026-06-12

## Result

The Lucas/binomial support clue survives the natural q-binomial upgrade, but
the all-one payload does not.

On the tiny `h,t <= 2` triangle,

```text
[2 choose 1]_q = 1 + q
```

so the q-binomial seed has coefficients

```text
[1, 1, 1, 1, 1+q, 1].
```

The all-one seed forces `q = 0`.  That is the degenerate Boolean/Pascal
support limit, not a multiplicative character or root-of-unity parameter.

## Exhaustive Finite Checks

The gate checks all nonzero `q` in `F_3`, `F_5`, and `F_2029`, and all `507`th
roots of unity in `F_2029`.

For every unit `q` with correct support:

```text
q-binomial residual = target + q*S*X^3Y
```

The mismatch orbit is always

```text
138, 310, 482
```

No unit `q` gives the all-one payload, and no global, scalar, or separable
`h/t/S` rescaling flattens it.

## Producer Consequence

This keeps the Lucas support as a useful positive hint but rules out a
straight Gaussian-binomial / q-Pascal producer.  A viable ray-local producer
must either explain a real mixed twist that cancels the `q*S*X^3Y` orbit, or
arrive at the all-one payload by a different mechanism.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_q_binomial_twist_falsifier_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_q_binomial_twist_falsifier_gate.py
```
