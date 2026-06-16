# P25 Lane B: Robert KSY Kubert-Lang Anti-Invariant Producer Contract

Updated: 2026-06-13 17:25 PDT

## Purpose

The recent rigidity gates make the anti-invariant normalized-y target rigid.
This note connects that rigid target back to the existing KSY finite producer
spine.

## Accepted Compact Payload

A theorem hit may target:

```text
C = (47,28)
D = (22,3)
K = (57,0), primitive K trace
orientation = forward or reverse
```

It does not need to emit an independent `T` edge:

```text
base = C - D = (25,25)
T    = -2C + K = (38,113)
```

On the quotient `C_3 x C_169`:

```text
C      = (2,28)
base   = (1,25)
D      = (1,3)
T=-2C  = (2,113)
T/2    = -C = (1,141)
```

The derived quotient factor certificate is therefore the existing target:

```text
base=(1,25), D=(1,3), T=(2,113), primitive K
```

## Verified Contract

The integration gate replays:

```text
anti-invariant product intake          = pass
selector rigidity                      = pass
D-slice weight rigidity                = pass
atomic weight rigidity                 = pass
quotient factor certificate            = pass
source quotient packet                 = pass
raw exponent saturation is not selector = pass
```

## First Falsifiers

Reject a theorem/proof/lit hit if it only supplies:

```text
raw KL exponent balance without finite theta2 intake
missing/collapsed/nonprimitive K trace
truncated, wrong, missing, doubled, or reweighted D segment
shifted or inverted center without matching orientation
nonuniform K-layer or atom weights
q-cycle/source-coordinate convention confusion
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_rows=1/1
```

## Interpretation

The current moonshot target is no longer a loose finite pattern.  It is a
compact theorem contract:

```text
prove a challenge-legal Robert/Siegel/Kubert-Lang/KSY identity for the exact
equal-weight K-traced anti-invariant normalized-y product.
```

The finite verifier side is done for this lane; the remaining debt is the
arithmetic producer identity.
