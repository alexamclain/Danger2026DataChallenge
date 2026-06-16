# Marginal Block-Moore Theorem Candidate

This note records the useful rank-metric import for the current CRT marginal
theorem.

## Linear Algebra Lemma

Let `C/E` be a finite field extension of degree `d`, with `Q=|E|`.  For
vectors

```text
v_i = (v_{i,1},...,v_{i,k}) in C^k,      i=1,...,r,
```

define the block-Moore matrix over `C`:

```text
BM(v)_{i,(ell,j)} = v_{i,ell}^{Q^j},
ell=1,...,k,  j=0,...,d-1.
```

Then:

```text
rank_E{v_i in C^k} = rank_C BM(v).
```

Proof sketch: choose a normal `E`-basis of `C`.  Expanding all `v_i` in this
basis gives an `r x k*d` matrix over `E`.  Applying the `Q^j` Frobenius
coordinates is right multiplication by a block-diagonal Moore matrix attached
to the normal basis.  That matrix is invertible over `C`, and scalar
extension from `E` to `C` preserves row rank.

So the p24 marginal-rank theorem can be stated as block-Moore nonvanishing,
not just as coordinate rank in an arbitrary trace basis.

## p24 Specialization

For the tensor-factor trace-frame reduction:

```text
E = F_p(mu_m)
C/E has degree 179
Top_k(J_r(theta)) in C^k
```

The three marginal targets become:

```text
Omega_1:
  158 rows in C
  block-Moore width = 179
  need rank_C = 158

Omega_211:
  210 rows in C^2
  block-Moore width = 2*179 = 358
  need rank_C = 210

Omega_3:
  368 rows in C^3
  block-Moore width = 3*179 = 537
  need rank_C = 368
```

This is exactly the rank-metric/Gabidulin surface:

```text
no nonzero structured CRT-axis source word is killed by every Frobenius
coordinate functional in the selected Top_k window.
```

## Why It Helps

The block-Moore form is coordinate-free over `C/E`.  It avoids making the
proof depend on a chosen normal-basis coordinate minor and connects the target
to normal-basis/class-field language:

```text
selected CM marginal rows are rank-metric normal on the CRT-axis source.
```

This could beat sqrt scaling if the determinant/minor can be identified as a
class-field norm or p-unit.  The proof would verify a fixed block-Moore
nonvanishing in the degree-179 trace-frame surface, then use the existing
Lean-checked descent chain.

## Boundary

This lemma is an equivalence, not the missing arithmetic theorem.  It does not
explain why the p24 CM rows have full `E`-rank; it only gives a better
intrinsic object whose p-unit status might be provable.

The structured-code audit:

```text
p24/tensor_factor_marginal_cs_structure_audit.py
```

shows that natural trace-coordinate matrices do not have low
Toeplitz/Hankel/cyclic displacement rank in the pinned toy row.  The
block-Moore route is therefore the surviving rank-metric formulation, not an
observed elementary structured-matrix determinant.

## Lean Use

Once the arithmetic theorem is fixed, Lean can productively check the finite
linear-algebra implication:

```text
block-Moore rank full
  => marginal E-rank full
  => CrtMarginalAnnihilatorGate hypotheses
  => axis injectivity
  => L1 packet nonvanishing.
```

The arithmetic p-unit theorem itself is still outside the current Lean gate.
