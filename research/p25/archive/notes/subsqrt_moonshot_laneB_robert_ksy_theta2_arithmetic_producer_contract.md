# P25 Lane B: Robert KSY/Hilbert-90 Arithmetic-Producer Contract

Updated: 2026-06-13 15:38 PDT

## Purpose

The minimal finite spine tells us which payloads the verifier can consume. This
contract separates those finite payloads from the missing arithmetic theorem.

A future theorem or literature hit is useful only if it emits one of the
accepted interfaces below, or if it emits value-level data together with the
required root/branch selection.

## Accepted Finite Interfaces

```text
hilbert90_two_signs             size 2    accepted
source_quotient_packet          size 6    accepted
quotient_factor_classes         size 3    accepted
source_factor_tuple             size 31   accepted
sparse_theta2_divisor           size 300  accepted
sparse_theta2_inverse_divisor   size 300  accepted
compact_ksy_theta2              size 975  accepted certificate skeleton
```

These are verifier interfaces, not arithmetic proofs. A theorem-side producer
must explain why the object is emitted by a challenge-legal identity rather
than by hand selection.

## Rejected Or Conditional Shortcuts

```text
theta2_value_unit_without_branch   rejected/conditional
plain_bridge_as_theta2             rejected
q_cycle_packet_as_source_packet    rejected
nonprimitive_k_multiplier          rejected
wrong_quotient_d_class             rejected
```

The value-level unit case is conditional because `gcd(4^780-1, p-1) = 11`.
There are eleven `F_p^*` value branches, and the finite source-mask contract
cannot choose among them. This ambiguity is harmless for divisor/additive
payloads but real for multiplicative unit values.

## Normalization Boundary

Divisor/additive theta2 payloads can use the finite resolvent normalization:

```text
support resolvent term budget = 46800
telescoping compact budget    = 975
```

Value-level multiplicative payloads must additionally supply the branch/root
selection. Post-hoc exponent inversion is not available on `F_p^*`.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py
```

Expected marker:

```text
robert_ksy_theta2_arithmetic_producer_contract_rows=1/1
```

## Interpretation

The next moonshot target is now sharply phrased:

```text
find a challenge-legal arithmetic source for one accepted spine interface
```

Useful hits may arrive as Hilbert-90 signs, a source quotient packet, quotient
factor classes, source factor data, sparse theta2 divisor data, or compact
KSY theta2 data. Hits that only match support, use the old q-cycle convention,
use nonprimitive `K`, use wrong `D`, or assert value-level normalization without
branch selection should be rejected immediately.
