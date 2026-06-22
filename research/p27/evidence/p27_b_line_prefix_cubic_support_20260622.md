# P27 B-Line Prefix Cubic Support Screen

Date: 2026-06-22

## Claim

The direct genus-1 cubic source for combined B-line all-plus prefixes is
negative in the p27-signature promotion fields `q=1607,1847,2087`.

This is distinct from the earlier cubic screen for individual selectors.  Even
if `d3(B)` and `d4(B)` are separately generic, a single low-genus source could
still have selected the combined prefix:

```text
legal B and d3=+1 and d4=+1
```

The exact screen tests whether each all-plus prefix subset is the squareclass
of a monic cubic:

```text
chi(B^3 + aB^2 + bB + c)
```

with global polarity allowed.  A positive for gate4 would be a genus-1 source
candidate enforcing two selected gates at once.  No such cubic exists in the
promotion fields.

## Artifacts

Gate:

```text
research/p27/archive/gates/p27_b_line_prefix_cubic_support_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_prefix_cubic_support_probe_q1607_q1847_q2087_gate5_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_cubic_support_probe.py \
  --small-primes 1607,1847,2087 \
  --max-gate 5 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_cubic_support_probe_q1607_q1847_q2087_gate5_20260622.txt
```

## Results

For gate3, this reproduces the earlier `d3(B)` cubic negative:

```text
q1607 gate3: plus/minus = 28/21, exact cubics = 0
q1847 gate3: plus/minus = 45/18, exact cubics = 0
q2087 gate3: plus/minus = 25/32, exact cubics = 0
```

For the decisive combined gate4 prefix:

```text
q1607 gate4: plus/not-plus = 19/30, exact cubics = 0
q1847 gate4: plus/not-plus = 19/44, exact cubics = 0
q2087 gate4: plus/not-plus = 18/39, exact cubics = 0
```

For gate5:

```text
q1607 gate5: plus/not-plus = 19/30, exact cubics = 0
q1847 gate5: one-sided zero-plus tail, skipped as a selector
q2087 gate5: plus/not-plus = 18/39, exact cubics = 0
```

The q1607/q2087 small-field plateaus through gate5 therefore do not come from
a visible monic cubic prefix selector.

## Interpretation

Positive:

```text
The test targets the right moonshot shape: one B-line source enforcing multiple
selected gates at once.
The exact solver rules out the nearest genus-1 combined-prefix shortcut.
```

Negative:

```text
No monic cubic selects the d3+d4 all-plus prefix on legal B.
No monic cubic explains the q1607/q2087 gate5 plateaus.
The B-line plateau artifacts are not visible cubic source laws.
```

This pushes the B-line route farther away from visible low-degree source
support and toward actual Kummer/divisor-class extraction or a non-obvious
recurrence among the `f_j(B)` classes.

## Continue / Kill

```text
continue = offline B-line divisor/Kummer extraction
continue = specialized elimination over Bline after legal-cover saturation
continue = recurrence/coupling only if it uses extracted f_j(B) classes

kill = monic cubic source for the combined gate4 prefix
kill = monic cubic explanation of q1607/q2087 gate5 plateaus
kill = GPU production from B prefix buckets without an extracted source
```

```text
p27_b_line_prefix_cubic_support_rows=1/1
```
