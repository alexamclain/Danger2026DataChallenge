# Frobenius Packet Testing Barrier

This note checks whether the new Frobenius-orbit propagation lemma can be
turned into a probabilistic or compressed reduced-normality certificate.

## Packet Compression

For a quotient-period vector

```text
Y(T) = sum_{r=0}^{m-1} y_r T^r in F_p[T]/(T^m-1),
```

a single class character is the evaluation of `Y` at a root of unity.  Over
`F_p`, characters come in Frobenius packets: if `f(T)` is an irreducible
factor of `T^m-1`, the whole packet is

```text
Y(T) mod f(T).
```

This is the right finite-field object.  For the third p24 target,

```text
m = 66254,
ord_66254(p) = 5460.
```

So primitive odd packets have degree `5460`, not one scalar character over a
large root-of-unity extension.

## Why It Still Does Not Select

The packet remainder is still a full-support linear functional of the
embedded period values.  Computing it exactly requires the same hidden
subgroup sums

```text
y_r = sum_{h in H} j_{rh}.
```

In a black-box model this cannot be certified from samples.  If a degree-`d`
packet factor is left with `d` unknown coordinates, those coordinates can be
altered to force the packet remainder to zero while agreeing on every queried
coordinate.

The toy script

```text
p24/frobenius_packet_testing_barrier.py
```

uses the calibrated `D=-5000`, `h=30`, quotient-size-10 CM cycle over
`F_1259`, where quotient characters are grouped into Frobenius packets.  It
computes all packet remainders and then alters exactly `deg(f)` period
coordinates to kill one packet.

Representative output:

```text
chosen_factor_degree=2
agrees_on_period_coordinates=8/10
packet_killed=1
modified_values_distinct=1
```

Thus packet testing is a good way to state reduced normality over `F_p`, but
it is not a sub-sqrt algorithm unless another theorem computes the packet
remainders without the embedded subgroup projector.

## Cyclic Code Formulation

Mill's sidecar check suggested the exact coding version.  If a packet
vanishes, the annihilator of the embedded CM vector becomes a cyclic code in

```text
F_p[T]/(T^h-1).
```

Then a sparse additive selector exists precisely when the coset

```text
e_H + Ann(j)
```

has a representative of Hamming weight below `|H|`.

I added:

```text
p24/cyclic_code_projector_weight_toy.py
p24/cyclic_code_projector_weight_scan.py
```

It first computes the p24 quotient packet degrees without huge factorization:

```text
T^66254 - 1 over F_p:
  degree 1:     2 factors
  degree 35:   12 factors
  degree 156:   2 factors
  degree 5460: 12 factors
```

So only `28` packet residues would certify quotient normality if the embedded
period vector `Y` were already known.

On the calibrated `D=-5000`, `h=30` CM cycle, the natural annihilator is zero.
The script then artificially inserts one degree-2 packet into the annihilator
and brute-forces the minimum-weight representative of `e_H + Ann(j)` for
several quotient sizes:

```text
quotient_size subgroup_size projector_weight best_coset_weight
3             10            10               10
5              6             6                6
6              5             5                5
10             3             3                3
15             2             2                2
```

Thus even a toy packet kernel does not automatically create a lower-support
projector.  A p24 win would need either:

```text
1. a way to compute the 28 packet residues without summing over H; or
2. a genuine large annihilator whose coset with e_H has much lower weight.
```

The existing CM scans show no natural packet vanishings, and reduced
normality heuristics predict none.

The broader scan tests the same coding escape across several small CM cycles.
Run:

```text
python3 p24/cyclic_code_projector_weight_scan.py \
  --max-cases 4 --max-quotients 2 --max-q-for-degree2 1300
```

Output:

```text
rows=8
reduced_weight_rows=0
```

Every row had natural reduced normality (`natural_gcd_degree=0`), then an
artificial degree-2 packet kernel was inserted.  In all eight quotient cases,
the minimum Hamming weight in `e_H + Ann(j)` stayed equal to the subgroup
projector weight.  This is still toy evidence, but it gives no sign that
cyclic-code annihilators naturally produce sparse projector representatives.

The quotient-spectrum refinement is recorded in:

```text
p24/quotient_spectrum_support_theorem.md
p24/quotient_spectrum_support_toy.py
```

Quotient-character nonvanishing proves the support bound only for formulas
already known to descend to `G/H`.  For arbitrary additive Hecke/projector
operators the exact condition is still the affine-code minimum:

```text
min_{B in Ann(J)} wt(e_H + B) = |H|.
```

The toy quotient-support scan inserted artificial low-degree packet kernels
in small cyclic rings:

```text
rows=1016
nonquotient_reduced_rows=0
quotient_reduced_rows=0
```

This supports the same boundary, but does not prove the p24 minimum-distance
statement.

The actual small CM reduced-normality failures behave the same way.  In:

```text
p24/failure_projector_weight_audit.py
```

both known failure rows,

```text
D=-216 q=103 h=6
D=-300 q=139 h=6
```

still have `min wt(e_H+Ann(J)) = |H|` for every nontrivial quotient.  Packet
vanishing is therefore not enough; a sparse selector requires a much more
special annihilator/coset interaction.

The artificial counterexample in

```text
p24/cyclic_code_min_weight_counterexample.py
```

shows such an interaction can exist in principle:

```text
q=7, h=6, quotient_size=2, vanished_nonquotient_characters=[1,4],
projector_weight=3, best_weight=2.
```

So packet language is exact, but the useful p24 theorem has to be arithmetic:
the selected CM annihilator must be zero or at least avoid these structured
multi-packet cancellations.

The first artificial reductions are not random.  The lemma

```text
p24/dual_coset_annihilator_lemma.md
```

shows that a complete vanished translate `a+Q_H` of the quotient-character
subgroup gives a codeword supported on `H`, and can cancel `gcd(a,|H|)`
projector positions.  This explains the bounded scan reductions in

```text
p24/cyclic_code_min_weight_scan.py
```

and makes the p24 condition sharper: the CM annihilator must avoid harmful
dual-coset vanishings, or at least avoid enough of them to create a sparse
selector.

The relative-resolvent refinement is recorded in:

```text
p24/harmful_dual_coset_relative_resolvent_lemma.md
```

It shows that `a+Q_H` vanishes exactly when the nontrivial `H`-character `a`
has zero relative sum on every quotient fiber:

```text
P_u(a) = sum_k zeta_n^(a k) j_{u+m k} = 0      for all u.
```

For the third p24 target, `n=3107441` is prime and `ord_n(p)=388430`, so one
`F_p`-stable harmful event propagates through `388430` nontrivial relative
characters, i.e. through `66254*388430=h/8` full class characters.

## Consequence

The propagation lemma makes a p24 reduced-normality failure rigid: primitive
bad quotient characters would vanish in packets of size `5460`.  But
probability, sparse sampling, or a generic cyclic-code reformulation does not
turn this rigidity into a certificate.

The surviving constructive target is unchanged:

```text
compute the non-genus relative period packets themselves,
or compute the child/recovery polynomial directly,
without enumerating the H-coset.
```
