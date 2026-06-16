# p24 Retrospective Synthesis

Date: 2026-06-06 / 2026-06-07

Purpose: hand a fresh agent the benefit of the whole search without forcing
them to reload the archive.  This note is intentionally about composition:
which facts survived, which failures mean something, and where old fragments
may now fit the current theorem.

This is not a proof of the p24 certificate.  It is a map of the proof state.

## Read This First

The `p24/` folder is now a research archive:

```text
files total:       1343
markdown notes:     559
python probes:      634
lean gates:         121
```

Do not start by reading all route files.  Start with the front-door handoff,
then read:

```text
p24/00_HANDOFF_INDEX_20260607.md
p24/00_FRESH_EYES_SYNTHESIS_20260607.md
p24/00_CURRENT_CONTEXT.md
p24/00_FRESH_AGENT_HANDOFF_20260607.md
p24/00_GLOBAL_SYNTHESIS_HANDOFF.md
p24/00_THEOREM_ATTEMPTS_LEDGER.md
p24/00_ROUTE_MAP.md
```

After that, load only the narrow route files named by the synthesis.

## One Honest Sentence

We have a small verifier surface and many formal equivalences, but not yet the
arithmetic producer theorem.  The current frontier is no longer "find a clever
search"; it is "prove an explicit selected CM/Lang/Jacobi product identity."

## Fixed Facts

```text
p = 10^24 + 7
sqrt_floor = 10^12
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441

E = F_p(mu_m), [E:F_p] = 5460
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7
rho = p^780 fixes the left 157-frequency and shifts the right quotient by 6
raw relative order of rho = 38843 = 7 * 5549
```

The class group is cyclic and squarefree.  That is good tower bookkeeping; it
is not an embedded root selector above the split prime.

## Certificate Surfaces

There are three useful scales.

```text
best hoped-for final payload:
  4 field elements:
  Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
  about 4e-12 * sqrt(p)

fixed-frequency verifier:
  156 * 7 = 1092 scalar equations
  compressed as 48 = 42 mixed octic + 6 anchor equations

selected-chain fallback:
  3107811 slots = 3.107811e-6 * sqrt(p)
```

The small verifier and the four-element payload are conditional.  The missing
input is still a p-unit/product-formula producer, not finite linear algebra.

## What We Actually Learned

### 1. Generic CM Structure Is Too Weak

Repeated actual-CM controls fail the identities we need:

```text
D=-4751:   0/91 full mixed/anchor/recombined-balance shifts
D=-5000:   0/60 raw packets with zero trivial C projection
D=-6719:   covariance and telescope hold, anchor descent fails
D=-13319:  right-combo/product internal traces and anchors fail
D=-13319 selected defects:
            140/140 force C-zero fiber
              0/140 satisfy full inversion/row-balance identities
```

So the missing theorem cannot be "ordinary CM packet plus covariance."  It
must use the selected weighted trace-GCD packet, an explicit CM/Lang unit, or
a principal divisor/product formula.

### 2. Cyclic Tower Bookkeeping Does Not Select Roots

The `2,157,211,3107441` tower is unique as a subgroup tower, but the embedded
children over the ordinary split prime are torsors.  Genus/quadratic data
helps only at the order-2 layer.  The odd layers still need non-genus phase
data or determinant-line p-unit data.

This killed the seedless class-field-tower selector route, but it did leave
useful quotient bookkeeping for the trace-GCD route.

### 3. Frobenius Covariance Is Usually The Obstruction, Not The Proof

The p24 action `rho=p^780` is perfectly aligned with the right quotient:

```text
right shift = 6 mod 7.
```

But covariance alone places a packet in a nontrivial eigenspace.  It does not
make it zero.  After descent/recombination, the nontrivial covariance claim
can become equivalent to the desired vanishing, hence circular.

The surviving use is:

```text
covariance + telescope + one honest descended anchor => seven H-coset sums zero.
```

The anchor is the arithmetic theorem.

### 4. Hilbert-90 Is A Handoff, Not A Discovery Tool

The product-coboundary machinery is formal once nested internal trace zero is
proved.  Inverting Hilbert-90 after discovering trace zero is fine for the
certificate handoff.  Using Hilbert-90 inversion to produce the trace-zero
identity is circular.

The current honest order is:

```text
prove selected CM/Lang internal trace zero
  => matching right coboundary
  => product coboundary
  => six right-character vanishings
  => 1092 verifier equations
```

### 5. The Best Current Theorem Is Rank-621 Admissible Jacobi Membership

After `Tr_{B/C}`, the current target is a packet on:

```text
C_7 x C_179.
```

The strongest finite form is membership in the rank-621 admissible C-axis
Jacobi-carry span.  The carry is:

```text
theta_{u,v}(t) = [ut] + [vt] - [(u+v)t]

u right-trivial and C/E-nontrivial
v C/E-nontrivial
u+v C/E-nontrivial
```

The broad C-axis family has rank `625`, but four directions leak.  Do not use
the broad family unless those four leaks are explicitly killed.

Equivalent Fourier conditions on `C_7 x C_179`:

```text
F(a,0)=0 for a=1,...,6
F(a,b)+F(-a,-b)=0 for nontrivial right a and C/E conjugate pairs
F(0,b)+F(0,-b)=(-1/89)*F(0,0)
sum_{b>0}(F(-a,b)-F(a,b))=0 for a=1,2,3
```

Counts:

```text
6 + 6*89 + 89 + 3 = 632 equations
ambient dimension = 7*179 = 1253
solution dimension = 621
```

### 6. The Same Target Has A Cleaner Value/Product Form

For raw packet `g(r,c)` and selected defect:

```text
f(r,c) = g(r,c) - g(r,0)
```

it is enough to prove:

```text
g(r,0)+g(-r,0)=A_0
g(r,c)+g(-r,-c)=A_1 for c != 0
sum_c g(r,c)-179*g(r,0)=B independent of r
```

Multiplicatively, for `U(r,c)=omega^g(r,c)`, this becomes:

```text
U(r,0)U(-r,0)=alpha_0
U(r,c)U(-r,-c)=alpha_1 for c != 0
prod_c U(r,c)/U(r,0)^179 = beta.
```

This is the current best mathematical shape: constant pair-products plus a
constant selected row-product ratio.

### 7. Literal Jacobi Sums Explain A Real Part Of The Target

Small exact finite-field Jacobi-sum probes with `N=7c` show:

```text
raw off-C-zero pair-products: 3/3 rows pass
raw full selected row-product ratio: fails in right-mixed cases
```

The failure is now sharply localized.  For right-mixed Jacobi sums:

```text
all six nonzero right rows have the same selected row-product ratio;
only the right-zero anchor differs;
the anchor defect is universal across sampled admissible pairs for each c.
```

Even better, the literal finite-field defect has the exact formula:

```text
delta_c = (q - 2)^(-(c - 1)).
```

Reason:

```text
J(1,1)=q-2
J(1,lambda)=-1 for lambda nontrivial
```

Checked samples:

```text
c=5:  delta_c = 44  in F_211
c=11: delta_c = 586 in F_617
c=13: delta_c = 589 in F_911
right_mixed_anchor_defect_formula_rows=3/3
```

This defect is not a `mu_(7c)`, `mu_7`, or `mu_c` multiplier and has no
`c`-th root in the sampled value fields.  So the correction cannot be a mere
root-of-unity normalization.  It must be a genuine selected-anchor,
distribution, residue, or unit correction.

The newest gate identifies the literal correction in the finite-field Jacobi
model.  Normalize only the single degenerate anchor:

```text
U(0,0)=J(1,1)=q-2
U'(0,0)=U(0,0)/(q-2)=1
```

and leave every other packet value unchanged.  This simultaneously repairs
the C-zero pair-products and the selected row-product ratio, exhaustively over
the right-mixed admissible pairs for c=5,11,13:

```text
exhaustive_right_mixed_pairs=72,540,792
single_anchor_correction_rows=3/3
corrected_pair_product_rows=3/3
corrected_row_ratio_rows=3/3
corrected_product_formula_rows=3/3
anchor_scale_formula_rows=3/3
```

So in the literal Jacobi model, the three global balances are not mysterious
independent equations.  They are the single `J(1,1)/(q-2)` degenerate-anchor
normalization plus the punctured Hasse-Davenport product formula.

The symbolic Hasse-Davenport gate removes finite-field summation from this
part of the problem.  It checks c=5,11,13,17,19 and p24 c=179 by residue
accounting: `B_k` and `A_kB_k` run through the same punctured C-coset, so
their Gauss factors cancel in the selected row ratio.  For p24 this covers
all `189036` right-mixed admissible pairs.  The remaining open input is the
CM/Lang realization of the reduced packet.

The reduced-anchor fingerprint gate translates the single multiplicative
anchor into selected-defect coordinates.  The raw correction `-e_(0,0)`
becomes the punctured right-zero row.  For p24 this has `178` nonzero entries,
Fourier values `H(a,0)=178`, `H(a,b)=-1` for `b != 0`, and right difference
supported on the two adjacent rows around right-zero.  This fingerprint alone
leaks forbidden C-trivial bidegrees, so it must cancel the matching raw
Jacobi/CM-Lang leak.

The reduced-anchor / adjacent-anchor bridge now makes the old covariance
route a slice of the same object.  The adjacent-anchor descent theorem sees
only the `C/E`-trivial row-sum slice `A=(c-1)e_0` of the punctured row.  For
p24 this is `178*e_0`; all six nontrivial right projectors are nonzero, and
adjacent difference multiplies them by nonzero scalars.  Thus the old anchor
target is cancellation of this `b=0` leak, while the full CM/Lang unit still
has to realize the whole punctured right-zero row.

The reduced-anchor C-slice decomposition isolates the rest of that row.  The
`C/E`-nontrivial residual has zero row sums, is invisible to the old
adjacent-anchor theorem, and has Fourier profile `H(a,0)=0`, `H(a,b)=-1` for
`b!=0`.  For p24 this is `1246` nonzero `C/E`-nontrivial Fourier channels.
So the old covariance branch accounts for the six `b=0` right channels; the
new arithmetic theorem must realize the full residual with a selected
CM/Lang unit and p-integrality.

## The Most Promising Composition

The old right-difference/covariance branch and the new Jacobi branch now look
like two views of the same missing anchor.

Old branch:

```text
adjacent right-difference traces T_i
covariance:  T_{i+6}=rho(T_i)
telescope:   sum_i T_i=0
missing:     rho(T_0)=T_0
```

New branch:

```text
Jacobi/Hasse-Davenport punctured-right theorem
  => nonzero right rows already balanced
single degenerate-anchor normalization
  => right-zero anchor cancels delta_179
```

Composition to test/prove:

```text
the adjacent-anchor descent condition is exactly cancellation of the
C/E-trivial row-sum slice of the Hasse-Davenport right-zero defect.
```

If this is true, the problem is no longer 632 unrelated equations.  It becomes:

```text
prove the punctured Hasse-Davenport/Jacobi product identity;
prove one selected trace-GCD anchor correction.
```

That is the cleanest route currently visible.

## Other Compositions Worth Rechecking

1. Admissible Jacobi span plus right-difference trace:
   the four Fourier families may split into structural conjugate-pair
   equations plus the three global balances seen by adjacent differences.

2. p^780 covariance plus admissible pair compatibility:
   compatibility may remove the `C/E`-trivial component that blocks anchor
   descent, but old anchor-vs-C-centering controls show this is not automatic.

3. Fixed-frequency augmentation plus internal-character filter:
   the older `R_7=F_p[y]/(y^7-1)` augmentation identity may be the same six
   nontrivial projector vanishings after the `B/C` trace.

4. Paired-kernel criterion plus admissible span:
   perhaps leakage need not vanish before pairing if the rank-621 structure
   forces the six projectors into the selected left kernel.

5. Two-resultant surface plus fixed-frequency theorem:
   if the H-coset theorem proves no fixed defects, recheck whether it supplies
   the fixed-orbit determinant p-unit needed by the four-element certificate.

## Routes Not To Reopen Casually

Do not retry these unless a new ingredient directly changes the failure mode:

```text
class-set enumeration as the main proof
abstract cyclic squarefree tower selector
generic CM covariance
ordinary left-character pairing
plain Stickelberger/right-axis Stickelberger
generic Jacobi carries outside the admissible C-axis subfamily
trace-only anchor compression
anchor-only compression without C/E centering
post-fit interpolation or post-fit displacement operators
visible natural-coordinate GRS/Cauchy signatures
Strong-Rayleigh / matrix-tree shortcuts without CM weights
Lean as theorem-discovery engine
large computations producing only pass/fail bits
```

## What Computation Should Do Now

Compute is useful, but it should be a theorem microscope.

High-value experiments:

```text
1. Prove/test the punctured Hasse-Davenport row-product theorem abstractly.
2. Build exact small analogues with the selected trace-GCD weighting, not only
   generic CM rows.
3. Report the four Fourier-family residuals separately.
4. Report the three value-side residuals separately.
5. Test whether the right-difference anchor equals the Jacobi right-zero
   anchor defect.
6. Mine explicit unit/divisor exponents for the selected anchor correction.
7. Use many small exact runs in parallel, but make each output a formula or
   residual vector, not just a pass/fail bit.
```

Low-value experiments:

```text
full p24 class-set enumeration;
generic actual-CM rows without selected weighting;
support-only checks;
post-fit sections/operators;
long CPU jobs that do not test a named theorem.
```

## Lean Should Formalize The Handoff

Lean is useful for:

```text
product identities => value identities;
value identities => Fourier families;
Fourier families => admissible span;
admissible span => forbidden bidegree zero;
forbidden bidegree zero => internal trace zero;
internal trace zero => right/product coboundary;
six character vanishings + centering => 1092 verifier;
payload count inequalities.
```

Lean is not expected to discover the CM/Lang product formula.  Use it after
the objects are explicit.

## The Next Theorem To Try To Prove

The best single statement to attack is:

```text
For the selected weighted trace-GCD packet after Tr_{B/C}, there is a
p-integral multiplicative lift U(r,c) whose divisor/product formula is the
literal admissible Jacobi punctured-right Hasse-Davenport formula, and whose
selected right-zero anchor contains the CM/Lang analogue of the
J(1,1)/(q-2) normalization, cancelling the universal
delta_179 = (q-2)^(-178)-type defect in the p24 specialization.
```

This wording is deliberately schematic because the actual `q-2` analogue in
the p24 CM/Lang unit setting must still be identified.  But it captures the
newest global synthesis:

```text
most equations are now structural;
the remaining obstruction is one selected degenerate-anchor unit;
generic CM data says the correction is not automatic;
literal Jacobi sums say the correction is exactly the J(1,1)/(q-2)
normalization.
```

## Current Confidence

Closer:

```text
the verifier is small;
the finite implication stack is mostly formal;
the live theorem is much narrower than before;
the exact row-zero Jacobi defect is a real new clue.
```

Still uncertain:

```text
we have not identified the p24 CM/Lang unit or divisor producing the selected
anchor correction;
actual-CM controls argue hard against universal shortcuts;
success probably requires a new explicit finite-field/CM product identity.
```

So the right posture is neither "blocked" nor "nearly done."  We are in a
better-defined proof search with one very sharp obstruction.
