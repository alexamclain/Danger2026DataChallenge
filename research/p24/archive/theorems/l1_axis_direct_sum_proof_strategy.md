# L1 Axis Direct-Sum Proof Strategy

This note isolates the proof shape suggested by the axis-injectivity scans.

## Axis Blocks

For a packet factor `f_a | Phi_n`, use complement-section fibers

```text
F_r(X) = sum_k j_{n*r + m*k} X^k mod f_a.
```

For each component

```text
c in {2,157,211}
```

define the `c`-axis packet elements

```text
Y_{c,t} = sum_{r == t mod c} F_r,      0 <= t < c.
```

They all have the same trace:

```text
sum_{t=0}^{c-1} Y_{c,t} = Y_0 = sum_r F_r.
```

The axis coefficient space can be written as

```text
<Y_0> + span{Y_{2,t} - Y_{2,0}}
      + span{Y_{157,t} - Y_{157,0}}
      + span{Y_{211,t} - Y_{211,0}}.
```

Axis injectivity is equivalent to this sum being direct, with dimensions

```text
1 + (2-1) + (157-1) + (211-1) = 368.
```

## Sufficient Theorem

For each Frobenius packet `a`, it is enough to prove:

```text
1. Y_0 != 0.

2. For every c in {2,157,211}, the c axis has internal rank c:
   the elements Y_{c,0}, ..., Y_{c,c-1} span a c-dimensional F_p-space
   modulo the packet field.

3. The three trace-zero spaces

     U_c = span{Y_{c,t} - Y_{c,0} : 1 <= t < c}

   have direct sum, and none intersects <Y_0>.
```

This is more structured than one 368-by-388430 rank statement.  It has a
class-field tower interpretation: each `U_c` is the trace-zero part of a
degree-`c` smooth-axis layer after the other two complement factors have been
traced out.

## Why This Could Be Proveable

The component degrees are pairwise coprime:

```text
2, 157, 211.
```

Before reduction, the corresponding class-field layers should be linearly
disjoint over their common quotient base.  A successful proof would show that
the selected reduction at `p=10^24+7` preserves this directness for the
nontrivial `H`-character packet.

The desired arithmetic input can therefore be phrased as:

```text
no selected-prime congruence collapses the trace-zero parts of these three
smooth-axis subextensions inside the H-character packet field.
```

This is still hard, but it is a tower statement rather than a generic
hyperplane-avoidance slogan.

## Base-Field Frobenius Modules

The geometric character support has 368 frequencies, but over `F_p` these
frequencies group into Frobenius-stable modules.  I added:

```text
p24/l1_axis_frobenius_module_audit.py
```

For p24 it reports:

```text
component orbit_count orbit_size nontrivial_dimension
        2           1          1                     1
      157           1        156                   156
      211           6         35                   210

trivial_module_dimension=1
nontrivial_irreducible_module_count=8
total_frobenius_stable_module_count=9
total_axis_dimension=368
component_lcm_order=5460
```

Thus a base-field proof can target nine Frobenius-stable pieces:

```text
1 trivial module,
1 module from the nontrivial 2-character,
1 irreducible 156-dimensional module from the 157-axis,
6 irreducible 35-dimensional modules from the 211-axis.
```

This is a cleaner class-field statement than 368 unrelated character
resolvents.  The selected-prime theorem becomes:

```text
the images of these nine Frobenius-stable axis modules remain a direct sum
inside every degree-388430 H-packet field.
```

There is also useful packet-field intersection accounting.  I added:

```text
p24/axis_packet_field_intersection_audit.py
```

For p24 it reports:

```text
packet_degree=ord_n(p)=388430
packet_degree_factorization={2: 1, 5: 1, 7: 1, 31: 1, 179: 1}

component char_degree intersection_degree compositum_degree chars_in_packet
        2           1                   1           388430               1
      157         156                   2         30297540               0
      211          35                  35           388430               1
```

So the `211`-axis characters already diagonalize inside the H-packet field,
while the `157`-axis requires adjoining `F_{p^156}` and intersects the packet
field only in `F_{p^2}`.  This suggests a refined proof split, but with a
rank caveat:

```text
1. organize the 211-axis by packet-field character coordinates;
2. handle the 157-axis by a linearly-disjoint external character field over
   the quadratic intersection;
3. prove the selected CM packet vector does not create a congruence tying
   those two axis systems together.
```

The first item is not a proof by itself.  A DFT matrix with packet-field
coefficients is invertible as a packet-field coordinate transform, but it need
not preserve the `F_p`-span of the coordinate entries.  The toy

```text
p24/packet_field_dft_rank_warning_toy.py
```

shows this over `F_4/F_2`: an invertible packet-field matrix sends a vector
whose coordinates span one `F_2` dimension to one whose coordinates span two.
Thus the formal theorem still has to be a base-field directness statement, or
the corresponding tensor/Moore scalar-extension statement.

The packet-field component analogue is tested in

```text
p24/component_character_module_boundary.md
```

In all dimension-possible reported rows, component character modules had full
rank and no zero Frobenius orbit.  This is the closest toy analogue so far to
the p24 `211`-axis part of the proof split.

The module decomposition over the actual H-packet field is recorded in

```text
p24/packet_field_k_module_audit.py
```

It reports:

```text
full_k_splitting_degree_over_packet=78

axis_components_over_packet:
  2-axis:   {1: 1}
  157-axis: {78: 2}
  211-axis: {1: 210}

full_K_over_packet:
  orbit_size_histogram={1: 421, 78: 844}
```

So the axis theorem over one packet field asks for directness of

```text
1 constant module,
1 nontrivial 2-axis line,
2 irreducible 78-dimensional 157-axis modules,
210 one-dimensional 211-axis character lines.
```

This is a module decomposition target, not an automatic rank equivalence from
diagonalization.  Any proof using these character lines has to transport
directness through the Moore/tensor formalism or prove directness back over
`F_p`.

## Experimental Support

The updated scan

```text
p24/l1_axis_injectivity_scan.py
```

now records `block_internal_failure_rows`.

Composite-`m`, all-origin eligible window:

```text
packet_rows=162
injective_rows=162
injective_failures=0
block_internal_failure_rows=0
pair_directness_failure_rows=0
cross_directness_failure_rows=0
full_k_injective_possible_rows=42
full_k_injective_rows=42
full_k_injective_failure_rows=0
rank_defect_histogram={0: 162}
```

Mixed all-row window:

```text
packet_rows=129
dimension_bound_rows=80
injective_possible_rows=49
injective_rows=49
injective_failures=0
block_internal_failure_rows=0
pair_directness_failure_rows=0
cross_directness_failure_rows=0
full_k_injective_possible_rows=49
full_k_injective_rows=49
full_k_injective_failure_rows=0
rank_defect_histogram={0: 49, 1: 37, 2: 14, 3: 24, 4: 2, 5: 2, 6: 1}
```

The rank defects in the mixed window are dimension-bound rows with
`deg(f) < dim(W_axis)`.  Among eligible rows, neither internal axis normality
nor cross-axis directness has failed.

A larger targeted window with `80 <= h <= 260` found:

```text
packet_rows=43
injective_rows=43
injective_failures=0
block_internal_failure_rows=0
pair_directness_failure_rows=0
cross_directness_failure_rows=0
full_k_injective_possible_rows=40
full_k_injective_rows=40
full_k_injective_failure_rows=0
injective_pivot_prefix_max=7
full_k_pivot_prefix_max=7
```

## Next Proof Obligation

The main missing lemma is a selected-prime directness statement:

```text
U_2 ⊕ U_157 ⊕ U_211 ⊕ <Y_0>
```

remains direct after reduction into each p24 packet field.

A sharper group-algebra reformulation is now recorded in:

```text
p24/l1_axis_annihilator_theorem.md
p24/l1_axis_group_algebra_annihilator_toy.py
```

It identifies the axis space with the cyclotomic support:

```text
Q_axis(Z) = Phi_1(Z) Phi_2(Z) Phi_157(Z) Phi_211(Z),
deg Q_axis = 368.
```

For each H-packet vector `beta_a`, axis injectivity is equivalent to:

```text
Ann(beta_a) cap W_axis = {0},
```

or, in squarefree factor language:

```text
gcd(A_a(Z), Q_axis(Z)) = 1,
```

where `A_a` is the product of K-character factors killed by the packet vector.
Thus the selected-prime theorem can be stated as nonvanishing of the constant,
2-axis, 157-axis, and 211-axis K-character components of every H-packet.

A useful next finite test is to enlarge the small-CM search for rows with
larger component degrees and `deg(f) >= dim(W_axis)`, because those are the
first places a genuine cross-axis intersection could appear.
