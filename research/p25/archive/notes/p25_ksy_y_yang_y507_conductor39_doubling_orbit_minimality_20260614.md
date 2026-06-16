# P25 KSY-y Yang Y_507 Conductor-39 Doubling-Orbit Minimality

Updated: 2026-06-14 10:28 PDT

## Result

The full `12`-step doubling-orbit norm of `E_7/E_1` is forced by
Yang/Yu modular-unit legality on `X_1(39)`.

All proper doubling suborbit norms were checked:

```text
proper suborbit rows          = 27
proper legal rows             = 0
full orbit rows               = 1
legal rows                    = 1
proper elementary rows        = 9
proper signed-orbit failures  = 9
```

The full orbit is the only legal row:

```text
length = 12
support = 24
signed orbit bad counts = ((3,0),(13,0))
equals U_chi = true
```

## Boundary

The seed ratio and every proper suborbit are killed as standalone `X_1(39)`
modular units:

```text
length 1 and 2:
  fail quadratic congruence modulo 39

length 3, 4, and 6:
  pass elementary congruences
  fail Yang/Yu signed orbit condition at prime 3
```

So a theorem may use the seed ratio `E_7/E_1` only inside the full
`12`-step doubling-orbit norm, or it must provide an explicit boundary/ratio
that repairs the failed legality.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_doubling_orbit_minimality_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_doubling_orbit_minimality_rows=1/1
```
