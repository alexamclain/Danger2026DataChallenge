# P27 B-Line Magma Staging Smoke

Date: 2026-06-22

## Claim

The B-line extraction target is now concrete enough for CAS, but the online
Magma calculator is too small for the full normalization path.

The staged q7 legal B-cover saturation succeeds:

```text
BLEGAL_SATURATION_ONLY 1 93
RESULT p27_b_line_legal_saturation_q7 done
```

But heavier online runs time out:

```text
legal B-cover with point/curve/component calls: 504 Gateway Timeout
legal B-cover plus d3 reverse-source equations: 504 Gateway Timeout
```

This means the legal B-line cover is a real dimension-1 object after
saturation, but genus/component extraction and the d3 all-plus cover need
offline Magma/Sage or a more specialized elimination strategy.  Online Magma
is useful as a syntax/saturation sanity check here, not as the main
normalization engine.

## Artifacts

Fixtures:

```text
research/p27/archive/fixtures/p27_b_line_legal_saturation_q7_magma.m
research/p27/archive/fixtures/p27_b_line_legal_cover_q7_magma.m
research/p27/archive/fixtures/p27_b_line_d3_cover_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_legal_saturation_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_legal_saturation_q7_magma_20260622.html
research/p27/archive/probe_outputs/p27_b_line_legal_cover_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_legal_cover_q7_magma_20260622.html
research/p27/archive/probe_outputs/p27_b_line_d3_cover_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_d3_cover_q7_magma_20260622.html
```

Successful command:

```bash
curl -L -S -A 'Mozilla/5.0 Codex p27 research' \
  --data-urlencode input@research/p27/archive/fixtures/p27_b_line_legal_saturation_q7_magma.m \
  https://magma.maths.usyd.edu.au/calc/ \
  -o research/p27/archive/probe_outputs/p27_b_line_legal_saturation_q7_magma_20260622.html
```

The full legal and d3 cover submissions used the same command shape and
returned `504 Gateway Timeout`.

## What The Fixtures Test

The legal B-cover fixture builds the eta=`+1` legal source over `P1_B`:

```text
E: W^2 = X^3 - X
T^2 = X(X^2+1)(X^2+2X-1)
compactD_R: X*R^2 = criterion_num
Bline*(X^2 - 1)^2 = 8X^2
beta^2*U_den^2 = U_num^2 - 4U_den^2
```

and saturates by the known denominator/artifact product:

```text
X*(X-1)*(X+1)*(T-2X^2)*(X^2+1)
```

The d3 fixture then adds:

```text
reverse_x = 0
reverse_Y = 0
```

from the B-line Kummer extraction packet.

## Interpretation

Positive:

```text
The staged legal B-cover reaches a dimension-1 saturated scheme over q7.
The fixture is now concrete and reproducible for external CAS/offline Magma.
The online calculator can at least validate the saturation stage.
```

Negative:

```text
Online Magma cannot compute point/curve/component data for the legal B-cover.
Online Magma cannot handle the full d3 all-plus B-cover fixture.
This reinforces that the B-line moonshot requires offline normalization or
targeted elimination, not web-calculator Curve(S) calls.
```

## Continue / Kill

```text
continue = offline Magma/Sage normalization of the saturated legal B-cover
continue = eliminate over Bline after saturation, not before
continue = compute branch divisor/genus for the d3 cover using specialized CAS

kill = online Magma as the primary B-line normalization workflow
kill = claiming B-line sourceability from finite-field counts alone
kill = further GPU production work before a source/recurrence is extracted
```

```text
p27_b_line_magma_staging_rows=1/1
```
