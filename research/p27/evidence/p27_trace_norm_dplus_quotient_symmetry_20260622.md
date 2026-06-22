# P27 Trace/Norm Dplus Quotient Symmetry

Date: 2026-06-22

## Claim

The trace/norm `Dplus` cover has a real visible quotient, but the descended
class is not a tiny product of the obvious quotient-conic characters.

Positive quotient handle:

```text
Dplus is invariant under z -> -z.
Dplus is invariant under t -> -1/t when paired with w -> -w/t^2.
```

The quotient coordinates are:

```text
a = t - 1/t
g = w/t
a^2 + g^2 = 4
```

This is the first genuinely quotient-shaped positive result in the `Dplus`
lane.  It says the next math target is not the full genus-69 orientation cover
as written; it is the descended Kummer/divisor class on this conic quotient.

Follow-up correction:
[P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md).
The conic quotient is not a free sampler by itself.  Symbolically,
`u=-core=u0+u1*z` satisfies `Norm_z(u)=F*S^2`, where
`F=t(t^2+2t-1)(t^2+1)=z^2`.  Thus the quotient fiber constancy is conditional
on the domain-spin cover.  The live object is a relative Hilbert-90/Kummer
class over `z^2=F`, not a standalone `R(m)`.

Negative shortcut result:

```text
No stable low-weight product of the tested natural a/g/m characters explains
the descended Dplus class across heldout fields.
```

So this is a CAS/theorem handle, not yet a direct GPU source.

## Probes

Symmetry gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_symmetry_probe.py
```

Symmetry output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_symmetry_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_symmetry_probe.py \
  --qs 607,1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_symmetry_probe_20260622.txt
```

Quotient-character gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_quotient_character_probe.py
```

Quotient-character output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_quotient_character_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_quotient_character_probe.py \
  --qs 607,1607,1847,2087 \
  --max-weight 3 \
  --min-coverage 0.98 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_quotient_character_probe_20260622.txt
```

## Symmetry Result

The probe tests the `z/w` deck flips and the domain involution:

```text
z^2 = t(t^2+2t-1)(t^2+1)
w^2 = -(t^2+2t-1)(t^2-2t-1)
iota: t -> -1/t
```

Across `q=607,1607,1847,2087`:

```text
zflip same_rate = 1.000000000
iota_zp_wm same_rate = 1.000000000
iota_zm_wm same_rate = 1.000000000
```

The two invariant `iota` versions differ only by the already-invisible
`zflip`.  The `wflip` and `zwflip` maps are not invariants; they mix `Dplus`
and `Dminus` at about half:

```text
q607  wflip same_rate = 0.502762431
q1607 wflip same_rate = 0.501246883
q1847 wflip same_rate = 0.501084599
q2087 wflip same_rate = 0.500959693
```

Thus the visible quotient is specific, not the whole deck group.

## Quotient Consistency

Using:

```text
a = t - 1/t
g = w/t
a^2 + g^2 = 4
```

the finite-field fibers are consistent:

```text
q607:  quotient_points = 182, fiber_size_4 = 180, fiber_size_2 = 2
q1607: quotient_points = 402, fiber_size_4 = 400, fiber_size_2 = 2
q1847: quotient_points = 462, fiber_size_4 = 460, fiber_size_2 = 2
q2087: quotient_points = 522, fiber_size_4 = 520, fiber_size_2 = 2
```

No fiber conflicts were reported.  Generic fibers have size four, exactly as
expected from `zflip` and the domain involution.

## Character Screen

The quotient conic was parameterized by:

```text
m = g/(a-2)
```

The screen tested low-weight products up to weight `3` from natural atoms in
`a`, `g`, and `m`, requiring at least `0.98` coverage.

The best per-field train scores are small and field-specific:

```text
q607  best = 0.629834254, combo = a2+1,a2-1,m+1
q1607 best = 0.595000000, combo = a+g-1,ag-1,m2-1
q1847 best = 0.599128540, combo = a+g,a-g-1,m2-m+1
q2087 best = 0.574712644, combo = a+g-1,g,g2+1
```

The q607 best combo does not hold out:

```text
q1607 fixed = 0.508728180
q1847 fixed = 0.529284165
q2087 fixed = 0.476007678
```

This is the expected signature of a real relative class whose branch divisor
is not one of the tiny visible products tested here.

## Interpretation

Positive:

```text
Dplus descends through zflip and the domain involution paired with w -> -w/t^2.
The quotient is the genus-0 conic a^2+g^2=4.
This gives a smaller, named CAS target than the full source-orientation cover.
```

Negative:

```text
The descended class is not explained by the tested low-weight a/g/m atoms.
The ordinary wflip does not preserve Dplus.
This is not yet a GPU sampler or a production filter.
```

## Next Test

Compute the exact relative Kummer/divisor class over the domain-spin cover:

```text
z^2 = t*(t^2+2t-1)*(t^2+1)
a = t - 1/t
g = w/t
a^2 + g^2 = 4
```

The decisive artifact would be one of:

```text
1. A relative Hilbert-90 coboundary/Kummer representative for u=-core.
2. A proof that the descended branch divisor is too large/generic to source
   cheaply.
3. A low-genus further quotient or recurrence that couples this class to d3.
```

GPU should not use this yet as a production source.  It becomes GPU-relevant
only after the descended source map or branch divisor is named.

## Continue / Kill

```text
continue = exact Kummer/divisor extraction on the conic quotient
continue = use a=t-1/t, g=w/t as the Dplus quotient coordinates
continue = include the domain-spin cover z^2=F in that extraction
continue = GPU direct-source work only after a source map or branch divisor is
           supplied

kill = searching Dplus as a function of a alone
kill = standalone R(m) search on the bare conic parameter line
kill = low-weight products of the tested a/g/m atoms
kill = wflip or zwflip as Dplus-preserving quotient maps
```

## Linked Artifacts

- Dplus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- Relative descent: [P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md)
- Source-orientation pricing: [P27 Trace/Norm Source-Orientation Cover](p27_trace_norm_source_orientation_cover_20260621.md)
- Orientation phase screen: [P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_quotient_symmetry_rows=1/1
```
