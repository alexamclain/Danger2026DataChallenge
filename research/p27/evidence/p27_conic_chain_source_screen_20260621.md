# P27 Conic-Chain Source Screen

Date: 2026-06-21

## Claim

The quadratic gate recurrence gives a genuine low-dimensional chain object.

For `A=2-c^2` and `x_j=r_j^2`, one all-plus legal step is captured by:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

The `h_j` conic is the next x-square gate.  The conjugate `g_j` conic is
needed for legal halving, since:

```text
x_j^2 + A*x_j + 1
  = (r_j^2 + c*r_j + 1)(r_j^2 - c*r_j + 1).
```

Adding another all-plus gate adds three variables and three equations, so the
lifted chain remains dimension `2` in the tested algebraic and finite-field
screens.  This is the strongest source-shaped structure so far.

It is still not a finished beat-sqrt sampler: the chain has not yet been
pulled back to the legal X1(16)/compactD starting surface.

## Artifacts

Finite-field source probe:

```text
research/p27/archive/gates/p27_conic_chain_source_probe.py
research/p27/archive/probe_outputs/p27_conic_chain_source_probe_q103_q263_q607_depth4_20260621.txt
research/p27/archive/probe_outputs/p27_conic_chain_source_probe_q1607_depth2_20260621.txt
```

Magma dimension smoke:

```text
research/p27/archive/fixtures/p27_conic_chain_dimension_q7_magma.m
research/p27/archive/probe_outputs/p27_conic_chain_dimension_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_conic_chain_dimension_q7_magma_20260621.html
```

Legal pullback smoke/count:

```text
research/p27/archive/fixtures/p27_eprime_conic_chain_pullback_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_conic_chain_pullback_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_conic_chain_pullback_q7_magma_20260621.html
research/p27/archive/gates/p27_legal_conic_pullback_count_probe.py
research/p27/archive/probe_outputs/p27_legal_conic_pullback_count_probe_q1607_q1847_q2087_depth2_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_chain_source_probe.py \
  --small-primes 103,263,607 \
  --depth 4 \
  | tee research/p27/archive/probe_outputs/p27_conic_chain_source_probe_q103_q263_q607_depth4_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_chain_source_probe.py \
  --small-primes 1607 \
  --depth 2 \
  | tee research/p27/archive/probe_outputs/p27_conic_chain_source_probe_q1607_depth2_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_legal_conic_pullback_count_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 2 \
  | tee research/p27/archive/probe_outputs/p27_legal_conic_pullback_count_probe_q1607_q1847_q2087_depth2_20260621.txt
```

## Algebraic Smoke

Online Magma over q7:

```text
CONIC_CHAIN_DEPTH1 2 3 62
CONIC_CHAIN_DEPTH2 2 6 128
System Error: User memory limit has been reached
RESULT p27_conic_chain_dimension_q7 done
```

Interpretation:

```text
depth 1: dimension 2
depth 2: dimension 2
depth 3: too heavy for web Magma, but not contradicted
```

The full E-prime legal pullback fixture also exceeds the web memory limit
before a dimension checkpoint:

```text
System Error: User memory limit has been reached
RESULT p27_eprime_conic_chain_pullback_q7 done
```

So online Magma is not the right normalization path for the combined legal
pullback.

## Finite-Field Counts

Depth 4 over moderate fields:

```text
q103:
  step1 outputs/q^2 = 0.5001
  step2 outputs/q^2 = 0.4721
  step3 outputs/q^2 = 0.4536
  step4 outputs/q^2 = 0.4445
  xdouble mismatches = 0 at every step

q263:
  step1 outputs/q^2 = 0.5000
  step2 outputs/q^2 = 0.4888
  step3 outputs/q^2 = 0.4813
  step4 outputs/q^2 = 0.4748
  xdouble mismatches = 0 at every step

q607:
  step1 outputs/q^2 = 0.5000
  step2 outputs/q^2 = 0.4951
  step3 outputs/q^2 = 0.4915
  step4 outputs/q^2 = 0.4867
  xdouble mismatches = 0 at every step
```

P27-signature guard field q1607 at depth 2:

```text
q1607:
  step1 outputs/q^2 = 0.500000581
  step2 outputs/q^2 = 0.498138008
  step1 lifts/q^2 = 1.998756219
  step2 lifts/q^2 = 7.977646025
  xdouble mismatches = 0
```

Legal-source pullback counts over p27-signature guard fields:

```text
q1607:
  legal candidates = 784
  d3 plus/minus = 448/336
  depth1 candidates with conic lift = 448
  depth1 matches d3-plus indicator = 784/784
  d4 plus/minus after d3 = 304/144
  depth2 candidates with conic lift = 304
  depth2 matches d4-plus indicator after d3 = 448/448

q1847:
  legal candidates = 1008
  d3 plus/minus = 720/288
  depth1 candidates with conic lift = 720
  depth1 matches d3-plus indicator = 1008/1008
  d4 plus/minus after d3 = 304/416
  depth2 candidates with conic lift = 304
  depth2 matches d4-plus indicator after d3 = 720/720

q2087:
  legal candidates = 912
  d3 plus/minus = 400/512
  depth1 candidates with conic lift = 400
  depth1 matches d3-plus indicator = 912/912
  d4 plus/minus after d3 = 288/112
  depth2 candidates with conic lift = 288
  depth2 matches d4-plus indicator after d3 = 400/400
```

## Interpretation

Positive:

```text
The lifted all-plus chain is not losing a fresh dimension per gate.
The output projection to (c,r_j) stays near half of the plane through the
tested depths, and the lifted multiplicity grows as expected.
The transition equation always doubles back correctly under Montgomery xDBL.
On actual legal label-2 / compactD rows, the conic-chain lift is not merely
analogous to d3/d4; it is equivalent to d3/d4 in the tested guard fields.
```

Important caveat:

```text
The projection to a starting pair (c,r0) does thin: about 0.19 q^2 starts have
a first lift in the tested fields.  The source object is the lifted chain, not
just a naive scan over (c,r0).
```

Still missing:

```text
The legal X1(16)/compactD starting constraint is now count-verified against
the conic-chain lift, but not normalized as a low-genus model.
No low-genus model or parametrized walk for the combined legal source is known.
The chain alone does not yet produce a DANGER3 certificate.
```

## Concrete Next Tests

```text
1. Replace the memory-heavy E-prime legal pullback fixture with a staged
   elimination/quotient: first impose `A=2-c^2` and `x5=r0^2`, then add the
   conjugate conics, then compute dimension/components.

2. Derive a rational parametrization of the one-step pair surface:
     h^2 + g^2 = 2*r^2 + 2,
     c = (h^2 - g^2)/(2*r),
   then test whether the r_next relation is a low-genus correspondence or a
   fresh double cover.

3. If the legal pullback remains dimension >=1 with manageable genus, ask the
   GPU agent for a sampler/probe over the conic-chain coordinates.
```

## Continue / Kill

```text
continue = legal X1(16)/compactD pullback to conic-chain coordinates
continue = low-genus/sourceability test for the r_next correspondence
continue = finite-field guard counts after adding the legal source equations

kill = claiming beat-sqrt from the conic chain before legal pullback
kill = scanning only (c,r0) as if the lifted chain multiplicity did not matter
kill = treating the h conic alone as legal without the conjugate g conic
```

```text
p27_conic_chain_source_screen_rows=1/1
```
