# Cyclic Class-Tower Selector Obstruction

Date: 2026-06-06

## Point

The third p24 trace has the best class-group structure we have seen:

```text
D_K = -652834595820939249713143
h(D_K) = 205880396014 = 2 * 157 * 211 * 3107441
Cl(O_K) ~= C_h
```

The class number is squarefree, so the class group is cyclic as an abstract
abelian group.  This is genuinely useful: it removes subgroup ambiguity from
the tower

```text
2, 157, 211, 3107441.
```

But it does not choose compatible roots after reducing at the split ordinary
prime above

```text
p = 10^24 + 7.
```

## Finite Obstruction

At a completely split prime, roots of an abstract quotient field form a
torsor for the quotient class group.  If

```text
H_child < H_parent <= G,
```

then the children above a parent root form an

```text
H_parent / H_child
```

torsor.  A canonical rule selecting one child would be an equivariant section

```text
G/H_parent -> G/H_child.
```

No such section exists for a nontrivial layer.  An element of `H_parent` fixes
the parent coset but moves every possible child coset, contradicting
equivariance.

The finite Lean gate is:

```text
p24/lean/CyclicTowerSectionObstructionGate.lean
```

It records the abstract moving-stabilizer contradiction and the p24 numerical
facts:

```text
2 * 157 * 211 * 3107441 = 205880396014
1 < 157, 1 < 211, 1 < 3107441
3107441 < sqrt(10^24+7)
```

The executable p24 audit is:

```text
p24/cyclic_class_tower_selector_obstruction.py
```

## Consequence For The Current Proof

Cyclicity gives a clean tower skeleton:

```text
genus layer:       degree 2
odd phase layers: degree 157 and 211
recovery layer:   degree 3107441
```

The genus layer is the only piece supplied by quadratic/genus data, because
`D_K` has two prime factors and the genus quotient has order `2`.

The odd layers remain non-genus embedded phase data.  Therefore:

```text
abstract split class-field equations
+ cyclic squarefree subgroup structure
!= p24 root selector
```

The selected-chain route would still need embedded relative child
polynomials, or equivalently non-genus relative class-character traces, for
the `157` and `211` refinements.

The trace-GCD p-unit route avoids selecting a child root, which is why it is
still the better proof surface.  But it still needs the embedded determinant
section:

```text
Xi_O0 in O_p^*
Xi_O1 in O_p^*
diamond/unit determinant-line transport by p-units.
```

Thus the class tower helps organize the proof, but the missing theorem is
unchanged in kind: construct the embedded non-genus `157/211` CM/Lang phase
data, or an equivalent phase-aware Fitting/Borcherds determinant identity,
without enumerating the class set.
