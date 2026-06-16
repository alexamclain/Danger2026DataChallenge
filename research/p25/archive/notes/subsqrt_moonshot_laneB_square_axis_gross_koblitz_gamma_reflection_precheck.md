# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Gamma Reflection Precheck

Date: 2026-06-13

## Result

Reflection alone does not produce the anomaly projector.

For the naive Jacobi gamma divisor:

```text
U(A) + U(B) - U(A+B)
A = t*N/3
B = (h-t mod 3)*N/3
N = 507
```

and the odd/even `p^2` half-orbit difference, using:

```text
p^39 = -1 mod 507
U(-x) = -U(x) up to sign/Teichmuller factors
```

the reflected residual is nonzero exactly on:

```text
(1,2):  +234 * U(169)
(2,1):  -234 * U(169)
```

All other seed cells vanish.

## Consequence

This is not the desired one-cell projector.  It is a signed two-cell residue:
the target anomaly `(2,1)` plus the false positive `(1,2)`.

So the HD/GK route remains alive only if the next multiplication/unit step
does real work:

- remove the `(1,2)` false positive,
- account for the remaining free `U(169)` symbol,
- and turn the signed residual into an arithmetic unit phase or point
  correction.

Reflection by itself is now killed as a complete explanation.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py
```
