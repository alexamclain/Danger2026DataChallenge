/-!
Finite gate for the mixed Moore-circulant theorem candidate.

The arithmetic theorem now being targeted says that the six p24 mixed
Hermitian seed cycles have no nonzero skew-linearized annihilator of
`p`-degree `<156`.

This file does not prove that arithmetic statement.  It checks the finite
logic around it: once every mixed-block rank failure is known to produce a
nonzero skew annihilator, an annihilator-free seed tuple rules out rank
failure.
-/

namespace P24.MixedMooreGate

def AllZero {ι κ α : Type} [Zero α] (eval : ι → κ → α) : Prop :=
  ∀ i k, eval i k = 0

def HasNonzeroAnnihilator {Coeff ι κ α : Type} [Zero α]
    (zeroCoeff : Coeff)
    (eval : Coeff → ι → κ → α) : Prop :=
  ∃ coeff, coeff ≠ zeroCoeff ∧ AllZero (eval coeff)

def AnnihilatorFree {Coeff ι κ α : Type} [Zero α]
    (zeroCoeff : Coeff)
    (eval : Coeff → ι → κ → α) : Prop :=
  ∀ coeff, coeff ≠ zeroCoeff → ∃ i k, eval coeff i k ≠ 0

theorem no_nonzero_annihilator_from_free
    {Coeff ι κ α : Type} [Zero α]
    (zeroCoeff : Coeff)
    (eval : Coeff → ι → κ → α) :
    AnnihilatorFree zeroCoeff eval →
      ¬ HasNonzeroAnnihilator zeroCoeff eval := by
  intro h_free h_ann
  rcases h_ann with ⟨coeff, h_nonzero, h_all_zero⟩
  rcases h_free coeff h_nonzero with ⟨i, k, h_coord_nonzero⟩
  exact h_coord_nonzero (h_all_zero i k)

theorem no_rank_failure_from_annihilator_free
    {Coeff ι κ α : Type} {RankFailure : Prop} [Zero α]
    (zeroCoeff : Coeff)
    (eval : Coeff → ι → κ → α)
    (rankFailureGivesAnnihilator :
      RankFailure → HasNonzeroAnnihilator zeroCoeff eval)
    (h_free : AnnihilatorFree zeroCoeff eval) :
    ¬ RankFailure := by
  intro h_failure
  have h_no_ann :
      ¬ HasNonzeroAnnihilator zeroCoeff eval :=
    no_nonzero_annihilator_from_free zeroCoeff eval h_free
  exact h_no_ann (rankFailureGivesAnnihilator h_failure)

theorem rank_ok_from_no_nonzero_annihilator
    {Coeff ι κ α : Type} {RankFailure : Prop} [Zero α]
    (zeroCoeff : Coeff)
    (eval : Coeff → ι → κ → α)
    (rankFailureGivesAnnihilator :
      RankFailure → HasNonzeroAnnihilator zeroCoeff eval)
    (h_no_ann : ¬ HasNonzeroAnnihilator zeroCoeff eval) :
    ¬ RankFailure := by
  intro h_failure
  exact h_no_ann (rankFailureGivesAnnihilator h_failure)

end P24.MixedMooreGate
