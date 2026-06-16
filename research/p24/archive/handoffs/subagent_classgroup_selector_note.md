# p24 Conductor-2 Class-Group Selector Note

Question: do the conductor-2 CM target discriminants for

```text
p = 10^24 + 7
```

hide exploitable class-group, genus, small-ideal, or class-polynomial
decomposition structure that can select a target root/class in sub-sqrt time?

Target curve-side traces and maximal CM discriminants:

```text
t = 1020608380936
  D_K = -739589633190799177940983
  |D_K| = 29 * 25503090799682730273827

t = -78903246840
  D_K = -998443569409526507503607
  |D_K| = 7 * 211 * 4973929 * 135907507341779

t = -1178414874616
  D_K = -652834595820939249713143
  |D_K| = 599 * 1089874116562502921057
```

All three have order discriminant `4 D_K`; since `D_K == 1 mod 8`, the prime
`2` splits and the conductor-2 ring-class multiplier is

```text
2 * (1 - (D_K/2)/2) = 1.
```

So `Pic(Z + 2 O_K) -> Pic(O_K)` has trivial conductor kernel.  The conductor-2
order is not a second class group with extra cheap choices; for selection
purposes it is the same class group as the maximal order.

## Extra Test: 2-Class Structure Beyond Genus

The previous no-go was that genus characters save only `1, 3, 1` bits.  A
remaining possibility was hidden higher 2-class structure: ambiguous classes
might lift to order `4`, `8`, etc., giving additional quadratic class-field
layers and a finer class-polynomial decomposition than ordinary genus.

Using the standard Redei matrix for the odd fundamental discriminants, with
prime discriminant factors `d_i`, off-diagonal entries

```text
R_ij = 0 if (d_j / |d_i|) = +1, else 1,
```

and diagonal entries chosen so each row sums to zero, the computed matrices are:

```text
D_K = -739589633190799177940983
prime discriminants: [29, -25503090799682730273827]
R = [[1, 1],
     [1, 1]]
rank(R) = 1, r - 1 = 1, 4-rank = 0

D_K = -998443569409526507503607
prime discriminants: [-7, -211, 4973929, -135907507341779]
R = [[1, 1, 0, 0],
     [0, 1, 1, 0],
     [0, 1, 0, 1],
     [1, 1, 1, 1]]
rank(R) = 3, r - 1 = 3, 4-rank = 0

D_K = -652834595820939249713143
prime discriminants: [-599, 1089874116562502921057]
R = [[1, 1],
     [1, 1]]
rank(R) = 1, r - 1 = 1, 4-rank = 0
```

Thus the Sylow-2 part is exactly elementary genus 2-torsion:

```text
Cl[2-primary] ~= (Z/2)^(r-1)
```

for these targets.  There is no hidden 4-rank or higher 2-power class-field
tower to exploit.  After the genus labels are fixed, the residual class group
is odd and still has estimated size:

```text
1.393439e11, 1.041208e11, 1.030138e11
```

respectively.

## Ramified and Special-Factor Baits

The middle discriminant is the most tempting one because it contains the
prime-discriminant factor `-7`, matching the cheap identity

```text
p = n^2 + 7.
```

But this only says that the `Q(sqrt(-7))` genus component splits at `p`; in
fact all prime-discriminant genus components split at `p` for the target rows:

```text
t = 1020608380936:
  [29, -25503090799682730273827] have Kronecker symbol +1 at p

t = -78903246840:
  [-7, -211, 4973929, -135907507341779] have Kronecker symbol +1 at p

t = -1178414874616:
  [-599, 1089874116562502921057] have Kronecker symbol +1 at p
```

That is exactly what the principal representation of `p` by the CM order
already predicts.  It selects the genus field splitting behavior, not one
class among the roughly `1e11` classes left in the principal genus.

The small ramified primes also do not give fixed points.  Their ideal classes
are ambiguous involutions: useful as genus labels, but not principal
low-degree self-loops.  For example, the factors `7`, `29`, `211`, `599`, and
`4973929` can define ramified correspondences, but those correspondences act on
the CM root set rather than choosing a canonical root.

## Small-Ideal Relation Barrier

Any principal non-scalar relation of norm `N` in an imaginary quadratic order
of discriminant `D` satisfies

```text
4N = x^2 + |D| y^2,  y != 0,
```

so

```text
N >= ceil(|D| / 4).
```

For the three rows:

```text
ceil(|D_K|/4) =
  184897408297699794485246
  249610892352381626875902
  163208648955234812428286
```

These are about `1.6e11` to `2.5e11` times `sqrt(p)`.  In particular, no
sub-sqrt norm relation, CM cycle equation, or low-degree modular-polynomial
self-loop can select the target class.

For split small primes, a short class-cycle length would not be enough anyway.
If a split prime ideal of norm `ell` had order `m`, the relation norm
`ell^m` would still be at least `|D|/4`; a small `m` would only partition the
already huge root set into many small cycles unless it came with an independent
choice of the correct cycle.  Producing that choice is again the original
class-selection problem.

## Class-Polynomial Decomposition

The only decomposition exposed by the discriminant factorization is genus
decomposition, and the Redei calculation shows that the 2-primary decomposition
ends there.  Over `F_p`, the full class polynomial already splits because the
prime above `p` is principal.  Splitting over the genus field, or over the
known `-7` component in the middle row, therefore supplies labels for factors
that are already split modulo `p`; it does not supply a canonical linear
factor.

Any further decomposition would have to come from a large odd quotient of the
class group.  The discriminant factorization provides no visible small
presentation for such a quotient, and computing or evaluating such an odd
class invariant is essentially the ordinary CM class-invariant/root problem.

## Verdict

No exploitable p24 class-group/genus selector is visible.

The strengthened no-go is:

```text
conductor-2 kernel: trivial
genus quotient: only 1, 3, 1 bits
Redei 4-rank: zero for all three discriminants
2-primary class structure: exactly genus, no hidden 4/8/... layers
ramified small primes: ambiguous genus involutions, not root selectors
non-scalar principal relation norm: far above sqrt(p)
residual principal-genus class count: about 1e11
```

A successful route would need a genuinely new odd-part class selector: some
way to name one class in the large odd residual group without constructing the
class invariant, walking a sqrt-scale isogeny/class orbit, or merely restating
the principal splitting condition.
