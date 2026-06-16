/-!
Finite ray-kernel verticality gate.

This file does not formalize class field theory.  It records the finite
consequence used in `ray_kernel_embedding_boundary.md`:

* if a level-1 value factors through the ray-to-class projection, then every
  element in the ray kernel fixes it;
* if the kernel action is transitive on each ray fiber, then any
  kernel-invariant construction is constant on the fiber and therefore cannot
  distinguish level structures above the same class coordinate.

For p24, the arithmetic input is the exact sequence
`U_F -> Cl_F(K) -> Cl(K)` and Shimura reciprocity for level-1 `j`.  Lean only
checks the small torsor logic after that input is supplied.
-/

namespace P24.RayKernelVerticality

def FactorsThrough {Ray Class Value : Type}
    (projection : Ray → Class) (value : Ray → Value) : Prop :=
  ∃ classValue : Class → Value, ∀ r, value r = classValue (projection r)

def ActsVertically {Kernel Ray Class : Type}
    (projection : Ray → Class) (act : Kernel → Ray → Ray) : Prop :=
  ∀ u r, projection (act u r) = projection r

def FiberTransitive {Kernel Ray Class : Type}
    (projection : Ray → Class) (act : Kernel → Ray → Ray) : Prop :=
  ∀ r s, projection r = projection s → ∃ u, act u r = s

def KernelInvariant {Kernel Ray Value : Type}
    (act : Kernel → Ray → Ray) (value : Ray → Value) : Prop :=
  ∀ u r, value (act u r) = value r

theorem factors_through_eq_on_fibers
    {Ray Class Value : Type}
    (projection : Ray → Class) (value : Ray → Value)
    (h_factor : FactorsThrough projection value)
    {r s : Ray}
    (h_same : projection r = projection s) :
    value r = value s := by
  rcases h_factor with ⟨classValue, h_value⟩
  calc
    value r = classValue (projection r) := h_value r
    _ = classValue (projection s) := by rw [h_same]
    _ = value s := (h_value s).symm

theorem vertical_action_fixes_factored_value
    {Kernel Ray Class Value : Type}
    (projection : Ray → Class)
    (act : Kernel → Ray → Ray)
    (value : Ray → Value)
    (h_vertical : ActsVertically projection act)
    (h_factor : FactorsThrough projection value) :
    ∀ u r, value (act u r) = value r := by
  intro u r
  exact factors_through_eq_on_fibers projection value h_factor (h_vertical u r)

theorem invariant_eq_on_fibers_of_transitive_kernel
    {Kernel Ray Class Value : Type}
    (projection : Ray → Class)
    (act : Kernel → Ray → Ray)
    (value : Ray → Value)
    (h_transitive : FiberTransitive projection act)
    (h_invariant : KernelInvariant act value)
    {r s : Ray}
    (h_same : projection r = projection s) :
    value r = value s := by
  rcases h_transitive r s h_same with ⟨u, hu⟩
  calc
    value r = value (act u r) := (h_invariant u r).symm
    _ = value s := by rw [hu]

theorem vertical_move_not_detected
    {Kernel Ray Class Value : Type}
    (projection : Ray → Class)
    (act : Kernel → Ray → Ray)
    (value : Ray → Value)
    (h_vertical : ActsVertically projection act)
    (h_factor : FactorsThrough projection value)
    {u : Kernel} {r : Ray}
    (_h_moved : act u r ≠ r) :
    value (act u r) = value r :=
  vertical_action_fixes_factored_value projection act value h_vertical h_factor u r

theorem no_horizontal_distinction_from_kernel_invariant
    {Kernel Ray Class Value : Type}
    (projection : Ray → Class)
    (act : Kernel → Ray → Ray)
    (value : Ray → Value)
    (h_transitive : FiberTransitive projection act)
    (h_invariant : KernelInvariant act value)
    {r s : Ray}
    (h_same : projection r = projection s)
    (h_diff : value r ≠ value s) :
    False :=
  h_diff (invariant_eq_on_fibers_of_transitive_kernel
    projection act value h_transitive h_invariant h_same)

end P24.RayKernelVerticality
