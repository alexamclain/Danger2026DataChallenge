# P27 First-Lift Elliptic-Cover Port

Date: 2026-06-21

## Claim

The strongest p25 practical structure ports to p27:

```text
D16(y) = y(y - 2)G(y)
H(y)   = (y - 1)G(y)
G(y)   = (y^2 - 2)(y^2 - 2y + 2)
D16(y)H(y) = G(y)^2 y(y - 1)(y - 2)
```

Inside accepted `X1(16)` nonsplit fibers, the first-lift/domain gate
`H(y)` square can be sourced by the residual elliptic curve

```text
w^2 = y(y - 1)(y - 2)
```

or, with `x = y - 1`,

```text
E: w^2 = x^3 - x.
```

On p27 this is a live practical source for the first halving bit.  It does not
beat sqrt scaling by itself, but it is now the first GPU A/B candidate because
it sources the first gate rather than filtering random `y`.

## P25 Prior Art

The p25 work already established the first-lift boundary:

- `research/p25/evidence/p25_v2_first_lift_gate_structure_20260619.md`
- `research/p25/evidence/p25_v2_first_lift_ecover_sampler_20260619.md`
- `research/p25/evidence/p25_v2_first_lift_ecover_deeper_firstbranch_20260619.md`
- `research/p25/evidence/p25_v2_second_lift_pullback_20260619.md`

Important transfer lesson:

```text
useful = residual elliptic-cover sampler for the first lift
not useful = broad low-degree Legendre labels
not found = cheap y-line character for the second lift
```

P27 inherits that exact first-lift identity.  The question tested here is
whether the actual sampler remains competitive for `p = 10^27 + 103`.

## Commands

Build:

```bash
cc -O3 -o src/pomerance src/pomerance.c
```

Seed 133 A/B:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 133 1000000 x16halvestatsnonsplit \
  > research/p27/archive/probe_outputs/p27_ecover_port_baseline_seed133_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 133 1000000 x16halvestatsnonsplittracedomain \
  > research/p27/archive/probe_outputs/p27_ecover_port_tracedomain_seed133_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 133 1000000 x16halvestatsnonsplitdgate \
  > research/p27/archive/probe_outputs/p27_ecover_port_dgate_seed133_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 133 1000000 x16halvestatsnonsplitecover \
  > research/p27/archive/probe_outputs/p27_ecover_port_ecover_seed133_1M_20260621.txt 2>&1
```

Seed 134 confirmation:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 134 1000000 x16halvestatsnonsplit \
  > research/p27/archive/probe_outputs/p27_ecover_port_baseline_seed134_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 134 1000000 x16halvestatsnonsplitdgate \
  > research/p27/archive/probe_outputs/p27_ecover_port_dgate_seed134_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 134 1000000 x16halvestatsnonsplitecover \
  > research/p27/archive/probe_outputs/p27_ecover_port_ecover_seed134_1M_20260621.txt 2>&1
```

Residual 2-descent support probes:

```bash
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 135 1000000 x16halvestatsnonsplitecoverdescent \
  > research/p27/archive/probe_outputs/p27_ecover_2descent_seed135_1M_20260621.txt 2>&1
/usr/bin/time -p ./src/pomerance 1000000000000000000000000103 136 2000000 x16halvestatsnonsplitecoverdescent \
  > research/p27/archive/probe_outputs/p27_ecover_2descent_seed136_2M_20260621.txt 2>&1
```

## First-Lift A/B Result

Score is:

```text
score(depth) = emitted_rate_Mps * survive_rate_at_depth
```

Seed 133:

```text
mode          rate_Mps  d16_score     d18_score     d20_score     rel_d16  rel_d18  rel_d20
baseline      0.153530  3.561896e-05  9.211800e-06  1.535300e-06  1.000    1.000    1.000
dgate         0.091742  4.146738e-05  1.174298e-05  1.651356e-06  1.164    1.275    1.076
tracedomain   0.091675  4.143710e-05  1.173440e-05  1.650150e-06  1.163    1.274    1.075
ecover        0.110058  4.798529e-05  1.540812e-05  3.962088e-06  1.347    1.673    2.581
```

Seed 134:

```text
mode          rate_Mps  d16_score     d18_score     d20_score     rel_d16  rel_d18  rel_d20
baseline      0.151330  3.813516e-05  9.987780e-06  3.329260e-06  1.000    1.000    1.000
dgate         0.091588  4.542765e-05  1.318867e-05  4.029872e-06  1.191    1.320    1.210
ecover        0.109310  5.006398e-05  1.267996e-05  3.060680e-06  1.313    1.270    0.919
```

Depth 20 is already sparse at 1M, so the robust read is depths 16 and 18:

```text
ecover beats baseline at d16 on both seeds: 1.31x to 1.35x
ecover beats baseline at d18 on both seeds: 1.27x to 1.67x
ecover is competitive with or better than dgate while sampling the first gate
directly
```

## Residual 2-Descent Split

The residual elliptic 2-descent classes did not reveal a second gate.

In the 2M seed 136 run:

```text
class (+,+,+): samples=999088,  d16=0.000558509, d18=0.000134122, d20=0.000028026
class (-,+,-): samples=1000912, d16=0.000527519, d18=0.000125885, d20=0.000027974
```

The split is nearly flat.  The 1M seed 135 run also failed to show a stable
deep advantage; apparent differences moved around as counts became sparse.

This matches the p25 second-lift pullback verdict: the first lift has a clean
elliptic source, but the next lift is not exposed by a visible residual
2-descent class.

## Interpretation

Positive:

```text
The p25 first-lift elliptic-cover source ports to p27.
It is the best current practical GPU A/B candidate.
It amortizes the prior p24/p25 work instead of restarting from label scans.
```

Negative:

```text
This is still a one-bit constant-factor improvement.
The residual elliptic 2-descent split is not the second-bit/tower law.
No sqrt-beating claim follows from ecover alone.
```

## GPU Ask

Ask the GPU agent for same-stream p27 telemetry:

```text
baseline = raw X1(16) nonsplit selected-halving path
candidate A = first-lift elliptic-cover source, E: w^2=x^3-x, y=x+1
candidate B = domain/dgate first-lift filter, as a control
candidate C = ecover plus explicit d2/d3 prefix filters, if cheap
```

Report:

```text
per GPU-second rate
depth/survivor lift
effective survivor lift per GPU-second
whether d2/d3 prefix filters preserve the expected 1/2-per-layer behavior
```

## Continue / Kill

```text
continue = GPU same-stream A/B of baseline vs ecover vs dgate/domain
continue = ecover + explicit d2/d3 prefix telemetry
continue = math search for a source law beyond the first residual elliptic cover

kill = residual elliptic 2-descent classes as the second-gate selector
kill = claiming ecover beats sqrt scaling without a growing tower law
kill = broad low-degree label scans not tied to d_j or an iterated 2-cover
```

## Linked Artifacts

- `research/p27/archive/probe_outputs/p27_ecover_port_baseline_seed133_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_dgate_seed133_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_tracedomain_seed133_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_ecover_seed133_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_baseline_seed134_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_dgate_seed134_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_port_ecover_seed134_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_2descent_seed135_1M_20260621.txt`
- `research/p27/archive/probe_outputs/p27_ecover_2descent_seed136_2M_20260621.txt`

```text
p27_first_lift_ecover_port_rows=1/1
```
