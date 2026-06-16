# Trace-Frame Borcherds P-Unit Boundary

Date: 2026-06-05

This note states the exact product-formula route that could prove the current
trace-frame p-unit theorem, and separates it from the divisor shortcuts that
have already failed.

## Candidate Theorem

Let:

```text
Xi_lead in K_m Q(zeta_n)^<p>
```

be the determinant-line element whose eight residues are the leading
trace-frame Plucker determinants, up to p-units.  A Borcherds/Schofer style
proof would need to construct a phase-aware product:

```text
Psi_lead
```

such that:

```text
Psi_lead(CM(O)) = Xi_lead * U
```

where `U` is a p-unit at every prime above:

```text
p = 10^24 + 7.
```

It would also need a local-intersection formula proving:

```text
ord_P(Psi_lead(CM(O))) = 0
```

at the selected ordinary split primes above `p`.  Then:

```text
Xi_lead is a p-unit
```

and the already-gated trace-frame norm certificate follows.

The finite implication is abstracted in:

```text
p24/lean/TraceFrameBorcherdsPUnitGate.lean
```

## What The Product Must Remember

The product/divisor cannot be genus-level, full-class-level, or plain
selected-`j` level.  It must retain the order-`3107441` non-genus phase
inside the trace-frame determinant-line norm.

Equivalent targets are:

```text
delta_all in A_all^*
R_lead,Omega is a p-unit for every beta orbit Omega
the selected 368 x 368 CM translate minor is a p-unit
the CM-weighted Fourier Schubert minor is a p-unit
```

Thus the Borcherds input would have to produce the selected Schubert
determinant-line value, not merely a symmetric norm of singular moduli.

## Why The Easy Divisor Route Is Closed

The following diagnostics already rule out the obvious recognition strategy:

```text
p24/trace_frame_lead_divisor_support_boundary.md
  The leading determinant norm is not a low-degree plain-j divisor with small
  Heegner support in moving trace-frame rows.

p24/trace_frame_lead_phase_shape_boundary.md
  It is not a bounded low-bidegree function of one oriented edge.

p24/trace_frame_lead_phase_recurrence_boundary.md
  The moving trace-frame determinant norm has period 13 but maximal
  Berlekamp-Massey order 13, matching period-preserving random controls.
  Thus the only visible recurrence is tautological periodicity.

p24/trace_frame_orbit_zero_lemma_degree_boundary.md
  A single crossed-product orbit gives only |Omega| zeros.  In the moving
  trace-frame toy the plain-j degree is 78 while the orbit size is 12; for
  p24 the analogous half-class scale is 102940198007 while |Omega| is 5549.
  So a zero-lemma proof needs a genuinely small phase divisor or a local
  intersection formula, not a large plain-j divisor.

p24/trace_frame_translate_minor_dominance_boundary.md
  Principal-term dominance proves only characteristic-zero nonvanishing and
  the selected leading minor does not have an obvious many-principal-factor
  term.

p24/trace_frame_weighted_fourier_expansion.md
  The determinant is full-support Cauchy-Binet cancellation in the CM weights.
```

The analogous Hermitian packet diagnostic:

```text
p24/agent_hermitian_punit_followup.md
p24/phase_divisor_heegner_support_boundary.md
```

reached the same boundary: easy plain-`j` Heegner support is not visible; a
successful product formula must construct a genuinely phase-aware divisor.

## Local-Intersection Route

If such a divisor is constructed, the proof shape is clean:

```text
1. Identify Psi_lead / Xi_lead as a p-unit factor.
2. Use a local valuation formula for the CM value of Psi_lead.
3. Show the principal part has no p-local representation/intersection term at
   the selected ordinary split prime.
4. Conclude ord_P(Psi_lead)=0 and hence ord_P(Xi_lead)=0.
5. Feed Xi_lead p-unitness into the trace-frame norm-compressed certificate.
```

The obstruction is step 1.  Existing global product formulas naturally compute
symmetric products, pairwise difference norms, genus traces, or CM averages.
Those operations discard the high-order packet phase that the trace-frame
minor needs.

## Boundary

This route remains one of the few plausible arithmetic exits, but it now has
a precise missing input:

```text
construct a phase-aware Borcherds/divisor object whose CM value is the
trace-frame leading determinant-line norm Xi_lead, without enumerating the
order-3107441 class packet.
```

Until such a construction is supplied, product-formula technology repackages
the p-unit theorem rather than proving it.
