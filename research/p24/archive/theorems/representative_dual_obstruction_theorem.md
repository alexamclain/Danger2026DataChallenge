# Representative Dual Obstruction Theorem

This note rewrites the one-punit target `L_rep != 0` as a dual kernel
avoidance statement.

## Representative Row

The equivariant representative row is:

```text
deleted O4,
prefix blocks O2,O3,O5,O6,
tail block O1,
tail window = first 16 Lang coordinates of O1.
```

For `lambda in L=F_p(mu_157)`, write the six right-trace values as

```text
a_j(lambda) = Tr_{E/R_j}(lambda*S_j),      j=1,...,6.
```

Here `R_j` is the degree-35 right factor attached to orbit `O_j`, and the
Lang/trace-dual coordinates identify each `a_j(lambda)` with a 35-dimensional
`F_p`-coordinate block.

## Dual Obstruction

The representative leading Moore determinant `L_rep` vanishes if and only if
there exists a nonzero `lambda in L` such that:

```text
a_2(lambda) = 0,
a_3(lambda) = 0,
a_5(lambda) = 0,
a_6(lambda) = 0,
pi_16(a_1(lambda)) = 0.
```

Here `pi_16` is the projection to the first 16 Lang coordinates in the
equivariant `O1` tail window.

Equivalently:

```text
L_rep != 0
```

is the transversality statement:

```text
Phi(L) ∩ E_rep = {0},
```

where `Phi(lambda)=(a_1(lambda),...,a_6(lambda))` and `E_rep` is the
54-dimensional erasure subspace:

```text
O4 full block
+ final 19 Lang coordinates of O1.
```

The two forms are the same: preserving the kept 156 coordinates is equivalent
to erasing the deleted full block `O4` and the unused tail coordinates in
`O1`.

## Arithmetic Target

The current p24 theorem is therefore:

```text
No nonzero lambda in F_p(mu_157) satisfies
  a_2(lambda)=a_3(lambda)=a_5(lambda)=a_6(lambda)=0
  and pi_16(a_1(lambda))=0.
```

The unit-2 action transports this single statement to the other five deletion
rows.  Thus this one dual obstruction theorem is equivalent to the
equivariant one-punit certificate.

## Why This Helps

This form exposes the actual arithmetic geometry:

```text
four full relative traces cut L down to an expected 16-dimensional kernel;
the first 16 tail coordinates of the fifth trace must separate that kernel.
```

So a proof of `L_rep != 0` can be attacked either by the determinant

```text
L_rep = MooreDet(prefix_140 + tail_16),
```

or by the two-stage kernel theorem:

```text
K = ker(a_2,a_3,a_5,a_6) has dimension 16,
pi_16(a_1)|_K is injective.
```

The second form is not a weaker theorem; it is exactly the `B*T`
factorization of the same leading Moore determinant.

The finite equivalence is checked by:

```text
p24/lean/RepresentativeDualObstructionGate.lean
p24/representative_dual_obstruction_toy.py
```

The same dual obstruction can now be stated as a linearized trace-gcd:

```text
K = common kernel of the four full prefix trace blocks,
dim_Fp K = 16,
gcd_p-lin(P_K, tail_16) = X.
```

The finite p24 numerical gate and actual small-CM audit are:

```text
p24/lean/TraceGcdGate.lean
p24/lang_trace_gcd_kernel_audit.py
p24/linearized_trace_gcd_certificate_boundary.md
```

Toy outputs:

```text
q=3, prefix_dim=8, tail_dim=3:
  determinant_kernel_mismatches=0
  split_mismatches=0
  prefix_full_tail_fail=444/1000

q=2, prefix_dim=5, tail_dim=2:
  determinant_kernel_mismatches=0
  split_mismatches=0
  prefix_full_tail_fail=484/1000
```

The nonzero `prefix_full_tail_fail` counts are a useful warning: full prefix
rank alone is not enough.  The representative tail injectivity theorem is a
genuine arithmetic condition, not a formal consequence of the four full
blocks.
