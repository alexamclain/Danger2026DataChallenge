# P25 KSY-y Koo-Shin II Section 5 Delta Boundary

Updated: 2026-06-14 07:39 PDT

## Purpose

The supplied arXiv sequel is not the missing Koo-Shin 2010 paper, but its
Section 5 has real prime-power class-field content.  This note records the
usable part and the boundary: it is context, not a p25 product producer.

## Source

```text
supplied_pdf = /Users/agent/Downloads/1007.2318v1.pdf
extracted_text = /tmp/p25_lit_scout/koo_shin_supplied_1007_2318_text.txt
title = On some arithmetic properties of Siegel functions (II)
arxiv = 1007.2318v1
```

## Section 5 Rows

```text
Section 5 setup:
  window = extracted_text:1516-1566
  positive = generators of class fields with prime-power conductors using
             singular values of Delta and Siegel-Ramachandra invariants
  boundary = CM/ring-class-field generator context, not finite p25 P

Theorem 5.1:
  window = extracted_text:1568-1649
  positive = a norm of the Siegel-Ramachandra invariant g_f(C0) generates an
             abelian extension L/K under prime-power conductor and degree
             hypotheses
  boundary = class-field generator via Artin characters, not p25 row labels

Lemma 5.3:
  window = extracted_text:1653-1705
  positive = prod_{w=1..N-1} g_(0,w/N)^12 equals
             N^12 Delta(N tau)/Delta(tau)
  boundary = one-axis full-residue Siegel product, with no C_3 row graph,
             D/K trace, or p25 orientation

Theorem 5.4:
  window = extracted_text:1707-1777
  positive = p^12 Delta(p^ell theta)/Delta(p^(ell-1) theta) is a real
             algebraic integer generating a ring class field when p is inert
             or ramified
  boundary = CM singular-value generator for prime-power conductor, not a
             challenge-legal finite-field identity or 75-atom normalized-y
             product
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_ii_section5_delta_boundary_gate.py
```

Expected marker:

```text
ksy_y_koo_shin_ii_section5_delta_boundary_rows=1/1
```

## Verdict

Koo-Shin II Section 5 is a useful cousin: it confirms that Koo/Shin use
prime-power Siegel/Delta product identities to build class-field generators.
But its visible product is one-axis and Delta-based.  It does not supply exact
`P`, the mixed `C_3 x C_169` row graph, equal weights over the p25 atoms, or
the required orientation.

The missing paper remains:

```text
Koo and Shin, On some arithmetic properties of Siegel functions
Math. Z. 264 (2010), 137-177
Section 5 / Theorem 5.2
```
