# Fixed-Frequency p24 Projector/Internal-Trace Pipeline Gate

Date: 2026-06-06

## Point

The current fixed-frequency proof frontier has several formal layers:

```text
projector internal trace zero
  -> matching right coboundary
  -> product coboundary
  -> six nontrivial right-character payloads vanish
  -> ordinary centering plus those six payloads
  -> 1092 H-coset scalar verifier
```

The new Lean gate packages this chain so the remaining arithmetic theorem is
visible as one input:

```text
for every nontrivial right quotient projector, the final internal trace of
the actual weighted CM/Lang obstruction is zero.
```

## Lean Gate

```text
p24/lean/TraceGcdProjectorTracePipelineGate.lean
```

It proves:

```text
AllProjectorInternalTraceZero
  -> AllCharacterPayloadZero

AllProjectorInternalTraceZero
  -> AllRowsCentered
  -> AllHCosetSumsZero
```

under the already-isolated formal hypotheses:

```text
final internal trace zero gives matching right coboundary;
matching right coboundary gives product coboundary;
product coboundary kills character payload;
centering plus character payloads gives H-coset zeroes.
```

## p24 Counts

The gate pins the counts:

```text
six nontrivial character payloads: 6 * 156 = 936
ordinary centering coordinates:   156
H-coset verifier coordinates:     7 * 156 = 1092
raw packet product terms:         6 * 10 * 7 = 420
1092 < sqrt(10^24 + 7)
```

## Consequence

This does not prove the arithmetic trace identity.  It removes ambiguity about
what remains: prove the zero final internal trace for the six projected
weighted `G_chi` CM/Lang obstruction packets.  After that, the fixed-frequency
H-coset verifier follows formally.
