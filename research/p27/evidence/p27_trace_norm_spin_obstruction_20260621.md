# P27 Trace/Norm Spin Obstruction

Date: 2026-06-21

## Claim

The trace/norm `domain_line` bit descends under the quotient involution

```text
t = y - 1
a = t - 1/t
sigma(t) = -1/t
F = t*(t^2 + 2t - 1)*(t^2 + 1)
domain_line = chi(F)
```

but it is not an ordinary small rational-character bit on the `a`-line.  It
has an odd valuation at the ramification divisor `t^2 + 1` of the quotient
map `t -> a`.  This makes the active object a spin/half-divisor class, not
just `chi(R(a))` for a visible rational function `R`.

## Exact Check

Algebraically,

```text
F(t) / F(-1/t) = t^6
```

so `chi(F)` is invariant under `t -> -1/t` away from zeros and poles.  However
the quotient map has derivative

```text
da/dt = (t^2 + 1) / t^2
```

and `F` contains the ramification factor `t^2+1` to odd exponent `1`.

That odd ramification is the obstruction to replacing the bit with a plain
low-degree rational character on the quotient line.

## Online Magma Validation

Small field:

```text
q = 607
q mod 8 = 7
```

This matches the p27 signs `chi(-1)=-1` and `chi(2)=+1`.

Input:

```text
research/p27/archive/fixtures/p27_trace_norm_spin_q607_magma.m
```

Saved outputs:

```text
research/p27/archive/probe_outputs/p27_trace_norm_spin_q607_magma_20260621.txt
research/p27/archive/probe_outputs/p27_trace_norm_spin_q607_magma_20260621.xml
```

Result:

```text
RESULT p27_trace_norm_spin_q607 ok true 1 604 0 3
```

Meaning:

```text
ratio_ok = true
valuation of F at ramification factor t^2+1 = 1
paired nonzero rows = 604
paired chi(F) mismatches = 0
excluded zero rows = 3
```

## Interpretation

Positive:

```text
domain_line really descends through the trace/norm quotient at the character
level.
The online Magma workflow is usable for compact p27 small-field checks.
```

Negative:

```text
The failed tiny `R(a)` searches were looking in the wrong class for this bit.
Visible rational functions on the a-line are not the natural home of the
domain selector.
```

## Continue / Kill

```text
continue = extract the actual double cover / half-divisor class over the
           lemniscatic quotient E: v^2 = u^3 - u
continue = ask Magma/Sage for divisor classes and cover maps, not another
           low-degree R(a) fit
continue = test whether the T_line/D_plus half-norm bit lives in a related
           spin class that can be sourced directly

kill = more blind small-degree rational-character scans on the a-line for
       domain_line
kill = interpreting trace/norm D_plus as "just find a better polynomial in a"
```

## Next Concrete Test

Build the trace/norm double covers explicitly over the elliptic quotient

```text
C: b^2 = 16 - a^4
E: v^2 = u^3 - u,  u = 4/a^2
```

and compute whether the `domain_line` and normalized `T_line` covers share a
low-degree quotient, Prym factor, or repeatable Kummer class.  A positive
result here would be a real sqrt-beating candidate because it would source the
`D_plus` stratum rather than post-filtering raw `y` draws.

```text
p27_trace_norm_spin_obstruction_rows=1/1
```
