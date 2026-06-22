# P27 A/B/K Gamma4/Gamma5 CAS Fixture

Date: 2026-06-22

## Claim

The repeated-gamma question now has an executable Magma fixture:

```text
gamma4^2 = V + 2 on F_A(Unext,V)=0
gamma5^2 = Wnext + 2 on F_A(V,Wnext)=0
```

This is the concrete offline CAS object for deciding whether the f4/f3 and
f5/f4 Kummer classes are related or fresh independent half-covers.

It is not a GPU production object.  The GPU recurrence-coupling run already
killed current sign-word/gamma buckets without a named quotient or source map.

## Fixture

Magma fixture:

```text
research/p27/archive/fixtures/p27_abk_gamma4_gamma5_localized_noR_q7_magma.m
```

Online calculator output:

```text
research/p27/archive/probe_outputs/p27_abk_gamma4_gamma5_localized_noR_q7_magma_20260622.xml
```

Submission command:

```bash
curl -L -s -A 'Mozilla/5.0 Codex p27 research' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode input@research/p27/archive/fixtures/p27_abk_gamma4_gamma5_localized_noR_q7_magma.m \
  --max-time 75 \
  https://magma.maths.usyd.edu.au/xml/calculator.xml \
  | tee research/p27/archive/probe_outputs/p27_abk_gamma4_gamma5_localized_noR_q7_magma_20260622.xml
```

The saved online response is a `504 Gateway Timeout`, so no online
dimension/genus/component result exists.  This is now an offline Magma/Sage
handoff.

## Chart

The fixture uses the same localized no-R source chart as the f3/f4 fixture:

```text
X*iX = 1
(X-1)*iXm = 1
(X+1)*iXp = 1
(T-2X^2)*iTm = 1
(X^2+1)*iX2p = 1
U_den*iU = 1
E_W = 0
T_cover = 0
Bline_relation = 0
first_half_beta = 0
reduced_Unext = 0
H^2 = Unext + 2
```

Then it attaches:

```text
F_A(Unext,V) = 0
gamma4^2 = V + 2
F_A(V,Wnext) = 0
gamma5^2 = Wnext + 2
```

## CAS Questions

1. Normalize the localized no-R repeated-gamma chart.

Required outputs:

```text
dimension, components, reducedness, irreducibility
genus of the relevant selected components
projection degrees to B, Unext, V, and Wnext
obvious sign/reciprocal/deck involutions
```

2. Compare the two Kummer classes.

Required outputs:

```text
div(V+2) and div(Wnext+2) modulo squares
whether gamma5/gamma4 is a square, pullback, translate, coboundary, or norm
whether gamma4 and gamma5 live on one quotient/Prym factor
first quotient map or divisor identity if one exists
```

3. If a relation appears, turn it into a source-denominator test.

Required outputs:

```text
source parameters and denominator
legal rows emitted
prefix depth distribution
target/source_draw versus ordinary X1(16)
```

## Promote / Kill

Promote:

```text
gamma4 and gamma5 become related on a low-genus/sourceable quotient
or a quotient/Prym factor carries repeated selected classes
or an explicit recurrence/coboundary gives a source-normalized win
```

Kill:

```text
gamma4 and gamma5 are fresh unrelated Kummer layers after normalization
the selected components are high-genus/generic with no quotient
the only proposed sampler is a sign-word bucket already killed by GPU
```

## Continue / Kill

```text
continue = run offline Magma/Sage normalization on this fixture
continue = compare gamma4 and gamma5 divisors/classes after component separation
continue = keep GPU recurrence telemetry only as regression instrumentation

kill = online Magma as the extraction engine for this fixture
kill = GPU production from gamma buckets before CAS names a quotient/source
```

## Linked Artifacts

- [P27 A/B/K Symbolic Kummer CAS Brief](p27_abk_symbolic_kummer_cas_brief_20260622.md)
- [P27 A/B/K F4/F5 Transition Count](p27_abk_f4_f5_transition_count_20260622.md)
- [P27 GPU Recurrence-Coupling Telemetry](p27_gpu_recurrence_coupling_20260622.md)
- [P27 Gamma-Chain 20k Telemetry](p27_gamma_chain_p27_20k_telemetry_20260622.md)

```text
p27_abk_gamma4_gamma5_cas_fixture_rows=1/1
```
