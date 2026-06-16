# Trace-GCD Prefix Adjoint Trace Independence

Date: 2026-06-06

## Point

The Schur-pivot target needs a named p-unit prefix theorem before the
`16 x 16` quotient-tail Schur complement can be useful.  The prefix part can
be stated without choosing coordinates or a Plucker pivot.

For p24 set:

```text
L = F_p(mu_157),        [L:F_p] = 156
R = F_p(mu_211),        [R:F_p] = 35
E = L R.
```

For the four representative prefix right orbits

```text
B = {O2,O3,O5,O6},
```

write their mixed periods as

```text
S_j = H_{157,211}(1,v_j) in E,      j in B.
```

The prefix trace map is:

```text
A_B : L -> R^4
lambda |-> (Tr_{E/R}(lambda*S_j))_{j in B}.
```

The desired prefix rank statement is:

```text
rank_Fp(A_B) = 4*35 = 140.
```

Since `dim_Fp L = 156`, this is equivalent to:

```text
A_B is surjective,
dim_Fp ker(A_B) = 16.
```

## Trace-Adjoint Form

Use the trace pairings:

```text
<x,y>_L = Tr_{L/F_p}(x*y),
<x,y>_R = Tr_{R/F_p}(x*y).
```

Then the `F_p`-adjoint of `A_B` is:

```text
A_B^* : R^4 -> L
(y_j)_{j in B} |-> Tr_{E/L}(sum_{j in B} y_j*S_j).
```

Indeed:

```text
sum_j Tr_{R/F_p}(y_j * Tr_{E/R}(lambda*S_j))
  = Tr_{L/F_p}(lambda * Tr_{E/L}(sum_j y_j*S_j)).
```

Therefore:

```text
rank_Fp(A_B) = rank_Fp(A_B^*).
```

The p24 prefix theorem can be stated intrinsically as:

```text
Tr_{E/L}(y_2*S_2 + y_3*S_3 + y_5*S_5 + y_6*S_6) = 0
  with y_j in R
  =>
y_2 = y_3 = y_5 = y_6 = 0.
```

This is the four-prefix analogue of the six-orbit trace-intersection theorem
already recorded in:

```text
p24/hermitian_mixed_trace_intersection_theorem.md
p24/hermitian_mixed_left_subfield_span_theorem.md
```

The six-orbit theorem asks whether the map `L -> R^6` is injective.  The
representative prefix theorem asks whether the four-block map `L -> R^4` is
surjective.

The same prefix condition was already present as the first local-unit target
in:

```text
p24/trace_gcd_local_unit_proof_target.md
```

and as the block-subspace-design rank statement in:

```text
p24/lang_block_subspace_design_boundary.md
```

The new point here is naming the exact adjoint map whose injectivity proves
that rank statement.

The same condition has an additive Hilbert-90 nonintersection form in:

```text
p24/trace_gcd_prefix_hilbert90_nonintersection.md
```

There the theorem becomes:

```text
span_R{S_2,S_3,S_5,S_6} cap (tau_R - 1)E = {0}
```

after also proving the four periods are `R`-independent.

## Direct-Sum Form

For each selected prefix orbit define the `F_p`-subspace:

```text
W_j = Tr_{E/L}(R*S_j) = {Tr_{E/L}(y*S_j) : y in R} subset L.
```

Then:

```text
image(A_B^*) = W_2 + W_3 + W_5 + W_6.
```

The prefix theorem is equivalently:

```text
W_2 + W_3 + W_5 + W_6 is a direct sum,
dim_Fp(W_2 + W_3 + W_5 + W_6) = 140.
```

This is the narrow CS/subspace-design formulation that is still genuinely
arithmetic: prove directness for four actual CM trace-dual subspaces, not for
a random block code.

## Relation To The Schur Pivot

If the adjoint map is injective, then the four prefix blocks have rank `140`.
Consequently some `140 x 140` prefix Plucker coordinate is a p-unit.  After
choosing such a coordinate pivot, the quotient-tail determinant can be
represented by the ordinary Schur complement from:

```text
p24/trace_gcd_residual_schur_pivot_target.md
p24/trace_gcd_residual_schur_complement_toy.py
```

This does not yet name the best row set `X` for the Plucker pivot.  It does
separate the two arithmetic obligations:

```text
1. prefix-adjoint injectivity:
   R^4 -> L is injective;

2. quotient-tail p-unit:
   the first 16 Lang/trace-dual functionals of O1 are nonsingular on
   ker(A_B).
```

Together these are exactly the representative `140+16` certificate.

## Why The Fixed Fourier Minor Theorem Is Not Enough

The fixed Fourier-head/Vandermonde theorem proves p-unitness of the projection
side in the selected Lang-head expansion.  It proves that the fixed
Schubert/Fourier coefficients are nonzero.

The prefix-adjoint theorem is about the actual CM periods `S_j`.  It asks
whether the `R`-linear combinations of four actual mixed periods have no
relative trace down to `L`.  Nonzero fixed Fourier coefficients do not prevent
cancellation in this actual CM Plucker/Fitting coefficient.

So the missing p24 theorem is still arithmetic:

```text
no nonzero R-linear combination of the four selected CM periods has
zero E/L trace.
```

## Coding-Theory Interpretation

The full trace-dual code is:

```text
Phi : L -> R^6 ~= F_p^210,
Phi(lambda) = (Tr_{E/R}(lambda*S_j))_j.
```

The representative bad event is a word supported inside the named
`54` scalar coordinates:

```text
O4 full block + final19(O1).
```

A scalar distance theorem

```text
wt(Phi(lambda)) >= 55       for every nonzero lambda
```

would prove the representative row.  MSRD/Gabidulin/subspace-design language
can help only if it proves this arithmetic distance for the actual CM trace
code.  Without that bridge, coding theory restates the nonintersection
condition.

This boundary is recorded in:

```text
p24/msrd_lrs_import_boundary.md
p24/representative_cs_theory_candidate_boundary.md
```

The prefix-adjoint theorem is the first half of this support statement:

```text
no nonzero lambda is supported entirely outside O2,O3,O5,O6
unless it lies in a 16-dimensional kernel K.
```

The second half is the tail-on-kernel determinant:

```text
first16(O1) separates K.
```

## Toy Gate

The finite linear-algebra equivalence is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_adjoint_trace_toy.py
```

The finite p24 handoff is Lean-checked in:

```text
p24/lean/TraceGcdPrefixAdjointGate.lean
```

It verifies in coprime finite extensions that:

```text
rank(A_B) = rank(A_B^*),
A_B is surjective <=> A_B^* is injective,
dim ker(A_B) = dim L - dim R^k,
```

and includes forced dependent controls where the prefix theorem fails.

## Current Missing Theorem

For the actual p24 embedded CM periods:

```text
Tr_{E/L}(sum_{j in {2,3,5,6}} y_j*S_j) = 0
  =>
all y_j = 0.
```

Once this is proved, the remaining target is the already isolated
linearized-resultant p-unit on the resulting `16`-dimensional kernel:

```text
det(tau_a(k_b))_{1<=a,b<=16} != 0 mod p.
```

This is now a sharper route than searching for an unnamed prefix Plucker
minor.
