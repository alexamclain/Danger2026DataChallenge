/-!
Finite two-torsion gate for the conductor-2/nonsplit note.

This is not a formal CM proof.  It records the finite `F_2` linear-algebra
piece used in `p24/conductor2_nonsplit_gate.md`:

* identity Frobenius fixes the full two-dimensional 2-torsion;
* a nontrivial unipotent Frobenius with characteristic polynomial `(X-1)^2`
  fixes exactly one coordinate line.
-/

namespace P24.TwoTorsionGate

def f2add : Bool → Bool → Bool
  | false, b => b
  | true, b => !b

def idFrob (v : Bool × Bool) : Bool × Bool :=
  v

def unipotentFrob (v : Bool × Bool) : Bool × Bool :=
  (f2add v.1 v.2, v.2)

def Fixed (T : Bool × Bool → Bool × Bool) (v : Bool × Bool) : Prop :=
  T v = v

theorem id_fixes_all (v : Bool × Bool) :
    Fixed idFrob v := by
  rfl

theorem unipotent_fixed_iff_second_zero (v : Bool × Bool) :
    Fixed unipotentFrob v ↔ v.2 = false := by
  cases v with
  | mk x y =>
      cases x <;> cases y <;> simp [Fixed, unipotentFrob, f2add]

theorem unipotent_not_identity :
    unipotentFrob (false, true) ≠ (false, true) := by
  decide

theorem unipotent_fixes_nonzero_line :
    Fixed unipotentFrob (true, false) := by
  simp [Fixed, unipotentFrob, f2add]

theorem unipotent_does_not_fix_transverse_vector :
    ¬ Fixed unipotentFrob (false, true) := by
  simp [Fixed, unipotentFrob, f2add]

end P24.TwoTorsionGate
