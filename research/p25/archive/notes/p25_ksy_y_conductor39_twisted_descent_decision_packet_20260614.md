# P25 KSY-y Conductor-39 Twisted-Descent Decision Packet

Updated: 2026-06-14 19:45 PDT

## Purpose

The degree-6 route is real, but not every degree-6 descent is useful.  This
packet separates the dead pure-norm route from the surviving twisted
ratio/Hilbert-90 route.

The routine gate now uses recorded markers for the degree-6 value-descent
packet, expert-answer smoke packet, Frobenius orbit, coset Frobenius pairing,
and Hilbert-90 boundary.  It keeps its own seven route decisions executable
without recomputing those deeper dependency trees.

## Descent Facts

```text
two_conjugate_sum_support              = 0
three_conjugate_sum_equals_word        = 1
six_conjugate_sum_support              = 0
pure_character_degree6_norm_cancels    = 1
Q satisfies Frob_p(Q)=Q^-1             = 1
W=Q^6 satisfies the inverse contract   = 1
balanced_h90_support                   = 24
sparse_h90_support                     = 12
```

Interpretation:

```text
ordinary degree-6 norm of the pure character word = dead
ordinary W + Frob_p(W) pair sum                   = dead
twisted quotient / ratio / Hilbert-90 boundary    = live helper
finite value or divisor theorem + period 156      = source-stage closer
```

## Route Rows

```text
pure_degree6_norm_of_character_word:
  decision = reject_pure_degree6_norm_cancels
  falsifier = six-conjugate additive norm of the pure character word is zero

two_conjugate_pair_sum:
  decision = reject_pair_sum_cancels
  falsifier = Frob_p(W)=-W, so two-conjugate sum has support zero

three_conjugate_shadow:
  decision = helper_only_signed_orbit_shadow_value_theorem_missing
  missing  = finite value/divisor theorem

quotient_Q_frobenius_inverse:
  decision = helper_only_ratio_boundary_value_theorem_missing
  missing  = finite value theorem for the quotient/ratio object

hilbert90_boundary_without_value:
  decision = helper_only_hilbert90_boundary_value_theorem_missing
  missing  = finite value/divisor theorem

twisted_ratio_value_without_period156:
  decision = conditional_value_theorem_missing_period156_context
  missing  = period-156 branch/root/telescoping context

twisted_ratio_period156_value:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing
```

## Counts

```text
route_count              = 7
rejected_rows            = 2
helper_only_rows         = 3
conditional_rows         = 1
source_closing_rows      = 1
period156_closing_rows   = 1
```

## Practical Meaning

If an expert says "take the degree-6 norm," the first question is whether it
is the pure character norm.  If yes, it is killed by cancellation.  A useful
answer must instead name a twisted ratio, quotient, Hilbert-90 preimage, or
non-pure lift whose value/divisor identity survives the alternating Frobenius
signs and carries period-`156` context.

Even that only closes the source theorem stage.  It still needs DANGER3
framing, extraction to `(A,x0)`, and official `vpp.py`.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_twisted_descent_decision_packet_gate.py
```

Marker:

```text
ksy_y_conductor39_twisted_descent_decision_packet_rows=1/1
```

Dependency markers:

```text
ksy_y_conductor39_degree6_value_descent_packet_rows=1/1
ksy_y_conductor39_expert_answer_smoke_rows=1/1
ksy_y_yang_y507_conductor39_frobenius_orbit_rows=1/1
ksy_y_yang_y507_conductor39_coset_frobenius_pairing_rows=1/1
ksy_y_yang_y507_conductor39_hilbert90_boundary_rows=1/1
```
