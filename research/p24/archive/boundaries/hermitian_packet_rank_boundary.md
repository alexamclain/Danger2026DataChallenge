# Hermitian Packet Rank Boundary

This note records a finite-field rank diagnostic for the preferred Hermitian
packet scalar.

## Question

Could the Hermitian nonvanishing theorem be reduced to a simple packet-field
rank statement?

For a packet factor `f | Phi_n`, the relative-content vector is

```text
V = (J_0 mod f, ..., J_{m-1} mod f) in (F_q[X]/f)^m.
```

The Hermitian scalar is a norm form in this packet algebra.  A tempting
thought is that the actual CM vector might have a special rank property that
keeps it away from the isotropic cone.

## Corrected Span Diagnostic

I updated:

```text
p24/hermitian_packet_structure_scan.py
```

to report maximal possible base-field span:

```text
rank_Fq(V) = min(m, deg f)
```

rather than the too-strong condition `rank_Fq(V)=deg f`, which is impossible
when `deg f > m`.

Quick run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_packet_structure_scan.py \
  --max-cases 8 --min-h 12 --max-h 80 --max-abs-D 9000 \
  --max-quotients 3 --min-n 5 --q-stop 80000 \
  --random-trials 20 --shuffle-trials 20
```

Summary:

```text
packet_rows=12
cm_hermitian_zero_packets=0
cm_any_zero_coordinate_packets=0
cm_any_zero_term_packets=0
cm_maximal_span_packets=12
cm_span_defect_packets=0
factor_degree_gt_m_packets=7
random_vector_zeros=0
random_vector_span_defects=1
shuffled_cycle_zeros=0
shuffled_cycle_span_defects=0
worst_span_rank_ratio=1.000000
```

So in this window the CM packet vectors have maximal possible span.  But so
do random and shuffled controls almost always.  This is a sanity check, not a
certificate.

## Why Maximal Span Is Not Enough

The existing isotropy toy

```text
p24/energy_isotropy_obstruction_toy.py
```

now reports:

```text
maximal_base_field_span=1
hermitian_energy=(0, 0)
energy_zero=1
```

It gives a full-span vector in a quadratic packet field with zero Hermitian
energy.  Thus maximal packet-field span does not rule out isotropy even in
the smallest relevant model.

## Consequence

The rank-only route is closed:

```text
CM packets appear maximal-rank,
but maximal rank does not imply Hermitian nonvanishing.
```

The missing p24 input is still arithmetic.  A successful theorem must explain
why the actual CM packet vector avoids the Hermitian isotropic cone at the
selected split prime, not merely why it spans a large packet-field subspace.

Pascal's packet-rank sidecar records the same conclusion in determinant
language:

```text
p24/agent_packet_rank_sidecar.md
```

Reduced normality and translate-rank are good diagnostics, but Hermitian
nonvanishing is still a selected-prime isotropy-avoidance theorem.
