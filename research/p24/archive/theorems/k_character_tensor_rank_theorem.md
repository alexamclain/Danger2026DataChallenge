# K-Character Tensor Rank Theorem Target

This note records the corrected K-character route after the packet-Frobenius
cocycle audit.

## Tensor Accounting

I added:

```text
p24/tensor_decomposition_accounting.py
```

For the p24 third trace it reports:

```text
m = 66254 = 2 * 157 * 211
n = 3107441
ord_n(p) = 388430
ord_m(p) = 5460
gcd(ord_n(p), ord_m(p)) = 70
lcm(ord_n(p), ord_m(p)) = 30297540
```

Let

```text
A_a = F_p[X]/(f_a),        deg(f_a)=388430
E   = F_p(mu_m),           [E:F_p]=5460.
```

Then

```text
A_a tensor_{F_p} E ~= product_{70} B_i,
```

where each `B_i/E` has degree

```text
388430 / 70 = 5549.
```

Over `E`, all K-character roots are available and fixed by E-Frobenius:

```text
axis_orbits_under_E_Frobenius_on_K:
  constant: {1: 1}
  2:        {1: 1}
  157:      {1: 156}
  211:      {1: 210}
```

The H-packet still has internal orbit size:

```text
5549.
```

The same split also explains the beta-product orbit count in the trace-frame
route:

```text
(n-1)/ord_n(p^ord_m(p)) = 560 = 8 * 70.
```

So the `560` nonzero beta-orbit crossed-product factors are the `70`
scalar-extension factors inside each of the eight `F_p` H-packets.  This
bookkeeping bridge is recorded in:

```text
p24/beta_orbit_tensor_factor_bridge.md
```

The key dimension inequality is:

```text
5549 > dim(W_axis) = 368.
```

So one tensor factor has enough room to certify the entire axis map.

## Tensor-Rank Audit

I added:

```text
p24/k_character_tensor_rank_scan.py
```

It computes K-character resolvents over the tensor algebra

```text
A tensor F_q(mu_m) = F_q(mu_m)[X]/(f),
```

not by choosing a single embedding of `A` into a larger field.

Pinned rows:

```text
D=-8711, q=8747, h=132, m=12, n=11, deg=10, [E:F_q]=2
axis_rank=6/6, axis_character_rank=6/6, axis_zero=0
full_K_rank=10/12, full_K_character_rank=10/12, full_K_zero=0

D=-10919, q=11243, h=156, m=12, n=13, deg=12, [E:F_q]=2
axis_rank=6/6, axis_character_rank=6/6, axis_zero=0
full_K_rank=12/12, full_K_character_rank=12/12, full_K_zero=0
```

The `D=-8711` full-K rank is dimension-bound because `deg=10 < m=12`, but
the axis theorem is dimension-possible and full.

Broader small nonsplit tensor window:

```text
rows=30
extension_degree_histogram={2: 15, 3: 2, 4: 11, 5: 1, 6: 1}
axis_rank_mismatch_rows=0
full_k_rank_mismatch_rows=0
axis_dimension_possible_rows=5
axis_dimension_possible_failure_rows=0
axis_support_not_rank_rows=25
axis_dimension_possible_support_not_rank_rows=0
full_k_dimension_possible_rows=2
full_k_dimension_possible_failure_rows=0
```

This validates the tensor DFT implementation and repeats the earlier pattern:
rank failures seen so far are dimension-forced, not CM-structural.

## One-Factor Refinement

I added:

```text
p24/k_character_tensor_factor_rank_scan.py
```

This factors `f` over `E=F_q(mu_m)` and measures the axis-character rank
inside each irreducible tensor factor separately.

Pinned rows:

```text
D=-8711, q=8747, h=132, m=12, n=11
deg(f)=10, [E:F_q]=2, factors=2, factor_degree=5, axis_dim=6
tensor_rank=6
factor_ranks=[5,5]
full_factor_count=0
```

Here no single factor can carry full axis rank because `5 < 6`.

```text
D=-10919, q=11243, h=156, m=12, n=13
deg(f)=12, [E:F_q]=2, factors=2, factor_degree=6, axis_dim=6
tensor_rank=6
factor_ranks=[6,6]
full_factor_count=2
```

This is the small analogue of the p24 one-factor hope: each tensor factor has
exactly enough dimension and already certifies the full axis rank.

Small broader factor window:

```text
rows=20
tensor_factor_count_histogram={2: 20}
full_tensor_axis_possible_rows=3
full_tensor_axis_failure_rows=0
one_factor_full_axis_rows=2
one_factor_dimension_possible_rows=2
one_factor_dimension_possible_no_full_factor_rows=0
```

So in the rows tested so far, whenever one tensor factor has enough dimension
for the axis theorem, at least one tensor factor has full axis rank.  This is
evidence for the p24 one-factor determinant target, not a proof.

The factor ranks were equal in every tested row:

```text
pinned D=-10919:
  equal_factor_rank_rows=1
  unequal_factor_rank_rows=0

broader factor window:
  equal_factor_rank_rows=20
  unequal_factor_rank_rows=0
```

This is explained in:

```text
p24/tensor_factor_rank_symmetry.md
```

The reason is semilinear Frobenius: it sends `R_s(eta)` to `R_{p*s}(eta^p)`
and the selected axis frequency set is stable under `s -> p*s`.

## Component Block Refinement

I added:

```text
p24/k_character_tensor_factor_block_scan.py
p24/tensor_factor_block_directness.md
```

This checks the one-factor axis rank block-by-block:

```text
constant block,
2-axis block,
157-axis block,
211-axis block.
```

In the small broader window it reported:

```text
rows=20
block_internal_unforced_failure_rows=0
pair_directness_unforced_failure_rows=0
dimension_possible_full_failure_rows=0
```

So every observed component or pair failure was dimension-forced.  This
supports the p24 proof shape:

```text
component block normality + cross-block directness in one B_i
  => one-factor axis rank
  => base packet axis injectivity.
```

## Theorem Target

For one p24 H-character packet and one tensor factor

```text
B_i / E,       [B_i:E]=5549,
```

define the K-character resolvents

```text
R_s = sum_{r,k} zeta_m^(s*r) j_{n*r+m*k} eta_i^k,
```

where `eta_i` is the selected H-character root in `B_i`.

Let `S_axis` be the 368-frequency set:

```text
{0}
union nonzero characters of the 2-axis
union nonzero characters of the 157-axis
union nonzero characters of the 211-axis.
```

The strongest compact tensor theorem would be:

```text
{R_s : s in S_axis}
is E-linearly independent in at least one B_i.
```

By tensor-factor rank symmetry, this is equivalent to independence in every
`B_i`.

Because scalar extension is faithful, the Lean gates

```text
p24/lean/ScalarExtensionGate.lean
p24/lean/AxisInjectivityGate.lean
```

now include the one-factor descent implication:

```text
one tensor-factor axis map injective
  => scalar-extended axis map has trivial kernel on the base source
  => original base-field packet axis map is injective.
```

So the current arithmetic theorem can be stated in the degree-`5549`
`E`-factor alone.

## 2026-06-08 One-Factor Refinement

The p24 component character degrees and tensor intersections are:

```text
ord_2(p)   = 1
ord_157(p)= 156
ord_211(p)= 35
ord_m(p)  = 5460
ord_n(p)  = 388430
gcd(ord_m(p), ord_n(p)) = 70

A_a tensor F_p(mu_m) splits into 70 factors B_i/E,
[B_i:E] = 5549.

For each component c in {2,157,211},
gcd(ord_c(p), 5549) = 1.
```

Thus inside a single tensor factor the smooth-axis character fields are
linearly disjoint from the H-subpacket factor.  The missing theorem is not a
field-intersection issue; it is the selected CM/Moore determinant
nonvanishing:

```text
det(R_s^(Q^j))_{s in S_axis, 0 <= j < 368} != 0
inside one B_i,        Q = p^5460.
```

Latest bounded tensor-factor stress pass:

```text
K-character tensor factor-rank scan:
  rows=130
  full_tensor_axis_possible_rows=32
  full_tensor_axis_failure_rows=0
  one_factor_dimension_possible_rows=6
  one_factor_dimension_possible_no_full_factor_rows=0
  equal_factor_rank_rows=130
  unequal_factor_rank_rows=0

K-character tensor factor block-rank scan:
  rows=130
  one_factor_dimension_possible_rows=6
  block_internal_unforced_failure_rows=0
  pair_directness_unforced_failure_rows=0
  dimension_possible_full_failure_rows=0
```

This is still evidence, not proof.  It does, however, remove the need to work
in the full degree-`388430` packet when pursuing the axis route.

The stronger version,

```text
the same independence holds in every B_i,
```

is suggested by the pinned rows but is not needed for the certificate.

## Why This Is Sharper

The original packet axis determinant lives in a degree-388430 packet field
over `F_p`.  The tensor one-factor determinant lives in degree 5549 over
`E=F_p(mu_m)`.

As an `F_p` norm, one tensor factor has degree

```text
5460 * 5549 = 30297540,
```

still far below the class size and far below `sqrt(p)`.  This is not yet a
construction, but it is the smallest clean determinant surface found so far
that retains all K-character phases and avoids the packet-Frobenius cocycle.

## Boundary

Nonzero K-character resolvents alone are not a formal proof.  The broader
small scan has `axis_support_not_rank_rows=25`; all were dimension-bound, but
they show that support does not imply rank in general.

The stronger "distinct K-eigenvalues imply independence" shortcut is also
invalid inside one tensor factor.  The boundary is recorded in:

```text
p24/tensor_factor_k_action_boundary.md
```

The small row `D=-8711` has six nonzero selected K-character resolvents with
distinct K-labels in a degree-5 tensor factor, so no internal `E`-linear
K-action can be diagonalizing them there.

The missing arithmetic input is therefore a **tensor Moore/normality
statement** for the selected CM resolvents:

```text
not just R_s != 0,
but the 368 selected R_s are E-linearly independent in one degree-5549
H-subpacket factor.
```

The intrinsic determinant version is recorded in:

```text
p24/tensor_factor_moore_certificate.md
```

It uses the Moore determinant

```text
det(R_s^(Q^j))_{s in S_axis, 0 <= j < 368},      Q=|F_p(mu_m)|.
```

This is the current most explicit form of the embedded class-field tower
identity route.
