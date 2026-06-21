# P27 E-Prime D3 Z-Source Magma Smoke

Date: 2026-06-21

## Claim

The actual `d3` source cover can now be staged as a concrete curve over the
E-prime quotient, but online Magma cannot compute its genus within the web
calculator limits.

The successful staging is:

```text
1. build the E' first-half pullback in variables U,V,X,T,R,B,z
2. saturate the first-half ideal first
3. add the reverse-source equation for x6 = z^2
```

Over q7 this produces:

```text
D3_Z_AFTER_FIRSTHALF_SCHEME 1 62 0
```

So the d3 z-source is no longer a vague request: it is a named dimension-1
scheme with an explicit 62-polynomial basis after first-half saturation.  The
remaining offline CAS task is genus/normalization/branch-class extraction for
that curve.

## Artifacts

All-at-once z-source fixture:

```text
research/p27/archive/fixtures/p27_eprime_d3_zsource_saturated_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_saturated_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_saturated_q7_magma_20260621.html
```

Sequential saturation diagnostic:

```text
research/p27/archive/fixtures/p27_eprime_d3_zsource_sequential_saturation_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_sequential_saturation_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_sequential_saturation_q7_magma_20260621.html
```

Staged-after-first-half fixture:

```text
research/p27/archive/fixtures/p27_eprime_d3_zsource_after_firsthalf_saturation_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_after_firsthalf_saturation_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_d3_zsource_after_firsthalf_saturation_q7_magma_20260621.html
```

## Method

The E-prime coordinates are:

```text
E': V^2 = U^3 + 4U
X^2 - U*X - 1 = 0
W = V*X^2/(X^2+1)
```

The first-half pullback uses the already validated equations for:

```text
T cover
compactD R-root
first-half B-root
```

The d3 source variable is:

```text
x6 = z^2
```

and the reverse-doubling equation is the scaled form of:

```text
x5 = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1)).
```

This fixture deliberately does **not** adjoin the final `Y^2=d3` root.  On the
nonsplit path, the next selected x-square criterion is already the d-next
criterion, so the z-source is the cheapest staged cover for the `d3` bit.

## Results

All-at-once saturation is too heavy for online Magma:

```text
EPRIME_D3_ZSOURCE_RAW_SCHEME 3 6 196
System Error: User memory limit has been reached
```

Sequential saturation also hits the online memory limit on the first
saturation step:

```text
SEQ_STEP raw 3 6 196
System Error: User memory limit has been reached
```

The successful staging is first-half saturation followed by adding the z
equation:

```text
AFTER_FIRSTHALF_SAT 2 61 0
D3_Z_AFTER_FIRSTHALF_SCHEME 1 62 0
System Error: User memory limit has been reached
RESULT p27_eprime_d3_zsource_after_firsthalf_saturation_q7 done
```

Interpretation:

```text
first-half saturation in A7 has dimension 2 because z is still free
adding reverse_z cuts it to dimension 1
online Magma cannot compute genus or further z-saturation for this curve
```

## Interpretation

Positive:

```text
The actual d3 z-source cover is now packaged as an explicit dimension-1 object.
The right staging order is known: first-half saturation first, then reverse_z.
The online calculator reaches the curve checkpoint before memory failure.
```

Negative:

```text
The cover is too heavy for online Magma genus/normalization.
The E' descent plus z-source still does not reveal a cheap source inside the
web-calculator budget.
```

This changes the expert/CAS ask from "find something relevant on E'" to:

```text
Normalize the q7/q1607 E' d3 z-source curve defined by the staged ideal:
  Iclean = Saturation(first_half_pullback, X*(X-1)*(X+1)*(X^2+1)*(T-2X^2))
  J = Iclean + <reverse_z>
Compute genus, branch divisor over E', and any low-genus factors.
```

## Continue / Kill

```text
continue = offline Magma/Sage normalization/genus of J
continue = branch/Kummer class extraction for d3 over E'
continue = compare d4 only after d3 class is named

kill = online Magma as the main workflow for full d3 z-source genus
kill = all-at-once saturation of the z-source ideal
kill = GPU sampler without a lower-genus factor or recurrence from J
```

```text
p27_eprime_d3_zsource_magma_rows=1/1
```
