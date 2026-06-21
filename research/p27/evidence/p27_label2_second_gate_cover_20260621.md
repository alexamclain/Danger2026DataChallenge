# P27 Label-2 Second-Gate Cover

Date: 2026-06-21

## Claim

The p27 second selected-halving gate now has a named label-2 cover
formulation.

The first-lift residual elliptic cover gives

```text
E: W^2 = X^3 - X.
```

Use the label-2 orbit coordinate

```text
y = 2X/(X - 1)
```

and write the original `X1(16)` fiber root as

```text
T^2 = X(X^2 + 1)(X^2 + 2X - 1).
```

In this `(X,W,T)` field, the compact second-gate criterion from
`label2_compact_d_class128` is explicit. For p27, the useful class is:

```text
compactD = -1
```

equivalently the underlying compact criterion is a square. This exactly
selects the depth-5 to depth-6 gate in the measured p27 label-2 stream.

This is not yet a sqrt-beating result. It is a sharper source-cover target:
sample or exploit the mixed cover

```text
R^2 = criterion(X,W,T)
```

cheaply, then test whether the same pattern repeats for `d3,d4,...`.

## Symbolic Gate

Command:

```bash
python3 research/p27/archive/gates/p27_label2_second_gate_symbolic_gate.py \
  | tee research/p27/archive/probe_outputs/p27_label2_second_gate_symbolic_20260621.txt
```

Output:

```text
label2_y = 2*X/(X - 1)
T2 = X*(X**2 + 1)*(X**2 + 2*X - 1)
mt_coeff = (X + 1)*(2*W*X + X**3 + X**2 - X - 1)
m0 = (X**2 + 1)*(X**2 + 2*X - 1)*(W*X + W + 2*X**2)
compactD_criterion =
  W*(X**2 + 1)*(m0 + mt_coeff*T)/X
norm_T_remaining_linear =
  4*W*X**2 + 4*W*X + X**4 + 6*X**3 - 2*X - 1
norm_TW_remaining_linear =
  (X**2 + 1)**2*(X**2 - 2*X - 1)**2
x_line_quadratic_character_gate = 0
second_gate_lives_on_mixed_X_W_T_cover = 1
```

Interpretation:

```text
The second gate is not a visible X-line character.
After taking norms through T and W, the remaining obstruction collapses to a
square on the X-line.
So the gate has Hilbert-90 / mixed-cover shape, not ordinary branch-divisor
shape.
```

## P27 Sign And Exactness

Command:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  137 1000000 x16halvestatsnonsplitecoverlabel2mixed \
  > research/p27/archive/probe_outputs/p27_label2_mixed_seed137_1M_20260621.txt 2>&1
```

The `label2_D` split exactly separates the second gate:

```text
label2_D class D=-1 samples=499018
  depth16 survive=0

label2_D class D=+1 samples=500982
  depth16 survive=512
  depth18 survive=126
  depth20 survive=38
```

The compact formula has the opposite sign on p27:

```text
label2_compact_D mismatch_vs_D = 1000000 / 1000000
```

Thus for p27:

```text
second gate = label2_D = +1 = compactD = -1.
```

This p27 sign is why the new modes below were added instead of reusing the old
`compactd` mode.

## Corrected-Sign CPU Probe

Added experimental modes:

```text
x16halvenonsplitecoverlabel2compactdneg
x16halvestatsnonsplitecoverlabel2compactdneg
```

They keep the old `compactd` behavior intact and set the compact filter target
to `-1`.

Same-seed 500k stats:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  138 500000 x16halvestatsnonsplitecoverlabel2 \
  > research/p27/archive/probe_outputs/p27_label2_base_seed138_500k_20260621.txt 2>&1

/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  138 500000 x16halvestatsnonsplitecoverlabel2compactd \
  > research/p27/archive/probe_outputs/p27_label2_compactd_seed138_500k_20260621.txt 2>&1

/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 \
  138 500000 x16halvestatsnonsplitecoverlabel2compactdneg \
  > research/p27/archive/probe_outputs/p27_label2_compactdneg_seed138_500k_20260621.txt 2>&1
```

Result:

```text
mode          rate_Mps  d16_survive_rate  d18_survive_rate  d20_survive_rate
label2        0.108585  0.000472          0.000088          0.000020
compactd      0.036065  0                 0                 0
compactdneg   0.032541  0.000956          0.000200          0.000052
```

So:

```text
compactd selects the wrong p27 sign and should not be used for p27.
compactdneg exactly starts at depth 6 and gives about the expected 2x
conditional survivor lift.
current CPU implementation is too slow to promote as production.
```

The score comparison at depth 16 is:

```text
label2      score ~= 0.108585 * 0.000472 = 5.13e-5
compactdneg score ~= 0.032541 * 0.000956 = 3.11e-5
```

This makes `compactdneg` a structure/GPU test, not a CPU production mode.

## Moonshot Test Cards

### Card A: GPU Exact Second-Gate A/B

Implement p27 label-2 compactD with the corrected sign:

```text
candidate = ecover label-2 source with compactD = -1
control   = ecover label-2 source without compactD
```

Report:

```text
same-stream coverage
per GPU-second rate
d16/d18/d20 survivor lift
effective survivor lift per GPU-second
verification that compactD=-1 equals d2 square / depth-6 pass
```

Promotion bar:

```text
GPU can compute compactD cheaply enough that the 2x conditional lift beats the
throughput loss.
```

### Card B: Cover Genus / Decomposition

Ask Sage/Magma, or an expert, for the curve:

```text
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
R^2 = W(X^2 + 1)(m0 + mt_coeff*T)/X
```

with

```text
mt_coeff = (X + 1)(2WX + X^3 + X^2 - X - 1)
m0       = (X^2 + 1)(X^2 + 2X - 1)(WX + W + 2X^2).
```

Decisive outputs:

```text
genus
Jacobian decomposition / elliptic quotients
existence of a cheap F_p point source or low-degree map from an elliptic curve
```

Promotion bar:

```text
The cover is dominated by a source we can walk as cheaply as the first ecover,
or it has a repeatable tower structure.
```

Kill condition:

```text
Generic high-genus double cover with no useful low-degree quotient or
repeatable map.
```

### Card C: Third-Gate Recurrence

Inside `compactD=-1` rows, compute the selected next gate:

```text
d3 = x6^2 + A*x6 + 1
```

Then test whether a label-2-style compact criterion can be re-expressed on the
new cover coordinates with the same norm-square collapse.

Promotion bar:

```text
same algebraic criterion shape repeats for d3, giving a plausible tower.
```

Kill condition:

```text
d3 is again random 1/2 with no recycled compact criterion.
```

## Interpretation

Positive:

```text
The second gate is no longer unnamed: it has an explicit mixed-cover formula.
The p27 sign is known: use compactD=-1, not compactD=+1.
This gives concrete GPU and Sage/Magma tests that could lead to a source
tower.
```

Negative:

```text
The current CPU compactD filter loses on survivor-per-second.
A fixed d1+d2 prefix is still only a constant factor.
The actual sqrt-beating question is whether the mixed cover can be sourced and
iterated.
```

Follow-up: [P27 Label-2 Cover Genus And Recurrence Probe](p27_label2_cover_genus_recurrence_20260621.md)
prices this mixed cover as genus `17` in a finite-local ramification probe and
finds no immediate `d3` recurrence after `compactD=-1`.

Positive follow-up:
[P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
shows that the `T -> -T` involution lifts to the full second-gate cover with
order `4`.  Riemann-Hurwitz gives `D/<alpha>` genus `1`, so the second gate is
a cyclic quartic cover over the residual elliptic curve `E: W^2=X^3-X`.
This gives a concrete target: derive the cyclic quartic character/source over
`E`, then test whether it recurs for `d3/d4`.

Packet-source follow-up:
[P27 Label-2 E[2] Packet Source Probe](p27_label2_e2_packet_source_probe_20260621.md)
kills the easiest residual-elliptic packet source.  The selector is exact and
has `~2x` candidate lift, but `1.0x` source lift through depth `24`.

## Continue / Kill

```text
continue = GPU same-stream label2 vs compactD=-1 A/B
continue = Sage/Magma cyclic quartic / alpha-equivariant decomposition over E
continue = symbolic/telemetry pass for the d3 recurrence inside compactD=-1

kill = p27 use of compactD=+1
kill = CPU promotion of compactdneg without a major optimization
kill = treating one extra forced gate as sqrt-beating
kill = E[2] packet source from current evidence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_label2_second_gate_symbolic_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_label2_second_gate_symbolic_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_mixed_seed137_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_resid_seed137_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_base_seed138_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_compactd_seed138_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_compactdneg_seed138_500k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_h90_lift_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_packet3_seed142_200k_depth24_20260621.txt`
- Production smoke: `research/p27/archive/probe_outputs/p27_label2_compactdneg_prod_seed139_250k_20260621.txt`

```text
p27_label2_second_gate_cover_rows=1/1
```
