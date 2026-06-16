# Subagent CS/ML/Probability Theorem Candidates

Date: 2026-06-05

This note preserves a read-only subagent synthesis.  The useful import from
CS/probability/ML theory is not generic randomness as proof, but exact
nonvanishing languages that can instantiate the finite trace-GCD gates.

## 1. Trace-GCD Operator-Resultant Unit

Statement shape:

```text
f(Y)=det(P V_univ A) in O_F[Y]/(Y^211 - 1)
Res(Y^211 - 1, f) = prod_t det(P V_t A) is a p-unit.
```

Why it matters:

```text
Res != 0 => Delta(t) != 0 for all t
          => W cap V_t^{-1} C = {0} for all t
          => trace-GCD Schubert finite gate.
```

Evidence/falsifier:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
p24/lang_trace_gcd_schubert_orbit_theorem.md
p24/lang_trace_gcd_spectral_scan_boundary.md
```

Small experiment:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_fast_falsifier_harness.py --workers 4
```

Falsify by finding an eligible actual-CM row with `zeros>0`, product zero, or
an operator/resultant mismatch in the toy identity.

## 2. Support-Specific Moore/Subspace-Polynomial P-Unit

Statement shape:

```text
dim ker(A_B) = 16,
det(tau_a(k_b))_{1<=a,b<=16} in F_p^*
```

for the representative p24 support:

```text
B = {O2,O3,O5,O6}, tail = first 16 coordinates of O1.
```

Why it matters:

This is the smallest mixed proof-facing object.  It proves the representative
leading Moore p-unit, and the existing unit-orbit gates propagate that to the
six deletion rows.

Evidence/falsifier:

```text
p24/punit_route_comparison_frontier.md
p24/trace_gcd_schubert_support_dictionary.md
p24/representative_cs_theory_candidate_boundary.md
```

Small experiment:

Run the pinned small-CM block/subspace audits and falsify by finding a row
where prefix rank is full but the selected tail rank gain is too small.

## 3. Trace-Frame Schubert Packet-Norm Identity

Statement shape:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail
```

are equivariant packet Schubert determinant elements whose relative norms to
the base packet field are p-units.

Why it matters:

This compresses packetwise Schubert p-units to a few norm statements and
would feed the trace-frame leading Plucker gate.

Evidence/falsifier:

```text
p24/trace_frame_factorized_schubert_punit.md
p24/tensor_factor_plucker_norm_miner.md
```

Small experiment:

Mine the same norm identity across several small CM rows after CM-adapted
basis changes; demote if the identity does not survive holdout rows.

## 4. Metric-Preserving LRS/MSRD Equivalence

Statement shape:

```text
W_axis(B) is p-integrally block-equivalent to an LRS/MSRD code
```

with sufficient sum-rank distance, or the mixed `[210,156]` code has the
exact scalar-support metric needed for the 54-coordinate erasure support.

Why it matters:

An actual metric-preserving equivalence would force the support obstruction
away without proving the selected determinant directly.

Evidence/falsifier:

```text
p24/msrd_metric_boundary.md
p24/trace_frame_lrs_signature_boundary.md
```

Small experiment:

Normalize small pinned rows and solve for q-linearized LRS evaluation data.
Failure does not hurt the operator-resultant route; it only demotes hidden
MSRD further.

## 5. Pointwise Selected-Prime Anti-Concentration

Statement shape:

```text
#{sigma : Z(sigma P) = 0} = 0
```

for the relevant Schubert section, trace-Gram determinant, or packet scalar at
the selected prime above p.  A quantitative bound `<1` would be enough.

Why it matters:

This would turn anti-concentration into a deterministic p-unit theorem.  It
must be pointwise for the selected prime; average Chebotarev or
Schwartz-Zippel-style evidence is not certificate evidence.

Evidence/falsifier:

```text
p24/subagent_probability_lift_sidecar.md
p24/cs_ml_theory_imports.md
```

Small experiment:

Run packetized content and trace-frame residual audits on exact small CM rows;
any eligible selected-prime zero falsifies the pointwise theorem candidate.

## Ordering

The current priority order remains:

```text
1. operator-resultant p-unit / compressed norm soundness;
2. support-specific Moore tail-on-kernel p-unit;
3. trace-frame packet norm identity;
4. MSRD/LRS only with an explicit metric-preserving equivalence;
5. pointwise anti-concentration only if it becomes a deterministic
   selected-prime zero-count theorem.
```
