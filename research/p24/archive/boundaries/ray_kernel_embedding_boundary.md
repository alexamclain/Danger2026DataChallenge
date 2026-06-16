# Auxiliary Ray-Kernel Embedding Boundary

This note records why the Cho/Koo/Shin smaller-generator theorem is adjacent
to, but does not solve, the p24 embedded Hilbert-class selector.

## Source Theorem Shape

The cached papers in `p24/lit/` prove several ray-class generator statements.
The most tempting one is the smaller-generator theorem in

```text
p24/lit/smaller_generators_1407.5713.tar
```

For a ray modulus `F`, if the local ray part contains an odd prime order class
`C'`, then a quotient of Siegel-Ramachandra invariants

```text
g_F(C') / g_F(C_0)
```

can generate the ray class field `K_F` over `K`, under explicit local-size
conditions.  The quotient is a modular unit in the cases relevant here.

The theorem is genuinely useful for constructing ray fields.  It does not,
by itself, construct an embedded quotient of the level-1 Hilbert class field.

## Auxiliary Prime Temptation

Even though the p24 primes `157` and `211` themselves do not appear in their
squarefree local ray kernels, small auxiliary rational primes do.

The search

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/auxiliary_ray_kernel_search.py \
  --limit 200000 --count 12
```

starts:

```text
layer q kronecker q_minus_chi quotient_mod_units quotient_factor
  157    941        -1         942                471 {3: 1, 157: 1}
  157   3767        -1        3768               1884 {2: 2, 3: 1, 157: 1}
  157   5023        -1        5024               2512 {2: 4, 157: 1}
  157   6907        -1        6908               3454 {2: 1, 11: 1, 157: 1}
  157   9421         1        9420               4710 {2: 1, 3: 1, 5: 1, 157: 1}
  211   2111         1        2110               1055 {5: 1, 211: 1}
  211   2953        -1        2954               1477 {7: 1, 211: 1}
  211   3797        -1        3798               1899 {3: 2, 211: 1}
  211   4643         1        4642               2321 {11: 1, 211: 1}
```

So there is no shortage of auxiliary ray kernels with `157` or `211`
torsion.  The obstruction is not local availability.

## Verticality Lemma

Let

```text
1 -> U_F -> Cl_F(K) -> Cl(K) -> 1
```

be the standard ray-to-Hilbert class exact sequence.  The group `U_F` is the
local principal congruence part.  By Shimura reciprocity, its Artin action on
a level-`F` modular function changes the chosen level structure, but its
projection to the level-1 singular modulus is trivial:

```text
j(Cu) = j(C)        for C in Cl_F(K), u in U_F.
```

Consequently, any construction using only characters or generators from
`U_F` is vertical over a fixed level-1 CM root.  Taking traces, norms, ratios,
or Kummer extractions along `U_F` can produce ray-class units or functions
attached to that root, but it does not move between the `Cl(K)`-conjugate
`j` roots.

After taking `U_F`-invariants, the result descends to the Hilbert class field
as a natural class-equivariant function of the same embedded `j` root.  It is
not a section of

```text
Cl(K)/H_parent -> Cl(K)/H_child
```

and it does not pair abstract child roots with embedded `j` periods.

## Why Norming Down Does Not Help

One might try to compute a ray-class generator at an auxiliary level and norm
it down to the Hilbert class field.  But the norm over a subgroup of `U_F`
still fixes the ordinary class coordinate.  The result is a product over
level structures above the same `j(C)`, not a relative trace over the desired
Hilbert-class subgroup.

To affect the p24 odd tower layers, a character of `Cl_F(K)` must be
nontrivial after projection to `Cl(K)`.  Choosing such a character is exactly
choosing the unramified class direction.  Evaluating its relative trace or
projector is the original order-`157`, order-`211`, or order-`3107441`
embedded class-period problem.

## Consequence

The smaller-generator theorem does not close the p24 theorem gap.  It gives:

```text
explicit ray-class units and ray-field generators
```

but the certificate needs:

```text
an embedded unramified Hilbert-class phase tied to level-1 j roots.
```

The only way to use auxiliary ray fields would be to add a new theorem that
canonically couples the vertical ray kernel with the horizontal Hilbert class
torsor.  Such a coupling would be a class-field section or an embedded
relative-period identity; both are equivalent to the remaining selector
problem, not consequences of the existing ray-class generator theorems.
