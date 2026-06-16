# P25 Lane B: Robert KSY Kubert-Lang CRT Coupling

Updated: 2026-06-13 16:40 PDT

## Purpose

The Kubert-Lang exponent-matrix precheck passed for the exact six-cell packet
at mixed level `507` and also passed after projecting to the prime-power
`C_169` axis.  This gate asks whether the projection is enough.

It is not.  The six-cell packet is a graph lift in `C_3 x C_169`; the row-3
selector is theorem-critical data.

## Exact Packet

Using the common-level embedding

```text
q = 169 * right + 3 * c  mod 507
```

the source packet is:

```text
positive: (1,25) q=244 -> (2,28) q=422 -> (0,31) q=93
negative: (0,138) q=414 -> (1,141) q=85 -> (2,144) q=263
```

The visible steps are:

```text
D = (1,3),    q_step = 178, order 507, 3D = q_step 27
T = (2,113),  q_step = 170, order 507
```

So the `D` segment and the `T` edge are both primitive in the `C_507`
encoding; this is not a hidden order-3 subgroup or a prime-power-axis artifact.

## Projection Falsifiers

The `C_169` projection is:

```text
(25,+1), (28,+1), (31,+1), (138,-1), (141,-1), (144,-1)
```

It has the right exponent congruences, but it does not identify which row in
`C_3` each point occupies.

Concrete failures:

```text
full C169 pullback support          = 18, not 6
row marginals                       = 0 in every row
row x C-projection product support  = 0
```

Thus the packet is neither a full pullback from `C_169` nor a product of row
and `C_169` marginals.

## Row-Lift Enumeration

Keeping the six projected `C_169` cells fixed, there are `3^6 = 729` possible
row lifts.

```text
KL congruence lifts       = 261
balanced row lifts        = 93
balanced KL lifts         = 93
D-segment/T-edge lifts    = 9
fixed T=(2,113) lifts     = 3
exact base + D + T lift   = 1
```

Also, the `C` quadratic relation and the mixed quadratic relation are
automatically satisfied for all `729` row lifts at this level.  The elementary
Kubert-Lang congruences therefore cannot be the selector by themselves.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_crt_coupling_rows=1/1
```

## Interpretation

The C169 prime-power projection is useful as a necessary congruence check, but
it is not a finite p25 producer.  A serious Kubert-Lang/Sprang/Robert theorem
candidate must emit the mixed graph data:

```text
(1,25) -> (2,28) -> (0,31)
```

and its `T=(2,113)` translate.  Literature search should now prefer theorem
statements with branch, period, differential, or distribution data that
preserve this row selector, not just prime-power Siegel-unit congruences.
