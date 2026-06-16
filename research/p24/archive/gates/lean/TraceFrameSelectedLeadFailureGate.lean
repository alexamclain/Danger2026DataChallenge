/-!
Finite gate for the selected-leading failure module.

The selected p24 leading coordinate uses all of the first two trace/top
blocks and only the first ten coordinates of the third block.  Therefore its
failure condition is:

  prefix = 0 and selected tail head = 0.

The full intrinsic top-three annihilator `F_27` is the smaller condition:

  prefix = 0 and full third tail coefficient = 0.

Thus full-annihilator avoidance is necessary but not sufficient for the
selected leading Plucker coordinate.  This file records the safe implication
and a tiny counterexample to the converse.
-/

namespace P24.TraceFrameSelectedLeadFailureGate

def SelectedLeadAvoidance {Source Factor Prefix Head : Type}
    [Zero Source] [Zero Prefix] [Zero Head]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (head : Factor → Head) : Prop :=
  ∀ source,
    pref (eval source) = 0 →
      head (eval source) = 0 →
        source = 0

def FullTopThreeAvoidance {Source Factor Prefix Coeff : Type}
    [Zero Source] [Zero Prefix] [Zero Coeff]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (coeff : Factor → Coeff) : Prop :=
  ∀ source,
    pref (eval source) = 0 →
      coeff (eval source) = 0 →
        source = 0

def SelectedLeadFailure {Source Factor Prefix Head : Type}
    [Zero Source] [Zero Prefix] [Zero Head]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (head : Factor → Head)
    (source : Source) : Prop :=
  source ≠ 0 ∧ pref (eval source) = 0 ∧ head (eval source) = 0

def FullTopThreeFailure {Source Factor Prefix Coeff : Type}
    [Zero Source] [Zero Prefix] [Zero Coeff]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (coeff : Factor → Coeff)
    (source : Source) : Prop :=
  source ≠ 0 ∧ pref (eval source) = 0 ∧ coeff (eval source) = 0

theorem selected_avoidance_implies_full_top_three_avoidance
    {Source Factor Prefix Head Coeff : Type}
    [Zero Source] [Zero Prefix] [Zero Head] [Zero Coeff]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (head : Factor → Head)
    (coeff : Factor → Coeff)
    (h_coeff_zero_to_head_zero :
      ∀ factor, coeff factor = 0 → head factor = 0)
    (h_selected :
      SelectedLeadAvoidance eval pref head) :
    FullTopThreeAvoidance eval pref coeff := by
  intro source h_prefix h_coeff
  exact h_selected source h_prefix
    (h_coeff_zero_to_head_zero (eval source) h_coeff)

theorem full_top_three_failure_implies_selected_failure
    {Source Factor Prefix Head Coeff : Type}
    [Zero Source] [Zero Prefix] [Zero Head] [Zero Coeff]
    (eval : Source → Factor)
    (pref : Factor → Prefix)
    (head : Factor → Head)
    (coeff : Factor → Coeff)
    (h_coeff_zero_to_head_zero :
      ∀ factor, coeff factor = 0 → head factor = 0)
    {source : Source}
    (h_failure : FullTopThreeFailure eval pref coeff source) :
    SelectedLeadFailure eval pref head source := by
  exact ⟨h_failure.1, h_failure.2.1,
    h_coeff_zero_to_head_zero (eval source) h_failure.2.2⟩

inductive TwoSource where
  | zero
  | bad
  deriving DecidableEq

instance : Zero TwoSource := ⟨TwoSource.zero⟩

inductive Bit where
  | zero
  | one
  deriving DecidableEq

instance : Zero Bit := ⟨Bit.zero⟩

def toyEval (source : TwoSource) : TwoSource := source

def toyPrefix (_source : TwoSource) : Bit := 0

def toyHead (_source : TwoSource) : Bit := 0

def toyCoeff : TwoSource → Bit
  | TwoSource.zero => 0
  | TwoSource.bad => Bit.one

theorem toy_full_top_three_avoidance :
    FullTopThreeAvoidance toyEval toyPrefix toyCoeff := by
  intro source _h_prefix h_coeff
  cases source with
  | zero => rfl
  | bad => cases h_coeff

theorem toy_not_selected_lead_avoidance :
    ¬ SelectedLeadAvoidance toyEval toyPrefix toyHead := by
  intro h_selected
  have h_bad_zero : TwoSource.bad = 0 := by
    exact h_selected TwoSource.bad rfl rfl
  cases h_bad_zero

theorem full_top_three_avoidance_does_not_imply_selected_lead_avoidance :
    FullTopThreeAvoidance toyEval toyPrefix toyCoeff ∧
      ¬ SelectedLeadAvoidance toyEval toyPrefix toyHead := by
  exact ⟨toy_full_top_three_avoidance, toy_not_selected_lead_avoidance⟩

end P24.TraceFrameSelectedLeadFailureGate
