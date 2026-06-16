# Unit Distribution Obstruction

This note records the precise exception in which Siegel/Ramachandra-unit
distribution relations might have helped, and why the p24 odd layers do not
fall into it.

## Ray kernels versus Hilbert class layers

Let `K` be the third p24 CM field and let `Cl_m(K)` denote a ray class group
of modulus `m`.  If `m' | m`, the natural map

```text
Cl_m(K) -> Cl_{m'}(K)
```

has kernel represented by principal ideals with a congruence condition.  In
particular, its image in the ordinary class group `Cl(K)` is trivial.  This is
the class-field-theory reason distribution relations lower ray modulus: they
collapse local/congruence directions, not arbitrary unramified Hilbert class
subgroups.

Equivalently, the exact sequence

```text
O_K^* -> (O_K/m)^* -> Cl_m(K) -> Cl(K) -> 1
```

shows that the extra ray part sits above the Hilbert class field.  Norms or
distribution relations along this kernel do not select a subgroup inside
`Cl(K)`.

## p24 odd layers

For the third strict trace,

```text
D_K = -652834595820939249713143
h(K) = 2 * 157 * 211 * 3107441
G = Cl(K) ~= C_h.
```

After the degree-2 genus layer, the desired tower layers of degrees `157` and
`211` lie inside the principal genus, hence inside the unramified Hilbert
class group.  They are not local ray kernels.

The audit script

```text
p24/ray_kernel_distribution_audit.py
```

checks the simple local sizes.  Since neither `157` nor `211` divides `D_K`,
the local unit group modulo `ell` has order `(ell-1)^2` or `ell^2-1`, so it
has no `ell`-primary part.  The first `ell`-primary ray factors occur in the
ramified filtration from `ell^2` to `ell`, whose kernel maps trivially to
`Cl(K)`.

The same audit now checks the squarefree composite levels that could have
looked relevant:

```text
level=33127  = 157*211
level=66254  = 2*157*211
level=206498 = 2*223*463
level=103249 = 223*463
```

Their local unit parts factor as:

```text
33127:  {2:6, 3:2, 5:1, 7:1, 13:1, 53:1, 79:1}
66254:  {2:6, 3:2, 5:1, 7:1, 13:1, 53:1, 79:1}
206498: {2:4, 3:4, 7:2, 11:2, 37:2}
103249: {2:4, 3:4, 7:2, 11:2, 37:2}
```

None contains `157` or `211`.  Thus even the composite ray levels attached to
the p24 quotient and the oriented split correspondence do not supply the odd
unramified phases as local ray-kernel directions.

## Consequence for modular units

Admissible constructions from

```text
1. Siegel/Ramachandra or Weber modular-unit values;
2. Shimura-reciprocity conjugation formulas;
3. ray-class norm and distribution relations;
4. genus/reflection data;
5. Kummer extraction after adjoining quotient roots of unity
```

have two outcomes for the p24 odd layers.

They either produce an abstract ray/class-field generator whose reduced roots
are not paired with the embedded `j`-periods, or they compute the desired
unramified phase by applying the ordinary class subgroup idempotent, i.e. an
`H`-sized trace/norm.

Normal-basis theorems for ray class generators do not change this.  A normal
generator gives all conjugates; projecting it to the `157` or `211` child is
still the relative class-character trace

```text
T_s(aK) = sum_{u in K/L} zeta^{su} y_{a u L}.
```

Thus the one plausible modular-unit exception is closed for p24: the odd
relative phases are conductor-one, non-genus, unramified class-group layers,
not ray-kernel/local-unit layers.
