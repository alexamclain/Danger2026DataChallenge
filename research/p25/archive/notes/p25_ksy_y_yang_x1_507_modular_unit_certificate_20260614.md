# P25 KSY-y Yang X1(507) Modular-Unit Certificate

Updated: 2026-06-14 08:55 PDT

## Source

Yifan Yang, `Modular unit and cuspidal divisor class groups of X_1(N)`:
<https://arxiv.org/pdf/0712.0629>.

Relevant source clauses:

```text
Proposition 2:
  for odd N, product E_g^e_g is modular on Gamma_1(N) if
  sum e_g = 0 mod 12 and sum g^2 e_g = 0 mod N.

Lemma 4 / Yu orbit condition:
  for composite N, the signed orbit sums over prime divisors control whether
  the product lies in the cusp-over-infinity modular-unit group.

Lemma 5:
  if N = nM, then product_{k=0}^{n-1} E^{(N)}_{kM+a} = E^{(M)}_a.
```

## P25 Unit

The six quotient cells from the p25 K-trace descent define:

```text
U_507 = E_25 E_197 E_369 / (E_138 E_310 E_482)
```

Residues:

```text
25   -> +1
197  -> +1
369  -> +1
138  -> -1
310  -> -1
482  -> -1
```

## Certificate

Odd-level modularity congruences:

```text
N = 507
sum e_g mod 12     = 0
sum g^2 e_g mod N  = 0
```

Signed orbit condition:

```text
prime factors of 507 = 3, 13
signed orbit bad counts:
  3  -> 0
  13 -> 0
```

Controls:

```text
unsigned orbit bad counts:
  3  -> 6
  13 -> 6

general even-N formula controls fail:
  sum g e_g mod 2        = 1
  sum g^2 e_g mod 2N     = 507
```

The controls are useful guardrails.  This is specifically the odd-level,
signed-quotient Yang/Yu certificate, not an unsigned or even-level shortcut.

## Verdict

Positive payload:

```text
the six-cell quotient packet is a Yang/Yu-compatible modular unit product on
X_1(507)
```

First missing clause:

```text
no source theorem yet identifies this X_1(507) unit with the KSY normalized-y
finite product/value plus period-156 and DANGER3 extraction data
```

Practical effect:

```text
future source hits should connect KSY normalized-y or value identities to this
exact U_507 unit, not merely prove modular-unit admissibility
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_x1_507_modular_unit_certificate_gate.py
```

Marker:

```text
ksy_y_yang_x1_507_modular_unit_certificate_rows=1/1
```
