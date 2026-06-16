# p24 End-of-Day Conditional Testing

Date: 2026-06-07

Question: do we have enough to start testing inside the search space if we are
willing to fill in proof after a computational success?

## Answer

Yes for the theorem/proof search space; not yet for a completed p24
certificate search space.

The finite verifier is ready, but it still needs a selected p-integral
CM/Lang coordinate or subgroup kernel polynomial as input.  Once that input is
supplied, the reduced-anchor local-unit gate makes the p-unit check exact:

```text
R_c(x)=Phi_c(x)/(x-1)^(c-1) is a unit iff x notin mu_c
K_H(T) is a unit iff T is neither O nor a nonzero point of H
```

For p24, `c=179`, so the forbidden cyclotomic anchor locus has size `179`.
The follow-up resultant-avoidance gate packages the same check as:

```text
gcd(M(T), X(T)^179 - 1) = 1
```

or equivalently:

```text
Res(M(T), X(T)^179 - 1) != 0
```

or a Bezout identity in the selected finite algebra.

## Runs

Harness:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory

task_count=264
passed=264
failed=0
```

Low-moment actual-CM selector sweep:

```text
rows=218
rows_all_unique_within_degree_bound=218
rows_unique_at_degree_one=131
rows_unique_no_later_than_random_entropy=173

additional control:
rows=103
rows_all_unique_within_degree_bound=103
rows_unique_at_degree_one=65
rows_unique_no_later_than_random_entropy=82
```

Selected-prime relative/resultant scan:

```text
packet_rows=23906
unique_packet_rows_ignoring_origin=1248
coord_zero_packets=0
distinguished_zero_packets=0
content_zero_packets=0

additional control:
packet_rows=12211
unique_packet_rows_ignoring_origin=755
coord_zero_packets=0
distinguished_zero_packets=0
content_zero_packets=0
```

Packetized content scan:

```text
packet_rows=23906
unique_packet_rows_ignoring_origin=1248
coord_zero_packets=0
content_failures=0
energy_zero_packets=0
hermitian_zero_packets=0
```

Packet-factor shape scan:

```text
zero_hits=0
prime_zero_hits=0
composite_zero_hits=0
```

## Interpretation

These runs are useful theorem microscopes.  They support the low-moment
selector and product/resultant producer surface, and they found no cheap
selected-prime counterexample or imprimitive recurrence escape in the widened
small-CM window.

They did not produce a p24 DANGER triple.  A large direct Pomerance run remains
a lottery: it can be launched, but it does not test the asymptotic speedup
unless a new producer/filter is supplied.
