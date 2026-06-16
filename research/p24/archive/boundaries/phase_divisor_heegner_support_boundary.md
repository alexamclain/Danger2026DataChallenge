# Phase Divisor Heegner-Support Boundary

Date: 2026-06-05

This note records a small falsification test for the easiest
Borcherds/Schofer-style p-unit route.

## Question

The phase-aware Borcherds candidate would be more credible if the packet scalar
already looked like a divisor with Heegner or cuspidal support in small CM
examples.  A cheap diagnostic is:

```text
1. interpolate the packet scalar as a rational function of the selected j;
2. factor its numerator/denominator over F_q;
3. compare numerator roots against target CM roots and small Heegner roots.
```

This does not test every possible Borcherds product.  It only tests the easy
explanation:

```text
the phase-aware packet norm is already a simple Heegner-supported divisor in j.
```

## Tool

The diagnostic is:

```text
p24/phase_divisor_heegner_support_scan.py
```

It uses small full CM cycles, computes a minimal rational interpolant for the
packet scalar, and compares numerator roots with reductions of Hilbert class
polynomials for bounded fundamental discriminants.

## Runs

Non-genus Hermitian row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/phase_divisor_heegner_support_scan.py \
  --D -2239 --q 2243 --ell 2 --m 7 --factor-index 0 \
  --scalar hermitian --max-heegner-abs-D 3000 --max-heegner-h 30
```

reported:

```text
h=35, m=7, n=5, factor_degree=4
rational_degree=18
numerator_roots=[940,1191]
denominator_roots=[141,1711]
numerator_roots_in_target_cm=[]
heegner_discriminants_tested=48
heegner_roots_total=357
heegner_hits=0/2.
```

The ordinary autocorrelation control on the same row is invariant:

```text
rational_degree=0
numerator_roots=[]
denominator_roots=[].
```

Sibling non-genus row:

```text
D=-2239, q=2243, ell=2, m=5, n=7, scalar=hermitian:
  factor_degree=6
  rational_degree=17
  numerator_roots=[]
  denominator_roots=[].
```

Calibrated `D=-5000` row:

```text
D=-5000, q=1259, ell=3, m=10, n=3, scalar=hermitian:
  rational_degree=15
  numerator_roots=[285,564]
  numerator_roots_in_target_cm=[]
  small_heegner_hits=1/2, at D=-935.
```

The single small-Heegner collision is not a supported-divisor pattern: the
other numerator root is generic, and neither root is in the target CM set.

## Consequence

The tautological phase packet divisor does not look Heegner-supported in the
plain `j` coordinate.  This strengthens the earlier divisor-shape result:

```text
plain j degree is generic;
oriented edge degree is generic;
plain j numerator support is generic or absent.
```

Therefore a Borcherds/Schofer/Lauter-Viray proof would need to construct a
genuinely phase-aware divisor, not merely recognize the interpolated scalar as
a low-degree or small-Heegner-support modular function.

The arithmetic p-unit target remains:

```text
prove the named packet norm / representative Moore determinant is a p-unit at
p = 10^24 + 7.
```
