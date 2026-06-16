# RS-Tail Frequency Resultant Gate

Date: 2026-06-06

## Point

The frequency-defect theorem reduces the fixed p24 determinant to local
frequency facts:

```text
35 local rank-4 Plucker gates;
16 nonzero defect tail residues;
one 16x16 tail Vandermonde p-unit.
```

The next compression is to avoid proving those as `35+16` unrelated local
claims.  If the local Plucker values and defect tail residues are evaluations
of cyclic polynomial sections, then resultants certify all frequencies at
once.

## Finite Gate

Let `omega` be a primitive `n`th root and let `A subset Z/nZ`, `|A|=k`, be the
defect frequencies.

Assume the frequency-defect local data is represented by p-integral cyclic
sections:

```text
P(x)       local 4x4 Plucker section;
T(x)       defect tail-residue section;
S_A(x)     selector/divisor with roots {omega^a : a in A} inside mu_n.
```

The local p-unit hypotheses are implied by:

```text
Res(P, x^n - 1) in O_p^*,
product_{a in A} T(omega^a) in O_p^*,
S_A has exactly k simple roots inside mu_n.
```

Then the existing frequency-defect gate gives the selected-basis p-unit.

Equivalently, in Bezout language:

```text
U(x) P(x) + V(x) (x^n - 1) = 1       mod p
```

proves the local Plucker gate at every frequency, and a second Bezout relation
between `T` and `S_A` proves every defect tail residue is nonzero.

## P24 Target

For p24:

```text
n = 35
k = 16
```

The theorem to discover is therefore sharper:

```text
construct P_24(x), T_24(x), S_24(x) from the CM/Lang fixed RS-tail map;
prove Res(P_24, x^35 - 1), Res(T_24, S_24), and the selector discriminant are
p-units at p = 10^24+7.
```

This would replace frequency-by-frequency checking with a small cyclic
resultant/Bezout certificate.  It is class-set-free if the three sections are
defined intrinsically from the six-block CM/Lang object rather than from the
enumerated class set.

The cyclic sections must also descend.  If the local values are `F_a` over
`F_p(mu_35)`, then a base cyclic section requires

```text
F_{p a} = F_a^p.
```

For the selector, the defect set must be Frobenius-stable.  Since
`p mod 35 = 22`, p24 has seven fixed frequencies and seven length-4
Frobenius orbits.  A stable support of size `16` can be either:

```text
0 fixed singletons + 4 length-4 orbits:   35 choices;
4 fixed singletons + 3 length-4 orbits:   1225 choices.
```

The four-length-4 slogan therefore needs an additional arithmetic theorem:
fixed frequencies are ordinary.  With that theorem the selector choices drop
from `1260` to `35`.

The fixed-frequency ordinary theorem is local:

```text
for a in 5Z/35Z,  tau_a in image(P_a),
equivalently rank(P_a,tau_a)=rank(P_a).
```

The mixed-support control in the fixed-frequency gate shows why this theorem
is necessary: mixed supports still descend and still have a p-unit tail
Vandermonde.

## Boundary

This gate does not yet prove the p24 theorem.  It moves the missing arithmetic
from:

```text
prove 19 ordinary Plucker units and 16 defect tail residues separately
```

to:

```text
identify the CM/Lang cyclic sections whose resultants are those products.
```

That is a real narrowing: the resultants are determinant-line sections, so
they are natural candidates for a Borcherds/Fitting/local-intersection proof.

## Check

The finite reduction and controls are in:

```text
p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
p24/trace_gcd_rs_tail_defect_support_accounting.py
p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.py
```

It checks:

```text
good Plucker resultant + good tail-support resultant + correct selector
  => selected basis;
zero Plucker resultant
  => an ordinary frequency failure and omitted-support kernel;
zero tail-support resultant
  => a defect residue failure and omitted-support kernel;
wrong selector support size
  => rejected before the selected-basis conclusion.
Frobenius-compatible values
  => descend to base cyclic sections;
arbitrary splitting-field interpolants
  => rejected as post-fit evidence.
```
