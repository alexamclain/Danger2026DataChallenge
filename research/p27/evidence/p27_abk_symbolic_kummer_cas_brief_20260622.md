# P27 A/B/K Symbolic Kummer CAS Brief

Date: 2026-06-22

## Claim

The current first-class moonshot is no longer another visible bucket or
fixed-prefix GPU filter.  The live below-sqrt test is:

```text
normalize the selected A/B/K Kummer tower and decide whether successive
selected gate classes are related, sourceable, or fresh independent half-covers
```

This brief is the compact symbolic bridge between the finite-field A-level
fixtures, the B-line reduced-cover packet, the conic tower equations, and the
trace/norm `Dplus` descent.  It is the artifact to hand to an offline
Magma/Sage/CAS agent before spending a large GPU run on this lane.

Machine-readable manifest:

```text
research/p27/archive/fixtures/p27_abk_symbolic_kummer_cas_brief_20260622.json
```

## Coordinates

Use the following equivalent coordinate views as checks on the same selected
classes, not as independent lanes.

```text
A = B^2 - 2
A = 2 - c^2
x_j = r_j^2
```

One conic transition is:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

With:

```text
a_j = r_{j+1} - 1/r_{j+1}
L_j = h_j - g_j - 2*r_j
```

the selected selector layer is:

```text
Z_j^2 = -(L_j + a_j)*(L_j - a_j)*c*r_{j+1}
```

The reduced B-line first transition is:

```text
U = x6 + 1/x6
(U - 2*x5)^2 = 4*(x5^2 + A*x5 + 1)
f3 = chi(U + 2)
```

After imposing the f3 layer:

```text
H^2 = U + 2
```

the next generic transition can be staged as:

```text
F_A(U,V) =
  (V^2 - 4)^2
  - 4*U*(V^2 - 4)*(V + A)
  + 16*(V + A)^2
  = 0

gamma^2 = V + 2
f4/f3 class = gamma
```

The V4 factorization of that quartic is:

```text
Y = V + 2
R^2 = H^2 - 4
S^2 = B^2 + H^2 - 4
Y = (H +/- R)*(H +/- S)
f4 = chi(H + R)*chi(H + S)
```

This factorization is explanatory, not a source law by itself: the separate
phase factors are sheet-dependent, while only the product is canonical on the
selected rows.

## Evidence Boundary

Positive facts to preserve:

```text
selected gates descend to whole A fibers in p27 samples through d14
A, B, K, and Sroot fixtures are exact coordinate views of the same classes
Dplus post-gate d3/d4 also descends to A, routing Dplus class work here
the reduced B-line equation gives an explicit f3 cover before reverse z/Y
the gamma transition gives an exact staged f4/f3 class over the f3 layer
the V4 factorization names phase classes for bounded telemetry
```

Negative facts to avoid rerunning:

```text
visible A-line degree <= 4 branch support is killed
A-line S3, affine, PGL2, hidden-X power, and Chebyshev recurrences are killed
B/K/lambda visible quartic buckets are killed
low-degree B-line plane relations for the reduced fibers are killed through degree 20
fixed prefix filters and source buckets do not improve raw source denominator enough
online Magma has already hit the useful limit on localized reduced-cover genus data
```

## CAS Tasks

1. Normalize the legal/core reduced f3 cover.

Required output:

```text
function field or normalized curve for the selected legal/core source
components and fields of definition
genus of each relevant component
branch divisor degree and support field degrees for U+2
obvious sign, reciprocal, and B/A/K/Sroot quotient maps
comparison against q1607/q1847/q2087 fixture rows
```

Start from the localized complete-intersection or no-R reduced chart, not from
product saturation.  Impose the selected-source legal/core cut before
interpreting all-chart point-count fibers.

2. Extract the f4/f3 Kummer class.

Required output:

```text
normalize F_A(U,V)=0 over the f3-plus base
compute div(V+2) modulo squares
classify gamma as pullback, coboundary, translate, quotient class, or fresh cover
record how the V4 alpha/beta phases transform under H -> -H and sheet signs
```

3. Repeat one layer.

Required output:

```text
same construction after f4-plus
compare f5/f4 with the f4/f3 gamma class
decide whether f3,f4,f5 are related by pullback, translate, coboundary, iterate, or recurrence
```

4. If a relation appears, turn it into a source-denominator test.

Required output:

```text
source parameters and denominator
legal rows emitted
prefix depth distribution
target/source_draw versus ordinary X1(16)
target/GPU-second if handed to GPU
```

## Promote / Kill

Promote if:

```text
genus <= 1 sourceable component appears
or an explicit quotient/Prym factor carries multiple selected classes
or f3,f4,f5 share a pullback/translate/coboundary/iterate relation
or a direct sampler beats independent half-loss with source-normalized margin
```

Kill if:

```text
the legal/core f3 cover is high-genus/generic after quotients
and f4/f5 are fresh unrelated half-covers
or the only source is an all-chart artifact outside the selected legal domain
or the only GPU proposal is a new one-bit filter or phase bucket with no raw-source win
```

## GPU Boundary

GPU work on this lane should wait for a named map or be strictly bounded
telemetry:

```text
allowed = emit A/B/K/Sroot,U,H,V,gamma,alpha,beta across d3..dN with raw-source denominators
allowed = test a direct sampler or quotient source named by CAS
not allowed = large production from A-prefix, Bplus, alpha, beta, or fixed quadratic buckets
```

The only current production-shaped GPU ask outside this CAS lane remains the
separate fused/native `Dplus` pricing test:
[P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md).

## Linked Artifacts

- [P27 First-Class Moonshot Tests After Quadratic Probe](p27_first_class_moonshot_tests_after_quad_20260622.md)
- [P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)
- [P27 B-Line Reduced-Cover Symbolic Packet](p27_b_line_reduced_cover_symbolic_packet_20260622.md)
- [P27 B-Line Reduced-Domain Reconciliation](p27_b_line_reduced_domain_reconcile_20260622.md)
- [P27 B-Line Gamma Class Handoff](p27_b_line_gamma_class_handoff_20260622.md)
- [P27 B-Line Gamma V4 Factorization](p27_b_line_gamma_v4_factorization_20260622.md)
- [P27 Conic Tower Quotient CAS Handoff](p27_conic_tower_quotient_cas_handoff_20260622.md)
- [P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
- [P27 No-R Quotient/Prym Test Packet](p27_noR_quotient_prym_test_packet_20260622.md)

```text
p27_abk_symbolic_kummer_cas_brief_rows=1/1
```
