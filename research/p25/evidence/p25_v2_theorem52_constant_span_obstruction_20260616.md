# P25 v2 Theorem 5.2 Constant-Span Obstruction

Updated: 2026-06-16

## Purpose

Test the last natural Koo-Shin 2010 Theorem 5.2 repair after selector
rigidity: maybe some nontrivial product of powers of the four legal
conductor-39 rows becomes a constant-exponent product, so Theorem 5.2 could
control it.

This pass kills that repair.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_theorem52_constant_span_obstruction_gate.py
```

The gate returned `p25_v2_theorem52_constant_span_obstruction_rows=1/1`.

## Quotient-C4 Lattice

Normalize the four legal quotient-`C4` exponent patterns by dividing by `3`:

```text
m=1:  A = ( 1,  1, -1, -1)
m=2:  B = (-1,  1,  1, -1)
m=4: -A = (-1, -1,  1,  1)
m=8: -B = ( 1, -1, -1,  1)
```

The legal row span is therefore:

```text
xA + yB = (x-y, x+y, -x+y, -x-y)
```

For this vector to be constant, the first two coordinates force `y=0`, and
then the first and third coordinates force `x=0`.  Hence the only constant
vector in the integer span is the zero vector.

## Interpretation

Theorem 5.2 is still useful rigidity/root-descent context, but it does not
close the current p25 target in any of these ways:

```text
single legal row          -> nonconstant quotient-C4 pattern
product of legal rows     -> constant only when the product cancels trivially
prime-axis projection     -> loses mixed conductor-39 source
one-coset boundary repair -> boundary control, not legal source row
```

## Verdict

```text
legal_row_span_rank = 2
nonzero_constant_intersections = 0
zero_constant_intersections = 1
theorem52_helper_rows = 1
theorem52_direct_closer_rows = 0
next = finite value/divisor theorem for one legal row, not another
       Theorem 5.2 constant-product repair
```
