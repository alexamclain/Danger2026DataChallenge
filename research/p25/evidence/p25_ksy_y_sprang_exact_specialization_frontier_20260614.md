# P25 KSY-y Sprang Exact-Specialization Frontier

Updated: 2026-06-14 08:14 PDT

## Purpose

The post-Koo-Shin reroute made Sprang/Kronecker `D=2` the first theorem front
door.  The distribution-shape boundary then killed broad kernel/torsion
interpretations.  This checkpoint decides what remains actionable.

## Target Checksum

```text
positive = ((0,31), (1,25), (2,28))
negative = ((0,138), (1,141), (2,144))
support  = 6
D        = (1,3)
ord(D)   = 507
3D       = (0,9)
T        = (2,113)
```

The three positive atoms are a short mixed-level arithmetic segment.  They are
not a subgroup/coset distribution.

## Sprang Boundary

Current Sprang source clauses remain useful vocabulary, but not direct p25
payloads:

```text
Sprang 1801 even-D omega surface
  keep as vocabulary, not payload
  missing exact base, D-segment, T edge, orientation, and K trace

Sprang 1801 distribution over kernels/torsion translations
  kill literal kernel-distribution closer
  finite falsifier: ord(D)=507 and 3D=(0,9)

Sprang D=2 nonzero torsion shadow
  kill literal D=2 torsion-image closer
  finite falsifier: every hom C2 x C2 -> C3 x C169 is zero, so support maps
  to one point rather than the row-labeled triple

Sprang 1802 Kato-Siegel theta_D comparison
  kill direct thetaD2 import
  blocker: displayed Kato-Siegel comparison is prime-to-6

Sprang 1802 cohomology/Eisenstein formula
  kill as direct product closer
  missing finite P/theta2 divisor or value identity
```

## Live Row

Sprang continues only on a named source theorem or formula hit that emits:

```text
exact mixed C3 x C169 row-labeled positive layer
T-translate orientation
K-traced P/theta2 or theta2-inverse payload
challenge-legal finite-field framing
```

Without that new source hit, the active theorem search should move to the next
front door: Kubert-Lang / KSY exact product.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_exact_specialization_frontier_gate.py
```

Marker:

```text
ksy_y_sprang_exact_specialization_frontier_rows=1/1
```
