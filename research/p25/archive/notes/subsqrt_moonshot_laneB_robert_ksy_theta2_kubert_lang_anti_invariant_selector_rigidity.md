# P25 Lane B: Robert KSY Kubert-Lang Anti-Invariant Selector Rigidity

Updated: 2026-06-13 17:11 PDT

## Purpose

The raw KL exponent screen is saturated for anti-invariant packets, so exponent
balance is not a selector.

This gate asks whether the finite quotient packet itself is rigid.

## Result

Scanning every center and `D` step in `C_3 x C_169`:

```text
centers scanned = 507
D steps scanned = 507
pairs scanned   = 257049
```

The forward `theta2^-1` packet has exactly two matches:

```text
C=(2,28), D=(1,3)
C=(2,28), D=(2,166)  # D reversal
```

The reverse `theta2` packet has exactly two matches:

```text
C=(1,141), D=(1,3)   # inverse center
C=(1,141), D=(2,166) # inverse center, D reversal
```

Support-only matching gives no extra unsigned hits, and `D=0` gives no match.

## Raw Validation

The four quotient survivors all validate against the existing raw
theta2/resolvent path:

```text
(47,28), D=(22,3)    -> theta2^-1, sign -1
(47,28), D=(53,166)  -> theta2^-1, sign -1
(28,141), D=(22,3)   -> theta2, sign +1
(28,141), D=(53,166) -> theta2, sign +1
```

Here `(53,166)=-D` and `(28,141)=-C` in `C_75 x C_169`.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_rows=1/1
```

## Interpretation

The accepted anti-invariant packet is not a loose KL-congruence family.  It is
rigid up to the two unavoidable symmetries: orientation/inversion of the center
and reversal of the length-three `D` segment.

A theorem or literature hit must emit this rigid `C,D,K` packet, or an exactly
equivalent theta2 payload.  Merely producing an exponent-balanced
anti-invariant divisor is not enough.
