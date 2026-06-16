# P25 KSY-y Yang Y_507 Conductor-39 Doubling-Orbit Norm

Updated: 2026-06-14 10:20 PDT

## Result

The compact coset quotient

```text
Q = prod_{h in <2>} E_{7h}/E_h
```

is exactly the 12-step doubling-orbit norm of one seed ratio:

```text
R = E_7 / E_1
Q = prod_{i=0..11} [2]^i R
```

In exponent notation:

```text
seed word R       = E_7 / E_1 = ((1,-1),(7,+1))
orbit length      = 12
orbit support     = 24
orbit norm        = U_chi = 1_{7<2>} - 1_{<2>}
```

There is no cancellation in the orbit norm.

## Frobenius Boundary

For the ordered cycle `h_i=2^i`, Frobenius acts by:

```text
Frob_p(h_i)    = 7 h_{i+11}
Frob_p(7 h_i) = h_{i+9}
```

So a single seed ratio does **not** descend by itself.  Its Frobenius image is
a skew inverse pair, not its own inverse:

```text
Frob_p(E_7/E_1) != (E_7/E_1)^-1
```

But the full doubling-orbit norm does descend:

```text
Frob_p(Q) = Q^-1
Q^6 = (1 - Frob_p)(Q^3)
```

## Interpretation

This gives the cleanest current theorem-facing source request:

```text
produce the 12-step doubling-orbit norm of E_7/E_1 on X_1(39),
then apply W=6*U_chi and the 13-fiber Yang distribution to X_1(507)
```

Reject single-seed descent claims unless they also supply the full orbit norm
or another boundary that repairs the skew Frobenius pairing.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_doubling_orbit_norm_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_doubling_orbit_norm_rows=1/1
```
