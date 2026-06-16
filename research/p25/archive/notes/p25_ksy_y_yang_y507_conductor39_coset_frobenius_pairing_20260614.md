# P25 KSY-y Yang Y_507 Conductor-39 Coset Frobenius Pairing

Updated: 2026-06-14 10:12 PDT

## Result

Let

```text
H = <2> in (Z/39Z)^*
Q = prod_{h in H} E_{7h} / E_h
U_chi = 1_{7H} - 1_H
```

For p25:

```text
p mod 39 = 23 = 7 * 2^11
p * 7   = 5  = 2^9
p^2     = 22 = 2^8
```

So on the ordered 12-cycle `h_i = 2^i`:

```text
Frob_p(h_i)      = 7 h_{i+11}
Frob_p(7 h_i)   = h_{i+9}
Frob_p^2(h_i)   = h_{i+8}
Frob_p^2(7 h_i) = 7 h_{i+8}
```

Thus Frobenius swaps numerator and denominator layers:

```text
Frob_p(U_chi) = -U_chi
Frob_p(Q)     = Q^-1
```

and the period-norm word has the explicit Hilbert-90 form:

```text
W = 6 * U_chi = (1 - Frob_p)(3 * U_chi)
```

Equivalently, in value language:

```text
Q^6 = (1 - Frob_p)(Q^3)
```

## Interpretation

This is the descent contract for the compact coset quotient.  A value-side
theorem can target a norm-one quotient `Q` with `Frob_p(Q)=Q^-1`, or an
explicit Hilbert-90 preimage whose boundary is `Q^6`.

This still does not supply the finite-field value/divisor theorem, DANGER3
framing, `(A,x0)` extraction, or official `vpp.py` verification.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_coset_frobenius_pairing_rows=1/1
```
