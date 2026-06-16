# L1 p-Unit Boundary

This note records what the new tower-native scalar

```text
L_1 = M_0 + P_2 + P_157 + P_211
```

does and does not buy.

## Scalar Shape

For the p24 complement split

```text
h = m*n
m = 66254 = 2 * 157 * 211
n = 3107441,
```

the coefficient of the complement coordinate `r` in `L_1` is

```text
w(r) = 1 + (r mod 2) + (r mod 157) + (r mod 211).
```

Thus:

```text
1 <= w(r) <= 368.
```

The principal singular modulus is at `r=0`, so it still has coefficient `1`.
The characteristic-zero principal dominance proof for `M_0` therefore
survives with only a `log(368)` loss.

The audit

```text
p24/l1_height_divisibility_audit.py
```

reports:

```text
dominance_margin_L1=2.538350e12
dominance_margin_L1_over_log_p=4.593297e10
```

So `L_1` is nonzero over `C` for every nontrivial p24 relative
`H`-character packet.

## p-Adic Propagation

The scalar `L_1` is still an `H`-character eigenvector: all terms use the
same relative `H`-character in the recovery direction.  Therefore a selected
zero modulo the p24 split prime still propagates through:

```text
n * ord_n(p) = 3107441 * 388430 = 1207023307630
```

split prime factors over the Frobenius packet.

The same height audit reports:

```text
packet_pdiv_log=n*ord_n_p*log_p=6.670257e13
packet_norm_upper_log_with_coeff=6.127695e24
packet_room_ratio=9.186594e10
```

Thus height and principal dominance still do not prove p-unitness.

## Lost K-Trivial Structure

The support audit

```text
p24/l1_character_support_audit.py
```

reports:

```text
axis_support_size=368
translation_stabilizer_size=1
translation_orbit_size=66254
quotient_field_norm_packaging_survives=0
```

So `L_1` is not a `K`-trivial complement trace.  It has axis-shaped
`K`-character support:

```text
1 trivial K character
+ 1 nontrivial character on the 2-factor
+ 156 nontrivial characters on the 157-factor
+ 210 nontrivial characters on the 211-factor
= 368 K-character frequencies.
```

Its translation orbit under `K` is full size `m=66254`.  Therefore `L_1`
depends on the selected embedded `K`-origin and is not an element of the
degree-`n` quotient field fixed by `K`.

This is the tradeoff:

```text
M_0:
  K-trivial, clean quotient-field norm package, but small CM counterexamples;

L_1:
  tower-native and rescues known M_0 failures, but selected K-origin remains
  part of the p-adic theorem.
```

## Refined Axis-Injectivity Target

The selected-origin issue can be made sharper than a one-scalar p-unit
assertion.  Let

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}.
```

After removing redundant constants,

```text
dim(W_axis) = 1 + 1 + 156 + 210 = 368.
```

For each p24 packet factor `f_a | Phi_3107441`, define

```text
T_a(w) = sum_r w(r) F_r mod f_a,
F_r(X) = sum_k j_{n*r + m*k} X^k
```

as a map

```text
W_axis -> F_p[X]/(f_a).
```

If `T_a` is injective for all eight packet orbits, then every nonzero
axis-supported coefficient function has a nonzero selected packet value.  In
particular, `L_1` is nonzero because

```text
w_L1(r) = 1 + (r mod 2) + (r mod 157) + (r mod 211)
```

is a nonzero element of `W_axis`.

This is stronger and cleaner than proving `Res(Phi_n,L_1) != 0` directly: the
arithmetic input becomes a 368-element linear independence theorem inside the
degree-388430 packet field.

I added:

```text
p24/l1_axis_injectivity_scan.py
p24/l1_axis_injectivity_theorem.md
p24/lean/AxisInjectivityGate.lean
```

The broad eligible scan

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_axis_injectivity_scan.py \
  --max-cases 70 --min-h 12 --max-h 180 --max-abs-D 80000 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --include-linear \
  --require-deg-ge-axis-dim --random-trials 8 --summary-only
```

reported:

```text
packet_rows=148
injective_possible_rows=148
injective_rows=148
injective_failures=0
l1_zero_rows=0
rank_defect_histogram={0: 148}
injective_pivot_prefix_min=2
injective_pivot_prefix_max=4
```

The all-origin eligible window reported:

```text
packet_rows=272
injective_possible_rows=272
injective_rows=272
injective_failures=0
l1_zero_rows=0
rank_defect_histogram={0: 272}
```

Every rank defect seen so far occurs only when `deg(f) < dim(W_axis)`, where
injectivity is impossible for dimension reasons.  The p24 packet degree is
`388430`, far larger than `368`.

## Selected-Origin Toy Scan

I added:

```text
p24/l1_selected_origin_zero_scan.py
```

Pinned `M_0` failure:

```text
D=-899, q=281, h=14, m=2, n=7
```

Output:

```text
M0_zero_rows=1
L1_zero_rows=0
M0_selected_origin_zeros=14
L1_selected_origin_zeros=0
```

So the known complement-trace zero is a full-origin `M_0` failure, while
`L_1 = M_0 + P_2` rescues every selected origin.

Bounded selected-origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_selected_origin_zero_scan.py \
  --max-cases 30 --min-h 12 --max-h 100 --max-abs-D 20000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 200000 \
  --max-splitting-primes 2 --include-linear --summary-only
```

Output:

```text
scalar_rows=392
M0_zero_rows=0
L1_zero_rows=0
M0_selected_origin_zeros=0
L1_selected_origin_zeros=0
```

No selected-origin `L_1` zeros appeared in this bounded window.

Pinned prime-`n` product-coordinate counterexample:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/crt_partial_moment_linear_combo_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear --fixed-lambdas 1 --summary-only
```

Output:

```text
packet_rows=3
family_failures=0
candidate_failures=0
lambda_ones_failures=0
first_good_lambda_histogram={'(1,)': 3}
```

And the selected-origin version:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_selected_origin_zero_scan.py \
  --only-D -956 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 3307 --q-stop 3308 \
  --include-linear --summary-only
```

found:

```text
m0_zero_rows=0
l1_zero_rows=0
m0_selected_origin_zeros=0
l1_selected_origin_zeros=0
```

So `L_1` survives the same row that killed the broad product-coordinate
theorem.

Broader selected-prime fixed-all-ones scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/crt_partial_moment_linear_combo_scan.py \
  --max-cases 60 --min-h 12 --max-h 160 --max-abs-D 60000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 160 --q-stop 600000 \
  --max-splitting-primes 3 --include-linear \
  --fixed-lambdas 1 --summary-only
```

Output:

```text
packet_rows=579
family_failures=0
candidate_failures=0
lambda_ones_failures=0
first_good_lambda_histogram={'(1, 1)': 30, '(1,)': 549}
```

The matching projection-family scan reported:

```text
packet_rows=579
content_failures=0
m0_partial_family_failures=0
first_projection_histogram={'M0': 579}
```

The selected-origin scan in a smaller window also stayed clean:

```text
scalar_rows=272
m0_zero_rows=0
l1_zero_rows=0
m0_selected_origin_zeros=0
l1_selected_origin_zeros=0
```

Composite-`m` selected-origin stress scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/l1_selected_origin_zero_scan.py \
  --max-cases 8 --min-h 12 --max-h 120 --max-abs-D 25000 \
  --max-prime-quotients 0 --max-composite-quotients 4 \
  --min-n 3 --max-n 80 --q-stop 120000 \
  --max-splitting-primes 1 --include-linear \
  --require-composite-m --summary-only
```

Output:

```text
scalar_rows=16
m0_rows=8
l1_rows=8
m0_zero_rows=0
l1_zero_rows=0
m0_selected_origin_zeros=0
l1_selected_origin_zeros=0
```

This is a deliberately small quick-return test of the selected-origin caveat.
It is not a proof and does not replace the p-unit theorem, but it failed to
find a composite-`m` analogue where `L_1` vanishes.

## Current Meaning

The clean scalar certificate target is still:

```text
Res(Phi_3107441, L_1) != 0 mod p.
```

If proved, this gives the exact relative-content certificate using one
resultant and only the intermediate `2`, `157`, and `211` tower layers.

The selected-prime scans above make `L_1` the cleanest currently surviving
constructive scalar target:

```text
finite-field surface: one resultant;
construction shape:   degree-n base plus 2,157,211 partial layers;
dominance input:      principal coefficient remains 1;
known toy failures:   none for L1 in the tested windows.
```

But the proof cannot be just:

```text
M_0 quotient trace p-unitness + coefficient tweak.
```

It must prove a selected-origin p-unit theorem for the axis-supported
`K`-character combination, or separately prove nonvanishing through the three
intermediate partial-moment layers.

The finite-field zero lemma does not close this gap.  The follow-up note

```text
p24/l1_zero_lemma_boundary.md
```

checks that a selected `L_1` zero forces only the relative `H` orbit, not the
full `K`-translation orbit.  Thus the divisor-count criterion would require
pole degree below `n`, equivalently `delta < 1`, even if the four scalar
pieces are multiplied together.  This rules out the current zero-lemma route
for `L_1`; the remaining target is genuinely selected-origin p-unitness or a
new finite-field identity.

The companion interpolation diagnostic

```text
p24/l1_interpolation_shape_boundary.md
```

also gives a negative result for a cheap plain-`j` identity.  In composite
small-CM rows, `L_1` packet norms are `H`-periodic but otherwise have generic
interpolation degree and no bounded rational relation below the
`floor(h/2)` threshold.  Thus any finite-field identity for `L_1` must retain
the non-genus packet phase more directly than a one-variable rational function
of the selected singular modulus.

## Translate-Rank Boundary

The packet-rank sidecar

```text
p24/agent_packet_rank_sidecar.md
```

clarifies the clean rank statement available for `L_1`: its `K`-translate
family has character support of size

```text
1 + 1 + 156 + 210 = 368.
```

So a natural determinant/rank theorem would prove that the `368` supported
mixed CM resolvents are nonzero, equivalently that the `K`-translate span of
the `L_1` packet has rank `368`.  This would show the translate family is not
identically zero.  It still does not prove selected-origin nonvanishing:
a nonzero `368`-frequency word can vanish at one specified `K` coordinate by
ordinary finite-field cancellation.  The missing step remains selected-origin
hyperplane avoidance, i.e. p-unitness at the chosen split prime.
