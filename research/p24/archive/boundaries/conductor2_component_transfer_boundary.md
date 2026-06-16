# Conductor-2 Component Transfer Boundary

The conductor-2/nonsplit gate clarifies the final DANGER3 branch, but it does
not by itself construct the embedded odd-prime component quotient.

## Toy Transfer

I added:

```text
p24/conductor2_component_transfer_toy.py
```

For the `p=103`, `t=8`, `D=-87`, `ell=7` calibration:

```text
max_roots=[5, 29, 32, 43, 60, 70]
conductor2_roots=[4, 44, 62, 63, 85, 86]
max_component_sizes=[3]
conductor2_component_sizes=[3]
vertical_down_degrees=[1]
max_cycle_sums=[4, 29]
conductor2_cycle_sums=[50, 88]
down_image_component_indices=[(1,), (0,)]
paired_max_to_conductor2_sums=[(4, 88), (29, 50)]
sum_sets_equal=0
```

The descending `2`-isogeny gives an equivariant bijection from the maximal
surface roots to the conductor-2 floor roots, and sends each `ell`-component
to one `ell`-component.  But the embedded period values change.  The
conductor-2 cycle sums are not the same quotient values as the maximal cycle
sums.

## Bounded Scan

I generalized this in:

```text
p24/conductor2_component_transfer_scan.py
```

Bounded run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/conductor2_component_transfer_scan.py \
  --max-p 700 --max-h 30 --max-ell 17 --max-rows 20
```

Output summary:

```text
rows=20
all_equivariant=1
rows_with_same_sum_set=0
```

Rows included component counts `2` and `3` and component sizes `3`, `4`, `5`,
`6`, and `7`.  In every row, the vertical map preserved the component
partition, but the conductor-2 component-sum set differed from the maximal
component-sum set.

## Interpretation

This supports the expected volcano/class-field picture:

```text
Pic(Z+2O_K) ~= Pic(O_K)
```

transports the odd-prime class action, and the descending `2`-isogeny realizes
that transport on embedded roots.  However, constructing the transported
component sums still requires the embedded roots or an equivalent identity.

So the conductor-2 branch fixes the final verifier target, but it does not
lower the class-field selection problem.  The p24 `ell=677` theorem still has
to construct the `314` conductor-2 component sums over `F_p` without first
enumerating the `205880396014` roots.

The remaining possible escape hatch would be a formula that computes the
image-period sums under the descending `2`-isogeny from a smaller set of
maximal-order component invariants.  These scans rule out the simplest
collapse, namely equality of component-sum quotients or component-blind
vertical transfer.
