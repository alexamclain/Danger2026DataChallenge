# Trace-GCD Phase-Unit Dictionary Boundary

Date: 2026-06-06

This note records a bounded attempt to recognize the actual trace-GCD
right-phase determinant sequence as a product of simple phase-aware units.

## Pinned Row

The row is the same faithful small CM row used by the norm-triangle and
orbit-norm audits:

```text
D=-13319, q=13463, h=140, m=28, n=5,
left=4, right=7.
```

The phase-coordinate scan reports exact descent to the right phase algebra:

```text
right_class_mismatches=0
phase_compression_factor=20
```

For the two omitted rows, the right sequences are:

```text
omitted=0:
  [2125, 6973, 11434, 2597, 12105, 2133, 3022]

omitted=1:
  [11423, 4693, 4157, 13397, 8480, 3228, 8474]
```

Both have one full nonzero DFT orbit of support:

```text
omitted=0: support [3,5,6]
omitted=1: support [1,2,4]
```

This is a genuine small-row simplification, but it is not expected to lift to
p24: for `right=211`, `tail=16`, the p24 exterior support is already all of
`Z/211Z` by distinct 3-subset sums.

## Unit-Span Attempt

The bounded dictionary was:

```text
right-binomial units:
  Norm_O(1 - c*zeta_7^(k*t)), c <= 20;

small Heegner-fiber units:
  products over visible phase fibers, |D| <= 1000, h <= 20.
```

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_chow_phase_divisor_span_scan.py \
    --random-controls 5 \
    --max-binomial-constant 20 \
    --max-heegner-abs-D 1000 \
    --max-heegner-h 20 \
    --all-omitted
```

The dictionary has size `173`.  In discrete-log coordinates modulo the prime
factors of `q-1 = 13462`, it reports:

```text
q_minus_1_prime_factors=[2, 53, 127]

omitted=0:
  mod 2:   dictionary_rank=3/7, target_in_span=0
  mod 53:  dictionary_rank=7/7, target_in_span=1
  mod 127: dictionary_rank=7/7, target_in_span=1

omitted=1:
  mod 2:   dictionary_rank=3/7, target_in_span=0
  mod 53:  dictionary_rank=7/7, target_in_span=1
  mod 127: dictionary_rank=7/7, target_in_span=1
```

The odd-log containment happens only at full ambient rank, and the mod-2
component is not captured.  This is interpolation in unit coordinates, not a
product formula.

## Consequence

The pinned row still supports the Fitting p-unit theorem because its six
actual orbit norms are nonzero.  But the obvious product route

```text
actual trace-GCD phase determinant
  = product of small right-binomial and low-Heegner fiber units
```

does not survive this bounded check.

The missing theorem therefore remains genuinely phase-aware:

```text
construct the trace-GCD Fitting/Borcherds section itself, or prove directly
that its seven p24 orbit norms have zero local intersection at the selected
ordinary CM point.
```
