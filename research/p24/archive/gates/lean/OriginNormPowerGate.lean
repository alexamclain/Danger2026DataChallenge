/-!
Finite gate for the origin-norm power bridge.

The arithmetic observation is that, in trace-GCD origin coordinates, a larger
origin norm may be a p-unit multiple of a power of the reduced right product.
Lean does not formalize the power formula here.  It records the finite logic:

* if a zero of the reduced right product forces the larger norm to vanish,
* and the larger norm is nonzero,
* and a zero determinant factor forces the reduced right product to vanish,

then every determinant factor is nonzero.
-/

namespace P24.OriginNormPowerGate

def RightProductDetectsFactorZeros {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (rightProduct : Scalar) : Prop :=
  (∃ t, Delta t = 0) → rightProduct = 0

def FullNormDetectsRightProductZero {Scalar : Type} [Zero Scalar]
    (rightProduct fullNorm : Scalar) : Prop :=
  rightProduct = 0 → fullNorm = 0

theorem right_product_nonzero_from_full_norm
    {Scalar : Type} [Zero Scalar]
    (rightProduct fullNorm : Scalar)
    (h_detects : FullNormDetectsRightProductZero rightProduct fullNorm)
    (h_full_nonzero : fullNorm ≠ 0) :
    rightProduct ≠ 0 := by
  intro h_right_zero
  exact h_full_nonzero (h_detects h_right_zero)

theorem right_factors_nonzero_from_full_norm
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (rightProduct fullNorm : Scalar)
    (h_factor_detects :
      RightProductDetectsFactorZeros Delta rightProduct)
    (h_norm_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm)
    (h_full_nonzero : fullNorm ≠ 0) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_right_nonzero :
      rightProduct ≠ 0 :=
    right_product_nonzero_from_full_norm rightProduct fullNorm
      h_norm_detects h_full_nonzero
  exact h_right_nonzero (h_factor_detects ⟨t, h_delta_zero⟩)

theorem selected_good_from_full_origin_norm
    {Index Scalar : Type} [Zero Scalar]
    (Delta : Index → Scalar)
    (rightProduct fullNorm : Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (h_factor_detects :
      RightProductDetectsFactorZeros Delta rightProduct)
    (h_norm_detects :
      FullNormDetectsRightProductZero rightProduct fullNorm)
    (h_full_nonzero : fullNorm ≠ 0)
    (h_det_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_det_to_good selected
    (right_factors_nonzero_from_full_norm Delta rightProduct fullNorm
      h_factor_detects h_norm_detects h_full_nonzero selected)

end P24.OriginNormPowerGate
