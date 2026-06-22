# P27 B-Line Second Reduced-Fiber Fixture

Date: 2026-06-22

## Claim

The first `f4/f3` reduced-fiber artifact is now frozen.  After restricting to
legal B rows with `f3=d3=+1`, halving once more, and reducing by
`v=x7+1/x7`, every active B row has:

```text
64 x7 occurrences
16 distinct x7 roots
8 distinct v=x7+1/x7 roots
chi(v+2) = f4(B)
```

This is a concrete CAS handoff for comparing the next selected Kummer class
against the first reduced `f3` cover.  It is not yet a source or GPU bucket.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_second_reduced_fiber_probe.py
```

Probe output:

```text
research/p27/archive/probe_outputs/p27_b_line_second_reduced_fiber_probe_20260622.txt
```

Fixture packet:

```text
research/p27/archive/gates/p27_b_line_second_reduced_fiber_fixture_packet.py
```

Readable packet:

```text
research/p27/archive/probe_outputs/p27_b_line_second_reduced_fiber_fixture_packet_20260622.txt
```

JSON fixture:

```text
research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_second_reduced_fiber_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6,8,10,12,14,16,18,20 \
  --max-power 64 \
  | tee research/p27/archive/probe_outputs/p27_b_line_second_reduced_fiber_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_second_reduced_fiber_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_second_reduced_fiber_fixture_packet_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_second_reduced_fiber_fixture_packet.py \
  --small-primes 1607,1847,2087 \
  --json \
  > research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json
```

## Results

Field summaries:

```text
q1607: rows=28, f4 plus/minus=19/9, occ64=28, x16=28, v8=28
q1847: rows=45, f4 plus/minus=19/26, occ64=45, x16=45, v8=45
q2087: rows=25, f4 plus/minus=18/7, occ64=25, x16=25, v8=25
```

The selector identity held in every row:

```text
q1607: v_plus_2_matches_d4 = 28
q1847: v_plus_2_matches_d4 = 45
q2087: v_plus_2_matches_d4 = 25
```

The coefficient interpolation remains maximal on the sampled legal rows:

```text
q1607: v coeff degrees = 27 for all 8 coefficients
q1847: v coeff degrees = 44 for all 8 coefficients
q2087: v coeff degrees = 24 for all 8 coefficients
```

There were no exact power-sum or reciprocal power-sum selectors through
exponent `64`.  The q1607/q2087 near-75% hits are field/tail artifacts; q1847
has none.

The low-degree plane-relation screen is also negative in the stable systems:

```text
(B,v) and (B,v+2): extra_nullity = 0 through degree 20 in all fields
f4-plus subcover: extra_nullity = 0 through forced interpolation in all fields
```

The only extra relations are tiny minus-tail artifacts:

```text
q1607 f4-minus: extra_nullity = 3 at degree 10, killed at higher forced range
q2087 f4-minus: extra_nullity = 3 at degree 8, killed by q1847
```

## Interpretation

Positive:

```text
The f4-over-f3-plus reduced fiber is now a compact, reusable object.
The next CAS ask is no longer vague: normalize this 8-v cover over the
legal f3-plus B domain and compare its class to the first reduced f3 cover.
```

Negative:

```text
No visible norm, power-sum, coefficient, or low-degree plane relation produces
a sampler.
The fixture does not justify GPU production or another B-bucket search.
```

## Continue / Kill

```text
continue = offline normalize the f4-over-f3-plus 8-v cover
continue = compare its branch/divisor/Kummer class with the f3 reduced cover
continue = use the JSON fixture as the CAS regression packet

kill = visible low-degree plane relations for the second reduced fiber through degree 20
kill = power-sum or reciprocal power-sum selectors through exponent 64
kill = GPU production from second-fiber B buckets before a class/source is named
```

```text
p27_b_line_second_reduced_fiber_rows=1/1
```
