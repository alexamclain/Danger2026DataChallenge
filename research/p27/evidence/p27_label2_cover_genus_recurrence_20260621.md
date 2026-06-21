# P27 Label-2 Cover Genus And Recurrence Probe

Date: 2026-06-21

## Claim

The label-2 second-gate cover is explicit, but the first genus/ramification
diagnostic makes it look too large to be the next cheap source by itself.

The intermediate cover

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
```

has genus `5`.  Adding the corrected p27 second-gate square root

```text
R^2 = compactD_criterion(X,W,T)
```

appears to give a ramified double cover of genus `17`, not an unramified or
elliptic-dominated cover.

The immediate third-gate recurrence check is also negative: after forcing
`d1` and `d2`, the next selected gate survives at essentially `1/2`.

## Genus Probe

Command:

```bash
python3 research/p27/archive/gates/p27_label2_cover_genus_probe.py \
  | tee research/p27/archive/probe_outputs/p27_label2_cover_genus_probe_20260621.txt
```

The intermediate genus comes from the three quadratic quotients of the
biquadratic cover over the `X`-line:

```text
genus_W  = genus(W^2 = X^3 - X) = 1
genus_T  = genus(T^2 = X(X^2+1)(X^2+2X-1)) = 2
genus_WT = genus(squarefree product quotient) = 2
genus_C  = 1 + 2 + 2 = 5
```

The local valuation probe uses `p=17`, where the visible branch factors split
and the characteristic is good.  It found:

```text
finite_odd_local_orders = 16
infinity_odd_local_orders = 0
ramification_points_for_R_cover = 16
genus_R_cover_if_smooth = 17
```

Representative odd local orders:

```text
x=1 and x=-1 over both T signs
roots of X^2+1 over both W signs
roots of X^2+2X-1 over both W signs
remaining W-linear L roots over both T signs
```

The common branch at `X=0` and both infinity classes had even order.

## Third-Gate Recurrence Check

After the corrected second-gate filter, the next gate remains balanced.

Commands:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  138 500000 x16halvestatsnonsplitecoverlabel2compactdneg \
  > research/p27/archive/probe_outputs/p27_label2_compactdneg_seed138_500k_20260621.txt 2>&1

/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  140 500000 x16halvestatsnonsplitecoverlabel2compactdneg \
  > research/p27/archive/probe_outputs/p27_label2_compactdneg_seed140_500k_20260621.txt 2>&1
```

Results:

```text
seed 138:
  depth6 survive = 500000
  depth7 survive = 250626  ratio = 0.501252
  depth8 survive = 125426  ratio = 0.500451 from depth7

seed 140:
  depth6 survive = 500000
  depth7 survive = 251048  ratio = 0.502096
  depth8 survive = 125278  ratio = 0.499020 from depth7
```

This is exactly the random half-loss profile.  The label-2 compact criterion
captures the second gate, but it does not automatically force the third.

## Interpretation

Positive:

```text
The tower checkpoint is much sharper than before:
  first gate  = residual elliptic cover
  second gate = explicit label-2 mixed cover
```

Negative:

```text
The second cover prices as genus 17 in the current diagnostic.
The immediate d3 survival remains random-looking.
A simple "walk the next cover" plan is not yet a sqrt-beating mechanism.
```

Trace decomposition follow-up:

```text
The small-prime trace screen reconciles the intermediate V4 cover after a
+1 common-branch correction at X=0.
The new Prym trace aD-aC is not a small combination of the visible W/T/WT
quotient traces with coefficients in [-8,8].
```

See [P27 Label-2 Cover Trace Decomposition Probe](p27_label2_cover_trace_decomposition_20260621.md).

Order-4 lift follow-up:

```text
The T-deck involution does lift to the full second-gate cover.
With S = W(X+1)+2X^2, one has S^2=X*L and
m0^2-mt^2*T^2 = 4*T^2*S^2.
The lifted automorphism has order 4, with square equal to the R-deck
involution.
Riemann-Hurwitz gives D/<alpha> genus 1, so the second-gate cover is a cyclic
quartic cover over the residual elliptic curve E: W^2=X^3-X.
```

See [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md).

Online Magma follow-up:

```text
q=607:  main component degree 30, genus 17; projection artifact degree 1, genus 0
q=1471: main component degree 30, genus 17; projection artifact degree 1, genus 0
```

See [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md).
This confirms the raw eliminated cyclic-quartic model is not secretly low
genus; the remaining source-shaped test is the alpha quotient/Prym
decomposition of the genus-17 component.

## Concrete Tests Left

### Sage/Magma Verification

Verify the genus, ramification, and order-4 quotient over characteristic zero:

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
R^2 = W(X^2 + 1)(m0 + mt_coeff*T)/X
alpha: T -> -T,
       R -> R*(m0-mt_coeff*T)/(2*T*(W(X+1)+2X^2))
```

Report:

```text
genus of C=(X,W,T)
genus of D=(X,W,T,R)
ramification divisor of D -> C
Prym/Jacobian decomposition
genus and explicit coordinates for D/<alpha>
alpha-eigenspace decomposition
cyclic quartic character over E=(X,W)
any elliptic or genus-2 quotient that dominates the compactD=-1 stratum
```

### GPU Telemetry

Still test `compactD=-1` only if native GPU arithmetic makes it cheap:

```text
baseline: ecover label-2
candidate: ecover label-2 + compactD=-1
negative control: ecover label-2 + compactD=+1
```

Do not promote on the fixed second gate alone; promote only if per-GPU-second
survivor lift beats the throughput loss or if d3/d4 telemetry reveals a
non-random recurrence.

### Tower Recurrence

The next mathematical target is no longer "find d2"; it is:

```text
find a recurrence or decomposition that makes the genus-17 second cover
iterable or reducible.
```

Kill condition:

```text
Magma confirms a generic genus-17 cover with no useful low-degree quotient,
and GPU d3/d4 telemetry stays at independent 1/2 loss.
```

## Continue / Kill

```text
continue = Sage/Magma genus and Prym/Jacobian decomposition
continue = GPU compactD=-1 only as same-stream telemetry
continue = d3/d4 recurrence search only if tied to the mixed-cover structure

kill = treating compactD=-1 as a sqrt-beating source by itself
kill = broad scans for another visible one-bit character
kill = CPU production use of compactdneg at current speed
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_label2_cover_genus_probe.py`
- Gate: `research/p27/archive/gates/p27_label2_cover_trace_probe.py`
- Gate: `research/p27/archive/gates/p27_label2_h90_lift_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_cover_genus_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_cover_trace_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_h90_lift_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_cyclic_components_q607_magma_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1471_magma_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_compactdneg_seed138_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_compactdneg_seed140_500k_20260621.txt`
- Related: [P27 Label-2 Second-Gate Cover](p27_label2_second_gate_cover_20260621.md)
- Related: [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md)

```text
p27_label2_cover_genus_recurrence_rows=1/1
```
