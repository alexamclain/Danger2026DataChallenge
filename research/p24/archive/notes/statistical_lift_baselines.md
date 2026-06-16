# Statistical / Probability Lift Baselines

Question: can probability techniques improve the strict p24 search
asymptotically, rather than only improving constants?

This note records the current local baselines.  They are deliberately small
scale and exact: for small `p=n^2+7`, the scripts compute all Montgomery
traces by FFT convolution, then measure the exact strict x-only bucket.

## Mixed CRT Trace Residues

Added:

```text
p24/mixed_crt_trace_residue_optimizer.py
```

The optimizer searches levels

```text
N = 2^d * R
```

where `R` is a squarefree product of small odd primes.  It grants a very
generous oracle that imposes exactly the union of the six strict target trace
residues modulo `N` at only `Gamma0(N)` cost, then charges linearly for any
remaining Hasse trace lifts.

Representative run:

```text
python3 p24/mixed_crt_trace_residue_optimizer.py \
  --prime-bound 47 --max-odd-part 20000 --min-depth 28 --max-depth 42 --top 30
```

Best row:

```text
depth=40
odd_part=1
level=1099511627776
target_residue_count=2
survivors=6
gamma0_over_sqrt=1.649267
proxy_over_sqrt=1.649267
```

So mixed small-prime trace residues do not improve on the pure `2^40` exact
trace-residue oracle in this search window, and even the best generous oracle
remains a constant times `sqrt(p)`.

## Partial Oriented Depth As A Rare Event

Representative run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py \
  --min-p 100000 --max-p 1000000 --max-rows 10 \
  --n-modulus 8 --n-residue 0 --fit-min-depth 5
```

Aggregate output:

```text
aggregate_fitted_beta_x1=1.038291
aggregate_fitted_beta_x0=-0.000000
conclusion=oriented_depth_sampler_by_rejection_has_beta_about_one_x0_has_no_orientation
```

I reran a slightly broader exact calibration:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py \
  --min-p 100000 --max-p 600000 --max-rows 8 \
  --n-modulus 8 --n-residue 0 --fit-min-depth 5
```

The aggregate had small-depth noise but the same conclusion:

```text
aggregate_fitted_beta_x1=0.943004
aggregate_fitted_beta_x0=-0.000000
depth 9: x1_cost=59.568, x0_cost=1.333
```

The apparent subunit beta in this short range is not a stable sampler: row
fits range from `0.86` to `1.08`, and the older deeper calibration moves back
above `1`.  The geometric distinction remains exact: `X0` is cheap because it
forgets the orientation, while `X1` pays roughly one bit per oriented lift.

The `X0` trace-residue bucket is cheap but unoriented; it does not supply the
strict point.  The oriented `X1`-like bucket shrinks with beta about one,
which is exactly the exponent that preserves sqrt scaling.

I also reran the first `X1(16)->X1(32)` feature scan:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x16_first_lift_p24_feature_scan.py \
  --accepted 5000 --target-depth 12 --depths 6 8 10 12 \
  --norm-coeff 2 --report-top 20
```

The calibration prime was `p=57527`, matching the p24 residue modulo `9240`.
After conditioning on nonsplit `X1(16)` and a first lift, the base depth-12
rate was `120/5000 = 0.024`.  The best scanned quotient/norm bucket had:

```text
lift=1.293996
hit=80/2576
capture=0.666667
feature=Norm(-2+2*y+2*y^2+z)
```

This is a constant classifier, not a growing-depth score.  No stable high-lift
bucket appeared.

## Low-Degree Character Labels

Representative run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/low_degree_character_trace_scan.py \
  --min-p 10000 --max-p 180000 --max-rows 10 \
  --coeff-bound 2 --n-modulus 8 --n-residue 0 --top 8
```

Aggregate output:

```text
aggregate good=10482/360626 base_rate=0.029066
best_aggregate_lift=1.485000
conclusion=only_constant_scale_low_degree_character_labels_seen
```

The best features are essentially the split/nonsplit Montgomery label in
disguise.  They capture about half the space and lift the hit rate by a
constant factor, not by a factor growing with the target depth.

## Dyadic A/J Buckets

Representative run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/dyadic_parameter_residue_audit.py \
  --min-p 10000 --max-p 250000 --max-rows 10 \
  --max-bits 10 --n-modulus 8 --n-residue 0 --top 8
```

The best `j mod 2^10` bucket has lift `3.351`, but capture is only `0.0029`.
The score drops as buckets get narrower:

```text
j bits=1:  lift=1.040 capture=0.5201
j bits=10: lift=3.351 capture=0.0029
conclusion=dyadic_A_or_j_residues_show_only_constant_bucket_lifts_not_a_growing_trace_v2_selector
```

This is the usual statistics trap: high lift in tiny buckets is not an
exponent-changing sampler unless the capture/lift tradeoff scales better than
random.

## Low-Height Formula Windows

Added:

```text
p24/low_height_formula_window_audit.py
p24/low_height_formula_window_audit.md
```

This tests a softer variant of exact formulas: scan a moving interval

```text
|A - f(n)| <= W(p)
```

around low-height LFT centers `f(n)=(a*n+b)/(c*n+d)`.  On the same exact
near-square calibration rows, with `1008` centers of coefficient height `3`,
the best aggregate rows were only constant-factor:

```text
p^0.50 last_width=248 hits=147/3722
capture=0.014024 lift=1.359 coverage=0.010321

fixed_128 last_width=128 hits=106/2570
capture=0.010113 lift=1.419 coverage=0.007126
```

So neighborhoods of simple formulas do not create a sub-sqrt preselector.

## Current Standard For A Useful Statistics Lift

A productive probabilistic technique needs to show one of:

```text
1. an oriented-depth sampler with empirical/theoretical beta < 1 for growing
   depth h, not just small finite-depth noise;
2. a feature family whose lift grows with h while capture does not shrink
   proportionally;
3. a way to sample exact trace residues modulo a growing level at cost below
   the corresponding modular index;
4. a class/root selector that samples the target CM torsor without needing a
   seed root or enumerating a sqrt-scale class object.
```

No current local statistical probe meets those standards.

## Rare-Event / Importance-Sampling Sidecar

Huygens audited multilevel splitting, sequential Monte Carlo, cross-entropy,
adaptive feature learning, and rare-event scheduling.

The no-go shape is:

```text
sample X1(2^h), then pay residual tail 2^(40-h)
```

If the partial oriented sampler costs `2^h`, the product remains
sqrt-scale.  `X0(2^h)` is cheaper, but it omits the exact orientation the
verifier needs; recovering that orientation is the hard `X1` cover again.

Feature-learning/cross-entropy methods are useful only if the learned score
has holdout lift growing with depth while keeping non-negligible capture.
Existing local scans fail that bar: low-degree characters, dyadic residues,
odd cosets, additive/multiplicative spectra, and moment features provide
constant or unstable row-local lifts.  In particular,
`p24/odd_character_residual_entropy_scan.py` had median holdout lift `1.003`.

The sidecar's falsifiable test:

```text
On exact small p=n^2+7 rows, train a proposed score on half the rows and test
on the holdout.  Pass only if log2(lift) grows linearly with target depth and
capture does not collapse.
```

No current probability route passes this test.  Probability is moving entropy
around, not removing the target trace/orientation entropy.

## Trace-Distribution / Equidistribution Sidecar

Linnaeus audited trace-distribution, character-sum, random-matrix, and
equidistribution tools.

For p24 the strict x-only event is exactly the six signed Hasse traces:

```text
±1178414874616, ±1020608380936, ±78903246840
```

The discrete Sato-Tate mass of these six points is about `1.70e-12`, giving a
naive trace-level expected search of about `5.89e11`, i.e. square-root scale.
The near-square condition `p=n^2+7` gives the cheap `D=-7` trace `±2n`, but
that trace has only `v2=3`.

The clean split is:

```text
constant-factor classifiers:
  A±2, split/nonsplit, fixed X1(16), bounded low-degree characters,
  small residue/coset buckets

exponent-changing selectors:
  need epsilon*log(p) growing bits that retain the target traces and cost less
  than the saved search
```

Known ways to obtain growing bits are growing modular level, SEA-style trace
residues, or CM/class-field root selection; the local p24 audits put those
back at sqrt scale or worse.

Concrete tests worth keeping:

```text
1. proposed feature f(A,n): exact small-field train/holdout over p=n^2+7,
   n=0 mod 8; reject if lift plateaus
2. proposed trace residues: convert to modular-index plus survivor-count proxy
3. proposed CM/class invariant: require an explicit embedded quotient and
   recovery map without enumerating the target CM orbit
4. proposed Jacobi/hypergeometric trace: verify the target CM conductor appears
   in cheap p^f-1 data
```

Under known methods, probability/equidistribution explains the rarity and
validates constant gates; it does not name the rare Montgomery `A`.

## Class-Group / Random-Walk Probability

Added:

```text
p24/class_group_probability_audit.py
```

The smooth third target makes generic group algorithms tempting:

```text
h = 205880396014 = 66254 * 3107441
sqrt(h) ~= 453740 << sqrt(p)
```

But the separation is:

```text
abstract smooth class group != embedded root torsor over F_p
```

Pollard rho, birthday methods, hidden shift, expander walks, and random
self-reducibility are useful once there is an embedded class-action oracle,
such as `g -> j(g*E0)`, or a seed CM root.  Without that, they find relations
in the abstract class group we already know; they do not output an `F_p`
`j`-invariant.

Representative output from the audit:

```text
trace=-1178414874616
  h/sqrt_p=0.205880
  sqrt_h/sqrt_p=4.537405e-07
  random_j_expected=4.857189e+12

oracle_separation:
  seeded_embedded_root_available -> already have a CM j root
  embedded_class_action_oracle_available -> Pollard/hidden-shift costs about sqrt(h)
  abstract_class_group_only -> samples labels, not Fp j-values
  no_seed_no_embedded_invariant -> random walk has no Fp state space to walk
```

So class-group probability methods are sub-`sqrt(p)` only after the missing
embedded quotient/root oracle has been supplied.  They do not themselves
remove the embedding requirement.
