# Trace-Frame Leading Plucker Pivot Theorem

Date: 2026-06-05

This note sharpens the selected Plucker certificate from an existential
coordinate choice to a canonical leading-prefix candidate after choosing the
trace-frame basis/order.  The intrinsic theorem remains the flag statement
`W_axis(B) cap F_27 = {0}`; the leading prefix is the named finite certificate
surface.

## p24 Candidate Coordinate

Keep the trace-frame setup:

```text
E = F_p(mu_m)
C/E has degree 179
B/C has degree 31
Top_3 : B -> C^3
dim_E W_axis = 368
```

Choose the normal `E`-basis of `C` produced by the trace-frame construction and
order coordinates by top coefficient block, then by the normal-basis coordinate
inside `C`.

The leading Plucker coordinate candidate is:

```text
I_lead = first 368 coordinates of C^3
       = all 179 coordinates of top block 1
       + all 179 coordinates of top block 2
       + first 10 coordinates of top block 3.
```

The sharpened selected-coordinate theorem candidate is:

```text
delta_lead = det coordinate_{I_lead}(Top_3(R_s)) != 0 in E
```

for every p24 H-packet, or equivalently the product of the eight packetwise
`delta_lead` values is a p-unit.

This is verifier-useful relative to the previous selected-coordinate
statement:
the verifier no longer has to search or name one of

```text
binom(537,368) ~= 10^143.820126
```

coordinates.  The coordinate is determined by the field tower and basis rule.

## Equivalent Kernel-Tail Form

The maximum-rank-profile statement predicts:

```text
rank Top_1(W_axis) = 179
rank Top_2(W_axis) = 358
rank Top_3(W_axis) = 368.
```

The leading coordinate theorem is the ordered, finite-coordinate refinement:

```text
1. the first top block has rank 179;
2. adding the second top block raises rank to 358;
3. the first 10 normal coordinates of the third top block separate the
   remaining 10-dimensional kernel.
```

Thus the hard p24 p-unit can be written as a product of pivot residuals:

```text
Delta_lead = B_1 * B_2 * T_10,
```

where `B_1` and `B_2` are full-block Moore/Schubert residuals and `T_10` is
the ten-coordinate tail determinant on `ker Top_2`.

This is now the smallest named determinant target inside the trace-frame
route.

The residual product is bookkeeping, not yet a proof of independent p-unit
factors.  The finite selected-origin statement is:

```text
Norm_{E/F_p}(delta_lead) != 0,
```

or the eight-packet decomposition-field product of these selected-origin
norms.

An origin-stable strengthening would take a beta product of the leading
determinants.  That is a stronger theorem: it proves the same coordinate works
for every beta translate of the embedded origin.

## Small Actual-CM Pivot Audit

I added:

```text
p24/trace_frame_plucker_pivot_audit.py
```

It computes the same trace-frame matrix on small tensor-factor CM rows and
records the deterministic pivot columns from row reduction.  It uses:

```text
top_count = ceil(raw_rank / subdegree)
```

which is the p24 rule `ceil(368/179)=3`.

Pinned axis row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_plucker_pivot_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --scan-origins --max-rows 40
```

reported:

```text
rows=40
full_top_rank_rows=40
top_rank_failure_rows=0

subdegree=2 top_count=3 blocks=[0,1,2] count=20
subdegree=3 top_count=2 blocks=[0,1]   count=20
```

In every displayed origin, the pivot columns were exactly the leading prefix:

```text
pivots=[0,1,2,3,4,5]
```

for the full-axis rows.

The component-plus-constant rows behaved the same way:

```text
target=constant_plus_4:
  rows=24
  full_top_rank_rows=24
  pivot columns always [0,1,2,3]

target=constant_plus_3:
  rows=24
  full_top_rank_rows=24
  pivot columns always [0,1,2]
```

This is still small-data evidence, not a proof.  Its value is that it names a
specific determinant consistent with the p24 split theorem.

## Residual-Value Audit

I added:

```text
p24/trace_frame_leading_residual_value_audit.py
```

It computes the actual leading determinant and Gaussian pivot products grouped
by top block.  On the same pinned full-axis row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_leading_residual_value_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --scan-origins --max-rows 24
```

reported:

```text
rows=24
nonzero_determinant_rows=24
zero_determinant_rows=0
determinants_in_base_field=0
determinant_norms_available=24
distinct_det_norms=2
zero_det_norms=0
```

The two determinant norms are exactly the two intermediate subdegree choices:

```text
subdegree=2, top_count=3: det_norm=11069 across tested origins
subdegree=3, top_count=2: det_norm=8644 across tested origins
```

The determinant itself does not descend to the base field in this toy; its
norm does.  The block residual norms were all nonzero but varied with origin,
so the reliable invariant surface is the norm of the full leading determinant,
not the separate residual factors.

There is an important caveat.  In the pinned `m=12` full-axis toy,

```text
raw_rank = tensor_factor_degree = 6.
```

So the full-axis leading determinant is a determinant of a full-space map; its
origin-stable norm can be dimension-forced by multiplication-by-`theta`
covariance.  This is not p24-shaped, because p24 has:

```text
raw_rank = 368 << tensor_factor_degree = 5549.
```

I therefore reran the same audit on lower-rank axis analogues from the same
CM row:

```text
m=4: raw_rank=4, tensor_factor_degree=6
m=3: raw_rank=3, tensor_factor_degree=6
```

Both had:

```text
rows=24
nonzero_determinant_rows=24
zero_det_norms=0
distinct_det_norms=24
```

This is closer to the p24 geometry and says not to expect the selected
leading-coordinate norm to be origin-invariant for free.

Component-plus-constant runs also had no zero determinant norms, but their
determinant norms varied across origins:

```text
constant_plus_4:
  rows=24, zero_det_norms=0, distinct_det_norms=24

constant_plus_3:
  rows=24, zero_det_norms=0, distinct_det_norms=24
```

This is a useful boundary: the full-axis coupling carries extra cancellation
or covariance in the dimension-forced toy, but the p24-shaped theorem must
still control a genuinely moving selected coordinate or prove its beta
product.

The alpha/beta separation is recorded in:

```text
p24/trace_frame_leading_origin_covariance.md
```

For p24, alpha shifts multiply the full-axis determinant by `(-1)^alpha`,
whose norm from `E` to `F_p` is `1`.  Beta shifts are the genuine arithmetic
content.

2026-06-08 D0 interpretation: the beta-zero factor is the unshifted leading
determinant in this same determinant line.  The pinned axis rerun with
`--target axis` gave `zero_block_products=0` in every displayed row, so the
toy D0 determinant factors through nonzero Gaussian block residuals.  The
individual block residual norms move with the origin, while the full
determinant norm is invariant only in the dimension-forced full-axis toy; the
lower-rank analogues do not have this free invariance.  Thus the useful p24
D0 target is:

```text
selected-origin prefix/block residual p-unit
+ determinant-line alpha transport by explicit p-units
=> D_0 is a p-unit.
```

This would discharge the beta-zero part of the four-element verifier
separately.  It does not touch the nonzero beta-orbit crossed norm, which
remains the deeper beta-shift theorem.

## Boundary

I tried a broader row scan, but stopped it after it spent time in Hilbert-root
setup without producing output.  The intended workflow is pinned structural
rows only, not broad CPU scanning.

The theorem gap is now:

```text
prove the selected-origin p24 leading-prefix trace-frame determinant
delta_lead has Norm_{E/F_p}(delta_lead) != 0 in each H-packet.
```

The most plausible proof shapes are:

```text
1. a selected-origin class-field norm identity for Norm_{E/F_p}(delta_lead)
   or its eight-packet product;
2. a residual-kernel theorem proving the first 10 third-block coordinates
   give a nonzero tail determinant on ker Top_2, while preserving the
   selected embedded phase;
3. a hidden block-equivalence to an MSRD/LRS code whose canonical generator
   basis is this leading trace-frame basis.
4. a stronger beta-product theorem proving all beta translates of the leading
   coordinate are p-units, at the cost of carrying the full H-phase product.
```

Random rank, generic Plucker support, and ordinary trace-coordinate recurrence
do not prove this.  The improvement is the named determinant surface.

## Residual-Tail Refinement

The leading determinant has a smaller failure object, recorded in:

```text
p24/trace_frame_residual_tail_frontier.md
p24/trace_frame_residual_tail_audit.py
```

After the first two top `C`-blocks, p24 should have:

```text
K_2 = W_axis cap F_28
dim_E K_2 = 10.
```

The intrinsic final step is that the third top coefficient

```text
b_28 : K_2 -> C
```

is injective.  The leading-prefix finite certificate is the stronger
Schubert-tail statement that the first ten normal-basis coordinates of
`b_28` already give an isomorphism:

```text
pi_10 o b_28 : K_2 -> E^10.
```

Equivalently, there is no nonzero axis weight `w` such that

```text
g'(theta)*x_w =
  q_0 + ... + q_27 theta^27 + c theta^28
```

with `c` supported only in the normal-basis tail
`span_E{nu_10,...,nu_178}`.  Small partial-tail tensor rows have no leading
tail failures and no proper Frobenius-stable residual image, so the likely
proof remains a selected-prime Schubert p-unit theorem rather than a hidden
subfield-invariance theorem.

## Lean Gate Status

No new Lean file is needed for this refinement.  The finite implication is
already covered by:

```text
p24/lean/TraceFrameGate.lean
p24/lean/TensorFactorProjectionGate.lean
p24/lean/ScalarExtensionGate.lean
```

A proof that the leading-prefix coordinate projection is injective on the
factor-projected axis rows feeds directly into those gates.  The missing work
is entirely arithmetic: proving `delta_lead` is nonzero at the selected prime.
