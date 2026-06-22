# P27 Trace/Norm Dplus Four-U Rational Screen

Date: 2026-06-22

## Claim

The post-Dplus four-`U` cover is not explained by a small visible rational
formula in the obvious base coordinates.

After:

```text
t = y - 1
a = t - 1/t
A = a^4/4 - 2
U = x6 + 1/x6
```

each tested `Dplus` row has four `U` values.  Let:

```text
prod(Z - U_i) = Z^4 - e1*Z^3 + e2*Z^2 - e3*Z + e4.
```

A train/heldout rational reconstruction screen found no expression for any
`e1,e2,e3,e4` as a rational function of degree `(20,20)` in:

```text
t, a, or A.
```

This kills the cheap visible-base version of the four-`U` source law.  It does
not kill a higher-degree cover, quotient/Prym decomposition, or relation to the
H90 payload class.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_ucover_rational_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_ucover_rational_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_ucover_rational_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --rows 150 \
  --train 100 \
  --max-degree 20 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_ucover_rational_probe_20260622.txt
```

## Sample

```text
rows = 150
train = 100
heldout = 50
max_degree = 20
raw_y_draws = 2253
nonsplit_y = 1132
Dplus_y = 288
accepted_rows = 150
U_count_4 = 150
```

The probe uses a rational form:

```text
e_i(x) = (n0 + n1*x + ... + nd*x^d) /
         (1 + q1*x + ... + qd*x^d)
```

with `x` equal to `t`, `a`, or `A`, solving on the train set and requiring
exact heldout agreement.

## Results

Every screened pair was negative:

```text
variable=t coeff=e1 verdict=none_deg_le_20
variable=t coeff=e2 verdict=none_deg_le_20
variable=t coeff=e3 verdict=none_deg_le_20
variable=t coeff=e4 verdict=none_deg_le_20

variable=a coeff=e1 verdict=none_deg_le_20
variable=a coeff=e2 verdict=none_deg_le_20
variable=a coeff=e3 verdict=none_deg_le_20
variable=a coeff=e4 verdict=none_deg_le_20

variable=A coeff=e1 verdict=none_deg_le_20
variable=A coeff=e2 verdict=none_deg_le_20
variable=A coeff=e3 verdict=none_deg_le_20
variable=A coeff=e4 verdict=none_deg_le_20
```

## Interpretation

Positive:

```text
The four-U cover is now a named object with a bounded visible-formula screen.
The test used exact finite-field reconstruction and heldout validation.
The x6 squareclass target from the previous note remains the right next class.
```

Negative:

```text
No coefficient of the four-U quartic is a visible low-degree rational function
of t, a, or A through degree (20,20).
The cover should not be handed to GPU as a simple t/a/A source formula.
```

## Updated Next Test

The next useful work is not broader rational fitting.  It is:

```text
derive or normalize the four-U cover as a cover over the Dplus/H90 base;
compare the x6 squareclass on x6^2 - U*x6 + 1 with A_eta = U_eta + z*W_eta;
look for a quotient/Prym/coboundary relation, or prove the class is fresh.
```

Promote only if:

```text
the cover decomposes to a low-genus/sourceable quotient;
or the x6 squareclass is related to A_eta by a named class identity.
```

Kill if:

```text
the four-U cover is generic/high-genus after obvious quotients and chi(x6) is
independent of A_eta and later A-level classes.
```

## Continue / Kill

```text
continue = CAS normalization of the four-U cover
continue = x6 squareclass versus H90 A_eta class comparison
continue = use GPU only for same-stream rows if CAS needs scale

kill = low-degree rational formulas for e1..e4 in t,a,A through degree 20
kill = GPU production from a guessed four-U base formula
kill = broader coefficient fishing without a divisor/class reason
```

## Linked Artifacts

- [P27 Trace/Norm Dplus X6/U-Class](p27_trace_norm_dplus_x6_uclass_20260622.md)
- [P27 Trace/Norm Dplus A-Coordinate Bridge](p27_trace_norm_dplus_a_coordinate_bridge_20260622.md)
- [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- [P27 Sqrt-Beating Test Queue After Coupling Kill](p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md)

```text
p27_trace_norm_dplus_ucover_rational_screen_rows=1/1
```
