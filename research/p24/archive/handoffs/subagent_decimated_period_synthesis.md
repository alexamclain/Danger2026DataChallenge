# Subagent Decimated-Period Synthesis

Date: 2026-06-06

Source: existing subagent `019e9b29-643e-7fb0-b4fb-273c97ab129c`.
No edits were made by the subagent.

## Ranked Proof Routes

### 1. Factorized Schubert / Schur-Complement p-Unit

Best candidate theorem:

```text
Top_2 prefix p-unit
+ minimal 10-dimensional A/B intersection
+ residual-tail p-unit on that forced intersection
=> Top_3 injective on W_axis.
```

Here:

```text
A = W_0 + W_2 + W_157,      dim A = 158
B = W_211,                  dim B = 210
dim C^2 = 358
```

so a successful prefix theorem must have:

```text
dim Top_2(A) cap Top_2(B) = 158 + 210 - 358 = 10.
```

Then the third trace coordinate must separate this forced `10`-dimensional
kernel.

Why plausible: this exactly matches the selected `179 + 179 + 10 = 368`
coordinate shape and uses the 31-term trace only through the relative
coefficient flag.

First falsifier:

```text
p24/trace_frame_prefix_intersection_audit.py
p24/trace_frame_leading_residual_value_audit.py
```

Look for a dimension-sufficient small CM row where component ranks are full
but the A/B intersection is larger than forced, or where the residual-tail
determinant vanishes.

Likely obstruction: component p-units alone are too weak.  Existing
forced-kernel audits show cross-block cancellation in dimension-forced cases.

### 2. Relative Low-Degree Exclusion / Divisor Theorem

Candidate theorem:

```text
no nonzero CRT-axis combination satisfies
g'(theta) * x_w in C[theta]_{<=27}.
```

Equivalently:

```text
W_axis(B) cap F_27 = {0}.
```

Why plausible: the decimated 31-term trace makes failure a relative-degree
`27` congruence instead of a raw degree-`388430` rank statement.

First falsifier:

```text
p24/trace_frame_low_degree_congruence_audit.py
```

Likely obstruction: forced small kernels already use multiple axis blocks and
fill the low tail, so sparse-tail or one-component arguments are unlikely.

### 3. Hidden MSRD/LRS / Folded-Moore Identity

Candidate theorem:

```text
after the g'(theta) relative coefficient map B ~= C^31,
W_axis(B) is p-unit block-equivalent to an MSRD/LRS sum-rank code
of E-dimension 368 and distance at least 5013.
```

Then every 3-block projection is injective, including the selected top-three
projection.

Why plausible: the code has 31 blocks of size 179, dimension 368, and
Singleton bound 5182, so the required distance has slack 169.

First falsifier:

```text
p24/trace_frame_msrd_invariant_audit.py
p24/tensor_factor_relative_block_structure_audit.py
```

Likely obstruction: natural-basis audits show random-like/maximal
displacement ranks, so a proof would need a non-obvious class-field
block-equivalence.

### 4. CRT Character-Module Direct Position

Candidate theorem:

```text
the 211 packet-field character module and the {0,2,157} module have minimal
relative trace-frame intersection, and the residual 10-head separates that
forced intersection.
```

Why plausible: `ord_211(p)=35` divides `ord_n(p)=388430`, so the 211-axis
diagonalizes inside the H-packet field, while the 157-axis requires external
character scalars.  This asymmetry may be useful if handled through the
tensor/Moore scalar-extension formalism.

First falsifier:

```text
p24/component_character_module_scan.py
p24/k_character_tensor_factor_block_scan.py
```

Likely obstruction: packet-field DFT can change base-field rank, so
diagonalization is a coordinate chart, not an automatic proof.

## Shortcut To Avoid

Small-support coordinate-minor compression remains unlikely.  The beta and
trace-coordinate support audits show selected Plucker minors rapidly acquire
full beta-character support, so a sparse interpolant/resultant explanation is
not the promising route.

## Current Recommendation

The next proof-facing target should be the factorized Schubert theorem:

```text
Top_2(A) and Top_2(B) have full rank,
their intersection has the forced dimension 10,
and Top_3/Top_2 separates that 10-dimensional intersection.
```

This is the most structured form of the decimated-period rank theorem and
the most likely place where a new finite-field/class-field identity could
replace class-set enumeration.
