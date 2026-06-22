# P27 Trace/Norm D_plus Cover

Date: 2026-06-21

## Claim

The GPU result promotes trace/norm `D_plus` as the only current structural
search-space narrowing lead: fixed `d2/d3/d4` prefixes do not shrink raw source
scope, while `D_plus` captured all observed depth-20 through depth-30 survivors
in the `1B + 1B` raw-y A/B.

Follow-up:
[P27 Trace/Norm D_plus Prefix Identity](p27_trace_norm_dplus_prefix_identity_20260621.md).
The `4x` lift is now understood as an exact two-gate prefix.  Dplus is still a
useful algebraic cover, but by itself it is not a hidden late-depth recurrence.

This note names the exact p27 cover equation behind `D_plus`.  After the
domain root is present, `D_plus` is exactly one combined squareclass:

```text
t = y - 1
B = t^2 + 1
C = t^2 + 2t - 1
z^2 = t*C*B
eps_h = chi(t)
eps_v = chi((t+1)*C)
hcore = C*B + eps_h*2*t*z
vcore = 2*C*t^2 + eps_v*z*w
core = (1-t^2)*B*C*(t+1)*vcore*hcore
D = -chi(core)
```

Because `p27 mod 4 = 3`, `D_plus` is equivalent to `-core` being square.

## P27 Probe

Gate:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_trace_norm_dplus_cover_probe.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_cover_probe_20260621.txt
```

Result:

```text
usable_rows = 16096
D_+1 = 8128
D_-1 = 7968
core_+1 = 7968
core_-1 = 8128
dplus_cover_square = 8128
dplus_cover_nonsquare = 7968
D_core_mismatch = 0
D_Tline_relation_mismatch = 0
dplus_cover_mismatch = 0
```

The orientation selectors are balanced:

```text
orientation_+1_+1 = 3936
orientation_+1_-1 = 4124
orientation_-1_+1 = 3982
orientation_-1_-1 = 4054
```

## Online Magma Checks

### Domain Spin Quartic

Eliminating `t` from

```text
a = t - 1/t
r^2 = t*(t^2+2t-1)*(t^2+1)
```

gives:

```text
r^4 - (a+2)(a^2+1)(a^2+4)r^2 + (a+2)^2(a^2+4) = 0.
```

Input:

```text
research/p27/archive/fixtures/p27_trace_norm_domain_quartic_q607_magma.m
```

Output:

```text
RESULT p27_domain_quartic_q607 true true 2 667 5
```

Meaning:

```text
elimination identity ok = true
named quartic ok = true
projective genus = 2
affine F_607 points = 667
projective singular points = 5
```

### D_plus Combined Cover

Input:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_cover_q607_magma.m
```

Output:

```text
RESULT p27_dplus_cover_q607 724 436 436 284 4 876 0 188 176 180 180
```

Meaning:

```text
rows = 724
dplus = 436
cover_square = 436
cover_nonsquare = 284
cover_zero = 4
cover_points = 876
mismatch = 0
orientation ++,+-,-+,-- = 188,176,180,180
```

This independently validates that the named `-core` cover is exactly the
finite-field `D_plus` selector on the small p27-compatible field `q=607`.

## Interpretation

Positive:

```text
D_plus now has a concrete source-cover equation.
The domain spin cover is low genus (genus 2 in the q=607 Magma check).
The full D_plus selector is one combined squareclass once the orientation
selectors eps_h and eps_v are fixed.
This is the right mathematical object for the GPU 4x structural narrowing
lead.
```

Follow-up source-orientation pricing:
[P27 Trace/Norm Source-Orientation Cover](p27_trace_norm_source_orientation_cover_20260621.md).
Making `eps_h` and `eps_v` available as square-root data produces a degree-16
genus-21 base and predicted genus 69 after the final `D_plus` square root.  So
the direct full-cover sampler is not the first production route; the live
route is quotient/Prym extraction or recurrence/coupling telemetry.

Follow-up orientation telemetry:
[P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md).
The exact `eps_h/eps_v` phases and nearby `H/VQ/T_line` buckets do not
stably predict `d3` or `d4`; they should remain diagnostic data, not GPU
production filters.

Negative:

```text
The formula still contains eps_h=chi(t) and eps_v=chi((t+1)C).
Those orientation bits explain why the current implementation pays fresh
Legendre costs.
This is not yet a production sampler or a proof of sub-sqrt search.
```

## Concrete Sqrt-Beating Tests

1. Four-component orientation cover:

```text
Split by eps_h, eps_v in {+1,-1}.
For each component, ask Magma/Sage for genus, quotient maps, and Prym/Jacobian
decomposition of:
  w^2 = -(t^2+2t-1)(t^2-2t-1)
  z^2 = t(t^2+2t-1)(t^2+1)
  s^2 = -core
with the relevant orientation constraints.
```

A positive result would be a low-genus quotient or recurrence that samples
`D_plus` directly instead of classifying rejected raw-y draws.

2. Direct GPU sampler target:

```text
Try to generate points on the D_plus cover, or on a quotient of it, and map
them back to ordinary X1(16) candidates.
Promotion bar: raw-source target/source lift beats 1.25x and survives held-out
depth-24/depth-26 telemetry.
```

3. Coupled trace/norm recurrence:

```text
Test whether the D_plus cover class recurs or pushes forward to the next
selected x-square gate, rather than just acting as a one-time 4x stratum.
```

## Continue / Kill

```text
continue = Magma/Sage quotient decomposition of the named D_plus cover
continue = GPU direct-source experiment if a quotient map is found
continue = use this exact core formula for any further D_plus telemetry

kill = treating fixed d2/d3/d4 prefixes as source shrink
kill = searching for D_plus as a tiny R(a) character
kill = using eps_h/eps_v or H/VQ/T_line buckets as post-Dplus filters
kill = promoting current trace/norm classifier as production without a direct
       sampler or cheaper orientation source
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_trace_norm_dplus_cover_probe.py`
- P27 output: `research/p27/archive/probe_outputs/p27_trace_norm_dplus_cover_probe_20260621.txt`
- Magma domain input: `research/p27/archive/fixtures/p27_trace_norm_domain_quartic_q607_magma.m`
- Magma domain output: `research/p27/archive/probe_outputs/p27_trace_norm_domain_quartic_q607_magma_20260621.txt`
- Magma domain XML: `research/p27/archive/probe_outputs/p27_trace_norm_domain_quartic_q607_magma_20260621.xml`
- Magma D_plus input: `research/p27/archive/fixtures/p27_trace_norm_dplus_cover_q607_magma.m`
- Magma D_plus output: `research/p27/archive/probe_outputs/p27_trace_norm_dplus_cover_q607_magma_20260621.txt`
- Magma D_plus XML: `research/p27/archive/probe_outputs/p27_trace_norm_dplus_cover_q607_magma_20260621.xml`
- Related GPU note: [P27 GPU Search-Space Narrowing Probe](p27_gpu_search_space_narrowing_20260621.md)
- Prior spin note: [P27 Trace/Norm Spin Obstruction](p27_trace_norm_spin_obstruction_20260621.md)

```text
p27_trace_norm_dplus_cover_rows=1/1
```
