# p24 Admissible Jacobi Spectral Boundary

Date: 2026-06-07

## Point

The admissible Jacobi theorem should not be treated as a black-box
rank-`621` membership test.  This boundary computes its Fourier-side
fingerprint in small exact models `C_7 x C_c`.

## Result

For `c=5,11,13`, the admissible carry span has:

```text
C-trivial slice rank:           1
nontrivial C-slice ranks:       all 7
conjugate C-pair ranks:         all 8, not 14
cumulative increments:          1, 7, ..., 7, 4
```

Checked rows:

```text
c=5:  rank=12, increments=[1,7,4]
c=11: rank=33, increments=[1,7,7,7,7,4]
c=13: rank=40, increments=[1,7,7,7,7,7,4]
```

The p24 extrapolation is:

```text
C-pair count = (179-1)/2 = 89
rank = 1 + 7*88 + 4 = 621
```

## Consequence

The proof target is sharper than support vanishing:

```text
for each conjugate C/E character pair,
the weighted packet must satisfy the admissible pair-compatibility relations,
with three additional terminal global relations.
```

Equivalently, proving that every nontrivial `C/E` slice has full right support
is not enough.  The hard part is compatibility between `b` and `-b` C/E
characters across the selected weighted packet.

This is a better shape for a proof or for coefficient mining:

```text
mine the selected weighted packet for conjugate-C-pair formulas,
not only for zero forbidden bidegrees.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary.py
```

No p24 CM roots or class set are enumerated.
