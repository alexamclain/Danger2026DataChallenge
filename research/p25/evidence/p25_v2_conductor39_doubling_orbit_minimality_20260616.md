# P25 v2 Conductor-39 Doubling-Orbit Minimality

Updated: 2026-06-16

## Purpose

Promote one more guardrail for the unified H0/conductor-39 theorem target:
the conductor-39 source can be described from the seed ratio `E_7/E_1`, but
only inside the full 12-step doubling-orbit norm.  Proper suborbits are not
legal standalone `X_1(39)` modular units.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_doubling_orbit_minimality_20260614.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_conductor39_doubling_orbit_minimality_gate.py
```

The gate returned `p25_v2_conductor39_doubling_orbit_minimality_rows=1/1`.

## Orbit Norm

```text
seed ratio = E_7 / E_1
orbit length = 12
orbit support = 24
single_seed_ratio_descends = no
full_orbit_required = yes
Frob_p(full orbit norm) = inverse
```

So the seed is useful notation, but it is not a legal descent by itself.

## Proper Suborbit Screen

All proper doubling suborbit candidates were checked:

```text
proper_rows = 27
proper_legal_rows = 0
proper_elementary_congruence_rows = 9
proper_signed_orbit_failure_rows = 9
full_orbit_forced_by_yang_yu = yes
```

The shorter candidates fail in two ways:

```text
length 1 and 2:
  fail quadratic congruence modulo 39

length 3, 4, and 6:
  may pass elementary congruences
  fail the Yang/Yu signed-orbit condition at prime 3
```

The only legal row is the full length-12 orbit.

## Meaning

This kills a natural cheap theorem shape:

```text
seed ratio E_7/E_1
or proper doubling suborbit
as standalone conductor-39 modular unit
```

A source theorem may still use the seed ratio as a producer, but only if it
keeps the full 12-step doubling norm or supplies an explicit boundary/ratio
repairing the Yang/Yu failure.

## Verdict

```text
continue_conductor39 = yes
shortcut_remaining = no
positive_artifact = full 12-step doubling norm is the minimal legal source
remaining_gap = finite arithmetic value/divisor theorem for the full
                12-step doubling norm, not a seed or proper-suborbit shortcut
discard_condition = any proposal using E_7/E_1 or a proper suborbit as a
                    standalone source unit without repairing legality
```
