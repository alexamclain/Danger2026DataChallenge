/-!
Finite gate for trace-GCD diamond/right-unit equivariance.

The arithmetic theorem may construct the trace-GCD Fitting determinant-line
sections so that the right-unit/diamond action carries one orbit section to
the next, after multiplying by a p-unit transition factor.  This file records
only the finite consequence:

* a determinant-line comparison `Xi_next = unit * Xi_current`;
* p-unit transition factors preserve p-unitness;
* one representative p-unit therefore propagates around the six nonzero
  p24 right orbits;
* together with the fixed orbit p-unit, all seven orbit norms are p-units.

No modular curve, CM, Fitting module, determinant, or p-adic geometry is
formalized here.
-/

namespace P24.TraceGcdDiamondEquivarianceGate

def UnitScaled {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (unit : Unit)
    (current next : Scalar) : Prop :=
  next = scale unit current

def ScaleTransfersPUnit {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop) : Prop :=
  ∀ unit value, PUnitScale unit → PUnitScalar value →
    PUnitScalar (scale unit value)

def DeterminantTransportScale {Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (sourceDetInv targetDet transition : Scalar) : Prop :=
  transition = mul targetDet sourceDetInv

def PUnitMulClosed {Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop) : Prop :=
  ∀ left right, PUnitScalar left → PUnitScalar right →
    PUnitScalar (mul left right)

theorem punit_transition_from_integral_det_transport
    {Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (sourceDetInv targetDet transition : Scalar)
    (h_mul_closed : PUnitMulClosed mul PUnitScalar)
    (h_source : PUnitScalar sourceDetInv)
    (h_target : PUnitScalar targetDet)
    (h_transition :
      DeterminantTransportScale mul sourceDetInv targetDet transition) :
    PUnitScalar transition := by
  unfold DeterminantTransportScale at h_transition
  rw [h_transition]
  exact h_mul_closed targetDet sourceDetInv h_target h_source

theorem punit_arrow_from_commuting_integral_det_transport
    {Scalar : Type}
    (mul : Scalar → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (sourceDetInv targetDet transition current next : Scalar)
    (h_mul_closed : PUnitMulClosed mul PUnitScalar)
    (h_source : PUnitScalar sourceDetInv)
    (h_target : PUnitScalar targetDet)
    (h_transition :
      DeterminantTransportScale mul sourceDetInv targetDet transition)
    (h_next : next = mul transition current)
    (h_current : PUnitScalar current) :
    PUnitScalar next := by
  have h_transition_punit : PUnitScalar transition :=
    punit_transition_from_integral_det_transport
      mul PUnitScalar sourceDetInv targetDet transition
      h_mul_closed h_source h_target h_transition
  rw [h_next]
  exact h_mul_closed transition current h_transition_punit h_current

theorem punit_arrow_from_unit_scaled
    {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (unit : Unit)
    (current next : Scalar)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_unit : PUnitScale unit)
    (h_scaled : UnitScaled scale unit current next)
    (h_current : PUnitScalar current) :
    PUnitScalar next := by
  unfold UnitScaled at h_scaled
  rw [h_scaled]
  exact h_transfer unit current h_unit h_current

theorem six_cycle_punits_from_scaled_diamond
    {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (x1 x2 x3 x4 x5 x6 : Scalar)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (_h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 x1 x2)
    (h23 : UnitScaled scale u23 x2 x3)
    (h34 : UnitScaled scale u34 x3 x4)
    (h45 : UnitScaled scale u45 x4 x5)
    (h56 : UnitScaled scale u56 x5 x6)
    (_h61 : UnitScaled scale u61 x6 x1)
    (h_x1 : PUnitScalar x1) :
    PUnitScalar x1 ∧ PUnitScalar x2 ∧ PUnitScalar x3 ∧
      PUnitScalar x4 ∧ PUnitScalar x5 ∧ PUnitScalar x6 := by
  have h_x2 : PUnitScalar x2 :=
    punit_arrow_from_unit_scaled scale PUnitScalar PUnitScale
      u12 x1 x2 h_transfer h_u12 h12 h_x1
  have h_x3 : PUnitScalar x3 :=
    punit_arrow_from_unit_scaled scale PUnitScalar PUnitScale
      u23 x2 x3 h_transfer h_u23 h23 h_x2
  have h_x4 : PUnitScalar x4 :=
    punit_arrow_from_unit_scaled scale PUnitScalar PUnitScale
      u34 x3 x4 h_transfer h_u34 h34 h_x3
  have h_x5 : PUnitScalar x5 :=
    punit_arrow_from_unit_scaled scale PUnitScalar PUnitScale
      u45 x4 x5 h_transfer h_u45 h45 h_x4
  have h_x6 : PUnitScalar x6 :=
    punit_arrow_from_unit_scaled scale PUnitScalar PUnitScale
      u56 x5 x6 h_transfer h_u56 h56 h_x5
  exact ⟨h_x1, h_x2, h_x3, h_x4, h_x5, h_x6⟩

theorem seven_orbit_punits_from_fixed_and_scaled_diamond
    {Scalar Unit : Type}
    (scale : Unit → Scalar → Scalar)
    (PUnitScalar : Scalar → Prop)
    (PUnitScale : Unit → Prop)
    (x0 x1 x2 x3 x4 x5 x6 : Scalar)
    (u12 u23 u34 u45 u56 u61 : Unit)
    (h_transfer : ScaleTransfersPUnit scale PUnitScalar PUnitScale)
    (h_u12 : PUnitScale u12)
    (h_u23 : PUnitScale u23)
    (h_u34 : PUnitScale u34)
    (h_u45 : PUnitScale u45)
    (h_u56 : PUnitScale u56)
    (h_u61 : PUnitScale u61)
    (h12 : UnitScaled scale u12 x1 x2)
    (h23 : UnitScaled scale u23 x2 x3)
    (h34 : UnitScaled scale u34 x3 x4)
    (h45 : UnitScaled scale u45 x4 x5)
    (h56 : UnitScaled scale u56 x5 x6)
    (h61 : UnitScaled scale u61 x6 x1)
    (h_x0 : PUnitScalar x0)
    (h_x1 : PUnitScalar x1) :
    PUnitScalar x0 ∧ PUnitScalar x1 ∧ PUnitScalar x2 ∧
      PUnitScalar x3 ∧ PUnitScalar x4 ∧ PUnitScalar x5 ∧
      PUnitScalar x6 := by
  have h_cycle :
      PUnitScalar x1 ∧ PUnitScalar x2 ∧ PUnitScalar x3 ∧
        PUnitScalar x4 ∧ PUnitScalar x5 ∧ PUnitScalar x6 :=
    six_cycle_punits_from_scaled_diamond
      scale PUnitScalar PUnitScale x1 x2 x3 x4 x5 x6
      u12 u23 u34 u45 u56 u61 h_transfer
      h_u12 h_u23 h_u34 h_u45 h_u56 h_u61
      h12 h23 h34 h45 h56 h61 h_x1
  exact ⟨h_x0, h_cycle⟩

theorem p24_diamond_payload_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_diamond_payload_improves_safe_orbit_payload :
    4 < 14 := by
  decide

theorem p24_unit2_prime_to_right_level :
    Nat.gcd 2 211 = 1 := by
  native_decide

theorem p24_transport_denominators_prime_to_p :
    Nat.gcd 1000000000000000000000007
      (2 * 35 * 156 * 157 * 211 * 5460) = 1 := by
  native_decide

theorem p24_unit2_six_steps_is_frobenius_rotation17 :
    (2 ^ 6) % 211 = (114 ^ 17) % 211 := by
  native_decide

theorem p24_tail_rotation17_inside_right_orbit :
    17 < 35 := by
  decide

end P24.TraceGcdDiamondEquivarianceGate
