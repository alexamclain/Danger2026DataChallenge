# P25 KSY-y Yang Y507 Conductor-39 Hilbert-90 Sparse Selector Structure

Updated: 2026-06-14 10:52 PDT

## Result

The four legal support-`12` Hilbert-90 gauges have a compact selector form.
Let the four Frobenius orbits be:

```text
O0 = (1, 23, 22, 38, 16, 17)
O1 = (2, 7, 5, 37, 32, 34)
O2 = (4, 14, 10, 35, 25, 29)
O3 = (8, 28, 20, 31, 11, 19)
```

Multiplication by `2` cycles them:

```text
O0 -> O1 -> O2 -> O3 -> O0
```

Multiplication by `4` swaps opposite classes:

```text
O0 <-> O2
O1 <-> O3
```

The legal sparse gauges are exactly the sign selectors

```text
s = (s0, s1, -s0, -s1),  s0,s1 in {+1,-1}
V_s(r) = 3 * (s([r]) - chi_39(r)).
```

Thus they are anti-invariant under multiplication by `4` on the Frobenius
quotient.

## Mixedness

All four legal sparse gauges preserve the conductor-`39` mixedness:

```text
pushforward mod 3  = 0
pushforward mod 13 = 0
```

The all-positive/all-negative one-coset sparse gauges fail this selector law;
their proper-axis pushforwards are nonzero, and they remain formal controls.

## Intake

A theorem hit may target a legal sparse gauge by giving this quotient sign
selector.  A one-coset sparse support statement is still rejected unless it
comes with a separate Hilbert-90 ratio/boundary explaining why the formal gauge
is allowed.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_rows=1/1
```
