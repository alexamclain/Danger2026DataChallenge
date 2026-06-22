# P27 K/S First-Half Cover Magma Smoke

Date: 2026-06-21

## Claim

The K/S branch-extraction lane now has a first actual normalization-style
checkpoint.  The raw reverse-source equations are too large for the online
Magma calculator, but a staged eta-component extraction reaches a meaningful
intermediate result:

```text
after saturating away cleared-denominator artifacts,
the first post-alpha / first-half cover is a curve of genus 37 over q=7.
```

This is not a p27 theorem and not a promotion-field result.  It is a serious
negative smoke for the low-genus K/S source route, because genus `37` appears
before adding the final reverse-square variables `z,Y`.

## Artifacts

Full K-coordinate source fixture:

```text
research/p27/archive/fixtures/p27_ks_reverse_source_cover_q7_magma.m
```

Eta-component source fixture:

```text
research/p27/archive/fixtures/p27_ks_reverse_source_eta_component_q7_magma.m
```

Raw first-half fixture:

```text
research/p27/archive/fixtures/p27_ks_first_half_cover_q7_magma.m
```

Saturated first-half fixture:

```text
research/p27/archive/fixtures/p27_ks_first_half_cover_saturated_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_ks_reverse_source_cover_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_ks_reverse_source_eta_component_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_ks_first_half_cover_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_ks_first_half_cover_saturated_q7_magma_20260621.txt
```

Raw online responses:

```text
research/p27/archive/probe_outputs/p27_ks_reverse_source_cover_q7_magma_20260621.html
research/p27/archive/probe_outputs/p27_ks_reverse_source_eta_component_q7_magma_20260621.html
research/p27/archive/probe_outputs/p27_ks_first_half_cover_q7_magma_20260621.html
research/p27/archive/probe_outputs/p27_ks_first_half_cover_saturated_q7_magma_20260621.html
```

## Method

The fixtures instantiate the handoff equations from
[P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
over the tiny p27-signature field `q=7`, i.e. `q = 7 mod 16`.

The full source uses variables:

```text
X, W, T, B, R, z, Y, eta, K
```

The eta-component source fixes `eta=+1` and omits explicit `K`, since:

```text
K = K_num(X) / K_den(X)
```

The staged first-half source stops before the final reverse-square variables
`z,Y`, using only:

```text
E:             W^2 = X^3 - X
T-cover:       T^2 = X(X^2+1)(X^2+2X-1)
compactD:      X*R^2 = W(X^2+1)(m0+mt*T)
first-half:    B^2*U_den^2 = U_num^2 - 4*U_den^2
```

The raw first-half scheme has denominator artifacts.  The saturated fixture
uses Magma's official
[`Saturation(I, f)`](https://magma.maths.usyd.edu.au/magma/handbook/text/1323)
ideal intrinsic, saturating by:

```text
bad = X*(X-1)*(X+1)*(T-2X^2)
```

These are exactly the cleared-denominator / degenerate divisors in the
first-half formula.

## Results

### Full Source

The full source fixture reaches the online calculator memory limit:

```text
Current total memory usage: 329.2MB, failed memory request: 99.2MB
System Error: User memory limit has been reached
RESULT p27_ks_reverse_source_cover_q7 done
```

### Eta Component

The eta-component fixture also reaches the memory limit:

```text
Current total memory usage: 298.3MB, failed memory request: 113.7MB
System Error: User memory limit has been reached
RESULT p27_ks_reverse_source_eta_component_q7 done
```

### Raw First-Half Layer

The raw first-half scheme is not yet the desired curve:

```text
SCHEME_OK 2 4
AFFINE_POINTS 77
```

Interpretation:

```text
dimension 2 = denominator/projection artifacts remain
```

The online calculator then times out during component decomposition.

### Saturated First-Half Layer

After saturation, the same first-half layer becomes a curve:

```text
SAT_SCHEME_OK 1 42 3
SAT_CURVE_OK 37 3
```

Interpretation:

```text
dimension = 1
saturated ideal basis size = 42
affine F_7 points = 3
genus = 37
```

The calculator still times out during later affine/projective component
decomposition, but the cheap curve coercion and genus computation complete.

## Interpretation

Positive:

```text
The exact K/S source equations are now executable as Magma fixtures.
The denominator artifact is identified and corrected by saturation.
The first meaningful saturated layer gives a concrete genus value.
```

Negative:

```text
The first post-alpha / first-half cover is already genus 37 in the q7 smoke.
The full reverse-square source is heavier still.
This is far above the genus <= 1 promotion bar for an elliptic/rational source.
```

This does not fully kill K/S, because q7 is tiny and the online calculator did
not complete promotion-field normalization.  But it changes the burden of
proof: the K/S route now needs a non-obvious quotient, recurrence, or
decomposition of this genus-37 layer.  A direct low-genus source from the
raw handoff equations is no longer plausible.

## Consequence

The next concrete tests should be:

```text
1. Offline Magma/Sage saturation and normalization over q=1607, q=1847, q=2087.
2. Decomposition of the saturated genus-37 first-half layer under residual
   involutions, especially Sroot -> -Sroot and alpha.
3. Only after a low-genus quotient is found, test d4 recurrence or GPU source.
```

Do not continue with visible K/S branch products or coefficient widening.

## Continue / Kill

```text
continue = offline/promotion-field saturated normalization
continue = quotient/decomposition of the genus-37 first-half layer
continue = carry Sroot and alpha actions through the saturated ideal

kill = direct low-genus K/S source from the unsaturated handoff equations
kill = online-Magma full source normalization as the main workflow
kill = GPU sampler based only on the current K/S source equations
```

## Linked Artifacts

- Parent packet: [P27 K/S Branch-Extraction Packet](p27_ks_branch_extraction_packet_20260621.md)
- K handoff: [P27 Kummer Branch-Extraction Handoff](p27_kummer_branch_extraction_handoff_20260621.md)
- K-line branch screen: [P27 Kummer Branch-Divisor Screen](p27_kummer_branch_divisor_screen_20260621.md)
- Saturated fixture: `research/p27/archive/fixtures/p27_ks_first_half_cover_saturated_q7_magma.m`
- Saturated output: `research/p27/archive/probe_outputs/p27_ks_first_half_cover_saturated_q7_magma_20260621.txt`

```text
p27_ks_first_half_cover_magma_rows=4/4
```
