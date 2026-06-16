# RS-Tail Frequency-Defect Gate

Date: 2026-06-06

## Point

The cyclic-shift displacement route had one circular-looking step: the
Plucker chart `C` exists only after the selected `156` columns are already
known to be a basis.

The frequency-defect gate removes that circle.  It gives a finite determinant
criterion before forming `C`.

## Finite Theorem Shape

Let `n` be prime to `p`, let `omega` be a primitive `n`th root, and let

```text
W subset F^{6n}
```

be invariant under the common cyclic shift on six length-`n` blocks.  After
Fourier diagonalization,

```text
W = direct_sum_{a in Z/nZ} W_a,
W_a subset F^6.
```

Keep four full blocks, keep the first `k` time samples of a fifth tail block,
and omit the sixth block plus the remaining `n-k` tail samples.

Assume there is a defect frequency set `A`, `|A|=k`, such that:

```text
for a notin A:
  dim W_a = 4
  projection W_a -> four selected full blocks is an isomorphism;

for a in A:
  dim W_a = 5
  projection W_a -> four selected full blocks has rank 4;
  projection W_a -> four selected full blocks plus the tail block has rank 5.
```

Then projection

```text
W -> selected coordinates
```

is an isomorphism.

## Proof

Suppose `w in W` vanishes on the selected coordinates.

The four full selected blocks vanish at every time.  Fourier inversion gives
that, for every frequency `a`, the component `w_a in W_a` maps to zero in the
four selected full block coordinates.

For `a notin A`, the local projection is an isomorphism, hence `w_a=0`.

For `a in A`, the local projection kernel is a line.  The rank jump after
adding the tail block is exactly the basis-free statement that this kernel
line has nonzero tail coordinate, so

```text
w_a = c_a l_a,
```

where the tail coordinate of `l_a` is `tau_a != 0`.

The first `k` tail samples vanish, so the coefficients `c_a` satisfy

```text
sum_{a in A} c_a tau_a omega^{a s} = 0,      0 <= s < k.
```

This is a `k x k` Vandermonde matrix in the distinct values `omega^a`, scaled
by the nonzero `tau_a`.  Its determinant is

```text
(product_{a in A} tau_a) * product_{a<b}(omega^b - omega^a),
```

so it is nonzero.  Therefore all `c_a=0`, hence `w=0`.

Since `dim W = 4n+k`, which equals the number of selected coordinates, the
selected projection is an isomorphism.

## P24 Specialization

For the fixed RS-tail square:

```text
n = 35
k = 16
selected coordinates = 4*35 + 16 = 156
omitted coordinates  = 35 + 19 = 54
```

The target p24 proof can now be sharpened to:

```text
1. construct the common cyclic/Lang shift integrally;
2. diagonalize it by the p-unit Fourier transform because p does not divide 35;
3. prove 19 ordinary local prefix projections are p-unit isomorphisms;
4. prove 16 defect local prefix projections have p-unit rank 4 and p-unit
   rank jump after adding the tail coordinate;
5. multiply by the 16x16 tail Vandermonde p-unit.
```

This proves `det(Psi_RS)` is a p-unit and only then forms the Plucker chart
used by the low-displacement/Riccati route.

## Evidence

The finite gate and its controls are implemented in:

```text
p24/trace_gcd_rs_tail_frequency_defect_gate_toy.py
p24/trace_gcd_rs_tail_basis_free_frequency_gate_toy.py
p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
p24/trace_gcd_actual_cm_frequency_defect_boundary.py
p24/trace_gcd_actual_cm_basis_free_section_audit.py
p24/lean/TraceGcdFrequencyDefectGate.lean
p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean
```

It verifies:

```text
frequency-defect gate => selected basis;
the same gate is basis-free under arbitrary local row-basis changes;
zero defect tail residue => selected rank drops;
bad ordinary local Plucker gate => selected rank drops.
all three rows are cyclic-shift invariant;
the two failing controls have a nonzero omitted-support kernel.
```

So cyclic invariance alone is not enough.  The selected-basis theorem needs the
local frequency projection-rank p-units and defect prefix-to-prefix-plus-tail
rank jumps, after which the tail Vandermonde factor is automatic.

In any chosen p-integral local basis this is the older Plucker/minor and
tail-residue statement.  The basis-free form is the proof-facing version:
the actual CM/Lang spectral rows need only supply descended projection maps,
not a friendly row basis.

The actual-CM boundary audit measures this local profile on the current
smaller uploaded rows.  It reports `frequency_profile_gate_rows=0/10` and
`clean_p24_like_shape_rows=0/10`: tail-only full-rank rows are too small to
calibrate the p24 gate, and prefix-plus-tail singular controls have extra tail
residue frequencies (`3` visible where the toy p24 defect model would have the
smaller local tail dimension).  Thus the smaller rows remain useful boundary
data, not positive evidence for the p24 p-unit local theorem.

The basis-free section audit refines this failure.  On the same rows, the
rank profile is Frobenius-covariant in `10/10` cases and no support is
nonstable, so cyclic descent is not the observed obstruction.  The nontrivial
prefix-plus-tail rows fail because their defect support has the wrong size in
`4/4` cases.  This points the p24 proof at an intrinsic defect-selector
theorem, especially the no-fixed-frequency-defect lemma, rather than at a
descent workaround.

The Lean gate records the finite handoff and p24 counts:

```text
19 + 16 = 35,
19*4 + 16*5 = 156,
4*35 + 16 = 156,
35 + (35 - 16) = 54,
gcd(10^24+7,35)=1.
```

The separate fixed-frequency order-7 Lean gate records the next finite
handoff:

```text
order-7 augmentation + P4=y^(-2)T + denominator unit
  => seven fixed-frequency tail-in-prefix relations;
tail-in-prefix + prefix Plucker p-units
  => no fixed defects;
no fixed defects
  => stable size-16 support candidates reduce from 1260 to 35.
```

## Relation To Moore/Schur

The frequency-defect gate is the diagonalized local form of the existing
Moore/Schur split.

Order the selected coordinates as four full selected blocks followed by the
`k` tail samples.  After Fourier diagonalization, the selected matrix is block
diagonal up to p-unit Fourier and permutation factors:

```text
prefix block:
  product over all n frequencies of local 4x4 Plucker determinants;

tail quotient block:
  k x k Vandermonde on the defect frequencies, scaled by tau_a.
```

Thus:

```text
Delta_selected
  = p-unit
    * product_a Delta_local_prefix(a)
    * product_{a in A} tau_a
    * Vandermonde(omega^a : a in A).
```

This identifies the frequency-local Plucker product with the prefix Moore
factor and the defect tail residues with the quotient-tail Moore factor.  The
toy

```text
p24/trace_gcd_rs_tail_frequency_moore_schur_factor_toy.py
```

checks the factorization and shows that both failing controls remain
cyclic-shift invariant.

The resultant packaging note

```text
p24/trace_gcd_rs_tail_frequency_resultant_gate.md
```

records the next proof target: construct cyclic polynomial sections
`P_24(x)`, `T_24(x)`, and a defect selector `S_24(x)` so that
`Res(P_24,x^35-1)` and `Res(T_24,S_24)` are the local Plucker and defect
tail-residue products.  The toy checks that these resultants imply the local
frequency gates, while zero-Plucker, zero-tail-residue, and wrong-support
controls are rejected.

The descent note

```text
p24/trace_gcd_rs_tail_cyclic_section_descent.md
```

records the guardrail that local values must satisfy `F_{p a}=F_a^p` to
descend to base cyclic sections; arbitrary splitting-field interpolants are
post-fit and not certificate evidence.  It also records the p24 defect-support
accounting: a base selector of size `16` must be Frobenius-stable, but descent
alone allows either four length-4 orbits (`35` choices) or four fixed
frequencies plus three length-4 orbits (`1225` choices).  The reduction to
only four length-4 orbits needs the extra arithmetic theorem that fixed
frequencies are ordinary.  The finite fixed-frequency ordinary gate sharpens
that theorem to `tau_a in image(P_a)` for every fixed `a in 5Z/35Z`, and
checks that mixed fixed supports are not rejected by descent or the tail
Vandermonde alone.

## Remaining Arithmetic

The missing theorem is now local:

```text
prove the required p24 local frequency Plucker minors and tail residues are
p-units from the CM/Lang construction, without enumerating the class set.
```

The newest narrower form is:

```text
identify the CM/Lang cyclic sections P_24,T_24,S_24 and prove their
resultants/selector discriminant are p-units.
```

This is narrower than the previous hidden-MSRD/LRS statement and avoids the
post-fit displacement pitfall.
