# P25 v2 H0 / Conductor-39 Unified Target

Updated: 2026-06-16

## Purpose

Check whether the two first-pass theorem fronts, H0 and mixed conductor 39,
are genuinely separate finite theorem targets or two source languages for the
same support-156 Yang/Hilbert-90 product family.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`

## Command

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_h0_conductor39_unified_target_gate.py
```

The gate returned `p25_v2_h0_conductor39_unified_target_rows=1/1`.

## Result

The H0 legal products and the conductor-39 legal sparse Yang/H90 products are
the same four finite targets:

```text
support_period = 156
quotient_representatives = (1, 2, 4, 8)
canonical_stabilizer = (1, 16, 22)
```

Rows:

```text
m=1
H0 target = canonical_H0
conductor-39 selector = legal_sparse_selector_0
constants = (3, 3, -3, -3)
P = (7, 17, 23, 34, 37, 38)
N = (4, 8, 10, 11, 20, 25)
lift = +78 / -78
boundary = Norm_156(Y_507)

m=2
H0 target = H0_translate
conductor-39 selector = legal_sparse_selector_2
constants = (-3, 3, 3, -3)
P = (7, 14, 29, 34, 35, 37)
N = (1, 8, 11, 16, 20, 22)
lift = +78 / -78
boundary = Norm_156(Y_507)

m=4
H0 target = H0_translate
conductor-39 selector = legal_sparse_selector_3
constants = (-3, -3, 3, 3)
P = (14, 19, 28, 29, 31, 35)
N = (1, 2, 5, 16, 22, 32)
lift = +78 / -78
boundary = Norm_156(Y_507)

m=8
H0 target = H0_translate
conductor-39 selector = legal_sparse_selector_1
constants = (3, -3, -3, 3)
P = (17, 19, 23, 28, 31, 38)
N = (2, 4, 5, 10, 25, 32)
lift = +78 / -78
boundary = Norm_156(Y_507)
```

All four rows have:

```text
same H0 and conductor-39 finite product = yes
lifted support = 156
lifted product shape = 78 positive Yang-fiber factors over 78 negative factors
boundary equals Norm_156(Y_507) = yes
```

## Interpretation

H0 and conductor 39 remain distinct source languages:

```text
H0 language: exact legal H0/H0-translate product
conductor-39 language: mixed U_chi/W object preserving chi_3 tensor chi_13
```

But at the finite value/divisor level they collapse to the same target family.
The first-pass moonshot should therefore not count H0 and conductor 39 as two
independent finite theorem targets. They are two entrances to one theorem ask.

## Unified Ask

The narrow expert/source ask is now:

```text
Find an arithmetic finite value theorem or divisor/additive identity for one
of the four legal support-156, 78-over-78 Yang/Hilbert-90 products above,
with (1 - Frob_p) boundary equal to Norm_156(Y_507), preferably with
period-156 branch/root/telescoping context if the output is value-level.
```

Equivalent source presentations are acceptable if they preserve either:

```text
H0 / H0-translate legality
```

or:

```text
mixed conductor-39 U_chi/W structure with chi_3 tensor chi_13 preserved
```

The downstream requirements remain unchanged: DANGER3 framing, same-`j`
`X_1(8112)` bridge, `X_1(16)` extraction, halving, and official `vpp.py`.

## Verdict

```text
continue_first_pass = yes
frontier_shape = one finite target family with two source languages
positive_artifact = unified four-row support-156 product target
still_missing = finite value/divisor theorem, then DANGER3 extraction
discard_condition = any proposed H0/conductor-39 result that does not hit one
                    of these four rows or lacks the Norm_156(Y_507) boundary
```
