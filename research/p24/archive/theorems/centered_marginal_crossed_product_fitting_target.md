# Centered Marginal Crossed-Product Fitting Target

Date: 2026-06-06

This note sharpens the centered full-origin/Borcherds route into a concrete
Fitting-object theorem.

## Local Schubert Map

Work in the centered ambient space

```text
H = {w_0=0},       dim H = 210.
```

Let `W_C subset H` be the p24 centered row space:

```text
dim W_C = 156.
```

For a right window

```text
I_t = {t, t+1, ..., t+156} mod 211,
```

let

```text
B_t = {w in H : w is constant on I_t},     dim B_t = 54.
```

The quotient has dimension:

```text
dim H/B_t = 156.
```

The centered window determinant is the determinant of the quotient map:

```text
phi_t : W_C -> H/B_t,
Delta_C(t) = det(phi_t)
```

up to a p-unit choice of determinant-line bases.

Equivalently, after cyclic differencing `Q_b=P_b-P_{b-1}`,

```text
Delta_C(t) = det(Q_{t+1}, ..., Q_{t+156})
```

because the affine columns `P_{t+i}-P_t` are unit-triangular cumulative sums
of the consecutive `Q` columns.  This support-form restatement is audited in:

```text
p24/centered_marginal_difference_code_boundary.md
p24/centered_marginal_difference_code_audit.py
```

Thus the local bad event is:

```text
coker(phi_t) != 0
```

or equivalently:

```text
Fitt_0(coker(phi_t)) = 0.
```

## Orbit Fitting Object

Let `O` be a right Frobenius orbit in `Z/211Z` under multiplication by
`p mod 211`.  For p24:

```text
ord_211(p) = 35,
O = {0} or |O|=35,
number of orbits = 7.
```

The direct orbit Schubert map is

```text
Phi_O : direct_sum_{t in O} W_C -> direct_sum_{t in O} H/B_t,
Phi_O = direct_sum_{t in O} phi_t.
```

Then:

```text
Fitt_0(coker(Phi_O))
  = prod_{t in O} Fitt_0(coker(phi_t))
  = p-unit * prod_{t in O} Delta_C(t).
```

For nonzero p24 orbits this is a square Fitting determinant of size:

```text
35 * 156 = 5460.
```

The singleton orbit is size `156`.

This object is too large to be a final payload if expanded as a matrix, but it
is the right determinant-line object for an arithmetic producer.  A
Borcherds/Fitting proof should recognize the determinant line, not enumerate
the matrix entries or the class set.

## Crossed-Product Version

The direct-sum form is honest but hides the descent structure.  A
phase-aware class-field proof should instead construct a transported
semilinear orbit module:

```text
E_O = direct_sum_{i=0}^{r-1} W_C^{(q^i)}
F_O = direct_sum_{i=0}^{r-1} (H/B_{q^i t_0})^{(q^i)}
```

with `r=|O|`, together with the transported map

```text
Phi_O^tw : E_O -> F_O.
```

The determinant is unchanged up to p-units:

```text
det(Phi_O^tw) = p-unit * prod_{t in O} Delta_C(t).
```

This is the centered analogue of the crossed-product Fitting norm that
survived in the trace-GCD route.  It avoids the false base-coefficient
interpolant condition: the values `Delta_C(t)` need not satisfy
`Delta_C(qt)=Delta_C(t)`, but the orbit determinant still descends as a
phase-aware norm.

The determinant-level Kummer descent audit reaches the same conclusion:
individual powers `Delta_C(t)^e` do not descend on nontrivial small-CM
Frobenius orbits except at trivial exponents.  See:

```text
p24/centered_marginal_plucker_kummer_descent_boundary.md
p24/centered_marginal_plucker_kummer_descent_audit.py
```

## The Missing Theorem

The p24 certificate would follow from either of the following equivalent
producer statements.

Orbit form:

```text
For every right Frobenius orbit O, the p-integral phase-aware Fitting
section det(Phi_O^tw) is a p-unit at the selected ordinary prime above
p = 10^24 + 7.
```

Full-origin form:

```text
There is a p-integral phase-aware full-origin Fitting section Psi_C,full
whose selected CM value equals the full-origin centered Chow product up to
p-units, and v_p(Psi_C,full)=0.
```

The origin-norm power theorem then gives:

```text
Psi_C,full p-unit
  => Pi_C,right^(975736474) p-unit
  => Pi_C,right p-unit.
```

The finite implication is checked in:

```text
p24/lean/CenteredFullOriginBorcherdsGate.lean
p24/lean/CenteredBorcherdsPUnitGate.lean
p24/lean/CenteredArcProductGate.lean
```

## What Computation Should Test

Computation should not expand the p24 `5460 x 5460` orbit matrices or the
full origin norm.  Useful small-scale tests are:

```text
1. verify on small actual-CM rows that det(Phi_O) equals the orbit product
   with the same p-unit conventions as Delta_C(t);

2. test whether transported orbit bases can make Phi_O^tw block-cyclic with
   predictable determinant signs;

3. mine small rows for local-intersection evidence: when Delta_C(t)=0, does
   it correspond exactly to nontrivial coker(phi_t), with no extra vertical
   denominator factor?
```

The first identity is formal once bases are fixed; the useful part is catching
sign, centering, and quotient-basis errors before trying to prove the
class-field theorem.

The actual-CM block-cycle plumbing check is now recorded in:

```text
p24/centered_marginal_orbit_fitting_block_cycle_audit.md
p24/centered_marginal_orbit_fitting_block_cycle_audit.py
```

On the pinned `D=-13319, q=13463, m=28, n=5, pair=(4,7)` row, the direct-sum
and signed block-cycle determinants match the orbit products on all three
right Frobenius orbits, with singular controls detecting zero exactly.
Thus the crossed-product determinant-line assembly is sound; it is not the
missing arithmetic p-unit theorem.

## Boundary

This target still does not prove the certificate.  It narrows the missing
arithmetic theorem to a named object:

```text
the centered Schubert quotient map Phi_O^tw has p-unit determinant at the
selected p24 ordinary CM reduction.
```

That theorem must come from embedded non-genus `157/211` phase data, a
local-intersection formula, or an equivalent class-field identity.  A scalar
global product found after enumerating class origins would not meet the
asymptotic requirement.
