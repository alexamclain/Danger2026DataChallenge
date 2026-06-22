# P27 Trace/Norm Source-Orientation Cover

Date: 2026-06-21

## Claim

The trace/norm `D_plus` cover has a precise equation, but directly sourcing
the two orientation characters is geometrically expensive.  The source cover
that makes

```text
eps_h = chi(t)
eps_v = chi((t+1)C)
```

available as square-root data has genus `21` before the final `D_plus` square
root and predicted genus `69` after it, for every sign component.

This does not kill trace/norm `D_plus`; the GPU A/B still promotes it as the
only current structural narrowing lead.  It does kill the naive direct sampler
"just add the orientation roots and sample the full cover" unless a hidden
quotient/Prym factor is found.

Follow-up context:
[P27 Trace/Norm D_plus Prefix Identity](p27_trace_norm_dplus_prefix_identity_20260621.md).
Since `D_plus` is an exact two-gate prefix, this genus-69 cost should be read
as the cost of directly sourcing that early prefix through the full
orientation cover.  The sqrt-beating route still needs a quotient or recurrence
that reaches post-Dplus gates.

Follow-up context:
[P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md).
The orientation phases themselves were tested against `d3` and `d4`; the
rates stayed near half across seed groups, and the apparent high bucket moved.
So the reason to study this cover is quotient/Prym structure, not direct
orientation-bucket filtering.

Follow-up quotient:
[P27 Trace/Norm Dplus Quotient Symmetry](p27_trace_norm_dplus_quotient_symmetry_20260622.md).
The first visible quotient has now been identified: `Dplus` descends to
`a=t-1/t`, `g=w/t`, `a^2+g^2=4`.  This is a better next CAS target than the
full orientation-source cover, although the tested low-weight quotient
characters do not explain the class.

Follow-up relative-descent correction:
[P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md).
The quotient is conditional on the domain-spin cover because
`Norm_z(-core)=F*S^2`.  So a bare conic sampler is killed; the CAS target is a
relative Hilbert-90/Kummer class over `z^2=F`.

## Cover

Use:

```text
t = y - 1
B = t^2 + 1
C = t^2 + 2t - 1
R = t^2 - 2t - 1
```

The orientation-source base adjoins:

```text
u_h^2 = eps_h * t
u_v^2 = eps_v * (t+1)C
z^2 = t*C*B
w^2 = -C*R
```

The final `D_plus` cover then adjoins:

```text
s^2 = -core
core = (1-t^2)*B*C*(t+1)*vcore*hcore
hcore = C*B + eps_h*2*t*z
vcore = 2*C*t^2 + eps_v*z*w
```

## Online Magma Validation

Input:

```text
research/p27/archive/fixtures/p27_trace_norm_source_orientation_q607_magma.m
```

Output:

```text
RESULT source_orientation_base 21 16
RESULT source_branch_overlap 1 1 12 16 2 2 14 69
RESULT source_branch_overlap 1 -1 12 16 2 2 14 69
RESULT source_branch_overlap -1 1 12 16 2 2 14 69
RESULT source_branch_overlap -1 -1 12 16 2 2 14 69
```

Meaning:

```text
orientation-source base genus = 21
orientation-source base degree over F_q(t) = 16
on M=F_q(t,z,w), odd core branch divisor degree = 16
orientation roots kill branch degree = 2
surviving branch degree on M = 14
pullback surviving branch degree to orientation base = 4*14 = 56
predicted final genus = 2*21 - 1 + 56/2 = 69
```

The calculation is over `q=607`, matching p27's signs `chi(-1)=-1` and
`chi(2)=+1`.

## Interpretation

Positive:

```text
The orientation-source cost is now quantified exactly enough for planning.
The four sign components behave uniformly.
Riemann-Hurwitz gives a concrete final genus prediction instead of a vague
"probably expensive" warning.
```

Negative:

```text
The full direct source cover is not a cheap genus-1/genus-2 sampler.
The two orientation signs are a real geometric cost, not just implementation
bookkeeping.
Current GPU trace/norm filtering remains a classifier until a quotient,
recurrence, or cheaper orientation source is found.
```

## Concrete Next Tests

1. Quotient/Prym extraction:

```text
Ask Magma/Sage for low-genus quotients or Jacobian/Prym decomposition of the
genus-69 orientation components.  The relevant positive artifact is not the
full cover but a quotient map that still remembers D_plus.
```

2. Recurrence/coupling test:

```text
Use GPU telemetry to test whether D_plus pushes forward to later selected
x-square gates.  A recurrence would exploit D_plus without sampling the full
orientation cover.
```

3. Cheaper orientation source:

```text
Look for a way to obtain eps_h and eps_v jointly from the domain spin cover or
trace/norm quotient, rather than adjoining both orientation roots separately.
```

## Continue / Kill

```text
continue = trace/norm D_plus as a structural narrowing lead
continue = exact Kummer/divisor extraction on the Dplus conic quotient
continue = relative Hilbert-90/Kummer extraction over the domain-spin cover
continue = quotient/Prym decomposition of the genus-69 source components
continue = GPU recurrence/coupling telemetry for D_plus versus later gates

kill = direct full-orientation-cover sampler as the first production plan
kill = bare conic quotient as a standalone Dplus sampler
kill = low-weight tested a/g/m quotient-character products
kill = eps_h/eps_v or H/VQ/T_line buckets as post-Dplus GPU filters
kill = treating eps_h and eps_v as free once Dplus is named
kill = another tiny R(a) character scan for Dplus
```

## Linked Artifacts

- Magma input: `research/p27/archive/fixtures/p27_trace_norm_source_orientation_q607_magma.m`
- Magma output: `research/p27/archive/probe_outputs/p27_trace_norm_source_orientation_q607_magma_20260621.txt`
- Magma XML: `research/p27/archive/probe_outputs/p27_trace_norm_source_orientation_q607_magma_20260621.xml`
- Prior D_plus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- Orientation phase screen: [P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md)
- Quotient symmetry: [P27 Trace/Norm Dplus Quotient Symmetry](p27_trace_norm_dplus_quotient_symmetry_20260622.md)
- Relative descent: [P27 Trace/Norm Dplus Relative Descent](p27_trace_norm_dplus_relative_descent_20260622.md)
- GPU narrowing: [P27 GPU Search-Space Narrowing Probe](p27_gpu_search_space_narrowing_20260621.md)

```text
p27_trace_norm_source_orientation_cover_rows=1/1
```
