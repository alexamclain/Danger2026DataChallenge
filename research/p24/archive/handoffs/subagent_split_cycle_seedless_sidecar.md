# Split-Cycle Seedless Sidecar

This sidecar answers the narrow question:

```text
Can a split-prime horizontal cycle quotient, especially p24 ell=677 with
index 314 and order 655670051, be made seedless from Phi_ell plus a low-degree
genus/top invariant, without enumerating the full CM class set?
```

Conclusion: not by the natural component/resultant construction.  The cycle
sum quotient is real and useful after embedded CM vertices are available, but
`Phi_ell` plus low-degree top data does not supply the fixed CM-order filter or
the non-genus relative phase.  It either produces the universal closed-cycle
object with extra components, or it requires an embedded relation equivalent to
the missing quotient-period theorem.

## 1. Component polynomial from Phi_ell plus low-degree top data

For a split prime whose class has order `r`, the intended quotient values are

```text
Y_C = sum_{x in C} x
```

where `C` ranges over horizontal `ell`-isogeny components inside the fixed
CM torsor.  The polynomial

```text
prod_C (Y - Y_C)
```

has the desired quotient degree, but its definition already quantifies over
the fixed embedded CM components.

There are three natural ways to try to compute it:

```text
embedded roots / graph:
  works, but enumerates the CM vertices;

elimination with H_D(j_i)=0 and Phi_ell edges:
  works in toys, but uses the class polynomial or equivalent CM-order filter;

elimination with Phi_ell edges and no CM-order filter:
  computes universal closed ell-cycles, not the target CM quotient.
```

A low-degree genus/top invariant only helps if it comes with an embedded
relation to the `j`-torsor strong enough to filter the target CM order and pair
the child components.  That relation is exactly the missing theorem, not a
free consequence of `Phi_ell`.

## 2. Toy success and failure

The positive elimination toy is:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/seedless_cycle_elimination_toy.py
```

It uses:

```text
D=-87
q=103
ell=7
h=6
ell_class_order=3
```

and eliminates from

```text
H_D(x_i)=0
Phi_7(x0,x1)=Phi_7(x1,x2)=Phi_7(x2,x0)=0
Y=x0+x1+x2.
```

Output:

```text
cycle_sums_from_embedded_check=[4, 29]
eliminated_cycle_sum_polynomial=(Y - 29)*(Y - 4)

seedless_elimination_recovers_cycle_sum_quotient_when_H_D_is_available=1
elimination_uses_H_D_polynomial=1
```

So the algebraic identity is valid when the fixed CM order is supplied.

The matching seedless failure removes the `H_D` equations and enumerates the
universal simple 3-cycles of `Phi_7` over the same field.  A tiny inline check
gave:

```text
unfiltered Phi_7 3-cycle toy
D=-87 q=103 ell=7
universal_vertices=103
universal_simple_3cycles=10
universal_distinct_cycle_sums=10
universal_cycle_sums=[4, 9, 28, 29, 50, 55, 65, 76, 80, 88]
CM_roots=6
CM_cycle_sums=[4, 29]
CM_sums_subset_universal=True
```

Thus the universal `Phi_7` closed-cycle condition contains the desired CM
cycle sums, but it does not select them.  The missing filter is not a constant
factor nuisance; it is the fixed CM-order/class-field information.

The split-cycle quotient toy also confirms the same shape:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/split_cycle_quotient_toy.py
```

For `D=-5000`, `q=1259`, `h=30`, and `ell=11` of class order `3`, it reports:

```text
component_count=10
component_sizes=[3]
distinct_edge_sums=30
distinct_edge_products=30
cycle_sum_polynomial_degree=10
constructing_cycle_values_used_embedded_cm_vertices=1
```

Local edge invariants retain the full orbit; the quotient degree appears only
after whole-component aggregation.

## 3. p24 ell=677 versus the degree-157 target

For the best third p24 trace:

```text
h = 205880396014 = 2 * 157 * 211 * 3107441
```

the split-prime audit gives:

```text
ell = 677
class_order = 655670051 = 211 * 3107441
cycle_count/index = 314 = 2 * 157
Gamma0(677) degree proxy = 678
seeded walk proxy = 678 * 655670051 = 444544294578
seeded walk proxy / sqrt(p) = 0.444544
```

This is attractive if a seed root or embedded quotient were already known: the
formal seeded proxy is below `sqrt(p)`.  But the seedless closed-cycle degree
proxy is enormous:

```text
log10 psi(677^655670051) = 1.855932e9.
```

So `ell=677` does not provide a new seedless theorem.  It repackages the same
first non-genus layer as a single split-prime component quotient:

```text
G / <g^(2*157)> has degree 314.
```

After separating the genus degree `2`, each parent has the same degree-`157`
child refinement targeted in `degree157_refinement_target.md`.  The `ell=677`
form is a convenient graph presentation of the genus-plus-157 quotient, not a
different source of embedded phase data.

## 4. Exact obstruction statement

A useful boundary theorem to prove formally is:

```text
Let T_D be the embedded CM j-torsor for a fixed order O_D, and let Phi_ell be
the universal ell-isogeny correspondence on the j-line.  The component-sum
polynomial for the horizontal action of a split prime ell on T_D is computable
from Phi_ell by elimination only after imposing either H_D(j)=0 or an
equivalent embedded relation R(Z,j)=0 whose fibers are the desired CM torsor
or quotient fibers.

Without such a CM-order filter, the closed-cycle equations for Phi_ell define
the universal ell-cycle locus, whose components include non-target CM orders
and non-horizontal cycles.  A low-degree invariant Z with no embedded pairing
relation to j cannot distinguish the fixed horizontal class components.
```

In class-field language:

```text
If B is the stabilizer of the low-degree top invariant and H < B is the target
cycle stabilizer, then the child/component polynomial over a B-invariant value
requires the embedded relative traces for B/H.  Those traces are not determined
by the abstract quotient degree or by Phi_ell alone.
```

For p24, the successful theorem would still need to supply one of:

```text
1. a non-enumerative embedded relation R(Z,j) for the degree-314 quotient;
2. equivalently, the paired degree-157 child relation F_157(Z,Y);
3. equivalently, the nontrivial embedded relative class-character traces.
```

Absent that, the split-cycle resultant route is another presentation of the
same missing embedded class-field theorem, not an asymptotic speedup.

