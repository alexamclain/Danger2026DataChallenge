/-!
Finite gate for the denominator-safe prefix plus selected-tail crossed package.

The selected-tail determinant is proof-facing, but it is only denominator-safe
after the prefix chart has been certified.  The finite package is therefore:

* prefix Schubert factors A, B, AB are p-units for every beta packet;
* selected-tail crossed-product reduced norms rule out the tail bad event
  for every beta packet;
* prefix good plus no selected-tail bad event gives the trace-frame
  certificate.

This file proves only that finite implication.  The p-integral construction
of the prefix sections and selected-tail crossed norms is the missing
arithmetic theorem.
-/

namespace P24.TraceFramePrefixTailCrossedPackageGate

structure PrefixDeltas (Scalar Beta : Type) where
  deltaA : Beta → Scalar
  deltaB : Beta → Scalar
  deltaAB : Beta → Scalar

structure PrefixNorms (Scalar : Type) where
  xiA : Scalar
  xiB : Scalar
  xiAB : Scalar

def PrefixGood {Scalar Beta : Type} [Zero Scalar]
    (deltas : PrefixDeltas Scalar Beta)
    (beta : Beta) : Prop :=
  deltas.deltaA beta ≠ 0 ∧
  deltas.deltaB beta ≠ 0 ∧
  deltas.deltaAB beta ≠ 0

def ReducedNormMatchesProduct {Orbit Scalar : Type}
    (reducedNorm orbitProduct : Orbit → Scalar) : Prop :=
  ∀ orbit, reducedNorm orbit = orbitProduct orbit

def TailBadForcesOrbitProductZero {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (TailBad : Beta → Prop)
    (orbitProduct : Orbit → Scalar) : Prop :=
  ∀ beta, TailBad beta → orbitProduct (orbitOf beta) = 0

theorem prefix_good_from_global_norms
    {Scalar Beta : Type} [Zero Scalar]
    (deltas : PrefixDeltas Scalar Beta)
    (norms : PrefixNorms Scalar)
    (h_any_zero_A :
      (∃ beta, deltas.deltaA beta = 0) → norms.xiA = 0)
    (h_any_zero_B :
      (∃ beta, deltas.deltaB beta = 0) → norms.xiB = 0)
    (h_any_zero_AB :
      (∃ beta, deltas.deltaAB beta = 0) → norms.xiAB = 0)
    (h_xiA : norms.xiA ≠ 0)
    (h_xiB : norms.xiB ≠ 0)
    (h_xiAB : norms.xiAB ≠ 0) :
    ∀ beta, PrefixGood deltas beta := by
  intro beta
  refine ⟨?_, ?_, ?_⟩
  · intro h_zero
    exact h_xiA (h_any_zero_A ⟨beta, h_zero⟩)
  · intro h_zero
    exact h_xiB (h_any_zero_B ⟨beta, h_zero⟩)
  · intro h_zero
    exact h_xiAB (h_any_zero_AB ⟨beta, h_zero⟩)

theorem orbit_product_nonzero_from_reduced_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm orbitProduct : Orbit → Scalar)
    (orbit : Orbit)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_norm_nonzero : reducedNorm orbit ≠ 0) :
    orbitProduct orbit ≠ 0 := by
  intro h_zero
  exact h_norm_nonzero (by
    rw [h_match orbit, h_zero])

theorem no_tail_bad_from_reduced_norms
    {Beta Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (TailBad : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_tail_zero :
      TailBadForcesOrbitProductZero orbitOf TailBad orbitProduct)
    (h_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0) :
    ∀ beta, ¬ TailBad beta := by
  intro beta h_bad
  have h_orbit_nonzero :
      orbitProduct (orbitOf beta) ≠ 0 :=
    orbit_product_nonzero_from_reduced_norm
      reducedNorm orbitProduct (orbitOf beta) h_match
      (h_norms_nonzero (orbitOf beta))
  exact h_orbit_nonzero (h_tail_zero beta h_bad)

theorem reduced_norms_nonzero_from_global_norm
    {Orbit Scalar : Type} [Zero Scalar]
    (reducedNorm : Orbit → Scalar)
    (globalNorm : Scalar)
    (h_any_zero :
      (∃ orbit, reducedNorm orbit = 0) → globalNorm = 0)
    (h_global_nonzero : globalNorm ≠ 0) :
    ∀ orbit, reducedNorm orbit ≠ 0 := by
  intro orbit h_zero
  exact h_global_nonzero (h_any_zero ⟨orbit, h_zero⟩)

theorem all_trace_frames_good_from_prefix_and_tail
    {Scalar Beta : Type} [Zero Scalar]
    (deltas : PrefixDeltas Scalar Beta)
    (TailBad TraceFrameGood : Beta → Prop)
    (h_prefix_tail_trace :
      ∀ beta, PrefixGood deltas beta → ¬ TailBad beta → TraceFrameGood beta)
    (h_prefix_good : ∀ beta, PrefixGood deltas beta)
    (h_no_tail_bad : ∀ beta, ¬ TailBad beta) :
    ∀ beta, TraceFrameGood beta := by
  intro beta
  exact h_prefix_tail_trace beta (h_prefix_good beta) (h_no_tail_bad beta)

theorem no_harmful_from_prefix_norms_and_tail_reduced_norms
    {Scalar Beta Orbit : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (deltas : PrefixDeltas Scalar Beta)
    (prefixNorms : PrefixNorms Scalar)
    (TailBad TraceFrameGood Harmful : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (h_prefix_tail_trace :
      ∀ beta, PrefixGood deltas beta → ¬ TailBad beta → TraceFrameGood beta)
    (h_trace_no_harmful :
      ∀ beta, TraceFrameGood beta → ¬ Harmful beta)
    (h_any_zero_A :
      (∃ beta, deltas.deltaA beta = 0) → prefixNorms.xiA = 0)
    (h_any_zero_B :
      (∃ beta, deltas.deltaB beta = 0) → prefixNorms.xiB = 0)
    (h_any_zero_AB :
      (∃ beta, deltas.deltaAB beta = 0) → prefixNorms.xiAB = 0)
    (h_xiA : prefixNorms.xiA ≠ 0)
    (h_xiB : prefixNorms.xiB ≠ 0)
    (h_xiAB : prefixNorms.xiAB ≠ 0)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_tail_zero :
      TailBadForcesOrbitProductZero orbitOf TailBad orbitProduct)
    (h_tail_norms_nonzero :
      ∀ orbit, reducedNorm orbit ≠ 0) :
    ∀ beta, ¬ Harmful beta := by
  intro beta
  apply h_trace_no_harmful
  apply all_trace_frames_good_from_prefix_and_tail
    deltas TailBad TraceFrameGood h_prefix_tail_trace
  · exact prefix_good_from_global_norms
      deltas prefixNorms h_any_zero_A h_any_zero_B h_any_zero_AB
      h_xiA h_xiB h_xiAB
  · exact no_tail_bad_from_reduced_norms
      orbitOf TailBad reducedNorm orbitProduct h_match
      h_tail_zero h_tail_norms_nonzero

theorem no_harmful_from_prefix_norms_and_global_tail_norm
    {Scalar Beta Orbit : Type} [Zero Scalar]
    (orbitOf : Beta → Orbit)
    (deltas : PrefixDeltas Scalar Beta)
    (prefixNorms : PrefixNorms Scalar)
    (TailBad TraceFrameGood Harmful : Beta → Prop)
    (reducedNorm orbitProduct : Orbit → Scalar)
    (tailGlobalNorm : Scalar)
    (h_prefix_tail_trace :
      ∀ beta, PrefixGood deltas beta → ¬ TailBad beta → TraceFrameGood beta)
    (h_trace_no_harmful :
      ∀ beta, TraceFrameGood beta → ¬ Harmful beta)
    (h_any_zero_A :
      (∃ beta, deltas.deltaA beta = 0) → prefixNorms.xiA = 0)
    (h_any_zero_B :
      (∃ beta, deltas.deltaB beta = 0) → prefixNorms.xiB = 0)
    (h_any_zero_AB :
      (∃ beta, deltas.deltaAB beta = 0) → prefixNorms.xiAB = 0)
    (h_xiA : prefixNorms.xiA ≠ 0)
    (h_xiB : prefixNorms.xiB ≠ 0)
    (h_xiAB : prefixNorms.xiAB ≠ 0)
    (h_match : ReducedNormMatchesProduct reducedNorm orbitProduct)
    (h_tail_zero :
      TailBadForcesOrbitProductZero orbitOf TailBad orbitProduct)
    (h_any_tail_norm_zero :
      (∃ orbit, reducedNorm orbit = 0) → tailGlobalNorm = 0)
    (h_tail_global_nonzero :
      tailGlobalNorm ≠ 0) :
    ∀ beta, ¬ Harmful beta :=
  no_harmful_from_prefix_norms_and_tail_reduced_norms
    orbitOf deltas prefixNorms TailBad TraceFrameGood Harmful
    reducedNorm orbitProduct
    h_prefix_tail_trace h_trace_no_harmful
    h_any_zero_A h_any_zero_B h_any_zero_AB
    h_xiA h_xiB h_xiAB
    h_match h_tail_zero
    (reduced_norms_nonzero_from_global_norm
      reducedNorm tailGlobalNorm h_any_tail_norm_zero
      h_tail_global_nonzero)

theorem p24_prefix_tail_package_subsqrt :
    4 < 1000000000000 := by
  decide

theorem p24_tensor_orbit_package_subsqrt :
    560 < 1000000000000 := by
  decide

end P24.TraceFramePrefixTailCrossedPackageGate
