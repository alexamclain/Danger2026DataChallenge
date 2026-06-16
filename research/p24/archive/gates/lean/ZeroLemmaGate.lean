/-!
Finite-field zero-lemma gate for the p24 correspondence route.

This file uses only Lean core.  It does not formalize divisors on modular
curves; instead it records the small logical step used by
`correspondence_zero_lemma_window.md`:

* harmful packet vanishing would give at least `classNumber` zeros;
* a nonzero modular function has at most `poleDegree` zeros;
* if `poleDegree < classNumber`, harmful vanishing is impossible.

The arithmetic/geometric input is the proof that a proposed p24 correspondence
function really has the stated pole degree and is not identically zero.
-/

namespace P24.ZeroLemmaGate

theorem no_harmful_from_zero_bound
    (harmful : Prop)
    (classNumber poleDegree zeroCount : Nat)
    (h_harmful_zeros : harmful → zeroCount = classNumber)
    (h_zero_bound : harmful → zeroCount ≤ poleDegree)
    (h_pole_lt_class : poleDegree < classNumber) :
    ¬ harmful := by
  intro hh
  have hz : zeroCount = classNumber := h_harmful_zeros hh
  have hb : zeroCount ≤ poleDegree := h_zero_bound hh
  have hclass_le_pole : classNumber ≤ poleDegree := by
    rw [← hz]
    exact hb
  have hpole_lt_pole : poleDegree < poleDegree :=
    Nat.lt_of_lt_of_le h_pole_lt_class hclass_le_pole
  exact Nat.lt_irrefl poleDegree hpole_lt_pole

theorem no_harmful_from_correspondence_window
    (harmful : Prop)
    (classNumber poleDegree order index delta zeroCount : Nat)
    (h_class : classNumber = order * index)
    (h_pole : poleDegree = order * delta)
    (h_order_pos : 0 < order)
    (h_harmful_zeros : harmful → zeroCount = classNumber)
    (h_zero_bound : harmful → zeroCount ≤ poleDegree)
    (h_delta_lt_index : delta < index) :
    ¬ harmful := by
  intro hh
  have h_pole_lt_class : poleDegree < classNumber := by
    rw [h_pole, h_class]
    exact Nat.mul_lt_mul_of_pos_left h_delta_lt_index h_order_pos
  exact no_harmful_from_zero_bound harmful classNumber poleDegree zeroCount
    h_harmful_zeros h_zero_bound h_pole_lt_class hh

theorem no_scalar_window_if_delta_ge_one
    (order delta zeroCount poleDegree : Nat)
    (h_zero : zeroCount = order)
    (h_pole : poleDegree = order * delta)
    (h_delta_ge_one : 1 ≤ delta) :
    ¬ poleDegree < zeroCount := by
  intro hlt
  have h_zero_le_pole : zeroCount ≤ poleDegree := by
    rw [h_zero, h_pole]
    have hmul : order * 1 ≤ order * delta :=
      Nat.mul_le_mul_left order h_delta_ge_one
    simpa using hmul
  exact (Nat.not_lt_of_ge h_zero_le_pole) hlt

theorem no_scalar_family_window_if_total_delta_ge_pieces
    (pieces order totalDelta zeroCount poleDegree : Nat)
    (h_zero : zeroCount = order * pieces)
    (h_pole : poleDegree = order * totalDelta)
    (h_pieces_le_delta : pieces ≤ totalDelta) :
    ¬ poleDegree < zeroCount := by
  intro hlt
  have h_zero_le_pole : zeroCount ≤ poleDegree := by
    rw [h_zero, h_pole]
    exact Nat.mul_le_mul_left order h_pieces_le_delta
  exact (Nat.not_lt_of_ge h_zero_le_pole) hlt

theorem orbit_zero_impossible_from_pole_lt_orbit
    (orbitZero : Prop)
    (orbitSize poleDegree zeroCount : Nat)
    (h_orbit_zeros : orbitZero → zeroCount = orbitSize)
    (h_zero_bound : orbitZero → zeroCount ≤ poleDegree)
    (h_pole_lt_orbit : poleDegree < orbitSize) :
    ¬ orbitZero := by
  exact no_harmful_from_zero_bound
    orbitZero orbitSize poleDegree zeroCount
    h_orbit_zeros h_zero_bound h_pole_lt_orbit

theorem pinned_trace_frame_plain_j_degree_not_below_orbit :
    ¬ 78 < 12 := by
  decide

theorem p24_third_trace_half_class_degree_not_below_beta_orbit :
    ¬ 102940198007 < 5549 := by
  decide

end P24.ZeroLemmaGate
