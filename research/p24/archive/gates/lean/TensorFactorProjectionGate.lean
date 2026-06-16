/-!
Finite gate for one tensor-factor projection certificates.

The p24 tensor route now targets one irreducible factor `B_i` of

    A_a tensor F_p(mu_m).

This file checks only the abstract logic:

* if a projection of the extended evaluation map to one factor is injective,
  then the extended evaluation map itself is injective;
* if a coordinate projection after that factor projection is injective, then
  the factor projection is injective.

Combined with `ScalarExtensionGate.lean`, this is the formal bridge from a
nonzero one-factor coordinate minor to base packet axis injectivity.
-/

namespace P24.TensorFactorProjectionGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

theorem injective_from_factor_projection
    {Source TensorAlgebra Factor : Type}
    (extEval : Source → TensorAlgebra)
    (factorProject : TensorAlgebra → Factor)
    (h_factor_injective :
      Injective (fun source => factorProject (extEval source))) :
    Injective extEval := by
  intro left right h_eval
  apply h_factor_injective
  exact congrArg factorProject h_eval

theorem factor_injective_from_coordinate_projection
    {Source TensorAlgebra Factor Coordinates : Type}
    (extEval : Source → TensorAlgebra)
    (factorProject : TensorAlgebra → Factor)
    (coordinateProject : Factor → Coordinates)
    (h_coordinate_injective :
      Injective
        (fun source => coordinateProject (factorProject (extEval source)))) :
    Injective (fun source => factorProject (extEval source)) := by
  intro left right h_factor
  apply h_coordinate_injective
  exact congrArg coordinateProject h_factor

theorem injective_from_factor_coordinate_projection
    {Source TensorAlgebra Factor Coordinates : Type}
    (extEval : Source → TensorAlgebra)
    (factorProject : TensorAlgebra → Factor)
    (coordinateProject : Factor → Coordinates)
    (h_coordinate_injective :
      Injective
        (fun source => coordinateProject (factorProject (extEval source)))) :
    Injective extEval := by
  apply injective_from_factor_projection extEval factorProject
  exact factor_injective_from_coordinate_projection
    extEval factorProject coordinateProject h_coordinate_injective

end P24.TensorFactorProjectionGate
