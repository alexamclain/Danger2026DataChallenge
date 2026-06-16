# Upstream DANGER3 Dataset Experiment Audit

Date: 2026-06-04

Purpose: use Andrew Sutherland's upstream DANGER3 datasets as experimental
evidence for the strict `p = 10^24 + 7` problem, rather than only searching
the literature.

Scope note: these files contain DANGER3 Montgomery triples or successful
`(p,A)` prefixes.  They are useful for testing density, branch, and
low-degree character selectors in the original search space.  They do **not**
contain the CM relative fibers

```text
J_u(X)=sum_k j_{u+m*k}X^k
```

for the p24 class-field packet theorem, so they cannot directly test

```text
Res(Phi_3107441,J_u) != 0 mod p
```

or exact relative content for the target.

## Data Imported

Cloned read-only local corpus:

```text
p24/upstream_DANGER3/
```

Relevant upstream files:

```text
pp10.txt        all triples (p,A,x0), p <= 2^10
pp12.txt.gz     all triples (p,A,x0), p <= 2^12
pp16A.txt.gz    all distinct successful prefixes (p,A), p <= 2^16
pp20.txt        one triple per prime, 3 < p < 2^20
pp24.txt.gz     one triple per prime, 3 < p < 2^24
```

Small data hygiene note: upstream README says the `10^19` update triple is for
`10^19+61`; the same `(A,x0)` verifies for `10^19+51`, not `10^19+61`.

## Reproducible Local Audits

Added:

```text
p24/upstream_dataset_feature_audit.py
p24/upstream_prefix_character_scan.py
p24/upstream_terminal_branch_audit.py
p24/upstream_large_one_witness_stream_audit.py
p24/upstream_nearsquare_prefix_gate_audit.py
p24/full_small_triple_halving_audit.py
p24/full_small_triple_x0_invariant_audit.py
```

Verified:

```text
python3 -m py_compile p24/upstream_dataset_feature_audit.py
python3 -m py_compile p24/upstream_prefix_character_scan.py
python3 -m py_compile p24/upstream_terminal_branch_audit.py
python3 p24/upstream_dataset_feature_audit.py
python3 p24/upstream_prefix_character_scan.py --min-p 32768 --max-p 65536 --top 8
python3 p24/upstream_prefix_character_scan.py --min-p 32768 --max-p 65536 --residue 7 --top 8
python3 p24/upstream_terminal_branch_audit.py --residue 7 --tail-threshold 2048
python3 p24/upstream_large_one_witness_stream_audit.py https://math.mit.edu/~drew/pp28.txt.gz --sample-size 20000 --near-c 63 --keep-near 50000 --max-terminal 50000 --bins 16
python3 p24/upstream_nearsquare_prefix_gate_audit.py --c 7 --n-mod 8 --n-residue 0 --min-p 32768 --max-p 65536
python3 p24/full_small_triple_halving_audit.py --source p24/upstream_DANGER3/pp12.txt.gz --output-md p24/full_small_triple_pp12_audit.txt
python3 p24/full_small_triple_halving_audit.py --source p24/upstream_DANGER3/pp12.txt.gz --residue 7 --min-p 2048 --output-md p24/full_small_triple_pp12_p7_tail_audit.txt
```

## What The Data Teaches

The one-per-prime `pp24` witnesses are heavily biased:

```text
rows=1077869
split_counts={-1: 1074967, 1: 2902}
terminal_counts={'quadratic_root': 1464, 'zero_root': 1076405}
```

This is a witness/generator bias, not the full solution density.  The all-prefix
file is much closer to balanced:

```text
pp16A prefix_split_counts={-1: 2641160, 1: 2071909}
```

The all-prefix data reinforces the expected square-root barrier.  Normalizing
successful `A` prefixes by `sqrt(p)` gives bounded constants, organized mostly
by how many Hasse-lattice target orders are available:

```text
target_orders=1 mean_good_A_over_sqrt=2.048154
target_orders=2 mean_good_A_over_sqrt=3.634469
target_orders=3 mean_good_A_over_sqrt=5.206613
target_orders=4 mean_good_A_over_sqrt=6.023870
```

So the observed density is compatible with

```text
# good Montgomery A for a fixed p = Theta(sqrt(p))
```

up to the expected fixed constants from Hasse-window target trace count and
split/nonsplit branch structure.

## Character Signals

The strongest cheap character signal in the `p % 8 == 7` slice is:

```text
feature=A-2 best_sign=-1 capture=0.748937 approx_lift=1.497874
feature=A+2 best_sign=+1 capture=0.748937 approx_lift=1.497874
```

The terminal branch audit explains this as a fixed branch mixture.  In the
`p % 8 == 7` all-triple data, successful prefixes have only these sign
patterns:

```text
(chi(A+2), chi(A-2), chi(A^2-4))
( 1, -1, -1): 10030
(-1, -1,  1):  5374
( 1,  1,  1):  5374
```

This is useful as a constant-factor orientation/filter, but it is not a
depth-growing selector.  Other fixed low-degree Legendre labels were
essentially unbiased after this terminal-branch explanation, with lifts near
`1.00`.

## Larger Linked One-Witness Data

The upstream README also links larger one-witness archives:

```text
pp28.txt.gz  one triple per prime, 3 < p < 2^28
pp30.txt.gz  one triple per prime, 3 < p < 2^30
pp32.txt.gz  one triple per prime, 3 < p < 2^32
```

HTTP HEAD on 2026-06-04 showed compressed sizes about:

```text
pp28: 174789799 bytes
pp30: 684123983 bytes
pp32: 2702673797 bytes
```

An independent side audit also verified that local `pp24` is exactly the prefix
of each larger one-witness archive:

```text
local_pp24 rows=1077869
last_p=16777213
sha256=c85fad4afb36898ff43e0e6094534c56f92bdabc2316d6e7243dc8fcfde755c1
pp28_first_1077869 equal_local=True
pp30_first_1077869 equal_local=True
pp32_first_1077869 equal_local=True
```

The first `1,300,000` rows, extending past local `pp24`, are also identical in
`pp28`, `pp30`, and `pp32`.  This supports treating these files as ordered
extensions from one fixed witness generator.

Streaming all of `pp28` gives:

```text
rows=14630841
max_p=268435399
target_order_count_hist={1: 14366, 2: 3603724, 3: 7293053, 4: 3719698}
A_over_p_bins and x_over_p_bins nearly uniform over 16 bins
reservoir_split_counts={-1: 19992, 1: 8}
reservoir_terminal_counts={'quadratic_root': 4, 'zero_root': 19996}
```

For the closest small analogue to the p24 shape,
`p = n^2 + 7` with `n == 0 mod 8`, the one-witness files are even more
structured:

```text
pp24 analogue rows=142
split_counts={-1: 142}
gate_counts={(1, -1, -1): 142}

pp28 analogue rows=460
split_counts={-1: 460}
gate_counts={(1, -1, -1): 460}
```

This initially looked theorem-shaped, but the all-prefix `pp16A` slice says it
is a representative-selection bias.  For the same near-square family in the
upper half of `pp16A`:

```text
prime_rows=6
good_A_rows=7456
split_total={-1: 3680, 1: 3776}
gate_total=(-1, -1, 1):1888,(1, -1, -1):3680,(1, 1, 1):1888
dominant_gate=(1, -1, -1)
dominant_gate_capture=0.493562
mean_good_A_over_sqrt=5.945777
```

Across all `pp16A` rows with `p=n^2+7`, `n == 0 mod 8`, the dominant gate
captures only `0.483170` of successful prefixes.  Thus the published
one-witness generator appears to pick the zero/nonsplit branch consistently in
this subfamily, but the full set of certificates remains split across fixed
character gates with square-root-scale density.

The p24 analogue also has three target orders in the Hasse interval.  Filtering
the upper-half `pp16A` near-square rows by that count does not improve the
gate into a theorem:

```text
target_orders=3 total=5398
dominant_gate=(1, -1, -1)
capture=0.483512
```

This is the right negative lesson for the current p24 CM route: the upstream
DANGER3 data has not revealed a growing statistical selector in the
Montgomery prefix space.  The separate CM packet scans in

```text
p24/relative_resultant_selected_prime_scan.py
p24/packetized_relative_content_scan.py
p24/relative_packet_factor_shape_scan.py
```

are the relevant evidence for the prime relative-normality theorem.  They
remain supportive but circumstantial: prime `n` rows have stayed clean, while
composite `n` controls produce genuine one-factor cyclic-code failures.

## Hidden Recipe Check

A possible concern was that the one-per-prime upstream witnesses might encode a
simple repeated inverse-halving branch recipe.  Streaming the `pp24` witnesses
and inspecting the last x-only states gave:

```text
last3_counts:
  (+1, 0, infinity): 538616
  (-1, 0, infinity): 537789
  (other, other, infinity): 1464
```

The penultimate zero-branch state is split essentially evenly between `+1` and
`-1`, and the previous state is not a tiny symbolic alphabet.  This does not
look like a low-complexity branch-code construction hiding in the upstream
witnesses.

## Full-Triple x0 / Halving-Word Data

The full small files expose every accepted x-coordinate, not just `(p,A)`
prefixes.  On exact `pp12`:

```text
rows=3083880
distinct_prefixes=80263
x_per_A_quantiles_10_25_50_75_90_99=16,16,32,32,64,128
symmetry_closure_rates=reciprocal:1.000000 negA_negx:1.000000 orbit4:1.000000
```

Thus the data has exact constant symmetries

```text
x -> 1/x
(A,x) -> (-A,-x)
```

and their 4-orbit, but those quotient only by constants.  The strongest
low-degree x-visible characters are still the prefix-level branch characters:

```text
all pp12:
  A+2 capture=0.664848
  A^2-4 capture=0.662931
  x, x±1, x+1/x, A*x±1 all around 0.50

p % 8 == 7, p >= 2048:
  A-2 / A+2 capture=0.670996
  x-specific characters all around 0.50
```

Most importantly, inverse-halving branch words behave like uniform choices
after the terminal branch degeneracy.  On all `pp12` triples:

```text
inverse_four_prefix_captures:
length=1 capture=0.335258
length=2 capture=0.084645
length=3 capture=0.021237
length=4 capture=0.005468
length=5 capture=0.001430
length=6 capture=0.000372
```

The p24-relevant `p % 8 == 7` tail has the same decay:

```text
length=1 capture=0.335498
length=2 capture=0.087114
length=3 capture=0.022275
length=4 capture=0.005656
length=5 capture=0.001570
length=6 capture=0.000436
```

This supports the inverse-chain entropy conclusion from another angle: the
published full-triple data does not hide a growing branch-word selector.

## Relation To p22/p23

Subagent and local audits agree:

```text
p22 trace = -160218218486
#E = 2^37 * 72759576143
chi(A^2 - 4) = -1

p23 trace = -227792650122
#E = 2^39 * 181898940355
chi(A^2 - 4) = -1
```

The theorem-shaped lesson is the p23 one already isolated:

```text
If chi(A^2 - 4) = -1, the rational 2-Sylow is cyclic.  For an X1(16)
marked point in this nonsplit family, first-branch halving survives to depth d
iff v2(#E(Fp)) >= d.
```

That explains the practical p23 constant-factor win.  It does not by itself
change the exponent for p24, because fixed `X1(16)` still leaves a trace
rare-event of size `Theta(1/sqrt(p))`.

## p24 Implication

For `p = 10^24 + 7`, `k=40`, the strict traces remain:

```text
  1020608380936
  -78903246840
  -1178414874616
```

with signs allowed through the quadratic twist.  The upstream datasets support
using nonsplit/terminal orientation as a constant-factor filter if one were
running a search.  They do not expose a data-driven selector that shrinks the
target trace entropy with a growing number of bits.

Current theorem candidate that would be genuinely new:

```text
Find a cheap closed-form trace-residue or oriented 2-power tower selector whose
lift grows with depth while capture does not shrink at the same exponential
rate.
```

Every dataset-derived feature tested here is either:

1. a fixed terminal-branch/group-structure constant,
2. a witness-selection artifact,
3. or a sqrt-scale trace selector whose cost moves rather than removes the
entropy.

Conclusion: upstream data is useful, but it currently strengthens the frontier
rather than producing the p24 asymptotic speedup.
