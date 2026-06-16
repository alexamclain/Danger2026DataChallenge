/-!
Finite gate for the embedded selector degree lower bound.

The mathematical note `p24/finite_field_selector_degree_theorem.md` uses a
curve/fiber argument: if a rational function is constant on an `H`-coset of
CM points, then the corresponding fiber contains at least `|H|` distinct
points, so the function degree is at least `|H|`.

This Lean file checks only the finite numerical/logical skeleton.  The
geometry supplies the external input:

* `fiberSize value` is at least the selected coset size;
* every fiber size is at most the function degree.

Then `cosetSize <= degree`, so a bounded-degree selector is impossible when
`degree < cosetSize`.
-/

namespace P24.SelectorDegreeLowerBoundGate

def FiberBound {Value : Type} (fiberSize : Value → Nat) (degree : Nat) : Prop :=
  ∀ value, fiberSize value ≤ degree

theorem selector_degree_lower_bound
    {Value : Type}
    (fiberSize : Value → Nat)
    (degree cosetSize : Nat)
    (selectedValue : Value)
    (h_coset_in_fiber : cosetSize ≤ fiberSize selectedValue)
    (h_fiber_bound : FiberBound fiberSize degree) :
    cosetSize ≤ degree :=
  Nat.le_trans h_coset_in_fiber (h_fiber_bound selectedValue)

theorem no_selector_below_coset_size
    {Value : Type}
    (fiberSize : Value → Nat)
    (degree cosetSize : Nat)
    (selectedValue : Value)
    (h_coset_in_fiber : cosetSize ≤ fiberSize selectedValue)
    (h_fiber_bound : FiberBound fiberSize degree)
    (h_too_small : degree < cosetSize) :
    False := by
  have h_lower : cosetSize ≤ degree :=
    selector_degree_lower_bound
      fiberSize degree cosetSize selectedValue h_coset_in_fiber h_fiber_bound
  exact Nat.not_lt_of_ge h_lower h_too_small

theorem third_trace_recovery_degree_subsqrt :
    3107441 < 1000000000000 := by
  decide

theorem third_trace_quotient_degree_subsqrt :
    66254 < 1000000000000 := by
  decide

theorem third_trace_selected_chain_payload_subsqrt :
    2 + 157 + 211 + 3107441 < 1000000000000 := by
  decide

theorem third_trace_selected_chain_plus_anchor_subsqrt :
    2 + 157 + 211 + 3107441 + 179 + 89 < 1000000000000 := by
  decide

theorem third_trace_full_relative_payload_subsqrt :
    2 + 2 * 157 + 314 * 211 + 3107441 < 1000000000000 := by
  decide

theorem first_trace_order19_recovery_degree_subsqrt :
    14670196166 < 1000000000000 := by
  decide

theorem first_trace_order19_payload_subsqrt :
    19 + 14670196166 < 1000000000000 := by
  decide

theorem p24_recovery_degree_dominates_anchor_degrees :
    89 < 3107441 ∧ 179 < 3107441 ∧ 5549 < 3107441 := by
  decide

theorem p24_kernel_degree_too_small_for_recovery_selector
    {Value : Type}
    (fiberSize : Value → Nat)
    (selectedValue : Value)
    (h_coset_in_fiber : 3107441 ≤ fiberSize selectedValue)
    (h_fiber_bound : FiberBound fiberSize 89) :
    False :=
  no_selector_below_coset_size
    fiberSize 89 3107441 selectedValue h_coset_in_fiber
    h_fiber_bound (by decide)

theorem p24_anchor_degree_too_small_for_recovery_selector
    {Value : Type}
    (fiberSize : Value → Nat)
    (selectedValue : Value)
    (h_coset_in_fiber : 3107441 ≤ fiberSize selectedValue)
    (h_fiber_bound : FiberBound fiberSize 179) :
    False :=
  no_selector_below_coset_size
    fiberSize 179 3107441 selectedValue h_coset_in_fiber
    h_fiber_bound (by decide)

theorem p24_internal_degree_too_small_for_recovery_selector
    {Value : Type}
    (fiberSize : Value → Nat)
    (selectedValue : Value)
    (h_coset_in_fiber : 3107441 ≤ fiberSize selectedValue)
    (h_fiber_bound : FiberBound fiberSize 5549) :
    False :=
  no_selector_below_coset_size
    fiberSize 5549 3107441 selectedValue h_coset_in_fiber
    h_fiber_bound (by decide)

end P24.SelectorDegreeLowerBoundGate
