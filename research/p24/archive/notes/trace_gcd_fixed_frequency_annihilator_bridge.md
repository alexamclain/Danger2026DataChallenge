# Fixed-Frequency Annihilator Bridge

Date: 2026-06-06

## Point

The no-fixed-defect support reduction is local at the seven fixed frequencies
`a in 5Z/35Z`.  The useful arithmetic form is not just a rank condition; it is
a trace-pairing annihilator inclusion.

## Local Data

At a fixed frequency `a`, write the four selected prefix values as:

```text
P_a = (V_{a,2}, V_{a,3}, V_{a,5}, V_{a,6})
```

and the tail local value as:

```text
tau_a = V_{a,1}.
```

The local ordinary gate has two pieces:

```text
rank(P_a) = 4;
tau_a in span_Fp(P_a).
```

The first is the fixed-frequency Plucker p-unit.  The second is the
no-fixed-defect condition.

## Dual Form

Using the trace pairing on `L`, the no-fixed-defect condition is equivalent to:

```text
if Tr(lambda V_{a,j}) = 0 for j in {2,3,5,6},
then Tr(lambda V_{a,1}) = 0.
```

In other words:

```text
Ann(P_a) subset Ann(tau_a).
```

This is the likely proof-facing form: construct the fixed-frequency CM/Lang
adjoint relation showing that every trace functional killing the four prefix
values also kills the tail value.

## Primal Form

Equivalently, prove seven local linear relations:

```text
V_{a,1}
  = c_{a,2} V_{a,2}
  + c_{a,3} V_{a,3}
  + c_{a,5} V_{a,5}
  + c_{a,6} V_{a,6},

c_{a,j} in F_p,
```

one for each `a in 5Z/35Z`.

Because `p = 10^24+7` satisfies `p = 1 mod 7`, these fixed frequencies are
base-rational in the `7`-part.  A stronger class-set-free route would package
the coefficients as cyclic sections over `F_p[y]/(y^7-1)` rather than as seven
unrelated relations.

The finite cyclic packaging is isolated in:

```text
p24/trace_gcd_fixed_frequency_cyclic_syzygy.md
```

It shows that the seven pointwise relations are equivalent to one syzygy over
`R_7 = F_p[y]/(y^7-1)`, while also recording why post-fit interpolation alone
is not arithmetic evidence.

## Check

The finite bridge is tested in:

```text
p24/trace_gcd_fixed_frequency_annihilator_bridge_toy.py
```

It checks:

```text
tail in prefix span
  iff every prefix annihilator kills the tail;

tail in prefix span
  removes the fixed defect line;

prefix full rank
  remains a separate Plucker p-unit condition.
```

## Next Arithmetic Target

Prove the dual inclusion from the actual CM/Lang construction:

```text
Ann(V_{a,2},V_{a,3},V_{a,5},V_{a,6}) subset Ann(V_{a,1})
```

for all seven fixed frequencies, without enumerating the class set.
