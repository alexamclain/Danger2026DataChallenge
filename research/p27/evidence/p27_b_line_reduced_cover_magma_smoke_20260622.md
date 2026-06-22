# P27 B-Line Reduced-Cover Magma Smoke

Date: 2026-06-22

## Claim

The reduced B-line d3 cover is now a concrete Magma fixture, but the online
Magma calculator cannot saturate even the q7 reduced model within its memory
limit.

This confirms the current boundary:

```text
continue = offline Magma/Sage normalization or specialized elimination
kill    = relying on the online calculator for reduced-cover extraction
kill    = launching a large GPU run before a source/recurrence is extracted
```

## Artifacts

Fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_cover_saturation_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_saturation_q7_magma_20260622.html
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_saturation_q7_magma_20260622.txt
```

## Command

```bash
curl -L -S -A 'Mozilla/5.0 Codex p27 research' \
  --data-urlencode input@research/p27/archive/fixtures/p27_b_line_reduced_cover_saturation_q7_magma.m \
  https://magma.maths.usyd.edu.au/calc/ \
  -o research/p27/archive/probe_outputs/p27_b_line_reduced_cover_saturation_q7_magma_20260622.html
```

## Result

The calculator terminated during:

```text
Isat := Saturation(I, bad);
```

with:

```text
The computation exceeded the memory limit and so was terminated prematurely.
Current total memory usage: 357.1MB, failed memory request: 32.0MB
System Error: User memory limit has been reached
Runtime error: Variable 'Isat' has not been initialized
```

The run used Magma V2.29-8 and stopped after about `10.269s` with total memory
usage `357.09MB`.

## Interpretation

Positive:

```text
The reduced-cover fixture is explicit and submit-ready.
The obstruction is now a real CAS resource boundary, not an undefined formula.
This is a better handoff for Drew/offline Magma/Sage than the full reverse z/Y
cover.
```

Negative:

```text
The online calculator cannot even finish the q7 reduced saturation.
No genus, component, branch divisor, quotient, or sampler was extracted.
This gives no reason to promote a large GPU run.
```

## Continue / Kill

```text
continue = offline normalization of the reduced 4-u / 8-x cover
continue = try variable elimination over Bline/A/Sroot before full saturation
continue = compare the extracted f3 class with f4/f3 only after d3 normalizes

kill = online Magma as the extraction engine for this cover
kill = GPU production from the quadratic-gate or B-line bucket evidence alone
```

```text
p27_b_line_reduced_cover_magma_smoke_rows=1/1
```
