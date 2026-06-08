# p24 Fresh-Eyes Synthesis

Date: 2026-06-07

Purpose: reset the global picture after the large p24 exploration.  This is
the note to read when the work starts feeling branchy.  It is organized around
what survived, what failed for structural reasons, and which old fragments now
compose with the current proof target.

This is not a certificate.  It is a context-saving handoff.

## Bottom Line

We are not done, and the remaining uncertainty is still real.  But the problem
is no longer a broad search through the class set.

The current state is:

```text
small verifier surfaces exist conditionally;
finite implication chains are heavily tested;
generic CM shortcuts have mostly been ruled out;
the remaining theorem is an explicit selected CM/Lang/Jacobi producer.
```

The best current proof shape is:

```text
punctured Hasse-Davenport/Jacobi product formula
+ selected degenerate-anchor CM/Lang unit
=> rank-621 admissible packet on C_7 x C_179
=> internal trace zero
=> right/product coboundary
=> 1092 H-coset verifier
=> fixed-frequency part of the sub-sqrt certificate.
```

The live hard part is the first line.  Everything after it is increasingly
formal.

## Fixed p24 Data

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

The class group is cyclic and squarefree.  That is good bookkeeping for the
`2,157,211,3107441` tower, but it does not select embedded child roots over
the ordinary split prime.  Treat cyclicity as indexing data, not a root
selector.

## How Much Has Been Tried

The theorem-level ledger currently records:

```text
live routes:                3
discarded/demoted routes:  20
total theorem routes:      23
```

The cheap falsifier harness is broader than the theorem ledger.  The latest
green sweep after the cyclotomic-divisor, scalar-search, residual-factor,
Kummer-descent, diamond-norm, and compressed-search-readiness gates was:

```text
task_count=264
passed=264
failed=0
```

Those 264 tasks are not 264 proof attempts.  They are mostly small exact gates,
boundary checks, and Lean/Python handoff tests.

The current archive scale is:

```text
files total:       1401
markdown notes:     582
python probes:      654
lean gates:         136
```

Do not reload the whole archive.

## Certificate Surfaces

There are three distinct scales.  Keep them separate.

### Four-Element Surface

Best conditional final payload:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

This is the desired constant-size certificate surface.  It still needs two
arithmetic producers:

```text
fixed orbit:      det(Psi_RS) is a p-unit
nonzero orbit:    Nrd_O(Phi_t) is a p-unit
```

Unit-2/diamond transport is in good formal shape after those producers.

### Fixed-Frequency H-Coset Surface

Current verifier interface:

```text
156 left rows * 7 right H-cosets = 1092 scalar equations
```

Compressed equivalent:

```text
48 independent equations = 42 mixed octic + 6 anchor
```

This is not a sample count.  It is a small finite verifier interface for a
selected weighted packet theorem.

### Selected-Chain Fallback

Finite payload:

```text
selected chain:      3107811 slots = 3.107811e-6 * sqrt(p)
full relative table: 3174011 slots = 3.174011e-6 * sqrt(p)
```

This beats sqrt for this p24 instance, but it does not yet solve the requested
asymptotic problem because it still needs an embedded selector or recovery
producer that avoids dense class-set enumeration.

## The Current Main Theorem

After `Tr_{B/C}`, the live packet is on:

```text
C_7 x C_179
```

The strongest finite target is membership in the rank-621 admissible C-axis
Jacobi-carry span.  For Fourier coefficients `F(a,b)` this is equivalent to
four families:

```text
1. F(a,0)=0 for a=1,...,6
2. F(a,b)+F(-a,-b)=0 for nontrivial right a and C/E conjugate pairs
3. F(0,b)+F(0,-b)=(-1/89)*F(0,0)
4. sum_{b>0}(F(-a,b)-F(a,b))=0 for a=1,2,3
```

Counts:

```text
ambient dimension = 7 * 179 = 1253
equations = 6 + 6*89 + 89 + 3 = 632
solution dimension = 621
```

Value-side equivalent.  If `g(r,c)` is the raw packet and
`f(r,c)=g(r,c)-g(r,0)`, it is enough to prove:

```text
g(r,0)+g(-r,0)=A_0
g(r,c)+g(-r,-c)=A_1 for c != 0
sum_c g(r,c)-179*g(r,0)=B independent of r
```

Multiplicatively, for `U(r,c)=omega^g(r,c)`:

```text
U(r,0)U(-r,0)=alpha_0
U(r,c)U(-r,-c)=alpha_1 for c != 0
prod_c U(r,c)/U(r,0)^179 = beta.
```

This is the most proof-friendly shape: constant pair-products plus a constant
selected row-product ratio.

## What Is Already Solid

Finite/formal stack:

```text
raw product identities
  => selected-defect value identities
  <=> four Fourier families on C_7 x C_179
  <=> rank-621 admissible C-axis Jacobi span
  => forbidden C-trivial bidegrees vanish
  => final internal trace zero
  => right coboundary / product coboundary handoff
  => 1092 H-coset verifier equations
```

The formal parts are not the bottleneck.  Lean and exact Python gates are good
at hardening these arrows after a producer theorem is stated.

What remains open is the arithmetic producer:

```text
construct the selected p-integral CM/Lang packet or unit whose specialization
has the product identities above.
```

The latest local-unit gate sharpens this:

```text
R_c(x)=Phi_c(x)/(x-1)^(c-1) is a unit iff x avoids mu_c
K_H(T) is a unit iff T avoids O and the nonzero subgroup H

p24 c = 179
forbidden cyclotomic anchor locus size = 179
```

So a conditional computation can immediately check a supplied producer, but
there is still no honest compressed p24 root search until that selected
p-integral coordinate/subgroup polynomial is constructed.

The new resultant-avoidance bridge gives the exact post-producer certificate
shape.  If the selected coordinate is represented in a finite algebra
`F_q[T]/(M(T))` by `X(T)`, then:

```text
R_c(X) is a unit
  iff X(T)^c - 1 is a unit modulo M(T)
  iff Res(M(T), X(T)^c - 1) != 0
  iff A(T)M(T)+B(T)(X(T)^c-1)=1 for some Bezout pair.
```

For p24 this means one resultant/Bezout p-unit against `X^179-1` can certify
the reduced-anchor local-unit condition once the selected CM/Lang coordinate
exists.  It still does not construct that coordinate.

## The Most Important Positive Clue

Literal finite-field Jacobi sums explain a large part of the target.

For small `N=7c` probes, right-mixed admissible Jacobi packets satisfy:

```text
off-C-zero pair-products work;
the selected row-product ratio is already constant on the six nonzero
  right rows;
only the right-zero anchor differs.
```

The exact finite-field anchor defect is:

```text
delta_c = (q - 2)^(-(c - 1))
```

because:

```text
J(1,1)=q-2
J(1,lambda)=-1 for lambda nontrivial
```

The single correction:

```text
U(0,0)=J(1,1)=q-2
U'(0,0)=U(0,0)/(q-2)=1
```

repairs both the C-zero pair-products and the selected row-product ratio in
the exhaustive `c=5,11,13` right-mixed checks.  The symbolic
Hasse-Davenport gate then covers `c=5,11,13,17,19` and p24 `c=179` without
finite-field summation, including all `189036` p24 right-mixed admissible
pairs.

The newest scalar search exhaustively replaces `U(0,0)` by every value-field
scalar in the `c=5,11,13` models.  The only scalars that work for every
right-mixed admissible pair are:

```text
x = +1, -1.
```

Thus the scalar ambiguity around the degenerate anchor is only a sign.  The
`+1` branch is the reduced `Jdagger(1,1)=1` packet used by the
cyclotomic-divisor residual; the `-1` branch is a sign normalization, not a
new divisor shape.

The residual-factor search then tests whether the row-sum slice and the
`R_c` residual can be realized as separate base-field multiplicative factors.
For both valid signs this would require a `c`-th root of the selected anchor
scalar.  In the `c=5,11,13` Jacobi value fields, no such root exists for
either sign.  Therefore:

```text
do not search for independent base-field h_triv and h_nontriv factors;
use divisor/norm language or an auxiliary extension whose norm descends.
```

The positive Kummer-descent gate then supplies the exact auxiliary shape.
Adjoin `beta` with `beta^c=s`, where `s` is the selected anchor correction
scalar after the final sign choice.  The row-sum slice and the `R_c` residual
split over that auxiliary extension, their product descends to the base
selected correction, and the selected correction forces:

```text
R_c exponent e = 1.
```

For p24, the live theorem is now:

```text
construct a p-integral auxiliary Kummer/norm/divisor realization of
R_179 = Phi_179(X)/(X-1)^178,
with exponent e=1 and final +/- sign normalization.
```

So the new picture is:

```text
nonzero right rows: punctured Hasse-Davenport algebra
right-zero row:     one selected degenerate-anchor correction
```

The missing p24 object is the selected trace-GCD/CM-Lang analogue of this
degenerate anchor after `Tr_{B/C}`.

## The Anchor Split That Composes Old Work

The selected-defect footprint of the single raw anchor correction is the
punctured right-zero row:

```text
h(r,k)=1  if r=0 and k != 0
h(r,k)=0  otherwise
```

For p24 this row has `178` nonzero spatial entries and Fourier profile:

```text
H(a,0)=178
H(a,b)=-1 for b != 0
```

The old adjacent-anchor/covariance route sees only the `C/E`-trivial row-sum
slice:

```text
h_triv = ((c-1)/c) * e_0 * sum_k e_k
row-sum slice on C_7 = (c-1)e_0
```

This accounts for the six nonfixed right `b=0` channels.  It does not account
for the rest of the anchor.

The residual is:

```text
h_nontriv = h - h_triv
H_nontriv(a,0)=0
H_nontriv(a,b)=-1 for b != 0
```

For p24 it has:

```text
7 * (179 - 1) = 1246
```

nonzero `C/E`-nontrivial Fourier channels.

This is a major synthesis point:

```text
old adjacent-anchor descent = cancellation of the b=0 slice;
new CM/Lang unit theorem = realization of the full punctured row,
including the 1246-channel C/E-nontrivial residual.
```

## Fresh-Eyes Observation Now Gated

The residual is not amorphous.  Multiplying by `c` gives an integral
degree-zero divisor on the `C_c` coordinate:

```text
c * h_nontriv = sum_{k != 0} [zeta_c^k] - (c - 1)[1].
```

For prime `c`, this is exactly the divisor of the rational cyclotomic unit:

```text
R_c(X) = Phi_c(X) / (X - 1)^(c - 1).
```

Equivalently:

```text
div(R_c) = sum_{k != 0} [zeta_c^k] - (c - 1)[1].
```

For p24, `c=179`, so the candidate residual unit is:

```text
R_179(X) = Phi_179(X) / (X - 1)^178.
```

This does not prove the certificate.  It gives a concrete target for the
remaining anchor theorem:

```text
show that the selected trace-GCD/CM-Lang degenerate anchor specializes to the
appropriate p-integral analogue of R_179, with the b=0 row-sum slice and the
C/E-nontrivial residual matched to the raw punctured Hasse-Davenport packet.
```

This formal divisor identity is now gated in:

```text
p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.py
p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.md
p24/lean/TraceGcdReducedAnchorCyclotomicDivisorGate.lean
```

The gate passes for `c=5,11,13,17,19,179`, including the p24 marker:

```text
p24_residual_integral_fourier_channels=1246
```

The next step is no longer to test the formal divisor bookkeeping.  It is to
connect this principal divisor to a p-integral selected CM/Lang unit
specialization.

## What The Failed Routes Teach

The failures are coherent.  They mostly say:

```text
generic structure is too weak;
the selected weighted trace-GCD packet must be used.
```

### Class-Field Tower Selector

Result: demoted.

Cyclicity gives unique subgroup layers, but embedded child roots above the
split prime are torsors.  The odd layers need non-genus phase data.  This is
bookkeeping, not a selector.

Latest boundary: widening the abstract tower fiber-map scan on the
`D=-671` and `D=-815` controls found no degree `1` or `2` rational maps and
no degree `1`, `2`, or `3` polynomial maps pairing the abstract child roots
in either orientation; random controls for the rational part were also
`0/30`.  So the selected-chain route remains a verifier surface, not a
producer, until a genuine embedded phase theorem is supplied.

### Generic CM Covariance

Result: discarded as producer.

Covariance gives eigenspaces, not zero.  In several gates, after descent it
becomes circular because the desired vanishing is exactly what would make the
descended covariance nontrivial.

Useful remnant:

```text
covariance + telescope + one descended anchor => seven H-coset sums zero.
```

The anchor is the arithmetic theorem.

### Hilbert-90

Result: formal handoff, not discovery.

After internal trace zero, Hilbert-90 gives the potential.  Trying to invert
Hilbert-90 before proving trace zero is circular.

### Plain Stickelberger Or Generic Jacobi Carry

Result: discarded/demoted.

Plain Stickelberger leaks forbidden bidegrees.  Broad C-axis Jacobi carries
have rank `625` and include four leaky directions.  The viable family is the
rank-`621` admissible C-axis subfamily, or a rank-625 theorem plus an explicit
four-leak cancellation.

### Anchor-Only Or Trace-Only Compression

Result: discarded.

Anchor zero can hold while forbidden `C/E`-trivial bidegrees leak.
`C/E`-centering can hold while the selected-child anchor fails.  The section
choice matters.

### Actual-CM Generic Rows

Result: negative controls.

Known failures:

```text
D=-4751:   0/91 full mixed/anchor/recombined-balance shifts
D=-5000:   0/60 raw packets with zero trivial C projection
D=-6719:   covariance and telescope hold, anchor descent fails
D=-13319:  right-combo/product internal traces and anchors fail;
           no universal degree-<5 base/value-field relative-coordinate
           multiplier repairs the anchor across all 140 sections
D=-13319 selected defects:
             140/140 force C-zero fiber
               0/140 satisfy full identities
```

Do not propose a theorem of the form "all embedded CM packets have this
identity" unless it directly explains why these controls are outside the
selected p24 packet.

### Post-Fit Linear Algebra

Result: rejected as producer evidence.

Interpolation, post-fit displacement operators, and arbitrary splitting-field
sections can manufacture finite identities after seeing data.  Any acceptable
operator or section must be intrinsic, Frobenius-compatible, and attached to
the CM/Lang construction.

### CS, ML, Probability, Matrix-Tree Ideas

Result: mostly orientation tools, not producers.

They are useful for suggesting rank condensers, minors, or search heuristics.
They have not produced a p-unit or exact CM/Lang identity.  The
Strong-Rayleigh and matrix-tree shortcuts do not survive the CRT-axis
coefficient structure as standalone proofs.

## What Old Facts Now Compose

### Composition 1: Jacobi Sums Plus Anchor Correction

Literal Jacobi sums give:

```text
punctured nonzero-row product identities
```

The single degenerate anchor gives:

```text
right-zero correction
```

Together they are the cleanest route to the rank-621 packet theorem.

### Composition 2: Adjacent Anchor As Row-Sum Slice

The older right-difference/covariance branch is not separate.  It asks for
the `b=0` row-sum slice of the same reduced anchor.  This explains why it
kept getting close but did not see the full `C/E`-nontrivial residual.

The newest adjacent-anchor gate compresses this branch further.  If the
single adjacent anchor has rho-orbit polynomial
`A(y)=a_0+...+a_6y^6`, then:

```text
rho(T_0)=T_0
  iff a_0=...=a_6
  iff A(y) == 0 mod Phi_7(y).
```

So the six anchor projectors are one cyclic divisibility condition.  With
pointwise covariance and telescoping, proving this selected `Phi_7`
divisibility gives the `48` compressed right-difference equations.

### Composition 3: Cyclotomic Divisor As Residual Candidate

The full residual after removing the row-sum slice is the divisor of
`Phi_c(X)/(X-1)^(c-1)` after multiplying by `c`.  This may be the missing
bridge between:

```text
finite-field J(1,1)/(q-2) normalization
and
CM/Lang/Siegel/Ramachandra unit distribution relations.
```

Fresh boundary: the bridge is only residual-side.  Rechecking the old
ray-kernel obstruction with the new `R_179` language shows that classical
Siegel/Ramachandra/Robert distribution relations still collapse
ray-congruence kernels, not the p24 conductor-one unramified `157/211`
Hilbert-class phases.  The refreshed audit again gives no `157` or `211`
local unit factor at the squarefree levels `157*211`, `2*157*211`,
`223*463`, or `2*223*463`.

So this composition can certify the chosen residual unit after a selected
auxiliary fiber exists; it cannot itself choose the embedded fiber.

### Composition 4: Product-Coboundary After Trace Zero

The right potential should not be found first.  Prove the selected internal
trace zero/product formula, then invoke the already-built Hilbert-90 and
product-coboundary handoff.

### Composition 5: Fixed-Frequency Back To Four Elements

If the fixed-frequency theorem proves the no-fixed-defect determinant
identity, reattach it to the two-resultant surface:

```text
fixed determinant p-unit
+ one nonzero crossed norm p-unit
+ unit-2 transport
=> four field elements.
```

### Composition 6: Centered Fitting P-Unit Route

The centered profile gives a parallel determinant-line p-unit target:

```text
Delta_C(t) = det(W_C -> H/B_t),
Pi_O = prod_{t in right Frobenius orbit O} Delta_C(t).
```

Lean checks the finite implication from orbit/full-origin p-unitness to the
centered arc product.  The actual-CM orbit-Fitting audit verifies the
direct-sum and signed block-cycle determinant plumbing on the pinned
`D=-13319` row with zero mismatches and correct singular controls.  But the
phase-divisor holdout has `nonrandom_span_hits=0` and rejects
coordinatewise/Kummer-only payloads.  So this route is live only as a
phase-aware Schubert/Fitting determinant section with a local p-unit theorem;
bounded elementary phase-unit products are demoted.

The newest local-intersection pass sharpens that message.  Simple
class-polynomial roots at the split prime and random transversality estimates
do not imply the Schubert determinant is a p-unit.  An exterior toy cancels a
translated determinant even with all fixed coefficients and Plucker
coordinates nonzero.  The actual-CM norm triangle still identifies the
honest object as the crossed-product/Fitting orbit norm, not a base-field
polynomial.  Phase-coordinate descent helps in the pinned row, but p24 has
full exterior right support by subset size `3`, so seven orbit norms remain
the robust payload surface.

The determinant representatives are now unified enough to avoid another
branch explosion.  The residual Moore/Chow toy shows that residual products
equal Moore determinants and split into a prefix Moore section times the Moore
section of prefix-annihilator tail images.  The Schur-complement toy shows the
same event after choosing a p-unit prefix pivot.  The actual-CM
trace-pairing/subspace audit has `rows=10`, `trace_rank_mismatches=0`, and
`nonzero_event_mismatches=0`; its conclusion is that trace-pairing
nonvanishing and residual-norm-product nonvanishing detect the same p-unit.
So the live theorem can be phrased as trace-gcd, Moore residual, Chow/Fitting,
or Schur-complement p-unitness.  These are representatives of one target, not
four new routes.

The most concrete fixed-orbit proof split is now:

```text
Prefix: rank 140 for the right-normal-basis coefficients
  Tr_{E/L}(eta_i * H_{157,211}(1,v_j)),
  with eta_i the type-6 Gaussian normal basis of F_p(mu_211)/F_p.

Tail: after a named p-unit prefix pivot, rank 16 for the RS-tail
  Schur-complement columns modulo the prefix span.
```

The supporting checks are all existing artifacts: normal-basis reconstruction,
p24 Gaussian-period bookkeeping (`ord_211(p)=35`, type `6`, coset cover
`210`), Lean prefix-erasure/Schur gates, actual-CM Gaussian/RS-tail rank
audits, and a widened metric-aware orbitwise Schur falsifier with `20` rows
and no Schur/Gram/right-class failures.  The same audits include singular
controls, so this is not a formal dimension argument; it is a sharper
arithmetic theorem statement.

For the prefix half, the most useful restatement is now semilinear:

```text
M_0 : K^{35*4} -> L,       K=F_p(mu_35), L=F_p(mu_157)
T(x)_{b,j}=x_{p^{-1}b,j}^p,  T^4=1.

prefix p-unit <=> core_T(ker M_0)=0
               <=> no fixed relation F_p^28 + K^28 -> L
               <=> fixed-adjoint syndrome L -> F_p^28 + K^28 is onto
               <=> 140-coordinate Moore residual is nonzero.
```

This is the best place to import rank-metric/subspace-evasive ideas: the
first component kernel is necessarily large, but it must contain no nonzero
orbit under the order-4 semilinear motion.  That theorem is still arithmetic,
because `M_0` is the actual CM Gaussian frequency table.

The full fixed-orbit theorem then adds one tail resultant:

```text
Norm(Delta_140(C_prefix)) is a p-unit
  => residual kernel has dimension 16;

Norm(Delta_16(P_prefix(T_tail))) is a p-unit
  => RS tail is injective on that kernel;

both together <=> fixed representative determinant is a p-unit.
```

This is the current cleanest fixed-orbit certificate surface.  The remaining
work is to prove these named Moore/linearized-resultant p-units arithmetically
for the actual p24 CM/Lang table, then pair the fixed-orbit p-unit with the
nonzero-orbit crossed norm.

## Best Next Proof Program

The next proof attempt should not branch randomly.  It should try to prove the
following concrete theorem, or falsify it cleanly in a faithful small model:

```text
There is a p-integral selected CM/Lang multiplicative packet U(r,c) after
Tr_{B/C} whose divisor/product formula is the punctured Hasse-Davenport
identity on nonzero right rows, and whose degenerate right-zero anchor is the
CM/Lang analogue of R_179(X)=Phi_179(X)/(X-1)^178.
```

Expected consequence:

```text
the additive selected defect lies in the rank-621 admissible C-axis Jacobi
span on C_7 x C_179.
```

The proof must account for:

```text
1. p-integrality at the selected prime above p;
2. the b=0 row-sum slice seen by adjacent-anchor descent;
3. the 1246-channel C/E-nontrivial residual;
4. cancellation of the raw punctured Hasse-Davenport leak;
5. compatibility with the selected child/section, not just quotient traces.
```

## Best Next Computation

Compute should be a theorem microscope.

High-value tests:

```text
1. Gate the formal divisor identity
   c*h_nontriv = div(Phi_c(X)/(X-1)^(c-1))
   for small c and c=179.

2. In small faithful selected-weight analogues, report the four Fourier
   families separately instead of one pass/fail bit.

3. Report the reduced-anchor residual split:
   b=0 row-sum slice versus C/E-nontrivial residual.

4. Test whether candidate CM/Lang unit divisors specialize to the cyclotomic
   residual shape before testing expensive p24 data.

5. Once a theorem statement is explicit, add Lean gates for the finite
   implications and count checks.

6. Keep the finite selector lower bound in view: bounded-level invariants are
   ruled out, but a third-trace recovery object of degree `3107441` is still
   below `sqrt(p)`.  This is the allowed positive scale for an embedded
   class-field recovery theorem.

7. Do not confuse that degree bound with a computable polynomial.  The
   relative-coset toy shows one coset polynomial is enough only after the
   quotient phase is selected; symmetrizing over all phases returns the full
   class polynomial.  The p24 height audit makes ordinary complex/CRT
   computation too large even with aggressive constant-factor class
   invariant height savings.

8. On the centered p-unit branch, test determinant-line statements rather
   than entrywise unit payloads.  The existing holdout shows coordinatewise
   nonzero/Kummer data can miss determinant zero; the Fitting determinant is
   the object that must be proved p-unit.
```

Low-value tests:

```text
full p24 class-set enumeration;
generic actual-CM rows without selected trace-GCD weighting;
support-only checks;
post-fit operators;
large jobs that output only pass/fail.
```

## Lean Use

Lean should be used heavily for finite scaffolding:

```text
product identities => value identities;
value identities => Fourier families;
Fourier families => admissible span;
admissible span => forbidden bidegree zero;
forbidden bidegree zero => internal trace zero;
internal trace zero => right/product coboundary;
centering + six characters => 1092 verifier;
payload/count inequalities.
```

Lean should not be expected to discover the CM/Lang unit.  Use it once the
objects and theorem statement are explicit.

## Minimal Read Queue For A Fresh Agent

Start here:

```text
1. p24/00_HANDOFF_INDEX_20260607.md
2. p24/00_FRESH_EYES_SYNTHESIS_20260607.md
```

Then, if proving the live theorem:

```text
3. p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
4. p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_decomposition_theorem.md
5. p24/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md
6. p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.md
7. p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.md
8. p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.md
9. p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.md
10. p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.md
11. p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search.md
12. p24/trace_gcd_fixed_frequency_jacobi_anchor_residual_factor_search.md
13. p24/trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate.md
14. p24/00_THEOREM_ATTEMPTS_LEDGER.md
```

Open `00_ROUTE_MAP.md` only to find narrow route files after choosing a
specific route.  Avoid reading the whole `p24/` archive.

## Honest Confidence

Closer:

```text
the verifier is small;
the finite chain is strong;
the current theorem is much narrower than the original search;
the Jacobi/Hasse-Davenport anchor defect is a real structural clue;
the reduced anchor now splits cleanly into old and new obstructions.
```

Still uncertain:

```text
no p24 CM/Lang unit producer has been proved;
generic CM controls are strongly negative;
the selected section and p-integrality are still the dangerous parts.
```

Latest finite sharpening:

```text
ordinary cyclic C/E translation norm of [zeta_179]-[1] telescopes to 1;
diamond/unit norm over (Z/179Z)^* gives R_179;
therefore the producer must expose diamond/unit action or an equivalent
finite-field identity, not the cyclic trace norm.
```

Elliptic-unit correction:

```text
[P]-[O] is not principal on an elliptic curve for nonzero torsion P;
the whole subgroup divisor sum_{Q in H, Q != O}[Q]-(178)[O] is principal
for c=179 because the nonzero subgroup sum is zero;
so the live producer target is the direct subgroup/diamond divisor or a
descended cyclotomic coordinate, not an individual elliptic one-point factor.
```

Concrete producer primitive:

```text
K_H(x)=prod_{Q in (H\{O})/{+-1}}(x-x(Q)) has exactly that subgroup divisor;
for c=179, deg K_H=89 and pole order=178;
K_H^2 is the Vélu x-denominator shape, but K_H itself is the R_179 residual;
for p24 this is auxiliary CM/Lang/cyclotomic data, not a final-curve
F_p-rational 179-isogeny, since 179 does not divide #E(F_p) and
t^2-4p is nonsquare mod 179.
```

New p24-specific sharpening:

```text
p mod 179 = 77
ord_179(p)=89=(179-1)/2
-1 notin <p> mod 179
```

Therefore the `178` nonzero diamond exponents split over `F_p` into two
Frobenius half-orbits of size `89`, and each half-orbit chooses exactly one
representative from every `{a,-a}` pair.  The reduced-anchor target can be
phrased as a selected Frobenius half-product, or equivalently as the
inversion-quotient kernel polynomial `K_H`, plus its reciprocal/sign
normalization.  This is a real reduction of the theorem surface; it is not an
extra producer.  The remaining theorem is still to construct the selected
p-integral CM/Lang half-product or kernel polynomial without enumerating the
class set.

Ephemeral Lean check: `q=77`, `q^89=1 mod 179`, the `89` Frobenius powers
are distinct, and the orbit contains exactly one member from each `{a,-a}`
pair.

Cyclotomic local interpretation: `p` has residue degree `89` and two primes
in `Q(zeta_179)`, but it is inert of degree `89` in the real/inversion
quotient because `<p,-1>=(Z/179Z)^*`.  Thus the two signs/half-products are
local orientations in the full cyclotomic layer; the degree-`89`
kernel-polynomial quotient is the canonical inversion-invariant object.

Real-cyclotomic resultant form: with
`S_0=2`, `S_1=Y`, `S_{k+1}=Y*S_k-S_{k-1}`,

```text
Psi_179(Y)=1+sum_{k=1}^{89}S_k(Y),
Phi_179(X)=X^89 Psi_179(X+X^{-1}).
```

A local finite-field check over the actual `F_p` gave:

```text
deg Psi_179 = 89
gcd(Psi_179, Y^p-Y)=1
Y^(p^89)=Y mod Psi_179
Psi_179 irreducible over F_p
```

Thus a selected inversion coordinate `Y` can certify the nontrivial forbidden
roots by the degree-`89` resultant `Res(M, Psi_179(Y))` rather than the
oriented primitive-root part of the degree-`179` test against `X^179-1`.
The basepoint/denominator check remains separate: `Psi_179(2)=179`, so the
real-cyclotomic polynomial does not detect `X=1` or the elliptic `O` pole.

Finite-field Kummer update: in the actual p24 reduction fields, the
`179`th-power map is bijective.  The named degrees

```text
1, 4, 156, 5460, 5460*179, 5460*5549, 31, 179
```

are all nonzero modulo `89=ord_179(p)`, so no named field contains `mu_179`
and `gcd(179,p^d-1)=1` in each case.  Therefore the anchor row-sum /
`R_179` residual split can be done after reduction by a unique `179`th-root
exponent.  This helps finite testing and certificate compression, but it does
not supply the missing p-integral selected CM/Lang producer.

Consequence for the local-unit target: if the selected coordinate is in one
of those named p24 reduction fields, then `X^179=1` already implies `X=1`.
So the nontrivial forbidden-root part of `R_179(X)` is automatic; only the
basepoint/denominator condition remains.  The degree-`89` `Psi_179`
resultant is needed only for a producer formulated in an auxiliary
real-cyclotomic algebra, not for a coordinate already descended to the named
class-field side.

Conditional final collapse of the basepoint check: the reduced Jacobi packet
has corrected anchor value `x=+/-1`; the Kummer descent scalar for the
row-sum/residual split is `s=(q-2)/x`.  After reduction in characteristic
`p`, this is `s=±2`.  Since `±2 != 1 mod p`, a named-field solution of
`beta^179=s` cannot have `beta=1`.  Explicitly in `F_p`, the unique roots of
`-2` and `2` are non-`1`.  Therefore the local-unit side is fully discharged
once the actual CM/Lang producer proves:

```text
corrected anchor value x = +/-1;
Kummer scalar s = (q-2)/x, the Jacobi q-2 analogue up to sign;
selected coordinate lies in a named p24 reduction field.
```

The producer theorem remains the bottleneck; the local forbidden-locus
avoidance would no longer be.

Operational search posture:

```text
residual product size: 178 diamond terms;
F_p Frobenius half-products: 2 of degree 89;
real-cyclotomic forbidden polynomial: one irreducible degree 89 Psi_179
  if using an auxiliary inversion algebra;
named-field reduction: nontrivial mu_179 avoidance automatic, only X!=1/O;
Jacobi scalar ±2 branch: basepoint X=1 also automatic once scalar is identified;
kernel-polynomial generator choices after fixing selected subgroup: 1;
conditional verifier surface: 2 signs * forced e=1 * 1 kernel polynomial,
then 48/1092 finite equations;
but selected-section/fiber pairing is still missing; trace/sum alone leaves
~10^69 random-scale first-layer candidates at p24;
executable producer candidates currently available: 0;
generic Pomerance smoke: 1000000 p24 trials in 7.67s, no hit, lottery only.
```

Low-moment selector window:

```text
p24 entropy says 4 first-layer moments plus 26 second-layer moments would
randomly isolate the selected fibers;
actual-CM selector sweep supports the finite collision behavior:
  default rows 19/19 unique within degree bound, 14/19 at degree 1;
  wider rows 65/65 unique within degree 6, 43/65 at degree 1;
  end-of-day widened rows 218/218 unique within degree 6,
    131/218 at degree 1, 173/218 no later than random entropy;
  additional end-of-day control rows 103/103 unique within degree 7,
    65/103 at degree 1, 82/103 no later than random entropy;
the exact dictionary is sparse signed moment-curve relations after canceling
overlap; Newton already forbids reduced collision size <= k, so p24 only
needs to rule out sizes 5..157 in layer one and 27..211 in layer two;
union entropy still has slack:
  first layer over two parents: log10 expected collisions = -2.522422;
  second layer over 314 parents: log10 expected collisions = -4.721562;
construction target is now sharper too: child power sums are relative traces
Tr(Y^d) of quotient-period powers; p24 has 30 nominal selected relative
traces, but the two P1 values are automatic parent periods, so the genuinely
new higher-moment target is 28 selected values; P1 still remains part of the
30 selector constraints because higher-only entropy is not enough at p24
scale; if kept as parent-field moment functions the surface remains 8172
coefficients; equivalently, by Newton identities the producer may target
28 new truncated child-polynomial coefficients:
  first layer e2..e4 = 3,
  second layer e2..e26 = 25;
this is now the most useful CPU-heavy theorem microscope, but it still needs
an intrinsic relative-trace producer and a CM anti-collision theorem.
```

Selected-prime packet controls, widened on 2026-06-07:

```text
relative/resultant packets:
  23906 packet rows, 1248 unique rows ignoring origin;
  coord_zero=0, distinguished_zero=0, content_zero=0.

additional end-of-day relative/resultant control:
  12211 packet rows, 755 unique rows ignoring origin;
  coord_zero=0, distinguished_zero=0, content_zero=0.

packetized content/energy/Hermitian sufficient certificates:
  same 23906 packet rows;
  coord_zero=0, content_failures=0, energy_zero=0, hermitian_zero=0.

packet-factor vanishing shape:
  zero_hits=0.

upstream DANGER3 pp24 small-prime control:
  pp24.txt.gz ends at p=16777213 and contains no p=10^24+7 candidate;
  direct point-count recovery for p<30000 gives rows=3243, misses=0,
  trace-bucket ranks={0:328, 1:2371, 2:544}; in the exact p24 mod-64
  residue bucket, n=104 with ranks={0:13, 1:83, 2:8}.  Simple residue scans
  mod m<=128 only show small-sample enrichments, not a robust lower-bucket
  filter.
```

This supports the product/resultant producer target as a theorem microscope.
The upstream small-prime data is useful control evidence, but it did not
produce the p24 CM/Lang input or a reliable direct-search shortcut.

Abstract quotient coordinate stress test:

```text
p24/abstract_embedded_pairing_low_bidegree_scan.md

Question:
  do abstract unramified quotient roots pair with embedded period quotient
  roots by a low-bidegree relation F(X,Y)=0?

Result:
  D=-2239, q=2243, quotient n=7:
    support 6 bidegree (2,1)/(1,2): 0/5040 matchings in both orientations
    support 9 bidegree (2,2): 5040/5040 matchings, same as random controls

Summary:
  low_support_rows=8
  actual_low_support_rows_with_pairing=0

Meaning:
  plain abstract quotient coordinates still do not supply the embedded
  non-genus phase.  A successful producer must construct relative fibers /
  class-character traces directly, or bypass them with the p-unit/divisor
  identity.
```

The right posture is:

```text
not blocked;
not close enough to claim success;
now concentrated on one explicit product/divisor theorem.
```
