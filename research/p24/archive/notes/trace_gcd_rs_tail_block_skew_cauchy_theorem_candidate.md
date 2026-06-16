# RS-Tail Block/Skew Cauchy Theorem Candidate

The selected fixed square uses `156` of the `210` natural fixed-source
columns.  If the selected columns are a basis, the omitted `54` columns define
a Plucker-ratio chart

```text
C in Mat_{156 x 54}(F_p).
```

The visible scalar-GRS toy tests the special case in which this chart is
scaled Cauchy.  That is too narrow.  The block/skew Cauchy candidate is the
operator identity

```text
A C - C B = R S,                 rank(R S) <= rho,
```

where:

```text
A = transported operator on the selected 156-dimensional side,
B = transported operator on the 54-dimensional omitted/erasure side,
R,S = low-rank residue maps coming from the same class-field/Lang data.
```

The canonical p24 candidate for `A` and `B` is now sharper: take the full
coordinate cyclic shift on the six `35`-coordinate Lang blocks, reorder
coordinates as selected plus omitted, and use the selected and omitted diagonal
blocks `M_SS` and `M_OO`.  The four full selected blocks and the omitted full
block are shift-stable; only the truncated tail block has two cut edges.  Thus
the expected low-rank residue is controlled by two rank-one boundary maps.

For a graph chart `[I C]` whose full row space is invariant under this shift,
the exact identity is the graph/Riccati equation

```text
M_SS C + C M_OS C - C M_OO - M_SO = 0.
```

Consequently the pure Sylvester displacement

```text
M_SS C - C M_OO
```

has rank at most `rank(M_SO)+rank(M_OS)`, which is `2` for the p24 tail split.
This identifies the candidate operators without postfitting them to `C`.

In the scalar Cauchy case `C_ij = u_i v_j/(x_i-y_j)`, this becomes

```text
diag(x) C - C diag(y) = u v^T,
```

so the entrywise-inverse rank `<= 2` invariant is only the scalar shadow of the
more useful displacement-rank theorem.

## P-Unit Consequence

A p24 proof via this route must construct `A,B,R,S` over the p-integral
CM/Lang model, with p-unit changes of basis, and prove a small `rho`
independent of the class set.  Then the omitted `54`-coordinate erasure
condition becomes a named block/skew Cauchy or MSRD erasure theorem.  Since
`54 < 55 = 210 - 156 + 1`, an actual hidden MSRD/LRS equivalence of the
full `210`-column object would imply the selected determinant is a p-unit.

Equivalently, this theorem would prove `det(Psi_RS)` is a p-unit without
enumerating the `h = 205880396014` class set.

## Current Evidence

Supported:

```text
p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py
p24/trace_gcd_plucker_displacement_handoff_toy.py
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
p24/trace_gcd_rs_tail_cyclic_operator_boundary_toy.py
p24/lean/TraceGcdPluckerDisplacementHandoffGate.lean
```

The new displacement toy verifies:

```text
scalar Cauchy => displacement rank 1;
scalar entrywise-inverse rank <= 2 is the scalar shadow;
block resolvent/skew Cauchy => low Sylvester displacement rank;
transported basis changes preserve the rank;
random charts with the same dimensions fail.
low-rank full-column operator boundary => low-rank chart displacement;
random fixed-operator charts fail while post-fit operators can cheat.
shift-invariant full code => cyclic-shift displacement rank 2;
corrected cyclic-shift Riccati residual rank 0;
p24 boundary ranks are expected to be 1 and 1 from the two tail cut edges.
cyclic/Lang column boundary => rank-two Plucker handoff residue;
whole omitted block contributes no boundary, only the split tail block does.
```

Boundary:

```text
p24/trace_gcd_actual_cm_full_plucker_chart_boundary.py
p24/trace_gcd_actual_cm_frequency_defect_boundary.py
```

The present small actual-CM rows do not contain a nontrivial selected-basis
calibration row for the full chart, so they cannot validate or falsify this
candidate yet.  The matching frequency-profile audit also finds no clean
p24-like local-gate calibration: tail-only rows are too small, and the
prefix-plus-tail singular controls fail the local frequency gate.

## Non-Circular Frequency Gate

The selected-basis step can be isolated before forming the Plucker chart:

```text
p24/trace_gcd_rs_tail_frequency_defect_gate_theorem.md
p24/trace_gcd_rs_tail_frequency_defect_gate_toy.py
p24/trace_gcd_rs_tail_frequency_resultant_gate.md
p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py
p24/trace_gcd_rs_tail_cyclic_section_descent.md
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
```

After diagonalizing the common cyclic/Lang shift, the finite theorem requires
`19` ordinary local frequency projections to be p-unit isomorphisms and `16`
defect frequency lines to have p-unit tail residues.  The remaining `16 x 16`
tail gate is a Fourier/Vandermonde determinant, hence a p-unit because
`p` does not divide `35`.

This turns the chart assumption into an explicit local arithmetic obligation:
prove those local Plucker minors and tail residues are p-units from the
CM/Lang construction.  The toy controls now also show that the failing rows are
still cyclic-shift invariant; the extra p-unit local gates, not cyclic
invariance by itself, are what remove omitted-support kernel vectors.

The frequency-resultant gate is the next possible compression of that
obligation: if the local Plucker and defect-residue values are evaluations of
CM/Lang cyclic sections, then two resultant/Bezout p-unit certificates plus
the defect selector support replace the individual frequency checks.
The cyclic-section descent gate adds the necessary guardrail: those local
values must be semilinear Frobenius-compatible, and the defect support must be
Frobenius-stable, before a base resultant certificate is legitimate.

The actual-CM frequency-profile audit checks that this obligation is not
already visible in the smaller rows: `frequency_profile_gate_rows=0/10`, so no
small uploaded row currently substitutes for the missing p24 local theorem.

## Next Testable Consequence

Once an actual row has a nontrivial selected basis for the full selected-plus-
omitted span, compute the Plucker chart `C` and test whether the known
Lang/Frobenius transport operators give low rank for `A C - C B`.  The first
operator pair to test is the selected/omitted block decomposition of the
transported coordinate cyclic shift.  The test must use operators fixed by the
arithmetic construction, not fitted after seeing `C`; otherwise it is only a
generic low-rank fitting problem.

A stronger block-LRS version should also expose normalized block Plucker
cross-ratios.  After fixing three block kernels by p-unit block changes, the
remaining block spectra should agree with the same transported skew-Cauchy
operator data.  A mismatch on a genuine selected-basis actual row would falsify
the hidden block-LRS strengthening while leaving the direct Sylvester
transversality route open.
