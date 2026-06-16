# P25 Lane B: Robert KSY Kubert-Lang Anti-Invariant Source Boundary

Updated: 2026-06-13 17:30 PDT

## Purpose

The anti-invariant producer contract is now the exact theorem target:

```text
C = (47,28)
D = (22,3)
K = (57,0), primitive trace
orientation = forward or reverse
```

This gate maps the current source families to that contract.

## Continue

```text
Sprang/Kronecker D=2
  Continue only if it emits the exact product over A=C+jD+kK,
  or exact theta2/theta2^-1 data with period-156 telescoping context.

Kubert-Lang exact exponent matrix
  Continue only as an exact matrix search for the six quotient cells,
  the derived factor word, or the 300-term theta2 payload.

Koo-Shin-Yoon normalized y / wp-prime
  Continue because the target is literally a normalized-y anti-invariant
  product, but generic ray-class generation is not enough.
```

## Conditional

```text
Siegel-Robert value units
  Continue only with explicit branch/root control or period-156 fixedness,
  or if the theorem outputs divisor/additive theta2 data directly.
```

## Kill

```text
ordinary Kato theta_D direct proof
literal Robert subgroup/coset support
raw KL exponent balance alone
nonuniform weighted product variants
```

The raw KL-only route is killed because missing `K`, collapsed `K`, truncated
`D`, wrong `D`, and shifted center all pass raw exponent sums.

The weighted-product route is killed because D-slice and atomic support
read-off force equal weights on all `75` atoms.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_rows=1/1
```

## Next Probe

Instantiate one of:

```text
D=2 Kronecker / KSY normalized-y formula
exact Kubert-Lang exponent matrix
```

Then run the result through:

```text
p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate.py
```

No broad literature reread is needed for this lane.
