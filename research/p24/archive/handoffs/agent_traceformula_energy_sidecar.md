# Trace-Formula Energy Sidecar

Question: can known CM trace, relative trace, theta lift, Gross-Zagier, or
singular-moduli product formulas compute or prove nonzero of the p24 relative
energies

```text
E_a = sum_u P_u(a) P_u(-a)
    = sum_d zeta_n^(a*d) C_d,
C_d = sum_i j_i j_{i+m*d},
```

without enumerating the embedded class set?

## p24 Target

For the third strict p24 trace:

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441 prime
ord_n(p) = 388430
(n - 1) / ord_n(p) = 8
```

The class group is cyclic in the local PARI audit.  The genus quotient has
order `2`, because `D_K` has two prime factors and the Redei refinement in the
local notes gives no extra 2-primary layer.  The energy characters on
`H=<g^m>` therefore have prime order `3107441` and lie in the non-genus,
principal-genus direction.

The scalar energy is a relative trace:

```text
Theta_a = sum_k zeta_n^(a*k) sigma^(m*k)(j_0)
P_u(a) = sigma^u(Theta_a)
E_a = sum_u sigma^u(Theta_a) sigma^u(Theta_-a)
```

up to the harmless normalizing factor already recorded in
`relative_energy_certificate.md`.  Equivalently, it is the high-order Fourier
coefficient of the CM pair-correlation sequence
`C_d = Tr(j * sigma^(m*d)j)`.

## What Existing Formulas Actually Supply

Zagier's trace theorem and the Bruinier-Funke theta-lift extension compute
global CM traces, i.e. sums of CM values over all classes, as coefficients of
weight `3/2` modular/harmonic Maass forms.  Zagier's paper also discusses
"relative traces", but there the relative field is a real quadratic subfield
coming from a discriminant factorization, not an arbitrary high-order subgroup
of a ring class group.  Source anchors:

- Zagier, "Traces of singular moduli":
  https://people.mpim-bonn.mpg.de/zagier/files/tex/TracesSingModuli/fulltext.pdf
- Bruinier-Funke, "Traces of CM values of modular functions":
  https://arxiv.org/abs/math/0408406

Twisted-trace extensions such as Choi's are still genus-character/Dirichlet
style twists.  Choi explicitly defines the twist through a generalized genus
character before proving modularity of the trace generating series.  This is
not a character of order `3107441` in the principal genus.

- Choi, "Twisted traces of singular moduli of weakly holomorphic modular
  functions": https://arxiv.org/abs/1105.1223

Borcherds/Gross-Zagier/Schofer/Lauter-Viray style product formulas compute
Galois-symmetric products, averages, or valuations: norms of differences of
singular moduli, averages of Borcherds products over CM cycles, or
intersection multiplicities.  These formulas are extremely useful for global
divisibility, but they erase the relative phase.  They can see a product over
all cosets; they do not select the Fourier coefficient of the order-`3107441`
autocorrelation.

- Gross-Zagier, "On Singular Moduli":
  https://archive.mpim-bonn.mpg.de/id/eprint/2947/
- Schofer, "Borcherds forms and generalizations of singular moduli":
  https://arxiv.org/abs/math/0603714
- Lauter-Viray, "On singular moduli for arbitrary discriminants":
  https://arxiv.org/abs/1206.6942

Relative trace formula and Waldspurger/Gross-Prasad technology can relate
toric periods to central `L`-values for automorphic representations.  That is
the right philosophical neighborhood for a square of a class-character period,
but it does not give the needed finite-field unit statement.  It proves
complex/automorphic identities or horizontal nonvanishing in families, not
that the prescribed p24 algebraic integer `E_a` avoids one selected split
prime above `p`.

- Martin-Whitehouse, "Central L-values and toric periods for GL(2)":
  https://doi.org/10.1093/imrn/rnn127
- Burungale-Tian, "Horizontal non-vanishing of Heegner points and toric
  periods": https://doi.org/10.1016/j.aim.2019.106938
- Wei Zhang, "Periods, cycles, and L-functions: a relative trace formula
  approach": https://arxiv.org/abs/1712.08844

## Concrete Obstruction For `E_a`

The autocorrelation transform is not a global trace.  It is a projection by a
specific high-order unramified class character:

```text
E_a = sum_d chi_a((g^m)^d) * Tr(j * (g^m)^d j).
```

Any formula that averages over all `d`, over genus classes, over all CM
pairs, or over all cosets has already discarded `chi_a`.  Reintroducing
`chi_a` means either:

1. summing over the order-`3107441` subgroup;
2. constructing a modular/theta object carrying the corresponding unramified
   Hecke character of `K`; or
3. constructing a Borcherds/product divisor whose CM value is already the
   desired relative norm/energy.

Option 1 is the forbidden class-set enumeration.  Option 2 has natural
dihedral/half-integral level tied to `|D_K|`, not to the small numbers
`m` or `n`; the local audit `non_genus_twisted_trace_level_audit.py` records
the standard proxy:

```text
|D_K| = 652834595820939249713143
weight-1 dihedral level proxy:    5.449e22
half-integral trace level proxy:  4.904e23
sqrt(p) = 1.000e12
```

Option 3 is circular unless the divisor/product construction already contains
the order-`3107441` relative projector.  Existing Gross-Zagier/Borcherds
product formulas produce global norms or valuations; the full relative product
polynomial is exactly the missing embedded high-order quotient data.

There is also a p-adic gap.  The local dominance bound in
`singular_moduli_normality_bound.py` proves characteristic-zero nonvanishing
of all class-character resolvents for the p24 singular moduli.  But the p24
certificate needs nonvanishing after reduction at one specified split prime.
Known trace/product/L-value formulas do not rule out divisibility of the
specific high-order energy by that selected prime.  Naive norm-height
exclusion is far too weak because the singular-modulus heights are enormous
relative to `log p`.

## Verdict

No viable known theorem found.

The exact missing theorem would have to be new and phase-aware:

```text
For each of the eight Frobenius orbits of nontrivial characters of
H=<g^66254> of order 3107441, prove that

  E_a = sum_d zeta_n^(a*d) sum_i j_i j_{i+66254*d}

is nonzero modulo the selected p24 split prime,

or compute this scalar in sub-class-enumeration work.
```

Known CM trace and theta-lift formulas express only global/genus trace data
or move the high-order character into a modular object of discriminant-scale
level.  Known Gross-Zagier/Borcherds/product formulas control symmetric norms
or valuations and erase the order-`3107441` phase.  Known relative trace
formula nonvanishing is analytic/complex and not a selected-prime p-adic unit
certificate.  Thus these tools currently rephrase `E_a`; they do not compute
or prove its p24 finite-field nonzero without the same embedded high-order
relative-period primitive.
