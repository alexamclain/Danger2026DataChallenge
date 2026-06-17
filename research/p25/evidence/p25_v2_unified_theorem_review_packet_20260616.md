# P25 v2 Unified Theorem Review Packet

Updated: 2026-06-16

## Purpose

Freeze the exact first-pass theorem statement in a form an expert can review
quickly.  This packet does not claim the missing theorem exists.  It states
what would count as progress, what is already saturated, and what should be
discarded without another broad reread.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`
- `evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md`
- `evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_additive_normalizer_source_scan_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_unified_theorem_review_packet_gate.py
```

The gate returned `p25_v2_unified_theorem_review_packet_rows=1/1`.

## Exact Target Rows

The first-pass theorem target is one of these four equivalent finite rows.
H0 and conductor 39 are source languages; the finite target family is shared.

```text
m=1
H0 source           = canonical_H0
conductor-39 source = legal_sparse_selector_0
constants           = (3, 3, -3, -3)
positive residues   = (7, 17, 23, 34, 37, 38)
negative residues   = (4, 8, 10, 11, 20, 25)
lifted product      = 78 positive / 78 negative Yang-fiber factors
boundary            = Norm_156(Y_507)

m=2
H0 source           = H0_translate
conductor-39 source = legal_sparse_selector_2
constants           = (-3, 3, 3, -3)
positive residues   = (7, 14, 29, 34, 35, 37)
negative residues   = (1, 8, 11, 16, 20, 22)
lifted product      = 78 positive / 78 negative Yang-fiber factors
boundary            = Norm_156(Y_507)

m=4
H0 source           = H0_translate
conductor-39 source = legal_sparse_selector_3
constants           = (-3, -3, 3, 3)
positive residues   = (14, 19, 28, 29, 31, 35)
negative residues   = (1, 2, 5, 16, 22, 32)
lifted product      = 78 positive / 78 negative Yang-fiber factors
boundary            = Norm_156(Y_507)

m=8
H0 source           = H0_translate
conductor-39 source = legal_sparse_selector_1
constants           = (3, -3, -3, 3)
positive residues   = (17, 19, 23, 28, 31, 38)
negative residues   = (2, 4, 5, 10, 25, 32)
lifted product      = 78 positive / 78 negative Yang-fiber factors
boundary            = Norm_156(Y_507)
```

## Accepted Theorem Shapes

The preferred closer is:

```text
Arithmetic finite divisor/additive identity
for one row m in {1,2,4,8}
with Hilbert-90 boundary
(1 - Frob_p)H = Norm_156(Y_507)
and scalar-fixing additive/value/basepoint/branch/telescoping data
```

The value-side closer is acceptable only in the sharper support-period form:

```text
Finite value identity
for one row m in {1,2,4,8}
with period-156 branch/root/telescoping context
and boundary Norm_156(Y_507)
```

If the theorem is stated in character/projector language, the accepted
finite-theorem shape is:

```text
W boundary / Norm_156(Y_507) boundary
+ exact row-antisymmetric C4_1 phase selecting one legal edge
+ mixed tensor row sign
+ oriented row / boundary-sign convention
+ arithmetic source theorem
+ scalar-fixed finite divisor/additive identity for the selected row
```

Selector data without the finite theorem is not enough. Coarse quartic phase,
quartic magnitude, quadratic data, or phase data without the mixed row sign is
still repair; reciprocal phase without boundary sign is repair; reciprocal
phase with the positive boundary is rejected; same-parity quartic phase is
rejected.

In each case the identity has to come from an arithmetic source theorem. A
finite computation or product payload without source provenance is not enough.
A divisor/H90 statement only up to an unspecified `F_p^*` scalar is also not
enough; the additive/value side must fix that scalar.

## Review Questions

1. Is there a known finite divisor/additive theorem for one legal support-156
   H0/conductor-39 product with `(1-Frob_p)H = Norm_156(Y_507)` and a
   scalar-fixed finite identity?
2. If the theorem is divisor/additive, what datum fixes the `F_p^*` scalar:
   finite additive value, basepoint, branch/root, or telescoping product?
3. Is there a period-156 value theorem with branch/root/telescoping control for
   the same product family, avoiding the ambient period-780 `mu_11` ambiguity?
4. If the theorem is stated in character/projector language, does it give the
   exact row-antisymmetric `C4_1` phase, mixed tensor row sign, and oriented
   row/boundary-sign convention, not just quartic magnitude, one sign,
   quadratic data, or reciprocal phase with the wrong boundary?
5. Would H0/H0-translate language or mixed `U_chi/W` conductor-39 language make
   the same finite theorem cheaper to prove?
6. If the theorem is class-field or unit-theoretic, can it be framed as a finite
   non-CM identity acceptable for DANGER3 extraction?

## Stop Signs

These are not progress by themselves:

```text
source legality only:
  Koo-Shin/Yang source or unit-generation theorem without value/divisor content

boundary only:
  Hilbert-90 or Norm_156 boundary without an identity for one legal row

divisor class or up-to-scalar only:
  principal-divisor, divisor-class, dense additive relation, or value statement
  that leaves the F_p^* scalar unspecified

ambient value only:
  period-780 value theorem without period-156 branch/root/telescoping context

mu11 quotient only:
  ambient-period-780 value theorem only after taking an 11th power or
  quotienting by mu_11; still missing one selected F_p value

projection or suborbit:
  prime-axis projection, one-coset gauge, or proper doubling suborbit

quartic selector only:
  exact C4_1 selector or edge phase data without a scalar-fixed finite theorem

coarse quartic or missing row sign:
  one quartic sign, quartic magnitude, quadratic component, or quotient-C4
  phase without mixed tensor row sign

reciprocal quartic phase with wrong boundary:
  reciprocal C4_1 phase without boundary-sign convention, or reciprocal phase
  asserted with positive Norm_156(Y_507) boundary; needs oriented row data or
  reciprocal -Norm_156(Y_507) boundary

same-parity quartic phase:
  same-parity quartic edge or phase data; zero W boundary or wrong mixed tensor
  target

theorem52 constant-span repair:
  Koo-Shin 5.2 constant-product repair by multiplying legal rows; legal
  quotient-C4 span has no nonzero constant-exponent vector

finite payload only:
  local finite product computation with no arithmetic source theorem

local source stack as written:
  Koo-Shin 2010, KSY 1007.2307, and Koo-Shin II local extracts contain helper
  vocabulary but no scalar-fixing additive normalizer for the current row
```

## Downstream Boundary

An accepted source theorem would be a real first-pass theorem win, but it would
not yet be a DANGER3 submission.  The downstream ladder would still be:

```text
DANGER3 finite-identity / non-CM framing
same-j X_1(8112) bridge
practical X_1(16) A,xP16 payload
38 halving links or direct x0
official vpp.py verification
```

Current counts:

```text
accepted_source_stage_clauses = 6
current_source_theorems = 0
submission_ready_rows = 0
```

## Verdict

This is the compact expert ask:

```text
Find or rule out an arithmetic finite divisor/additive theorem, the equivalent
exact quartic-character finite theorem, or a period-156 value theorem with
branch/root/telescoping context, for one of the four legal support-156
H0/conductor-39 products above, with boundary Norm_156(Y_507). If the answer
is divisor/additive, identify the finite datum that fixes the F_p^* scalar.
```

Everything else is a support note unless it supplies that theorem, supplies the
post-theorem DANGER3 extraction, or gives a sharp falsifier for this exact
statement.
