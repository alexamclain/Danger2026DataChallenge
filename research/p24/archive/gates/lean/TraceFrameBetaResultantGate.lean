/-!
Finite gates for the trace-frame beta-product resultant.

The arithmetic object is an interpolant `f` for the beta determinant sequence.
Because the determinant values lie in the base field `E`, the interpolant is
fixed by a semilinear Frobenius/exponent twist.  This file records only the
abstract finite implication; the actual finite-field interpolation and p-unit
theorem live outside Lean.
-/

namespace P24.TraceFrameBetaResultantGate

def EvaluationsSeparate {Poly Point Value : Type}
    (eval : Poly → Point → Value) : Prop :=
  ∀ left right, (∀ point, eval left point = eval right point) → left = right

def AllValuesFixed {Point Value : Type}
    (valueFrob : Value → Value)
    (values : Point → Value) : Prop :=
  ∀ point, valueFrob (values point) = values point

theorem semilinear_fixed_from_fixed_values
    {Poly Point Value : Type}
    (eval : Poly → Point → Value)
    (twist : Poly → Poly)
    (valueFrob : Value → Value)
    (poly : Poly)
    (h_eval_separates : EvaluationsSeparate eval)
    (h_twist_eval :
      ∀ point, eval (twist poly) point = valueFrob (eval poly point))
    (h_values_fixed :
      ∀ point, valueFrob (eval poly point) = eval poly point) :
    twist poly = poly := by
  apply h_eval_separates
  intro point
  calc
    eval (twist poly) point = valueFrob (eval poly point) := h_twist_eval point
    _ = eval poly point := h_values_fixed point

def OrbitProductCertificate {Orbit : Type}
    (GoodOrbit : Orbit → Prop) : Prop :=
  ∀ orbit, GoodOrbit orbit

def BetaBelongsToOrbit {Beta Orbit : Type}
    (orbitOf : Beta → Orbit)
    (GoodBeta : Beta → Prop)
    (GoodOrbit : Orbit → Prop) : Prop :=
  ∀ beta, GoodOrbit (orbitOf beta) → GoodBeta beta

theorem selected_beta_from_orbit_product
    {Beta Orbit : Type}
    (orbitOf : Beta → Orbit)
    (GoodBeta : Beta → Prop)
    (GoodOrbit : Orbit → Prop)
    (selected : Beta)
    (h_belongs : BetaBelongsToOrbit orbitOf GoodBeta GoodOrbit)
    (h_product : OrbitProductCertificate GoodOrbit) :
    GoodBeta selected := by
  exact h_belongs selected (h_product (orbitOf selected))

theorem all_betas_from_orbit_product
    {Beta Orbit : Type}
    (orbitOf : Beta → Orbit)
    (GoodBeta : Beta → Prop)
    (GoodOrbit : Orbit → Prop)
    (h_belongs : BetaBelongsToOrbit orbitOf GoodBeta GoodOrbit)
    (h_product : OrbitProductCertificate GoodOrbit) :
    ∀ beta, GoodBeta beta := by
  intro beta
  exact h_belongs beta (h_product (orbitOf beta))

def ReducedNormMatchesProduct {Orbit Scalar : Type}
    (reducedNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, reducedNorm orbit = orbitProduct orbit

def InversePayload {Scalar : Type} [Mul Scalar] [One Scalar]
    (value inverse : Scalar) : Prop :=
  value * inverse = 1

theorem nonzero_from_inverse_payload
    {Scalar : Type} [Zero Scalar] [One Scalar] [Mul Scalar]
    (value inverse : Scalar)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload value inverse) :
    value ≠ 0 := by
  intro h_value_zero
  exact h_one_ne_zero (by
    calc
      (1 : Scalar) = value * inverse := h_payload.symm
      _ = (0 : Scalar) * inverse := by rw [h_value_zero]
      _ = 0 := h_zero_mul inverse)

theorem orbit_product_nonzero_from_reduced_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm orbitProduct : Orbit → Scalar)
    (orbit : Orbit)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_norm_nonzero : reducedNorm orbit ≠ 0) :
    orbitProduct orbit ≠ 0 := by
  intro h_zero
  exact h_norm_nonzero (by
    rw [h_match orbit, h_zero])

theorem all_betas_from_reduced_norm_product
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (GoodBeta : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_belongs :
      ∀ beta, orbitProduct (orbitOf beta) ≠ 0 → GoodBeta beta)
    (h_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0) :
    ∀ beta, GoodBeta beta := by
  intro beta
  exact h_belongs beta
    (orbit_product_nonzero_from_reduced_norm
      reducedNorm orbitProduct (orbitOf beta) h_match
      (h_norms_nonzero (orbitOf beta)))

theorem lead_values_nonzero_from_reduced_norm_product
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (leadDet : Beta → Scalar)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_zero_factor :
      ∀ beta, leadDet beta = 0 → orbitProduct (orbitOf beta) = 0)
    (h_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0) :
    ∀ beta, leadDet beta ≠ 0 := by
  intro beta h_zero
  exact
    (orbit_product_nonzero_from_reduced_norm
      reducedNorm orbitProduct (orbitOf beta) h_match
      (h_norms_nonzero (orbitOf beta)))
    (h_zero_factor beta h_zero)

theorem all_trace_frames_good_from_lead_reduced_norms
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (leadDet : Beta → Scalar)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (TraceFrameGood : Beta → Prop)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_zero_factor :
      ∀ beta, leadDet beta = 0 → orbitProduct (orbitOf beta) = 0)
    (h_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0)
    (h_lead_good :
      ∀ beta, leadDet beta ≠ 0 → TraceFrameGood beta) :
    ∀ beta, TraceFrameGood beta := by
  intro beta
  exact h_lead_good beta
    (lead_values_nonzero_from_reduced_norm_product
      orbitOf leadDet reducedNorm orbitProduct h_match
      h_zero_factor h_norms_nonzero beta)

theorem reduced_norms_nonzero_from_global_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm : Orbit → Scalar)
    (globalNorm : Scalar)
    (h_any_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    ∀ orbit, reducedNorm orbit ≠ 0 := by
  intro orbit h_zero
  exact h_global_nonzero (h_any_zero ⟨orbit, h_zero⟩)

theorem all_trace_frames_good_from_global_reduced_norm
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (leadDet : Beta → Scalar)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm : Scalar)
    (TraceFrameGood : Beta → Prop)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_zero_factor :
      ∀ beta, leadDet beta = 0 → orbitProduct (orbitOf beta) = 0)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0)
    (h_lead_good :
      ∀ beta, leadDet beta ≠ 0 → TraceFrameGood beta) :
    ∀ beta, TraceFrameGood beta := by
  exact all_trace_frames_good_from_lead_reduced_norms
    orbitOf leadDet reducedNorm orbitProduct TraceFrameGood
    h_match h_zero_factor
    (reduced_norms_nonzero_from_global_norm
      reducedNorm globalNorm h_any_norm_zero h_global_nonzero)
    h_lead_good

theorem all_trace_frames_good_from_global_reduced_norm_inverse_payload
    {Beta Orbit Scalar : Type} [Zero Scalar] [One Scalar] [Mul Scalar]
    (orbitOf : Beta → Orbit)
    (leadDet : Beta → Scalar)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm globalNormInverse : Scalar)
    (TraceFrameGood : Beta → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload globalNorm globalNormInverse)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_zero_factor :
      ∀ beta, leadDet beta = 0 → orbitProduct (orbitOf beta) = 0)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_lead_good :
      ∀ beta, leadDet beta ≠ 0 → TraceFrameGood beta) :
    ∀ beta, TraceFrameGood beta := by
  exact all_trace_frames_good_from_global_reduced_norm
    orbitOf leadDet reducedNorm orbitProduct globalNorm TraceFrameGood
    h_match h_zero_factor h_any_norm_zero
    (nonzero_from_inverse_payload
      globalNorm globalNormInverse h_zero_mul h_one_ne_zero h_payload)
    h_lead_good

theorem no_harmful_from_global_reduced_norm_inverse_payload
    {Beta Orbit Scalar : Type} [Zero Scalar] [One Scalar] [Mul Scalar]
    (orbitOf : Beta → Orbit)
    (leadDet : Beta → Scalar)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (globalNorm globalNormInverse : Scalar)
    (TraceFrameGood Harmful : Beta → Prop)
    (h_zero_mul : ∀ right : Scalar, (0 : Scalar) * right = 0)
    (h_one_ne_zero : (1 : Scalar) ≠ 0)
    (h_payload : InversePayload globalNorm globalNormInverse)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_zero_factor :
      ∀ beta, leadDet beta = 0 → orbitProduct (orbitOf beta) = 0)
    (h_any_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_lead_good :
      ∀ beta, leadDet beta ≠ 0 → TraceFrameGood beta)
    (h_trace_no_harmful :
      ∀ beta, TraceFrameGood beta → ¬ Harmful beta) :
    ∀ beta, ¬ Harmful beta := by
  intro beta
  exact h_trace_no_harmful beta
    (all_trace_frames_good_from_global_reduced_norm_inverse_payload
      orbitOf leadDet reducedNorm orbitProduct globalNorm globalNormInverse
      TraceFrameGood h_zero_mul h_one_ne_zero h_payload h_match
      h_zero_factor h_any_norm_zero h_lead_good beta)

def p24N : Nat := 3107441

def p24NonzeroBetaCount : Nat := p24N - 1

def p24QOrbitLength : Nat := 5549

def p24QOrbitCount : Nat := 560

def p24RhoQuotientOrbitLength : Nat := 7

def p24RhoQuotientOrbitCount : Nat := 80

def p24PFrobeniusQuotientOrbitLength : Nat := 70

def p24PFrobeniusQuotientOrbitCount : Nat := 8

def p24PacketDegree : Nat := 388430

def p24RhoOrder : Nat := 38843

theorem p24_nonzero_beta_q_orbit_count :
    p24NonzeroBetaCount = p24QOrbitCount * p24QOrbitLength := by
  decide

theorem p24_rho_quotient_orbit_accounting :
    p24QOrbitCount =
      p24RhoQuotientOrbitCount * p24RhoQuotientOrbitLength := by
  decide

theorem p24_p_frobenius_quotient_orbit_accounting :
    p24QOrbitCount =
      p24PFrobeniusQuotientOrbitCount *
        p24PFrobeniusQuotientOrbitLength := by
  decide

theorem p24_packet_degree_from_q_orbits :
    p24PacketDegree = p24PFrobeniusQuotientOrbitLength * p24QOrbitLength := by
  decide

theorem p24_rho_order_from_q_orbits :
    p24RhoOrder = p24RhoQuotientOrbitLength * p24QOrbitLength := by
  decide

end P24.TraceFrameBetaResultantGate
