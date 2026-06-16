# P25 KSY-y: Sparse Hilbert-90 Yang Lift

Updated: 2026-06-14 11:15 PDT

## Purpose

The legal sparse conductor-`39` Hilbert-90 gauges are now lifted through
Yang's `13`-fiber distribution.  This gives the smallest current legal
value-side target for the conductor-`39` primary route.

## Result

Each legal support-`12` Hilbert-90 selector on `X_1(39)` lifts to a
support-`156` potential on level `507`:

```text
H_s = distribution_lift_39_to_507(V_s)
support(H_s) = 156
coefficient counts = (-6,78), (6,78)
```

Its Frobenius boundary is exactly the period norm:

```text
(1 - Frob_p) H_s = Norm_156(Y_507)
support(Norm_156(Y_507)) = 312
coefficient counts = (-6,156), (6,156)
```

This halves the lifted potential support relative to the balanced lift:

```text
balanced lifted potential support = 312
legal sparse lifted potential support = 156
```

The four legal lifted potentials are one orbit of a canonical `78/78`
Yang-fiber product under the conductor-`39` doubling subgroup.  The canonical
row is:

```text
positive residues mod 39 = {7,17,23,34,37,38}
negative residues mod 39 = {4,8,10,11,20,25}
```

expanded over all fibers `a+39k`, `k=0..12`.

## Legal Sparse Rows

The four legal selectors are the same anti-invariant quotient sign selectors:

```text
(3, 3, -3, -3)
(3, -3, -3, 3)
(-3, 3, 3, -3)
(-3, -3, 3, 3)
```

After Yang lift, all four have vanishing pushforwards to both `mod 3` and
`mod 13`, so they preserve the mixed conductor-`39` source object.

## Control

The all-positive/all-negative one-coset gauges also have the same formal
Frobenius boundary after lifting, but they remain illegal:

```text
formal positive lift support = 156, coefficients = (6,156)
formal negative lift support = 156, coefficients = (-6,156)
mod 3 pushforward = nonzero
mod 13 pushforward = nonzero
```

So boundary equality alone is not sufficient.  The value-side theorem target
must emit a legal mixed sparse selector, not a one-coset sparse lift.

## Verdict

This is a sharper theorem target, not a finish:

```text
new target = value/divisor theorem for legal support-156 H_s
normal form = canonical 78-over-78 Yang-fiber product, up to <2>-translate
boundary   = (1 - Frob_p)H_s = Norm_156(Y_507)
missing    = finite-field value/divisor theorem, DANGER3 framing, extraction
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_rows=1/1
```
