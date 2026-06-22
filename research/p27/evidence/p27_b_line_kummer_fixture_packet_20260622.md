# P27 B-Line Kummer Fixture Packet

Date: 2026-06-22

## Claim

The B-line route now has compact finite-field fixtures for the actual
conditional Kummer sequence:

```text
f3(B), f4(B), f5(B), ...
```

Here `f_j` means the selected gate `d_j` character on the B values that
survived the previous all-plus prefix.  This is the right input for a
Magma/Sage/expert class comparison: recover the normalized class for `f3`,
then decide whether `f4/f5` are pullbacks, translates, coboundaries, iterates,
or fresh independent half-covers.

## Artifacts

Generator:

```text
research/p27/archive/gates/p27_b_line_kummer_fixture_packet.py
```

Readable packet:

```text
research/p27/archive/probe_outputs/p27_b_line_kummer_fixture_packet_20260622.txt
```

JSON fixture:

```text
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_kummer_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  --max-gate 6 \
  | tee research/p27/archive/probe_outputs/p27_b_line_kummer_fixture_packet_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_kummer_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  --max-gate 6 \
  --json \
  > research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
```

## Fixture Contents

The fixture records the core/legal B rows and conditional gate classes for the
p27-signature guard fields.

```text
q1607:
  core_B = 200
  legal_B = 49
  f3 rows = 49, plus/minus = 28/21
  f4 rows = 28, plus/minus = 19/9
  f5 rows = 19, plus/minus = 19/0
  f6 rows = 19, plus/minus = 0/19

q1847:
  core_B = 230
  legal_B = 63
  f3 rows = 63, plus/minus = 45/18
  f4 rows = 45, plus/minus = 19/26
  f5 rows = 19, plus/minus = 0/19
  f6 rows = 0

q2087:
  core_B = 260
  legal_B = 57
  f3 rows = 57, plus/minus = 25/32
  f4 rows = 25, plus/minus = 18/7
  f5 rows = 18, plus/minus = 18/0
  f6 rows = 18, plus/minus = 18/0
```

There are no mixed or missing B groups in these conditional rows before the
field tail becomes empty.

## Interpretation

Positive:

```text
The actual B-line conditional classes are now frozen in a compact, reusable
fixture.
The class-comparison task is concrete: f3 first, then f4/f3.
No-mixed-B descent remains clean in q1607/q1847/q2087.
```

Bridge update:
[P27 B/K/Sroot Fixture Bridge](p27_b_ksroot_fixture_bridge_20260622.md)
shows that this B-line fixture and the K/Sroot fixture are exact coordinate
views of the same conditional classes through all recorded gates.  Use B as
the simpler genus-0 quotient and K/Sroot as signed-sheet/parity checks, not as
independent moonshot evidence.

Second bridge:
[P27 B/A Fixture Bridge](p27_b_a_fixture_bridge_20260622.md)
shows that the frozen A-level `d3,d4` rows are exactly the B-line rows under
`A=B^2-2`, with `267/267` sign matches and no collisions across the three
p27-signature fields.  Treat A as another coordinate for the same class
extraction problem.

Fiber-invariant follow-up:
[P27 B-Line Fiber Invariant Probe](p27_b_line_fiber_invariant_probe_20260622.md)
shows that each legal B has `32` next-root occurrences, `8` distinct x-roots,
and `4` reciprocal-quotient values `u=x+1/x`, with `f3=chi(u+2)` throughout.
However, products/norms are square, power sums through exponent `64` do not
select f3, and the four-u polynomial coefficients are not low-degree on the
legal-B set.  The reduced 4-u/8-x cover is the next normalization target.

Second reduced-fiber follow-up:
[P27 B-Line Second Reduced-Fiber Fixture](p27_b_line_second_reduced_fiber_20260622.md)
freezes the analogous `f4` object over the `f3=+1` legal B-domain.  Each
active B row has `64` x7 occurrences, `16` distinct x7 roots, and `8`
reciprocal-quotient values `v=x7+1/x7`, with `f4=chi(v+2)` throughout.  No
stable power-sum or low-degree plane relation appears through the tested
bounds, so this is a CAS class-comparison packet rather than a GPU bucket.

Transition/orientation follow-up:
[P27 B-Line Transition Closure And Orientation](p27_b_line_transition_closure_orientation_20260622.md)
shows that the quotient transition from `u` to `v` has `4` generic v-roots per
u-root, while the actual source keeps the `2` roots with
`chi(v^2-4)=chi(v+A)=+1`.  This is the visible materialization layer, not the
moonshot class: `chi(v+2)=f4(B)` is constant even on the discarded generic
roots.  The next CAS object is therefore `F_A(u,v)=0`, `rho^2=v^2-4`,
`gamma^2=v+2`.

Gamma norm follow-up:
[P27 B-Line Gamma Norm/Coboundary Boundary](p27_b_line_gamma_norm_coboundary_20260622.md)
shows that `Norm_4(v+2)=16*(A-2)^2` and the actual/missing two-root gamma norms
are square, but the naive parent-`x6` formula is false and visible pair
invariants do not predict `f4`.  Keep the H90/coboundary route alive as a CAS
class computation, not as a norm bucket.

Explicit H90 follow-up:
[P27 B-Line Gamma H90 Quotient](p27_b_line_gamma_h90_quotient_20260622.md)
shows that the quotient collapses to the first reduced cover:
`(v1+2)/(v2+2) + (v2+2)/(v1+2) = u`, and if `h^2=(v1+2)/(v2+2)` then
`(h+1/h)^2=u+2`.  No visible H90 quotient product predicts `f4`.

F3/H90 layer follow-up:
[P27 B-Line Gamma Over F3/H90 Layer Relation Screen](p27_b_line_gamma_f3_layer_relation_20260622.md)
adjoins both sheets `H=+/-(h+1/h)` with `H^2=u+2`.  The stable pair-coordinate
screens in `(B,H)`, `(B,tau)`, `(B,H^2)`, and `(B,tau_sym)` do not expose the
`f4` split.  The remaining B-line work is true divisor/Kummer-class extraction
for `gamma`, not visible coordinate fitting.

Gamma class handoff:
[P27 B-Line Gamma Class Handoff](p27_b_line_gamma_class_handoff_20260622.md)
freezes the staged q1607/q1847/q2087 rows for
`A=B^2-2`, `H^2=u+2`, `F_A(u,v)=0`, and `gamma^2=v+2`.  Every active `(B,u)`
parent has four generic transition roots, two materialized roots, and two
discarded roots; `chi(v+2)` is constant on the generic roots.  The next B-line
pass should classify the resulting gamma class, then compare it with the next
f5/f4 class.

V4 factorization follow-up:
[P27 B-Line Gamma V4 Factorization](p27_b_line_gamma_v4_factorization_20260622.md)
shows that the quartic in `Y=v+2` has square discriminant and split resolvent.
After adjoining `R^2=H^2-4` and `S^2=B^2+H^2-4`, the roots are
`(H +/- R)*(H +/- S)`.  The component characters
`alpha=chi(H+R)` and `beta=chi(H+S)` both flip under `H -> -H`, but their
product is `f4`.  This turns the next test into phase-sequence recurrence or
telescoping, not a standalone B bucket.

Phase sequence follow-up:
[P27 B-Line Alpha/Beta Phase Sequence Screen](p27_b_line_alpha_beta_phase_sequence_20260622.md)
tests that recurrence idea on p27 train/heldout and q1607/q1847/q2087.  No
alpha/beta phase state or link product clears the source-normalized promotion
bar.  Keep the V4 decomposition for CAS class extraction and optional GPU
telemetry, not as a production sampler.

Negative:

```text
The later f5/f6 rows are visibly field-tail dominated.
They become one-sided with field-dependent signs and should not be promoted
as recurrence evidence.
```

So the meaningful first-pass B-line CAS target is:

```text
recover f3(B), then compare f4 on the f3-plus domain.
```

Do not read the small guard-field `f5/f6` one-sided rows as a source law unless
a larger p27/GPU telemetry run supplies heldout counts with a raw-source
denominator and a named class.

## Continue / Kill

```text
continue = use JSON rows for B-line normalized Kummer/divisor extraction
continue = recover f3 branch degree, support field degrees, genus, components
continue = cross-check any class through the A/B/K/Sroot fixture bridges
continue = normalize the reduced 4-u / 8-x d3 fiber cover
continue = normalize the second reduced f4/f3 8-v cover
continue = use the staged transition/materialization/gamma model for f4/f3
continue = compute an explicit H90 quotient for gamma^2=v+2
continue = compute gamma over the f3/H90 layer as the remaining class
continue = extract the gamma divisor/Kummer class over that layer
continue = use the gamma class handoff as the current CAS/GPU packet
continue = keep the V4 alpha/beta phases as optional telemetry columns
continue = compare f4/f3 as a class relation after f3 is named
continue = use f5/f6 rows only as tail/regression checks for an extracted class

kill = treating one-sided guard-field f5/f6 tails as promotion evidence
kill = counting A-level, B-line, and K/Sroot fixtures as independent positives
kill = B-line norm/trace/power-sum selectors as a production sampler
kill = second-fiber low-degree B-plane relations as a production sampler
kill = chi(v^2-4) materialization as a production sampler
kill = naive gamma norm or visible pair-invariant predictors as source laws
kill = explicit H90 quotient as a standalone f4 source law
kill = visible f3/H90-layer pair-coordinate source laws for gamma
kill = current alpha/beta phase-state split as a production sampler
kill = more B-bucket GPU production before a source/recurrent class exists
kill = widening visible low-degree B scans already killed by q1847
```

```text
p27_b_line_kummer_fixture_packet_rows=1/1
```
