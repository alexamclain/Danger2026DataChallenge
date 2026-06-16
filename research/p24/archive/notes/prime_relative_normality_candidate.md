# Prime Relative-Normality Candidate

This note records a refinement of the relative-product route.

## Setup

For `h=m*n`, write

```text
P_u(a) = sum_k zeta_n^(a*k) j_{u+m*k}.
```

The exact p24 packet certificate only needs the vector

```text
(P_0(a), ..., P_{m-1}(a))
```

to be nonzero.  A stronger product certificate asks for every coordinate to
be nonzero:

```text
P_u(a) != 0 for every u.
```

The earlier product route was too strong in general.  The known counterexample
has composite recovery length:

```text
D=-1336, q=1777, h=12, m=2, n=6,
relative_fibers=[1400, 0].
```

For p24, however,

```text
n = 3107441
```

is prime.  This suggests a narrower theorem:

```text
Prime relative-normality candidate:
  for prime n, every selected nontrivial relative character packet of every
  H-orbit of reduced singular moduli has nonzero coordinate P_u(a), except
  possibly at primes dividing an explicit relative normality index.
```

For fixed `u`, this is the finite-field relative normality of the length-`n`
orbit

```text
j_u, j_{u+m}, ..., j_{u+m(n-1)}
```

over the quotient field.  The product certificate is the product of the
nontrivial character resolvents of that orbit.

## New Diagnostic

I added:

```text
p24/hermitian_packet_structure_scan.py
p24/relative_normality_prime_composite_scan.py
```

It records for packetized small CM examples:

```text
coord_zero_count    number of relative coordinates P_u(a) vanishing
term_zero_count     number of Hermitian summands vanishing
span_rank           F_q-span rank of the coordinate residues
```

It also has random-vector and shuffled-cycle controls for small runs.  The
controls are diagnostics only, not certificates.

Small sanity run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_packet_structure_scan.py \
  --max-cases 8 --min-h 12 --max-h 60 --max-abs-D 8000 \
  --max-quotients 3 --min-n 5 --q-stop 80000 \
  --random-trials 100 --shuffle-trials 100 --summary-only
```

Output:

```text
packet_rows=12
cm_hermitian_zero_packets=0
cm_any_zero_coordinate_packets=0
cm_any_zero_term_packets=0
cm_full_span_packets=5
cm_span_defect_packets=7
random_vector_zeros=0/1200
shuffled_cycle_zeros=0/1200
```

The span statistic is not a viable p24 theorem: for p24 the packet degree is

```text
deg f_a = 388430
```

while the coordinate count is only

```text
m = 66254.
```

So full base-field span is impossible.  The useful signal is coordinate
nonvanishing.

Broader prime-`n` packet run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_packet_structure_scan.py \
  --max-cases 160 --min-h 12 --max-h 150 --max-abs-D 60000 \
  --max-quotients 8 --min-n 5 --q-stop 600000 \
  --random-trials 0 --shuffle-trials 0 --summary-only
```

Output:

```text
packet_rows=255
cm_hermitian_zero_packets=0
cm_any_zero_coordinate_packets=0
cm_any_zero_term_packets=0
cm_full_span_packets=152
cm_span_defect_packets=103
worst_span_rank_ratio=0.111111
max_coord_zero_count=0
max_term_zero_count=0
```

This does not prove the theorem, but it separates the situation:

```text
composite n: individual coordinate zero observed;
prime n packet scans so far: no individual coordinate zero observed.
```

The sharper prime/composite scan tests primitive relative-character packets
for both prime and composite recovery lengths.  It also includes degree-one
packets when requested, because selected-character failures in small fields
can be linear.

Pinned reproduction of the known composite failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_normality_prime_composite_scan.py \
  --only-D -1336 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 1777 --q-stop 1778 \
  --include-linear
```

Output:

```text
D=-1336 q=1777 h=12 m=2 n=6 n_prime=0 deg=1 coord_zero=1
prime_coord_zero_packets=0
composite_coord_zero_packets=1
composite_hermitian_zero_packets=0
```

Broader mixed run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_normality_prime_composite_scan.py \
  --max-cases 160 --min-h 12 --max-h 150 --max-abs-D 60000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 150 --q-stop 600000 \
  --include-linear --summary-only
```

Output:

```text
packet_rows=651
prime_packet_rows=301
composite_packet_rows=350
prime_coord_zero_packets=0
composite_coord_zero_packets=2
prime_content_zero_packets=0
composite_content_zero_packets=0
prime_hermitian_zero_packets=0
composite_hermitian_zero_packets=0
composite_coord_zero_samples:
  D=-656 q=173 h=16 m=4 n=4 deg=1 coord_zero=1
  D=-1028 q=293 h=16 m=4 n=4 deg=1 coord_zero=1
```

At this stage the small-data split appeared to be:

```text
prime n:     no product-coordinate failures in this 301-row window;
composite n: coordinate failures exist, but exact content and Hermitian stay
             nonzero in the observed rows.
```

Selected-prime rotation matters: the finite-field embedding can choose any
root in the split CM torsor.  I added `--scan-origins` to rotate the class
cycle and test every selected origin.

Pinned composite failure with origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_normality_prime_composite_scan.py \
  --only-D -1336 --min-h 12 --max-h 20 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 12 --q-start 1777 --q-stop 1778 \
  --include-linear --scan-origins
```

Output:

```text
composite_packets_with_some_origin_coord_zero=1
selected_origin_tests=72
selected_origin_coord_zeros=12
```

So the known composite coordinate-zero packet is structural across all
selected origins.

Moderate mixed origin scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_normality_prime_composite_scan.py \
  --max-cases 80 --min-h 12 --max-h 100 --max-abs-D 25000 \
  --max-prime-quotients 5 --max-composite-quotients 5 \
  --min-n 3 --max-n 100 --q-stop 250000 \
  --include-linear --scan-origins --summary-only
```

Output:

```text
packet_rows=313
prime_packet_rows=153
composite_packet_rows=160
prime_packets_with_some_origin_coord_zero=0
composite_packets_with_some_origin_coord_zero=1
selected_origin_tests=5861
selected_origin_coord_zeros=16
```

This is stronger evidence for the p24 shape than the origin-zero scan alone:

```text
prime n stayed clean in this smaller origin-rotation window;
composite n failures, when present, persist through all origins in the tested
examples.
```

After adding random-baseline accounting, the same moderate origin scan gave:

```text
expected_prime_coord_zero_packets_random=0.394428
expected_composite_coord_zero_packets_random=0.323599
expected_prime_origin_coord_zeros_random=6.055355
expected_composite_origin_coord_zeros_random=4.777915
```

So the absence of prime-origin coordinate zeros is stronger than a tiny-sample
accident in this toy window.  It is still only evidence: it is an
anti-cancellation phenomenon for CM packet vectors, not a proof.

This evidence was later superseded by the multi-splitting counterexample in
`p24/prime_relative_normality_counterexample.md`.  The earlier scans were too
small, and in particular did not sample enough splitting primes for the
`D=-956, q=3307` prime-`n` failure.

Correction: origin shifts are not independent for coordinate/resultant
vanishing.  The later note

```text
p24/relative_origin_shift_invariance.md
```

proves that shifting the class-cycle origin sends each relative fiber to a
permuted fiber multiplied by a power of `X` modulo `X^n-1`.  Therefore
zero/nonzero modulo any packet factor `f | Phi_n` is invariant under origin
rotation.  The origin scans above should be read as consistency checks, not as
extra random trials.  The prime-relative-normality target itself is unchanged.

I also added:

```text
p24/relative_zero_structure_inspector.py
```

to inspect the composite zero coordinates.  Runs on the known examples:

```text
D=-1336, q=1777, h=12, n=6
D=-656,  q=173,  h=16, n=4
D=-1028, q=293,  h=16, n=4
```

showed that the zero fibers do **not** have a smaller proper period.  Thus the
simple explanation

```text
composite failure = pullback from a proper quotient of Z/nZ
```

is false in these examples.  The failures are genuine primitive
root-of-unity cancellations in degree-one packets.  Prime `n` still looks
clean, but the proof has to use more than the absence of proper divisors.

## Relation To Known Normal-Basis Results

The nearby literature has normal-basis theorems for carefully chosen class
invariants.  For example, Jung-Koo-Shin prove that singular values of certain
Siegel functions form normal bases of ray class fields over imaginary
quadratic fields:

```text
https://arxiv.org/abs/1007.2312
```

That is adjacent but not directly enough for p24:

```text
known result:  existence/normality for special Siegel-function generators;
p24 need:      selected-prime reduction of level-1 j relative packets;
missing:       explicit p-unit statement for the relative normality index.
```

Still, this suggests a possible proof shape:

1. Define the relative group determinant

   ```text
   Delta_u = product_{a=1}^{n-1} P_u(a)
   ```

   or its Frobenius-packet norm.

2. Interpret `Delta_u` as the nontrivial-character part of the normality
   determinant for the degree-`n` relative CM orbit.

3. Prove the selected p24 prime does not divide this determinant for every
   quotient coordinate `u`.

Equivalently:

```text
Res(Phi_n(X), J_u(X)) is a p-unit
```

for the eight p24 Frobenius packets, with `n=3107441`.  For prime `n`, this
single resultant covers every nontrivial relative character.  Over `F_p`, the
packet condition is:

```text
J_u(X) mod f_a(X) != 0
```

for each irreducible packet factor `f_a | Phi_n`.

This is an augmentation-normality statement, not full cyclic normality.  The
full circulant determinant has an extra trivial-period factor `J_u(1)`, and
small prime-`n` examples show that this trivial factor can vanish while every
primitive packet remains nonzero.  The correction is recorded in:

```text
p24/relative_augmentation_normality.md
p24/relative_circulant_rank_scan.py
```

For p24 this would be stronger than needed but still sub-sqrt useful: one
nonzero product certificate for each of the eight Frobenius packets would
rule out every harmful packet without enumerating the class set.

The finite implication is checked in:

```text
p24/lean/RelativeNormalityGate.lean
```

It proves the abstract gate:

```text
if every quotient coordinate has a nonzero relative-normality determinant,
and a vanished coordinate forces its determinant to vanish,
then every packet coordinate is nonzero, hence no harmful all-zero packet can
occur.
```

Verified with:

```text
lean p24/lean/RelativeNormalityGate.lean
```

## Current Status

Update: a later multi-splitting selected-prime stress scan found a prime-`n`
coordinate failure:

```text
D=-956 q=3307 ell=5 h=15 m=5 n=3 deg=1 coord_zero=1
content_zero=0 hermitian_zero=0
```

The pinned inspector shows the vanished length-3 fiber has no proper period:

```text
roots=[57] coeffs=[615,1471,658] proper_periods=[]
```

The full record is in:

```text
p24/prime_relative_normality_counterexample.md
```

So this is no longer a plausible broad theorem:

```text
prove prime-order relative normality modulo the selected split prime.
```

It may still be true as a p24-specific product certificate, but prime recovery
length by itself is not the missing explanation.  The surviving general
targets are exact packet content and the Hermitian p-unit scalar; both survived
the new row.
