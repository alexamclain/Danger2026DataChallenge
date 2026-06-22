# P27 BSM Surface Incidence Probe

Date: 2026-06-22

## Claim

The staged surface

```text
m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
```

is a useful CAS coordinate, but it is not a source shrink.

Over q1607/q1847/q2087, the surface has about `q^2` points.  It contains the
canonical legal d3-plus `(B,A,x)` rows, and no canonical d3-minus rows, but it
hits those rows at `constant/q` density:

```text
q1607: d3plus_bax_rate_times_q = 0.559
q1847: d3plus_bax_rate_times_q = 0.781
q2087: d3plus_bax_rate_times_q = 0.384
```

So the surface is another exact model of the one-step conic pullback.  It does
not solve the sparse legal B-domain denominator, and does not justify GPU
production by itself.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_bsm_surface_incidence_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_bsm_surface_incidence_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_bsm_surface_incidence_probe_q1607_q1847_q2087_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_bsm_surface_incidence_probe.py \
  --small-primes 607 \
  | tee research/p27/archive/probe_outputs/p27_bsm_surface_incidence_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_bsm_surface_incidence_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_bsm_surface_incidence_probe_q1607_q1847_q2087_20260622.txt
```

## Results

Surface size:

```text
q1607: surface_points = 2576024, surface_points/q^2 = 0.997512052
q1847: surface_points = 3404024, surface_points/q^2 = 0.997835205
q2087: surface_points = 4347224, surface_points/q^2 = 0.998084062
```

Canonical d3-plus incidence:

```text
q1607:
  d3plus_ax = 112
  surface_d3plus_bax_points = 896
  surface_unique_d3plus_bax = 112
  d3plus_bax_rate_on_surface = 0.000347823
  d3plus_bax_rate_times_q = 0.558951314

q1847:
  d3plus_ax = 180
  surface_d3plus_bax_points = 1440
  surface_unique_d3plus_bax = 180
  d3plus_bax_rate_on_surface = 0.000423029
  d3plus_bax_rate_times_q = 0.781334092

q2087:
  d3plus_ax = 100
  surface_d3plus_bax_points = 800
  surface_unique_d3plus_bax = 100
  d3plus_bax_rate_on_surface = 0.000184025
  d3plus_bax_rate_times_q = 0.384061185
```

Legal B incidence:

```text
q1607: legal_B_rate_on_surface = 0.030033882
q1847: legal_B_rate_on_surface = 0.034333483
q2087: legal_B_rate_on_surface = 0.027425318
```

The legal B restriction is a constant-factor improvement only if the legal
B-domain is already available.  It is not a direct below-sqrt source.

## Interpretation

Positive:

```text
The surface captures all canonical d3-plus target rows in the guard fields.
On legal canonical B/A/x rows, the surface is selecting the d3-plus side.
The equation is a good input for staged normalization/component work.
```

Negative:

```text
The surface itself is essentially q^2-sized.
Canonical d3-plus incidence is still constant/q.
The legal B-domain remains the real source denominator.
```

Thus the next math test should add the legal B-cover or its normalized
function-field class to this surface, rather than sampling the surface on GPU.

Update:
[P27 BSM Halving-Cover Identity](p27_bsm_halving_cover_identity_20260622.md)
shows that this surface is exactly the ordinary selected-halving cover in
different coordinates.  With `A=B^2-2`, `x=m^2/16`, and `z=s^2`, the equation
has discriminant `16*(x^2+A*x+1)`.  So the incidence result should be read as
"BSM repackages the x-square plus halving-discriminant-square condition," not
as a new source surface.

## Continue / Kill

```text
continue = staged CAS: surface + legal B-domain + next Kummer selector
continue = look for low-genus quotient/components after imposing legal B
continue = use the surface as a compact handoff equation for expert review
continue = only use BSM after adding a genuinely non-inherited selector

kill = GPU sampling of the raw BSM surface
kill = treating legal-B restriction as a source unless legal B itself is sourced
kill = further raw incidence counts without a new quotient or selector
kill = BSM as an independent source surface
```

```text
p27_bsm_surface_incidence_rows=1/1
```
