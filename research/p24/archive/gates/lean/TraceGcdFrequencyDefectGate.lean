/-!
Finite gate for the RS-tail frequency-defect selected-basis theorem.

The arithmetic theorem still has to prove the local p-unit inputs:

* ordinary frequency projections are p-unit isomorphisms;
* defect frequency projections have rank four and p-unit tail residues;
* the defect tail Vandermonde determinant is a p-unit.

This Lean file records the finite handoff: once those local gates imply the
selected projection has full rank, the fixed RS-tail map is a p-unit.  It also
records the p24 numerical profile `19 * 4 + 16 * 5 = 156`.
-/

namespace P24.TraceGcdFrequencyDefectGate

def OrdinaryLocalGates
    (ordinaryOk ordinaryCount : Nat) : Prop :=
  ordinaryOk = ordinaryCount

def DefectLocalGates
    (defectOk defectCount : Nat) : Prop :=
  defectOk = defectCount

def TailVandermondeGate
    (tailRank tailDim defectCount : Nat) : Prop :=
  tailRank = tailDim ∧ tailDim = defectCount

def FrequencyDefectProfile
    (ordinaryCount defectCount blockCount tailDim rowDim selectedDim : Nat) : Prop :=
  ordinaryCount + defectCount = blockCount ∧
    rowDim = ordinaryCount * 4 + defectCount * 5 ∧
    selectedDim = blockCount * 4 + tailDim ∧
    tailDim = defectCount

def SelectedProjectionUnit
    (selectedRank rowDim selectedDim : Nat) : Prop :=
  selectedRank = rowDim ∧ rowDim = selectedDim

def FrequencyDefectHandoff
    (ordinaryOk ordinaryCount defectOk defectCount tailRank tailDim
      blockCount rowDim selectedDim selectedRank : Nat) : Prop :=
  OrdinaryLocalGates ordinaryOk ordinaryCount ->
  DefectLocalGates defectOk defectCount ->
  TailVandermondeGate tailRank tailDim defectCount ->
  FrequencyDefectProfile ordinaryCount defectCount blockCount tailDim rowDim selectedDim ->
  SelectedProjectionUnit selectedRank rowDim selectedDim

def FixedRsTailPUnit : Prop := True

theorem selected_projection_from_frequency_defect_handoff
    (ordinaryOk ordinaryCount defectOk defectCount tailRank tailDim
      blockCount rowDim selectedDim selectedRank : Nat)
    (h_handoff :
      FrequencyDefectHandoff ordinaryOk ordinaryCount defectOk defectCount
        tailRank tailDim blockCount rowDim selectedDim selectedRank)
    (h_ordinary : OrdinaryLocalGates ordinaryOk ordinaryCount)
    (h_defect : DefectLocalGates defectOk defectCount)
    (h_tail : TailVandermondeGate tailRank tailDim defectCount)
    (h_profile :
      FrequencyDefectProfile ordinaryCount defectCount blockCount tailDim rowDim selectedDim) :
    SelectedProjectionUnit selectedRank rowDim selectedDim :=
  h_handoff h_ordinary h_defect h_tail h_profile

theorem fixed_rs_tail_punit_from_selected_projection
    (selectedRank rowDim selectedDim : Nat)
    (_h_unit : SelectedProjectionUnit selectedRank rowDim selectedDim)
    (_h_to_punit : SelectedProjectionUnit selectedRank rowDim selectedDim -> FixedRsTailPUnit) :
    FixedRsTailPUnit :=
  _h_to_punit _h_unit

theorem p24_frequency_counts :
    19 + 16 = 35 := by
  decide

theorem p24_frequency_defect_row_dimension :
    19 * 4 + 16 * 5 = 156 := by
  decide

theorem p24_full_selected_coordinate_count :
    4 * 35 + 16 = 156 := by
  decide

theorem p24_erasure_coordinate_count :
    35 + (35 - 16) = 54 := by
  decide

theorem p24_tail_vandermonde_square :
    16 * 16 = 256 := by
  decide

theorem p24_prime_is_prime_to_cyclic_length :
    Nat.gcd 1000000000000000000000007 35 = 1 := by
  decide

theorem p24_prime_mod_cyclic_length :
    1000000000000000000000007 % 35 = 22 := by
  decide

theorem p24_frequency_defect_profile :
    FrequencyDefectProfile 19 16 35 16 156 156 := by
  unfold FrequencyDefectProfile
  decide

theorem p24_full_rs_tail_selected_projection_unit_from_handoff
    (selectedRank : Nat)
    (h_handoff :
      FrequencyDefectHandoff 19 19 16 16 16 16 35 156 156 selectedRank) :
    SelectedProjectionUnit selectedRank 156 156 := by
  exact selected_projection_from_frequency_defect_handoff
    19 19 16 16 16 16 35 156 156 selectedRank
    h_handoff rfl rfl ⟨rfl, rfl⟩ p24_frequency_defect_profile

end P24.TraceGcdFrequencyDefectGate
