# L1 Axis Annihilator Theorem

Date: 2026-06-05

This note reformulates `L1` axis injectivity as a group-algebra annihilator
condition.

## Axis Space As Cyclotomic Support

Let `K ~= C_m`, with:

```text
m = 66254 = 2 * 157 * 211.
```

Write the group algebra as:

```text
F_p[K] = F_p[Z]/(Z^m - 1).
```

The `L1` axis coefficient space is:

```text
W_axis = <1>
       + trace-zero functions of r mod 2
       + trace-zero functions of r mod 157
       + trace-zero functions of r mod 211.
```

Equivalently, in the semisimple group algebra, `W_axis` is the direct sum of
the cyclotomic factors:

```text
Q_axis(Z) = Phi_1(Z) Phi_2(Z) Phi_157(Z) Phi_211(Z).
```

Its dimension is:

```text
deg Q_axis = 1 + 1 + 156 + 210 = 368.
```

## Packet Annihilator Form

For one H-packet factor `f_a | Phi_n`, let:

```text
beta_a = (F_0 mod f_a, ..., F_{m-1} mod f_a)
```

be the selected packet vector.  The axis map is the action map:

```text
T_a : W_axis -> F_p[X]/(f_a),
T_a(w) = w * beta_a.
```

Let:

```text
Ann_a = {w in F_p[K] : w * beta_a = 0}.
```

Then:

```text
T_a is injective on W_axis
  <=> Ann_a cap W_axis = {0}
  <=> no simple cyclotomic factor of Q_axis is killed by beta_a.
```

Equivalently, if `A_a(Z)` is the squarefree product of the irreducible
cyclotomic factors whose packet component vanishes, then the target is:

```text
gcd(A_a(Z), Q_axis(Z)) = 1.
```

This is the most compact `L1` producer theorem so far.

## p24 Meaning

For p24, this says that in each of the eight H-packets, the following
K-character resolvent components are p-units/nonzero:

```text
constant component,
nontrivial 2-axis component,
the 157-axis Frobenius module,
the six 211-axis Frobenius modules.
```

The module accounting is:

```text
over F_p:
  1 trivial module,
  1 nontrivial 2-module,
  1 irreducible 156-dimensional 157-module,
  6 irreducible 35-dimensional 211-modules.

over one degree-388430 H-packet field:
  1 constant line,
  1 nontrivial 2-axis line,
  2 irreducible 78-dimensional 157-axis modules,
  210 one-dimensional 211-axis lines.
```

So the theorem can be attacked either over `F_p` with nine Frobenius-stable
modules, or after scalar extension with the refined packet-field module
decomposition.

## Toy Verification

Added:

```text
p24/l1_axis_group_algebra_annihilator_toy.py
```

For the split toy `m=30=2*3*5`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_group_algebra_annihilator_toy.py \
  --q 181 --m 30 --components 2,3,5
```

reported:

```text
axis_dim=8
axis_exponents=[0,6,10,12,15,18,20,24]
eval_rank=8
rank_matches_nonzero_axis_exponents=1
axis_injective=1.
```

Planting one axis annihilator:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_group_algebra_annihilator_toy.py \
  --q 181 --m 30 --components 2,3,5 --kill-axis-exponent 15
```

reported:

```text
eval_rank=7
killed_axis_exponents=[15]
rank_matches_nonzero_axis_exponents=1
axis_injective=0.
```

This verifies the finite algebra:

```text
axis injectivity
  <=> no axis character lies in the packet annihilator.
```

## Remaining Arithmetic Theorem

The p24 proof still needs selected-prime p-unitness.  The new statement is
more structured:

```text
For each H-packet factor f_a, the selected CM packet vector beta_a has
nonzero projection to every cyclotomic factor dividing Q_axis.
```

This is weaker than full K-normality and stronger than the one-scalar `L1`
nonvanishing.  It is the preferred `L1` theorem target because it matches the
smooth tower layers exactly.
