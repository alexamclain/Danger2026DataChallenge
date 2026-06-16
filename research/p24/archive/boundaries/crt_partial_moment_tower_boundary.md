# CRT Partial-Moment Tower Boundary

This note records a useful but delicate refinement of the first
augmentation-jet target.

## Setup

For

```text
h = m*n,       gcd(m,n)=1,
```

write complement-section fibers

```text
F_r(X) = sum_k j_{n*r + m*k} X^k,       0 <= r < m.
```

The ordinary first moment is

```text
M_1(X) = sum_r r F_r(X),
```

with `r` represented by the integer in `[0,m)`.

For p24:

```text
m = 66254 = 2 * 157 * 211
n = 3107441.
```

Let `m = prod_i c_i` be the coprime prime-power decomposition, and let
`e_i` be the CRT idempotent:

```text
e_i == 1 mod c_i,
e_i == 0 mod c_j for j != i.
```

Define the partial moments

```text
P_i(X) = sum_{t=0}^{c_i-1} t * sum_{r == t mod c_i} F_r(X).
```

Each `P_i` is tower-shaped: it traces out all `K` factors except the
component of size `c_i`, so the visible intermediate degree is

```text
n * c_i.
```

For p24 these are:

```text
c_i = 2:   6214882
c_i = 157: 487868237
c_i = 211: 655670051
sum = 1149753170 = 0.001149753 * sqrt(10^24).
```

## Carry Trap

The tempting identity

```text
M_1 = sum_i e_i P_i
```

is false over `F_p` when `m` is composite.  It is only true modulo `m`.

Indeed, define the CRT lift

```text
tilde_r = sum_i e_i * (r mod c_i).
```

Then

```text
tilde_r == r mod m,
```

but usually `tilde_r != r` as an integer.  Since `p` does not divide `m`,
the difference does not vanish in `F_p`.

The exact identity is:

```text
sum_i e_i P_i(X) = M_1(X) + m*C(X),

C(X) = sum_r ((tilde_r - r)/m) F_r(X).
```

Equivalently:

```text
M_1(X) = CRT_M_1(X) - m*C(X),
CRT_M_1(X) = sum_i e_i P_i(X).
```

For p24, the idempotents are:

```text
e_2   = 33127
e_157 = 6752
e_211 = 26376
```

Already for `r=1`:

```text
33127 + 6752 + 26376 = 66255 = 1 + m.
```

So the carry is unavoidable.

## Toy Verification

I added:

```text
p24/augmentation_crt_derivative_toy.py
```

For the calibrated `D=-5000`, `h=30`, `m=6=2*3`, `n=5` toy:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/augmentation_crt_derivative_toy.py --D -5000 --m 6 --q-stop 200000
```

reports:

```text
naive_crt_linear_reconstruction_ok=0
carry_corrected_reconstruction_ok=1
```

For `m=5` prime, there is no nontrivial carry and the naive identity holds:

```text
naive_crt_linear_reconstruction_ok=1
```

Thus the first augmentation derivative itself is not unlocked by the
prime-factor tower unless the carry moment `C(X)` is also constructed.  The
carry function depends jointly on all CRT components, so it is not merely a
sum of single-component tower traces.

## Tower-Native Replacement

The CRT-linear object

```text
CRT_M_1(X) = sum_i e_i P_i(X)
```

is not the Hasse derivative, but it is still a legitimate scalar projection.
The exact content gate only needs a nonzero projection of the packet vector.
So a safer tower-native certificate target is:

```text
not all of M_0, P_2, P_157, P_211 vanish in any p24 packet.
```

Equivalently, for every packet factor `f_a | Phi_n`:

```text
gcd(f_a, M_0, P_2, P_157, P_211) = 1.
```

This target avoids the CRT carry while keeping all additional projections in
small intermediate layers.

## Small Scan

I added:

```text
p24/crt_partial_moment_projection_scan.py
```

Pinned `M_0` failures:

```text
D=-899, q=281, h=14, m=2, n=7:
  M0_zero=1
  first=P2
  m0_partial_family_failures=0

D=-216, q=103, h=6, m=2, n=3:
  M0_zero=1
  first=P2
  m0_partial_family_failures=0
```

Composite-`m` bounded scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/crt_partial_moment_projection_scan.py \
  --max-cases 100 --min-h 12 --max-h 180 --max-abs-D 90000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 180 --q-stop 800000 \
  --max-splitting-primes 2 --include-linear \
  --require-composite-m --summary-only
```

Output:

```text
packet_rows=702
content_failures=0
m0_failures=0
m0_crt_linear_pair_failures=0
m0_partial_family_failures=0
first_projection_histogram={'M0': 702}
```

So the new family has not failed, but the composite-`m` window did not even
stress it with an `M0` failure.

## Boundary

This is progress on the **construction shape**, not the p-unit theorem.

Positive:

```text
M_0 plus CRT partial moments gives a tower-native projection family.
For p24, the extra intermediate degrees sum to about 1.15e9, well below
sqrt(p)=1e12.
```

Negative:

```text
The literal first Hasse derivative M_1 has a carry term.
The carry term is joint in all K factors and may be as hard as the original
recovery labeling.
The selected-prime p-unit/nonvanishing proof is still missing.
```

The next refined theorem target is therefore:

```text
prove gcd(Phi_3107441, M_0, P_2, P_157, P_211) = 1 mod p,
```

with `P_c` defined as the embedded partial first moment over the `c`-factor
of the complement subgroup `K`.

## One-Scalar Packaging

The projection family can be packaged into one scalar:

```text
L_lambda(X) = M_0(X) + sum_i lambda_i P_i(X).
```

For any choice of `lambda_i`, the principal singular modulus has coefficient
`1`, because the principal term has `r=0` and hence contributes `0` to every
partial moment `P_i`.  Thus the same principal-term dominance proof used for
`M_0` still applies to small integer `lambda_i`.

The simplest p24 choice is:

```text
L_1 = M_0 + P_2 + P_157 + P_211.
```

Its coefficient on a complement coordinate `r` is:

```text
w(r) = 1 + (r mod 2) + (r mod 157) + (r mod 211),
```

so

```text
1 <= w(r) <= 368.
```

The original complement-trace dominance margin is about `2.538350e12` in log
scale, so losing the factor `368` is negligible:

```text
new_margin >= old_margin - log(368).
```

I added:

```text
p24/crt_partial_moment_linear_combo_scan.py
```

Pinned `M_0` failures:

```text
D=-899: first_good_lambda histogram {'(0,)': 5, '(1,)': 1}
D=-216: first_good_lambda histogram {'(0,)': 2, '(1,)': 1}
```

So `L_1 = M_0 + P_2` rescues the known prime-`n` `M0` failures.

Bounded composite-`m` search with `lambda_bound=2`:

```text
packet_rows=413
family_failures=0
candidate_failures=0
lambda_ones_failures=0
first_good_lambda_histogram={'(0, 0)': 413}
```

Fixed all-ones scan over prime and composite complement sizes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/crt_partial_moment_linear_combo_scan.py \
  --max-cases 80 --min-h 12 --max-h 160 --max-abs-D 70000 \
  --max-prime-quotients 8 --max-composite-quotients 8 \
  --min-n 3 --max-n 160 --q-stop 700000 \
  --max-splitting-primes 2 --include-linear \
  --fixed-lambdas 1 --summary-only
```

Output:

```text
packet_rows=516
family_failures=0
candidate_failures=0
lambda_ones_failures=0
first_good_lambda_histogram={'(1, 1)': 28, '(1,)': 488}
```

This supports a cleaner scalar target:

```text
prove Res(Phi_3107441, L_1) != 0 mod p.
```

This one-resultant theorem implies the projection-family gcd condition.  It
keeps the construction tower-shaped and keeps principal complex dominance.
It still leaves the same selected-prime p-unit/nonvanishing theorem to prove.

## Character Support Tradeoff

I added:

```text
p24/l1_character_support_audit.py
p24/l1_height_divisibility_audit.py
p24/l1_selected_origin_zero_scan.py
p24/l1_punit_boundary.md
```

For p24 it reports:

```text
axis_support_size=368
translation_stabilizer_size=1
translation_orbit_size=66254
H_eigen_zero_pdiv_exponent=n*ord_n_p=1207023307630
quotient_field_norm_packaging_survives=0
```

Interpretation:

```text
1. L_1 is still an H-character eigenvector.
   Therefore a selected zero propagates through the n H-conjugates and the
   Frobenius packet of size ord_n(p), just as for M_0.

2. L_1 is not K-trivial.
   Its K-character support is axis-shaped:

     trivial character
     + nontrivial characters on the 2-factor
     + nontrivial characters on the 157-factor
     + nontrivial characters on the 211-factor.

   This gives 1+(2-1)+(157-1)+(211-1)=368 full class-character resolvents
   per H-character.

3. The K-translation orbit of the coefficient function is full size m=66254.
   Thus L_1 depends on the selected K-origin.  It is not an element of the
   degree-n quotient field fixed by K, and it does not retain the clean
   quotient-field norm package of M_0.
```

So `L_1` improves the **construction shape** and one-resultant packaging, but
it weakens the p-adic theorem shape compared with the K-trivial complement
trace.  A proof of `Res(Phi_n,L_1) != 0 mod p` must control the selected
embedded K-origin or use the three intermediate tower layers directly; it is
not simply the complement trace p-unit theorem with better coefficients.
