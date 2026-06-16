# Reverse Canonical-Lift / Serre-Tate Barrier

Question: can Satoh/AGM/canonical-lift or Serre-Tate deformation machinery be
run "backwards" to choose a curve over the fixed field `F_p` whose Frobenius
eigenvalue satisfies `lambda == 1 mod 2^40`, without doing CM root selection
or walking `X1(2^40)`?

Current conclusion: no known distinct route.

## Why It Collapses

Satoh/AGM is a forward point-counting machine:

```text
start with an ordinary E/F_p
compute its canonical lift
recover Frobenius trace
```

Serre-Tate theory is local around a curve already chosen modulo `p`; its
coordinate classifies lifts of that fixed ordinary curve's `p`-divisible
group.  It is not a global parameter that freely selects a new finite-field
`j`.

The DANGER condition is a `2`-adic Tate-module condition with `2 != p`.
Prescribing

```text
lambda == 1 mod 2^40
```

is therefore a discrete prime-to-p torsion condition.  In the p24 Hasse
interval it is exactly the same trace-congruence problem already recorded:
six target traces.  Once `p` and `t` are fixed, Tate/Waterhouse put us in one
ordinary elliptic isogeny class, and constructing a representative is the CM
problem for

```text
D = t^2 - 4p.
```

Solving reverse canonical-lift equations with prescribed Frobenius is just
asking for an elliptic curve admitting an endomorphism `pi` satisfying

```text
pi^2 - t*pi + p = 0.
```

This is the CM/Heegner locus of discriminant `D`; over `F_p` its `j` values
are roots of the relevant Hilbert/ring-class polynomial, or equivalently the
target class-group/isogeny torsor.

## p24 Special Form

The identity

```text
p = 10^24 + 7 = n^2 + 7
```

does give the cheap small-CM discriminant `D=-7` for traces `t=+/-2n`.
Those curves are the near-square ECPP certificate already recorded locally,
but both curve and twist have only `v2=3`, not the strict verifier depth
`40`.

The strict p24 traces instead have fundamental discriminants comparable to
`p` and conductor `2`.  Canonical-lift language does not change that
large-CM-field fact.

## References Checked

- Satoh canonical-lift point counting:
  https://cds.cern.ch/record/487847
- Carls AGM/Frobenius-lift formulation:
  https://arxiv.org/abs/0911.1883
- Borger-Gurney / Serre-Tate local moduli:
  https://arxiv.org/abs/1608.05912
- Waterhouse classification:
  https://www.numdam.org/item/?id=ASENS_1969_4_2_4_521_0
- Given-number-of-points CM construction:
  https://www.microsoft.com/en-us/research/publication/constructing-elliptic-curves-with-a-given-number-of-points-over-a-finite-field/

## Bottom Line

Reverse Satoh, canonical lifts, Serre-Tate coordinates, and AGM do not supply
an independent sub-sqrt p24 selector.  They compute or describe Frobenius for
a curve already selected; prescribing the p24 Frobenius eigenvalue collapses
back to the same fixed-trace CM/class-polynomial or modular/isogeny-walk
problem.
