# P27 Trace/Norm Dplus H90 Quotient

Date: 2026-06-22

## Claim

The reduced relative `Dplus` cover is a cyclic-quartic/Hilbert-90 cover over
an explicit genus-1 quotient:

```text
E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1)
```

The order-4 lift is:

```text
alpha(t,z,w,s) = (t, -z, w, z*S/s)
S = (t-1)^3*(t+1)^4*(t^2+1)*(t^2+2t-1)^2
```

and:

```text
alpha^2 = s-deck involution
alpha^4 = identity
fixed quotient coordinates = t,w
```

This is the cleanest current `Dplus` moonshot object: not a GPU sampler yet,
but a degree-4 cyclic/Kummer cover over an elliptic curve.  The next theorem
test is the branch/Kummer class of this cover over `E_h90`, and whether it
recurs or couples to `d3`.

## Probes

Finite-field automorphism probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_h90_automorphism_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_automorphism_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_h90_automorphism_probe.py \
  --qs 607,1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_automorphism_probe_20260622.txt
```

Magma fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_h90_quotient_q607_magma.m
```

Magma output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quotient_q607_magma_20260622.txt
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quotient_q607_magma_20260622.xml
```

Command:

```bash
curl -sS \
  --data-urlencode input@research/p27/archive/fixtures/p27_trace_norm_dplus_h90_quotient_q607_magma.m \
  https://magma.maths.usyd.edu.au/xml/calculator.xml \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_quotient_q607_magma_20260622.xml
```

## Automorphism Check

Across `q=607,1607,1847,2087` and all four fixed sign pairs `eh,ev`, the
finite-field probe reports:

```text
alpha_invalid = 0
alpha2_not_sdeck = 0
alpha4_not_identity = 0
```

The generic affine orbit size is four.  Examples:

```text
q607:  points = 876,  orbit_size_4 = 872,  alpha_undefined = 4
q1607: points = 1604, orbit_size_4 = 1600, alpha_undefined = 4
q1847: points = 1948, orbit_size_4 = 1944, alpha_undefined = 4
q2087: points = 1956, orbit_size_4 = 1952, alpha_undefined = 4
```

The quotient coordinates are fixed as `(t,w)`.  The point/base ratios are
approximately degree `4`, with the four undefined branch points accounting for
the small affine discrepancy.

## Magma Pricing

Online Magma over `q=607` reports:

```text
RESULT h90_quotient_base 1 2 608
RESULT h90_relative_cover 1 1 17 4 8
RESULT h90_relative_cover 1 -1 17 4 8
RESULT h90_relative_cover -1 1 17 4 8
RESULT h90_relative_cover -1 -1 17 4 8
```

Meaning:

```text
E_h90 has genus 1 and degree 2 over F_q(t)
E_h90 has 608 degree-1 places over F_607
the relative Dplus cover has genus 17
the relative Dplus cover has degree 4 over E_h90
the relative Dplus cover has degree 8 over F_q(t)
the result is uniform across fixed orientation sign pairs
```

Riemann-Hurwitz for a degree-4 map `genus 17 -> genus 1` gives total
ramification contribution:

```text
2*17 - 2 - 4*(2*1 - 2) = 32
```

So the cover has the same broad shape as the earlier label-2 cyclic-quartic
lane: a genus-17 cyclic-quartic cover over an elliptic quotient.

Follow-up normalized model:
[P27 Trace/Norm Dplus H90 Quartic Model](p27_trace_norm_dplus_h90_quartic_model_20260622.md).
After scaling `rho=s/((t+1)(t^2+2t-1))`, the quartic depends on the orientation
signs only through `eta=eh*ev`.  The four sign components therefore reduce to
two genus-17 quartic classes over `E_h90`.

Follow-up branch class:
[P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md).
The first quadratic resolvent is just the domain-spin cover.  The new Kummer
payload is the second-layer class `rho^2=U_eta+z*W_eta`, with odd branch
divisor degree `16` over the genus-5 cover.

Follow-up row-bit factor test:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Factor Test](p27_trace_norm_dplus_u6_rowbit_h90_factor_20260622.md).
The post-Dplus `U6` row-bit lift remains irreducible of degree `32` after
base change from `F_607(t)` to `E_h90/F_607(t)`.  Thus the elliptic quotient
does not by itself split or source the row bit.

## Interpretation

Positive:

```text
The relative Dplus cover has an explicit order-4 H90 automorphism.
The quotient is the named elliptic curve E_h90, not an unknown genus-17 object.
The next CAS target is a cyclic-quartic/Kummer class over E_h90.
The four orientation components collapse to two eta classes.
The first resolvent is domain-spin; the second-layer Kummer class is A_eta.
```

Negative:

```text
The quotient alone is not a sampler; the hard part is the degree-4 cover.
Genus 17 remains too large for direct production.
The result is structural/theorem-facing, not a GPU green light by itself.
```

## Next Test

Extract the cyclic-quartic/Kummer data of the cover:

```text
N -> E_h90
E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1)
degree(N/E_h90) = 4
genus(N) = 17
ramification contribution = 32
```

The decisive next artifact is one of:

```text
1. explicit branch divisor/Kummer class over E_h90;
2. a decomposition/quotient/Prym factor that lowers the source;
3. a recurrence or equality linking this cyclic quartic class to d3;
4. a proof-shaped obstruction that the branch class is generic.
```

GPU remains useful only after (2) or (3), or as bounded telemetry for a named
class.

## Continue / Kill

```text
continue = cyclic-quartic/Kummer extraction over E_h90
continue = use the normalized eta quartics for branch extraction
continue = compare A_eta with the d3 Kummer class
continue = compare the E_h90 class with d3/d4 classes
continue = use alpha orbit telemetry only as validation

kill = generic CurveQuotient calls as the main online-Magma path
kill = treating four orientation components as separate classes after eta collapse
kill = searching for an additional first-resolvent shortcut
kill = H90 elliptic-base factorization as the easy row-bit source
kill = treating E_h90 alone as a Dplus source
kill = GPU production from this lane without a source map or d3 coupling
```

## Linked Artifacts

- Relative descent: [P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md)
- Normalized quartic: [P27 Trace/Norm Dplus H90 Quartic Model](p27_trace_norm_dplus_h90_quartic_model_20260622.md)
- Branch class: [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- Quotient symmetry: [P27 Trace/Norm Dplus Quotient Symmetry](p27_trace_norm_dplus_quotient_symmetry_20260622.md)
- Dplus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_h90_quotient_rows=1/1
```
