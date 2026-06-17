# P25 v2 Conductor-39 Yang/H90 Interface Contract

Updated: 2026-06-16

Marker: `p25_v2_conductor39_yang_h90_interface_contract_rows=1/1`

## Purpose

Promote the conductor-39 finite contract behind the first-pass theorem lane:
the mixed source object, its Yang lift to level 507, the Hilbert-90 boundary,
the sparse support-156 product normal form, and the first falsifiers for future
source-theorem hits.

This is not the missing value/divisor theorem. It is the compact target a
source theorem must hit.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `lanes/h0.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_20260614.md`

## Commands

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_coset_selector_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_conductor39_source_theorem_intake_gate.py
```

All seven gates returned their expected `rows=1/1` markers.

The lightweight v2 contract gate returned
`p25_v2_conductor39_yang_h90_interface_contract_rows=1/1`.

## Mixed Source Object

The primitive conductor-39 unit is genuinely mixed:

```text
U_chi = -chi_39 = -chi_3 * chi_13
support = 24
proper pushforward mod 3 = 0
proper pushforward mod 13 = 0
mod 3 pullback failure  = residues 1 and 7 have coefficients -1 and +1
mod 13 pullback failure = residues 1 and 14 have coefficients -1 and +1
additive separated = false
```

So a conductor-3, conductor-13, projection-only, pullback-only, or additive
separated explanation does not preserve the live object.

## Coset Selector

The same object has a compact cyclic coset quotient:

```text
level = 39
generator = 2
generator_order = 12
kernel <2> = (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)
coset 7<2> = (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)
U_chi = 1_{7<2>} - 1_{<2>}
p mod 39 = 23
Frob_p swaps the two cosets
Frob_p^2 preserves them
```

This is the cleanest source-level descriptor of the conductor-39 object.

## Frobenius And Hilbert-90 Boundary

The value route has a hard degree-6 cyclotomic constraint:

```text
ord_39(p) = 6
p^3 = -1 mod 39
primitive 39th roots first appear in degree 6
primitive 13th roots first appear in degree 6
primitive 3rd roots first appear in degree 2
Legendre(-39, p) = -1
```

Thus direct `F_p` shortcuts using primitive order-39 roots or `sqrt(-39)` are
invalid.

The conductor-39 word is an integral Hilbert-90 boundary:

```text
W = 6 * U_chi
W = (1 - Frob_p) V
balanced V support = 24, coefficients +/-3
sparse one-coset V support = 12, coefficients all +6 or all -6
```

The balanced half-character is the unique minimum `L_infty` gauge on each
Frobenius orbit, while sparse one-coset gauges minimize support.

## Sparse Yang Lift

The legal sparse Hilbert-90 gauges are the useful level-507 target:

```text
target_level = 507
lift_length = 13
support_period = 156
Norm_156(Y_507) support = 312, coefficients +/-6
legal sparse source support = 12, coefficients 6 positive and 6 negative
legal Yang lift support = 156, coefficients 78 positive and 78 negative
(1 - Frob_p) of each legal lift = Norm_156(Y_507)
```

There are four legal sparse selectors:

```text
constants = ( 3,  3, -3, -3)
constants = ( 3, -3, -3,  3)
constants = (-3,  3,  3, -3)
constants = (-3, -3,  3,  3)
```

Formal one-coset controls have the same boundary but fail the mixed-axis tests
because their mod-3 and mod-13 pushforwards are nonzero.

## Product Normal Form

The four legal support-156 potentials are one orbit under the doubling subgroup
`<2>` in `(Z/39Z)^*`:

```text
doubling_subgroup = (1, 2, 4, 8, 16, 32, 25, 11, 22, 5, 10, 20)
canonical_stabilizer = (1, 16, 22)
quotient_representatives = (1, 2, 4, 8)
```

Canonical product:

```text
positive residues = (7, 17, 23, 34, 37, 38)
negative residues = (4, 8, 10, 11, 20, 25)
lifted product = 78 positive Yang-fiber factors over 78 negative factors
boundary = Norm_156(Y_507)
```

The other three legal rows are its `<2>`-translates. This gives the current
best conductor-39 theorem target: a legal support-12 H90 selector, or the
canonical 78-over-78 Yang-fiber product, together with a finite value/divisor
theorem.

## Intake Classifier

The source-theorem intake classifier records the current decision ladder:

```text
snippet only                         -> reject: no theorem body
prime-axis projection                -> reject: loses mixed tensor
sparse one-coset without boundary    -> reject: formal gauge only
mixed unit without Yang lift         -> conditional: missing level-507 lift
mixed unit with Yang but no descent  -> conditional: missing H90/descent
mixed Yang/H90 source only           -> source identified, value/divisor theorem missing
finite value without period 156      -> conditional: missing period-156 context
divisor theorem without framing      -> source stage closed, DANGER3 framing missing
framed theorem without extraction    -> extraction missing
extracted unverified triple          -> official vpp.py missing
```

## Falsifiers

Reject a proposed conductor-39 theorem shape if its first output is any of:

```text
prime-axis projection or pullback
conductor-3-only or conductor-13-only source
additively separated mod-3/mod-13 explanation
formal one-coset sparse gauge without Hilbert-90 or ratio boundary
direct F_p primitive 39th-root or sqrt(-39) shortcut
value theorem without period-156 branch/root/telescoping context
norm-only statement without Frobenius anti-invariance or Hilbert-90 descent
source-stage theorem with no DANGER3 finite-identity framing
```

## Verdict

Conductor 39 remains live and is now sharply targetable:

```text
continue_conductor39 = yes
positive_artifact = mixed tensor + coset selector + sparse Yang/H90 product
still_missing = finite-field value/divisor theorem for the legal support-156
                H90/Yang product, plus DANGER3 framing and extraction
best_expert_ask = theorem for the canonical 78-over-78 Yang-fiber product, or
                  any <2>-translate, with (1-Frob_p) boundary equal to
                  Norm_156(Y_507)
```

## Recommendation

Ask source experts for a legal sparse Hilbert-90 potential or value/divisor
identity whose Yang lift is the support-156 period potential. Do not ask
broadly for conductor-39 facts; the finite target is now the canonical
78-over-78 product and its three doubling translates.
