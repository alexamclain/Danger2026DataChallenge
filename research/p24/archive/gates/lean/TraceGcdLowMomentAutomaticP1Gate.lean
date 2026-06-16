/-!
Finite handoff for the automatic first low moment.

For a parent quotient period `Z_u` and child quotient periods `Y_{u+a v}`,
the first child power sum is tautologically

  P_1(u) = sum_v Y_{u+a v} = Z_u.

Thus the p24 low-moment selector's nominal `4 + 26 = 30` relative traces
include two values already carried by the selected parent chain.  The
producer still must construct the higher moments.
-/

namespace P24.TraceGcdLowMomentAutomaticP1Gate

structure ChildMomentLayer where
  nominalMomentCount : Nat
  firstMomentIsParent : Prop

def NontrivialMomentCount (layer : ChildMomentLayer) : Nat :=
  layer.nominalMomentCount - 1

def FirstMomentKnownFromParent (layer : ChildMomentLayer) : Prop :=
  layer.firstMomentIsParent

theorem first_moment_needs_no_extra_producer
    (layer : ChildMomentLayer)
    (h_p1 : FirstMomentKnownFromParent layer) :
    layer.firstMomentIsParent := by
  exact h_p1

def p24FirstLayer : ChildMomentLayer where
  nominalMomentCount := 4
  firstMomentIsParent := True

def p24SecondLayer : ChildMomentLayer where
  nominalMomentCount := 26
  firstMomentIsParent := True

def p24NominalSelectedPathMoments : Nat :=
  p24FirstLayer.nominalMomentCount + p24SecondLayer.nominalMomentCount

def p24NontrivialSelectedPathMoments : Nat :=
  NontrivialMomentCount p24FirstLayer +
  NontrivialMomentCount p24SecondLayer

theorem p24_nominal_selected_path_moments :
    p24NominalSelectedPathMoments = 30 := by
  decide

theorem p24_nontrivial_selected_path_moments :
    p24NontrivialSelectedPathMoments = 28 := by
  decide

end P24.TraceGcdLowMomentAutomaticP1Gate
