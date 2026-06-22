# P27 A-Level Kummer Extraction Packet

Date: 2026-06-22

## Claim

The A-line route now has a concrete CAS handoff: extract the normalized
A-level Kummer/divisor classes behind selected gates, starting with d3 and
then comparing d4/d5/d6.

This packet is the replacement for blind A-polynomial scans.  It preserves the
positive result that selected gates descend to whole A-fibers, plus the
negative results that visible degree `<= 4` branch support on `P1_A` and
degree-one A-line recurrences are killed.

## Artifacts

Packet generator:

```text
research/p27/archive/gates/p27_a_level_kummer_extraction_packet.py
```

Readable packet:

```text
research/p27/archive/probe_outputs/p27_a_level_kummer_extraction_packet_20260622.txt
```

JSON fixture:

```text
research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_level_kummer_extraction_packet.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 40 \
  | tee research/p27/archive/probe_outputs/p27_a_level_kummer_extraction_packet_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_level_kummer_extraction_packet.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 40 \
  --json \
  | tee research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json
```

## Fixture Contents

The JSON fixture records A-labeled rows for the p27-signature fields:

```text
q1607:
  unique_A = 49
  d3 rows = 49, plus/minus = 28/21, mixed = 0
  d4 rows = 28, plus/minus = 19/9, mixed = 0

q1847:
  unique_A = 63
  d3 rows = 63, plus/minus = 45/18, mixed = 0
  d4 rows = 45, plus/minus = 19/26, mixed = 0

q2087:
  unique_A = 57
  d3 rows = 57, plus/minus = 25/32, mixed = 0
  d4 rows = 25, plus/minus = 18/7, mixed = 0
```

The full JSON includes the actual A values and signs, not only counts.

## CAS Task

1. Recover the normalized A-cover carrying d3.

Required outputs:

```text
A-line function field or correspondence carrying the d3 character
branch divisor degree and support field degrees
normalization genus and component count
whether d3 is sourceable despite no visible degree <=4 support
```

2. Compare successive A-line classes.

Required outputs:

```text
d4 class on the d3-plus prefix
d5/d6 classes when enough rows or equations are available
pullback / translate / coboundary / iterate relation among classes
first p27-relevant recurrence candidate for d3..d10
```

## Promote / Kill

Promote:

```text
stable low-genus/sourceable A-line class
named correspondence controlling multiple selected gates
recurrence or coboundary that beats independent half-loss source-normalized
```

Kill:

```text
d3 has high/generic branch degree with no quotient
d4/d5/d6 are unrelated fresh half-covers
no low-genus/sourceable normalized A-level object exists
```

## Continue / Kill

```text
continue = run Magma/Sage normalization/class extraction using the JSON rows
continue = compare d3/d4/d5/d6 classes once a normalized model exists
continue = use p27 d3..d10 prefix data as routing evidence, not as equations
continue = higher correspondence tests only when theorem-shaped

kill = blind A polynomial scans without a divisor reason
kill = visible A-branch S3 orbit/recurrence shortcut
kill = affine A-line recurrence d_{j+1}(A)=+/-d_j(m*A+b)
kill = degree-one rational A-line recurrence
kill = hidden-X power-map A-level recurrence for m=2..6
kill = S3-conjugated Chebyshev/Dickson A-line recurrence for m=2..12
kill = GPU A-bucket production before a source law exists
kill = treating finite-field rows alone as a proof of recurrence
```

Update: [P27 A-Line Named-Transform Recurrence Screen](p27_a_line_named_transform_recurrence_20260622.md)
tests the fixed S3 action preserving `A in {-2,2,infinity}`.  Non-identity
transforms have zero d3 coverage in q1847 and zero d3..d8 coverage in p27
train/heldout samples, so the CAS pass should not spend time on visible
branch-orbit recurrences.

Update: [P27 A-Line Affine Recurrence Screen](p27_a_line_affine_recurrence_screen_20260622.md)
tests all full-coverage affine maps `A -> m*A+b` for the first meaningful
`d3 -> d4` transition in q1607/q1847/q2087.  It finds zero exact affine
recurrences.  Later identity recurrences occur only in one-sided small-field
tails with field-dependent signs, so this packet should focus on actual
Kummer/divisor classes, coboundaries, or sourced non-affine correspondences.

Update: [P27 A-Line PGL2 Recurrence Screen](p27_a_line_pgl2_recurrence_screen_20260622.md)
extends the recurrence falsifier to every full-coverage degree-one rational
map `A -> (aA+b)/(cA+d)`.  It also finds zero exact `d3 -> d4` recurrences in
q1607/q1847/q2087.  Future correspondence tests should therefore be higher
degree or theorem-specified, not PGL2 restarts.

Update: [P27 A-Level Power-Correspondence Screen](p27_a_level_power_correspondence_screen_20260622.md)
tests the first theorem-shaped higher correspondence after the PGL2 kill.  It
uses the hidden B-line coordinate `B=8X^2/(X^2-1)^2`, projects through
`A=B^2-2`, and checks all Belyi-conjugated `X -> X^m` maps for `m=2..6`.
There are no exact forward or reverse `d3/d4` recurrences in
q1607/q1847/q2087, so hidden-X power maps should not distract the CAS pass from
actual normalized-cover Kummer classes.

Update: [P27 A-Line Chebyshev Recurrence Screen](p27_a_line_chebyshev_recurrence_screen_20260622.md)
tests the canonical self-maps of the A branch set,
`D_m(A)=2*T_m(A/2)`, for `m=2..12`, with S3 conjugation on both sides.  No
full-domain recurrence appears in q1607/q1847/q2087.  This closes the nearest
postcritically finite A-line dynamics route and keeps the packet focused on
actual normalized-cover Kummer extraction.

Update: [P27 B/A Fixture Bridge](p27_b_a_fixture_bridge_20260622.md)
checks the frozen A-level rows against the B-line fixture through
`A=B^2-2`.  For q1607/q1847/q2087 and gates `d3,d4`, all `267` rows form an
exact signed bijection.  Thus the A packet is a quotient view of the same
conditional classes as the B-line packet, not an independent moonshot lane.
Use A as a CAS/check coordinate inside the coordinated A/B/K/Sroot extraction.

Update: [P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
checks the trace/norm `Dplus` raw-y stream directly.  On three independent p27
seed groups, post-Dplus `d3` and `d4` after `d3=+1` have zero mixed `A`
groups.  This routes Dplus later-gate class comparison into the same A-level
Kummer extraction task; trace/norm remains separate only for fused/native
Dplus pricing and possible source maps into the two-gate prefix.

Update: [P27 A-Line Combined Prefix Support Screen](p27_a_line_prefix_support_20260622.md)
tests whether one visible low-degree A-character can select the all-plus
`d3&d4` prefix directly.  The answer is negative through degree `<= 4` in
q1607/q1847/q2087, with deeper prefixes either one-sided field tails or the
same negative row pattern.  This strengthens the packet boundary: extract
normalized Kummer/divisor classes; do not launch GPU A-prefix buckets from
finite-field prefix descent alone.

```text
p27_a_level_kummer_extraction_packet_rows=1/1
```
