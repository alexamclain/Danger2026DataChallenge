/-!
Finite gate for scalar-extension descent.

The p24 axis map is defined over `F_p`, but K-character diagonalization may
require adjoining independent smooth-axis roots of unity.  This file checks
the formal descent step:

if an evaluation map becomes injective after an injective scalar-extension
embedding of source and target, then the original map was already injective.

The arithmetic work is proving the extended/tensor rank.  Lean only verifies
that this is a valid sufficient certificate for the base packet map.
-/

namespace P24.ScalarExtensionGate

def Injective {α β : Type} (f : α → β) : Prop :=
  ∀ ⦃x y : α⦄, f x = f y → x = y

theorem injective_from_scalar_extension
    {Source Target ExtSource ExtTarget : Type}
    (eval : Source → Target)
    (extEval : ExtSource → ExtTarget)
    (embedSource : Source → ExtSource)
    (embedTarget : Target → ExtTarget)
    (h_commute :
      ∀ source, extEval (embedSource source) = embedTarget (eval source))
    (h_embed_source_injective : Injective embedSource)
    (h_ext_injective : Injective extEval) :
    Injective eval := by
  intro left right h_eval_eq
  apply h_embed_source_injective
  apply h_ext_injective
  calc
    extEval (embedSource left)
        = embedTarget (eval left) := h_commute left
    _ = embedTarget (eval right) := by rw [h_eval_eq]
    _ = extEval (embedSource right) := (h_commute right).symm

theorem injective_from_scalar_extension_factor
    {Source Target ExtSource Factor : Type}
    (eval : Source → Target)
    (factorEval : ExtSource → Factor)
    (embedSource : Source → ExtSource)
    (targetToFactor : Target → Factor)
    (h_commute :
      ∀ source, factorEval (embedSource source) =
        targetToFactor (eval source))
    (h_embed_source_injective : Injective embedSource)
    (h_factor_injective : Injective factorEval) :
    Injective eval := by
  intro left right h_eval_eq
  apply h_embed_source_injective
  apply h_factor_injective
  calc
    factorEval (embedSource left)
        = targetToFactor (eval left) := h_commute left
    _ = targetToFactor (eval right) := by rw [h_eval_eq]
    _ = factorEval (embedSource right) := (h_commute right).symm

theorem base_nonzero_from_extension_nonzero
    {Source Target ExtSource ExtTarget : Type}
    [Zero Source] [Zero Target] [Zero ExtSource] [Zero ExtTarget]
    (eval : Source → Target)
    (extEval : ExtSource → ExtTarget)
    (embedSource : Source → ExtSource)
    (embedTarget : Target → ExtTarget)
    (source : Source)
    (h_commute :
      ∀ source, extEval (embedSource source) = embedTarget (eval source))
    (h_embed_target_zero : embedTarget 0 = 0)
    (h_extension_nonzero : extEval (embedSource source) ≠ 0) :
    eval source ≠ 0 := by
  intro h_eval_zero
  have h_ext_zero : extEval (embedSource source) = 0 := by
    calc
      extEval (embedSource source)
          = embedTarget (eval source) := h_commute source
      _ = embedTarget 0 := by rw [h_eval_zero]
      _ = 0 := h_embed_target_zero
  exact h_extension_nonzero h_ext_zero

end P24.ScalarExtensionGate
