# P27 Line Half-Norm And Joint Stratum

Date: 2026-06-21

## Claim

The p27 `domain_line` bit is best understood as a half-norm squareclass on the
double cover `t -> a = t - 1/t`, not as an ordinary low-degree rational
Legendre character in `a`.  This explains why the visible rational-character
screens are negative.

The simultaneous target also simplifies: `T_line` is only defined on the
`domain_line = +1` rows in this trace/norm construction, so the joint `++`
problem is exactly the problem of selecting `T_line = +1` inside the domain.
There is no separate product-bit shortcut in the visible character span.

## Algebra

Let:

```text
t = y - 1
a = t - 1/t
F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

Then:

```text
F = t(t^2 + 2t - 1)(t^2 + 1)
t^2 = a t + 1
t^2 + 2t - 1 = (a + 2)t
t^2 + 1 = a t + 2
```

So:

```text
F = (a + 2)t^2(t^2 + 1)
chi(F) = chi((a + 2)(t^2 + 1))
```

Under the quotient involution:

```text
sigma(t) = -1/t
sigma(t^2 + 1) / (t^2 + 1) = 1/t^2
```

which is a square.  Therefore the squareclass of `t^2 + 1` descends to the
`a`-line even though it is not represented by an obvious rational function of
`a`.  Its norm is:

```text
Norm(t^2 + 1) = a^2 + 4
```

This is the right shape for a half-norm / descent torsor, not a tiny
`chi(R(a))` formula.

## Joint Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_line_joint_character_span_gate.py
```

Run:

```bash
python3 research/p27/archive/gates/p27_line_joint_character_span_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 256 \
  --max-records 8192 \
  --prefix-size 2048 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_line_joint_character_span_64tid_2chunk_256draw_8192rows_20260621.txt
```

## Result

Sample:

```text
raw_draws = 32768
nonsplit_y = 16432
k_points = 32864
domain_records = 16432
target_records = 8048
joint_records = 8048
joint_++ = 4068
joint_+- = 3980
joint_-+ = 0
joint_-- = 0
domain_inconsistent = 0
target_line_inconsistent = 0
```

The `joint_-+ = joint_-- = 0` lines are the bookkeeping point: joined target
rows are precisely the domain-positive rows.

Product span:

```text
rows = 8048
product_+1 = 4068
product_-1 = 3980
candidate_count = 65536
prefix_exact_survivors = 0
full_exact_count = 0
best_lift = 1.029794807
```

Joint `++` selector:

```text
baseline = 0.505467197
best prefix_lift = 1.056758594
corresponding full_lift = 1.028947593
```

The visible branch / first 2-isogeny character span therefore gives no exact
joint selector and no stable high-lift practical selector.

## Interpretation

Positive:

```text
domain_line has a concrete half-norm explanation:
  chi(F) = chi((a + 2)(t^2 + 1))
  sigma(t^2 + 1)/(t^2 + 1) is square
The joint target is no more complicated than T_line inside domain_line=+1.
```

Negative:

```text
No visible character product explains product_bit = domain_line*T_line.
No visible character product gives a stable meaningful lift for joint ++.
The remaining theorem target must explain the half-norm torsor or T_line by
non-visible theta/divisor/additive structure.
```

## Continue / Kill

```text
continue = ask for half-norm/descent identity for t^2+1 on a=t-1/t
continue = ask for theta/additive identity for T_line on E: v^2=u^3-u
continue = GPU A/B remains trace/norm D prefilter, not visible line characters

kill = looking for a separate product-bit shortcut in the visible span
kill = treating prefix-only ~1.06x joint lift as stable
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_line_joint_character_span_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_line_joint_character_span_64tid_2chunk_256draw_8192rows_20260621.txt`
- Related: [P27 Line 2-Isogeny Character Span](p27_line_2isogeny_character_span_20260621.md)
- Related: [P27 Trace/Norm Elliptic Line / Coset Audit](p27_trace_norm_elliptic_line_coset_20260621.md)

```text
p27_line_half_norm_joint_stratum_rows=1/1
```

