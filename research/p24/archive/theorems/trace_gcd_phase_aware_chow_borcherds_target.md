# Phase-Aware Trace-GCD Chow/Borcherds Target

Date: 2026-06-06

This note consolidates the current theorem target after:

```text
p24/trace_gcd_chow_norm_theorem_candidate.md
p24/trace_gcd_chow_integral_model.md
p24/trace_gcd_chow_plain_divisor_boundary.md
p24/trace_gcd_chow_tensor_bridge_boundary.md
```

The plain-`j` and one-edge divisor shortcuts are negative in the small
actual-CM diagnostic.  The tensor-factor route is adjacent but does not force
the selected Chow minor without a new determinant-line comparison.  The
remaining compact route is therefore a phase-aware Schubert-Fitting/Borcherds
theorem.

The positive phase-coordinate diagnostic is:

```text
p24/trace_gcd_chow_phase_coordinate_scan.py
p24/trace_gcd_chow_phase_coordinate_boundary.md
```

In the pinned small actual-CM row, the determinant descends exactly to the
right phase coordinate and has one nonzero Frobenius orbit of DFT support.
For p24, however, the exterior support is full by subset size `3`; a
one-orbit spectral collapse would require a new arithmetic cancellation
theorem.  Therefore the safe target remains seven orbit Chow norms, not a
single hidden Gauss-period norm.

## Theorem Target

For the conductor-2 p24 CM phase torsor, retaining the non-genus `157/211`
relative phase data, define for each right Frobenius orbit
`O subset Z/211Z`:

```text
s_O = Nrd_O(det(P V_univ A))
    = prod_{t in O} Chow_{V_t^{-1}C}(W_trace)
    = unit * Pi_O.
```

Here `Nrd_O` is the crossed-product/right-orbit reduced norm, `W_trace` is
the p-integral trace-GCD 16-plane, and `C=ker(P)` is the selected tail
19-plane.

The theorem to prove is:

```text
For every one of the seven right Frobenius orbits O,
there is an explicit p-integral phase-aware class-field/Borcherds/Fitting
product Psi_O such that

  s_O = p-unit * Psi_O

near the selected p24 CM point, and

  div(Psi_O) =
    pulled-back orbit Chow divisor D_O
    + boundary/vertical terms with no support at the selected prime over p.

Moreover

  v_p(Psi_O(x_p24)) = 0.

Therefore

  v_p(Pi_O) = 0

for all seven orbit Chow norms.
```

This would instantiate the 14-element orbit-product payload in

```text
p24/trace_gcd_subsqrt_certificate_manifest.md
p24/lean/TraceGcdChowNormGate.lean
p24/lean/TraceGcdChowBorcherdsPUnitGate.lean
```

and would beat `sqrt(p)` by construction.

The new Lean gate formalizes the final finite handoff:

```text
zero local intersection for Psi_O
+ p-unit comparison Psi_O -> s_O
+ Chow norm zero-detection
=> no translated Schubert bad event
=> selected trace-GCD row is good.
```

It now also covers the global full-divisor variant:

```text
p24/trace_gcd_global_chow_borcherds_handoff.md
```

A Borcherds product may naturally construct

```text
Psi_all ~ prod_{t mod 211} Chow_t(W,C)
```

rather than seven separate `Psi_O`.  If `Psi_all` is honestly compared to the
actual full Chow norm and is a p-unit, the finite payload shrinks to two
base-field elements while still excluding every translated Schubert zero.

## Lemma Stack

1. Integral Fitting norm.

```text
det(P V_univ A)
```

lives in the p-integral crossed-product/right-orbit order, and its reduced
orbit norm equals `Pi_O` up to a p-unit.

2. Chow equals Fitting divisor.

The zero locus of `det(P V_t A)` is exactly

```text
W_trace cap V_t^{-1}C != {0}
```

with the expected divisor multiplicity, so the orbit norm cuts out the
orbit Chow divisor `D_O`.

3. Phase descent.

The determinant section descends only after retaining the embedded `157/211`
relative phase data.  Plain `j`, one-edge coordinates, and ordinary
base-field residues are not honest enough.

4. Borcherds/class-field realization.

The pulled-back orbit Chow divisor is the divisor of an explicit
phase-aware Borcherds/Siegel/class-field product, possibly after boundary
correction away from the selected p24 prime.

5. p24 local valuation.

The CM value formula for that product has zero selected p-local contribution:

```text
v_p(Psi_O(x_p24)) = 0.
```

This is the actual p-unit theorem.

The local p24 data needed for this step is now explicit:

```text
p24/trace_gcd_p24_local_invariants.py
p24/trace_gcd_p24_local_intersection_invariants.md
```

It records the split ordinary prime above `p`, the two square-root
orientations `sqrt(D_K)=+/-t/2 mod p`, and the fact that the `157`/`211`
certificate levels are p-units.  Therefore the valuation theorem should be
phrased as a genuine zero local-intersection statement for the pulled-back
Chow divisor at one of these two ordinary embeddings.

The same p-local criterion is now stated directly for the block-cycle/Fitting
determinant line in:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

The residual-product route now gives a more explicit representative of the
same determinant-line section:

```text
p24/trace_gcd_residual_moore_chow_section.md
```

It writes the selected fixed scalar as the product of a 140-coordinate
Moore-Wronskian for the prefix and a 16-coordinate Moore-Wronskian of the
tail after applying the prefix annihilator `P_U`.  Thus the phase-aware
product `Psi_O` may equivalently be sought as a Borcherds/Fitting realization
of these Moore-Schubert sections.  The quotient-tail warning is important:
the tail section is not the Moore determinant of the raw tail coordinates.

## Most Likely Obstruction

The hard point is the fourth lemma.  The Chow divisor could remain a generic
high-degree Schubert divisor even on the phase torsor.  If so, there may be
no Borcherds/Siegel product with this exact divisor, and the proof must fall
back to a direct Fitting/noncancellation identity.

The next small-data falsifier should keep the full phase coordinates and ask
whether the orbit Chow norm divisor lies in a plausible span of
phase-aware Siegel/Borcherds/class-field divisors.  A random-sized component
outside that span would falsify the automorphic-divisor shortcut without
touching p24-scale computation.

The phase-coordinate scan refines this: first test whether the candidate
divisor is genuinely a right-phase object; then test whether its support is
small enough to be a known one-orbit class-field product.  The pinned row
passes both, while the p24 exterior support says the second pass needs new
CM cancellation.

The first bounded unit-product dictionary test is:

```text
p24/trace_gcd_chow_phase_divisor_span_scan.py
p24/trace_gcd_chow_phase_divisor_span_boundary.md
```

It tests right-binomial cyclotomic units and small Heegner-fiber units after
passing to discrete logs.  In the pinned row the odd log components become
full-rank, so containment is random, while the only non-full-rank component
mod `2` misses both Chow targets.  Thus the simplest phase-aware unit-product
explanation is demoted; a Borcherds/Fitting proof needs a more specific
divisor construction.

The first global-product scalar miner is:

```text
p24/trace_gcd_global_product_miner.py
p24/trace_gcd_global_product_mining_boundary.md
```

It found low-weight formulas for the one scalar `Pi_all` in the pinned small
row, but no low-weight formulas for the actual right-phase vector.  This
does not rule out `Psi_all`; it says the theorem must prove an honest
divisor/local-intersection comparison, not merely a scalar identity in
`F_q^*`.

The expanded special-divisor criterion and larger bounded unit-span rerun are
recorded in:

```text
p24/trace_gcd_chow_special_divisor_frontier.md
```

The result is still negative for the easy dictionary: small cyclotomic
right-binomial units plus small Heegner-fiber units do not recognize the
actual Chow phase vector before spanning the whole ambient vector space.

## Current Assessment

This target is closer to the finite certificate than the tensor/axis route:
it names exactly the seven orbit norms consumed by the Lean gate.  But it
has a single serious missing bridge, namely construction of the phase-aware
automorphic/Fitting divisor.

The tensor route may still be more constructive if this bridge fails, but it
currently needs its own determinant-line comparison before it proves the
selected Chow payload.
