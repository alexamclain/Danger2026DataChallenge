# P25 KSY-y Atom Terminology Guardrail

Updated: 2026-06-14 08:30 PDT

## Purpose

This note prevents a misleading reading of `75 atoms`.

In this workbench, a normalized-y atom is a fixed factor inside the target
product, not a practical search candidate.

## Meaning

The target product is:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

There are:

```text
3 D-segment positions
25 K-trace positions
3 * 25 = 75 fixed normalized-y atoms
```

Each atom is one fixed factor-pair:

```text
y(Q)/y(-Q), where Q=C+jD+kK
```

KSY's formula

```text
y(Q) = -g(2Q)/g(Q)^4
```

expands each normalized-y atom into four Siegel-footprint terms, giving the
recorded `300`-term theta2/theta2-inverse footprint.

## Guardrail

The moonshot theorem target is not to try 75 candidates.  It is to find or
prove an arithmetic identity that selects the whole fixed 75-atom product with
the correct orientation and challenge-legal finite-field framing.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_atom_terminology_guardrail_gate.py
```

Marker:

```text
ksy_y_atom_terminology_guardrail_rows=1/1
```
