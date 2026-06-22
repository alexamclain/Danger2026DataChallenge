# P27 Label-2 H90 / Order-4 Lift

Date: 2026-06-21

## Claim

The label-2 second-gate cover is not just a generic extra square root.  The
`T -> -T` deck involution on the intermediate cover has an exact lift to the
full second-gate cover, and that lift has order `4`.

This is the first positive quotient-shaped structure found after the genus-17
warning.  Riemann-Hurwitz predicts that the quotient by this order-4
automorphism has genus `1`, identifying the cover as a cyclic quartic cover
over the residual elliptic curve `E: W^2=X^3-X`.

Follow-up online Magma component checks confirm the eliminated cyclic-quartic
model has a degree-30 genus-17 main component over `q=607`, `q=1471`, and the
p27-signature field `q=1607`, plus a degree-1 genus-0 projection artifact.  See
[P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md).
Thus the open win is specifically the `alpha` quotient/Prym decomposition,
not a low-genus raw eliminated model.

This does not by itself beat sqrt scaling, but it changes the concrete target:
derive the elliptic cyclic-quartic character/source, and test whether that
structure recurs for later `d_j` gates.

Follow-up eliminated-map probe:
[P27 Label-2 Alpha Eliminated-Map Probe](p27_label2_alpha_eliminated_map_20260621.md).
On the eliminated cyclic-quartic model, the order-4 lift is the rational map

```text
R -> R*mt*(2*pref*m0 - R^2)/(2*S*(R^2 - pref*m0)).
```

It was validated over q1607, q1847, and q2087: the map preserves the curve,
squares to the `R`-deck involution, and fourth-powers to identity away from
the expected exceptional branch points.  The quotient/Prym request should use
this explicit map.

The p26 GPU trace/norm result adds an implementation guardrail: a real stratum
with `4x` conditional enrichment can still lose if the classifier costs more
than the enrichment buys.  For this p27 order-4 structure, a useful win must be
a direct sampler, a cheaper cyclic-quartic character test, or a recurrence
that improves `d3/d4` survivor rate per GPU-second.

## Identities

Use the label-2 equations:

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
```

and the second-gate mixed term:

```text
mt = (X + 1)(2WX + X^3 + X^2 - X - 1)
m0 = (X^2 + 1)(X^2 + 2X - 1)(WX + W + 2X^2)
```

Define:

```text
L = 4WX^2 + 4WX + X^4 + 6X^3 - 2X - 1
S = W(X + 1) + 2X^2
```

The new symbolic identities are:

```text
S^2 = X L
m0^2 - mt^2 T^2 = 4 T^2 S^2
```

For the second-gate squareclass

```text
h = W(X^2 + 1)(m0 + mt*T)/X
```

the `T`-deck ratio is an exact square:

```text
h(X,W,-T) / h(X,W,T)
  = ((m0 - mt*T)/(2*T*S))^2.
```

Thus the involution

```text
tau_T: (X,W,T) -> (X,W,-T)
```

lifts to the full cover `R^2=h` by:

```text
alpha:
  T -> -T
  R -> R * (m0 - mt*T)/(2*T*S)
```

Applying the lift twice multiplies `R` by `-1`, so:

```text
alpha^2 = R-deck involution
alpha has order 4
```

Eliminating `T` gives the cyclic quartic model over the residual elliptic
curve `E=(X,W)`:

```text
pref = W(X^2+1)/X
R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*S^2 = 0.
```

Here `T2=X(X^2+1)(X^2+2X-1)` is a function of `X`, so this is a degree-4
cover of `E`.

## Command

```bash
python3 research/p27/archive/gates/p27_label2_h90_lift_probe.py \
  | tee research/p27/archive/probe_outputs/p27_label2_h90_lift_probe_20260621.txt
```

Key output:

```text
S2_minus_XL = 0
norm_m_minus_4T2S2 = 0
T_deck_ratio_square_check = 0
T_deck_lift_alpha_squared = R_deck_involution
T_deck_lift_multiplier_square_product = -1
cyclic_quartic_over_E = R^4 - 2*prefactor*m0*R^2 + 4*prefactor^2*T2*S^2
alpha_fixed_points_inferred = 8
R_deck_fixed_points_inferred = 16
genus_D_mod_alpha_by_RH = 1
D_mod_alpha_identifies_residual_E = 1
```

Finite-field sanity checks also match the symbolic result:

```text
T deck:  zero nonsquare ratios on all tested primes
W deck:  mixed square/nonsquare ratios once enough points exist
WT deck: mixed square/nonsquare ratios once enough points exist
```

## Interpretation

Positive:

```text
The genus-17 second cover has a real order-4 symmetry.
The second gate is an anti-invariant Hilbert-90 / cyclic-4 object under T.
The quotient D/<alpha> has genus 1 by the current Riemann-Hurwitz count.
The second gate can be viewed as a cyclic quartic cover over E: W^2=X^3-X.
```

Negative:

```text
This does not force d3; prior compactD=-1 streams still show the next gate at
about 1/2.
The paired T-deck roots and the available half-branches do not provide a d3 or
d4 selector; the 5,000-pair alpha/branch recurrence probe saw all paired
branches agree on the next bit, but with random-looking half-loss rates.
The W and WT deck flips do not provide the same visible lift.
There is still no known low-genus/sourceable model.
The rational E[2] packet source was tested and has 1.0x source lift.
The residual E[3] coset source was tested and did not give a stable lift.
The visible residual-E quadratic-character span was tested and did not match.
```

The packet result is recorded in
[P27 Label-2 E[2] Packet Source Probe](p27_label2_e2_packet_source_probe_20260621.md).
The natural H90 norm-one feature screen is recorded in
[P27 Label-2 H90 Norm-One Recurrence Screen](p27_label2_h90_normone_recurrence_20260621.md).
The residual `[3]` result is recorded in
[P27 Label-2 Residual E[3] Coset Screen](p27_label2_residual_e3_coset_screen_20260621.md).
The visible character screen is recorded in
[P27 Label-2 Visible Residual-E Character Screen](p27_label2_visible_e_character_screen_20260621.md).
The alpha/branch recurrence screen is recorded in
[P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md).
The eliminated alpha map is recorded in
[P27 Label-2 Alpha Eliminated-Map Probe](p27_label2_alpha_eliminated_map_20260621.md).

## Decisive Next Tests

### Sage/Magma Quotient / Cyclic Quartic Test

Define:

```text
C: W^2 = X^3-X,
   T^2 = X(X^2+1)(X^2+2X-1)

D: R^2 = W(X^2+1)(m0+mt*T)/X
```

with `m0`, `mt`, and `S` as above, and the automorphism:

```text
alpha(X,W,T,R) =
  (X, W, -T, R*(m0-mt*T)/(2*T*S)).
```

Report:

```text
genus(D)
order and fixed points of alpha
genus(D/<alpha>)
explicit quotient coordinates if feasible
verification that D/<alpha> is the residual E=(X,W)
Jacobian/Prym decomposition respecting alpha
elliptic or genus-2 factors that dominate compactD=-1
explicit cyclic quartic character/function over E controlling compactD=-1
```

Promotion bar:

```text
The cyclic quartic over E admits a cheap finite-field source, a low-cost
character test with better than random loss, or a recurrence to d3/d4.
The net effect is positive in effective survivors per GPU-second, not only in
conditional survivor lift.
```

Kill condition:

```text
The cyclic quartic character is just the original random T/R square-root loss,
and d3/d4 telemetry stays independent 1/2.
```

### GPU Telemetry Coupling

Keep the GPU ask the same, but interpret it through the order-4 lift:

```text
baseline = ecover label-2
candidate = ecover label-2 + compactD=-1
inside candidate report d3_chi and d4_chi
```

Only promote if the order-4 structure is accompanied by a deeper recurrence or
per-GPU-second survivor lift after throughput loss.

## Continue / Kill

```text
continue = Sage/Magma alpha quotient and alpha-equivariant Prym decomposition
continue = use the eliminated alpha_R map as the quotient input
continue = derive explicit cyclic quartic character over E
continue = GPU compactD=-1 telemetry with d3/d4 inside the stratum

kill = treating compactD=-1 alone as sqrt-beating
kill = branch-choice or T-deck choice as a d3/d4 selector
kill = searching W/WT deck lifts as if they behaved like T
kill = E[2] packet selector as a source-level sqrt-beating route
kill = H90 norm-one squareclass products from the screened feature family
kill = E[3] coset source as an active moonshot lane
kill = visible residual-E quadratic character from the screened H90 factors
kill = generic visible-character scans unrelated to the alpha symmetry
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_label2_h90_lift_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_h90_lift_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_packet3_seed142_200k_depth24_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid3_coset0_seed145_2M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_visible_e_character_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_alpha_branch_recurrence_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_alpha_eliminated_map_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_h90_normone_recurrence_probe_20260621.txt`
- Related: [P27 Label-2 Cover Genus And Recurrence Probe](p27_label2_cover_genus_recurrence_20260621.md)
- Related: [P27 Label-2 Cover Trace Decomposition Probe](p27_label2_cover_trace_decomposition_20260621.md)
- Related: [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md)
- Related: [P27 Label-2 H90 Norm-One Recurrence Screen](p27_label2_h90_normone_recurrence_20260621.md)

```text
p27_label2_h90_order4_lift_rows=1/1
```
