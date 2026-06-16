# P25 KSY-y Atom Enumeration Falsifier

Updated: 2026-06-14 22:12 PDT

## Purpose

This note turns the `75 atoms` clarification into an operational router.

The KSY-y target has 75 fixed normalized-y atoms:

```text
Q = C + jD + kK
j = -1,0,1
k = 0..24
```

They are fixed factors in one product, not 75 candidate tries.  The accepted
finite geometry forces the full equal-weight product; after that, DANGER3 still
needs challenge-legal framing, cross-level extraction, and official `vpp.py`.

## Dependencies

```text
ksy_y_atom_terminology_guardrail_rows=1/1
robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows=1/1
ksy_y_cross_level_extraction_gap_rows=1/1
```

## Invariants

```text
atom_count = 75
atoms_are_search_candidates = 0
footprint_terms = 300
atomic_nullity = 0
missing_atom_rejected = 1
nonuniform_weights_rejected = 1
```

The rigidity input says each atom has disjoint normalized-y footprint support,
so the exact theta2/theta2-inverse target reads off every atom weight.  There is
no hidden null direction where a subset or nonuniform weighted product can
quietly replace the all-75 product.

## Router Rows

```text
literal_75_tries_plan:
  decision = reject_atom_enumeration_not_a_route
  missing  = 75 atoms are fixed product factors, not 75 candidate tries

single_atom_payload:
  decision = reject_missing_or_extra_atom_count
  missing  = exact theta2 payload forces all 75 fixed atoms

seventy_four_atom_subset:
  decision = reject_missing_or_extra_atom_count
  missing  = exact theta2 payload forces all 75 fixed atoms

nonuniform_all75_weights:
  decision = reject_nonuniform_atom_weights
  missing  = atomic-weight rigidity has nullity 0

all75_orientation_missing:
  decision = all75_product_orientation_missing
  missing  = theta2/theta2^-1 orientation

all75_identity_missing:
  decision = all75_product_identity_missing
  missing  = finite arithmetic identity selecting the all-75 product

all75_framing_missing:
  decision = all75_product_framing_missing
  missing  = challenge-legal non-CM/finite-field framing

all75_source_closed_extraction_missing:
  decision = source_closed_cross_level_extraction_missing
  missing  = same-j X_1(8112) bridge, X_1(16) payload, or concrete triple

all75_extraction_ready_vpp_missing:
  decision = extraction_ready_official_vpp_missing
  missing  = official DANGER3 vpp.py stdout True

official_vpp_verified_boundary:
  decision = submission_ready_after_official_vpp
  missing  = none
```

## Counts

```text
row_count = 10
rejected_rows = 4
theorem_missing_rows = 2
source_stage_closed_rows = 3
extraction_ready_rows = 2
submission_ready_rows = 1
current_submission_ready_rows = 0
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_atom_enumeration_falsifier_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_atom_enumeration_falsifier_gate.py
```

Marker:

```text
ksy_y_atom_enumeration_falsifier_rows=1/1
```

## Interpretation

A future lane should not spend time trying the 75 atoms as separate candidates.
The only live use of the atom structure is an all-75 equal-weight product
identity, or an exactly equivalent finite payload, followed by legal framing,
cross-level extraction, and official DANGER3 verification.
