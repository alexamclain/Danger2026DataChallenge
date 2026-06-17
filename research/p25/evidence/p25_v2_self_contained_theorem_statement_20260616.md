# P25 v2 Self-Contained Theorem Statement

Updated: 2026-06-16

## Purpose

State the current H0/conductor-39 moonshot target in one self-contained page
for expert review. This page does not claim the missing theorem exists. It
fixes the exact finite product rows, the three accepted source-stage
presentations, and the nearby statements that remain repair or reject rows.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_self_contained_theorem_statement_gate.py
```

The gate returned `p25_v2_self_contained_theorem_statement_rows=1/1`.

## Ambient Data

```text
p = 10000000000000000000000013
k = 42
sqrt_floor = 3162277660168
level = 507
conductor = 39
lift_length = 13
support_period = 156
p mod 39 = 23
boundary = Norm_156(Y_507)
```

Let `E_r` denote the level-507 Yang/Siegel-unit factor indexed by
`r mod 507`. For each row below, define:

```text
R_m =
  prod_{a in P_m, k=0..12} E_{a+39k}^6
  /
  prod_{b in N_m, k=0..12} E_{b+39k}^6
```

Each row has 78 positive and 78 negative lifted factors, total support 156,
and Hilbert-90 boundary `Norm_156(Y_507)`.

## Exact Rows

```text
m = 1
constants = (3, 3, -3, -3)
P_1 = (7, 17, 23, 34, 37, 38)
N_1 = (4, 8, 10, 11, 20, 25)
sha256 = eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e

m = 2
constants = (-3, 3, 3, -3)
P_2 = (7, 14, 29, 34, 35, 37)
N_2 = (1, 8, 11, 16, 20, 22)
sha256 = 97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9

m = 4
constants = (-3, -3, 3, 3)
P_4 = (14, 19, 28, 29, 31, 35)
N_4 = (1, 2, 5, 16, 22, 32)
sha256 = 28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6

m = 8
constants = (3, -3, -3, 3)
P_8 = (17, 19, 23, 28, 31, 38)
N_8 = (2, 4, 5, 10, 25, 32)
sha256 = ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

H0 and conductor 39 are source languages for this same finite target family.
One normalized row is enough.

## Source Graph Form

Equivalently, the conductor-39 source side is one oriented edge of a
quotient-`C4` graph:

```text
H = (1,3,9)
odd vertices  = 2H=(2,5,6), 7H=(7,8,11)
even vertices = H=(1,3,9), 4H=(4,10,12)

m=1: 7H -> 4H
m=2: 7H -> H
m=4: 2H -> H
m=8: 2H -> 4H
```

The four rows are exactly the four oriented edges of this `K_{2,2}` graph.
The target is one edge, not a vertex, projection, quotient, diagonal, row
square, or all-four aggregate.

For an integer combination in the edge basis `(m1,m2,m4,m8)`, the boundary
scale is the coefficient sum. Coefficient sum `1` gives the right `W` boundary
scale, but a non-unit vector is still:

```text
one legal edge + nonzero boundary-zero lattice content
```

and remains repair unless a source supplies that boundary-zero value,
selector/orientation data, or the direct one-edge theorem.

## Accepted Source-Stage Exits

The preferred exit is:

```text
Arithmetic finite divisor/additive theorem
for one exact row R_m, m in {1,2,4,8},
with Hilbert-90 boundary (1 - Frob_p)H = Norm_156(Y_507),
and finite additive/value/basepoint/branch/telescoping data
that fixes the otherwise invisible F_p^* scalar.
```

The value-side exit is acceptable only in the sharper support-period form:

```text
Finite value theorem
for one exact row R_m, m in {1,2,4,8},
with support-period-156 branch/root/telescoping context
selecting one F_p value,
and boundary Norm_156(Y_507).
```

Either exit must come from an arithmetic source theorem. A finite product
payload, local computation, or source-legality certificate alone is not enough.

The character-language finite-theorem exit is acceptable only in the exact
selector form:

```text
Exact row R_m selected by exact row-antisymmetric C4_1 phase
and mixed tensor row sign,
with W boundary / Norm_156(Y_507),
and scalar-fixed finite divisor/additive theorem for the selected row.
```

## Stop Signs

These are not source-stage wins unless repaired into one accepted exit above:

```text
source legality only
boundary only
divisor class or up-to-scalar statement only
ambient period-780 value
degree-6 value without explicit F_p descent
projection, prime-axis, or proper-suborbit statement
exact quartic selector without finite theorem
coarse quartic phase, magnitude, quadratic data, or missing row sign
same-parity quartic phase
wrong orientation or missing reciprocal boundary sign
row-square, diagonal aggregate, or all-four aggregate only
non-unit W-boundary edge combination
finite payload with no arithmetic source theorem
local Koo-Shin / KSY source stack as written
```

## Downstream Boundary

Even a source-stage theorem hit is not yet a DANGER3 submission. It must still
be routed through:

```text
DANGER3 finite-identity / non-CM framing
same-j X_1(8112) bridge
practical X_1(16) A,xP16 payload
38 halving links or direct x0
official vpp.py verification
```

## Verified Counts

```text
evidence_markers_ok = 9/9
payload_rows_ok = 4/4
row_hashes_ok = 4/4
row_supports_ok = 4/4
accepted_exits_ok = 3/3
stop_signs_ok = 14/14
current_source_theorems = 0
submission_ready_rows = 0
p25_v2_self_contained_theorem_statement_rows=1/1
```

## Verdict

The shortest current expert ask is:

```text
Does a known arithmetic source theorem give either a scalar-fixed
divisor/additive identity, the equivalent exact C4_1 character-selected finite
theorem, or a support-period-156 value identity for one of the four exact rows
R_m above, with boundary Norm_156(Y_507)?
```

If yes, route the theorem to the extraction contract. If no, the best outcome
is a sharp falsifier for this exact statement, not another broad source reread.
