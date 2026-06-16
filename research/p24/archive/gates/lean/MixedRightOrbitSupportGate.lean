/-!
Finite gate for the mixed right-orbit support strengthening.

The arithmetic candidate says that every nonzero left twist has at least two
nonzero right-orbit trace values.  This file checks the finite consequences:

* support >= 2 implies the original separation theorem;
* support >= 2 implies that deleting any one right orbit still separates.
-/

namespace P24.MixedRightOrbitSupportGate

def Separates {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value) : Prop :=
  ∀ lambda, lambda ≠ 0 → ∃ orbit, traceMap lambda orbit ≠ 0

def SupportAtLeastTwo {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value) : Prop :=
  ∀ lambda, lambda ≠ 0 →
    ∃ orbit₁ orbit₂,
      orbit₁ ≠ orbit₂ ∧
      traceMap lambda orbit₁ ≠ 0 ∧
      traceMap lambda orbit₂ ≠ 0

def DeleteOneSeparates {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value) : Prop :=
  ∀ deleted lambda, lambda ≠ 0 →
    ∃ orbit, orbit ≠ deleted ∧ traceMap lambda orbit ≠ 0

def LeadingDeleteOneSeparates
    {Lambda Orbit Coord CoordValue : Type} [Zero Lambda] [Zero CoordValue]
    (coordMap : Lambda → Orbit → Coord → CoordValue)
    (leading : Orbit → Orbit → Coord → Prop) : Prop :=
  ∀ deleted lambda, lambda ≠ 0 →
    ∃ orbit coord,
      orbit ≠ deleted ∧
      leading deleted orbit coord ∧
      coordMap lambda orbit coord ≠ 0

def ErasureAvoids
    {Lambda Erasure Coord CoordValue : Type} [Zero Lambda] [Zero CoordValue]
    (coordMap : Lambda → Coord → CoordValue)
    (erased : Erasure → Coord → Prop) : Prop :=
  ∀ erasure lambda, lambda ≠ 0 →
    ∃ coord, ¬ erased erasure coord ∧ coordMap lambda coord ≠ 0

theorem separates_from_support_at_least_two
    {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value)
    (h_support : SupportAtLeastTwo traceMap) :
    Separates traceMap := by
  intro lambda h_nonzero
  rcases h_support lambda h_nonzero with
    ⟨orbit₁, _orbit₂, _h_distinct, h_nonzero₁, _h_nonzero₂⟩
  exact ⟨orbit₁, h_nonzero₁⟩

theorem delete_one_separates_from_support_at_least_two
    {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value)
    (h_support : SupportAtLeastTwo traceMap) :
    DeleteOneSeparates traceMap := by
  intro deleted lambda h_nonzero
  rcases h_support lambda h_nonzero with
    ⟨orbit₁, orbit₂, h_distinct, h_nonzero₁, h_nonzero₂⟩
  by_cases h₁ : orbit₁ = deleted
  · exact ⟨orbit₂, by
      intro h₂
      apply h_distinct
      calc
        orbit₁ = deleted := h₁
        _ = orbit₂ := h₂.symm, h_nonzero₂⟩
  · exact ⟨orbit₁, h₁, h_nonzero₁⟩

theorem support_at_least_two_from_delete_one_and_separates
    {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value]
    (traceMap : Lambda → Orbit → Value)
    (h_delete : DeleteOneSeparates traceMap)
    (lambda : Lambda)
    (h_nonzero : lambda ≠ 0)
    (orbit₀ : Orbit)
    (h_orbit₀_nonzero : traceMap lambda orbit₀ ≠ 0) :
    ∃ orbit₁ orbit₂,
      orbit₁ ≠ orbit₂ ∧
      traceMap lambda orbit₁ ≠ 0 ∧
      traceMap lambda orbit₂ ≠ 0 := by
  rcases h_delete orbit₀ lambda h_nonzero with
    ⟨orbit₁, h_not_deleted, h_orbit₁_nonzero⟩
  exact ⟨orbit₀, orbit₁, h_not_deleted.symm, h_orbit₀_nonzero, h_orbit₁_nonzero⟩

theorem support_at_least_two_from_delete_one
    {Lambda Orbit Value : Type} [Zero Lambda] [Zero Value] [Inhabited Orbit]
    (traceMap : Lambda → Orbit → Value)
    (h_delete : DeleteOneSeparates traceMap) :
    SupportAtLeastTwo traceMap := by
  intro lambda h_nonzero
  let deleted : Orbit := default
  rcases h_delete deleted lambda h_nonzero with
    ⟨orbit₀, _h_orbit₀_not_deleted, h_orbit₀_nonzero⟩
  exact support_at_least_two_from_delete_one_and_separates
    traceMap h_delete lambda h_nonzero orbit₀ h_orbit₀_nonzero

theorem delete_one_separates_from_leading
    {Lambda Orbit Value Coord CoordValue : Type}
    [Zero Lambda] [Zero Value] [Zero CoordValue]
    (traceMap : Lambda → Orbit → Value)
    (coordMap : Lambda → Orbit → Coord → CoordValue)
    (leading : Orbit → Orbit → Coord → Prop)
    (h_leading : LeadingDeleteOneSeparates coordMap leading)
    (h_coord_refines_trace :
      ∀ lambda orbit coord,
        coordMap lambda orbit coord ≠ 0 → traceMap lambda orbit ≠ 0) :
    DeleteOneSeparates traceMap := by
  intro deleted lambda h_nonzero
  rcases h_leading deleted lambda h_nonzero with
    ⟨orbit, coord, h_not_deleted, _h_leading, h_coord_nonzero⟩
  exact ⟨orbit, h_not_deleted,
    h_coord_refines_trace lambda orbit coord h_coord_nonzero⟩

theorem delete_one_separates_from_erasure_avoidance
    {Lambda Orbit Value Coord CoordValue : Type}
    [Zero Lambda] [Zero Value] [Zero CoordValue]
    (traceMap : Lambda → Orbit → Value)
    (coordMap : Lambda → Coord → CoordValue)
    (coordOrbit : Coord → Orbit)
    (erased : Orbit → Coord → Prop)
    (h_erasure : ErasureAvoids coordMap erased)
    (h_unerased_not_deleted :
      ∀ deleted coord,
        ¬ erased deleted coord → coordOrbit coord ≠ deleted)
    (h_coord_refines_trace :
      ∀ lambda coord,
        coordMap lambda coord ≠ 0 → traceMap lambda (coordOrbit coord) ≠ 0) :
    DeleteOneSeparates traceMap := by
  intro deleted lambda h_nonzero
  rcases h_erasure deleted lambda h_nonzero with
    ⟨coord, h_not_erased, h_coord_nonzero⟩
  exact ⟨coordOrbit coord,
    h_unerased_not_deleted deleted coord h_not_erased,
    h_coord_refines_trace lambda coord h_coord_nonzero⟩

theorem support_at_least_two_from_leading
    {Lambda Orbit Value Coord CoordValue : Type}
    [Zero Lambda] [Zero Value] [Zero CoordValue] [Inhabited Orbit]
    (traceMap : Lambda → Orbit → Value)
    (coordMap : Lambda → Orbit → Coord → CoordValue)
    (leading : Orbit → Orbit → Coord → Prop)
    (h_leading : LeadingDeleteOneSeparates coordMap leading)
    (h_coord_refines_trace :
      ∀ lambda orbit coord,
        coordMap lambda orbit coord ≠ 0 → traceMap lambda orbit ≠ 0) :
    SupportAtLeastTwo traceMap := by
  exact support_at_least_two_from_delete_one traceMap
    (delete_one_separates_from_leading
      traceMap coordMap leading h_leading h_coord_refines_trace)

theorem support_at_least_two_from_erasure_avoidance
    {Lambda Orbit Value Coord CoordValue : Type}
    [Zero Lambda] [Zero Value] [Zero CoordValue] [Inhabited Orbit]
    (traceMap : Lambda → Orbit → Value)
    (coordMap : Lambda → Coord → CoordValue)
    (coordOrbit : Coord → Orbit)
    (erased : Orbit → Coord → Prop)
    (h_erasure : ErasureAvoids coordMap erased)
    (h_unerased_not_deleted :
      ∀ deleted coord,
        ¬ erased deleted coord → coordOrbit coord ≠ deleted)
    (h_coord_refines_trace :
      ∀ lambda coord,
        coordMap lambda coord ≠ 0 → traceMap lambda (coordOrbit coord) ≠ 0) :
    SupportAtLeastTwo traceMap := by
  exact support_at_least_two_from_delete_one traceMap
    (delete_one_separates_from_erasure_avoidance
      traceMap coordMap coordOrbit erased h_erasure
      h_unerased_not_deleted h_coord_refines_trace)

end P24.MixedRightOrbitSupportGate
