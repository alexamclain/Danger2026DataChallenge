# P25 KSY-y Yang X1 Orbit-Distribution Bridge

Updated: 2026-06-14 08:50 PDT

## Source

Yifan Yang, `Modular unit and cuspidal divisor class groups of X_1(N)`:
<https://arxiv.org/pdf/0712.0629>.

Relevant source handle:

```text
Lemma 5:
  if N = nM, then product_{k=0}^{n-1} E^{(N)}_{kM+a} = E^{(M)}_a
```

## P25 Instantiation

The p25 raw K trace has exactly this shape:

```text
N = 12675
M = 507
n = 25
K step = 507 mod 12675
raw coordinate step = (507 mod 75, 507 mod 169) = (57, 0)
```

The six quotient cells are the already-audited row-labeled packet:

```text
row 0: c31 - c138
row 1: c25 - c141
row 2: c28 - c144
```

Expanding each quotient cell by the Yang orbit
`a, a+507, ..., a+24*507` reconstructs the exact raw 150-factor K-trace source
mask.

The quotient packet also passes the Yang/Yu signed orbit condition at the prime
divisors of `507`:

```text
signed / +/- orbit bad counts:
  p = 3  -> 0
  p = 13 -> 0

unsigned orbit bad counts:
  p = 3  -> 6
  p = 13 -> 6
```

The unsigned failure is a useful control: the source condition is genuinely the
orbit condition on `(Z/NZ)/+/-`.

## Verdict

Positive payload:

```text
the 25-point K trace is not mysterious; it is the standard X_1(N) orbit
distribution descent from level 12675 to level 507
```

First missing clause:

```text
Yang's relation is one-dimensional E_a modular-unit distribution.  It does not
prove the remaining six-cell KSY normalized-y product/value identity, the
period-156 context, DANGER3 framing, or extraction.
```

Practical effect:

```text
future theorem search should focus on the six row-labeled quotient pairs, not
on rediscovering the raw 150-factor K trace
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_x1_orbit_distribution_bridge_gate.py
```

Marker:

```text
ksy_y_yang_x1_orbit_distribution_bridge_rows=1/1
```
