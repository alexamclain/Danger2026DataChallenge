# P27 K/A Base-Curve Magma Validation

Date: 2026-06-22

## Claim

Online Magma independently validates the explicit K/A base curve and its
B-rationalized branches over q607.

This strengthens the base-curve staging result but does not promote GPU
production.  The K/A base is clean; the remaining sqrt-beating problem is the
additional legal/d3 cover over that base.

## Artifacts

Input:

```text
research/p27/archive/fixtures/p27_ka_base_curve_q607_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_ka_base_curve_q607_magma_20260622.xml
research/p27/archive/probe_outputs/p27_ka_base_curve_q607_magma_20260622.txt
```

Command:

```bash
curl -L -s -A 'Mozilla/5.0 Codex p27 research' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode input@research/p27/archive/fixtures/p27_ka_base_curve_q607_magma.m \
  https://magma.maths.usyd.edu.au/xml/calculator.xml \
  | tee research/p27/archive/probe_outputs/p27_ka_base_curve_q607_magma_20260622.xml \
  | perl -0777 -ne 'while (/<line>(.*?)<\/line>/gs) { $x=$1; $x =~ s/&lt;/</g; $x =~ s/&gt;/>/g; $x =~ s/&amp;/&/g; print "$x\n" }' \
  | tee research/p27/archive/probe_outputs/p27_ka_base_curve_q607_magma_20260622.txt
```

## Result

```text
RESULT p27_ka_base_q607 ok 607 604 3 0 1208 0 0 0
```

Meaning:

```text
base_KA = 607
B-parameter covered KA = 604
base points missing from B chart = 3
B-chart points outside base = 0
B-chart rooted parameter rows = 1208
base equation mismatches = 0
B-branch equation mismatches = 0
discriminant-factor mismatches = 0
```

The three missing base points are the expected degenerate points outside the
nonzero B chart `B != 0, +/-2`.

## Interpretation

Positive:

```text
The K/A base equation is independently validated.
The discriminant factorization is validated over q607.
The B rationalization covers exactly the nondegenerate base chart and adds no
spurious K/A points.
```

Negative for sqrt beating:

```text
This does not identify the sparse legal subset.
This does not make base-curve sampling a GPU source.
The live object remains the legal/d3 cover over the K/A or Sroot base.
```

## Continue / Kill

```text
continue = normalize the additional legal cover over the validated K/A base
continue = use B/Sroot charts as CAS coordinates for branch extraction
continue = seek a genus <= 1 quotient, recurrence, or direct legal sampler

kill = blaming K/A equation mismatch for the missing source shrink
kill = direct GPU sampling of the base curve without the legal cover
kill = treating the three B-chart degeneracies as a hidden large source
```

```text
p27_ka_base_curve_magma_validation_rows=1/1
```
