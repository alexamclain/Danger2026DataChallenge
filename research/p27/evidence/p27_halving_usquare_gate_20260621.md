# P27 Halving U+2 X-Square Gate

Date: 2026-06-21

## Claim

For a successful Montgomery halving step, the next x-square gate can be tested
before materializing the two half x-coordinates.

If:

```text
x' + 1/x' = u
```

then the two half roots have product `1`, and:

```text
chi(x') = chi(u + 2) = chi(u - 2)
```

when the roots are defined and nondegenerate.

Since the p27 nonsplit tower has:

```text
chi(d_next) = chi(x_next)
```

this gives a concrete prefix-gate formula:

```text
next gate passes <=> chi(u + 2) = +1
```

after the successful `w = u^2 - 4` branch has been identified.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_halving_usquare_gate_probe.py \
  --target 5000 \
  --max-draws 1000000 \
  | tee research/p27/archive/probe_outputs/p27_halving_usquare_gate_probe_20260621.txt
```

The probe reuses the p27 compactD sample:

```text
sampled_pairs = 5000
total compactD/d2 roots = 10000
```

and checks d2-to-d3 and d3-to-d4.

## Result

d2 to d3:

```text
roots = 10000
good_records = 10000
x_count = 20000
product_mismatch = 0
uplus_mismatch = 0
uminus_mismatch = 0
uplus_uminus_mismatch = 0
next_d_mismatch = 0

chi(u+2)=-1 count = 5068
chi(u+2)=+1 count = 4932
reject_before_sqrt_w_share = 0.506800000
```

d3 to d4:

```text
d3plus_x6 = 9864
good_records = 9864
x_count = 19728
product_mismatch = 0
uplus_mismatch = 0
uminus_mismatch = 0
uplus_uminus_mismatch = 0
next_d_mismatch = 0

chi(u+2)=-1 count = 4760
chi(u+2)=+1 count = 5104
reject_before_sqrt_w_share = 0.482562855
```

So `chi(u+2)` exactly matches the next x-square / next-d gate in the sampled
compactD stream, but the rates are still random-looking half-losses.

## Derivation

The half roots are:

```text
x'_+ = (u + sqrt(u^2 - 4))/2
x'_- = (u - sqrt(u^2 - 4))/2
```

Then:

```text
x'_+ * x'_- = 1
```

If `x'=r^2`, then:

```text
u + 2 = x' + 1/x' + 2 = (r + 1/r)^2
u - 2 = x' + 1/x' - 2 = (r - 1/r)^2
```

Conversely, if `u+2` is square and the quadratic for `x'` splits, then `x'`
is square.  Thus `chi(x')=chi(u+2)`.  The same argument gives `chi(u-2)`
because `(u+2)(u-2)=u^2-4` is square on the successful branch.

## Practical Use

This is a prefix-filter cost test, not a sqrt-beating theorem by itself.

After a gate has passed and the successful `w` branch is known, GPU can test:

```text
chi(u + 2)
```

before computing `sqrt(w)` and materializing `x_next`.  In the measured p27
compactD stream, this would reject about half of d3 or d4 attempts before the
next branch root:

```text
d3 reject share = 0.5068
d4 reject share = 0.4826
```

The p26 filter-cost lesson applies: promote this only if it improves effective
survivors per GPU-second after accounting for the Legendre/sqrt cost.

## Moonshot Consequence

The x-square tower can now be phrased as an iterated sequence of named
characters:

```text
chi(u_j + 2) = +1
```

on the selected nonsplit halving path.

The remaining sqrt-beating problem is to find a source, theorem, theta
identity, or Kummer recurrence that couples many of these `u_j+2` characters at
once.  Independent `u_j+2` filtering remains a constant-factor prefix filter.

Follow-up recurrence screen:
[P27 U+2 Sequence Recurrence Screen](p27_usquare_sequence_recurrence_20260621.md).
On 30,000 compactD/d2 rows, the selected `u+2` sequence showed half-loss rates
through the first several prefix gates and no anomaly:

```text
gate 3 plus_rate = 0.500133333
gate 4 plus_rate = 0.497467342
gate 5 plus_rate = 0.496516613
gate 6 plus_rate = 0.500269833
```

So compactD does not by itself bias the later `u+2` sequence.

Follow-up norm/coboundary screen:
[P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md).
The norm identities through the two `s^2=d` branches are exact:

```text
Norm_s(u+2) = 4*x*(2-A)
Norm_s(u-2) = -4*x*(A+2)
Norm_s(u^2-4) = 16*x^2*(A^2-4)
```

But the selected `w`-square branch's `u+2` bit is not visible in the local
`A,x` norm/branch span.  The best 30k-row d3 score was only `0.5018`; the best
d4 score was `0.5025`.

## Continue / Kill

```text
continue = GPU A/B for u+2 precheck before sqrt(w) in d3/d4 prefix filters
continue = symbolic recurrence search for chi(u_j+2) across successive gates
continue = reverse-doubling all-plus source / non-visible H90 quotient
continue = expert ask framed as iterated Kummer characters chi(u_j+2)

kill = expecting compactD alone to bias the later u+2 sequence
kill = local A,x norm-character selector for selected u+2
kill = small selected-orientation product span for selected u+2
kill = treating independent u+2 filters as sqrt-beating
kill = branch-choice selector after the u+2 identity
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_halving_usquare_gate_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_halving_usquare_gate_probe_20260621.txt`
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)
- Related: [P27 U+2 Sequence Recurrence Screen](p27_usquare_sequence_recurrence_20260621.md)
- Related: [P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md)
- Related: [P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md)
- Related: [P27 X-Square / 2-Descent Gate](p27_xsquare_2descent_gate_20260621.md)
- Related: [P27 GPU Filter-Cost Lesson From P26](p27_gpu_filter_cost_lesson_from_p26_20260621.md)

```text
p27_halving_usquare_gate_rows=1/1
```
