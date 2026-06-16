/-!
Finite gate for the orbitwise Schur/Gram bridge in the trace-GCD route.

The arithmetic theorem may prove trace-GCD nonvanishing through Gram products:

    L_O * K_O = P_O * Pi_O^2

where `Pi_O` is the trace-GCD orbit product, `L_O` is the full leading Gram
orbit product, `K_O` is the kernel Gram orbit product, and `P_O` is the prefix
Gram orbit product.  Lean does not prove the determinant identity or any
p-adic unit statement.  It records the finite zero-detection logic:

* if a zero trace-GCD orbit product would force a zero full/kernel Gram
  product,
* the full Gram product is a unit, and
* either the kernel Gram product is a unit directly or prefix Gram
  nondegeneracy forces kernel Gram nondegeneracy,
* then every trace-GCD orbit product is nonzero.

Together with the usual orbit-product zero-detection for local determinant
values, this implies the selected trace-GCD row is good.
-/

namespace P24.TraceGcdSchurBridgeGate

def UnitPayload {Index Scalar : Type}
    (value inverse : Index → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  ∀ i, UnitRel (value i) (inverse i)

def ConservativeGramPayload {Orbit Scalar : Type}
    (prefixGram prefixGramInv : Orbit → Scalar)
    (fullGram fullGramInv : Orbit → Scalar)
    (kernelGram kernelGramInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop) : Prop :=
  UnitPayload prefixGram prefixGramInv UnitRel
  ∧ UnitPayload fullGram fullGramInv UnitRel
  ∧ UnitPayload kernelGram kernelGramInv UnitRel

def SchurZeroDetection {Orbit Scalar : Type} [Zero Scalar]
    (tailProduct fullGram kernelGram : Orbit → Scalar) : Prop :=
  ∀ orbit, tailProduct orbit = 0 →
    fullGram orbit = 0 ∨ kernelGram orbit = 0

def PrefixGramDetectsKernelNonzero {Orbit Scalar : Type} [Zero Scalar]
    (prefixGram kernelGram : Orbit → Scalar) : Prop :=
  ∀ orbit, prefixGram orbit ≠ 0 → kernelGram orbit ≠ 0

theorem tail_products_nonzero_from_schur_units
    {Orbit Scalar : Type} [Zero Scalar]
    (tailProduct fullGram fullGramInv kernelGram kernelGramInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel)
    (h_kernel_units :
      UnitPayload kernelGram kernelGramInv UnitRel) :
    ∀ orbit, tailProduct orbit ≠ 0 := by
  intro orbit h_tail_zero
  rcases h_schur orbit h_tail_zero with h_full_zero | h_kernel_zero
  · have h_full_nonzero : fullGram orbit ≠ 0 :=
      h_unit_nonzero (fullGram orbit) (fullGramInv orbit)
        (h_full_units orbit)
    exact h_full_nonzero h_full_zero
  · have h_kernel_nonzero : kernelGram orbit ≠ 0 :=
      h_unit_nonzero (kernelGram orbit) (kernelGramInv orbit)
        (h_kernel_units orbit)
    exact h_kernel_nonzero h_kernel_zero

theorem tail_products_nonzero_from_conservative_gram_payload
    {Orbit Scalar : Type} [Zero Scalar]
    (tailProduct : Orbit → Scalar)
    (prefixGram prefixGramInv : Orbit → Scalar)
    (fullGram fullGramInv : Orbit → Scalar)
    (kernelGram kernelGramInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_payload :
      ConservativeGramPayload prefixGram prefixGramInv
        fullGram fullGramInv kernelGram kernelGramInv UnitRel) :
    ∀ orbit, tailProduct orbit ≠ 0 := by
  rcases h_payload with ⟨_h_prefix, h_full, h_kernel⟩
  exact tail_products_nonzero_from_schur_units
    tailProduct fullGram fullGramInv kernelGram kernelGramInv UnitRel
    h_unit_nonzero h_schur h_full h_kernel

theorem tail_products_nonzero_from_prefix_full_gram_units
    {Orbit Scalar : Type} [Zero Scalar]
    (tailProduct prefixGram prefixGramInv fullGram fullGramInv
      kernelGram : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_prefix_to_kernel :
      PrefixGramDetectsKernelNonzero prefixGram kernelGram)
    (h_prefix_units :
      UnitPayload prefixGram prefixGramInv UnitRel)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel) :
    ∀ orbit, tailProduct orbit ≠ 0 := by
  intro orbit h_tail_zero
  rcases h_schur orbit h_tail_zero with h_full_zero | h_kernel_zero
  · have h_full_nonzero : fullGram orbit ≠ 0 :=
      h_unit_nonzero (fullGram orbit) (fullGramInv orbit)
        (h_full_units orbit)
    exact h_full_nonzero h_full_zero
  · have h_prefix_nonzero : prefixGram orbit ≠ 0 :=
      h_unit_nonzero (prefixGram orbit) (prefixGramInv orbit)
        (h_prefix_units orbit)
    have h_kernel_nonzero : kernelGram orbit ≠ 0 :=
      h_prefix_to_kernel orbit h_prefix_nonzero
    exact h_kernel_nonzero h_kernel_zero

def OrbitProductZeroOnValueZero {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (tailProduct : Orbit → Scalar) : Prop :=
  ∀ t, Delta t = 0 → tailProduct (orbitOf t) = 0

theorem values_nonzero_from_schur_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (tailProduct fullGram fullGramInv kernelGram kernelGramInv : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_tail_zero :
      OrbitProductZeroOnValueZero orbitOf Delta tailProduct)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel)
    (h_kernel_units :
      UnitPayload kernelGram kernelGramInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_tail_nonzero : tailProduct (orbitOf t) ≠ 0 :=
    tail_products_nonzero_from_schur_units
      tailProduct fullGram fullGramInv kernelGram kernelGramInv UnitRel
      h_unit_nonzero h_schur h_full_units h_kernel_units (orbitOf t)
  exact h_tail_nonzero (h_tail_zero t h_delta_zero)

theorem values_nonzero_from_prefix_full_gram_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (tailProduct prefixGram prefixGramInv fullGram fullGramInv
      kernelGram : Orbit → Scalar)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_prefix_to_kernel :
      PrefixGramDetectsKernelNonzero prefixGram kernelGram)
    (h_tail_zero :
      OrbitProductZeroOnValueZero orbitOf Delta tailProduct)
    (h_prefix_units :
      UnitPayload prefixGram prefixGramInv UnitRel)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel) :
    ∀ t, Delta t ≠ 0 := by
  intro t h_delta_zero
  have h_tail_nonzero : tailProduct (orbitOf t) ≠ 0 :=
    tail_products_nonzero_from_prefix_full_gram_units
      tailProduct prefixGram prefixGramInv fullGram fullGramInv
      kernelGram UnitRel h_unit_nonzero h_schur h_prefix_to_kernel
      h_prefix_units h_full_units (orbitOf t)
  exact h_tail_nonzero (h_tail_zero t h_delta_zero)

theorem selected_good_from_schur_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (tailProduct fullGram fullGramInv kernelGram kernelGramInv : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_tail_zero :
      OrbitProductZeroOnValueZero orbitOf Delta tailProduct)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel)
    (h_kernel_units :
      UnitPayload kernelGram kernelGramInv UnitRel)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_delta_to_good selected
    (values_nonzero_from_schur_units orbitOf Delta tailProduct
      fullGram fullGramInv kernelGram kernelGramInv UnitRel
      h_unit_nonzero h_schur h_tail_zero h_full_units h_kernel_units selected)

theorem selected_good_from_prefix_full_gram_units
    {Index Orbit Scalar : Type} [Zero Scalar]
    (orbitOf : Index → Orbit)
    (Delta : Index → Scalar)
    (tailProduct prefixGram prefixGramInv fullGram fullGramInv
      kernelGram : Orbit → Scalar)
    (Good : Index → Prop)
    (selected : Index)
    (UnitRel : Scalar → Scalar → Prop)
    (h_unit_nonzero :
      ∀ value inverse, UnitRel value inverse → value ≠ 0)
    (h_schur :
      SchurZeroDetection tailProduct fullGram kernelGram)
    (h_prefix_to_kernel :
      PrefixGramDetectsKernelNonzero prefixGram kernelGram)
    (h_tail_zero :
      OrbitProductZeroOnValueZero orbitOf Delta tailProduct)
    (h_prefix_units :
      UnitPayload prefixGram prefixGramInv UnitRel)
    (h_full_units :
      UnitPayload fullGram fullGramInv UnitRel)
    (h_delta_to_good : ∀ t, Delta t ≠ 0 → Good t) :
    Good selected := by
  exact h_delta_to_good selected
    (values_nonzero_from_prefix_full_gram_units orbitOf Delta tailProduct
      prefixGram prefixGramInv fullGram fullGramInv kernelGram UnitRel
      h_unit_nonzero h_schur h_prefix_to_kernel h_tail_zero h_prefix_units
      h_full_units selected)

theorem p24_minimal_schur_payload_count :
    2 * 2 * 7 = 28 := by
  decide

theorem p24_conservative_schur_payload_count :
    2 * 3 * 7 = 42 := by
  decide

end P24.TraceGcdSchurBridgeGate
