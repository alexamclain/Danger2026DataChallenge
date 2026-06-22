# P27 B-Line Gamma Specialized Square Smoke

Date: 2026-06-22

## Claim

The gamma class is not already square on the visible generic `B/H` transition.

With

```text
A = B^2 - 2
H^2 = u + 2
Y = v + 2
```

the generic transition is:

```text
Y^4
- 4*H^2*Y^3
+ (-4*B^2*H^2 + 8*B^2 + 32*H^2 - 32)*Y^2
+ 16*H^2*(B^2 - 4)*Y
+ 16*(B^2 - 4)^2.
```

A universal visible square identity for `Y=v+2` over the `B/H` layer would
survive nondegenerate one-parameter specializations.  Online Magma finds two
small irreducible specializations where `Y` is not square.

## Artifacts

Magma fixture:

```text
research/p27/archive/fixtures/p27_b_line_gamma_specialized_square_smoke_q7_q23_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_specialized_square_smoke_q7_q23_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_gamma_specialized_square_smoke_q7_q23_magma_20260622.txt
```

Endpoint:

```text
https://magma.maths.usyd.edu.au/xml/calculator.xml
```

## Result

```text
magma_version = 2.29-8
magma_time = 0.110
magma_memory = 32.09MB
P27_GAMMA_SPEC HB Q 7 IRR true
P27_GAMMA_SPEC HB Q 7 Y_SQUARE false
P27_GAMMA_SPEC HB Q 7 NORM_FORM 2*B^4 + 5*B^2 + 4
P27_GAMMA_SPEC HBPLUS1 Q 23 IRR true
P27_GAMMA_SPEC HBPLUS1 Q 23 Y_SQUARE false
P27_GAMMA_SPEC HBPLUS1 Q 23 NORM_FORM 16*B^4 + 10*B^2 + 3
RESULT p27_gamma_specialized_square_smoke done
```

The norm forms match the expected specialization of
`16*(B^2 - 4)^2`, so this is the norm-square / element-nonsquare pattern from
the gamma V4 factorization.

## Interpretation

Positive:

```text
The visible generic transition does not trivialize gamma.
This is a quick CAS falsifier for a universal B/H-layer square identity.
It is consistent with gamma being the first genuinely fresh post-f3 class.
```

Negative:

```text
This is a specialization smoke, not full normalization of the no-R reduced base.
It does not classify gamma as pullback, coboundary, quotient, or fresh half-cover.
It does not produce a source map or GPU production mode.
```

## Continue / Kill

```text
continue = normalize the no-R reduced base and compute div(v+2) modulo squares
continue = compare gamma with the f5/f4 class after f4-plus
continue = use this as a regression falsifier for any proposed visible B/H square identity

kill = gamma already square over the visible generic B/H transition
kill = trying to get a sampler from Norm(v+2) being square
kill = GPU B/H buckets without a named quotient or recurrence
```

```text
p27_b_line_gamma_specialized_square_smoke_rows=1/1
```
