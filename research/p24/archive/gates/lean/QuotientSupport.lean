/-!
Finite support gate for quotient-factored period selectors.

This file is deliberately algebra-light.  The Fourier cancellation step
``A(s) J(s) = E(s) J(s), J(s) != 0 => A(s)=E(s)`` is supplied as a hypothesis;
the theorem checks the remaining finite logic:

* if `A` and the subgroup projector `E` are supported on the quotient spectrum,
* and they agree on every quotient character,
* then they agree on every character.

For p24 this is the exact gate behind the statement that quotient-packet
nonvanishing suffices only for operators already known to descend to `G/H`.
-/

namespace P24.QuotientSupport

def SupportedOn {ι α : Type} [Zero α] (Q : ι → Prop) (f : ι → α) : Prop :=
  ∀ s, ¬ Q s → f s = 0

theorem equal_of_supported_and_equal_on
    {ι α : Type} [Zero α]
    (Q : ι → Prop)
    (A E : ι → α)
    (hA : SupportedOn Q A)
    (hE : SupportedOn Q E)
    (h_on_Q : ∀ s, Q s → A s = E s) :
    ∀ s, A s = E s := by
  intro s
  by_cases hs : Q s
  · exact h_on_Q s hs
  · calc
      A s = 0 := hA s hs
      _ = E s := (hE s hs).symm

theorem quotient_nonzero_forces_projector
    {ι α : Type} [Zero α]
    (Q : ι → Prop)
    (A E : ι → α)
    (hA : SupportedOn Q A)
    (hE : SupportedOn Q E)
    (h_cancel_on_nonzero : ∀ s, Q s → A s = E s) :
    ∀ s, A s = E s :=
  equal_of_supported_and_equal_on Q A E hA hE h_cancel_on_nonzero

theorem need_support_hypothesis_countergate
    {ι α : Type} [Zero α]
    (Q : ι → Prop)
    (A E : ι → α)
    (_h_on_Q : ∀ s, Q s → A s = E s)
    (s0 : ι)
    (_hs0 : ¬ Q s0)
    (h_diff : A s0 ≠ E s0) :
    ¬ (∀ s, A s = E s) := by
  intro h_all
  exact h_diff (h_all s0)

end P24.QuotientSupport
