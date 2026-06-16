# p24 Pomerance Certificate Research Log

Date: 2026-06-03 PDT

Target:

```text
p = 1000000000000000000000007 = 10^24 + 7
sqrt_floor(p) = 1000000000000
k = 40
2^k = 1099511627776
```

The verifier depth is one higher than p23.  Since the Hasse interval has
width `4*sqrt(p)+1`, only three group orders in the interval are divisible by
`2^40`.

```text
t =  1020608380936, v2(#E) = 42, odd part = 227373675443
t =   -78903246840, v2(#E) = 40, odd part = 909494701773
t = -1178414874616, v2(#E) = 41, odd part = 454747350887
```

The corresponding odd parts factor as:

```text
227373675443 = 29 * 71 * 110429177
909494701773 = 3 * 7 * 43309271513
454747350887 is prime
```

The prime odd part in the third target is useful only after the curve is
known: it makes projection to the 2-Sylow cheap.  It does not by itself select
the target isogeny class.  I wrote:

```text
p24/group_structure_audit.py
p24/prime_odd_part_small_probe.py
```

The group-structure audit records that, because `v2(p-1)=1`, the 2-primary
part is cyclic in the nonsplit Montgomery case and `C2 x C_{2^(v-1)}` in the
split case.  In particular, the middle target with `v2(#E)=40` must be on the
nonsplit/cyclic side to support an exact order-`2^40` point; split would have
2-primary exponent only `2^39`.

The small-field exact enumeration confirms that prime odd cofactors do not
create an obvious construction shortcut.  For example:

```text
python3 p24/prime_odd_part_small_probe.py

p=3037
k=7
target_signed_traces=[-94, -34, 34, 94]
side=curve trace=-34 order=3072 v2=10 odd=3  odd_prime=1
side=curve trace= 94 order=2944 v2= 7 odd=23 odd_prime=1
side=twist trace=-34 order=3072 v2=10 odd=3  odd_prime=1
side=twist trace= 94 order=2944 v2= 7 odd=23 odd_prime=1
side_counter=curve:210,twist:42
```

So even when all small target odd parts are prime, the task remains "hit the
right trace/isogeny class"; primality of the odd cofactor does not expose a
low-degree family of `A` values.

For the x-only verifier, the quadratic twist is not fixed by the certificate.
Thus the signed trace set for Montgomery `A` values is really:

```text
-1178414874616, -1020608380936, -78903246840,
  78903246840,  1020608380936,  1178414874616
```

These are only three discriminants up to sign, but trace-residue filters must
use the six signed traces unless they also fix the twist sign.

I added an elementary trace-shape audit:

```text
p24/target_trace_shape_audit.py
```

It records that for `p = n^2 + 7`, `n = 10^12`, the DANGER congruence is

```text
t == p + 1 == n^2 + 8 mod 2^40.
```

The six x-only traces are exactly the Hasse representatives of this residue
and its negative:

```text
python3 p24/target_trace_shape_audit.py

curve_side_residue=(p+1)_mod_2^k=1020608380936
opposite_xonly_residue=78903246840
v2(curve_side_residue)=3

signed_hasse_representatives:
  t=-1178414874616 ... v2(p+1-t)=41 v2(p+1+t)=4
  t=-1020608380936 ... v2(p+1-t)=4  v2(p+1+t)=42
  t=-78903246840   ... v2(p+1-t)=40 v2(p+1+t)=4
  t=78903246840    ... v2(p+1-t)=4  v2(p+1+t)=40
  t=1020608380936  ... v2(p+1-t)=42 v2(p+1+t)=4
  t=1178414874616  ... v2(p+1-t)=4  v2(p+1+t)=41
```

The obvious low-height near-square traces `0, +/-n, +/-2n` all have only
`v2=3` on both curve and twist sides.  The closest of them, `+n`, is still
`20,608,380,936` away from the nearest target trace.  Thus the target traces
come from the `2^40` residue condition, not from a visible low-height CM trace
formula.

## Immediate Consequences

The p23 `X1(16)` nonsplit method remains a credible fixed-prime tactic after
adapting square roots from `p == 5 mod 8` to this target's easier
`p == 3 mod 4` case.  But fixed `X1(16)` still only buys a constant factor,
not an asymptotic improvement.

The p24 congruence is suggestive but not enough for the known special-form
Pomerance construction:

```text
p == 11 mod 12
v2(p + 1) = 3
```

The trace-zero `j = 0` curve has order `p + 1` for `p == 2 mod 3`, but
`p + 1` has only a 2^3 factor, far below the required 2^40.

## CM / Prescribed-Order Audit

For a target trace `t`, CM construction would use the discriminant
`D = t^2 - 4p`.  It is fast only when the absolute discriminant has a large
square divisor, reducing the fundamental discriminant.

For p24 the three target absolute discriminants have no square divisor beyond
`2^2`:

```text
4p - 1020608380936^2
  = 2^2 * 29 * 25503090799682730273827

4p - (-78903246840)^2
  = 2^2 * 7 * 211 * 4973929 * 135907507341779

4p - (-1178414874616)^2
  = 2^2 * 599 * 1089874116562502921057
```

So the standard CM path has class-polynomial degree on the order of
`sqrt(|D|)`, and the known deterministic prescribed-subgroup construction has
no room to choose an auxiliary square factor: the required subgroup size is
already essentially `sqrt(p)`.

The small ramified factors in these discriminants do not create a cheap
self-isogeny shortcut.  A fixed point of the modular polynomial
`Phi_ell(j,j)=0` would require an actual endomorphism of degree `ell`, i.e. an
element of norm `ell` in the order:

```text
x^2 - Delta*y^2 = 4*ell.
```

For the p24 target discriminants `|Delta| >> 4*ell`, so the small ramified
ideals are not principal norm-`ell` ideals:

```text
python3 p24/ramified_self_loop_audit.py

trace=1020608380936   ell=29   has_norm_ell_element=False
trace=-78903246840    ell=7    has_norm_ell_element=False
trace=-78903246840    ell=211  has_norm_ell_element=False
trace=-1178414874616  ell=599  has_norm_ell_element=False
```

Thus the factors `7`, `29`, `211`, and `599` can support residue/status
filters, but they do not give a low-degree construction of the target CM
classes.

There is also a tempting near-square CM construction because

```text
p = 10^24 + 7 = (10^12)^2 + 7.
```

This gives a very cheap CM trace from the field of fundamental discriminant
`-7`, namely `t = +/- 2*10^12`.  I wrote:

```text
p24/near_square_cm_audit.py
```

The result is decisive for the strict verifier:

```text
python3 p24/near_square_cm_audit.py

cm_trace=2000000000000
  trace_mod_2^40=900488372224
  min_abs_distance_to_target=979391619064
  v2_order=3
  v2_twist_order=3

cm_trace=-2000000000000
  trace_mod_2^40=199023255552
  min_abs_distance_to_target=821585125384
  v2_order=3
  v2_twist_order=3
```

So `p = n^2 + 7` does give a fast known-trace curve, but it is not one of the
DANGER traces and both the curve and twist have only `2^3` in their group
orders.  It cannot produce a depth-40 x-only doubling certificate.

I also made this separation concrete by constructing an actual non-DANGER
elliptic certificate from the same near-square CM curve.  The class-number-one
`D=-7` curve has `j=-3375`; using

```text
E: y^2 = x^3 + a*x + b
```

with the standard `j`-model gives:

```text
p24/near_square_ecpp_certificate.py
p24/near_square_ecpp_certificate.json
```

The generated certificate verifies by finite-field group arithmetic:

```text
python3 p24/near_square_ecpp_certificate.py

j=-3375
trace=2000000000000
order=999999999998000000000008
order_factorization={'2': 3, '7': 1, '250698247': 1, '71229627932369': 1}
large_prime_factor=71229627932369
large_prime_gt_sqrt_p=True
v2_order=3
verification=PASS
danger3_bridge=NO_v2_order_is_only_3
```

The JSON records the curve, a point `P`, and `Q = [(#E)/q]P` of order
`q = 71229627932369`, with `q > sqrt(p)`.  This is a real fast elliptic
certificate in the broad ECPP/Pomerance sense.  But it gives no DANGER3 triple:
isogenies preserve the order, the quadratic twist has the opposite trace, and
both sides have only `v2=3`, so no transformation inside this CM class can
create an x-only point of order `2^40`.

To rule out the possibility that this is just a model mismatch, I converted the
same curve to Montgomery form:

```text
p24/near_square_montgomery_bridge_audit.py
```

The bridge audit finds rational 2- and 4-torsion and two Montgomery parameters:

```text
python3 p24/near_square_montgomery_bridge_audit.py

v2_order=3
v2_twist_order=3
two_torsion_x=214285714285833333333334
four_torsion_x=904761904761666666666673

montgomery_A=124999999999624999999999
  split_legendre_A2_minus_4=1
  max_curve_2power_exponent=2
  max_twist_2power_exponent=2

montgomery_A=875000000000375000000008
  split_legendre_A2_minus_4=1
  max_curve_2power_exponent=2
  max_twist_2power_exponent=2
```

So the fast `D=-7` certificate can indeed be expressed in Montgomery form, but
the split 2-primary structure has exponent only `4`.  The DANGER verifier
needs exact order `2^40`; a point of order `4` would hit infinity far too
early and fail the final `gcd(Zprev,p)=1` check.

I also tested whether the special shape `p = n^2 + 7` hides a low-height
Montgomery parameter formula that the CM audit would miss.  The script

```text
p24/near_square_formula_probe.py
```

uses the exact Montgomery trace convolution

```text
t(A) = - sum_c chi(c^2 - 4) chi(A + c)
```

to enumerate all Montgomery traces for small primes `p = n^2 + 7`, then tests
all small-coefficient linear fractional formulas for the signed parameter,
the squared parameter, and the Montgomery `j`-invariant

```text
A(n), A(n)^2, or j(n) = (a*n + b)/(c*n + d)
```

against the x-only DANGER trace bucket.

Four holdouts:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 1000 --max-p 250000 \
  --coeff-bound 5 --max-rows 40

rows=40
formula_count=6608
row=01 ... survivors_all_rows_so_far=862
row=02 ... survivors_all_rows_so_far=120
row=03 ... survivors_all_rows_so_far=12
row=04 ... survivors_all_rows_so_far=0
perfect_survivors=0
conclusion=no_low_height_LFT_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 10000 --max-p 1000000 \
  --coeff-bound 8 --max-rows 35

rows=35
formula_count=37296
row=01 ... survivors_all_rows_so_far=4026
row=02 ... survivors_all_rows_so_far=278
row=03 ... survivors_all_rows_so_far=14
row=04 ... survivors_all_rows_so_far=0
perfect_survivors=0
conclusion=no_low_height_LFT_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 10000 --max-p 1000000 \
  --coeff-bound 8 --max-rows 35 --square-parameter

square_parameter=True
rows=35
formula_count=37296
row=01 ... survivors_all_rows_so_far=1955
row=02 ... survivors_all_rows_so_far=63
row=03 ... survivors_all_rows_so_far=0
perfect_survivors=0
conclusion=no_low_height_LFT_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 10000 --max-p 1000000 \
  --coeff-bound 8 --max-rows 35 --j-parameter

j_parameter=True
rows=35
formula_count=37296
row=01 ... survivors_all_rows_so_far=1357
row=02 ... survivors_all_rows_so_far=34
row=03 ... survivors_all_rows_so_far=1
row=04 ... survivors_all_rows_so_far=0
perfect_survivors=0
conclusion=no_low_height_LFT_formula
```

So the near-square identity supplies the broad `D=-7` elliptic certificate,
but it does not appear to supply a simple rational-in-`n` Montgomery parameter
or `j`-parameter with the high `2^k` x-only trace condition.

I also checked the related bounded-height constant-parameter shortcut.  Maybe
the construction is not a formula in `n`, but a fixed small rational value of
`A`, `A^2`, or the Montgomery `j`-invariant that stays in the DANGER bucket for
the near-square family.  I wrote:

```text
p24/small_height_parameter_probe.py
```

It again uses exact trace convolution for small `p=n^2+7`, but intersects the
DANGER x-only bucket with all reduced rational constants of bounded height.

Holdouts:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/small_height_parameter_probe.py --min-p 10000 --max-p 1000000 \
  --max-rows 35 --height 80

height=80
A_candidate_count=7863
A2_candidate_count=3932
j_candidate_count=7863
row=01 ... survivors_A=864 survivors_A2=218 survivors_j=255
row=02 ... survivors_A=92  survivors_A2=8   survivors_j=3
row=03 ... survivors_A=4   survivors_A2=1   survivors_j=0
row=04 ... survivors_A=0   survivors_A2=0   survivors_j=0
conclusion=no_bounded_height_constant_parameter

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/small_height_parameter_probe.py --min-p 10000 --max-p 1000000 \
  --max-rows 35 --height 200

height=200
A_candidate_count=48927
A2_candidate_count=24464
j_candidate_count=48927
row=01 ... survivors_A=5078 survivors_A2=1300 survivors_j=1732
row=02 ... survivors_A=342  survivors_A2=54   survivors_j=33
row=03 ... survivors_A=24   survivors_A2=1    survivors_j=2
row=04 ... survivors_A=0    survivors_A2=0    survivors_j=0
conclusion=no_bounded_height_constant_parameter
```

Thus neither low-height rational functions in `n` nor fixed bounded-height
parameters explain the p24 target trace condition.

I also estimated the actual target class sizes to check whether one trace has
an unusually small hidden CM class.  The script:

```text
p24/cm_class_size_audit.py
```

uses a rough Euler-product estimate for `L(1, chi_D)` and the class-number
formula.  It is not a certified class-number computation, but it is enough to
separate "small class" from "sqrt-scale hidden subset":

```text
python3 p24/cm_class_size_audit.py

trace=1020608380936
  fundamental_D_K=-739589633190799177940983
  h_max_order_est=2.786879e+11
  random_j_expected_trials_est=3.588244e+12

trace=-78903246840
  fundamental_D_K=-998443569409526507503607
  h_max_order_est=8.329662e+11
  random_j_expected_trials_est=1.200529e+12

trace=-1178414874616
  fundamental_D_K=-652834595820939249713143
  h_max_order_est=2.060276e+11
  random_j_expected_trials_est=4.853718e+12
```

So the best CM target by this rough measure is the middle trace, but even that
is still a hidden isogeny-class subset of density about `8.3e-13`, i.e. the
same order as `1/sqrt(p)`.  An isogeny walk preserves trace, so without an
initial seed in the target isogeny class this does not become a sub-sqrt
construction.

I then checked whether the target trace classes nevertheless hide a deep
2-isogeny volcano that could be navigated from a cheap seed.  The answer is
no: the conductor of `Z[pi]` in the maximal CM order is only `2` for all three
target traces.  I wrote:

```text
p24/two_volcano_depth_audit.py
```

The output separates group-order 2-adic depth from CM-conductor depth:

```text
python3 p24/two_volcano_depth_audit.py

trace=1020608380936
  v2_group_order=42
  conductor_Zpi_in_OK=2
  v2_conductor=1

trace=-78903246840
  v2_group_order=40
  conductor_Zpi_in_OK=2
  v2_conductor=1

trace=-1178414874616
  v2_group_order=41
  conductor_Zpi_in_OK=2
  v2_conductor=1
```

So the large DANGER 2-power is Frobenius eigenvalue/orientation data, not a
long 2-volcano conductor chain.  There is no deep 2-isogeny descent/ascent
shortcut to the target classes.

I also checked the horizontal version of the same idea.  For all three target
fundamental fields `D_K == 1 mod 8`, so `2` splits in the CM field.  A direct
2-adic eigenvalue construction might hope that one of the split primes above
`2` has a very short class-group order, giving a short horizontal 2-isogeny
cycle.  I wrote:

```text
p24/split_two_ideal_relation_audit.py
```

If a power of a split prime above `2` is principal, its generator has norm
`2^m`.  But every non-scalar principal element in an imaginary quadratic order
of discriminant `D` has norm at least `|D|/4`, since

```text
4*N(alpha) = x^2 + |D|*y^2,  y != 0.
```

For p24 this gives:

```text
python3 p24/split_two_ideal_relation_audit.py

trace=1020608380936
  no_principal_power_of_split_2_before_m=78
  first_possible_power_norm=2^78=302231454903657293676544
  first_possible_norm_over_sqrt_p=3.022315e+11

trace=-78903246840
  no_principal_power_of_split_2_before_m=78
  first_possible_power_norm=2^78=302231454903657293676544
  first_possible_norm_over_sqrt_p=3.022315e+11

trace=-1178414874616
  no_principal_power_of_split_2_before_m=78
  first_possible_power_norm=2^78=302231454903657293676544
  first_possible_norm_over_sqrt_p=3.022315e+11
```

Thus even the split-prime-over-2 relation cannot be a short horizontal cycle.
The first possible principal split-2 relation already has norm far above
`sqrt(p)`, so a Landen/2-isogeny-cycle construction would not be the missing
sub-sqrt route.

I also scanned the exact DANGER trace congruence for small fundamental CM
discriminants:

```text
p24/small_cm_trace_search.py
```

The script CRT-combines `t^2 = 4p mod |D|` with
`t = p+1 mod 2^40` and checks the Hasse interval.  A run through
`|D| <= 100000` found no small-CM hits:

```text
python3 p24/small_cm_trace_search.py --max-abs-D 100000

compatible_traces=[-1178414874616, -78903246840, 1020608380936]

t=-1178414874616  fundamental_D=-652834595820939249713143
t=  -78903246840  fundamental_D=-998443569409526507503607
t= 1020608380936  fundamental_D=-739589633190799177940983

small_fundamental_D_hits=0
```

This closes the special-j/small-CM possibility more explicitly than the
initial `j=0` observation: the exact `2^40` trace congruence simply does not
intersect any small fundamental CM discriminant in the scanned range.

I also checked whether the target traces become cheap CM traces over a small
extension field and can then be descended.  If `E/F_p` has trace `t`, then over
`F_{p^m}` the trace `T_m` satisfies:

```text
T_0 = 2, T_1 = t, T_m = t*T_{m-1} - p*T_{m-2}
T_m^2 - 4*p^m = (t^2 - 4*p) * U_{m-1}(t,p)^2
```

so the extension discriminant differs from the base discriminant only by a
square factor.  I wrote:

```text
p24/extension_trace_cm_audit.py
```

Running through `m <= 8` verifies the identity for all three target traces and
reports `same_fundamental_D=True` at every extension degree:

```text
python3 p24/extension_trace_cm_audit.py --max-m 8

base_trace=1020608380936   base_fundamental_D_K=-739589633190799177940983
  m=2 ... same_fundamental_D=True
  ...
  m=8 ... same_fundamental_D=True

base_trace=-78903246840    base_fundamental_D_K=-998443569409526507503607
  m=2 ... same_fundamental_D=True
  ...
  m=8 ... same_fundamental_D=True

base_trace=-1178414874616  base_fundamental_D_K=-652834595820939249713143
  m=2 ... same_fundamental_D=True
  ...
  m=8 ... same_fundamental_D=True
```

Thus small extension/descent does not reduce the CM class-number barrier; it
only changes the conductor by a known square multiplier while preserving the
same large imaginary quadratic field.

I then checked a more structural CM escape hatch: perhaps we do not need the
full huge class polynomial if the target CM class is cut out by a short
isogeny cycle or a small principal relation.  For an order of discriminant
`D < 0`, a non-scalar principal relation of norm `n` comes from an element

```text
(x + y*sqrt(D))/2,  y != 0,
```

so

```text
4*n = x^2 + |D|*y^2.
```

Therefore every non-scalar relation has `n >= |D|/4`; below that bound the
only principal relations are scalar multiplications, which do not identify the
target CM class.  I wrote:

```text
p24/cm_relation_norm_barrier.py
```

For the three p24 target traces:

```text
python3 p24/cm_relation_norm_barrier.py

trace=1020608380936
  fundamental_D_K=-739589633190799177940983
  genus_factor_upper_bound=2
  min_non_scalar_principal_norm=184897408297699794485246
  min_norm_over_sqrt_p=1.848974e+11

trace=-78903246840
  fundamental_D_K=-998443569409526507503607
  genus_factor_upper_bound=8
  min_non_scalar_principal_norm=249610892352381626875902
  min_norm_over_sqrt_p=2.496109e+11

trace=-1178414874616
  fundamental_D_K=-652834595820939249713143
  genus_factor_upper_bound=2
  min_non_scalar_principal_norm=163208648955234812428286
  min_norm_over_sqrt_p=1.632086e+11
```

The genus reduction is also tiny: at most `8x` for the best trace.  Thus a
low-degree CM-relation/cycle construction is ruled out on norm grounds, not
just by failed search.  Any principal relation capable of selecting the target
CM class has degree far above `sqrt(p)`, so this cannot be the missing
asymptotic-speedup route.

I consolidated the CM/ray orientation facts in one script:

```text
p24/ray_orientation_audit.py
```

It records, for each target trace, that `D_K == 1 mod 8`, `2` splits, the
target order has conductor `2`, and the conductor-2 ring-class multiplier is
`1`.  It also prints the exact four `X0` eigenvalue roots modulo `2^40` and
the level-shift cost:

```text
python3 p24/ray_orientation_audit.py

trace=1020608380936
  D_K_mod_8=1 two_splits=True conductor_Zpi_in_OK=2
  ring_class_multiplier_h_4D_over_h_D=1/1

x0_eigenvalue_roots_at_level_k:
  lambda=1              ... v2(lambda-1)=40 v2(mu-1)=1  x1_orientation=True
  lambda=470852567047   ... v2(lambda-1)=1  v2(mu-1)=39 x1_orientation=False
  lambda=549755813889   ... v2(lambda-1)=39 v2(mu-1)=1  x1_orientation=False
  lambda=1020608380935  ... v2(lambda-1)=1  v2(mu-1)=40 x1_orientation=True

Gamma0(2^40)_index=1649267441664 index_over_sqrt_p=1.649267
Gamma0(2^41)_index=3298534883328 index_over_sqrt_p=3.298535
conclusion=ray_orientation_is_the_X0_to_X1_gap_and_level_shift_is_theta_2^k
```

So the ray-class/orientation formulation does not create a new CM escape
hatch: it is exactly the `X0`-to-`X1` orientation gap, and the natural
level-shift repair is already `Theta(2^k)`.

I then separated that norm barrier from the weaker question of genus
characters.  Genus characters only identify the class group modulo squares,
so if the p24 target class group had many prime-discriminant factors they
could, in principle, provide a cheap class selector.  I wrote:

```text
p24/genus_character_quotient_audit.py
```

For all three target traces the order discriminant is `Delta = 4*D_K` with
conductor `2`, and `D_K == 1 mod 8`, so `2` splits and the conductor-2 ring
class multiplier is exactly `1`.  The genus quotient is therefore just the
maximal-order quotient:

```text
python3 p24/genus_character_quotient_audit.py

trace=1020608380936
  prime_discriminant_factors=[29, -25503090799682730273827]
  genus_character_count=2
  genus_bits=1
  residual_classes_per_genus_est=1.393439e+11
  residual_entropy_bits_est=37.020

trace=-78903246840
  prime_discriminant_factors=[-7, -211, 4973929, -135907507341779]
  genus_character_count=8
  genus_bits=3
  residual_classes_per_genus_est=1.041208e+11
  residual_entropy_bits_est=36.599

trace=-1178414874616
  prime_discriminant_factors=[-599, 1089874116562502921057]
  genus_character_count=2
  genus_bits=1
  residual_classes_per_genus_est=1.030138e+11
  residual_entropy_bits_est=36.584
```

Thus even full genus information saves only `1`, `3`, and `1` bits
respectively, leaving about `2^36` to `2^37` hidden CM classes in a selected
genus.  This is a constant-factor filter, not an asymptotic route to a
DANGER3 triple.

## Asymptotic-Speedup Status

I also added a compact frontier note:

```text
p24/strict_danger3_frontier.md
```

It separates the broad fast certificates already found from the still-open
strict DANGER3 requirement, and summarizes the remaining live shape in one
place.

Known routes checked so far:

```text
fixed X1(16) / nonsplit halving: constant-factor only
generic growing X1(2^a): blocked by N^2 gonality/fiber cost
trace-residue filters: reduce expensive checks, not raw sqrt(p) entropy
special p == 11 mod 12 j=0 construction: v2(p+1) too small
small-CM construction: target discriminants have no large square part
prescribed-subgroup theorem: proven range m=o(sqrt(p)/(log p)^4), but DANGER needs m>sqrt(p)
```

The p24 numerical gap for the prescribed-subgroup theorem is large:

```text
python3 p24/prescribed_subgroup_range_audit.py

k = 40
m = 2^k = 1099511627776
sqrt(p)/(log p)^4 ~= 107224.067593
m / (sqrt(p)/(log p)^4) ~= 1.025434e+07
heuristic m*sqrt(p) runtime ~= 1.099512e+24
```

So the Shparlinski-Sutherland deterministic construction is not merely just
outside its proof range; for the needed DANGER level it is millions of times
above the allowable `m` scale and has no useful runtime saving.

The same paper's probabilistic flexible-divisor theorem is also mismatched to
the strict verifier.  It can output some divisor `m in [M,2M]` when
`M <= p^(1/2-epsilon)`, but DANGER fixes the divisor to be the pure power
`2^k` just above the Hasse-prime-divisor bound.  I wrote:

```text
p24/flexible_divisor_theorem_audit.py
```

For p24:

```text
python3 p24/flexible_divisor_theorem_audit.py

danger_k=40
danger_m=2^k=1099511627776
danger_m_over_sqrt=1.099511627776
danger_m_minus_sqrt=99511627776
danger_m_over_sqrt_over_log4=1.025434e+07
epsilon_if_using_M_2^(k-1)=1.082626e-02
epsilon_if_using_M_2^k=-1.716659e-03
strict_target=exact_power_of_two_not_arbitrary_divisor
```

Thus the flexible theorem is solving a nearby but materially different
problem: "find a curve order with some large divisor."  The DANGER3 verifier
needs "find a curve/twist order divisible by this exact `2^k > sqrt(p)`."

Sutherland's optimized `X1(2^a)` plane models show the expected growing-fiber
cost:

```text
python3 p24/x1_degree_growth_audit.py

X1(32): degree_x=11 degree_y=10 total_degree=16 terms=87
X1(64): degree_x=42 degree_y=40 total_degree=60 terms=1192
```

This does not rule out a genuinely different recursive tower sampler, but it
does rule out "just use the next optimized plane model" as an asymptotic
section.  The observed 32-to-64 fiber growth matches the `N^2` modular-curve
barrier already seen in the p23 notes.

I also wrote the corresponding p24 gonality note:

```text
p24/x1_section_gonality_barrier.md
```

For `N = 2^a`,

```text
[SL2(Z) : Gamma1(N)] = (3/4) * N^2
gonality(X1(2^a)) = Omega(N^2)
```

and the x-only sign quotient changes this only by a constant factor.  Thus a
true rational/bounded-genus tower section with overhead `N^alpha` and
`alpha < 1` cannot exist for the full order-`N` marked-point condition.  The
remaining "special 2-power tower" possibility must therefore mean genuinely
p-specific finite-field arithmetic, not a hidden rational parametrization of
the growing `X1(2^a)` tower.

The remaining live mathematical target is therefore sharper than for p23:

```text
Find a way to construct a curve in one of the three target isogeny classes,
or a point in the depth-40 Montgomery doubling preimage tree, without paying
class-number/sqrt(p) scale.
```

The most plausible directions are:

```text
1. a genuinely special 2-power tower section for cyclic 2-Sylow curves;
2. an inverse-doubling chain parameterization that removes the search over A;
3. a p24-specific trace construction not passing through large-D CM.
```

I then made the "partial oriented tower sampler" cost model explicit.  If one
could sample candidates already known to have x-only order `2^h` at amortized
cost

```text
C_h = 2^(beta*h),
```

then the remaining search would cost about `2^(40-h)`, and a strict sub-sqrt
route would need `beta < 1` for growing `h`.  Rejection from random
Montgomery `A` has `beta ~= 1`; `X0(2^h)` has constant density but lacks the
orientation.  I wrote:

```text
p24/partial_oriented_sampler_exponent_audit.py
```

It exact-counts, over small `p = n^2 + 7` fields, both the strict
split-corrected `X1` x-only bucket and the larger `X0` cyclic-chain bucket at
each depth.  A depth-9 aggregate run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py --min-p 50000 \
  --max-p 350000 --max-rows 10 --fit-min-depth 5

aggregate
  depth x1_count x1_density x1_cost x0_count x0_density x0_cost x0_over_x1
   5   261384 0.25021012      3.997   783486 0.74999282      1.333      2.997
   6   129036 0.12351985      8.096   783486 0.74999282      1.333      6.072
   7    64048 0.06131002     16.311   783486 0.74999282      1.333     12.233
   8    33568 0.03213300     31.121   783486 0.74999282      1.333     23.340
   9    17258 0.01652024     60.532   783486 0.74999282      1.333     45.398
aggregate_fitted_beta_x1=0.978428
aggregate_fitted_beta_x0=0.000000
```

A depth-10 run gives the same shape:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py --min-p 260000 \
  --max-p 900000 --max-rows 4 --fit-min-depth 5

aggregate_fitted_beta_x1=0.969191
aggregate_fitted_beta_x0=0.000000
```

Thus exact near-square data shows the expected dichotomy: oriented `X1` depth
shrinks at essentially one independent 2-adic bit per level, while `X0`
remains cheap only because it omits the orientation.  Any successful partial
tower sampler still needs a new mechanism that beats this measured
`beta ~= 1` rejection exponent.

## Small Calibration

`p24/x16_p24_calibration.py` adapts the p23 Python formulas to p24-style
`p == 7 mod 8` primes using a generic square-root helper.  A quick run:

```text
python3 p24/x16_p24_calibration.py --samples 3000 --target-depth 14 --start 50000
```

produced:

```text
calibration_prime = 57527
p_mod_8 = 7
accepted_x16 = 3000
nonsplit = 1474
nonsplit survive_depth_8 = 90/1474 = 0.061058
nonsplit survive_depth_10 = 14/1474 = 0.009498
```

Interpretation: the p24 residue class does not block the X1(16) machinery.
The p23 C code's `p == 5 mod 8` guard is implementation-specific.  But this
calibration is still fixed-level prescribed torsion, hence not the requested
asymptotic speedup.

I then tested the first non-generic rung from `X1(16)` toward `X1(32)`.  The
first-lift cover is

```text
z^2 = H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2).
```

For p23, quotient-derived Legendre/quartic features on this cover gave only
weak constant lifts.  Since p24-style primes have `p == 3 mod 4`, the factors
`u - 2 +/- 2i` live in `Fp2`, not `Fp`, so I wrote a p24-specific scan:

```text
p24/x16_first_lift_p24_feature_scan.py
```

It samples nonsplit `X1(16)` rows conditioned on `H(y)` square, computes
first-branch halving depth, and buckets by:

```text
u = (y^2 - 2)/(y - 1)
Legendre classes of u, u-2, (u-2)^2+4
Fp2 square/quartic classes of u-2+/-2i
Legendre classes of low-degree Norm(q(y)+z)=q(y)^2-H(y)
```

Two 12k holdouts at the p24-congruence calibration prime `p=57527`:

```text
python3 p24/x16_first_lift_p24_feature_scan.py \
  --accepted 12000 --seed 20260604 --target-depth 12

base depth-12 survival = 292/12000 = 0.024333
best bucket lift = 1.294462
best explicit quotient bucket lift ~= 1.16

python3 p24/x16_first_lift_p24_feature_scan.py \
  --accepted 12000 --seed 20260605 --target-depth 12

base depth-12 survival = 286/12000 = 0.023833
best bucket lift = 1.310318
best explicit quotient bucket lift = 1.163980
```

A larger 40k holdout:

```text
python3 p24/x16_first_lift_p24_feature_scan.py \
  --accepted 40000 --seed 20260606 --target-depth 12

base depth-12 survival = 1036/40000 = 0.025900
best low-degree norm bucket lift = 1.261512
best explicit Fp2 quotient bucket lift = 1.165762
capture of explicit quotient bucket = 0.579151
```

So the first-lift cover has visible algebraic signal over p24-style primes,
but only as a small constant-factor ranking feature.  The top low-degree norm
bucket changes across seeds, and the natural `Fp2` quotient classes give about
`1.16x`, not a growing tower selector.  This does not close every imaginable
special 2-power identity, but it rules out the visible first-lift
quotient/norm shortcut as the missing asymptotic primitive.

I also checked whether the near-square family hides a simple section one level
upstream from the final Montgomery parameter.  The previous formula probes
tested low-height expressions for `A`, `A^2`, and `j`; a section could
conceivably be simple in the `X1(16)` parameter and complicated after the
Montgomery conversion.  I wrote:

```text
p24/x16_near_square_section_probe.py
```

For small primes `p = n^2 + 7` with `n == 0 mod 8`, the script enumerates the
`X1(16)` y-line exactly, converts each valid y to its Montgomery parameter,
uses the exact Montgomery trace convolution, and marks only curves whose
curve or twist has enough x-only 2-power for the local DANGER depth.  It then
tests low-height LFTs in `n` for three upstream parameters:

```text
y
y^2
u = (y^2 - 2)/(y - 1)
```

The larger holdout used coefficient bound `8`, matching the earlier
`A`/`A^2`/`j` formula probes:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x16_near_square_section_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode y

formula_count=37296
row=01 ... survivors_all_rows_so_far=1788
row=02 ... survivors_all_rows_so_far=81
row=03 ... survivors_all_rows_so_far=5
row=04 ... survivors_all_rows_so_far=1
row=05 ... survivors_all_rows_so_far=0
conclusion=no_low_height_x16_section_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x16_near_square_section_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode y2

formula_count=37296
row=01 ... survivors_all_rows_so_far=1808
row=02 ... survivors_all_rows_so_far=83
row=03 ... survivors_all_rows_so_far=1
row=04 ... survivors_all_rows_so_far=0
conclusion=no_low_height_x16_section_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x16_near_square_section_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode u

formula_count=37296
row=01 ... survivors_all_rows_so_far=899
row=02 ... survivors_all_rows_so_far=23
row=03 ... survivors_all_rows_so_far=0
conclusion=no_low_height_x16_section_formula
```

So the near-square identity does not appear to produce a low-height section
on the `X1(16)` y-line, its square, or the natural first-lift quotient `u`.
This is stronger than the earlier `A`/`j` formula scan: a simple upstairs
section would have survived here even if its image in `A` looked complicated.

I then checked the analogous split-Montgomery / Legendre coordinates.  A
split Montgomery curve

```text
y^2 = x*(x^2 + A*x + 1)
```

has roots `r` and `1/r` of `x^2 + A*x + 1`, so

```text
A = -(r + 1/r)
lambda = r^2
j = 256*(1 - lambda + lambda^2)^3/(lambda^2*(1-lambda)^2).
```

Thus `r` or `lambda` could be low-height in `n` even when `A` and `j` are not.
This only tests the split subcase, so the local DANGER condition is stricter:
because full rational 2-torsion lowers the 2-primary exponent by one, the
curve or twist order needs `v2 >= k+1`.

I wrote:

```text
p24/legendre_near_square_parameter_probe.py
```

It computes exact Montgomery traces for small `p = n^2 + 7`, keeps only split
curves with enough x-only 2-power, and tests low-height LFTs in `n` for:

```text
root:    r and 1/r
lambda:  the full S3 orbit of lambda = r^2
landen:  (1-r)/(1+r), also with r inverted
```

The bound-8 holdouts:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/legendre_near_square_parameter_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode root

formula_count=37296
row=01 ... survivors_all_rows_so_far=1592
row=02 ... survivors_all_rows_so_far=72
row=03 ... survivors_all_rows_so_far=4
row=04 ... survivors_all_rows_so_far=0
conclusion=no_low_height_legendre_parameter_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/legendre_near_square_parameter_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode lambda

formula_count=37296
row=01 ... survivors_all_rows_so_far=1170
row=02 ... survivors_all_rows_so_far=26
row=03 ... survivors_all_rows_so_far=0
conclusion=no_low_height_legendre_parameter_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/legendre_near_square_parameter_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --mode landen

formula_count=37296
row=01 ... survivors_all_rows_so_far=1592
row=02 ... survivors_all_rows_so_far=72
row=03 ... survivors_all_rows_so_far=4
row=04 ... survivors_all_rows_so_far=0
conclusion=no_low_height_legendre_parameter_formula
```

So the near-square identity also does not expose a low-height split
2-torsion-root, Legendre-modulus, or Landen-coordinate section for the strict
DANGER trace condition.

Finally, because the prime family itself is quadratic in `n`, I widened the
formula family from LFTs to degree-2 rational maps:

```text
(a*n^2 + b*n + c)/(d*n^2 + e*n + f).
```

I wrote:

```text
p24/quadratic_near_square_parameter_probe.py
```

It reuses the exact marker sets from the `X1(16)` and Legendre probes, then
intersects them with all primitive degree-2 rational functions of bounded
coefficient height.  With coefficient bound `3`, there are `57,360` candidate
formulas.  I tested all six near-square coordinates:

```text
legendre-root
legendre-lambda
legendre-landen
x16-y
x16-y2
x16-u
```

Representative and worst-surviving rows:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/quadratic_near_square_parameter_probe.py --mode legendre-lambda \
  --min-p 10000 --max-p 180000 --max-rows 16 --coeff-bound 3

formula_count=57360
row=01 ... survivors_all_rows_so_far=1862
row=02 ... survivors_all_rows_so_far=28
row=03 ... survivors_all_rows_so_far=0
conclusion=no_low_height_quadratic_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/quadratic_near_square_parameter_probe.py --mode legendre-root \
  --min-p 10000 --max-p 180000 --max-rows 16 --coeff-bound 3

row=01 ... survivors_all_rows_so_far=2248
row=02 ... survivors_all_rows_so_far=72
row=03 ... survivors_all_rows_so_far=0
conclusion=no_low_height_quadratic_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/quadratic_near_square_parameter_probe.py --mode x16-u \
  --min-p 10000 --max-p 180000 --max-rows 16 --coeff-bound 3

row=01 ... survivors_all_rows_so_far=1392
row=02 ... survivors_all_rows_so_far=37
row=03 ... survivors_all_rows_so_far=1
row=04 ... survivors_all_rows_so_far=0
conclusion=no_low_height_quadratic_formula

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/quadratic_near_square_parameter_probe.py --mode x16-y2 \
  --min-p 10000 --max-p 180000 --max-rows 16 --coeff-bound 3

row=01 ... survivors_all_rows_so_far=2701
row=02 ... survivors_all_rows_so_far=123
row=03 ... survivors_all_rows_so_far=9
row=04 ... survivors_all_rows_so_far=2
row=05 ... survivors_all_rows_so_far=0
conclusion=no_low_height_quadratic_formula
```

The remaining two modes, `legendre-landen` and `x16-y`, also vanish by rows
`3` and `4` respectively.  Thus the tested near-square formula obstruction is
not just an LFT artifact: low-height quadratic-rational formulas in the most
natural strict-DANGER coordinates also behave like random hits and do not
persist.

I then closed a gap between single-valued rational formulas and generic
modular-curve rootfinding: a fixed-degree algebraic section for the final
Montgomery parameter.  In the family `p = n^2 + 7`, every polynomial
coefficient in `n` reduces modulo `p` to `a*n + b`, so I tested all low-height
implicit quadratics

```text
(a2*n+b2)*A^2 + (a1*n+b1)*A + (a0*n+b0) = 0.
```

Such a formula would be a two-valued closed construction for p24: solve one
quadratic and test its roots.  The script is:

```text
p24/implicit_quadratic_section_probe.py
```

With coefficient bound `4`, exact split-corrected small-field testing gives:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/implicit_quadratic_section_probe.py --min-p 10000 --max-p 220000 \
  --max-rows 16 --coeff-bound 4 --top 12

section_count=254616
row=01 ... perfect_survivors=8603
row=02 ... perfect_survivors=238
row=03 ... perfect_survivors=14
row=04 ... perfect_survivors=0
conclusion=no_low_height_implicit_quadratic_section
```

The last near misses are again paired by the `A -> -A` symmetry and disappear
on the next field.  This does not rule out high-degree or high-height
p-specific algebraic constructions, but it rules out the natural fixed
quadratic section over `Q(n)` that the earlier rational probes would have
missed.

I also tested the smallest implicit cubic version:

```text
p24/implicit_cubic_section_probe.py
```

This scans equations

```text
sum_{i=0}^3 (a_i*n+b_i)*A^i = 0
```

with nonzero cubic coefficient.  To keep the computation in the intended
small-scale regime, it evaluates each candidate only on the exact good-`A`
set for each calibration field.  With coefficient bound `2`:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/implicit_cubic_section_probe.py --min-p 10000 --max-p 220000 \
  --max-rows 16 --coeff-bound 2 --top 12

section_count=184584
row=01 ... hit_survivors=6241
row=02 ... hit_survivors=138
row=03 ... hit_survivors=0
conclusion=no_low_height_implicit_cubic_section
```

This is a smaller height range than the quadratic audit, but it rules out the
most obvious three-valued algebraic sections over `Q(n)`.

## Inverse-Chain Ansatz

For the affine map

```text
f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1)),
```

an edge `x -> t` determines `A` by a rational formula.  If the terminal
state is a root `u` of `x^2 + A*x + 1`, then `A = -(u + 1/u)`.

I tested the simple geometric inverse-chain ansatz:

```text
x_i = c^i * u
```

The first inverse edge imposes:

```text
u^2 = 1 / (c*(2-c)).
```

The second edge is then consistent only when:

```text
c^3 - 5*c^2 - 8*c - 4 = 0.
```

This looked promising, but the third edge adds an independent obstruction.
Over the p24 field, the cubic and the third-edge obstruction have gcd 1:

```text
python3 p24/inverse_chain_ansatz.py
p24_gcd(cubic, third_obstruction)_degree = 0
```

So this simple geometric section does not produce a depth-growing
construction for p24.

I also tested the zero-terminal fractional-linear iteration ansatz:

```text
x_0 = 0
x_1 = 1
x_{i+1} = (a*x_i + 1)/(c*x_i + 1)
```

with the requirement that the edge-determined Montgomery parameter
`A(x_{i+1}, x_i)` be independent of `i`.  The only common factor in the next
compatibility equations is `(a-c)^3`, which is the trivial constant-map case:

```text
python3 p24/inverse_chain_lft_ansatz.py
gcd(depth3, depth4) = (a - c)^3
gcd(depth3, depth5) = (a - c)^3
after_removing_a_minus_c gcd(depth3, depth4) = 1
after_removing_a_minus_c gcd(depth3, depth5) = 1
p24_gcd_reduced_depth3_depth4_total_degree = 0
p24_gcd_reduced_depth3_depth5_total_degree = 0
```

So the simplest Möbius-section model for the inverse-doubling tower is also
closed.

I later made the universal rational 2-torsion branch explicit.  The nonsplit
Montgomery branch used in the successful p23 search terminates at `x=0`, not
at a split root of `x^2 + A*x + 1`.  Since `f_A(+/-1)=0` for every `A`, a
sub-sqrt shortcut might conceivably come from a simple long inverse chain

```text
x_1 = 1 -> x_0 = 0
```

with the same edge-determined `A` on every earlier step.  I wrote:

```text
p24/universal_2torsion_branch_ansatz.py
```

It tests geometric, arithmetic, fixed-terminal LFT/geometric, and quadratic
recurrence sections.  The common compatibility factors are all degenerate:

```text
python3 p24/universal_2torsion_branch_ansatz.py

geometric_terminal_x0_branch
diff_gcd = (c - 1)^3
after_removing_constant_orbit = 1

arithmetic_terminal_x0_branch
diff_gcd = d^3
after_removing_constant_orbit = 1

lft_geometric_terminal_x0_branch
diff_gcd = (a - b)^3*(c - 1)^3
after_removing_degenerate_factors = 1

quadratic_recurrence_terminal_x0_branch
diff_gcd = c^3*(c - 2)^2
after_removing_degenerate_factors = 1
```

Thus the rational 2-torsion terminal branch has the same obstruction as the
split-terminal experiments: the obvious one-parameter inverse-chain sections
collapse to constant or invalid orbits.

I then tested a broader LFT-of-geometric orbit through the terminal point:

```text
x_i = u * (1 + a*(c^i - 1)) / (1 + b*(c^i - 1))
A = -(u + 1/u)
```

This contains ordinary geometric progressions and general fractional-linear
orbits with a chosen terminal `u`.  The first edge determines `u^2`; after
that, the next two compatibility equations share only the trivial factors
corresponding to a constant orbit:

```text
python3 p24/inverse_chain_lft_geometric_ansatz.py
u_squared_from_first_edge =
  -(b*c - b + 1)^2 / ((a*c - a + 1)*(a*c - a - 2*b*c + 2*b - 1))
gcd(edge2, edge3) = (a - b)^3*(c - 1)^3
after_removing_trivial_factors = 1
p24_reduced_gcd_total_degree = 0
```

So the natural "conjugated geometric progression" family is also closed.

The quotient coordinate

```text
s = x + 1/x
```

is cleaner for doubling:

```text
y = f_A(x) = (s^2 - 4)/(4*(s + A))
R_A(s) = y + 1/y
```

and the terminal pre-infinity state is simply `s = -A`.  I therefore tested
low-degree inverse-chain sections directly in `s`:

```text
shifted geometric: s_i = -A + d*(c^i - 1)
terminal LFT:      s_i = (-A + r*(c^i - 1))/(1 + b*(c^i - 1))
```

After eliminating the first-edge quadratic relation, the next two edge
conditions again share only degenerate factors:

```text
python3 p24/inverse_chain_s_coordinate_ansatz.py

shifted_geometric_s_orbit
gcd(resultants) = d^6*(c - 1)^6
after_removing_trivial = 1
p24_reduced_gcd_total_degree = 0

terminal_lft_s_orbit
gcd(resultants) = (-2*b + r)^3*(2*b + r)^3*(c - 1)^6
after_removing_degenerate_factors = 1
p24_reduced_gcd_total_degree = 0
```

The apparent `r = +/- 2b` branches are not surviving sections; on the
nonsingular first-edge branch their later-edge gcd is only pole/constant
factors:

```text
16*b^3*(c - 1)^3*(b*c - b + 1)^4
```

So the natural low-degree Kummer-line section families in both `x` and
`s=x+1/x` are now closed.

There is one more useful coordinate for this question.  If

```text
y = (s^2 - 4)/(4*(s + A)),  s_next = y + 1/y,
```

write `r = 1/y`, so `s_next = r + 1/r`.  Consecutive edge variables then
share the same Montgomery parameter exactly when

```text
A = F(r_prev, r_next)
  = r_next*(r_prev - 1/r_prev)^2/4 - (r_prev + 1/r_prev).
```

I wrote:

```text
p24/edge_coordinate_ansatz.py
```

and tested three low-dimensional section shapes:

```text
r_i = u*c^i
r_i = u*(1+a*(c^i-1))/(1+b*(c^i-1))
r_i = u^(2^i)
r_i = u + d*i
r_i = u + d*i + e*i^2
r_{i+1} = r_i^2 - c
```

The common fixed-`A` edge conditions again have only degenerate factors:

```text
python3 p24/edge_coordinate_ansatz.py

geometric_edge_coordinate_orbit
diff_gcd = c - 1
nondegenerate_diff_gcd = 1

lft_geometric_edge_coordinate_orbit
diff_gcd = (a - b)*(c - 1)
after_removing_degenerate_factors = 1

power_map_edge_coordinate_orbit
diff_gcd = (u - 1)^3
after_removing_u_minus_1 = 1

polynomial_edge_coordinate_orbits
linear_diff_gcd = d
linear_after_removing_constant_step = 1
quadratic_diff_gcd = 1

quadratic_recurrence_edge_coordinate_orbit
recurrence = r_{i+1} = r_i^2 - c
diff_gcd = -c + u**2 - u
after_removing_constant_orbit_total_degree = 0
```

So the edge square-root coordinate also does not expose a cheap geometric,
LFT-geometric, multiplicative-power, arithmetic, quadratic-polynomial, or
one-parameter quadratic-recurrence section for the long inverse chain.  In the
last case the only common factor is `c = u^2 - u`, which makes
`r_1 = r_0` and therefore gives a constant orbit.

## Odd Trace / Mixed-Modulus Audit

`p24/trace_lattice_model.py` enumerates the Hasse trace lattice exactly and
measures ideal odd-residue filters.  This is not a curve sampler; it only
answers how much entropy trace congruences could remove if they were available
for free.  Use `--xonly` to allow both quadratic-twist signs, which is the
right model for the verifier unless the construction fixes the twist.

At depth 28 there are 14,901 traces satisfying the `2^28` congruence.  The
best two-prime odd residue examples among primes up to 71 behave almost
exactly like independent residue filters:

```text
python3 p24/trace_lattice_model.py --d-min 20 --d-max 32 --combo-d 28 \
  --ells 5 7 11 13 17 19 29 31 37 41 43 47 53 59 61 67 71

combination_summary d=28 total=14901
  combo=(67, 71) product=4757 28/14901 = 0.001879
  combo=(61, 71) product=4331 28/14901 = 0.001879
  combo=(59, 71) product=4189 28/14901 = 0.001879
```

Prefixing small primes can isolate the three target traces at much lower
2-adic depth; for example at `d=20`, the cumulative filter through `ell=37`
already leaves exactly the three p24 target traces among 3,814,697 lattice
points.

Interpretation: trace congruences are arithmetically powerful, but only if they
can be imposed as construction data.  As rejection filters they pay back only
the entropy they remove, and generic modular-curve conditions of growing odd
level have the same gonality/fiber-cost problem as growing `X1(2^a)`.

The twist-symmetric `--xonly` model makes these odd filters weaker.  At
`d=28`, for example, the best two-prime filters among `5..41` leave hundreds
of traces, not dozens.  I corrected the x-only lattice model to enumerate the
union of the two 2-adic branches `t == +/- (p+1) mod 2^d`; this doubles the
one-branch counts while leaving rates unchanged:

```text
python3 p24/trace_lattice_model.py --xonly --d-min 38 --d-max 40 \
  --combo-d 28 --ells 5 7 11 13 17 19 29 31 37 41

combo=(37, 41) product=1517 355/14901 = 0.023824
combo=(31, 41) product=1271 423/14901 = 0.028387

corrected x-only union:
combo=(37, 41) product=1517 710/29802 = 0.023824
combo=(31, 41) product=1271 846/29802 = 0.028387
```

So odd residue filters are even less plausible as the missing asymptotic
primitive in the actual x-only setting.

To make the information-versus-construction split sharper, I added a greedy
exact-residue selector:

```text
p24/trace_residue_selector_audit.py
```

It enumerates the corrected x-only 2-adic lattice
`t == +/- (p+1) mod 2^d` and greedily picks odd primes whose exact target
residue sets leave the fewest traces.  This is an ideal oracle calculation:
it assumes exact trace residues are available for free.

At depth 28:

```text
python3 p24/trace_residue_selector_audit.py --d 28 --max-ell 200

initial_lattice_count=29802
step=1 ell=199 survivors=898 product=199
step=2 ell=191 survivors=24 product=38009
step=3 ell=37  survivors=6  product=1406333
isolated_exact_xonly_targets=True
```

At depth 20:

```text
python3 p24/trace_residue_selector_audit.py --d 20 --max-ell 200

initial_lattice_count=7629394
step=1 ell=199 survivors=230032 product=199
step=2 ell=197 survivors=7004   product=39203
step=3 ell=193 survivors=214    product=7566179
step=4 ell=113 survivors=10     product=854978227
step=5 ell=13  survivors=6      product=11114716951
isolated_exact_xonly_targets=True
```

This confirms that exact residues are arithmetically strong: modest odd
moduli can isolate the p24 target traces once some 2-adic prefix is fixed.
But this does not by itself beat sqrt scaling.  As rejection filters these
residues do not reduce the number of random curves needed to encounter the
trace class; as construction data the selected odd primes represent growing
modular information rather than a cheap sampler.

I then tested the cheaper Atkin/Elkies status variant: for an odd prime `ell`,
look only at whether

```text
Delta_ell = t^2 - 4p mod ell
```

is a square, nonsquare, or zero.  This is much coarser than exact trace
residue data, but in principle it could be cheaper to obtain from modular
polynomial root/no-root tests.  The model script is:

```text
p24/atkin_status_lattice_model.py
```

For the signed x-only target set at depth 28:

```text
python3 p24/atkin_status_lattice_model.py --d 28 --combo-size 3 \
  --ells 5 7 11 13 17 19 29 31 37 41

ell=  5 target_status=[-1]
ell=  7 target_status=[-1, 0]
ell= 11 target_status=[-1, 1]
ell= 13 target_status=[-1]
ell= 17 target_status=[-1, 1]
ell= 19 target_status=[-1, 1]
ell= 29 target_status=[-1, 0, 1]
ell= 31 target_status=[-1, 1]
ell= 37 target_status=[-1, 1]
ell= 41 target_status=[-1, 1]

through_ell= 13 ... 6882/29802:0.230924
combo=(5, 7, 13) ... 6882/29802:0.230924
```

Only `ell = 5, 7, 13` remove anything among these small status predicates.
The other tested primes either admit both square and nonsquare status for the
target traces, or all three statuses.  Running the same script with
`--curve-only` gives the same result because status depends on `t^2`, not the
trace sign.  As with the exact-residue model, the corrected x-only union
doubles the counts but leaves the ratios unchanged.

Conclusion: Atkin/Elkies status tests supply at most a few cheap half-bits in
this range, far weaker than exact trace residues.  As rejection filters they
do not reduce the underlying random-curve entropy; as construction data they
become another growing-level `X0`/status-intersection problem rather than an
asymptotic shortcut.

I then checked whether the high 2-adic bucket is visibly controlled by
low-degree quadratic-character labels in the raw Montgomery parameter `A`.
This is a direct version of the "cheap curve-level trace-v2 label" hope:
maybe a small Legendre symbol in `A` predicts the strict x-only DANGER bucket
without doing point counting.  I wrote:

```text
p24/low_degree_character_trace_scan.py
```

For small `p = n^2 + 7`, it computes every Montgomery trace exactly by
convolution, marks the strict x-only bucket with the split exponent correction,
and scans labels of the form:

```text
chi(q(A,n))
q(A,n) = c2(n)*A^2 + c1(n)*A + c0(n)
ci(n) = ai*n + bi
```

With coefficient bound `2`, allowing linear dependence on `n`, ten small
near-square fields give:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/low_degree_character_trace_scan.py --min-p 10000 --max-p 140000 \
  --max-rows 10 --coeff-bound 2 --top 6

aggregate good=10482/360626 base_rate=0.029066
aggregate_top_features
  sign=-1 lift=1.485 capture=0.743 coverage=0.500
    feature=((0)n+0)*A^2+((1)n+1)*A+((-2)n+-2)
  sign=-1 lift=1.485 capture=0.743 coverage=0.500
    feature=((0)n+0)*A^2+((1)n+-1)*A+((2)n+-2)
  sign=-1 lift=1.485 capture=0.743 coverage=0.500
    feature=((0)n+0)*A^2+((0)n+1)*A+((0)n+-2)
best_aggregate_lift=1.485000
conclusion=only_constant_scale_low_degree_character_labels_seen
```

The constant-coefficient version shows the same best labels more transparently:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/low_degree_character_trace_scan.py --min-p 10000 --max-p 140000 \
  --max-rows 10 --coeff-bound 2 --constant-coeffs --top 4

aggregate good=10482/360626 base_rate=0.029066
aggregate_top_features
  sign=-1 lift=1.485 capture=0.743 coverage=0.500 feature=A-2
  sign=+1 lift=1.485 capture=0.743 coverage=0.500 feature=A+2
best_aggregate_lift=1.485000
conclusion=only_constant_scale_low_degree_character_labels_seen
```

This is a real stable signal, but not a new asymptotic primitive.  The labels
`chi(A-2)` and `chi(A+2)` are exactly the first inverse-halving gates from the
terminal points `x=-1` and `x=+1`, since halving those points requires square
roots of `A-2` and `A+2`.  They choose a terminal branch and give a useful
constant-factor enrichment; iterating the idea is the inverse-doubling/X1 tower
already audited above, with the same growing orientation/fiber barrier.

To check whether several cheap character gates could nevertheless stack into a
larger selector, I added a train/holdout greedy stack audit:

```text
p24/character_gate_stack_scan.py
```

It trains on the first half of small near-square fields and evaluates the same
selected gates on held-out fields.  With constant coefficients, bound `2`:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/character_gate_stack_scan.py --min-p 10000 --max-p 220000 \
  --max-rows 16 --coeff-bound 2 --constant-coeffs --max-gates 6

base_holdout hits=11648/742760 precision=0.015682 lift=1.000

step=1 selected sign=+1 feature=A+2
  holdout hits=8906/371376 precision=0.023981 lift=1.529 capture=0.765 coverage=0.500

step=2 selected sign=-1 feature=A-2
  holdout hits=6164/185688 precision=0.033195 lift=2.117 capture=0.529 coverage=0.250

steps=3..6 select square/trivial refinements
  holdout lift stays about 2.116 to 2.117
```

Allowing the coefficients to depend linearly on `n` does not change the
holdout story:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/character_gate_stack_scan.py --min-p 10000 --max-p 220000 \
  --max-rows 16 --coeff-bound 2 --max-gates 6

step=1 selected a scalar multiple of A+2
  holdout lift=1.529
step=2 selected a scalar multiple of A-2
  holdout lift=2.117
steps=3..6 select square/trivial refinements
  holdout lift stays about 2.116 to 2.117
```

Thus cheap low-degree character gates can recover the known terminal-branch
and nonsplit-style constants, but they do not keep adding independent 2-adic
information on held-out fields.  This supports the earlier inverse-tree
conclusion: shallow inverse mass is a constant-factor ranking signal, while
growing depth is the same hard trace/orientation condition.

I then checked a still broader cheap-selector shape: additive structure in the
set of good Montgomery parameters itself.  If the strict bucket had a stable
low-frequency Fourier bias, or lived preferentially in simple residue classes
`A == r mod m`, that might point to a constructive p-specific selector outside
the character gates above.  I wrote:

```text
p24/additive_spectrum_trace_bucket.py
```

For each small prime `p = n^2 + 7`, the script computes the exact
split-corrected strict x-only bucket and forms the centered indicator
`1_good(A) - density` on nonsingular `A`.  It then measures the additive FFT
spectrum and aggregates small residue classes.

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/additive_spectrum_trace_bucket.py --min-p 10000 --max-p 180000 \
  --max-rows 12 --top 8

spectrum_summary
  max/sqrt(good): min=3.739 median=4.044 max=4.625
  low_energy_frac(|h|<=32): median=0.001706 max=0.006924
  low_energy_frac(|h|<=128): median=0.006968 max=0.021066

aggregate_residue_summary
  good=12444/513788 base_rate=0.024220
  m= 3 r= 2 lift=1.014 capture=0.338 coverage=0.333 hits=4206/171248
  m= 3 r= 0 lift=0.993 capture=0.331 coverage=0.333 hits=4121/171268
  m= 3 r= 1 lift=0.992 capture=0.331 coverage=0.333 hits=4117/171272
  m= 4 r= 3 lift=1.002 capture=0.250 coverage=0.250 hits=3117/128444

conclusion=no_stable_low_frequency_or_small_residue_selector_visible
```

The strongest Fourier coefficients occur at unrelated frequencies from row to
row and have random-extreme size, about four times `sqrt(good)`.  The
low-frequency energy is close to the fraction of frequencies inspected, and
the aggregate residue lifts collapse to essentially `1`.  This closes another
natural version of the "cheap trace-v2 label" hope: no additive low-complexity
selector is visible in exact small-field data.

I also audited the related mixed-torsion construction idea: force a divisor
`M` of the group order that is already larger than `sqrt(p)` or the Hasse
width, then recover the target trace.  The script
`p24/mixed_torsion_divisor_audit.py` shows that this does not give a cheaper
p24 route:

```text
python3 p24/mixed_torsion_divisor_audit.py

trace=1020608380936
  min_divisor_gt_sqrt = 2^7 * 71 * 110429177
  best_gt_sqrt_by_largest_prime = 2^40

trace=-78903246840
  min_divisor_gt_sqrt = 2^3 * 3 * 43309271513
  best_gt_sqrt_by_largest_prime = 2^40

trace=-1178414874616
  min_divisor_gt_sqrt = 2^40
  best_gt_sqrt_by_largest_prime = 2^40
```

So the odd factors can isolate traces only by introducing very large odd
levels.  By the same modular-curve cost logic, this moves the hard part rather
than producing an asymptotic speedup.

## X0(2^a) Orientation Gap

`X0(2^a)` is tempting because its level/index growth is linear rather than
quadratic.  But for the p24 residue class it does not impose the DANGER
condition; it only says Frobenius has some odd eigenvalue `lambda` modulo
`2^a`, giving traces

```text
t == lambda + p/lambda mod 2^a.
```

The audit:

```text
python3 p24/x0_orientation_audit.py
```

shows that for `p == 7 mod 16`, the `X0(2^a)` trace-residue image has size
`2^(a-3)`, a constant `1/8` fraction of all residues, while the DANGER residue
`p+1 mod 2^a` has only four odd-eigenvalue preimages.  At `a=40`:

```text
X0 trace residues = 137438953472 / 1099511627776 = 0.125
target orientations = 4
```

So `X0(2^a)` by itself cannot give the growing density gain.  The missing
primitive is exactly the orientation/eigenvalue selection that upgrades
`X0(2^a)` to rational `2^a` torsion, and the generic orientation cover has the
same growing-level barrier as `X1(2^a)`.

I also computed the exact p24 eigenvalue preimages:

```text
p24/x0_eigenvalue_orientation_audit.py
```

For the curve-side DANGER residue `t == p+1 mod 2^a`, the X0 equation factors:

```text
lambda + p/lambda == p+1 mod 2^a
(lambda - 1)*(lambda - p) == 0 mod 2^a.
```

Since `v2(p-1)=1`, there are four roots.  At level `a=40`:

```text
python3 p24/x0_eigenvalue_orientation_audit.py

lambda=1              mu=1020608380935  v2(lambda-1)=40 v2(mu-1)=1  x1_orientation=True
lambda=470852567047   mu=549755813889   v2(lambda-1)=1  v2(mu-1)=39 x1_orientation=False
lambda=549755813889   mu=470852567047   v2(lambda-1)=39 v2(mu-1)=1  x1_orientation=False
lambda=1020608380935  mu=1              v2(lambda-1)=1  v2(mu-1)=40 x1_orientation=True
```

So two of the four X0 orientations are genuine X1 orientations at level
`2^40`; the other two split the vanishing as `39+1`, giving at most a
`2^39` fixed direction at this level.  This is exactly the missing orientation
cover in concrete p24 arithmetic, not a hidden low-height exception.

I then checked the natural level-shift loophole: use `X0(2^(k+1))`, where a
generator `P` of an invariant cyclic subgroup can have Frobenius eigenvalue
`lambda == 1 mod 2^k` without being `1 mod 2^(k+1)`.  Then `2P` is rational
of order `2^k`.  This is a real equivalence, so I wrote:

```text
p24/x0_level_shift_audit.py
```

At p24:

```text
python3 p24/x0_level_shift_audit.py

level_a=40
  gamma0_index=1649267441664
  gamma0_index_over_sqrt_p=1.649267
  hasse_representatives=[-1178414874616, -78903246840, 1020608380936]

level_a=41
  gamma0_index=3298534883328
  gamma0_index_over_sqrt_p=3.298535
  hasse_representatives=[-1178414874616, 1020608380936]
  all four eigen-roots have rational_order_2^k_after_doubling=True
```

So `X0(2^41)` can encode a rational order-`2^40` point after doubling, but it
does not beat sqrt scaling as a sampler: the modular-curve index is already
`3.3*sqrt(p)` for p24 and is `Theta(2^k)` asymptotically.  The level shift
repackages the orientation problem into a growing X0 level; it does not supply
an `N^alpha` construction with `alpha < 1`.

I also tested the same idea in 2-isogeny-chain language, since a tempting
compression is:

```text
construct a rational cyclic 2^d-isogeny chain, then recover a 2^d point later
```

This gives an `X0(2^d)` object, while the verifier needs an oriented
`X1(2^d)`/x-only witness.  I wrote:

```text
p24/isogeny_chain_compression_audit.py
```

It exactly enumerates small `p == 7 mod 16` fields and compares:

```text
X0_d: E or its twist has a rational cyclic subgroup of order 2^d
X1_d: E or its twist has an x-coordinate of exact order 2^d
```

For the decimal-family calibration prime `p=10007`:

```text
python3 p24/isogeny_chain_compression_audit.py --p 10007 --max-depth 10

p=10007
k=7
nonsingular_A=10005
depth X0_chain_A X1_xonly_A X0_not_X1 X1_not_X0 x0_over_x1
 1      10005      10005         0         0 1.000000
 2      10005      10005         0         0 1.000000
 3       7503       5001      2502         0 1.500300
 4       7503       3750      3753         0 2.000800
 5       7503       2606      4897         0 2.879125
 6       7503       1386      6117         0 5.413420
 7       7503        738      6765         0 10.166667
 8       7503        192      7311         0 39.078125
```

So the isogeny-chain condition is much weaker than the verifier condition:
many curves have the rational cyclic chain, but most of those chains do not
select a rational generator/x-coordinate of the required order.  Recovering
that generator is exactly the missing orientation cover, not a free
post-processing step.

I recorded this as a standalone proof note:

```text
p24/x0_orientation_barrier.md
```

For `p == 7 mod 16`, the odd-eigenvalue trace image has size `2^(a-3)` and
the DANGER target residue has four eigenvalue preimages.  Therefore
`X0(2^a)` changes the exact target-residue probability from `1/2^a` to
`1/2^(a-3)`, an 8x constant factor, not a growing asymptotic gain.

To test the more refined AGM/Landen hope, I conditioned on the `X0` event and
asked whether cheap characters can choose the missing `X1` orientation.  I
wrote:

```text
p24/x0_orientation_character_scan.py
```

It computes exact traces for small `p = n^2 + 7`, marks the `X0(2^d)` chain
condition and the strict split-corrected `X1` x-only condition, then scans
low-degree labels `chi(q(A,n))` only inside the `X0` bucket.  At depth `8`,
constant-coefficient bound `2` gives:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x0_orientation_character_scan.py --min-p 10000 --max-p 120000 \
  --max-rows 8 --depth 8 --coeff-bound 2 --constant-coeffs --top 6

aggregate x1_inside_x0=8424/183960 base_rate=0.045793
aggregate_top_features
  sign=-1 lift=1.108 capture=0.738 coverage=0.667 hits=6220/122640 feature=A-2
  sign=+1 lift=1.108 capture=0.738 coverage=0.667 hits=6220/122640 feature=A+2
best_aggregate_lift=1.107550
conclusion=no_growing_low_degree_character_orientation_selector
```

Allowing the coefficients to depend linearly on `n` only returns scalar copies
of the same `A±2` labels, with the same best aggregate lift `1.107550`.  Thus
even after constructing the `X0` chain, the visible low-degree orientation
selector is only the terminal-branch constant; it does not turn `X0` into a
cheap oriented `X1` sampler.

## Half-Depth Division Polynomial Probe

I tested a possible baby-step idea: fix an affine midpoint `x`, build the
Montgomery `Z_m(A)` polynomial in the curve parameter `A`, and use its roots as
curves where this fixed `x` has 2-power depth `m`.  If one fixed `x` yielded
about `2^m` roots in `F_p`, then `m=20` would batch a p24 half-depth search.

The modular-curve point count predicts the opposite: for fixed `x`, there
should be only `O(1)` field roots; the degree growth is mostly over extension
fields.  The FLINT-backed probe confirms this for p24:

```text
python3 p24/half_depth_division_probe.py --x 3 --max-depth 10

depth degree usable_roots
1        1     1
2        3     1
3       15     2
4       63     2
5      255     3
6     1023     3
7     4095     5
```

So the naive `p^(1/4)` half-depth polynomial batch does not materialize: a
fixed coordinate gives only a few p24 curves, while enumerating enough fixed
coordinates reintroduces the lost entropy.

## Fixed-A Inverse-Mass Ranking

The external short-certificate repo has a useful fixed-`A` inverse tree:

```text
f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1))
```

and one inverse step reduces to two square-root tests in `y=x+1/x`.  This can
enumerate valid `x0` once `A` is chosen, and a shallow inverse-tree size gives
a ranking signal for bounded `A` regions.

I wrote a small full-field calibration:

```text
p24/inverse_mass_correlation_probe.py
```

For the small decimal-family prime `p=10007`:

```text
python3 p24/inverse_mass_correlation_probe.py --p 10007

k=7
rank_depth=3
full_depth=6
nonsingular_A=10005
full_hits=738
base_hit_rate=0.07376312
mass_hist=0:6255,8:3750
prefix=0.01 rate=0.26000000 lift=3.525 capture=0.035
prefix=0.10 rate=0.18900000 lift=2.562 capture=0.256
prefix=0.25 rate=0.29508197 lift=4.000 capture=1.000
```

This confirms that inverse mass is a real bounded-region ranking signal, but
not the missing exponent.  The mass bucket is essentially a partial-depth
2-adic filter: to exploit depth `h`, one still has to pay the entropy of
finding/ranking that depth-`h` bucket, and the remaining lift to depth `k`
behaves like the remaining 2-adic trace condition.  It is useful for short
post-hit/minimization searches, not for selecting the p24 target `A` at
sub-sqrt scale.

I then made the meet-in-the-middle scaling question p24-specific.  The
tempting story is that one might rank by a half-depth inverse tree and get a
`2^(k/2)` rather than `2^k` search.  I wrote:

```text
p24/inverse_mitm_scaling_audit.py
```

For each small near-square prime it computes, for every nonsingular `A`, the
inverse-tree mass at rank depth and whether a full strict hit exists.  With
half-depth ranking:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/inverse_mitm_scaling_audit.py --min-p 2000 --max-p 25000 --max-rows 4

row n=120 p=14407 k=8 rank_depth=3 full_depth=7
  full_hits=496/14405 base=0.034432
  rank_states_over_p=10.997 full_states_over_p=22.824
  max_rank_mass=8 A_at_max_mass=5400 full_hits_at_max_mass=496
  prefix=0.010 lift=4.235 capture=0.042
  prefix=0.250 lift=2.686 capture=0.671

row n=136 p=18503 k=8 rank_depth=3 full_depth=7
  full_hits=528/18501 base=0.028539
  rank_states_over_p=10.997 full_states_over_p=21.687
  max_rank_mass=8 A_at_max_mass=6936 full_hits_at_max_mass=528
  prefix=0.010 lift=2.652 capture=0.027
  prefix=0.250 lift=2.621 capture=0.655
```

Going one level deeper increases the lift but still only as a constant-depth
filter:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/inverse_mitm_scaling_audit.py --min-p 10000 --max-p 25000 \
  --max-rows 3 --rank-depth 4

row n=120 p=14407
  max_rank_mass=16 A_at_max_mass=1732 full_hits_at_max_mass=288
  prefix=0.100 lift=4.780 capture=0.478
  prefix=0.250 lift=4.000 capture=1.000

row n=136 p=18503
  max_rank_mass=16 A_at_max_mass=2068 full_hits_at_max_mass=260
  prefix=0.100 lift=4.375 capture=0.438
  prefix=0.250 lift=4.000 capture=1.000
```

So inverse MITM does not magically choose `A`: it ranks by the same partial
2-adic depth.  To make p24 sub-sqrt one would still need a cheap way to
construct the depth-20 `A` bucket; that is precisely the growing
prescribed-torsion/X1 condition already identified as the hard part.  The
inverse tree is valuable for recovering or shortening `x0` after `A` is
chosen, but it is not an exponent-changing selector for `A`.

I also made a global exact small-field version of this test:

```text
p24/inverse_tree_global_count.py
```

It enumerates every nonsingular `A` in a small field, builds exact inverse-tree
layers back from `Z=0`, and compares `A` values with exact-depth hits against
the same curve/twist trace-v2 eligibility.

For `p=3037`:

```text
python3 p24/inverse_tree_global_count.py --p 3037

inverse-tree global exact count
p=3037
k=7
max_depth=7
nonsingular_A=3035
relevant_v2_hist=3:1131,4:776,5:588,6:288,7:108,10:144

depth A_with_hits eligible_A_relevant_v2_ge_depth exact_x_states avg_states_per_A_with_hit mass_hist
 1     3035                               3035           6069                 1.999671 1:1518,3:1517
 2     3035                               3035           9102                 2.999012 2:2277,6:758
 3     2464                               3035           9076                 3.683442 0:571,2:1518,4:382,8:564
 4     1222                               1904           8880                 7.266776 0:1813,4:764,8:188,16:270
 5      592                               1128           8480                14.324324 0:2443,8:376,16:90,32:126
 6      294                                540           8832                30.040816 0:2741,16:180,32:42,64:72
 7      180                                252          13440                74.666667 0:2855,32:84,64:24,128:72
conclusion=inverse_tree_mass_is_the_same_2adic_trace_condition_not_a_free_batch
```

The exact inverse tree never creates new eligible `A` values outside the
2-adic trace bucket; it only reveals many `x0` values once `A` is already in
or near that bucket.  Thus backward enumeration is useful after the curve is
selected, but it does not remove the sqrt-scale problem of finding the target
trace class.

## Pocklington Certificate Path

There is a separate, much faster primality-certificate route for this specific
prime that does not use the DANGER3 Montgomery triple format:

```text
p - 1 = 2 * 7 * 29 * 2463054187192118226601
sqrt_floor(p) = 1000000000000
2463054187192118226601 > sqrt(p)
```

So a Pocklington certificate for the large factor certifies `p` with polylog
verification work once the recursive `n-1` factorizations are known.  I wrote:

```text
p24/pocklington_p24.py
p24/pocklington_p24_certificate.json
```

and verified the JSON certificate from disk:

```text
python3 p24/pocklington_p24.py
wrote p24/pocklington_p24_certificate.json
p=1000000000000000000000007
sqrt_floor=1000000000000
largest_factor_p_minus_1=2463054187192118226601
largest_factor_gt_sqrt=True
verification=PASS
```

Certificate chain summary:

```text
1000000000000000000000007 - 1
  = 2 * 7 * 29 * 2463054187192118226601

2463054187192118226601 - 1
  = 2^3 * 3 * 5^2 * 1543 * 1543067 * 1724137931

1724137931 - 1
  = 2 * 5 * 139 * 1240387

1240387 - 1
  = 2 * 3 * 7^2 * 4219

1543067 - 1
  = 2 * 7 * 19 * 5801
```

This is the clean asymptotic speedup if the requested object is a primality
certificate for this `p`.  It does **not** solve the stricter DANGER3 task of
finding a Montgomery `2^40` x-only Pomerance triple; that route remains open
after the audits above.

## Decimal-Family Probe

I compiled a local probe binary in `p24/pomerance_probe` from the existing C
search code and tested smaller primes in the same decimal family:

```text
p = 17          -> 17 3 5
p = 107         -> 107 19 67
p = 10007       -> 10007 6033 3037
p = 100000007   -> 100000007 22662438 55314890
p = 1000000007  -> 1000000007 605388542 486089049
```

All verify, but these look like ordinary random search hits rather than a
coherent formula in `10^n+7`.  In particular, this did not reveal a reusable
construction for the p24 target.

## Kummer Semiconjugacy Probe

In the quotient coordinate `s = x + 1/x`, Montgomery doubling is the rational
map

```text
y = (s^2 - 4) / (4 * (s + A))
R_A(s) = y + 1/y
```

A semiconjugacy `R_A(S(z)) = S(z^2)` would be a major shortcut: the depth-40
preimage condition would reduce to a multiplicative-order/root-extraction
condition in `z`, rather than a direct inverse walk.  I wrote:

```text
p24/kummer_semiconjugacy_probe.py
```

The symbolic affine-in-`z+z^-1` family

```text
S(z) = m * (z + z^-1) + n
```

has only constant solutions:

```text
symbolic_affine_u_semiconjugacy
nonconstant_solution_count=0
```

I also exhaustively checked small fields for the LFT family

```text
S(u) = (a*u + b) / (c*u + 1),  u = z + z^-1
```

excluding singular `A^2 = 4` and constant maps.  The result was:

```text
p= 5 nonconstant_nonsingular_lft_solutions=0
p= 7 nonconstant_nonsingular_lft_solutions=0
p=11 nonconstant_nonsingular_lft_solutions=0
p=13 nonconstant_nonsingular_lft_solutions=0
p=17 nonconstant_nonsingular_lft_solutions=0
p=19 nonconstant_nonsingular_lft_solutions=0
p=23 nonconstant_nonsingular_lft_solutions=0
p=29 nonconstant_nonsingular_lft_solutions=0
p=31 nonconstant_nonsingular_lft_solutions=0
```

This is evidence rather than a theorem for all rational maps, but it closes the
most natural degree-1 quotient semiconjugacy route.

I then broadened this to all rational maps of degree at most 2 in
`u=z+z^-1`, over several small fields.  The projective identity checked is:

```text
R_A(S(u)) = S(u^2 - 2)
```

with

```text
S(u) = (n0 + n1*u + n2*u^2)/(d0 + d1*u + d2*u^2).
```

The script is:

```text
p24/kummer_degree2_semiconjugacy_probe.py
```

and the exhaustive small-field result was:

```text
python3 p24/kummer_degree2_semiconjugacy_probe.py

p= 5 maps_checked=3720   nonconstant_nonsingular_degree_le_2_solutions=0
p= 7 maps_checked=19152  nonconstant_nonsingular_degree_le_2_solutions=0
p=11 maps_checked=175560 nonconstant_nonsingular_degree_le_2_solutions=0
p=13 maps_checked=399672 nonconstant_nonsingular_degree_le_2_solutions=0
```

This is still finite-field evidence rather than a classification theorem, but
it rules out the low-degree rational power-map shortcut far beyond the initial
LFT probe.

There is also a conceptual dynamical obstruction, recorded in:

```text
p24/semiconjugacy_obstruction.md
```

The source map `u -> u^2 - 2` is the Chebyshev/power quotient with parabolic
orbifold type `(2,2,infinity)`, while nonsingular Montgomery Kummer doubling is
an elliptic Lattes quotient of multiplication-by-2, with type `(2,2,2,2)`.
A nonconstant rational semiconjugacy between these postcritically finite
parabolic maps would have to respect the orbifold structure.  Thus a true
power-map shortcut is available only in the singular torus limits `A = +/-2`,
which the verifier rejects.

For p24 the singular torus escape hatch is even worse than just verifier
rejection.  I wrote:

```text
p24/torus_degeneration_audit.py
```

and it records the available 2-power in the split and nonsplit tori:

```text
python3 p24/torus_degeneration_audit.py

v2(p-1)=1
v2(p+1)=3
v2(p^2-1)=4
max_split_torus_2power=2^1
max_nonsplit_torus_2power=2^3
verifier_rejects_A_equals_plus_minus_2=True
```

So even if the singular `A=+/-2` limits were allowed, the multiplicative and
norm-one tori have only `2^1` and `2^3` depth.  The desired `2^40` power-map
shortcut is absent arithmetically as well as formally rejected by DANGER3.

## Original Pomerance Type-2 Audit

Pomerance's paper also permits a type-2 certificate: two independent points on
the same curve, of orders `2^k1` and `2^k2`, with product large enough to
exceed the Hasse bound for any prime divisor of `n`.  This is broader than the
DANGER3 single-point verifier, so I checked whether it could give the missing
exponent for `p24`.

I wrote:

```text
p24/pomerance_type2_audit.py
```

For two independent rational `2^m` directions over `F_p`, the Weil pairing
requires `2^m | p-1`.  Here

```text
p = 1000000000000000000000007
v2(p-1) = 1
danger_bound = 1000002000001
danger_single_point_k = 40
```

Thus the second independent 2-power can have order at most `2`, and the large
point in a type-2 certificate must still have exponent at least `39`:

```text
max_independent_second_2power=2^1
min_large_point_exponent_with_type2=39
type2_product_exponent_needed=40
```

Equivalently, type-2 changes only the cyclic-versus-noncyclic 2-Sylow constant
inside the same `v2(#E) >= 40` trace condition.  Since `10^n + 7` has
`v2(p-1)=1` for the whole family, this cannot be the desired asymptotic
speedup.

## Moment Complexity and Actual-p24 Tail Shards

After the additive FFT and residue audit, I made the remaining "hidden simple
`A`-line structure" question more explicit.  I wrote:

```text
p24/moment_complexity_audit.py
```

For small `p = n^2 + 7`, it computes the exact strict split-corrected good-`A`
set, then measures:

```text
low-degree Legendre-polynomial moment z-scores of 1_good(A) - density
power sums sum_good A^j represented as small a + b*n mod p
Hankel ranks of the raw and centered moment sequences over F_p
```

Representative run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/moment_complexity_audit.py --min-p 10000 --max-p 180000 \
  --max-rows 12 --max-moment-degree 24 --max-legendre-degree 24 \
  --hankel-size 10 --top 6

aggregate
  good=12444/513788 density=0.024220
  signed_legendre_z d24=-3.500 d2=+1.876 d16=-1.553 d10=+1.549
  mean_abs_legendre_z d8=1.790 d10=1.367 d16=1.268 d24=1.239
  odd_power_moments_zero_rows=12/12
  even_height_ratio_min_median=0.119
  even_height_ratio_median_median=0.305
  full_raw_hankel_rank_rows=12/12
  full_centered_hankel_rank_rows=12/12
  conclusion=no_stable_low_degree_moment_small_height_or_short_recurrence_signal
```

The odd power moments vanish in every row, which is the expected `A -> -A`
symmetry.  The even moments do not collapse to stable small `a + b*n`
representatives; the rowwise Legendre blips move around; and both raw and
centered Hankel matrices have full rank.  This is not a pseudorandomness
theorem, but it closes the most direct low-moment/short-recurrence version of a
cheap constructive selector.

In parallel, a bounded actual-p24 search audit checked whether any existing
structured shard is worth scaling.  The only reasonable one was an
informational `X1(16)->X1(32)` tail shard:

```text
python3 p24/x16_first_lift_p24_feature_scan.py \
  --p 1000000000000000000000007 \
  --accepted 100000 \
  --target-depth 24 \
  --depths 12 16 20 24 \
  --norm-coeff 0

accepted_curve_rows=100000
hit12=898
hit16=48
hit20=8
hit24=0
accepted_curve_rate=2458/s
```

After the forced first lift, the tail looks random at roughly one bit per
level.  A 100k-row shard has expected strict depth-40 success probability only
`100000 / 2^35 ~= 2.9e-6`; even a 1M-row diagnostic would remain a tail sanity
check, not a certificate hunt.  Low-height `A` frontiers and literal
`(A,x0)` frontiers have still worse hit probabilities once the existing
small-scale no-go audits are taken into account.

## Pair-Level Verifier Relation Audit

I then moved one step closer to the literal verifier equation.  Most cheap
selector audits project the accepted set onto `A`, but a transformed
certificate might conceivably live on a low-degree component in the pair
coordinates `(A, x)`.  I wrote:

```text
p24/pair_relation_rank_audit.py
```

For small `p = n^2 + 7`, it enumerates the exact accepted verifier pairs

```text
Z_k(A, x) = 0
Z_{k-1}(A, x) != 0
A^2 - 4 != 0
```

and checks whether all accepted pairs lie on a nonzero low-degree polynomial in
`A` and `x`.  A full evaluation rank for monomials of degree `<= D` rules out
any field-specific relation of that degree, and therefore any uniform
low-degree relation over `Q(n)` of that degree.

Representative run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/pair_relation_rank_audit.py --min-p 500 --max-p 5000 --max-rows 3 \
  --total-degree 10 --rect-a-degree 5 --rect-x-degree 5

row n p k accepted_pairs total_rank/nullity rect_rank/nullity
01 32 1031 6 2752 66/0 36/0
02 40 1607 6 5184 66/0 36/0
03 48 2311 6 8640 66/0 36/0
aggregate
  full_total_degree_rank_rows=3/3
  full_rectangular_rank_rows=3/3
  conclusion=no_low_degree_pair_component_visible
```

This does not classify all possible parametrizations, but it rules out the
most direct algebraic escape hatch: a hidden small component of the exact
Kummer verifier curve.  This aligns with the resultants/semiconjugacy audits:
over the algebraic closure every nonsingular `A` has deep preimages of
infinity, so a bare resultant tests the wrong object; adding Frobenius
rationality is precisely the growing `X1(2^k)` orientation problem.

I also updated `p24/target_trace_shape_audit.py` to print the elementary
quotient/remainder identity behind the six strict traces:

```text
p+1 = 2^40 * 909494701772 + 1020608380936
1020608380936 = 8 + 2^24 * 60833

curve-side traces:
  r       =  1020608380936    order / 2^40 = 909494701772
  r-2^40  =   -78903246840    order / 2^40 = 909494701773
  r-2*2^40= -1178414874616    order / 2^40 = 909494701774
```

The x-only verifier adds the negatives via the twist.  This identity is useful
bookkeeping, not a construction: it explains why the target traces are simple
as `2^40` Hasse representatives, while the nearby near-square CM traces
`0, +/-n, +/-2n` still have only `v2 = 3`, and the strict traces still carry
the huge fundamental CM fields recorded above.

## Mixed Odd-Level and Ramified-Ideal Rechecks

The target orders have small odd cofactors, so I rechecked the possible detour:
construct a curve from a mixed divisor of the target order, then recover the
strict `2^40` point by projection once the isogeny class is known.  I wrote:

```text
p24/mixed_level_index_audit.py
```

It enumerates divisors of the three curve-side target orders above the
DANGER/Pomerance bound and above the Hasse width, then computes the modular
indices for `Gamma0(N)` and `Gamma1(N)`.  `Gamma0` is the optimistic lower
bar, because it asks only for a rational cyclic subgroup of order `N`.

Representative run:

```text
python3 p24/mixed_level_index_audit.py

global_best
 threshold=danger_bound
  best_gamma0: divisor=1003580360576 factors={2: 7, 71: 1, 110429177: 1}
    gamma0=1526572956672 gamma0/sqrt=1.526573
  best_gamma1: divisor=1039422516312 factors={2: 3, 3: 1, 43309271513: 1}
    gamma1/sqrt=7.202661e+11
 threshold=hasse_width
  best_gamma0: divisor=2007160721152 factors={2: 8, 71: 1, 110429177: 1}
    gamma0=3053145913344 gamma0/sqrt=3.053146
  best_gamma1: divisor=2078845032624 factors={2: 4, 3: 1, 43309271513: 1}
    gamma1/sqrt=2.881064e+12
conclusion=mixed_odd_levels_do_not_give_subsqrt_modular_construction
```

Thus odd cofactors can exchange pure `2^40` for a mixed level, but the
cheapest cyclic-subgroup modular problem is still sqrt-scale or worse.  The
point-level `X1` versions are vastly larger.

I also broadened:

```text
p24/ramified_self_loop_audit.py
```

to print all odd ramified factors, not only the tiny ones.  This makes the
mid-sized factor `4973929` visible:

```text
trace=-78903246840
  factor(abs_delta)={2: 2, 7: 1, 211: 1, 4973929: 1, 135907507341779: 1}
  min_non_scalar_principal_norm=ceil(abs_delta/4)=998443569409526507503607
  ell=4973929 ramified=yes ell_over_sqrt_p=4.973929e-06
    has_norm_ell_element=False
conclusion=ramified_primes_give_only_nonprincipal_genus_information_not_self_loops
```

The reason is elementary: a degree-`ell` self-loop would require
`x^2 + |Delta| y^2 = 4 ell`.  For every ramified factor here,
`4 ell < |Delta|`, so no non-scalar element of norm `ell` exists; the ramified
ideals are nonprincipal and supply only the genus-class information already
counted as a constant-bit saving.

## Exceptional Automorphism / Class-Number-One CM Audit

I made the cheap-CM edge cases explicit in:

```text
p24/class_number_one_cm_audit.py
```

This checks the class-number-one Heegner discriminants

```text
-3, -4, -7, -8, -11, -19, -43, -67, -163
```

using Cornacchia reduction for the norm equation
`4p = t^2 + |D| f^2`, then compares the resulting traces with the six strict
DANGER traces.  This is the only CM family where constructing a curve is cheap
enough to matter asymptotically.

Representative run:

```text
python3 p24/class_number_one_cm_audit.py

D=-7
  trace=-2000000000000 conductor_factor=2 trace_mod_2^40=199023255552
    v2_order=3 v2_twist=3 strict_target_hit=False
  trace=2000000000000 conductor_factor=2 trace_mod_2^40=900488372224
    v2_order=3 v2_twist=3 strict_target_hit=False
D=-67
  trace=+-510254110615 ... v2_order=0 v2_twist=0 strict_target_hit=False
D=-163
  trace=+-1697841765049 ... v2_order=0 v2_twist=0 strict_target_hit=False
conclusion=class_number_one_CM_has_no_strict_DANGER_trace
```

The exceptional automorphism cases `j=0` and `j=1728` give no ordinary
strict-depth trace here (`p % 3 = 2` and `p % 4 = 3`, with only the
supersingular trace-zero behavior and `v2(p+1)=3`).  The near-square `D=-7`
case is exactly the broad ECPP certificate already found, but twists and
Montgomery transformations preserve the trace up to sign and cannot turn
`v2=3` into the required `2^40` x-only order.

An independent reverse-SEA audit reached the same constructive barrier from
the other side: exact odd trace residues can isolate the six target traces as
a free oracle, but constructing curves from those residues is a growing
modular-level problem.  Small Atkin/Elkies statuses remain constant filters;
marked odd torsion hits the same `Gamma1`/gonality barrier, and even optimistic
`Gamma0` mixed levels stay at or above sqrt scale as recorded above.

## Literal Verifier Equivalence Audit

I also checked whether the literal DANGER3 x-only verifier might be weaker than
the exact-order condition used throughout the frontier.  I wrote:

```text
p24/verifier_equivalence_audit.py
```

For small `p = n^2 + 7` rows it enumerates every nonsingular Montgomery `A`
and every affine `x`, runs the same k-step x-only doubling condition as
`vpp.py`, then compares the accepted x-count with the trace/group-structure
prediction:

```text
curve side exact order 2^k x-count
plus twist side exact order 2^k x-count
with split Montgomery curves losing one 2-primary exponent
```

Representative exact run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/verifier_equivalence_audit.py --min-p 500 --max-p 2500 --max-rows 3

row n p k total_A accepted_x predicted_x good_A mismatches max_abs_diff
01 32 1031 6 1029 2752 2752 108 0 0
02 40 1607 6 1605 5184 5184 212 0 0
03 48 2311 6 2309 8640 8640 348 0 0
aggregate
  checked_rows=3
  total_accepted_x=16576
  total_predicted_x=16576
  total_mismatching_A=0
  conclusion=literal_verifier_matches_exact_order_curve_or_twist_prediction
```

This supports the reduction used in the rest of the p24 work: there is no
extra x-only loophole hiding between the verifier and the exact `X1`-style
order condition, at least in exact small-field calibration.  The script now
has a `--max-literal-work` guard so wider ranges are skipped rather than
quietly turning into `p^2` computation.

## Reverse-SEA Exact-Residue Level Tradeoff

I tightened the reverse-SEA/no-free-residues statement in:

```text
p24/reverse_sea_level_tradeoff_audit.py
```

The script considers partial 2-adic depths `d`, then asks how much exact odd
trace-residue information is needed to isolate the six signed target traces.
It reports two quantities:

```text
R_lower:
  a lower bound on any odd modulus R that could isolate the target traces,
  using the fact that on a fixed 2-adic branch residues repeat every R indices
gamma0_lower/sqrt:
  the resulting optimistic lower bound for [SL2:Gamma0(2^d R)] / sqrt(p)
```

This bound allows fully correlated exact residues modulo the odd product; it is
stronger than the earlier independent per-prime residue-set filter.

Representative run:

```text
python3 p24/reverse_sea_level_tradeoff_audit.py \
  --depths 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 \
  --max-initial-count 1000000

depth initial_count R_lower gamma0_lower/sqrt ... gamma0/sqrt
23        953674  378897          4.767628 ... 405.270430
28         29802   11841          4.767816 ...  74.088186
34           466     186          4.793184 ...  11.957189
36           116      47          4.844723 ...   7.421703
39            14       6          4.947802 ...   9.895605
40             6       1          1.649267 ...   1.649267
conclusion=reverse_sea_exact_residue_construction_is_not_subsqrt_under_optimistic_level_proxy
```

For every partial depth `d < 40`, even the lower bound is already at least
`4.76 * sqrt(p)` under the deliberately generous `Gamma0` proxy.  The cheapest
row is `d=40`, which is just the original strict `2^40` condition with
`Gamma0` index `1.649 * sqrt(p)`.  Thus reverse-SEA trace residue construction
does not supply the missing sub-sqrt primitive, even if exact CRT correlation
between the six targets is allowed.

## X0 Orientation-Cover Degree Tradeoff

I also made the `X0` orientation cost explicit in:

```text
p24/x0_orientation_degree_tradeoff_audit.py
```

The cover from a cyclic `X0(2^d)` subgroup to an x-only oriented generator is
of degree

```text
phi(2^d) / 2 = 2^(d-2).
```

Thus the orientation information grows at exactly the level that `X0` was
trying to avoid.  Representative output:

```text
python3 p24/x0_orientation_degree_tradeoff_audit.py

depth free_x0_cover_residual/sqrt oriented_index/sqrt oriented_index_times_residual/sqrt
 4                     0.274878         9.600000e-11                        6.597070e+00
20                     0.274878         4.123169e-01                        4.323456e+05
28                     0.274878         2.702160e+04                        1.106805e+08
40                     0.274878         4.533472e+11                        4.533472e+11
conclusion=X0_orientation_cover_cost_grows_like_the_missing_X1_level
```

The `free_x0` column is a deliberately unrealistic lower proxy that ignores
the cost of constructing `X0` structure; it only gives a constant-factor story,
not an asymptotic one.  Once the `Gamma0(2^d)` modular construction cost is
included, the oriented-level proxy is already worse than sqrt at small fixed
depths and grows rapidly.  This is the degree-theoretic version of the earlier
character scans: `X0` can reduce trace residues, but the missing orientation is
the hard `X1` cover.

## Post-Trace Construction Audit

I separated the strict problem into two steps:

```text
1. construct a nonsingular Montgomery A in one of the signed target trace classes;
2. after such an A is known, produce an x-coordinate accepted by the verifier.
```

The second step is cheap in the group-theoretic sense.  Once a known curve or
twist has 2-primary exponent at least `k`, multiplying a random group point by
the odd part and the appropriate remaining 2-power gives an exact x-only
`2^k` coordinate with constant expected trials.  The dangerous step is still
constructing the `A` in the target trace class.

I wrote:

```text
p24/post_trace_construction_audit.py
```

It computes all Montgomery traces by convolution for small exact rows
`p = n^2 + 7`, conditions on the signed target traces
`p + 1 - s == 0 mod 2^k`, and counts:

```text
target_trace_A:
  nonsingular Montgomery parameters whose curve or twist trace is target
strict_good_A:
  those target-trace A values that survive the split/nonsplit x-only exponent rule
accepted_x_total:
  predicted verifier-accepted x-coordinates from the exact 2-primary structure
```

A small detailed run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/post_trace_construction_audit.py --min-p 10000 --max-p 180000 --max-rows 10 --details

aggregate
  checked_rows=10
  target_trace_A=15258
  strict_good_A=10482
  lost_to_split=4776
  accepted_x_total=1211136
  target_A_over_sum_sqrt=8.220026
  strict_A_over_sum_sqrt=5.647025
  avg_x_per_strict_A=115.544362
  projected_group_point_expected_trials_per_known_good_side<=2
  conclusion=post_trace_x0_is_constant_expected_after_A_is_known; target_trace_A_construction_remains_sqrt_scale_in_this_calibration
```

A wider exact trace-convolution run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/post_trace_construction_audit.py --min-p 100000 --max-p 1000000 --max-rows 20

aggregate
  checked_rows=20
  target_trace_A=80628
  strict_good_A=57240
  lost_to_split=23388
  accepted_x_total=19300096
  target_A_over_sum_sqrt=7.764530
  strict_A_over_sum_sqrt=5.512250
  avg_x_per_strict_A=337.178477
  projected_group_point_expected_trials_per_known_good_side<=2
  conclusion=post_trace_x0_is_constant_expected_after_A_is_known; target_trace_A_construction_remains_sqrt_scale_in_this_calibration
```

This closes a possible misunderstanding in the other direction: random affine
`x` values are sparse, but after a target-trace curve is known the certificate
coordinate is not the bottleneck.  The bottleneck is the trace-class selector.

I also checked the natural CM one-root loophole against the local references.
For a fixed ordinary trace, Deuring/CM says the `j`-invariants are roots of the
ring class polynomial of discriminant `t^2 - 4p`; the Montgomery map

```text
j(A) = 256 * (A^2 - 3)^3 / (A^2 - 4)
```

is bounded degree, so asking for Montgomery `A` instead of `j` does not change
the asymptotics.  The local prescribed-subgroup paper records that finding one
root of an already available split polynomial of degree `d` costs
`~O_p(d + p^(1/2))`, and constructing the Hilbert class polynomial costs
`~O_p(|D|)` in the relevant deterministic CM method.  For the p24 target traces
the discriminants have `|D| ~= p`, class-size estimates remain
`2.06e11` to `8.33e11`, genus characters save only 1 to 3 bits, and the
2-volcano conductor depth is only 1.  So there is no free "one root" shortcut
visible here.

## Low-Height LFT Bound-12 Extension

I reran the original near-square LFT probe at a higher coefficient bound:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 1000 --max-p 250000 \
  --max-rows 30 --coeff-bound 12

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 1000 --max-p 250000 \
  --max-rows 30 --coeff-bound 12 --square-parameter

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 1000 --max-p 250000 \
  --max-rows 30 --coeff-bound 12 --j-parameter
```

All three variants return:

```text
perfect_survivors=0
conclusion=no_low_height_LFT_formula
```

The direct `A(n)` survivors vanish by row 7, the `A^2(n)` survivors by row 5,
and the `j(n)` survivors by row 4.  This is only a bounded search, but it
pushes the simple near-square rational-section hypothesis a little farther out.

## Multiplicative Spectrum and Coset Audit

I checked a different possible selector shape: maybe the strict target bucket
is not additive/low-degree in `A`, but is biased toward a low-index
multiplicative coset in either the Montgomery parameter `A` or the Montgomery
`j`-invariant.  That would be constructive in a way the previous additive
spectrum and Legendre-polynomial probes would not necessarily see.

I wrote:

```text
p24/multiplicative_spectrum_trace_bucket.py
```

For each small exact row it:

```text
1. computes the exact strict x-only good-A bucket;
2. builds a primitive-root discrete-log table for F_p^*;
3. takes a multiplicative FFT of the good bucket in A and j;
4. measures the best low-order multiplicative coset lifts.
```

Small run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/multiplicative_spectrum_trace_bucket.py --min-p 10000 --max-p 180000 \
  --max-rows 10 --max-character-order 32 --top-spectrum 4 --top-cosets 10

aggregate
  A max/sqrt_hits min=3.739 median=4.356 max=4.801
  j max/sqrt_hits min=4.888 median=5.688 max=17.961
  best_low_order_coset_lifts
    j order=21 rows=2 median_lift=2.795 mean_lift=2.795 median_capture=0.131
    j order=22 rows=2 median_lift=1.823 mean_lift=1.823 median_capture=0.083
    ...
  conclusion=no_stable_low_order_multiplicative_coset_selector_visible
```

The big `j` spike in the first small row did not persist.  A wider exact
calibration:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/multiplicative_spectrum_trace_bucket.py --min-p 100000 --max-p 1000000 \
  --max-rows 20 --max-character-order 32 --top-spectrum 3 --top-cosets 8

aggregate
  A max/sqrt_hits min=4.509 median=4.928 max=6.177
  j max/sqrt_hits min=5.401 median=6.107 max=7.210
  best_low_order_coset_lifts
    j order=25 rows=3 median_lift=1.467 mean_lift=1.433 median_capture=0.058
    j order=31 rows=3 median_lift=1.365 mean_lift=1.373 median_capture=0.043
    A order=25 rows=3 median_lift=1.353 mean_lift=1.300 median_capture=0.054
    A order=31 rows=3 median_lift=1.353 mean_lift=1.355 median_capture=0.044
    j order=29 rows=2 median_lift=1.350 mean_lift=1.350 median_capture=0.046
    j order=22 rows=6 median_lift=1.300 mean_lift=1.333 median_capture=0.059
    A order=29 rows=2 median_lift=1.288 mean_lift=1.288 median_capture=0.044
    j order=14 rows=5 median_lift=1.263 mean_lift=1.265 median_capture=0.091
  conclusion=no_stable_low_order_multiplicative_coset_selector_visible
```

The largest multiplicative Fourier coefficients are random-sized
`O(sqrt(#good) * sqrt(log p))`-looking maxima, not stable small-order
characters.  Low-order cosets sometimes give a 1.2-1.4x lift, but only when
that order happens to divide `p-1`, with tiny capture and no stable bucket.
So multiplicative cosets join the additive spectrum and low-degree character
gates as constant-factor ranking signals, not an asymptotic trace-class
construction.

## Consecutive Cofactor Pattern Check

The three curve-side target orders have the visually tempting form:

```text
p + 1 = 2^40 * 909494701772 + 1020608380936
orders = 2^40 * q, 2^40 * (q + 1), 2^40 * (q + 2)
q = 909494701772
```

This is just the list of Hasse representatives of the single congruence
`t == p + 1 mod 2^40`, not an independent construction.  The odd cofactor
factorizations can be traded into mixed torsion divisors, but the best
optimistic `Gamma0` mixed divisor above the DANGER bound is still
`1.526573 * sqrt(p)`, and `Gamma1` is much worse.  The known prescribed
subgroup theorem is also far out of range because `2^40` is essentially
`sqrt(p)`, not `o(sqrt(p)/(log p)^4)`.

The large cofactor primes do not create a hidden CM identity either: the target
fields still have conductor `2`, no useful square conductor, and class-size
estimates `2.06e11` to `8.33e11`.  Thus the consecutive cofactors are useful
bookkeeping for the target traces, but not a selector for `A`.

## Fixed-Prime Prescribed-Order Audit

I also made explicit why "construct an elliptic curve of prescribed order" does
not bypass the fixed-p trace problem.  Bröker-Stevenhagen-style prescribed-order
algorithms are powerful when the field prime can be chosen or searched for a
small CM discriminant.  Here both `p` and the strict order are fixed, so the
trace and discriminant are fixed too.

I wrote:

```text
p24/prescribed_order_fixed_p_audit.py
```

Representative run:

```text
python3 p24/prescribed_order_fixed_p_audit.py

strict_target trace=1020608380936
  factor(order)={2: 42, 29: 1, 71: 1, 110429177: 1}
  fundamental_D=-739589633190799177940983
  conductor_in_Zpi=2
  abs_D_over_p=0.739590

strict_target trace=-78903246840
  factor(order)={2: 40, 3: 1, 7: 1, 43309271513: 1}
  fundamental_D=-998443569409526507503607
  conductor_in_Zpi=2
  abs_D_over_p=0.998444

strict_target trace=-1178414874616
  factor(order)={2: 41, 454747350887: 1}
  fundamental_D=-652834595820939249713143
  conductor_in_Zpi=2
  abs_D_over_p=0.652835

near_square_fast_CM_non_strict trace=2000000000000
  factor(order)={2: 3, 7: 1, 250698247: 1, 71229627932369: 1}
  fundamental_D=-7

conclusion=fixed_p_prescribed_order_reduces_to_large_discriminant_CM; variable_field_prescribed_order_algorithms_do_not_select_the_fixed_p24_trace
```

So the exact strict orders are factored and attractive, but over the fixed p24
field they force the same large discriminants as the target traces.  The one
cheap prescribed-order-looking object is the near-square `D=-7` curve, and it
has only `v2(order)=3`.

## Bounded-Degree Explicit-Family Entropy Audit

I then generalized the low-height formula searches into an entropy statement
for any bounded-degree explicit family over the `j`-line.  Suppose a shortcut
gives a parameter `u` and a degree-`d` rational map `j = phi(u)`.  This covers
the Montgomery `A` line, Legendre lambda, Edwards/Tate/Kubert fixed-level
families, and any other fixed-degree algebraic reparametrization of elliptic
curves.  A fixed ordinary target trace gives about `h(D)` target `j`-values, so
pulling the target set back through `phi` gives at most `d*h(D)` parameter
values.  Therefore bounded-degree families can only change constants; an
exponent-changing sampler needs growing degree/level or a new class selector.

I wrote:

```text
p24/low_degree_family_entropy_audit.py
```

Representative run:

```text
python3 p24/low_degree_family_entropy_audit.py

target trace class estimates
  trace=  1020608380936 h_est=2.786879e+11 h/sqrt_p=0.278688
  trace=   -78903246840 h_est=8.329662e+11 h/sqrt_p=0.832966
  trace= -1178414874616 h_est=2.060276e+11 h/sqrt_p=0.206028
  total_signed_j_classes_est=1.317682e+12
  random_j_expected_trials=7.589086e+11

bounded-degree family model
degree expected_trials expected_trials/sqrt_p
       1       7.589086e+11            7.589086e-1
       6       1.264848e+11            1.264848e-1
      16       4.743179e+10            4.743179e-2
   65536       1.158003e+07            1.158003e-5
 1000000       7.589086e+05            7.589086e-7

degree required for target trial exponents
alpha target_trials=p^alpha required_degree
 0.40         3.981072e+09        1.906292e+2
 0.30         1.584893e+07        4.788390e+4
 0.25         1.000000e+06        7.589086e+5

conclusion=bounded_degree_explicit_families_only_change_constants; exponent_saving_requires_growing_degree_or_new_class_selector
```

This closes the broad "maybe another simple one-parameter family has the trace"
route unless it comes with a genuinely new way to select the target CM class.
A degree-6 Montgomery-style pullback can give a nice fixed-p constant, but it
cannot prove asymptotic sub-sqrt scaling.  A p24-scale `p^(1/4)` random
parameter budget would require family degree around `7.6e5`, which is exactly
the growing-level cost that appears in the `X1`/`X0` audits.

## Finite-Field Identity Sidecar

I added a focused sidecar note:

```text
p24/finite_field_identity_sidecar.md
```

The only real theorem-level selector visible from `p = n^2 + 7` is the
`D = -7` CM identity.  It gives Frobenius trace `+/-2n`, so it would be a
strict DANGER selector exactly when

```text
2^k | (n - 1)^2 + 7
```

or

```text
2^k | (n + 1)^2 + 7
```

For p24 both valuations are only `3`, while the verifier needs `k = 40`.
Thus the near-square CM identity is a genuine selector on rare 2-adic branches
of the family, but not on this prime.

I also added:

```text
p24/near_square_target_discriminant_audit.py
```

Representative p24 run:

```text
python3 p24/near_square_target_discriminant_audit.py \
  --min-p 10000 --max-p 100000 --max-rows 8 --include-p24

p24_detail
n=1000000000000 p=1000000000000000000000007 k=40 target_traces=3 min_abs_D_over_p=0.652835 max_conductor=2 max_conductor_over_sqrt_p=2.000000e-12
  t=-1178414874616 fundamental_D=-652834595820939249713143 conductor=2 abs_D_over_p=0.652835
  t=-78903246840 fundamental_D=-998443569409526507503607 conductor=2 abs_D_over_p=0.998444
  t=1020608380936 fundamental_D=-739589633190799177940983 conductor=2 abs_D_over_p=0.739590
 conclusion=p24_strict_target_traces_are_large_discriminant_CM_classes_not_a_small_CM_identity
```

This rules out the small-CM/Jacobi-sum style finite-field identity for the
strict p24 traces: the target orders have conductor `2` and fundamental
discriminant comparable to `p`, so CM construction is again a `sqrt(p)`-class
problem.

## Public Lead Scan

I also ran an independent public/local lead scan and recorded it in:

```text
p24/public_lead_scan_20260604.md
```

It checked the local repo, the sibling short-certificate repo, the official
DANGER3 repository, the public Alexa and Ruehle forks, and web/GitHub hits for
the exact p24 constant.  No strict verifier-compatible p24 certificate or
asymptotic construction was found.  The public material still records p22/p23
successes and leaves `p = 10^24 + 7` as the next challenge target; the useful
public leads are already represented locally as constant-factor or
post-trace/inverse-tree diagnostics.

## Conductor-2 CM Root Sidecar

I also recorded the conductor-2 CM root question in:

```text
p24/conductor2_cm_root_sidecar.md
```

The useful distinction is that the principal representation
`t^2 - 4p = 4D_K` proves the CM roots for the strict traces split over `F_p`,
but it does not pick a root.  The conductor-2 kernel is trivial because
`D_K == 1 mod 8`, genus data saves only `1`, `3`, and `1` bits, and the
residual class counts remain about `1e11` in every target case.  The standard
CM path in `p24/prescribed_subgroup.tex` is still "compute `H_D`, find a root,
choose the twist"; for `|D_K| ~= p` both class-polynomial size and root
selection remain sqrt-scale or worse.

The note gives a falsifiable test for future claims: on small primes
`p = n^2 + 7`, a claimed shortcut should output a `j` or Montgomery `A` for a
conductor-2, large-`D_K` strict trace without trace-bucket enumeration or full
class-polynomial construction, and exact point counting / trace convolution
should show a hit rate bounded away from random.

## Half-Level X0 Lift Sidecar

I recorded the half-level `X0` meet-in-the-middle question in:

```text
p24/half_level_x0_lift_sidecar.md
```

The tempting split is `h ~= 20`, where constructing `X0(2^h)` cyclic subgroup
data has index about `p^(1/4)`.  The obstruction is that `X0(2^h)` knows only a
Frobenius-stable line with eigenvalue `lambda mod 2^h`, while the strict
verifier needs the oriented condition `lambda == 1 mod 2^40` (or the
dual/twist equivalent).  If

```text
lambda = 1 + 2^h u mod 2^40,
```

then the strict point forces:

```text
u == 0 mod 2^(40-h).
```

For `h = 20`, the bookkeeping is:

```text
[SL2:Gamma0(2^20)] = 3*2^19 = 1,572,864 ~= 1.57*p^(1/4)
residual_tail = 2^20 = 1,048,576
product = 3*2^39 ~= 1.649*sqrt(p)
```

So the half-level strategy only moves the missing bits from trace depth to
ray orientation depth.  A real speedup would need a canonical label on
`X0(2^h)` data that predicts the high tail `u` with growing advantage.  The
existing character, ray-orientation, isogeny-chain, and partial-oriented
sampler audits are negative for visible low-degree labels.

## Inverse-Chain MITM Split Tradeoff

I added a direct small-field audit of the baby-step/giant-step version of the
same idea:

```text
p24/inverse_chain_mitm_tradeoff_audit.py
```

For each exact small row it computes all Montgomery traces, marks the strict
full-depth x-only bucket, then conditions on partial oriented depth `h` and on
the weaker `X0(2^h)` trace condition.  The diagnostic is:

```text
stage cost to get partial depth * residual cost to reach full depth.
```

If an inverse-chain MITM changed the exponent, this product should shrink for
some split `h`.  It does not.

Small run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/inverse_chain_mitm_tradeoff_audit.py --min-p 10000 --max-p 120000 \
  --max-rows 6 --depths 2 3 4 5 6 7 8 9 10

aggregate
  h total full x1_partial x1_residual x1_product x0_partial x0_residual x0_product
   2   155358   5718     155358 0.03680531    27.169990     155358 0.03680531    27.169990
   3   155358   5718      77670 0.07361916    27.169990     116514 0.04907565    27.169990
   4   155358   5718      58248 0.09816646    27.169990     116514 0.04907565    27.169990
   5   155358   5718      38608 0.14810402    27.169990     116514 0.04907565    27.169990
   6   155358   5718      19476 0.29359211    27.169990     116514 0.04907565    27.169990
   7   155358   5718      10336 0.55321207    27.169990     116514 0.04907565    27.169990
   8   155358   5718       5718 1.00000000    27.169990     116514 0.04907565    27.169990
```

Larger run, including rows with `k = 10`:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/inverse_chain_mitm_tradeoff_audit.py --min-p 100000 --max-p 1000000 \
  --max-rows 10 --depths 3 4 5 6 7 8 9

aggregate
  h total full x1_partial x1_residual x1_product x0_partial x0_residual x0_product
   3  1692850  20944     846410 0.02474451    80.827445    1269630 0.01649614    80.827445
   4  1692850  20944     634800 0.03299307    80.827445    1269630 0.01649614    80.827445
   5  1692850  20944     421172 0.04972790    80.827445    1269630 0.01649614    80.827445
   6  1692850  20944     209502 0.09997041    80.827445    1269630 0.01649614    80.827445
   7  1692850  20944     105014 0.19944007    80.827445    1269630 0.01649614    80.827445
   8  1692850  20944      52208 0.40116457    80.827445    1269630 0.01649614    80.827445
   9  1692850  20944      25280 0.82848101    80.827445    1269630 0.01649614    80.827445
```

So partial-depth conditioning is not an independent selector.  For X1 it pays
some initial 2-adic bits and leaves the rest; for X0 the first stage is cheap
because it omits orientation, but the residual probability remains unchanged.
Either way the product is the full-depth cost.

## Small-Height Constant Parameter Frontier

Timestamp: 2026-06-04T05:06:03Z.

After separating the strict certificate problem into target-trace curve
construction plus post-trace `x0` projection, I checked the remaining
p-specific-looking loophole that does not require large computation: perhaps a
bounded-height constant Montgomery parameter, squared parameter, or Montgomery
`j`-invariant is systematically in the strict DANGER bucket for the near-square
family `p = n^2 + 7`.

I reran the exact convolution probe at a wider height:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/small_height_parameter_probe.py --min-p 100000 --max-p 1000000 \
  --max-rows 20 --height 200 --top 12
```

The run checked:

```text
A_candidate_count=48927
A2_candidate_count=24464
j_candidate_count=48927
```

Survivors vanished almost immediately:

```text
row=01 p=102407 survivors_A=1086 survivors_A2=282 survivors_j=372
row=02 p=108907 survivors_A=20   survivors_A2=0   survivors_j=2
row=03 p=118343 survivors_A=0    survivors_A2=0   survivors_j=0
```

The best non-perfect hit counts over all 20 rows were random-looking small
frequencies:

```text
top_A:  hits=5/20 at A=+-115/82
top_A2: hits=4/14 at A^2=183/59, hits=4/12 at A^2=5/182
top_j:  hits=3/20 for several unrelated constants
perfect_A_survivors=0
perfect_A2_survivors=0
perfect_j_survivors=0
conclusion=no_bounded_height_constant_parameter
```

This does not rule out a one-off p24 lucky constant.  But without a surviving
near-square family pattern or an installed SEA/Schoof implementation to point
count many fixed non-CM curves at the actual 24-digit prime, testing bounded
constants is only another finite lottery.  It gives no asymptotic route unless
one first supplies a constructive formula selecting the trace class.

## Two-Adic Trace Inversion Sidecar

Timestamp: 2026-06-04T05:38:00Z.

I recorded the Satoh/AGM/canonical-lift, Hasse-invariant, theta-constant, and
Legendre/Landen inversion question in:

```text
p24/two_adic_trace_inversion_sidecar.md
```

The conclusion is negative for the standard machinery.  These algorithms are
fast forward point-counting/trace-label tools for a supplied curve.  Reversing
them to construct a curve with Frobenius eigenvalue

```text
lambda == 1 mod 2^40
```

requires choosing a depth-40 Frobenius-fixed ray orientation.  In moduli terms,
that is the `X1(2^40)` tower, not just the `X0(2^40)` cyclic-subgroup tower.

The deterministic p24 checks rerun for this sidecar were:

```text
python3 p24/x0_eigenvalue_orientation_audit.py
python3 p24/ray_orientation_audit.py
python3 p24/x0_orientation_audit.py
```

They give the same barrier:

```text
at a=40, four X0 eigenvalue roots for the DANGER trace residue
only two roots have a true X1 orientation
X0 trace-residue image = 1/8 of all residues
Gamma0(2^40) index = 1.649267 * sqrt(p)
Gamma0(2^41) index = 3.298535 * sqrt(p)
```

For Legendre/theta/Landen recurrences, an inverse recurrence must prescribe a
coherent depth-40 square-root/isogeny branch before the curve is known.  At a
half level `h`, the missing tail is

```text
lambda = 1 + 2^h u mod 2^40,  u == 0 mod 2^(40-h),
```

which is exactly the ray/X1 lift.  The sidecar includes a falsifiable
small-prime test: on small `p=n^2+7` rows, a claimed inversion label must
predict this missing tail with growing advantage after conditioning on
`X0(2^h)`, while using only `2^o(k)` branch work.  Existing local trace-label
and X0/X1 audits are negative for the visible low-degree labels.

## Near-Singular Torus-Coordinate LFT Probe

The singular limits `A = +/-2` are rejected and have too little 2-power for
p24, but a nearby multiplicative-coordinate section could in principle be a
different p-specific identity.  I tested the natural perturbation shape

```text
A = +/- (r + 1/r)
r(n) = (a*n + b)/(c*n + d)
```

with small integer coefficients.  This is the split torus coordinate that
degenerates to `A = +/-2` when `r = +/-1`, so it gives the near-singular idea a
more direct test than scanning small constants in `A`.

I wrote:

```text
p24/torus_lft_parameter_probe.py
```

Moderate run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/torus_lft_parameter_probe.py --min-p 10000 --max-p 250000 \
  --max-rows 20 --coeff-bound 8 --top 12

row=01 p=14407 survivors_all_rows_so_far=3184
row=02 p=18503 survivors_all_rows_so_far=144
row=03 p=20743 survivors_all_rows_so_far=8
row=04 p=30983 survivors_all_rows_so_far=0
...
perfect_survivors=0
conclusion=no_low_height_torus_lft_parameter
```

Wider coefficient run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/torus_lft_parameter_probe.py --min-p 100000 --max-p 1000000 \
  --max-rows 12 --coeff-bound 16 --top 8

row=01 p=102407 survivors_all_rows_so_far=11616
row=02 p=118343 survivors_all_rows_so_far=256
row=03 p=123911 survivors_all_rows_so_far=0
...
perfect_survivors=0
conclusion=no_low_height_torus_lft_parameter
```

The top hit counts were small random-looking frequencies (`5/20` and `4/12`),
not surviving sections.  Thus the low-height perturbation of the singular
torus does not supply the missing trace selector.

## Low-Degree Correspondence / Trace-Shift Barrier

I also made explicit why the broad fast seed curves cannot be moved into the
strict target trace by a small algebraic correspondence:

```text
p24/low_degree_correspondence_barrier.py
```

Representative run:

```text
python3 p24/low_degree_correspondence_barrier.py

near_square_D_minus_7_seed
  trace=2000000000000 trace_mod_2^40=900488372224 v2_order=3 v2_twist=3 nearest_strict_trace=1178414874616 distance=821585125384
  trace=-2000000000000 trace_mod_2^40=199023255552 v2_order=3 v2_twist=3 nearest_strict_trace=-1178414874616 distance=821585125384
  j=-3375 not_exceptional=True
  isogeny_trace_shift_possible=False
  quadratic_twist_traces_only=+/-2n

strict_target_class_entropy
  total_signed_j_classes_est=1.317682e+12
  random_j_expected_trials=7.589086e+11

degree_required_for_exponent_saving
  p^0.40 1.906292e+2
  p^0.35 3.021270e+3
  p^0.30 4.788390e+4
  p^0.25 7.589086e+5

conclusion=low_degree_correspondences_from_the_fast_seed_curves_only_change_constants; trace_shift_requires_either_a_growing_level_or_a_new_class_selector
```

The arithmetic is simple but useful to keep visible: isogenies preserve trace,
the `j=-3375` near-square CM curve has only the two quadratic-twist traces
`+/-2n`, and any bounded-degree non-isogenous recipe is just a bounded-degree
family over the `j`-line.  The latter can improve constants, but not the
sqrt-exponent, unless the degree grows with the verifier level or a new class
selector is supplied.

## Ramified-Factor and Redei 4-Rank Audits

The latest class-group sidecar sharpened the CM no-go: the conductor-2 target
orders have no hidden 2-primary class structure beyond genus.  I added two
small reproducible audits:

```text
p24/ramified_factor_tradeoff_audit.py
p24/redei_4rank_audit.py
```

Representative ramified-factor run:

```text
python3 p24/ramified_factor_tradeoff_audit.py

trace=1020608380936
  prime_discriminants=[29, -25503090799682730273827]
  best small ramified quotient: impose 29, residual_classes=1.393440e+11

trace=-78903246840
  prime_discriminants=[-7, -211, 4973929, -135907507341779]
  best small ramified quotients: impose -7, -211, 4973929,
    optimistic_degree=4974150, residual_classes=1.041208e+11

trace=-1178414874616
  prime_discriminants=[-599, 1089874116562502921057]
  best small ramified quotient: impose -599, residual_classes=1.030138e+11

conclusion=ramified_prime_conditions_are_only_genus_quotients;
  for_p24_they_save_constant_bits_and_do_not_create_a_subsqrt_selector
```

The middle discriminant's `-7` component is the tempting bait because
`p=n^2+7`, but in this target CM order it is only a genus component.  It does
not lift the known `D=-7` near-square identity to a strict DANGER root/class
selector.

Representative Redei run:

```text
python3 p24/redei_4rank_audit.py

trace=1020608380936
  prime_discriminants=[29, -25503090799682730273827]
  rank_F2=1 r_minus_1=1 four_rank=0

trace=-78903246840
  prime_discriminants=[-7, -211, 4973929, -135907507341779]
  rank_F2=3 r_minus_1=3 four_rank=0

trace=-1178414874616
  prime_discriminants=[-599, 1089874116562502921057]
  rank_F2=1 r_minus_1=1 four_rank=0

conclusion=target_2primary_class_structure_stops_at_genus;
  there_are_no_hidden_4_or_8_rank_layers
```

So the conductor-2 kernel is trivial, genus saves only `1,3,1` bits, and the
principal-genus residual sets are still about `1e11` classes.  Any CM-based
strict route would need a new odd-part class selector, not ramified ideals,
genus characters, small-norm relations, or 2-primary class-field layers.

## Parallel Sidecar Status

I split three independent checks into subagents:

```text
public reconnaissance: no posted p24 strict triple/certificate found
modular-level/orientation: Atkin, Fricke, volcano, and CRT variants all
  reintroduce the missing 2-adic tail; best half-level tradeoff remains
  about 1.65*sqrt(p)
class-group selector: no hidden 2-primary layers; Redei 4-rank zero; no
  ramified/genus selector beyond constant bits
```

This keeps the live frontier narrow: a strict asymptotic win would need either
a genuinely new finite-field identity forcing the high 2-adic Frobenius
orientation, or an odd-part class selector for one of the large residual CM
class groups.  I have not found such a selector.

## x-Projection Concentration Audit

I checked a possible miss in the earlier A-line framing: maybe the verifier
certificate curve

```text
Z_k(A,x)=0,  Z_{k-1}(A,x) != 0
```

has a cheap projection to the `x`-line.  If one simple `x0` had a growing
number of compatible Montgomery parameters `A`, fixed-`x0` division could be a
strict shortcut even without an A-line trace selector.

I added:

```text
p24/x_projection_concentration_audit.py
```

Small exact run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/x_projection_concentration_audit.py --min-p 500 --max-p 12000 \
  --max-rows 6 --simple-height 20 --top 6

row n p k pairs occupied_x occupied_frac mean_per_x max_per_x
01 32 1031 6 2752 956 0.927255 2.669253 8
02 40 1607 6 5184 1548 0.963286 3.225887 11
03 48 2311 6 8640 2260 0.977932 3.738641 12

aggregate
  max_per_x_max=12
  mean_occupied_fraction=0.956157
  mean_pairs_per_x=3.211260
conclusion=x_projection_has_constant_sized_fibers;
  fixed_x_conditioning_does_not_create_a_depth_growing_A_selector
```

The projection is dense but flat: almost every `x` occurs, but each `x`
supports only a small constant number of `A`s.  A wider full enumeration was
stopped because it was turning into a bandwidth job.  I then used the existing
fixed-`x` division-polynomial probe at medium scale instead:

```text
python3 p24/half_depth_division_probe.py --p 102407 --x 2 --max-depth 9 --root-limit 50
python3 p24/half_depth_division_probe.py --p 102407 --x 3 --max-depth 9 --root-limit 50
python3 p24/half_depth_division_probe.py --p 102407 --x 5 --max-depth 9 --root-limit 50
```

At this field, the verifier depth is `k=9`; the fixed-`x` A-line polynomial at
depth 9 has degree `65535`.  The usable nonsingular roots were:

```text
x=2: usable_roots=4
x=3: usable_roots=2
x=5: usable_roots=3
```

Thus fixed-`x` conditioning behaves like the inverse-chain MITM split: it
moves the entropy into a high-degree division equation with constant-sized
root set.  It does not expose a depth-growing family of `A` values.

## Near-Square Radical Relation Barrier

I also made explicit why the `p=n^2+7` radical itself cannot be promoted to a
strict CM selector by giving the target curve a hidden `D=-7` endomorphism.
The new audit is:

```text
p24/near_square_radical_relation_barrier.py
```

Representative run:

```text
python3 p24/near_square_radical_relation_barrier.py --min-p 500 --max-p 50000 --max-rows 8

p24 near-square radical relation barrier
p=1000000000000000000000007
n=1000000000000
sqrt_minus_7_in_Fp=1000000000000
cheap_CM_field_D=-7

trace=1020608380936
  fundamental_D=-739589633190799177940983
  same_field_as_D_minus_7=False
  contains_minus_7_as_prime_discriminant=False
  v2_curve_order=42

trace=-78903246840
  fundamental_D=-998443569409526507503607
  same_field_as_D_minus_7=False
  contains_minus_7_as_prime_discriminant=True
  quotient_abs_D_over_7=142634795629932358214801
  explicit_sqrt_of_quotient_mod_p=148493089060000000000001
  sqrt_check=0
  v2_curve_order=40

trace=-1178414874616
  fundamental_D=-652834595820939249713143
  same_field_as_D_minus_7=False
  contains_minus_7_as_prime_discriminant=False
  v2_curve_order=41

p24_conclusion=the_D_minus_7_radical_supplies_only_genus_splitting;
  strict_target_CM_fields_are_distinct_ordinary_fields
```

The middle target is the bait: because its discriminant has a `-7` prime
discriminant factor, the known square root `n^2=-7 mod p` gives a square root
of the quotient `|D|/7` modulo `p`.  That is real information, but it is
exactly the genus-field splitting already counted by the genus/Redei audits.

The field-theory obstruction is sharper: an ordinary elliptic curve has
commutative endomorphism algebra.  If a strict target curve were isogenous to
or carried endomorphisms from both `Q(sqrt(-7))` and `Q(sqrt(D_K))`, then those
quadratic fields would have to coincide.  They do not for any of the three
p24 target traces.

Small near-square calibration rows also showed no generic strict trace whose
fundamental field is actually `D=-7`:

```text
row n p k target_traces same_D_minus_7_fields minus7_prime_discriminant_hits
01 32 1031 6 2 0 1
02 40 1607 6 3 0 0
03 48 2311 6 3 0 1
04 120 14407 8 2 0 2
05 136 18503 8 2 0 0
06 144 20743 8 3 0 0
07 176 30983 8 3 0 1
08 184 33863 8 3 0 0

calibration_conclusion=near_square_D_minus_7_field_coincidence_is_not_the_generic_strict_trace_mechanism
```

So the near-square radical is a genuine broad-certificate selector, and a
constant-bit genus label for one strict target, but not a strict root selector.

## Root-Only CM and High-Dimensional Inverse-Chain Sidecars

Two parallel sidecars checked whether the remaining live shapes are already
covered by known algorithms or by a more flexible inverse-chain parametrization:

```text
p24/subagent_root_only_cm_note.md
p24/subagent_inverse_chain_param_note.md
```

Root-only CM verdict:

```text
known CM / prescribed-order methods either compute a class object, require a
seed curve/root in the target isogeny class, or use freedom to choose a better
field/discriminant.  For fixed p24, the strict trace fixes |D| ~= p; the
principal representation proves splitting over F_p but does not select one
root among the huge residual class set.
```

The note cites the relevant primary algorithms: Agashe-Lauter-Venkatesan CRT
CM, Sutherland CRT/class-invariant methods, Belding-Broeker-Enge-Lauter,
Broeker-Stevenhagen prescribed-order constructions, Sutherland prescribed
torsion, and Shparlinski-Sutherland prescribed-subgroup results.  None supplies
a bounded-degree datum that names one strict p24 root without either a seed or
a sqrt-scale class object.

High-dimensional inverse-chain verdict:

```text
multi-variable recurrences, transfer matrices, EDS formulations, and
MITM/elimination repackage the strict X1(2^40) ray-orientation condition.
They either collapse to known degenerate cases, help only after A is known,
omit the verifier orientation via X0, or carry the full missing ray tail and
restore Theta(sqrt(p)) cost.
```

This strengthens the inverse-chain frontier: adding variables to the literal
chain does not make the certificate variety high-dimensional in the useful
sense.  It is a coordinate expansion of the same growing `X1` moduli problem,
unless a new p24-specific arithmetic label predicts the high 2-adic ray tail.

## Small Genus CM Factors and Prime Odd Cofactor

I checked a nearby construction idea: the strict target discriminants contain
small imaginary genus factors such as `-7`, `-211`, and `-599`.  If any of
these small CM fields were principal over the fixed p24 field and had high
2-adic depth, it would be a cheap strict curve construction rather than a
large-discriminant CM problem.

I added:

```text
p24/small_genus_cm_factor_audit.py
```

Representative run:

```text
python3 p24/small_genus_cm_factor_audit.py

p24 small genus CM factor audit
p=1000000000000000000000007
k=40

D=-7
  kronecker_split=1
  principal_trace_count=1
  traces=[{'trace': 2000000000000, 'conductor': 2,
           'v2_order': 3, 'v2_twist': 3, 'strict_hit': False},
          {'trace': -2000000000000, 'conductor': 2,
           'v2_order': 3, 'v2_twist': 3, 'strict_hit': False}]

D=-211
  kronecker_split=1
  principal_trace_count=0
  traces=[]

D=-599
  kronecker_split=1
  principal_trace_count=0
  traces=[]

D=-34817503
  kronecker_split=1
  principal_trace_count=0
  traces=[]

D=-1049499019
  kronecker_split=1
  principal_trace_count=0
  traces=[]

conclusion=small_imaginary_genus_factors_are_either_nonprincipal_over_Fp_
or_the_known_D_minus_7_depth3_curve;_no_strict_CM_shortcut
```

This separates quadratic splitting from principal CM over `F_p`.  The fields
`-211`, `-599`, `-7*4973929`, and `-211*4973929` split, so they are real
genus labels, but they do not give principal norm equations
`t^2 + |D| f^2 = 4p`.  Thus there is no fixed-field small-CM trace from them
to test.  The only principal small factor is the known near-square `D=-7`
curve, and it has depth `3`.

I also rechecked the prime-odd-cofactor row.  The strict curve-side orders are

```text
2^40 * q       with q   = 909494701772 = 2^2 * 29 * 71 * 110429177
2^40 * (q+1)   with q+1 = 909494701773 = 3 * 7 * 43309271513
2^40 * (q+2)   with q+2 = 909494701774 = 2 * 454747350887
```

The `q+2` row has odd part `454747350887` after the extra factor of `2`, so
projection is particularly pleasant after the curve is known.  But
`p24/group_structure_audit.py` still gives the governing conclusion:

```text
conclusion=prime_odd_part_helps_projection_only_after_target_isogeny_class_is_found
```

Small-field calibration in `p24/prime_odd_part_small_probe.py` also shows prime
odd parts occurring as ordinary target-order labels, not as a construction
selector.  The prime cofactor helps finish a certificate on a known target
curve; it does not reduce the trace-class entropy needed to find that curve.

## Small Split-Prime Cycle Barrier

I then separated one more CM-cycle loophole from the earlier ramified-prime and
split-2 audits.  A small split prime `ell` could have an ideal-class order
`m` around `log_ell(|D|)`, giving a short-looking chain of `ell`-isogenies.
Maybe one could solve those local cycle equations instead of computing a full
class polynomial.

I added:

```text
p24/small_split_prime_cycle_barrier.py
```

Representative run:

```text
python3 p24/small_split_prime_cycle_barrier.py

p24 small split-prime cycle barrier
p=1000000000000000000000007
sqrt_floor=1000000000000
split_prime_bound=200

trace=1020608380936
  best_split_prime_cycles_by_composite_norm
    ell min_m ell^m/sqrt_p h_est/min_m
     89    12   2.469904e+11   2.322399e+10
      2    78   3.022315e+11   3.572922e+09
     97    12   6.938424e+11   2.322399e+10

trace=-78903246840
  best_split_prime_cycles_by_composite_norm
    ell min_m ell^m/sqrt_p h_est/min_m
     47    14   2.566670e+11   5.949759e+10
      2    78   3.022315e+11   1.067905e+10
    137    11   3.190996e+11   7.572420e+10

trace=-1178414874616
  best_split_prime_cycles_by_composite_norm
    ell min_m ell^m/sqrt_p h_est/min_m
     17    19   2.390724e+11   1.084356e+10
     89    12   2.469904e+11   1.716897e+10
     29    16   2.502465e+11   1.287672e+10

conclusion=small_split_prime_cycles_either_have_composite_degree_far_above_
sqrt_p_or_leave_sqrt_scale_many_cycles_without_a_seed_root
```

The governing lower bound is again

```text
4 * ell^m = x^2 + |D| y^2,  y != 0,
```

so a non-scalar principal relation has composite degree at least `|D|/4`.
Writing it as `m` local low-degree modular equations does not select a root:
the CM root set is partitioned into about `h(D)/m` cycles, still billions to
tens of billions for the p24 targets.  Thus small split-prime cycles do not
give a sub-sqrt construction unless a separate seed/root selector is supplied.

## Edwards / Complete-Edwards Subfamily Audit

I checked whether Edwards or complete Edwards models give a genuinely new
structured family rather than another coordinate on the Montgomery line.  The
map for `a=1` twisted Edwards curves is

```text
A = 2*(1+d)/(1-d),      d = (A-2)/(A+2),
chi(A^2 - 4) = chi(d).
```

Thus complete Edwards with nonsquare `d` is exactly the nonsplit Montgomery
half, not a new trace selector.  I added:

```text
p24/edwards_nonsplit_constant_factor_audit.py
```

Representative exact run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/edwards_nonsplit_constant_factor_audit.py --min-p 10000 \
  --max-p 250000 --max-rows 12

aggregate
  total_A=513788
  nonsplit_A=256900
  split_A=256888
  strict_all=12444
  strict_nonsplit=6240
  strict_split=6204
  strict_density_all=0.02422011
  strict_density_complete_edwards_nonsplit=0.02428961
  strict_density_split=0.02415060
  complete_edwards_lift_vs_all=1.002870
  target_trace_all=18720
  target_trace_nonsplit=6240
  target_trace_split=12480

conclusion=complete_edwards_is_the_nonsplit_montgomery_half_and_changes_
strict_density_by_only_a_constant_factor
```

This matches the bounded-degree family entropy audit:

```text
conclusion=bounded_degree_explicit_families_only_change_constants;
  exponent_saving_requires_growing_degree_or_new_class_selector
```

So Edwards/complete-Edwards forms can be useful for implementation choices and
constant-factor split/nonsplit filtering, but they do not construct the rare
target trace class.

## Cyclotomic / Jacobi-Sum Quadratic Subfields

I then isolated the Jacobi-sum identity route.  For elliptic curves, a
closed-form Jacobi-sum trace is a CM trace in an imaginary quadratic subfield
of a cyclotomic field.  The cheap cyclotomic conductors visible from the small
factors of p24 are:

```text
p - 1 = 2 * 7 * 29 * 2463054187192118226601
p + 1 = 2^3 * 3^2 * 19 * 739 * 1187 * 833333316666667
```

I added:

```text
p24/cyclotomic_quadratic_subfield_audit.py
```

It enumerates negative fundamental discriminants whose conductor divides the
small smooth part of `p-1` or `p+1`, then solves

```text
t^2 + |D| f^2 = 4p
```

to see whether the subfield is principal over `F_p` and what 2-adic depth the
resulting CM trace has.

Representative run:

```text
python3 p24/cyclotomic_quadratic_subfield_audit.py

p24 cyclotomic quadratic-subfield CM audit
p=1000000000000000000000007
k=40
p_minus_smooth=406
p_plus_smooth=1200000024

p_minus_character_subfields
  smooth_conductor=406
  negative_fundamental_D_count=2
  D=          -7 split= 1 principal_traces=2
    trace= -2000000000000 conductor=              2 v2_order= 3 v2_twist= 3 strict_hit=0
    trace=  2000000000000 conductor=              2 v2_order= 3 v2_twist= 3 strict_hit=0
  D=        -203 split= 1 principal_traces=2
    trace= -1471186224951 conductor=    95091635647 v2_order= 0 v2_twist= 0 strict_hit=0
    trace=  1471186224951 conductor=    95091635647 v2_order= 0 v2_twist= 0 strict_hit=0
  any_principal_trace=1
  any_strict_hit=0

p_plus_unitary_character_subfields
  smooth_conductor=1200000024
  negative_fundamental_D_count=32
  all listed D have split=-1 and principal_traces=0
  any_principal_trace=0
  any_strict_hit=0

conclusion=cheap_cyclotomic_quadratic_subfields_give_no_strict_jacobi_sum_trace;
  _only_small_non_strict_CM_traces_or_nonprincipal_splitting
```

Thus the accessible small-order character/Jacobi-sum identities do not contain
a strict p24 trace.  Including the huge prime factors in the conductors would
no longer be a cheap cyclotomic identity; it is exactly the large-discriminant
CM/class-selection problem already tracked above.

## Dyadic A / j Residue Label Audit

The remaining "cheap curve-level label" possibility has a very literal
2-adic version: perhaps the verifier's high 2-power trace condition is visible
from the integer representatives of `A` or `j(A)` modulo `2^b`, before any
point counting.  I made that exact small-field test explicit in:

```text
p24/dyadic_parameter_residue_audit.py
```

It computes every strict good Montgomery parameter for small prime rows
`p=n^2+7`, then buckets by `A mod 2^b` and `j(A) mod 2^b`.

Representative larger run:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/dyadic_parameter_residue_audit.py --min-p 10000 \
  --max-p 500000 --max-rows 16 --max-bits 12

good=20072/988048
base_rate=0.02031480

A_best_by_bits
  bits= 8 best_lift r=  233 lift=1.378 capture=0.0054 hits=108/3857
  bits=12 best_lift r= 2164 lift=3.077 capture=0.0007 hits=15/240

j_best_by_bits
  bits= 8 best_lift r=   73 lift=1.606 capture=0.0064 hits=128/3924
  bits=12 best_lift r= 2378 lift=4.628 capture=0.0011 hits=22/234

top_buckets_by_score
  j bits= 1 r=    1 lift=1.034 capture=0.5173 coverage=0.5004
  A bits= 1 r=    1 lift=1.000 capture=0.5000 coverage=0.5000

conclusion=dyadic_A_or_j_residues_show_only_constant_bucket_lifts_not_a_
growing_trace_v2_selector
```

The high-lift buckets at larger `b` are tiny-sample extremes with capture
falling at the bucket size.  The best broad buckets remain the obvious parity
halves with near-unit lift.  So small dyadic residues of the usual curve
coordinates behave like random bucket refinements, not like a constructive
2-adic trace-v2 selector.

## Division-Polynomial Splitting Barrier

I also isolated a tempting direct-algebra route:

```text
Z_k(A,x) = 0
```

for the Montgomery x-only doubling recurrence.  Maybe one could eliminate `x`
or solve this equation directly rather than searching target traces.

The obstruction is that this equation is only the algebraic division-polynomial
condition.  Over `Fbar_p`, every nonsingular elliptic curve has full
`2^k`-torsion, so eliminating `x` does not cut out the rare target `A` values.
The verifier needs an exact-order division-polynomial root already defined
over `F_p`, and that splitting condition is exactly Frobenius acting by
`+1` or `-1` on a `2^k` ray.

I wrote the note:

```text
p24/division_polynomial_splitting_barrier.md
```

This ties the direct equation-solving idea back to the same `X1(2^40)`
orientation obstruction as the modular/tower and two-adic inversion audits.

## Intermediate Diamond Quotient Audit

One remaining modular-curve loophole was an intermediate quotient between
strict x-only `X1(2^40)/{+/-1}` and coarse `X0(2^40)`: remember some but not
all generator/orientation data, hoping to make construction cheaper while
leaving only a small lift.

For powers of two this quotient lattice is rigid.  After identifying `P` and
`-P`, the diamond group is cyclic of order

```text
phi(2^40)/2 = 2^38.
```

I added:

```text
p24/intermediate_diamond_quotient_audit.py
```

Representative run:

```text
python3 p24/intermediate_diamond_quotient_audit.py

Gamma0(2^k)_index=1649267441664
Gamma0_index_over_sqrt=1.649267
diamond_group_mod_sign_order=phi(2^k)/2=274877906944
diamond_group_mod_sign_structure=cyclic_2_power

subgroup_bits quotient_degree_to_X0 quotient_index_over_sqrt
            0          274877906944             4.533472e+11
           20                262144             4.323456e+05
           32                    64             1.055531e+02
           37                     2             3.298535e+00
           38                     1             1.649267e+00

best_quotient_index=subgroup_bits=38 index_over_sqrt=1.649267e+00
conclusion=intermediate_diamond_quotients_only_trade_modular_index_
against_the_same_missing_orientation_fiber
```

The coarsest quotient `X0(2^40)` has the smallest modular index and is still
above `sqrt(p)` before it supplies any strict verifier orientation.  Any
intermediate quotient closer to `X1` only raises the modular degree while
shrinking the residual orientation ambiguity by the same power of two.  So
diamond quotients do not create a sub-sqrt strict construction.

## Exact Class Group Structure / Odd-Tower Lead

The earlier CM audits used Euler-product class-number estimates.  I installed
`cypari2` from a prebuilt wheel and used PARI's quadratic class group routines
to get exact data for the three target fields.  I added:

```text
p24/exact_class_group_structure_audit.py
```

Representative run:

```text
python3 p24/exact_class_group_structure_audit.py

trace=1020608380936
  class_number=278733727154
  class_group_invariants=[278733727154]
  factor_class_number={2: 1, 19: 1, 7335098083: 1}

trace=-78903246840
  class_number=833035208344
  class_group_invariants=[208258802086, 2, 2]
  factor_class_number={2: 3, 104129401043: 1}

trace=-1178414874616
  class_number=205880396014
  class_group_invariants=[205880396014]
  factor_class_number={2: 1, 157: 1, 211: 1, 3107441: 1}

conclusion=exact_class_groups_do_not_give_a_root_but_the_third_target_has_
a_smoothish_odd_component_worth_separating_from_the_large_class_polynomial_
obstruction
```

This is the most interesting remaining lead.  The first two targets still have
large cyclic odd factors (`7.3e9` and `1.04e11`).  The third target has a
smooth-ish odd part:

```text
h/2 = 157 * 211 * 3107441.
```

In principle, an explicit class-field tower or class invariant whose largest
relative degree is `3107441` would be sub-sqrt for this fixed p24 target.  But
the exact class group does not itself name a root.  One still needs explicit
quotient invariants and the embedding back to the CM `j`-root / Montgomery
`A`.

I made a small PARI sanity check on the third target.  The degree-2 genus
quotient materializes immediately:

```text
bnrclassfield(..., Mat(2), 1) = x^2 + 599
```

which is exactly the already-known genus factor.  Asking PARI for the first
odd quotient of degree `157` overflowed a 512 MB PARI stack after about a
minute.  More importantly, `bnrclassfield` returns an abstract class-field
equation, not by itself the class invariant map that recovers one `j` root
modulo p.  So this remains a real but unresolved shape:

```text
construct an explicit odd class-field quotient/tower for
D_K=-652834595820939249713143, then recover a target CM j root over F_p
without enumerating h roots.
```

No such invariant/root-selection construction has been found yet.

I then checked whether this smooth-ish class group is visible through small
split-prime class actions.  I added:

```text
p24/smooth_class_tower_probe.py
```

Representative run:

```text
python3 p24/smooth_class_tower_probe.py --prime-bound 50000

trace=-1178414874616
class_number=205880396014
factor_class_number={2: 1, 157: 1, 211: 1, 3107441: 1}
split_primes_checked=2513

smallest_split_prime_by_generated_subgroup_index
  index ell order factor_order
         1     23 205880396014 {2: 1, 157: 1, 211: 1, 3107441: 1}
         2      2 102940198007 {157: 1, 211: 1, 3107441: 1}
       157   2897   1311340102 {2: 1, 211: 1, 3107441: 1}
       211  14057    975736474 {2: 1, 157: 1, 3107441: 1}
       314    677    655670051 {211: 1, 3107441: 1}
       422   7349    487868237 {157: 1, 3107441: 1}

conclusion=small_split_primes_generate_large_class_subgroups_but_still_
need_an_explicit_class_field_root_selector
```

So the third target's class group is not only smooth-ish; it is generated by
the small split prime `23`, and useful quotient indices are represented by
small primes like `2897` and `14057`.  This supports the idea that a tower of
small modular equations could describe the class action.  It still does not
name a seed/root in the target isogeny class.  A full `23`-isogeny cycle has
length `h`, and solving local cycle equations without a class-field invariant
or root selector is just the earlier cycle barrier in a more favorable-looking
coordinate system.

Pauli then audited this lead against known polycyclic/decomposed CM and
class-invariant methods, using Sutherland's decomposed CM method, CRT Hilbert
class polynomials, CRT class invariants, and p-adic/CRT Hilbert class
polynomial algorithms as the comparison points.  The resulting note is:

```text
p24/subagent_smooth_class_tower_note.md
```

I also added a small degree-tradeoff script:

```text
p24/decomposed_cm_tradeoff_audit.py
```

Representative run:

```text
python3 p24/decomposed_cm_tradeoff_audit.py

class_number=205880396014
class_factors=[2, 157, 211, 3107441]
sqrt_floor_abs_D=807981804139

divisor_split degree_a degree_b max_degree sum_degrees max_over_sqrt_p
(3107441,)        66254      3107441      3107441      3173695 3.107441e-06
(2, 3107441)      33127      6214882      6214882      6248009 6.214882e-06
(2, 211)            422    487868237    487868237    487868659 4.878682e-04

best_degrees=66254*3107441
best_largest_degree=3107441

known_method_obstruction
  decomposed_CM_reduces_root_degree_and_memory=1
  embedded_equations_required=1
  abstract_class_field_equation_suffices=0
  seed_CM_root_required_for_isogeny_orbit_enumeration=1
  known_embedded_construction_cost_scale=about_sqrt_abs_D_or_worse
```

So the smooth third target genuinely reduces the *final root degree* one would
face after obtaining embedded decomposed CM equations.  It does not remove the
known cost of constructing those embedded equations.  The relevant literature
methods that map back to `j` still build an embedded class object through
CRT/complex/p-adic/class-orbit work at roughly `sqrt(|D|)` scale or worse; the
abstract class-field routines expose quotient structure but do not provide an
embedded invariant with a recovery map to `j`.

I then separated one more possible misunderstanding: odd-level modular
relations can have very small degree without being free to construct.  I
added:

```text
p24/odd_level_invariant_degree_audit.py
```

Representative run:

```text
python3 p24/odd_level_invariant_degree_audit.py

level gamma0_index gamma0_over_sqrt
      23           24     2.400000e-11
     157          158     1.580000e-10
     211          212     2.120000e-10
    2897         2898     2.898000e-09
   14057        14058     1.405800e-08
 3107441      3107442     3.107442e-06

composite_factor_levels
  level=          33127 gamma0_index=          33496 gamma0_over_sqrt=3.349600e-08
  level=      487868237 gamma0_index=      490975836 gamma0_over_sqrt=4.909758e-04
  level=      655670051 gamma0_index=      658777704 gamma0_over_sqrt=6.587777e-04
  level=   102940198007 gamma0_index=   104086877232 gamma0_over_sqrt=1.040869e-01

conclusion=odd_level_invariants_have_subsqrt_recovery_degrees_but_do_not_
supply_embedded_equations_or_seed_roots_for_free
```

This means a small recovery map is plausible in principle for the smooth target
lead.  The missing part remains the embedded CM invariant/equation or seed
target vertex.  The class factorization and small split primes tell us what
the map could look like; they do not provide the map.

## Embedded Decomposition Calibration

To make the previous paragraph less abstract, I built a tiny decomposed-CM
calibration where all objects are computable:

```text
p24/embedded_decomposition_calibration.py
```

It uses the small ring-class discriminant

```text
D = -5000
h(D) = 30
q = 1259
```

where `H_D` splits completely modulo `q`, and a norm-3 ideal generates the
cyclic class group.  The script computes the 30 `j` roots, builds the
horizontal `3`-isogeny graph among them using `Phi_3`, walks the resulting
30-cycle, and then forms a decomposed embedded invariant by summing roots over
cosets of a subgroup of size 5.

Representative run:

```text
python3 p24/embedded_decomposition_calibration.py

hilbert_degree=30
split_roots=30
isogeny_graph_degrees=[2]
cycle_length=30

decomposition
subgroup_size=5
quotient_size=6
V_degree=6
U_selected_degree=5
selected_y=159
selected_coset_roots=[3, 1183, 1195, 923, 632]

conclusion=decomposed_CM_saves_final_root_degree_only_after_an_embedded_
CM_root_set_or_equivalent_invariant_has_been_constructed
```

This is exactly the p24 smooth-class issue in miniature.  The degree-30 root
problem decomposes into degree 6 plus degree 5, but the construction of those
polynomials used an actual seed root and the embedded `j`-root cycle.  An
abstract class group of order 30 would not have produced `V`, `U`, or the map
back to `j`.

I also added the asymptotic caveat:

```text
p24/smooth_class_asymptotic_caveat.md
```

The smooth third target is a real fixed-instance structural lead, but it is not
an asymptotic speedup by itself.  To become one, it would need both a theorem
forcing smooth target class groups in a growing family and an embedded
sub-sqrt construction of quotient invariants/recovery maps.  The present p24
data supplies only the fixed-instance smooth class group.

## Smooth Class Arithmetic Relation Audit

I checked whether the smooth class factors for the third target interact
directly with the finite-field arithmetic, target odd cofactor, or near-square
parameter.  A nontrivial gcd with `p-1`, `p+1`, or the target odd order would
have suggested a Kummer/radical shortcut or a direct projection label.

I added:

```text
p24/smooth_class_arithmetic_relation_audit.py
```

Representative run:

```text
python3 p24/smooth_class_arithmetic_relation_audit.py

curve_order=1000000000001178414874624
factor_curve_order={2: 41, 454747350887: 1}
class_number=205880396014
factor_class_number={2: 1, 157: 1, 211: 1, 3107441: 1}

gcds_with_class_number
  odd_order            gcd=           1 factors={}
  abs_DK               gcd=           1 factors={}
  p_minus_1            gcd=           2 factors={2: 1}
  p_plus_1             gcd=           2 factors={2: 1}
  n                    gcd=           2 factors={2: 1}
  trace                gcd=           2 factors={2: 1}

class_factor_residues
  factor p_mod factor p_order_mod_factor odd_order_mod_factor
       157       21                156                   150
       211      114                 35                    22
   3107441  2509452             388430               1327506

conclusion=class_group_smoothness_has_no_visible_kummer_or_group_order_
shortcut_with_p24_field_arithmetic
```

Thus the smooth class group and the verifier-friendly prime odd cofactor are
not coupled by an obvious divisibility relation.  This keeps the remaining
smooth-class route focused on an embedded class invariant/root selector, not a
field-arithmetic radical shortcut.

## Seedless 23-Cycle / Quotient-Cycle Audit

I tested the next natural constructive angle for the smooth third target:
whether the small split prime `23`, which generates the cyclic class group,
could define a seedless closed-cycle equation or quotient-cycle condition that
selects a target `j` root without constructing a Hilbert/class invariant.

I added:

```text
p24/seedless_cycle_resultant_audit.py
```

Representative run:

```text
python3 p24/seedless_cycle_resultant_audit.py

seedless_closed_cycle_degree_proxy
  label ell cycle_order index log10_psi(ell^order) log10_over_sqrt_p
  full_23_generator_cycle           23 205880396014        1           2.803531e+11       2.803531e+11
  index_157_subgroup_cycle        2897   1311340102      157           4.539792e+09       4.539792e+09
  index_211_subgroup_cycle       14057    975736474      211           4.047250e+09       4.047250e+09
  index_314_subgroup_cycle         677    655670051      314           1.855932e+09       1.855932e+09
  index_422_subgroup_cycle        7349    487868237      422           1.886210e+09       1.886210e+09

best_decomposed_cm_shape_if_embedded_invariants_are_known
  h=205880396014=66254*3107441
  quotient_degree=66254
  recovery_degree=3107441
  largest_final_root_degree_over_sqrt_p=3.107441e-06

seedless_subgroup_generator_lower_bound
  log10(degree) >= 9.354330e+05 before it selects a CM root.
```

The reason is structural.  A seedless modular condition for an endomorphism of
norm `ell^r` lives at `X0(ell^r)` degree

```text
psi(ell^r) = ell^r + ell^(r-1),
```

so the log-degree is about `r log10(ell)`.  For p24, the relevant orders `r`
are class subgroup orders.  The small prime `23` makes class action easy once
a target vertex is known; without a seed or an embedded CM-order filter, it
turns into an astronomically large modular resultant and also admits unrelated
orders/cycles.

The toy calibration makes the same point at a size we can see:

```text
D=-5000, h=30, q=1259, ell=3 generator
seedless_Phi_(3^30)_fixed_point_degree=274521509459532
embedded_H_D_degree=30
decomposed_after_embedded_cycle_degrees=6_and_5
```

So the decomposed-CM saving is real only after the embedded `j`-root orbit,
orbit sums, or an equivalent quotient invariant with a recovery map is already
available.  The seedless 23-cycle / quotient-cycle route does not supply that
primitive and does not beat sqrt-scale for the strict p24 certificate.

## Class-Invariant Stabilizer Audit

I then checked whether a known fixed/low-level class invariant could have the
large stabilizer that the smooth third target wants.  The desired shape is:

```text
h = 205880396014 = 66254 * 3107441
```

and an invariant fixed by a subgroup of size `3107441` would have class
polynomial degree `66254` with recovery degree `3107441`, both far below
`sqrt(p)`.

I added:

```text
p24/class_invariant_stabilizer_audit.py
```

Representative run:

```text
python3 p24/class_invariant_stabilizer_audit.py

split_prime_edge_invariants
  ell kronecker ideal_order ideal_index x0_map_degree edge_orbit_proxy edge_orbit_over_sqrt
        23         1 205880396014           1             24     205880396014         2.058804e-01
      2897         1   1311340102         157           2898     205880396014         2.058804e-01
     14057         1    975736474         211          14058     205880396014         2.058804e-01
   3107441         1 205880396014           1        3107442     205880396014         2.058804e-01

desired_large_stabilizer_quotients
  stabilizer_size quotient_degree recovery_degree largest_degree_over_sqrt
          3107441           66254         3107441             3.107441e-06
            66254         3107441           66254             3.107441e-06
```

The point of the table is that a small `X0(ell)->X(1)` degree and a useful
split-prime class action do not imply a large stabilizer.  They give edge data
in the CM isogeny graph.  The class group still moves the starting vertex of
the edge, so the edge invariant has a full class orbit up to small modular
symmetries.

The same script verifies this in the small `D=-5000` model:

```text
D=-5000, q=1259, ell=3, h=30
distinct_X0_edge_sums=30
distinct_X0_edge_products=30
distinct_unordered_edges=30
explicit_subgroup_size=5
explicit_quotient_coset_sums=6
```

So a generator-level edge invariant does not automatically quotient by a
subgroup.  The quotient appears only after explicitly forming embedded coset
sums/products, which is the class-orbit computation we were trying to avoid.

Boole independently checked the same question against known Weber/Atkin,
multiple eta-quotient, `X0(N)`, Atkin-Lehner, and Shimura reciprocity class
invariants.  The useful stabilizers from fixed level are bounded by modular
cover/ray data and small Atkin-Lehner or ramified-prime symmetries, not by
arbitrary odd subgroups like `3107441` or `66254`.  No known invariant gives
the desired p24 quotient without embedded orbit sums.

## X1 Tower MITM Cost Audit

I revisited the only non-CM primitive that still has the right flavor:
construct part of the strict `X1(2^40)` condition, say level `2^h` with
`h ~= 20`, then pay the residual tail separately.  This would beat sqrt only
if the level-`2^h` sampler itself costs `o(2^h)`.

I added:

```text
p24/x1_tower_mitm_cost_audit.py
```

Representative run:

```text
python3 p24/x1_tower_mitm_cost_audit.py

ordinary_tower_rejection_split
  h lift_cost_from_X1_16 residual_tail product product_over_2^k product_over_sqrt
  20              65536         1048576     68719476736         1.000000       6.871948e-02
  24            1048576           65536     68719476736         1.000000       6.871948e-02
  28           16777216            4096     68719476736         1.000000       6.871948e-02
  32          268435456             256     68719476736         1.000000       6.871948e-02
  40        68719476736               1     68719476736         1.000000       6.871948e-02
```

Starting from the known cheap `X1(16)` base, rejection through nested quadratic
covers costs `2^(h-4)`, while the remaining tail costs `2^(40-h)`.  The
product is always `2^36`, independent of the split point.  This is a
constant-factor improvement relative to all-`A` search, not an exponent
improvement.

The script also records what a real speedup would require:

```text
Assume a level 2^h sampler costs 2^(beta*(h-4)) from X1(16).
Work exponent is beta*(h-4)+(40-h); beta<1 is required.
```

Balanced meet-in-the-middle over branch words does not provide that by itself.
After `h/2` inverse steps one still has a positive-dimensional family in the
base parameter; making it finite means evaluating over field parameters or
constructing the missing high-degree equations.  The base-parameter subset
sizes are correspondingly bad:

```text
h=20: about p/2^10 = 9.77e8 * sqrt(p)
h=40: about p/2^20 = 9.54e5 * sqrt(p)
```

Heisenberg independently reached the same conclusion: the inverse-doubling
tower has no obvious group/collision structure for a subdensity MITM sampler;
caching and recursive batching change constants, while the log-work slope in
the number of quadratic lift conditions remains about `1`.

I also wrote down the algebraic version of the same barrier:

```text
p24/inverse_tower_intersection_degree_audit.py
```

Representative run:

```text
python3 p24/inverse_tower_intersection_degree_audit.py

split_depths degree_C degree_D bezout_product product_over_sqrt
 4+36             16    68719476736    1099511627776           1.099512
16+24          65536       16777216    1099511627776           1.099512
20+20        1048576        1048576    1099511627776           1.099512
24+16       16777216          65536    1099511627776           1.099512
36+ 4    68719476736             16    1099511627776           1.099512
```

The balanced split has two degree-`1048576` curves in the `(A,x)` plane, but
their intersection/resultant has degree `2^40`, about `1.0995*sqrt(p)`.  Thus
the split reduces the largest individual equation degree but not the total
certificate entropy.

## Odd-Cofactor Orientation Tradeoff

I checked a tempting route based on the clean target group orders.  The third
target order is especially simple:

```text
p + 1 - (-1178414874616) = 2^41 * 454747350887
```

Maybe one could force a large odd cofactor first, leaving only a short
2-primary finish.  The catch is the odd analogue of the `X0`/`X1` gap: an
`X0(m)` condition gives a Frobenius-stable cyclic subgroup, but `m | #E(F_p)`
requires Frobenius to act as `lambda=1` on that subgroup, or dually as
`lambda=p`.  That is an orientation condition of size about `phi(m)/2`.

I added:

```text
p24/odd_cofactor_orientation_tradeoff.py
```

Representative run:

```text
python3 p24/odd_cofactor_orientation_tradeoff.py

selected_odd_divisors
  trace m hasse_traces residual orient_cover orient*residual/sqrt gamma0/sqrt gamma1/sqrt
     -78903246840           21 190476190476 190476190476.000            6              1.142857 3.200000e-11 3.840000e-10
    1020608380936    110429177        36222     36222.000     55214588              1.999983 1.104292e-04 1.219460e+04
     -78903246840  43309271513           93        93.000  21654635756              2.013881 4.330927e-02 1.875693e+09
   -1178414874616 454747350887            8         8.000 227373675443              1.818989 4.547474e-01 2.067952e+11
     -78903246840 909494701773            5         5.000 259855629072              1.299278 1.385897e+00 7.202661e+11

best_by_x0_then_orientation_proxy
  trace=-78903246840 m=21 proxy_over_sqrt=1.142857
  trace=-78903246840 m=909494701773 proxy_over_sqrt=1.299278
  trace=-78903246840 m=3 proxy_over_sqrt=1.333333
```

So large odd cofactors really do shrink the residual Hasse trace count: the
prime `454747350887` leaves only eight possible traces.  But the missing odd
orientation cover has size `227373675443`, and the product is still
`1.818989*sqrt(p)`.  The best row overall is only the small divisor `m=21`,
and even there the proxy remains `1.142857*sqrt(p)`.

This closes the "force the odd cofactor first" version of the target-order
shape.  Odd cofactors are useful after the target isogeny class is known, but
they do not supply a sub-sqrt strict sampler.

## Near-Square D=-7 Seed 23-Coincidence Audit

I added:

```text
p24/near_square_seed_modular_neighbor_audit.py
```

Motivation: the smooth third strict target has

```text
t = -1178414874616
t/2 = -589207437308
n + t/2 = 410792562692 = 2^2 * 23 * 3391 * 1316761
```

and norm `23` generates the target CM class group.  Since `p=n^2+7` also gives
the cheap `D=-7` CM seed `j=-3375`, this raised a concrete question: does the
level-23 modular fiber from the cheap seed expose a target root over `F_p`?

Run:

```text
python3 -m py_compile p24/near_square_seed_modular_neighbor_audit.py
python3 p24/near_square_seed_modular_neighbor_audit.py
```

Key output:

```text
Phi_23_seed_fiber_has_new_Fp_root=0
any_new_odd_Fp_root_for_tested_levels=0
level_2_new_roots_same_D_minus_7_CM_field=(16581375,)
conclusion=the_23_near_square_coincidence_is_only_a_trace_congruence; it_does_not_supply_a_strict_target_root_or_sub_sqrt_certificate
```

The harmless level-2 root is the conductor-2 neighbor in the same
`Q(sqrt(-7))` CM field, so it still has trace `+/-2n` and `v2=3`.  The
tempting `23 | n+t/2` fact does not bridge the cheap near-square CM certificate
to any strict p24 target trace.

## Odd-Character Residual Entropy Scan

Hypatia added:

```text
p24/odd_character_residual_entropy_scan.py
```

This exact tiny-field audit asks whether, after conditioning on the known
Legendre-sign gates, low-order odd multiplicative cosets of low-degree
expressions in `A` and `n` provide stable extra trace-v2 information.

Verification:

```text
python3 -m py_compile p24/odd_character_residual_entropy_scan.py
python3 p24/odd_character_residual_entropy_scan.py
```

Key output:

```text
leave_one_out_summary evaluations=33 median_holdout_lift=1.003 positive_holdout_lifts=17/33 best_holdout_lift=1.720
conclusion=no_nonconstant_odd_character_residual_entropy_reduction_seen
```

So the residual odd-character buckets are row-local classifiers, not a stable
finite-field trace-v2 selector.

## Principal CM Root Torsor Audit

Added:

```text
p24/principal_cm_root_torsor_audit.py
```

This closes a subtle version of the smooth-CM hope: instead of computing an
entire class object, can we reduce the principal complex CM value
`j(tau_O)` modulo the p24 prime?

Toy calibration using `D=-5000`, `q=1259`, and the existing embedded
decomposition setup:

```text
python3 -m py_compile p24/principal_cm_root_torsor_audit.py
python3 p24/principal_cm_root_torsor_audit.py

split_roots_over_Fq=30
horizontal_cycle_length=30
frobenius_action_on_roots=identity
frobenius_fixed_roots=30
possible_principal_root_choices=30
possible_cycle_labelings_with_orientation=60
conclusion=principal_CM_root_reduction_requires_the_same_class_field_embedding_choice_as_selecting_a_root
```

The lesson transfers directly to p24.  The principal norm representation says
the target class polynomial splits completely over `F_p`; it does not choose a
prime of the class field above `p`, equivalently it does not choose one root of
the CM torsor.

## Gross-Zagier / Singular-Moduli Product Sidecar

Hilbert checked whether Gross-Zagier, Lauter-Viray, or small-CM intersection
formulas could turn the cheap `D=-7` seed into a strict p24 root selector.

No files were edited.  The useful no-go is structural:

```text
H_D(-3375) = product over target CM roots r of (-3375 - r)
```

Product/intersection formulas can factor this aggregate norm or determine
intersection multiplicities.  They can say whether a seed collides with some
target CM root modulo a prime, but they do not identify a linear factor
`X-r` or a class-group coordinate for `r`.  At the p24 prime, a collision with
`j=-3375` would force the cheap `Q(sqrt(-7))` curve to also have the strict
large CM field, impossible; locally it has trace `+/-2e12` and `v2=3`.

This reinforces the same distinction as the principal-root torsor audit:
aggregate class-field data does not select a vertex of the split CM torsor.

## Odd Target-Factor Chain Sidecar

Archimedes checked whether the prime-factor chain in the strict target orders
could be a recursive shortcut.  No files were edited.

The exact arithmetic is:

```text
(p+1-t_i)/2^40 = 909494701772, 909494701773, 909494701774
909494701774 = 2 * 454747350887
454747350887 - 1 = 2 * 29 * 71 * 110429177
```

So the chain is real but comes from adjacent trace lifts.  It certifies or
organizes cofactors once a curve in the target isogeny class exists.  It does
not select that curve.  Recursive ECPP, cyclotomic characters, and
`q`-isogeny interpretations all run back into the same obstruction:
`X0(q)` is an unoriented cyclic-subgroup condition, while `q | #E(F_p)`
requires the Frobenius eigenvalue orientation `lambda=1` or its dual.  For the
large prime `454747350887`, the residual trace count is only eight, but the
orientation cover is `(q-1)/2 = 227373675443`, giving the already-recorded
`1.818989*sqrt(p)` proxy.

## Second-Order Linear Inverse-Chain Audit

Added:

```text
p24/linear_recurrence_inverse_chain_audit.py
```

This checks a Chebyshev/Lucas-style hidden-torus ansatz for the universal
2-torsion terminal branch:

```text
x_0 = 0
x_1 = 1
x_{i+1} = a*x_i + b*x_{i-1}
```

For a valid inverse halving chain, the edge-determined Montgomery parameter
`A(x_i,x_{i-1})` must be independent of `i`.  The first compatibility
equations through depth 6 have no common one-parameter component:

```text
python3 -m py_compile p24/linear_recurrence_inverse_chain_audit.py
python3 p24/linear_recurrence_inverse_chain_audit.py

gcd_over_Q=1
gcd_over_Fp24_total_degree=0
gcd_over_Fp24=1
p24_resultant_gcd=a*(a - 1)**9
p24_isolated_first_three_compatibilities_only_degenerate=1
conclusion=second_order_linear_Chebyshev_Lucas_inverse_chain_section_does_not_exist
```

This closes the natural Lucas/Chebyshev recurrence shape as a nonsingular
inverse-chain section.  The p24 resultant check also rules out nondegenerate
isolated solutions to the first three compatibility equations in this ansatz.

## Explicit Halving / CM-Ray Combination Sidecars

Newton checked the classical halving-chain route from the Montgomery
2-torsion point `T=(0,0)`.  The first levels are genuinely explicit:

```text
2Q = T  =>  x(Q)=1 with y^2=A+2, or x(Q)=-1 with y^2=A-2
```

and on the `x=1` branch:

```text
A = ((u^2 - 1)^2 - 4u(u^2 + 1)) / (4u^2)
A + 2 = (u - 1)^4 / (4u^2)
```

But extending this to a full 39-step halving chain is exactly a marked
`X1(2^40)/±` point.  The Landen/Legendre view supplies `X0` isogeny-chain
data until the branch choices orient a Frobenius-fixed ray; for p24 the same
four-eigenvalue / two-strict-orientation barrier reappears.

Mencius checked the combined CM + strict ray-class route.  I turned the degree
calculation into:

```text
p24/cm_ray_class_orientation_degree_audit.py
```

Verification:

```text
python3 -m py_compile p24/cm_ray_class_orientation_degree_audit.py
python3 p24/cm_ray_class_orientation_degree_audit.py
```

Key output:

```text
x_only_orientation_cover=2^(k-2)=274877906944
t= 1020608380936  ray_degree/sqrt = 7.661774e+10
t=  -78903246840  ray_degree/sqrt = 2.289830e+11
t=-1178414874616  ray_degree/sqrt = 5.659197e+10
marked_quotient_degree_over_sqrt=1.821176e+04
conclusion=combining_CM_with_the_strict_2^40_ray_restores_the_orientation_cover_and_does_not_beat_sqrt
```

Thus ring-class `j` alone is smaller but unmarked, while a torsion/ray
invariant that marks the verifier's `x` includes the huge `2^38` orientation
cover.

## Higher-Order Jacobi / Hypergeometric Trace Barrier

Added:

```text
p24/jacobi_sum_cm_field_barrier.py
```

This addresses a broader version of the cyclotomic thought: maybe a
higher-order multiplicative character or hypergeometric trace identity can
produce one of the strict traces even though the cheap quadratic subfields do
not.

For an elliptic curve, any Jacobi-sum trace still generates the quadratic
CM field `Q(sqrt(t^2-4p))`.  A base-field character needs that conductor in
`p-1`; a unitary `F_{p^2}` character needs it in `p+1` or at least `p^2-1`;
a small-extension shortcut needs it in `p^f-1` for small `f`.

Verification:

```text
python3 -m py_compile p24/jacobi_sum_cm_field_barrier.py
python3 p24/jacobi_sum_cm_field_barrier.py
```

Key output:

```text
t= 1020608380936  gcd(conductor,p-1)=29  gcd(conductor,p+1)=1  first_f_le_64=none
t=  -78903246840  gcd(conductor,p-1)=7   gcd(conductor,p+1)=1  first_f_le_64=none
t=-1178414874616  gcd(conductor,p-1)=1   gcd(conductor,p+1)=1  first_f_le_64=none
conclusion=higher_order_jacobi_or_hypergeometric_identities_do_not_supply_a_cheap_strict_p24_trace
```

Thus higher-order character formulas do not bypass the large target quadratic
CM fields; at most they see the already-recorded genus factors.

## Fixed-Field Prescribed-Trace Algorithm Sidecar

Hume checked whether a known fixed-field exact-trace construction avoids the
large-discriminant CM/root-selection problem.  No files were edited.

The distinctions are:

```text
variable-field prescribed-order algorithms:
  choose the field/discriminant, so they do not apply once p is fixed

flexible divisor/subgroup algorithms:
  construct torsion/divisibility constraints, not the exact DANGER trace;
  p24's m=2^40 is also far outside the fixed-field theorem range

exact fixed-trace construction:
  standard route is CM for Q(sqrt(t^2-4p)), then root selection for H_D mod p
```

For p24, fixing `p` and any strict target order fixes `t` and
`Delta=t^2-4p`.  The existing audit shows the target fundamental
discriminants have `|D_K|/p` about `0.65..1.00` and conductor only `2`, so
there is no small-discriminant exact-trace shortcut analogous to the
non-strict `D=-7` near-square certificate.

Conclusion: no known fixed-field prescribed-trace theorem supplies the missing
strict p24 curve.  A new odd-part class/root selector would still be required.

## Exact Trace-Residue Oracle Tradeoff

Added:

```text
p24/exact_trace_residue_oracle_tradeoff.py
```

This closes a generous version of a possible reverse-SEA shortcut: suppose an
oracle can impose the exact union of the six strict target trace residues
modulo a level `N`, and charge only the `Gamma0(N)` modular index, even though
exact trace residues are richer than bare `X0(N)` data.  The remaining work is
the number of Hasse trace lifts that survive the residue oracle.

Verification:

```text
python3 -m py_compile p24/exact_trace_residue_oracle_tradeoff.py
python3 p24/exact_trace_residue_oracle_tradeoff.py
```

Key output:

```text
2^40  gamma0/sqrt=1.649267  target_residues=2  survivors=6  oracle_proxy/sqrt=1.649267
2^36  gamma0/sqrt=0.103079  target_residues=2  survivors=116 oracle_proxy/sqrt=1.992865
odd_prime_cofactor  gamma0/sqrt=0.454747 survivors=52 oracle_proxy/sqrt=3.941144
conclusion=unoriented_exact_trace_residue_construction_trades_constants_but_not_the_sqrt_exponent
```

So even an optimistic exact-residue construction only moves constants: lower
levels leave proportionally more Hasse lifts, while levels that isolate the
target traces cost `Theta(sqrt(p))`.

## Waterhouse/Mestre And Fixed-Trace Existence Theorems

Added:

```text
p24/waterhouse_mestre_fixed_trace_barrier.py
```

This closes a terminology trap.  Waterhouse/Rueck/Voloch give existence and
group-structure criteria, and Tate says fixed trace is the same as fixed
elliptic isogeny class over `F_p`.  But the constructive prescribed-subgroup
route in the local Sutherland/Shparlinski paper still proceeds by CM:
compute `H_D`, find a root modulo `p`, and choose the correct twist.  The
Mestre/Cremona-Sutherland "trick" referenced in finite-field software is a
point-counting aid, not a selector for a prescribed fixed trace.

Verification:

```text
python3 -m py_compile p24/waterhouse_mestre_fixed_trace_barrier.py
python3 p24/waterhouse_mestre_fixed_trace_barrier.py
```

Key output:

```text
abs_trace=1020608380936
  fundamental_D=-739589633190799177940983
  class_number_degree_H_D=278733727154
  class_number_over_sqrt=0.278734

abs_trace=78903246840
  fundamental_D=-998443569409526507503607
  class_number_degree_H_D=833035208344
  class_number_over_sqrt=0.833035

abs_trace=1178414874616
  fundamental_D=-652834595820939249713143
  class_number_degree_H_D=205880396014
  class_number_over_sqrt=0.205880

conclusion=Waterhouse_Rueck_Voloch_and_Mestre_do_not_bypass_the_large_CM_root_selector_for_strict_p24
```

So existence theorems do not supply the missing `(A,x0)`.  They certify that
the target isogeny classes exist; constructing an explicit representative is
the same large CM-root problem already tracked.

## Higher-Dimensional Factor Routes

Added:

```text
p24/higher_dimensional_factor_route_audit.md
```

Halley audited genus-2/Jacobian, abelian-surface, product/gluing, and Weil
restriction escape hatches.  The short version is that any construction whose
Jacobian or abelian variety contains the strict elliptic factor has already
encoded the same target elliptic isogeny class.  A simple primitive quartic CM
surface has no elliptic `F_p` factor; a split surface with the target factor
contains the large target quadratic CM field; and Weil restriction/descent
does not shrink the field because

```text
T_m^2 - 4*p^m = (t^2 - 4*p) * U_{m-1}(t,p)^2.
```

The local `p24/extension_trace_cm_audit.py` verifies this square-factor
identity.  Thus higher-dimensional wrappers do not produce a strict p24
elliptic curve without the same target `j` selector.

## Public Search Refresh

Updated:

```text
p24/public_lead_scan_20260604.md
```

The public sidecar checked the official DANGER3 repository, Ruehle's repo,
Alexa's fork, the p23 PR, GitHub code/issue/commit searches, and exact p24
integer web searches.  No verifier-compatible p24 triple or public
asymptotic strict-DANGER shortcut was found.  The strongest public practical
lead remains the p23 `X1(16)` nonsplit/halving method, which the public README
characterizes as a constant-factor improvement, not an asymptotic sub-sqrt
construction.

## Smooth Class Quotient-Invariant Refresh

Updated:

```text
p24/smooth_class_tower_route_note.md
```

James rechecked the smooth third target against explicit quotient class
invariants and decomposed/tower CM.  The sharp obstruction is not the abstract
existence of a quotient field; it is embedding.  Sutherland's decomposed CM
method can choose `G <= Cl(O)`, build a fixed-field polynomial of degree
`m=h/|G|`, and recover `j` with a degree-`|G|` polynomial, but the method must
enumerate the `G`-orbits of CM roots.  Directly modulo p24 this needs a seed
target CM root; via CRT, known methods enumerate CM roots over auxiliary
splitting primes and still pay the large-discriminant class-object cost.

For the best visible third-target split:

```text
h = 205880396014 = 66254 * 3107441
sqrt(h) ~= 453740
```

the quotient degree `66254` is attractive, but generic recovery degree
`3107441` is already above `sqrt(h)`, and constructing the embedded quotient
object is not known to be sub-sqrt.  Special class invariants such as Weber,
eta quotients, Atkin invariants, and generalized class polynomials reduce
heights or special ramified/Atkin-Lehner degrees; they do not give arbitrary
fixed class-group quotients with cheap `j` recovery.

So this remains the most structured live lead, but still lacks the missing
primitive:

```text
an explicit orbit-symmetric embedded odd quotient invariant, plus a small
recovery relation to j, computable at p24 without enumerating the target CM
torsor.
```

## Reverse Canonical-Lift / 2-Adic Deformation Sidecar

Added:

```text
p24/reverse_canonical_lift_barrier.md
```

Socrates checked whether Satoh/AGM/canonical-lift or Serre-Tate deformation
machinery can be inverted to prescribe the Frobenius eigenvalue
`lambda == 1 mod 2^40` over the fixed p24 field.  It does not give an
independent selector.  Satoh/AGM starts from an ordinary curve and computes
its trace; Serre-Tate coordinates are local around a curve already chosen
modulo `p`; and the prime-to-p `2`-adic condition is exactly the discrete
trace congruence already recorded.

For p24, prescribing the eigenvalue leaves the same six Hasse traces.  Once
`p` and `t` are fixed, Waterhouse/Tate put us in one ordinary isogeny class,
and solving the reverse equations asks for an endomorphism

```text
pi^2 - t*pi + p = 0,
```

which is the CM/Heegner locus of discriminant `t^2-4p`.  The near-square
identity `p=n^2+7` gives only the `D=-7`, trace `+/-2n`, depth-3 curves.

Conclusion: reverse canonical lifting is another language for the same fixed
trace CM/class-root problem, not a sub-sqrt p24 construction.

## Near-Square Small-Family Formula Rerun

I reran three exact small-field probes using the bundled Python with NumPy:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 10000 --max-p 400000 --max-rows 24 --coeff-bound 6 --top 8

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/near_square_formula_probe.py --min-p 10000 --max-p 400000 --max-rows 24 --coeff-bound 6 --j-parameter --top 8

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/legendre_near_square_parameter_probe.py --min-p 10000 --max-p 400000 --max-rows 18 --coeff-bound 6 --mode landen --n-modulus 8 --n-residue 0 --top 8
```

Key outputs:

```text
A-line LFTs:
  row 1 survivors=1390
  row 2 survivors=108
  row 3 survivors=6
  row 4 survivors=0
  conclusion=no_low_height_LFT_formula

j-line LFTs:
  row 1 survivors=432
  row 2 survivors=7
  row 3 survivors=1
  row 4 survivors=0
  conclusion=no_low_height_LFT_formula

Landen-coordinate LFTs:
  row 1 survivors=500
  row 2 survivors=20
  row 3 survivors=0
  conclusion=no_low_height_legendre_parameter_formula
```

The top formulas have a handful of hits over all rows, consistent with random
bucket density.  This does not prove no near-square identity exists, but it
continues to rule out the low-height rational sections that would be visible
at small scale.

## Statistical / Probability Lift Baselines

Added:

```text
p24/mixed_crt_trace_residue_optimizer.py
p24/statistical_lift_baselines.md
```

The mixed CRT optimizer searches generous exact trace-residue oracle levels

```text
N = 2^d * R
```

with `R` a squarefree product of small odd primes.  It counts Hasse survivors
by arithmetic progressions rather than enumerating trace lattices.

Verification:

```text
python3 -m py_compile p24/mixed_crt_trace_residue_optimizer.py
python3 p24/mixed_crt_trace_residue_optimizer.py --prime-bound 47 --max-odd-part 20000 --min-depth 28 --max-depth 42 --top 30
```

Key output:

```text
rank depth odd_part level/sqrt gamma0/sqrt residues survivors proxy/sqrt
   1    40        1   1.099512    1.649267        2         6    1.649267

conclusion=mixed_crt_trace_residue_levels_do_not_change_the_sqrt_exponent
```

So even when exact trace residues are granted as a stronger-than-`X0` oracle,
mixed small odd CRT information does not beat the pure `2^40` constant in the
tested window.  The reason is arithmetic: `2^40` keeps the three curve-side
target traces collided and the three twist-side traces collided; adding odd
residue information separates that progression and worsens constants.

I also reran exact small-field statistical baselines with the bundled Python:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py \
  --min-p 100000 --max-p 1000000 --max-rows 10 --n-modulus 8 --n-residue 0 --fit-min-depth 5

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/low_degree_character_trace_scan.py \
  --min-p 10000 --max-p 180000 --max-rows 10 --coeff-bound 2 \
  --n-modulus 8 --n-residue 0 --top 8

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/dyadic_parameter_residue_audit.py \
  --min-p 10000 --max-p 250000 --max-rows 10 --max-bits 10 \
  --n-modulus 8 --n-residue 0 --top 8
```

Key outputs:

```text
aggregate_fitted_beta_x1=1.038291
best_aggregate_lift=1.485000
j bits=10 best_lift=3.351 capture=0.0029
```

Thus partial oriented depth behaves like beta-one rejection at larger small
rows; cheap low-degree character labels give constant lift; and dyadic buckets
trade lift against collapsing capture.

Huygens audited multilevel splitting, SMC, cross-entropy, and importance
sampling.  The resulting bar for a productive probability method is:

```text
1. an oriented-depth sampler with cost 2^(beta h), beta < 1;
2. a cheap score whose holdout log2(lift) grows linearly with depth while
   capture stays non-negligible;
3. a transition kernel on partial-depth states with real drift toward deeper
   oriented depth without knowing the next Frobenius bit.
```

No local probability/statistics artifact currently meets that bar.  The
existing techniques move entropy around and improve constants; they do not
remove the target trace/orientation entropy.

Linnaeus separately checked trace-distribution, character-sum, random-matrix,
and equidistribution tools.  The six signed p24 traces have discrete
Sato-Tate mass about `1.70e-12`, giving a naive trace-level expected search of
about `5.89e11`, still square-root scale.  This matches the local exact scans:
constant classifiers such as `A±2`, split/nonsplit, fixed `X1(16)`,
low-degree characters, and small residue/coset buckets can help calibration,
but an exponent-changing selector needs about `epsilon*log(p)` growing bits
while retaining the target traces and costing less than the search saved.

Known sources of growing bits are growing modular level, SEA trace residues,
or CM/class-field root selection.  The p24 audits put all three back at
sqrt-scale or worse.  Thus probability/equidistribution describes the rarity
of the target; it does not name the rare Montgomery `A`.

Rawls checked probability algorithms on the smooth third target class group:
Pollard rho, birthday methods, hidden shift, random self-reducibility,
class-group random walks, expander mixing, horizontal isogeny cycles, and
probabilistic root selection over split class polynomials.

I added:

```text
p24/class_group_probability_audit.py
```

Verification:

```text
python3 -m py_compile p24/class_group_probability_audit.py
python3 p24/class_group_probability_audit.py
```

Key output:

```text
trace=-1178414874616
  h=205880396014
  sqrt_h=453740.450
  best_decomposed_degrees=66254*3107441

oracle_separation
  seeded_embedded_root_available -> already have a CM j root; certificate tail is cheap
  embedded_class_action_oracle_available -> Pollard/hidden-shift costs about sqrt(h)
  abstract_class_group_only -> samples labels, not Fp j-values
  split_H_D_polynomial_available -> output/input size already degree h
  no_seed_no_embedded_invariant -> random walk has no Fp state space to walk
```

Conclusion: class-group probability methods are potentially sub-`sqrt(p)` only
after the missing embedded root/class-action oracle exists.  They do not turn
the abstract smooth class group into a seedless p24 `j` root.

## Upstream DANGER3 Dataset Audit

The user pointed out that Andrew Sutherland's upstream DANGER3 repo has more
small-prime data than the local p22/p23 result artifacts.  I cloned it into:

```text
p24/upstream_DANGER3/
```

and added reproducible audits:

```text
p24/upstream_dataset_feature_audit.py
p24/upstream_prefix_character_scan.py
p24/upstream_terminal_branch_audit.py
p24/upstream_dataset_experiment_audit.md
```

Verification:

```text
python3 -m py_compile p24/upstream_dataset_feature_audit.py
python3 -m py_compile p24/upstream_prefix_character_scan.py
python3 -m py_compile p24/upstream_terminal_branch_audit.py
python3 p24/upstream_dataset_feature_audit.py
python3 p24/upstream_prefix_character_scan.py --min-p 32768 --max-p 65536 --top 8
python3 p24/upstream_prefix_character_scan.py --min-p 32768 --max-p 65536 --residue 7 --top 8
python3 p24/upstream_terminal_branch_audit.py --residue 7 --tail-threshold 2048
```

Dataset facts:

```text
pp12.txt.gz   all triples through 2^12
pp16A.txt.gz  all distinct successful (p,A) prefixes through 2^16
pp24.txt.gz   one witness triple per prime through 2^24
```

The one-per-prime `pp24` witnesses are highly biased:

```text
rows=1077869
split_counts={-1: 1074967, 1: 2902}
terminal_counts={'quadratic_root': 1464, 'zero_root': 1076405}
```

but this is witness-selection bias.  The all-prefix dataset is much closer to
balanced:

```text
prefix_split_counts={-1: 2641160, 1: 2071909}
```

The all-prefix density remains square-root scale.  Grouping by the number of
target orders in the Hasse window gives bounded constants:

```text
target_orders=1 mean_good_A_over_sqrt=2.048154
target_orders=2 mean_good_A_over_sqrt=3.634469
target_orders=3 mean_good_A_over_sqrt=5.206613
target_orders=4 mean_good_A_over_sqrt=6.023870
```

The strongest cheap character signal in the p24-relevant `p % 8 == 7` slice is
only a terminal-branch constant:

```text
feature=A-2 best_sign=-1 capture=0.748937 approx_lift=1.497874
feature=A+2 best_sign=+1 capture=0.748937 approx_lift=1.497874
```

The terminal audit explains this by the fixed sign-pattern mixture

```text
(chi(A+2), chi(A-2), chi(A^2-4))
( 1, -1, -1): 10030
(-1, -1,  1):  5374
( 1,  1,  1):  5374
```

so it is useful orientation information, not a depth-growing selector.  Other
fixed low-degree Legendre labels have holdout lifts essentially `1.00`.

I also checked whether upstream one-witness triples hide a deterministic
inverse-halving recipe.  Streaming `pp24` and inspecting the last x-only states
gave:

```text
(+1, 0, infinity): 538616
(-1, 0, infinity): 537789
(other, other, infinity): 1464
```

The penultimate zero branch is essentially balanced between `+1` and `-1`;
there is no tiny fixed branch code visible.

Subagents independently reached the same conclusion from p22/p23 plus upstream
data: the robust theorem-shaped lesson is the known nonsplit cyclic 2-Sylow
one:

```text
If chi(A^2-4)=-1, the rational 2-Sylow is cyclic.  For an X1(16) marked point,
first-branch halving survives to depth d iff v2(#E(Fp)) >= d.
```

That explains the p23 constant-factor speedup.  The upstream data does not
expose an asymptotic p24 selector; it strengthens the requirement that any new
method provide growing trace/orientation bits at sub-growing cost.

## Smooth Class Kummer / Radical Audit

I revisited the third target's smooth class group:

```text
trace = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
```

The smoothness suggests a solvable/radical class-field tower.  I added:

```text
p24/smooth_class_kummer_feasibility_audit.py
```

Verification:

```text
python3 -m py_compile p24/smooth_class_kummer_feasibility_audit.py
python3 p24/smooth_class_kummer_feasibility_audit.py
```

Key output:

```text
cyclic_factor_kummer_table
  ell divides_p_minus_1 p_mod_ell ord_p_mod_ell extension_degree_for_zeta ell_times_ord over_sqrt
       157 False               21           156                       156         24492 2.449200e-08
       211 False              114            35                        35          7385 7.385000e-09
   3107441 False          2509452        388430                    388430 1207023307630 1.207023e+00
   oddpart False        27978800775      30297540                  30297540 3118834766725002780 3.118835e+06

field_interaction_gcds
  p-1              gcd_with_h=2
  p+1              gcd_with_h=2
  curve_odd_order  gcd_with_h=1
  abs_DK           gcd_with_h=1
```

So the class group is smooth, but the odd class factors do not divide `p-1`;
direct Kummer radicals over `F_p` are not available.  The large factor would
require adjoining roots of unity over an extension of degree `388430`; the
full odd part has root-of-unity extension degree `30297540`.  Even ignoring
that, the missing object remains the same: explicit embedded
subfield/relative polynomials with a recovery map to the CM `j` root.  The
abstract smooth class group alone does not supply a seedless root selector.

Toy `D=-5000,h=30` checks continue to calibrate the obstruction:

```text
p24/embedded_decomposition_calibration.py
p24/principal_cm_root_torsor_audit.py
```

Once all embedded roots and a seed cycle are available, subgroup decomposition
reduces degrees (`30 -> 6 and 5`).  But Frobenius fixes every root over a
completely split prime, and any root can be labeled principal after rotating
the abstract class-group coordinate.  This is exactly the p24 missing
embedding choice in miniature.

## Trace Lattice And Split-2 Orientation Audits

I made the exact `n=10^12`, `M=2^40` trace-lattice arithmetic reproducible:

```text
p24/trace_lattice_relation_audit.py
```

Verification:

```text
python3 -m py_compile p24/trace_lattice_relation_audit.py
python3 p24/trace_lattice_relation_audit.py --linear-bound 64 --quadratic-bound 12
```

Key output:

```text
floor((p+1)/M)=909494701772
(p+1)_mod_M=1020608380936

offset=0 trace=1020608380936   order_div_M=909494701772
offset=1 trace=-78903246840    order_div_M=909494701773
offset=2 trace=-1178414874616  order_div_M=909494701774

best_trace_linear_relations value ~= a*n+b*M
  offset=0 score=1073491976 a=45 b=-40 residual=1073491976
  offset=1 score=1073491976 a=45 b=-41 residual=1073491976
  offset=2 score=1073491976 a=45 b=-42 residual=1073491976
```

The shared approximation

```text
t_j = 45*n - (40+j)*2^40 + 1073491976
```

is an arithmetic curiosity of this fixed lattice, not a small exact trace
formula.  A small-coefficient quadratic search in `n` and `M` for the
fundamental discriminants also left residuals of size about `8.8e20` to
`1.5e21`, so no visible low-height near-square identity emerged.

I also connected the strict 2-adic condition directly to the split ideal above
`2` in the target CM fields:

```text
p24/split2_strict_orientation_relation_audit.py
```

Verification:

```text
python3 -m py_compile p24/split2_strict_orientation_relation_audit.py
python3 p24/split2_strict_orientation_relation_audit.py
```

Key output:

```text
2_adic_eigenvalue_roots_for_target_trace_residue
  lambda=1             ... strict_orientation=True
  lambda=470852567047 ... strict_orientation=False
  lambda=549755813889 ... strict_orientation=False
  lambda=1020608380935 ... strict_orientation=True

target_split2_class_orders
trace=1020608380936   split2_order=278733727154 order_of_split2^40=139366863577
trace=-78903246840    split2_order=208258802086 order_of_split2^40=104129401043
trace=-1178414874616  split2_order=102940198007 order_of_split2^40=102940198007
```

So even though the strict eigenvalue root modulo `2^40` is known exactly, the
corresponding split-2 ideal class and its 40th power still have huge order in
the class group.  The 2-adic congruence is a ray/orientation condition, not a
seed CM-root selector.

## Atkin-Lehner / Fricke Quotient Limit Audit

I made explicit another modular-invariant loophole: perhaps a Fricke or
Atkin-Lehner quotient of `X0(N)` gives the desired smooth odd class quotient
without building orbit sums.  I added:

```text
p24/atkin_lehner_quotient_limit_audit.py
```

Verification:

```text
python3 -m py_compile p24/atkin_lehner_quotient_limit_audit.py
python3 p24/atkin_lehner_quotient_limit_audit.py
python3 p24/class_invariant_stabilizer_audit.py
python3 p24/intermediate_diamond_quotient_audit.py
```

Key output:

```text
level split gamma0_index full_AL_size quotient_degree_lb quotient_degree_over_sqrt
23                 1           24      2              12    1.200000e-11
3107441            1      3107442      2         1553721    1.553721e-06
157*211            1        33496      4            8374    8.374000e-09
157*211*3107441    1 104086877232      8     13010859654    1.301086e-02
```

The full Atkin-Lehner group saves only `2^omega(N)`.  That can improve
constants and coefficient heights, and for the huge composite odd-part level
the quotient degree is below `sqrt(p)` for this fixed p24 instance.  But this
is not the required large class-subgroup stabilizer:

```text
desired stabilizer 3107441 -> quotient degree 66254
desired stabilizer 66254   -> quotient degree 3107441
```

A normalizer quotient is not the same as a chosen smooth class subgroup.
The toy `D=-5000,h=30` calibration remains decisive: generator-level `X0(3)`
edge sums/products have 30 distinct values, while the degree-6 quotient appears
only after explicitly taking embedded coset sums using the root cycle.  Thus
Atkin-Lehner/Fricke invariants are useful fixed modular symmetries, not a
seedless construction of the arbitrary odd class-field quotient needed here.

## Upstream Good-A Projection Compression Audit

I tested whether Sutherland's exact all-good prefix dataset `pp16A.txt.gz`
compresses under natural Montgomery projections.  If a hidden constructive
invariant existed at low degree, the image of the good `A` set might have
growing fibers instead of the constant fibers expected from maps like
`A -> A^2` or `A -> j`.

I added:

```text
p24/upstream_goodA_projection_compression_audit.py
```

Verification:

```text
python3 -m py_compile p24/upstream_goodA_projection_compression_audit.py
python3 p24/upstream_goodA_projection_compression_audit.py --min-p 32768 --max-p 65536
python3 p24/upstream_goodA_projection_compression_audit.py --min-p 32768 --max-p 65536 --residue 7
```

Upper-half `pp16A` results:

```text
projection              mean_image/good  mean_max_fiber  mean_image/sqrt
A                       1.000000         1.000           4.593308
A2                      0.500008         2.000           2.296671
j                       0.412053         4.300           1.837803
terminal_ratio          1.000000         1.000           4.593308
terminal_ratio_signed   0.500008         2.000           2.296671
terminal_sign_pair      0.003876       439.567           0.015126
```

p24 congruence slice `p % 8 == 7`:

```text
projection              mean_image/good  mean_max_fiber  mean_image/sqrt
A                       1.000000         1.000           5.078520
A2                      0.500033         2.000           2.539328
j                       0.381146         3.935           1.902107
terminal_ratio          1.000000         1.000           5.078520
terminal_ratio_signed   0.500033         2.000           2.539328
terminal_sign_pair      0.003117       546.608           0.013498
```

Thus the useful projections have only bounded fibers: sign/A2 gives degree 2,
`j` gives a small constant-degree quotient, and terminal sign-pairs are just
the fixed branch buckets already explained by the upstream dataset audit.  No
natural projection tested here compresses the strict good-`A` set by a growing
factor.

## Upstream One-Witness Selection Audit

I also checked whether Sutherland's one-triple-per-prime files expose a
deterministic low-complexity selector.  If `pp20` or `pp24` always chose a
low-rank triple among all triples for the same prime, that rule might be a
constructive clue.

I added:

```text
p24/upstream_witness_selection_audit.py
```

Verification:

```text
python3 -m py_compile p24/upstream_witness_selection_audit.py
python3 p24/upstream_witness_selection_audit.py --max-p 4096 --top 10
```

On the `pp12` all-triple overlap:

```text
overlap_primes=560
terminal_counts={'quadratic': 29, 'zero': 531}
split_counts={-1: 507, 1: 53}
first_lexicographic_triple=2/560
first_good_A=16/560
first_x_for_selected_A=32/560
last_x_for_selected_A=36/560
mean_triple_rank_quantile=0.500923
mean_A_rank_quantile=0.499635
mean_x_rank_for_A_quantile=0.495521
```

So the witnesses are not first triples, first good `A` values, or first `x`
values for their selected `A`; their ranks are centered at about `1/2`.  They
do show the same constant nonsplit/zero-terminal bias already seen in the
larger `pp24` file.

Data hygiene note: `pp20` and `pp24` contain two small witnesses accepted by
`vpp.py` but absent from `pp12`/`pp10` all-triple files:

```text
(13, 12, 11)
(479, 401, 274)
```

Both pass the upstream verifier.  This appears to be an upstream dataset
inconsistency and does not affect the rank conclusion.

## Larger Upstream One-Witness Streams

The upstream DANGER3 README links one-witness archives beyond the local clone:

```text
pp28.txt.gz
pp30.txt.gz
pp32.txt.gz
```

I added and/or integrated:

```text
p24/upstream_large_one_witness_stream_audit.py
p24/upstream_large_one_witness_audit.py
p24/upstream_large_one_witness_audit.md
p24/upstream_nearsquare_prefix_gate_audit.py
p24/upstream_dataset_experiment_audit.md
```

Key results:

```text
pp28 rows=14630841
max_p=268435399
target_order_count_hist={1: 14366, 2: 3603724, 3: 7293053, 4: 3719698}
reservoir_split_counts={-1: 19992, 1: 8}
reservoir_terminal_counts={'quadratic_root': 4, 'zero_root': 19996}
```

Independent side audit confirmed that local `pp24` is exactly the prefix of
`pp28`, `pp30`, and `pp32`, and that the first `1,300,000` rows are identical
across the three larger archives.  The files are ordered extensions from the
same one-witness generator.

For the closest p24-shaped small family, `p=n^2+7` with `n == 0 mod 8`, the
one-witness representatives are completely in the fixed gate:

```text
pp24 analogue rows=142
gate_counts={(1, -1, -1): 142}
pp28 analogue rows=460
gate_counts={(1, -1, -1): 460}
```

But the full all-prefix `pp16A` slice shows that this is a representative
selection artifact, not a theorem about all good `A` values:

```text
upper-half pp16A near-square rows:
prime_rows=6
good_A_rows=7456
gate_total=(-1, -1, 1):1888,(1, -1, -1):3680,(1, 1, 1):1888
dominant_gate_capture=0.493562

target_orders=3 total=5398
dominant_gate=(1, -1, -1)
capture=0.483512
```

Thus the larger upstream data gives a strong fixed branch/generator signal,
but not a growing-depth selector for the p24 certificate.

## Inverse-Chain MITM Entropy

I consolidated the inverse-halving meet-in-the-middle obstruction in:

```text
p24/inverse_chain_state_entropy_audit.md
```

Runs:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 p24/inverse_chain_mitm_tradeoff_audit.py --min-p 10000 --max-p 80000 --max-rows 4 --depths 2 3 4 5 6 7 8 10 12
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 p24/inverse_mitm_scaling_audit.py --min-p 2000 --max-p 30000 --max-rows 4 --prefix-fracs 0.005 0.01 0.02 0.05 0.10 0.25
python3 p24/inverse_tower_intersection_degree_audit.py
```

Exact small-field calibration shows that partial depth and residual rarity
are reciprocal:

```text
h total full x1_partial x1_residual x1_product
2 84628 3026 84628 0.03575649 27.966953
4 84628 3026 31728 0.09537317 27.966953
6 84628 3026 10242 0.29545011 27.966953
8 84628 3026 3026 1.00000000 27.966953
```

For p24, every algebraic split has the same product:

```text
20+20 degree_C=1048576 degree_D=1048576
Bezout_product=2^40=1099511627776
2^40/sqrt(p)=1.099512
```

So inverse-chain MITM can lower the largest single degree, but it does not
remove the 40 bits of orientation entropy without an additional structure such
as a growing-depth section of `X1(2^d)`.

## Full Small-Triple x0 / Halving-Word Audit

Pascal audited the upstream full-triple files locally through `pp12` and
returned bounded findings from `pp10`/`pp12` rather than waiting on the huge
remote `pp14` stream.  Files added:

```text
p24/full_small_triple_halving_audit.py
p24/full_small_triple_x0_invariant_audit.py
p24/full_small_triple_pp10_audit.txt
p24/full_small_triple_pp12_audit.txt
p24/full_small_triple_pp12_p7_tail_audit.txt
```

Compile check:

```text
python3 -m py_compile p24/upstream_full_triple_stream_audit.py p24/full_small_triple_halving_audit.py p24/full_small_triple_x0_invariant_audit.py
```

Exact `pp12`:

```text
rows=3083880
distinct_prefixes=80263
x_per_A_quantiles_10_25_50_75_90_99=16,16,32,32,64,128
symmetry_closure_rates=reciprocal:1.000000 negA_negx:1.000000 orbit4:1.000000
```

So full triples have exact reciprocal and `(A,x)->(-A,-x)` symmetries, but
only as a constant quotient.  x-specific low-degree characters are balanced:

```text
all pp12:
  A+2 capture=0.664848
  A^2-4 capture=0.662931
  x, x±1, x+1/x, A*x±1 around 0.50

p % 8 == 7, p >= 2048:
  A±2 capture=0.670996
  x-specific characters around 0.50
```

The inverse branch words show uniform entropy after terminal degeneracy:

```text
all pp12 four-symbol prefix best captures:
0.335258, 0.084645, 0.021237, 0.005468, 0.001430, 0.000372

p % 8 == 7 tail:
0.335498, 0.087114, 0.022275, 0.005656, 0.001570, 0.000436
```

This independently reinforces that inverse-halving branches do not expose a
growing selector in the available full-triple data.

## Target Cofactor Embedding Audit

I checked one more constructive-order loophole: the third target has prime
odd cofactor after the large 2-power,

```text
#E = 2^41 * 454747350887.
```

If that cofactor, or the other large target cofactors, had small embedding
degree relative to `p`, an MNT/pairing-friendly style construction might have
been visible.  I added:

```text
p24/target_cofactor_embedding_audit.py
```

Run:

```text
python3 -m py_compile p24/target_cofactor_embedding_audit.py
python3 p24/target_cofactor_embedding_audit.py
```

Key large factors:

```text
trace=1020608380936:
  r=110429177 embedding_degree=110429176

trace=-78903246840:
  r=43309271513 embedding_degree=1665741212

trace=-1178414874616:
  r=454747350887 embedding_degree=454747350886
```

Some twist-side cofactors have embedding degree fractions like `r/5` or
`r/2`, but they are not on the strict high-2-power side and are still enormous.
Thus the prime-cofactor shape is useful after a curve exists, but does not
provide a fixed-field pairing-friendly or MNT-style constructor.

## Independent Constructive-Theorem Sweep

Nash did a final independent pass over prescribed-order/trace algorithms,
root-only Hilbert class polynomial methods, decomposed CM, pairing-friendly
cofactor constructions, reverse SEA/modular equations, and the `p=n^2+7`
identity.  No files were edited.

Verdict:

```text
no viable route found
```

The obstruction matches the local audits: for fixed `p`, prescribed order
fixes `t`, hence fixes `D=t^2-4p`; for the strict p24 traces these are
conductor-2 CM classes with fundamental discriminants comparable to `p` and
class sizes `~2.06e11`, `~2.79e11`, and `~8.33e11`.  Known constructive
theorems either choose the field/discriminant, or compute/select an embedded
CM root.

The only serious-looking route remains the third trace:

```text
h = 205880396014 = 2 * 157 * 211 * 3107441
best decomposed-CM split = 66254 * 3107441
```

But known decomposed CM still constructs embedded class data by CRT or
class-orbit enumeration.  It can obtain a root without writing the full
`H_D`, but it does not avoid building an embedded invariant/recovery structure
at class-polynomial scale.  Thus it is a memory/root-degree win, not the
missing asymptotic selector.

The remaining gap is crisp:

```text
new explicit embedded odd class-field invariant/tower
+ small recovery map to j
+ root selection over F_p without enumerating the target CM class set
```

Existing constructive theorems do not provide that object.

## Embedded Class-Field Tower Sharpening

I added:

```text
p24/p24_abstract_classfield_quotient_probe.py
p24/embedded_selector_identity_toy.py
p24/embedded_classfield_tower_worklog.md
```

The abstract p24 third-target tower is confirmed cheaply:

```text
Cl(O_K) = bnr.cyc = [205880396014]
bnrclassno(bnr,n) = gcd(n,h) for n in 2,157,211,66254,3107441,h
bnrclassfield(bnr,2,1) = x^2 + 599
```

So the class-field quotient layers exist exactly as the smooth-class split
suggests.  However, the quotient polynomial is not yet embedded: it supplies
neither a modular/class invariant with known stabilizer inside the CM `j` root
torsor nor a recovery relation `R(alpha,j)=0`.

The finite-field identity reformulation is now explicit.  We need either a
quotient map `q(j)` whose fibers are the desired class-subgroup cosets, or a
class-action eigenfunction `e(g*j)=chi(g)e(j)`.  In the existing D=-5000 toy
embedded decomposition, the first rational selector in the plain `j` coordinate
appears at degree 15, exactly the generic interpolation threshold for 30 CM
roots.  That is negative evidence for a hidden low-degree plain-`j` selector,
not a proof against a more structured Shimura-reciprocity/Siegel-unit route.

Current status of this lead:

```text
abstract tower: yes
subsqrt formal quotient/recovery degrees: yes, 66254 and 3107441
embedded invariant/recovery relation: not found
asymptotic certificate speedup: not found
```

## Siegel-Unit / Split-Cycle Theorem Attempt

I added:

```text
p24/split_cycle_quotient_toy.py
p24/p24_split_cycle_selector_audit.py
p24/siegel_unit_split_cycle_theorem_attempt.md
```

The Siegel-Ramachandra/Siegel-function literature confirms explicit ray-class
generators and Shimura-reciprocity actions, but the algorithms still compute
conjugates/minimal polynomials by class or ray-class enumeration.  They do not
give a sublinear trace/norm to an arbitrary Hilbert subfield.

The sharper embedded object is a split-prime cycle quotient.  In the D=-5000
toy, the split prime `ell=11` has class order `3`; the horizontal graph breaks
the 30 CM roots into ten 3-cycles.  X0 edge sums/products still have full
orbit, but whole-cycle sums give a degree-10 quotient.  That proves the shape
of the embedded invariant and also shows the seed issue: the toy construction
used the embedded vertices.

For p24, small split primes give stronger formal splits than the previous
balanced subgroup:

```text
ell=7349:
  class_order = 487868237 = 157 * 3107441
  cycle_count = 422
  largest_formal_degree = 4.88e8 = 4.88e-4 * sqrt(p)

ell=677:
  class_order = 655670051 = 211 * 3107441
  cycle_count = 314
  largest_formal_degree = 6.56e8 = 6.56e-4 * sqrt(p)
```

Counting a literal seeded modular-polynomial walk changes the tradeoff:
`ell=2` has the cheapest walk proxy at `0.309*sqrt(p)` but is only a
constant-factor square-root route, while `ell=677` is `0.445*sqrt(p)` and
`ell=7349` is `3.59*sqrt(p)`.  Thus the odd split-cycle theorem still needs a
non-walk way to construct or pair the cycle quotient.

The new theorem target is therefore:

```text
construct one embedded 7349-cycle or 677-cycle of target CM j-roots over F_p
without first finding a seed CM root.
```

This is closer than the abstract class-field quotient because it is tied to an
explicit modular correspondence `Phi_ell`, but the seed/cycle-selector theorem
is still missing.

## Class-Character Period Reframing

I added:

```text
p24/character_period_transform_toy.py
p24/class_character_period_route_audit.py
p24/seedless_cycle_elimination_toy.py
p24/class_character_period_reframing.md
```

The split-cycle periods are exactly inverse Fourier transforms of twisted
traces.  For cyclic `G=<g>` and subgroup `H=<g^m>`:

```text
y_r = sum_{k=0}^{n-1} j(g^{r+mk})
T_s = sum_{i=0}^{h-1} zeta_m^{s*i} j(g^i)
y_r = m^{-1} sum_s zeta_m^{-sr} T_s
```

The D=-5000 finite-field toy verifies this over `F_3851` for quotient size 10:

```text
inverse_dft_recovers_period_sums=1
period_polynomial_degree=10
```

For p24, the Fourier layer is cheap enough:

```text
ell=7349 quotient_size=422 root_of_unity_extension_degree=35
ell=677  quotient_size=314 root_of_unity_extension_degree=156
```

The missing primitive is therefore a sublinear formula for high-order
non-genus twisted traces `T_chi = sum chi(a) j(a)`.

A tiny seedless elimination check also works when `H_D` is supplied:

```text
D=-87, h=6, ell=7, q=103
eliminated cycle-sum polynomial = (Y - 29)*(Y - 4)
```

This proves the cycle quotient is an honest algebraic elimination target.  It
does not bypass p24, because using `H_D` there means starting with a
degree-`205880396014` class polynomial.

## Period Selector Status Refresh

I added:

```text
p24/period_moment_idempotent_toy.py
p24/relative_norm_phase_toy.py
p24/abstract_vs_embedded_quotient_toy.py
p24/non_genus_twisted_trace_level_audit.py
p24/genus_projection_period_toy.py
p24/cycle_period_complexity_scan.py
p24/period_selector_theorem_status.md
```

These narrow the remaining theorem further.

Direct moments do not bypass the character-trace primitive.  In the
quotient-size-10 toy,

```text
P_d = sum_r y_r^d
    = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}
```

and the script verifies the convolution formula exactly.  Genus-only moments
reconstruct a coarser repeated-average polynomial, not the true period
polynomial.

Product/norm periods have the same issue.  Individual coset products are valid
quotient coordinates, but global norms give only the product over all cosets
and erase the quotient phase.  A Gross-Zagier/Borcherds-style global norm is
therefore not enough; a useful theorem would need a relative norm retaining all
degree-314 or degree-422 quotient coefficients.

The abstract class-field quotient is also not enough by itself.  For `D=-87`,
PARI's abstract quotient `x^2+3` has roots `[10,93]` over `F_103`, while the
embedded `Phi_7` cycle-sum quotient has roots `[4,29]`.  Both split, but the
roots are unpaired without an explicit relation to `j`.  This is exactly the
p24 `bnrclassfield` issue in miniature.

The standard non-genus twisted-trace modular-form route has natural level
`|D_K|`, not the small quotient degree:

```text
|D_K| = 652834595820939249713143
weight-1 level |D_K| Sturm/index proxy ~= 5.45e22
proxy / sqrt(p) ~= 5.45e10
```

Thus the live theorem target is now extremely specific:

```text
compute high-order non-genus class-character periods, embedded relative to j,
without class enumeration or H_D.
```

A direct small-CM period complexity scan also found no hidden recurrence or
sparse spectrum in quotient periods.  In the bounded sample
`D=-5000,-215,-279,-287,-327,-335`, every tested period sequence had full
Berlekamp-Massey complexity `bm=m`; the two rows where the DFT was available
had full support.  This supports the high-order trace barrier rather than a
cheap low-complexity finite-field identity.

## Composite Split-Cycle Refinement

I added:

```text
p24/composite_split_cycle_audit.py
```

This computes discrete logs of small split prime ideals relative to the
norm-23 generator of the cyclic class group, using Pohlig-Hellman over

```text
h = 2 * 157 * 211 * 3107441.
```

It then searches signed products of split ideals whose class has a desired
index.

The best single-prime `index=422` candidate was `ell=7349`.  A smaller
composite representative exists:

```text
2 * 919:
  index = 422
  order = 487868237
  norm = 1838
  X0 index proxy = 2760
```

More importantly, the balanced decomposed-CM quotient now has an explicit
low-norm composite representative:

```text
2 * 463 * 223^(-1):
  index = 66254 = 2 * 157 * 211
  order = 3107441
  norm = 206498
  X0 index proxy = 311808
  seeded-walk proxy = 311808 * 3107441
                    = 968924963328
                    = 0.968925 * sqrt(p)
```

No single split prime below `250000` has index `66254`, and an exhaustive
signed prime-power search up to norm `10000` found no index-66254 product.

This does not solve the seedless quotient-polynomial problem.  It does,
however, sharpen the formal embedded object substantially: the most balanced
candidate now has quotient degree `66254` and recovery degree `3107441`, both
tiny relative to `sqrt(p)`.

## All-Trace Split-Cycle Audit

I added:

```text
p24/all_target_split_cycle_audit.py
p24/all_trace_period_frontier.md
p24/period_target_tradeoff_audit.py
```

The smooth third trace is not the only serious period-selector target.  Running

```text
python3 p24/all_target_split_cycle_audit.py --prime-bound 250000 --show 12
```

shows that the first strict trace has a much smaller quotient:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 278733727154 = 2 * 19 * 7335098083
Cl(O_K) cyclic

ell=19:
  order = 14670196166 = 2 * 7335098083
  cycle_count = 19
  X0 degree = 20
  seeded_walk_proxy = 293403923320 = 0.293404 * sqrt(p)
  quotient root-of-unity extension degree = 2

ell=107:
  order = 7335098083
  cycle_count = 38
  X0 degree = 108
  seeded_walk_proxy = 792190592964 = 0.792191 * sqrt(p)
```

The middle trace also has tiny formal quotients:

```text
t = -78903246840
h = 833035208344 = 8 * 104129401043
Cl(O_K) = (208258802086, 2, 2)

ell=2:
  order = 208258802086
  cycle_count = 4
  seeded_walk_proxy = 0.624776 * sqrt(p)
```

The first trace is the cleanest theorem experiment because it asks for an
order-19 non-genus period quotient, rather than order-157/order-211 data.  But
it is not the best certificate target: its recovery degree is still
`14670196166`.

The explicit tradeoff audit records:

```text
first_trace_ell19:
  quotient = 19
  recovery = 14670196166
  seeded_proxy = 293403923320

third_trace_composite_2_463_223inv:
  quotient = 66254
  recovery = 3107441
  correspondence_degree = 311808
  seeded_proxy = 968924963328
```

So the split is:

```text
first trace ell=19: best toy theorem target
third trace composite: best certificate-oriented target
```

The same obstruction remains in both cases: the quotient/cycle degrees are
attractive only after an embedded period polynomial or a seed CM root is
available.

## Composite Orientation Ambiguity

I added:

```text
p24/composite_orientation_ambiguity_audit.py
p24/composite_orientation_toy.py
p24/composite_orientation_degree_tradeoff.py
p24/oriented_composite_path_toy.py
```

The p24 composite target is genuinely an oriented ideal target.  For the third
trace:

```text
logs:
  ell=2   index=2
  ell=223 index=1
  ell=463 index=1

desired oriented product = 2 * 463 * 223^(-1):
  index = 66254
  order = 3107441

all sign choices for plain X0(2*223*463):
  subgroup_index = 2
  subgroup_order = 102940198007
```

Only two of the eight sign choices have index `66254`; the others have index
`2`.  Thus the good recovery degree is not a property of the unoriented
composite modular equation.  It requires an orientation selector, which is
another form of the missing high-order class-character data.

The `D=-5000` toy has the same shape:

```text
desired 3 * 17^(-1):
  oriented_component_count = 6
  oriented_component_sizes = [5]

plain X0(3*17):
  unoriented_component_count = 2
  unoriented_component_sizes = [15]
```

This closes the tempting shortcut "use the low-norm composite X0 relation
unoriented".  A viable theorem must construct oriented periods.

The degree tradeoff is also negative for literal walks:

```text
plain X0(206498):
  recovery = 102940198007
  seeded_proxy/sqrt = 3.21e4

binary sign labels:
  correspondence_degree = 2494464
  recovery = 3107441
  seeded_proxy/sqrt = 7.75

full X1/Gamma1-style orientation:
  seeded_proxy/sqrt = 2.48e4 to 9.94e4
```

So even a cheap binary orientation label does not turn the composite target
into a literal sub-sqrt walk.  The route remains a non-walk embedded period
theorem or nothing.

The oriented-path toy tests whether binary orientation might at least create a
local selector.  In the `D=-5000` analogue, the oriented product
`3 * 17^(-1)` has index `6` and order `5`, but local path values retain the
full orbit:

```text
distinct_path_sums = 30
distinct_path_products = 30
distinct_path_edge_pair_sums = 30
```

The quotient only appears after whole-cycle aggregation:

```text
component_count = 6
component_sizes = [5]
period_sum_polynomial_degree = 6
```

So binary orientation defines the right directed cycle, but does not supply a
seedless local quotient coordinate.

## Oriented Relation / Inverse-SEA Torsor Toy

Following a sidecar suggestion, I added:

```text
p24/oriented_relation_torsor_toy.py
```

In the `D=-5000`, `h=30` calibration, the norm-3 ideal labels the CM roots by
class-group position.  Oriented split primes act by translations:

```text
ell=3  log=1
ell=11 log=20
ell=43 log=9
```

The relation word

```text
3 * 11 * 43
```

has total log `30 == 0 mod h`, and the toy verifies:

```text
fixed_indices_count=30
fixes_every_cm_root=1
```

The single-prime cycle relation `11^3` likewise fixes every root while
partitioning the torsor into ten 3-cycles.  This directly models the inverse
SEA/oriented-Elkies obstruction: knowing the oriented split-prime directions
and their relations produces equivariant Cayley-graph constraints, not a
distinguished CM root.  A root selector still needs a period/origin-breaking
invariant.

## Order-19 Embedded Theorem Narrowing

I focused on the first strict trace because it is the cleanest missing-theorem
model:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 278733727154 = 2 * 19 * 7335098083
ell = 19
quotient = 19
recovery = 14670196166
```

New artifacts:

```text
p24/order19_kummer_shortcut_audit.py
p24/order_l_kummer_phase_toy.py
p24/order19_component_mover_audit.py
p24/order19_ring_ray_sequence_audit.py
p24/hecke_projector_barrier_audit.py
p24/power_level_stabilizer_toy.py
p24/order19_power2_level_audit.py
```

Facts:

```text
p mod 19 = -1
zeta_19 in F_{p^2}, not F_p
split prime above 2 has full class-group order h
its quotient log on G/<19> is 1
Phi_2/Phi_19 local orientation proxy = 60
```

So orientation is cheap after the components exist.  But Kummer only
diagonalizes known periods:

```text
T_s = sum_i zeta_19^(s*i) j_i
y_r = 19^(-1) sum_s zeta_19^(-s*r) T_s
```

The embedded traces `T_s` are still the missing primitive.

The conductor-19/ray shortcut is closed:

```text
ring class conductor 19 kernel = 18
ray one-prime-above-19 kernel = 9
first ray kernel with 19-part is prime-square and ramified
```

Thus the degree-19 quotient is unramified conductor-1 Hilbert class data, not
a small-conductor modular-unit layer.

The group-algebra support lower bound is exact once a proposed formula
restricts to a local Hecke operator on the CM torsor:

```text
e_H = sum_{k=0}^{n-1} g^(19*k),  n = 14670196166
support(e_H) = n
```

The split prime above 2 gives a full generator, but bounded local words do not
apply this projector.  Banach's sharpened gap: a complete no-go theorem must
also prove a faithfulness/lifting lemma excluding one-prime accidental
finite-field identities that do not lift to characteristic zero.

The high-power level temptation is also separated:

```text
X0(2^19)->X(1) degree = 786432
horizontal edge (j_i,j_{i+19}) orbit = h
desired projector support = h/19
```

The `D=-5000` power-level toy confirms the same shape: oriented generator
paths of length `m` retain the full orbit, while quotient degree appears only
after whole `<g^m>` aggregation.

Conclusion for this pass: order-19 remains the right theorem toy, but the
missing theorem is now very narrow.  It must compute non-genus high-order
class-character traces, or prove an equivalent finite-field identity applying
the subgroup projector without enumerating its support.  Kummer, small
conductor/ray class fields, cheap quotient orientation, and high-power
generator-level data do not by themselves provide the selector.

## Generator-Crater / Serre-Tate Follow-Up

I continued the full split-2 generator branch.  New artifacts:

```text
p24/generator_crater_sequence_complexity.py
p24/local_coset_invariant_scan.py
```

The generator-crater scan tests complete small CM cycles where a split prime
generates the full class group.  For the raw generator sequence and simple
edge transforms

```text
j_i
j_{i+1} - j_i
j_{i+1} / j_i
j_i + j_{i+1}
j_i * j_{i+1}
```

the Berlekamp-Massey complexity is essentially full in all eight toy cases.
Examples:

```text
D=-5000, h=30, ell=3: j bm=30, ratio bm=30, edge_product bm=30
D=-215,  h=14, ell=2: j bm=14, ratio bm=14, edge_product bm=14
D=-311,  h=19, ell=2: j bm=19, ratio bm=19, edge_product bm=19
```

This does not rule out a deep Serre-Tate identity, but it rules out the easy
short-recurrence crater-coordinate shape.

The local-coset scan searches for bounded-degree formulas

```text
F(j_i, ..., j_{i+w-1})
```

that are constant on cosets `i mod m` without aggregating the whole subgroup.
For `D=-5000`, `h=30`, width `<=3`, degree `<=3`, no nonconstant local
invariant appears in the meaningful quotient cases.  The only positive row is
the degenerate `m=15` case, whose subgroup order is `2`, so a width-3 window
already covers more than a component.

Boyle independently checked the Serre-Tate/theta/Landen/crater-coordinate
route.  Verdict: no positive construction.  Serre-Tate coordinates are local
around an already chosen curve; Landen/theta recurrences are forward tests
unless one supplies the whole coherent ray branch; a multiplicative crater
coordinate with `u(gx)=rho*u(x)` is precisely the missing class-character
eigenfunction.  Computing that eigenfunction or the relation back to `j` is
the embedded class-field period problem again.

Conclusion: the full split-2 generator remains useful because it gives a clean
labeling of the torsor, but it does not by itself make the order-19 quotient
constructive.  The remaining positive theorem target is unchanged:

```text
construct an embedded order-19 class-character eigenfunction/trace, or an
equivalent subgroup projector, with a computable relation back to j.
```

## Embedded Selector Theorem Boundary

I added:

```text
p24/embedded_selector_theorem_attempt.md
p24/middle_genus_split_alignment_audit.py
p24/parabolic_inverse_chain_ansatz.py
p24/normal_basis_support_toy.py
p24/singular_moduli_normality_bound.py
p24/finite_field_lifting_height_audit.py
p24/class_invariant_lifting_height_audit.py
p24/modular_function_degree_lower_bound.py
p24/structural_lifting_support_lemma.md
p24/relative_coset_polynomial_height_audit.py
p24/relative_coset_phase_toy.py
p24/exact_trace_crt_modular_degree_barrier.py
p24/abstract_embedded_pairing_non_genus_toy.py
p24/principal_singular_modulus_reduction_audit.py
p24/frobenius_principal_ideal_origin_audit.py
```

The theorem attempt separates the positive and negative directions.

Positive conditional:

```text
Given G=Cl(O)=<g>, |G|=m*n, H=<g^m>, compute
T_s = sum_i zeta_m^(s*i) j_i
for the characters of G/H without constructing H_D or enumerating the class
set.  Fourier inversion then gives y_r=sum_k j_{r+m*k}, and the quotient and
recovery degrees are max(m,n).
```

For p24:

```text
first trace order-19:
  m=19, n=14670196166, zeta_19 in F_{p^2}

third trace composite:
  m=66254, n=3107441, zeta_m extension degree 5460
```

So Kummer/Fourier is not the obstruction.  The obstruction is computing the
non-genus high-order twisted traces.

Negative conditional:

```text
If a proposed local modular-correspondence formula restricts to a
bounded-support group-algebra operator on the CM torsor and the relevant
singular moduli are normal for the quotient characters, then producing an
H-period forces the exact projector

e_H = sum_{k=0}^{n-1} g^(m*k),

so the support is at least n.
```

This gives support lower bounds:

```text
first trace order-19:  14670196166
third composite:       3107441
```

The remaining gap for a true no-go theorem is the lifting/faithfulness step:
prove that a bounded-height finite-field identity built from bounded-level
modular data must lift to the characteristic-zero CM torsor, unless p is
smaller than the formula height.  Without that, one-prime accidental
identities are not excluded.

The normal-basis support toy makes the group-algebra hypothesis exact in small
CM rows.  It computes

```text
J(T)=sum_i j_i*T^i
```

for a cyclic embedded class cycle and checks `gcd(J(T),T^h-1)`.  When the gcd
is `1`, the translates of `j` are a normal basis, and `L*j=e_H*j` implies
`L=e_H`.  Thus support at least `|H|` is not just a heuristic in those rows.

A bounded run:

```text
python3 p24/normal_basis_support_toy.py --max-cases 4

D= -5000 q=1259 ell=3 h=30 gcd_degree=0 normal=1 m=3  n=10
D= -5000 q=1259 ell=3 h=30 gcd_degree=0 normal=1 m=5  n=6
D= -5000 q=1259 ell=3 h=30 gcd_degree=0 normal=1 m=6  n=5
D= -5000 q=1259 ell=3 h=30 gcd_degree=0 normal=1 m=10 n=3
D=  -215 q=251  ell=2 h=14 gcd_degree=0 normal=1 m=7  n=2
D=  -239 q=383  ell=2 h=15 gcd_degree=0 normal=1 m=3  n=5
D=  -239 q=383  ell=2 h=15 gcd_degree=0 normal=1 m=5  n=3
D=  -279 q=283  ell=2 h=12 gcd_degree=0 normal=1 m=3  n=4
D=  -279 q=283  ell=2 h=12 gcd_degree=0 normal=1 m=4  n=3
D=  -279 q=283  ell=2 h=12 gcd_degree=0 normal=1 m=6  n=2
```

For the actual p24 targets I can prove the normality input directly.  The
conductor-2 discriminants `Delta=t^2-4p` are divisible by `4`, so the
principal reduced form is the unique form with `a=1`; all other reduced forms
have `a>=2`.  The standard estimate

```text
||j(tau)| - exp(pi*sqrt(|Delta|)/a)| <= 2079
```

then gives, for any class character `chi`,

```text
|sum chi(a) j(a)|
  >= exp(pi*S)-2079 - (h-1)*(exp(pi*S/2)+2079),
  S=sqrt(|Delta|).
```

The new audit confirms this lower bound is positive by trillions in
natural-log scale for all strict p24 CM torsors.  Thus `j` is a normal element
for the p24 class torsors.  The projector support lemma is now conditional
only on the formula being a lifted/local group-algebra operator, not on
unproved normality of the target singular modulus.

I then checked the obvious lifting proof and it fails.  If a residual formula
vanishes modulo every prime above `p`, its norm is divisible by `p^h`; a crude
height proof would need each complex conjugate to have size `<p`.  But for
the p24 singular moduli,

```text
log |j_principal| ~= 5e12
log p ~= 55
```

so the norm bound is much too large.  The remaining lifting/faithfulness
theorem cannot be proved by ordinary archimedean height of `j`; it needs a
structural bounded-level modular argument, or else accidental one-prime
finite-field identities remain logically possible.

I also checked whether known smaller class invariants could make the same norm
argument viable.  They cannot at p24 scale: even a `1/28` height factor leaves
log-size around `1e11`, still much larger than `log(p) ~= 55`.  Class
invariants reduce coefficient sizes by constants; they do not by themselves
create a lifting/faithfulness theorem for this fixed prime.

I added a modular-degree lower-bound audit for single modular-function class
invariants.  If `f:X_Gamma -> P^1` has degree `d`, then one `f`-value can have
at most `d` preimages and so can merge at most `d` distinct `j`-roots.  Any
single value constant on an H-coset of size `n` must have `d>=n`.  For the
live targets this means:

```text
first_trace_order19:                  d >= 14670196166
third_trace_composite_2_463_223inv:   d >= 3107441
```

This rules out fixed-level Weber/Siegel/Ramachandra-style class invariants as
selectors.  A degree-`n` growing-level construction for the third target is
not ruled out, but that is already the recovery-sized object and still has to
pair back to `j`.

I audited the most tempting growing-degree construction: compute the principal
H-coset recovery polynomial

```text
R_H(X)=prod_{a in H}(X-j(a)).
```

For the third target, `deg R_H=3107441`, so any root of `R_H mod p` would be a
strict target CM root and the degree is sub-sqrt.  Poincare pointed out the
extra phase obstruction: `R_H` is not a rational integer polynomial.  Its
coefficients live in the unramified quotient field, so reducing one coset
polynomial modulo `p` requires choosing the embedded quotient root/prime above
`p`.  The new `relative_coset_phase_toy.py` makes this visible in the
`D=-5000` model: the six degree-5 coset recovery polynomials are distinct
conjugates, and multiplying them all recovers the full degree-30 class
polynomial.

The coefficient-height obstruction is also severe.  The principal conjugate
has log-size around `5e12`; even an optimistic `1/28` class invariant leaves
log-size around `1.8e11`, whereas `log(p) ~= 55`.  Thus ordinary complex or
CRT class-polynomial computation of this relative polynomial modulo `p` does
not become a sub-sqrt finite-field selector.  A positive route would need
direct mod-`p` evaluation of the relative polynomial, which is essentially the
missing embedded period primitive again.

I added a non-genus abstract-vs-embedded pairing toy.  For

```text
D=-2239, h=35, ell=5, quotient size 5, q=2243
```

PARI's abstract degree-5 Hilbert quotient has roots

```text
[709, 834, 913, 987, 1043]
```

while the embedded `Phi_5` cycle-period sums are

```text
[9, 106, 587, 812, 1142].
```

The script finds no affine or Mobius map taking one unordered root set to the
other.  This is toy evidence that the abstract quotient root and the embedded
period root require extra phase data, not a simple finite-field coordinate
change.

I also audited the direct principal singular modulus idea.  Complex
dominance makes the principal conjugate canonical over `C`, but reduction
modulo a completely split rational prime is not canonical: it requires
choosing a prime above `p`, equivalently one class-polynomial root.  In the
small `D=-87`, `q=103` split example, there are six roots modulo `q` and no
finite-field root is singled out by the complex embedding alone.  For p24,
computing the principal algebraic integer before reducing is height-scale
(`log |j_principal| ~= 5e12`), so direct q-exp reconstruction is not a
sub-sqrt selector either.

I added the Frobenius-principal-ideal version of the same audit.  For each
fixed strict trace, `pi=(t+sqrt(Delta))/2` is an element of the CM order with
norm `p`; the corresponding prime above `p` is principal.  This proves
complete splitting in the ring class field, but it makes Frobenius act as the
identity on every target root over `F_p`.  Identity action fixes the entire
torsor and does not select an origin/root.

Locke's sidecar sharpened the lifting/support statement into a clean
conditional lemma.  If a proposed formula is an additive combination of
oriented horizontal modular correspondences with good reduction, acts
equivariantly on the whole CM torsor, and the reduced CM element is normal,
then it is an element of `k[G]`; equality with an `H`-period forces it to be
the exact projector `e_H`.  The support lower bound follows immediately.

The failure modes are now explicit: one-prime non-lifted congruences,
non-equivariant origin selectors, bad denominator/pole reduction, unoriented
or order-changing correspondences, nonlinear norms/resultants/root selection,
abstract quotient roots unpaired with `j`, or reduced normality failure.

Descartes' explicit class-field sidecar reached the same boundary from the
constructive side.  `bnrclassfield`, principalization, Kummer, ray-class, and
Siegel/Ramachandra machinery can define related abstract fields, but known
algorithms pair them with `j` by enumerating conjugates or taking the same
subgroup trace/norm.  A quick literature check found the relevant normal-basis
result for Siegel functions (Jung-Koo-Shin,
`https://arxiv.org/abs/1007.2312`), but that strengthens the group-algebra
picture rather than bypassing it: a normal ray-class generator still has to be
projected by the subgroup idempotent to reach the desired unramified subfield.

The order-19 quotient is not a small conductor layer:

```text
ring conductor 19 kernel = 18
one split-prime ray kernel = 9
first ray kernel with a 19-factor is prime-square and ramified
```

Kuhn checked the other possible escape: fixed-trace construction.  Verdict:
known methods do not avoid CM root selection for the fixed p24 traces.
Waterhouse is an existence/classification theorem, Honda-Tate/Tate identifies
the fixed trace with a fixed isogeny class, and practical CM methods still
compute a class equation root or equivalent embedded class-field data.  The
useful source anchors are:

```text
Waterhouse 1969:
  https://www.numdam.org/item/?id=ASENS_1969_4_2_4_521_0
Agashe-Lauter-Venkatesan:
  https://arxiv.org/abs/math/0111159
Microsoft Research summary:
  https://www.microsoft.com/en-us/research/publication/constructing-elliptic-curves-with-a-given-number-of-points-over-a-finite-field/
Enge:
  https://arxiv.org/abs/cs/0601104
Sutherland CRT:
  https://arxiv.org/abs/0903.2785
Bröker-Stevenhagen:
  https://arxiv.org/abs/math/0511729
```

Franklin's middle-trace sidecar is now a control case.  The middle trace has

```text
Cl ~= C_104129401043 x (C2)^3
Redei 4-rank = 0
ell=11 index=8 principal-genus cycle
```

so the quotient is explicit genus data, but the residual recovery degree
`104129401043` is still `0.104 * sqrt(p)`, and seeded `ell=11` work is above
`sqrt(p)`.

Cicero closed the parabolic verifier-equation gap.  The parabolic LFT limit

```text
x_i = u * (1 + alpha*i)/(1 + beta*i)
```

and the analogous edge-coordinate ansatz both have only the degenerate
`alpha=beta` common factor after compatibility equations.  There is still no
surviving low-dimensional verifier-native section.

Dalton rechecked the near-square structure.  Verdict: no hidden strict-trace
relation beyond the `2^40` residue condition.  The strict curve-side traces
are exactly the three Hasse representatives of `t == p+1 mod 2^40`:

```text
1020608380936
-78903246840
-1178414874616
```

The real near-square CM identity is the `D=-7` trace `±2n`, which gives only
`v2=3` on the curve/twist orders.  For the strict traces:

```text
t=-1178414874616  D=-652834595820939249713143  conductor=2
t=-78903246840    D=-998443569409526507503607  conductor=2
t=1020608380936   D=-739589633190799177940983  conductor=2
```

All have fundamental discriminant on the scale of `p`, and `gcd(Delta,n)=4`,
so the near-square `n` is not hiding as a large square conductor.

I added a compact exact trace-CRT barrier.  Exact trace residues are a strong
oracle: modulo a product `N` larger than the Hasse width, they isolate a
target trace.  But imposing such residues constructively is modular level
data.  In p24 the strict verifier already imposes

```text
N=2^40=1099511627776=1.0995*sqrt(p),
[SL2:Gamma0(2^40)] = 3*2^39.
```

Odd CRT residues can distinguish the remaining Hasse representatives and
improve constants, but the modular degree is already sqrt-scale.

## Finite-field selector theorem progress

I added:

```text
p24/finite_field_selector_degree_theorem.md
p24/finite_field_modular_zero_lemma.md
```

This proves a characteristic-`p` lower bound that does not depend on the
failed height-lifting argument.  If an embedded modular-correspondence cover
or algebraic-elimination cover carries distinct CM points indexed by `G`, and
a rational function on that cover is constant on `H`-cosets, then one fiber
contains `|H|` distinct CM points.  Therefore the function degree is at least
`|H|`.

Consequences:

```text
first trace order-19 toy:  degree >= 14670196166
third trace certificate target: degree >= 3107441
```

This rules out bounded local finite-field identities, fixed-level class
invariants, and small resultant covers as selectors.  It also explains the
toy split-cycle data: edge invariants keep full orbit size, while whole-cycle
invariants work only after their degree has grown to the cycle length.

What remains open is narrower.  Additive equivariant Hecke formulas still need
the reduced normality/nonvanishing theorem for class-character resolvents mod
this particular split prime.  Positive construction still has one plausible
shape: a growing-degree embedded object around the third target's
`|H|=3107441` recovery degree, plus a quotient-phase selector that avoids full
class enumeration.

The modular zero lemma handles the bounded p-specific accident loophole for
local formulas: if the residual difference of a proposed identity vanishes on
all `h` embedded CM points and has pole degree below `h`, it is a global mod-p
modular identity.  Ordinary linear Hecke-word identities are then killed by
Tate-cusp pole orders.  This is strictly weaker than full reduced normality,
but it is enough to rule out the bounded-level identities we were most worried
about.

## Class-field tower phase calibration

I added:

```text
p24/tower_phase_refinement_toy.py
p24/class_field_tower_phase_audit.md
```

This tests the tempting p24 third-trace tower

```text
2 -> 157 -> 211 -> recovery degree 3107441
```

on the small exact torsor `D=-5000`, `h=30=2*3*5`.  The quotient of size `6`
really does decompose as a degree-2 top period followed by relative degree-3
child polynomials.  The toy output gives two different child polynomials above
the two top roots:

```text
parent=0 top_value=1126 child_polynomial=[563, 777, 133, 1]
parent=1 top_value=532  child_polynomial=[648, 958, 727, 1]
```

Thus the tower representation is useful after the embedded relative
refinements are known.  It does not create them.  In the toy those
refinements were computed from the actual CM `j`-cycle, and the top
polynomial plus the abstract factorization did not determine the child phase.

For p24, the constructive theorem would need to compute the analogous
relative refinements for quotient factors `2,157,211` without enumerating the
full class set.

Schrodinger independently checked the same tower obstruction and pointed to
the oriented composite toy:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/oriented_composite_path_toy.py
```

Its output is the right miniature for `2*463*223^(-1)`: local oriented path
values keep all `30` starts, while whole-cycle aggregation collapses to `6`.
So binary orientation labels do not create a seedless local selector; they
only define which class-period aggregation is desired.

## Non-genus Trace Formula Boundary

I added:

```text
p24/non_genus_trace_formula_boundary.md
```

The surviving positive route can be stated as computing high-order
class-character traces

```text
T_s = sum_g chi_s(g) j_g
```

for characters of `Cl(O)/H` of order dividing `66254`.  I checked the
Zagier/Bruinier-Funke/Bruinier-Jenkins-Ono trace formula direction.  Those
theorems explain global traces and standard twisted traces through
weight-`3/2` modular forms/theta lifts, but they do not give the embedded
finite-field non-genus class-character trace needed here.  The corresponding
automorphic object has discriminant/level tied to
`|D_K| ~= 0.653*p`, so standard coefficient computation is not a sub-sqrt
selector.

## Near-Singular Window Audit

I added:

```text
p24/near_singular_window_audit.py
p24/near_singular_window_audit.md
```

This tests whether the rejected singular torus points `A=+/-2` have a useful
sub-sqrt perturbation window.  Exact small `p=n^2+7` calibration rows show no
such concentration.  Aggregate:

```text
good=10482/360626
base_rate=0.02906612
p^0.40 hits=30/1191 capture=0.002862 lift=0.867 coverage=0.003303
p^0.50 hits=108/3742 capture=0.010303 lift=0.993 coverage=0.010376
```

At `W ~= sqrt(p)`, capture is essentially coverage and lift is `1`; smaller
windows have tiny capture.  So near-singular scanning is not an asymptotic
selector.

## Fixed Trace and Tower Section Theorem

I added:

```text
p24/fixed_trace_cm_root_toy.py
p24/fixed_trace_cm_root_toy.md
p24/tower_section_obstruction.md
p24/relative_tower_character_toy.py
```

The fixed-trace toy corrects the Waterhouse/Mestre escape hatch.  For
`p=103`, `t=8`, `D_K=-87`, the Frobenius discriminant is
`t^2-4p=-348=4D_K`.  Enumerating curves over `F_103` gives:

```text
H_-87 roots mod p:   [5, 29, 32, 43, 60, 70]
H_-348 roots mod p:  [4, 44, 62, 63, 85, 86]
fixed |t|=8 j-set:   [4, 5, 29, 32, 43, 44, 60, 62, 63, 70, 85, 86]
sets_equal=1
```

So fixed trace names the relevant isogeny class/volcano; constructing one
curve over the fixed prime is still embedded CM root selection.

Parfit supplied the clean tower obstruction.  For a refinement layer

```text
L <= K <= G,
```

a seedless child selector would be a `G`-equivariant section `G/K -> G/L`.
If `s(K)=aL`, then for every `k in K`,

```text
s(K) = s(kK) = k aL,
```

so `K <= L`.  Thus no nontrivial tower layer has a canonical equivariant child
label.  The tower may still produce unordered relative child polynomials, but
it needs separate phase data.

The new relative-character toy identifies that phase data.  In the
`D=-5000`, `h=30` tower, the child polynomials above the two top roots are
inverse DFTs of relative class-character traces on `K/H`.  Because `F_1259`
does not contain `mu_3`, the nontrivial traces live in `F_{1259^2}`:

```text
parent=0 top_value=1126
  child_periods=[159, 1004, 1222]
  relative_character_traces_pairs=[(1126, 0), (196, 1041), (414, 218)]
  child_polynomial=[563, 777, 133, 1]

parent=1 top_value=532
  child_periods=[1062, 254, 475]
  relative_character_traces_pairs=[(532, 0), (587, 1038), (808, 221)]
  child_polynomial=[648, 958, 727, 1]
```

Bacon's constructive pass independently reached the same boundary: the p24
third-trace tower

```text
G > <g^2> > <g^314> > <g^66254>
```

is formally sub-sqrt if the embedded relative coefficients are computable
directly, but modular units, relative norms, and Kummer inversion all reduce
to the same missing primitive.

The theorem gap is now:

```text
horizontal relative-period lemma:
compute the embedded non-genus relative class-character traces for the odd
157 and 211 refinements of the p24 third trace, without enumerating Cl(O) or
constructing H_D, and with a recovery relation to j of degree <= 3107441.
```

The degree-2 layer is only genus, since

```text
D_K = -599 * 1089874116562502921057.
```

So the missing theorem is no longer "make a tower"; it is specifically the
odd relative phase theorem for the `157` and `211` layers.

## Odd Relative Phase Source Audit

I added:

```text
p24/odd_relative_phase_source_audit.py
p24/odd_relative_phase_source_audit.md
p24/genus_odd_phase_obstruction.md
```

This checks whether the third-trace odd phases might come from the visible
factorization

```text
D_K = -599 * 1089874116562502921057.
```

The answer is no, except for the already-known genus bit.  The quotient roots
of unity are cheap:

```text
ord_157(p)=156
ord_211(p)=35
ord_33127(p)=5460
```

but the corresponding small cyclotomic quadratic subfields are
`Q(sqrt(157))`, `Q(sqrt(-211))`, and `Q(sqrt(-599))`.  Only `-599` is relevant
to the target field, and it supplies only the degree-2 genus quotient.

For a Jacobi-sum construction of the actual target CM field, the conductor
must be divisible by `|D_K|`; the audit gives:

```text
ord_|D_K|(p)=14812380038735835154352
```

which is far beyond `sqrt(p)=10^12`.

The genus obstruction is purely group-theoretic.  Genus characters factor
through

```text
G/G^2.
```

For the third trace, `G` is cyclic of order `2*157*211*3107441`, so `G/G^2`
has order `2` and `G^2` has order `157*211*3107441`.  Any construction using
only ramified prime discriminants, Kronecker symbols, quadratic subfields, or
genus/reflection data is constant on `G^2`, hence cannot label the odd
`157`/`211` children.  The Redei audit gives 4-rank `0`, so there is no hidden
2-primary refinement before the odd principal-genus problem.

Goodall's independent read-only pass reached the same boundary: `D=-599`
splits but is nonprincipal over `F_p`, and known reflection/Kummer/Jacobi/
Scholz-genus machinery still reduces to the non-genus class-character traces

```text
T_chi = sum_a chi(a) j(a)
```

for order `157` and `211` characters.

## Direct Verifier Ray-Section Theorem

I added:

```text
p24/direct_verifier_ray_section_theorem.md
```

This consolidates the non-CM route through the literal verifier equation

```text
Z_k(A,x)=0,  k=40.
```

The main distinction is:

```text
over Fbar_p: every nonsingular A has 2^40-torsion;
over F_p: the verifier asks for a Frobenius-fixed exact-order ray.
```

Thus division-polynomial algebra by itself projects to essentially every
nonsingular Montgomery parameter.  The rare condition is not algebraic
existence of a torsion point but rationality of an exact ray:

```text
lambda ==  1 mod 2^40   curve side
lambda == -1 mod 2^40   twist side.
```

In moduli terms this is `X1(2^40)/{+-1}` over the Montgomery `X(2)` line.
Generic rational or bounded-genus sections are ruled out by the
`Gamma1(2^k)` index/gonality growth, and all tested coordinate sections
collapse:

```text
geometric/LFT x-chains, s=x+1/x, edge coordinate r, power/Chebyshev
semiconjugacy, Lucas recurrence, parabolic LFT limit, low-degree (A,x)
relations, and fixed-x fibers.
```

The inverse-chain MITM audits show the same degree accounting:

```text
degree(C_a)*degree(D_b)=2^a*2^b=2^40=1.099512*sqrt(p).
```

So a successful direct construction would need a genuinely p-specific label
for the Frobenius-fixed ray, not merely a solver for the universal
division-polynomial equation.

## p23 Transfer To p24 Scaling Audit

I added:

```text
p24/p23_transfer_to_p24_scaling_audit.md
```

The p23 method transfers as a fixed-level constant-factor tool:

```text
X1(16) prescribed torsion
nonsplit cyclic 2-Sylow
first-branch halving complete in the nonsplit family
```

but p24 needs depth `40`, so fixed `X1(16)` leaves a `36`-bit tail.  The exact
tower accounting is:

```text
lift X1(16) -> X1(2^h):  2^(h-4)
residual tail:           2^(40-h)
product:                 2^36 = 0.06871948 * sqrt(p)
```

This is a strong constant, not an exponent improvement.

Fresh p24-congruence calibration at `p=57527`:

```text
accepted_x16=5000
nonsplit=2486
nonsplit survive_depth_8  = 208/2486 = 0.083669
nonsplit survive_depth_12 = 28/2486  = 0.011263
```

The exact oriented-depth audit on four `p=n^2+7`, `n==0 mod 8` rows gave:

```text
aggregate_fitted_beta_x1=0.872407
aggregate_fitted_beta_x0=0.000000
```

The shallow x1 slope is noisy and earlier deeper runs are closer to 1, but the
interpretation is stable: oriented X1 depth costs about one bit per bit; X0
depth is cheap only because it omits the verifier orientation.

The p24 first-lift-cover feature scan also showed only constant lifts:

```text
base depth-12 = 120/5000 = 0.024
best bucket lift = 1.293996
best capture = 80/120 = 0.666667
```

So the p23 method remains a practical fixed-prime search improvement, not the
requested asymptotic p24 speedup.  A true scaling win from this line still
requires a growing `X1(2^h)` tower sampler with overhead exponent `beta < 1`,
or an equivalent p-specific ray-tail label.

## Admissible Seedless Selector Theorem

I added:

```text
p24/admissible_seedless_selector_theorem.md
```

This consolidates the finite-field degree theorem, structural support lemma,
finite-field zero lemma, tower-section obstruction, genus obstruction, and the
new prime-torsor obstruction into one conditional no-go theorem.

In the admissible model, a seedless construction may use prime-to-`p`
correspondences, rational functions on irreducible covers, bounded oriented
Hecke words, abstract quotient towers, and genus data, but it cannot insert an
external CM root or a prime-above-`p` label.

The consequences are:

```text
scalar H-coset coordinate:      degree >= |H|
additive H-period projector:    support >= |H|
abstract quotient tower:        roots unpaired with embedded j-periods
nontrivial tower child choice:  no G-equivariant section
genus-only data:                factors through G/G^2
```

For the third p24 target, `|H|=3107441`.  For the order-19 theorem toy,
`|H|=14670196166`.  Thus the theorem closes bounded local identities, genus
labels, sparse projector formulas, and bare abstract class-field towers.  The
surviving route remains exactly the embedded non-genus `157`/`211` relative
class-character trace computation, followed by degree-`3107441` recovery.

## Prime-Torsor Obstruction For Abstract Towers

I added:

```text
p24/prime_torsor_obstruction_theorem.md
```

This is the cleanest form of the abstract class-field tower obstruction.  If
the ordinary prime `frak_p | p` of `K` splits completely in the ring class
field `L_rc`, then every intermediate quotient `M=L_rc^H` reduces as

```text
O_M tensor_{O_K} F_p ~= product_{G/H} F_p.
```

So an abstract quotient polynomial modulo `p` gives a `G/H`-torsor of roots,
equivalently primes above `p`.  The embedded CM period quotient is another
`G/H`-torsor.  A compatible pairing between the abstract roots and embedded
periods is not intrinsic; the set of such pairings is itself a `G/H`-torsor.

In tower language, the children above a parent form an `H_parent/H_child`
torsor, and the existing section proof says that a seedless `G`-equivariant
child selector cannot exist unless the layer is trivial.

This closes the loophole "use `bnrclassfield`, reduce modulo `p`, and choose a
root".  Arbitrary finite-field root choice is fine after an embedded relation
to `j` is known.  It does not create that relation.  The remaining positive
route must still supply embedded non-genus relative class-character traces for
the odd `157` and `211` refinements, paired back to `j`, with final recovery
degree `3107441`.

## Period Correlation Idempotent Toy

I added and ran:

```text
p24/hecke_correlation_trace_boundary.md
p24/period_correlation_idempotent_toy.py
```

This closes the natural Hecke-correlation/moment reframing.  In the
`D=-5000`, quotient-size-10 calibration,

```text
C(d) = sum_i j_i j_{i+d}
sum_r y_r^2 = sum_{d in H} C(d)
```

and the script verifies:

```text
square_sum_equals_projected_autocorrelation=1
autocorrelation_spectrum_matches_trace_products=1
period_autocorrelation_bm_complexity=10
nonzero_spectral_components=10
```

The autocorrelation diagonalizes to `T_s*T_{-s}`, where the `T_s` are the same
quotient-character traces.  Thus moments/correlations/global Hecke traces are
not an independent selector unless one also supplies a cheap projector onto
the high-order subgroup `H`.  For p24 that missing projector is again the
embedded odd `157`/`211` relative-period theorem.

## Correspondence Recurrence And Resultant Boundary

I added:

```text
p24/correspondence_recurrence_resultant_boundary.md
```

and reran the supporting scripts:

```text
python3 p24/power_level_stabilizer_toy.py
python3 p24/oriented_composite_path_toy.py
python3 p24/seedless_cycle_resultant_audit.py
python3 p24/order19_power2_level_audit.py
```

This closes the natural "fast power the correspondence" variant.  A compact
chain or recurrence for repeated `Phi_ell` edges represents a long edge or
many hidden branches; it does not create the subgroup period.

Toy `D=-5000`, move `6`:

```text
oriented_path_count=30
distinct_path_sums=30
component_count=6
distinct_period_sums=6
```

The oriented composite analogue also keeps full local orbit data:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_period_sums=6
```

For p24, seedless closed-cycle resultants have enormous correspondence degree:

```text
ell=23 full generator cycle:
  order = 205880396014
  log10 psi(23^order) ~= 2.803531e11

ell=677 index-314 cycle:
  order = 655670051
  log10 psi(677^order) ~= 1.855932e9
```

The desired decomposed-CM degrees `66254` and `3107441` appear only after an
embedded quotient period or equivalent invariant is known.  Thus
recurrence/resultant compression is not a certificate-scale speedup unless it
also supplies the same high-order subgroup projector or non-genus relative
class-character traces.

## Reduced Resolvent Normality Scan

I added:

```text
p24/reduced_resolvent_vanishing_scan.py
p24/reduced_resolvent_normality_boundary.md
```

For a complete cyclic CM torsor, the scan forms

```text
J(T) = sum_i j_i T^i
```

and computes `gcd(J(T), T^h-1)`.  A nontrivial gcd is exactly a packet of
class-character resolvents that vanished after reduction.  When the gcd degree
is `0`, the reduced `j`-cycle is normal and the additive support lemma is
faithful.

Commands run:

```text
python3 -m py_compile p24/reduced_resolvent_vanishing_scan.py
python3 p24/reduced_resolvent_vanishing_scan.py \
  --max-cases 12 --min-h 12 --max-h 96 --max-abs-D 12000
python3 p24/reduced_resolvent_vanishing_scan.py \
  --max-cases 40 --min-h 12 --max-h 140 --max-abs-D 24000
python3 p24/normal_basis_support_toy.py --max-cases 8 --min-h 12 --max-h 96
```

Outputs:

```text
12-row scan:
  normal_rows=12
  nonnormal_rows=0
  quotient_dft_rows_with_roots=15
  quotient_dft_full_support_rows=15

40-row scan:
  normal_rows=40
  nonnormal_rows=0
  quotient_dft_rows_with_roots=46
  quotient_dft_full_support_rows=46
```

So no p-specific reduced character vanishing appeared in the small complete
CM cycles.  This is evidence against a helpful finite-field collapse and in
favor of the conditional projector support barrier, but it is not a p24 proof.
For p24, one would need to prove that the fixed split prime does not divide
the norms of all relevant odd non-genus resolvents

```text
T_chi = sum_g chi(g) j_g.
```

Naive height lifting fails, and known Gross-Zagier/intersection/norm formulas
do not currently give this all-character nonvanishing without the same
class-character period input.

## Smooth Torsor Search Boundary

I added:

```text
p24/smooth_torsor_search_tradeoff_audit.py
p24/smooth_torsor_search_boundary.md
```

and ran:

```text
python3 -m py_compile p24/smooth_torsor_search_tradeoff_audit.py
python3 p24/smooth_torsor_search_tradeoff_audit.py
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/post_trace_construction_audit.py --min-p 10000 --max-p 120000 \
  --max-rows 6 --n-modulus 8 --n-residue 0
```

This separates smooth-class navigation from first-root discovery.  For the
third trace, smoothness gives excellent formal decomposed degrees:

```text
best_embedded_quotient_degree=66254
best_embedded_recovery_degree=3107441
quotient_plus_recovery=3173695
```

But random discovery of a strict trace remains square-root density:

```text
sum_h_one_order_per_trace=1317649331512 = 1.317649*sqrt(p)
random_j_expected_trials_over_sqrt_using_sum_h=0.758927
two_order_proxy_expected_trials_over_sqrt=0.379464
generous_montgomery_A_degree_bound_expected_trials_over_sqrt=0.063244
```

Those constants can be attractive, but they do not change the exponent.  The
small-field post-trace audit agrees that after a target `A` is known, `x0` is
constant expected work:

```text
target_A_over_sum_sqrt=8.500883
strict_A_over_sum_sqrt=6.005442
avg_x_per_strict_A=97.802029
projected_group_point_expected_trials_per_known_good_side<=2
```

So smooth BSGS/Pohlig-Hellman/class navigation helps after a seed CM vertex,
after two known vertices, or after an embedded quotient root.  It does not
create the first target root or the embedded quotient equations.  The smooth
third trace remains the best formal route, but only if the missing odd
`157`/`211` embedded period theorem is supplied.

## Reduced Normality And Unit Distribution Tightening

I added:

```text
p24/reduced_normality_false_lemmas_toy.py
p24/reduced_normality_proof_frontier.md
p24/reduced_resolvent_propagation_lemma.md
p24/ray_kernel_distribution_audit.py
p24/unit_distribution_obstruction.md
```

and ran:

```text
python3 -m py_compile p24/reduced_normality_false_lemmas_toy.py \
  p24/ray_kernel_distribution_audit.py
python3 p24/reduced_normality_false_lemmas_toy.py
python3 p24/ray_kernel_distribution_audit.py
```

The false-lemma toy gives a split squarefree degree-5 vector over `F_11` with
distinct entries but zero Fourier components:

```text
distinct_values=[0, 1, 2, 4, 9]
dft_spectrum=[5, 0, 9, 8, 0]
zero_character_indices=[1, 4]
```

Thus split/separable roots and primitive generation of the split algebra do
not imply reduced normality of the specific `j` vector.  The proof frontier is
the normal determinant unit statement

```text
P_p does not divide product_chi sum_i chi(g)^i j_i.
```

Arendt's sidecar result is now recorded as a propagation lemma: if one
resolvent vanishes at a split prime above `p`, it vanishes at all `G`-translate
primes; and because `J(T)` has coefficients in `F_p`, bad characters occur in
Frobenius orbits.  For the third trace, primitive odd quotient characters have
orbit length

```text
ord_66254(p) = ord_33127(p) = 5460.
```

So any finite-field collapse is large and Galois-stable, not a one-character
accident.  It is still not impossible by current norm/height bounds.

Ohm's sidecar result is recorded as a unit-distribution obstruction.  The only
plausible modular-unit escape would be a ray-kernel distribution relation, but
p24's odd layers are conductor-one Hilbert-class layers.  The audit prints:

```text
ell=157 Kronecker(D,ell)=-1 |(O_K/ell)^*|=24648 no 157-factor
ell=211 Kronecker(D,ell)=-1 |(O_K/ell)^*|=44520 no 211-factor
```

The first `ell`-primary ray factors occur only in the ramified `ell^2 -> ell`
filtration, whose image in `Cl(K)` is trivial.  Thus
Siegel/Ramachandra/Weber distribution and normal-basis machinery does not
compute the p24 unramified `157`/`211` relative phase.

## Frobenius Packet And Cyclic Code Audit

I added:

```text
p24/frobenius_packet_testing_barrier.py
p24/frobenius_packet_testing_barrier.md
p24/cyclic_code_projector_weight_toy.py
p24/cyclic_code_projector_weight_scan.py
```

and ran:

```text
python3 -m py_compile p24/frobenius_packet_testing_barrier.py
python3 p24/frobenius_packet_testing_barrier.py
python3 -m py_compile p24/cyclic_code_projector_weight_toy.py
python3 p24/cyclic_code_projector_weight_toy.py
python3 -m py_compile p24/cyclic_code_projector_weight_scan.py
python3 p24/cyclic_code_projector_weight_scan.py \
  --max-cases 4 --max-quotients 2 --max-q-for-degree2 1300
```

The packet toy uses the `D=-5000`, `h=30`, quotient-size-10 CM cycle over
`F_1259`.  It finds all packet residues nonzero, then changes only two period
coordinates to kill one degree-2 packet while agreeing on the other eight:

```text
chosen_factor_degree=2
agrees_on_period_coordinates=8/10
packet_killed=1
```

So sparse/random sampling of period coordinates cannot certify packet
nonvanishing.

The cyclic-code audit computes the exact p24 quotient factor count:

```text
p24_packet_degree_counts={1: 2, 35: 12, 156: 2, 5460: 12}
```

Only 28 packet residues would need checking if the embedded period vector were
known.  But in the exact group-algebra model, a vanished packet gives an
annihilator code, and the selector question becomes the minimum Hamming weight
in `e_H + Ann(j)`.  In the calibrated toy, even an artificial degree-2 packet
annihilator did not reduce projector weight:

```text
quotient_size subgroup_size projector_weight best_coset_weight
3             10            10               10
5              6             6                6
6              5             5                5
10             3             3                3
15             2             2                2
```

Thus Frobenius packets are a compact way to state reduced normality, and a
potential verification format after embedded periods are known.  They are not
yet a construction of those periods or a sparse projector.

The broader scan across four small CM cycles gave:

```text
rows=8
reduced_weight_rows=0
```

All rows were naturally normal (`natural_gcd_degree=0`); after inserting an
artificial degree-2 packet annihilator, the minimum coset representative still
had the original projector weight.  So no small cyclic-code sparse-projector
accident appeared.

## Verifier-Side Compression Refresh

Avicenna checked the non-CM verifier surface again.  The conclusion matches
`p24/direct_verifier_ray_section_theorem.md`: `Z_k(A,x)=0` is universal over
`Fbar`; the arithmetic selector is the `F_p`-rational exact ray, equivalently
`lambda=+-1 mod 2^40`.

Resultants/MITM keep product degree `2^40`; rational canonical forms repackage
the same eigenvalue condition; Lattes-to-power compression only appears in
singular `A=+-2`; extension-field trace/norm of torsion coordinates is not
compatible with the x-only map; and `X0` quotients forget the generator
orientation.  The dichotomy is now:

```text
forget the marked ray -> X0/symmetric quotient plus residual orientation tail
retain the marked ray -> X1(2^40)/+- scale
```

No p-specific finite-field identity predicting the missing `X0 -> X1` tail is
visible.

## X1 Tower Sampling Conservation

I reran:

```text
python3 p24/x1_tower_mitm_cost_audit.py
python3 p24/inverse_tower_intersection_degree_audit.py
```

and added:

```text
p24/x1_tower_sampling_conservation.md
```

The point is to isolate the top-down sampler loophole.  If a level-`2^h`
`X1` sampler costs `C_h`, the remaining verifier tail costs `2^(40-h)`, so
work is

```text
C_h * 2^(40-h).
```

Ordinary recursive lifting from `X1(16)` has `C_h=2^(h-4)`, hence constant
post-base cost:

```text
2^(h-4) * 2^(40-h) = 2^36 = 0.06871948*sqrt(p).
```

So a true p24 tower win needs a sampler with

```text
C_h = 2^(beta*(h-4)), beta < 1.
```

The existing branch MITM, inverse-chain intersections, and `X0` quotients do
not supply that; they either keep product degree `2^40` or forget the
orientation tail.  This leaves the direct verifier route with the same kind
of missing object as the CM route: a p-specific label for the hidden ray
phase.

## Mixed-Level Oracle Refresh

I reran:

```text
python3 p24/mixed_crt_trace_residue_optimizer.py \
  --prime-bound 97 --max-odd-part 200000 --min-depth 24 --max-depth 42 --top 20
python3 p24/reverse_sea_level_tradeoff_audit.py \
  --depths 22 24 26 28 30 32 34 36 38 40 \
  --max-ell 1000 --max-steps 16 --max-initial-count 1000000
python3 p24/mixed_level_index_audit.py
python3 p24/mixed_torsion_divisor_audit.py
```

and added:

```text
p24/mixed_level_oracle_refresh.md
```

The wider CRT optimizer tested `80940` mixed levels.  The best optimistic
proxy remained pure `2^40`:

```text
depth=40
odd_part=1
survivors=6
gamma0_over_sqrt=1.649267
proxy_over_sqrt=1.649267
```

Shallower 2-adic levels plus odd residues can isolate the six target traces,
but the Gamma0 index is worse; for example:

```text
depth=36, ell=71: gamma0/sqrt=7.421703
depth=38, ell=23: gamma0/sqrt=9.895605
```

The branch-repeat lower bound already forces several `sqrt(p)` of Gamma0 cost
for shallower prefixes.  Mixed target-order divisors agree: above `sqrt(p)`,
the cheapest largest-prime-factor divisor is the pure `2^40` condition, while
odd alternatives introduce large levels.

Conclusion: mixed odd/2-adic trace residues are good bookkeeping and constant
factor diagnostics, not an asymptotic p24 selector under the optimistic level
proxy.

## Montgomery Trace Transform Barrier

I added:

```text
p24/montgomery_trace_transform_audit.py
p24/montgomery_trace_transform_barrier.md
```

and ran with the bundled NumPy runtime:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/montgomery_trace_transform_audit.py \
  --min-p 10000 --max-p 120000 --max-rows 6 --n-modulus 8 --n-residue 0 --top 6

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/additive_spectrum_trace_bucket.py \
  --min-p 10000 --max-p 120000 --max-rows 6 --n-modulus 8 --n-residue 0 \
  --max-modulus 64 --top 6

/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/multiplicative_spectrum_trace_bucket.py \
  --min-p 10000 --max-p 90000 --max-rows 4 --n-modulus 8 --n-residue 0 \
  --max-character-order 32 --top-spectrum 4 --top-cosets 6
```

The trace function has the exact convolution form

```text
t(A) = - sum_c chi(c^2 - 4) chi(A + c).
```

This is excellent for small-field calibration, but the full trace transform
did not reveal sparsity.  Across six p-shaped rows:

```text
support_fraction median = 1.000000
top16_energy median    = 0.002556
top64_energy median    = 0.010083
top256_energy median   = 0.039016
low32_energy median    = 0.002899
low128_energy median   = 0.010744
```

The strict bucket itself also had random-sized additive peaks:

```text
max_peak/sqrt(good) ~= 3.8 to 4.1
low_energy(|h|<=32) median ~= 0.0027
low_energy(|h|<=128) median ~= 0.0100
```

Low-order multiplicative cosets in `A` and Montgomery `j` showed only unstable
constant-factor lifts.  So the hypergeometric trace-function route is a full
trace oracle and a good diagnostic, not a visible sublinear selector for the
strict p24 residue class.

## Reduced Normality Theorem Refinement

I integrated the sidecar audits and added:

```text
p24/quotient_spectrum_support_theorem.md
p24/quotient_spectrum_support_toy.py
p24/reduced_normality_failure_audit.py
p24/p24_frobenius_packet_map.py
p24/failure_projector_weight_audit.py
p24/partial_orbit_invariance_theorem.md
p24/partial_orbit_window_toy.py
p24/cyclic_code_min_weight_counterexample.py
p24/cyclic_code_min_weight_scan.py
p24/dual_coset_annihilator_lemma.md
```

The clean additive-selector statement is:

```text
A*j = e_H*j  iff  A in e_H + Ann(J).
```

Thus full reduced normality (`Ann(J)=0`) is sufficient, but not logically
necessary.  The exact replacement is the cyclic-code minimum-distance
statement:

```text
min_{B in Ann(J)} wt(e_H + B) = |H|.
```

The tempting quotient-spectrum shortcut is valid only for formulas already
known to descend to the quotient `G/H`.  Quotient-character nonvanishing alone
does not control arbitrary sparse group-algebra operators, because free
non-quotient Fourier values can change coefficient support.

The quotient support toy compiled and ran:

```text
python3 -m py_compile p24/quotient_spectrum_support_toy.py
python3 p24/quotient_spectrum_support_toy.py \
  --max-h 18 --max-q 120 --max-q-degree2 47
python3 p24/quotient_spectrum_support_toy.py \
  --max-h 30 --max-q 300 --max-q-degree2 47
```

The larger output summary was:

```text
rows=1016
nonquotient_factor_rows=750
nonquotient_reduced_rows=0
quotient_factor_rows=266
quotient_reduced_rows=0
```

So artificial low-degree packet kernels did not reduce projector support in
this small algebra window.

The p24 packet map is:

```text
python3 p24/p24_frobenius_packet_map.py
```

For the third trace it reports:

```text
quotient_m packet_count = 28
subgroup_n packet_count = 9
class_h packet_count = 10156
```

Thus quotient-factored constructions have a 28-packet normality target, but
arbitrary additive selectors still need the full annihilator or the direct
minimum-weight theorem.

The universal reduced-normality conjecture is false.  The focused CM failure
audit compiled and ran:

```text
python3 -m py_compile p24/reduced_normality_failure_audit.py
python3 p24/reduced_normality_failure_audit.py \
  --max-failures 3 --min-h 2 --max-h 12 --max-abs-D 350
```

Output:

```text
D=-216 q=103 ell=5 h=6 gcd_degree=1 zero_order=3 quotient_failure=3/2/2
D=-300 q=139 ell=7 h=6 gcd_degree=1 zero_order=2 quotient_failure=2/3/1
```

These are actual split ordinary CM reduced-normality failures, both low-order
degree-1 packet accidents.  They rule out any proof that relies only on
splitness, squarefreeness, or local normal-basis existence.

But they still do not create sparse additive projectors:

```text
python3 -m py_compile p24/failure_projector_weight_audit.py
python3 p24/failure_projector_weight_audit.py
```

Output:

```text
D=-216 q=103 h=6 quotient_m=2 subgroup_n=3 projector_weight=3 best_weight=3
D=-216 q=103 h=6 quotient_m=3 subgroup_n=2 projector_weight=2 best_weight=2
D=-300 q=139 h=6 quotient_m=2 subgroup_n=3 projector_weight=3 best_weight=3
D=-300 q=139 h=6 quotient_m=3 subgroup_n=2 projector_weight=2 best_weight=2
```

So reduced normality can fail while the exact support barrier remains true.
This makes the minimum-weight theorem a strictly sharper target than full
normality.

However, the minimum-weight theorem is not a universal coding theorem.  I
added and ran:

```text
python3 -m py_compile p24/cyclic_code_min_weight_counterexample.py
python3 p24/cyclic_code_min_weight_counterexample.py
```

It gives:

```text
q=7, h=6, quotient_size=2, subgroup_size=3
quotient_characters=[0,3]
vanished_nonquotient_characters=[1,4]
projector_weight=3
best_weight=2
```

So a structured multi-packet annihilator can lower support even when quotient
characters do not vanish.  The actual small CM failures do not have this
interaction, but p24 still needs arithmetic control of the CM annihilator, not
just a generic cyclic-code lemma.

The bounded scan

```text
python3 p24/cyclic_code_min_weight_scan.py \
  --max-h 18 --max-q 80 --max-vanished 3 --max-words 200000
```

reported `reductions=13`.  The first reductions all have the same pattern:
the vanished non-quotient characters contain a full translate of the quotient
character subgroup `Q_H`:

```text
h=4  m=2 vanished=[1,3]     projector 2 -> best 1
h=6  m=2 vanished=[1,4]     projector 3 -> best 2
h=8  m=2 vanished=[1,5]     projector 4 -> best 3
h=12 m=3 vanished=[1,5,9]   projector 4 -> best 3
```

I recorded the explanation in:

```text
p24/dual_coset_annihilator_lemma.md
```

If an annihilator contains a whole dual coset `a+Q_H`, then it has a codeword
supported on `H`, and `e_H+Ann(J)` can cancel `gcd(a,n)` positions.  For the
third p24 trace `n=3107441` is prime, so one harmful dual coset lowers support
by only one; a dramatic sparse selector would need many such cosets or a more
structured CM annihilator.

A fresh higher-`h` normality scan:

```text
python3 p24/reduced_resolvent_vanishing_scan.py \
  --max-cases 20 --min-h 12 --max-h 80 --max-abs-D 8000
```

reported:

```text
normal_rows=20
nonnormal_rows=0
quotient_dft_full_support_rows=23/23
```

The p24 theorem target is now more precise:

```text
either prove the p24 singular-modulus normal determinant is a p-adic unit
under hypotheses that exclude the small low-order failures,
or prove directly that e_H + Ann(J) has no word of support < 3107441
for the third-trace torsor.
```

No certificate or asymptotic speedup has been found yet.

I also closed the partial-window constructive shortcut for the oriented
composite target:

```text
python3 -m py_compile p24/partial_orbit_window_toy.py
python3 p24/partial_orbit_window_toy.py
```

The theorem is elementary: for cyclic `H=<a>`, a subset aggregate over
`S <= H` is invariant under the `H`-coset shift only if `aS=S`, hence
`S=H`.  In the `D=-5000` oriented composite toy (`3*17^(-1)`, index `6`, orbit
size `5`), partial window polynomials had distinct count:

```text
length 1: 30
length 2: 30
length 3: 30
length 4: 30
length 5: 6
```

So a short symmetric arc along the p24 move `2*463*223^(-1)` cannot replace
the full degree-`3107441` recovery object.

## 2026-06-04: harmful dual-cosets as relative resolvents

I refined the structured-annihilator obstruction again:

```text
p24/harmful_dual_coset_relative_resolvent_lemma.md
p24/harmful_dual_coset_relative_toy.py
```

Let `h=m n`, `H=<m>`, and `Q_H={0,n,2n,...}`.  For a dual coset `a+Q_H`,
write `i=u+m k`.  Then

```text
R_{a+r n}
  = sum_u zeta_h^(a u) zeta_m^(r u)
          [sum_k zeta_n^(a k) j_{u+m k}].
```

The `m` values `R_{a+r n}` are the quotient DFT of the fiberwise relative
sums

```text
P_u(a)=sum_k zeta_n^(a k) j_{u+m k}.
```

Therefore a full harmful dual-coset vanishing is equivalent to

```text
P_u(a)=0 for every quotient fiber u.
```

The toy verifier over fields with `mu_h` in the base field reports, for
example:

```text
python3 p24/harmful_dual_coset_relative_toy.py

q=31 h=30 m=6 n=5 a=1
forced_coset_resolvents_zero=True
relative_sums_zero=True
inverse_indicator_support=[0, 6, 12, 18, 24]
projector_weight=5
best_weight_after_one_character_coset=4
```

and the imprimitive check

```text
python3 p24/harmful_dual_coset_relative_toy.py --q 97 --h 24 --m 4 --a 2
```

has `gcd_a_n=2` and lowers projector weight from `6` to `4`, matching the
`gcd(a,n)` cancellation count.

For the third p24 target:

```text
m=66254
n=3107441
p mod n=2509452
ord_n(p)=388430
(n-1)/ord_n(p)=8
```

Since `n` is prime, a single algebraic harmful coset cancels only one
projector position.  Over `F_p`, however, Frobenius propagates it to `388430`
nontrivial relative `H`-characters, or `66254*388430=h/8` full class
characters.  The missing theorem is now:

```text
no Frobenius orbit of nontrivial relative H-characters has P_u(a)=0
on every quotient fiber u.
```

This is weaker than full reduced normality and more arithmetic than generic
cyclic-code minimum distance.  It still has not produced a certificate or an
asymptotic speedup.

I added a natural small-CM scan for the exact relative condition:

```text
p24/natural_relative_resolvent_scan.py
```

It chooses split primes `q` with `q == 1 mod h`, so all `h`-th roots of unity
are in the base field, and checks:

```text
R_{a+r n}=0 for all r   <=>   P_u(a)=0 for all u.
```

The 10-case lightweight run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 \
python3 p24/natural_relative_resolvent_scan.py \
  --max-cases 10 --min-h 12 --max-h 60 --max-abs-D 5000 \
  --max-quotients 4 --q-stop 30000
```

reported:

```text
rows=10
quotient_rows=32
harmful_a_total=0
all_equivalences_verified=1
```

This is evidence only, but it is now testing the exact fiberwise relative
vanishing statement rather than a generic normality proxy.

I also recorded the exact certificate target in:

```text
p24/relative_resolvent_content_certificate.md
```

For one Frobenius orbit with minimal polynomial `f_a`, define

```text
J_u(X)=sum_k j_{u+m k} X^k.
```

The harmful packet vanishes if and only if

```text
J_u(X) == 0 mod f_a(X)       for every u.
```

So the exact certificate is a content/Bezout certificate:

```text
sum_u B_u(X) J_u(X) == 1 mod f_a(X).
```

For p24 there are eight such nontrivial `H`-character orbits.  A product of
the `J_u mod f_a` terms would be a sufficient nonvanishing certificate, but
not an equivalent one, because the product vanishes if even one fiber is zero.

## 2026-06-04: relative-resolvent conjugacy and product boundary

I recorded the class-action form of the same target in:

```text
p24/relative_resolvent_conjugacy_boundary.md
```

Over the class field with `mu_n` adjoined, if

```text
Theta_a = sum_k zeta_n^(a k) sigma^(m k)(j_0),
```

then

```text
P_u(a) = sigma^u(Theta_a).
```

For a selected prime `frak P` above `p`, harmful vanishing is:

```text
Theta_a in intersection_u sigma^(-u)(frak P).
```

So the exact finite-field target is the content ideal generated by the
quotient conjugates.  The quotient norm/product

```text
product_u P_u(a)
```

is a simpler sufficient certificate: if it is nonzero mod `frak P`, no
harmful packet exists.  But it is not equivalent, because one zero fiber makes
the product vanish while the harmful event requires all fibers to vanish.

I also expanded and instrumented the natural relative scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 \
python3 p24/natural_relative_resolvent_scan.py \
  --max-cases 100 --min-h 12 --max-h 96 --max-abs-D 20000 \
  --max-quotients 6 --q-stop 250000 --summary-only
```

It reported:

```text
rows=100
quotient_rows=317
relative_characters_tested=1268
relative_fibers_tested=4269
harmful_a_total=0
individual_zero_fiber_total=0
expected_random_zero_fibers=1.751551
all_equivalences_verified=1
```

and every quotient row had `min_nonzero_fibers=quotient_size`, so the stronger
individual-fiber product condition held in all tested natural CM cycles.  The
random baseline expected only about `1.75` individual zero fibers, so this is
useful calibration, not a standalone theorem.

The finite-field modular-zero lemma gives a conditional no-go: if
`Theta_a` could be realized as a low-pole rational modular function, vanishing
on the whole CM torsor would force a global mod-`p` identity.  The obstruction
is that realizing the order-`n` relative sum without a seed already requires
the embedded quotient/recovery data or a high-degree correspondence; compact
class-field notation does not lower the pole degree.

The sharper pole count is:

```text
third target quotient fibers m = 66254
relative fiber length n = 3107441
Frobenius packet degree ord_n(p) = 388430
n * ord_n(p) = 1207023307630
```

Thus the natural relative character projection is far above the pole-degree
threshold needed for the zero lemma on the `m` quotient fibers.

I also consolidated the first-trace order-19 version in:

```text
p24/order19_relative_content_boundary.md
```

The useful fact is `p == -1 mod 19`, so the Fourier/Kummer layer is quadratic.
The audits show this only gives a normal form after the embedded quotient
ordering is known:

```text
order19_kummer_shortcut:
  zeta_19 in F_p^2 diagonalizes known periods but does not construct them;

order19_ring_ray_sequence:
  conductor-19/ray kernels are 18, 9, 162, ... rather than the unramified
  degree-19 quotient;

order19_power2_level:
  X0(2^19) has small map degree 786432, but the horizontal edge has full
  class orbit;

order_l_kummer_phase_toy:
  unordered quotient period sets admit multiple Kummer constants.
```

So order-19 remains the cleanest theorem toy for a phase-aware identity, but
it is not a p24 certificate route by itself because the recovery degree is
`14670196166`.

I tested and corrected a tempting algebraic shortcut for the stronger product
condition:

```text
p24/relative_product_noninvariance_boundary.md
p24/relative_product_noninvariance_toy.py
```

For fixed `a`,

```text
R_{a+r n}
  = sum_u zeta_h^(a u) zeta_m^(r u) P_u(a),
```

This is an invertible Fourier transform, so it preserves the zero vector.  It
does not preserve coordinate products.  The toy verifies that the naive
identity

```text
prod_r R_{a+r n} ?= unit * prod_u P_u(a)
```

is false.

Thus there are two different strong sufficient certificates:

```text
relative product:
  every P_u(a) is nonzero;

dual-coset group determinant product:
  every R_{a+r n} is nonzero.
```

Both imply the exact content condition, but neither is equivalent to it or to
the other.

I then sharpened the same condition in split-algebra language:

```text
p24/relative_resolvent_split_algebra_theorem.md
p24/relative_resolvent_split_algebra_toy.py
```

For

```text
Theta_a = sum_k zeta_n^(a k) sigma^(m k)(j_0),
```

the component at `sigma^(u+m*l)P` is

```text
zeta_n^(-a*l) P_u(a).
```

Thus `b` zero quotient fibers give exactly `b*n` zero split components.  A
harmful all-fiber event is equivalent to `Theta_a` being zero in the entire
split class algebra modulo the selected cyclotomic prime.  This turns the
missing theorem into a p-adic unit statement for one representative of each
of the eight p24 relative-character Frobenius orbits.

The crude norm-height route still fails: full harmful vanishing forces
`p^h` split-prime divisibility of `Norm(Theta_a)`, but the principal singular
modulus has log-size about `2.54e12`, far above the per-quotient threshold
`m*log(p) ~= 3.64e6`.

I also made the finite split-algebra implication Lean-checkable:

```text
p24/lean/RelativeResolvent.lean
```

This is a core-Lean proof, not a CM proof.  It verifies the abstract finite
step: if level-zero components are the relative fiber values and a zero fiber
forces its whole split block to vanish, then all split components vanish if
and only if all relative fibers vanish.

The first useful scalar sufficient certificate is the relative energy:

```text
p24/relative_energy_certificate.md
p24/relative_energy_certificate_scan.py
```

For

```text
E_a = sum_u P_u(a) P_u(-a),
```

harmful vanishing implies `E_a=0`, so `E_a != 0` rules it out.  Expanding gives
both an autocorrelation transform and a safe Parseval identity:

```text
E_a = sum_d zeta_n^(a*d) C_d,
C_d = sum_i j_{i+m*d}j_i,
sum_r R_{a+r*n}R_{-a-r*n}=mE_a.
```

A 100-case toy CM scan checked the identities and found:

```text
quotient_rows=317
characters_tested=1268
harmful_total=0
energy_zero_total=0
expected_random_energy_zeros=0.576654
```

I then tested whether the autocorrelation sequence `C_d` might have a short
recurrence:

```text
p24/relative_energy_recurrence_boundary.md
p24/relative_autocorrelation_complexity_scan.py
```

The corresponding 100-case scan found:

```text
rows=237
full_or_near_full_bm_rows=237
low_bm_rows=0
full_dft_support_rows=237
total_energy_zeros=0
```

So the energy target is a cleaner scalar theorem, but no low-recurrence or
sparse-spectrum shortcut is visible at toy scale.

I refined the scalar packet degree:

```text
p24/energy_real_cyclotomic_packet_audit.py
```

For the p24 third trace,

```text
p^(388430/2) == -1 mod 3107441.
```

Since `C_d=C_-d`, each scalar `E_a` lives in the real cyclotomic packet of
degree `194215`, not the full content-vector degree `388430`.  The number of
packets remains eight because `-a` is already in the Frobenius orbit.

I then checked the Hecke/Brandt interpretation:

```text
p24/hecke_autocorrelation_boundary.md
p24/hecke_autocorrelation_toy.py
p24/agent_brandt_energy_sidecar.md
p24/agent_brandt_energy_probe.py
```

The exact identity

```text
C_d = Tr(J * P_{m*d} * J * P_{-m*d})
```

is valid once the oriented class-action permutation is known.  Ordinary
unoriented Hecke data gives packets such as `2*C_1`, and Hecke walk moments
recover `C_d` by triangular/Chebyshev inversion.  But this is a repackaging,
not a shortcut: the toy moment sequence has no short recurrence visible, and
the Brandt probe has full relative BM complexity and DFT support.

Trace-formula sidecar:

```text
p24/agent_traceformula_energy_sidecar.md
```

Known global CM trace, genus-twisted trace, Gross-Zagier/Borcherds product,
and relative trace formula tools either erase the order-`3107441` phase or
move it to a discriminant-scale automorphic object.  They do not currently
prove the selected p24 mod-`p` nonvanishing of the energy scalars.

## 2026-06-04: exact X0/X1 tail entropy

I sharpened the direct verifier half-level obstruction:

```text
p24/x0_x1_tail_entropy_theorem.md
p24/x0_x1_tail_entropy_audit.py
```

Even if an `X0`/tower construction has already supplied the oriented branch

```text
lambda == 1 mod 2^h,
```

there are exactly `2^(40-h)` lifts modulo `2^40`.  Only one lift is the true
`X1` orientation `lambda == 1 mod 2^40`; two lifts have the strict trace
residue `lambda+p/lambda == p+1 mod 2^40`, the second being the non-`X1` root
with `v2(lambda-1)=39`.

The proof is a short 2-adic calculation.  Write

```text
lambda = 1 + 2^h u,       p = 1 + 2c, c odd.
```

The strict trace condition is

```text
(lambda-1)(lambda-p) == 0 mod 2^40.
```

Since `h>=2`, `v2(lambda-p)=1`, so `u` must be `0` or
`2^(39-h) mod 2^(40-h)`.  Dividing
`lambda+p/lambda-(p+1)` by `2^(h+1)` gives a power series with odd linear
coefficient `(1-p)/2`, hence the trace-tail map is 2-to-1 and has
`2^(39-h)` residues.

The audit output includes:

```text
h=20 lifts=1048576 trace_residues=524288 strict_trace_lifts=2 true_x1_lifts=1
```

So the half-level `p^(1/4)` dream has an exact remaining `2^(k-h)` true-X1
tail.  This is not a statistical artifact of the small-field scans.

## 2026-06-04: hybrid trace/verifier route refreshed

I revisited the idea of avoiding CM root selection by combining exact
trace-residue information with the verifier equation:

```text
p24/hybrid_trace_verifier_boundary.md
```

The post-trace calibration, rerun with the bundled Python runtime, confirms
that `x0` is cheap after a strict trace `A` is known:

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/post_trace_construction_audit.py \
  --min-p 10000 --max-p 120000 --max-rows 8 --details

target_trace_A=12048
strict_good_A=8424
accepted_x_total=821248
target_A_over_sum_sqrt=8.754736
strict_A_over_sum_sqrt=6.121340
avg_x_per_strict_A=97.489079
```

The exact trace-residue oracle rerun:

```text
python3 p24/exact_trace_residue_oracle_tradeoff.py
```

again found pure `2^40` best among sampled levels:

```text
level=1099511627776
survivors=6
gamma0_over_sqrt=1.649267
oracle_proxy_over_sqrt=1.649267
```

Thus the hybrid route still trades between a fixed-trace CM selector and a
marked `X1(2^40)` ray selector.  It does not provide a third sub-sqrt
primitive.

The ray-degree audit makes the rule of thumb explicit:

```text
do not include Z_k in the CM quotient construction.
```

For the third trace, adding the x-only `2^40` ray orientation multiplies by
`2^38`:

```text
h * 2^38 = 56591972337130160521216 = 5.659197e10 * sqrt(p)
66254 * 2^38 = 18211760846667776 = 1.821176e4 * sqrt(p)
```

Thus even the dream degree-`66254` unmarked quotient becomes far too large if
it is marked by the verifier ray.  The viable split remains: construct
target-trace `A` first, then find `x0` afterward.

The upstream-data side probe also fits this conclusion.  Full small-triple
data shows exact constant symmetries

```text
x -> 1/x,
(A,x) -> (-A,-x),
```

and constant terminal filters such as `chi(A-2)=-1`, `chi(A+2)=+1`, but no
stable low-degree formula, recurrence, pair relation, or growing `A,x0`
invariant.  The only real finite-field identity remains the near-square
`D=-7` trace `+-2n`, and for p24 its relevant 2-adic valuation is only `3`,
not `40`.

## 2026-06-04: ordered composite chains still lack the subgroup projector

I sharpened the oriented-composite boundary in:

```text
p24/ordered_chain_stabilizer_boundary.md
```

Question: if plain `X0(206498)` forgets the sign of
`2*463*223^(-1)`, can an ordered chain of `2`, `223`, and `463` isogenies
retain the orientation cheaply and expose the degree-`66254` quotient?

Answer: it can retain orientation, but it still sees a finite path translated
through the full CM orbit.  A finite ordered path invariant has a stabilizer
only from translations preserving its finite labeled support.  Generically
that stabilizer is trivial.  To be invariant under the p24 move

```text
a = 2 * 463 * 223^(-1),
order(a)=3107441,
```

the support must contain the whole `<a>` orbit.  That is exactly the
degree-`3107441` subgroup aggregation/recovery object.

The `D=-5000` oriented-composite toy supports this:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_path_edge_pair_sums=30
component_count=6
distinct_period_sums=6
```

The partial-window rerun gives the same message at polynomial level:

```text
window_length=1..4 distinct_window_polys=30
window_length=5    distinct_window_polys=6
```

So ordered sign-chain data is not the missing theorem.  It is only a local
orientation input to the still-needed relative period construction.

## 2026-06-04: prescribed-order algorithm caveat

I checked the primary Bröker-Stevenhagen prescribed-order paper to make sure
we are not missing a known polynomial-time fixed-trace construction:

```text
p24/prescribed_order_variable_field_caveat.md
```

The efficient algorithm takes a desired order `N` and chooses a suitable prime
field `F_p` and small discriminant.  It explicitly says the constructed prime
field is typically different from `F_N`.  In the fixed-field formulation, with
`N=p+1-t`, the discriminant is

```text
Delta = t^2 - 4p,
```

and for most traces the field discriminant has the same scale as `p`.  That is
exactly the p24 situation.  So these algorithms do not bypass the fixed p24
large-CM-root selector.

## 2026-06-04: Lean is now useful for the finite certificate layer

I added a second Lean-core file:

```text
p24/lean/CertificateLogic.lean
```

It checks the abstract implication graph around the missing theorem:

```text
invertible finite transform preserves all-zero vectors;
content/Bezout certificate => packet is not all zero;
product nonzero => packet is not all zero;
energy nonzero => no harmful packet, provided harmful vanishing forces E_a=0;
all orbit certificates => no harmful Frobenius packet remains.
```

Together with

```text
p24/lean/RelativeResolvent.lean
```

this gives Lean-checked coverage for the finite indexing/logical reductions.
It still deliberately does not assert the p24 arithmetic nonvanishing theorem.
The open theorem remains: prove one content or energy nonvanishing statement
for each of the eight selected relative-character Frobenius packets.

## 2026-06-04: decomposition-field packet norm sharpens the energy target

I added:

```text
p24/decomposition_field_packet_norm_theorem.md
p24/cyclotomic_packet_norm_toy.py
```

The new theorem target packages the eight p24 energy packet checks into one
degree-8 decomposition-field p-unit statement.  For

```text
n = 3107441,
ord_n(p) = 388430,
p^(388430/2) = -1 mod n,
```

the real energy packet degree is `194215`, and the decomposition field

```text
M^+ = Q(zeta_n + zeta_n^-1)^<p>
```

has degree `8`.  If

```text
Xi_E = Norm_{E^+/M^+}(E_1),
```

then its eight residues at primes above `p` are the eight finite-field packet
norms.  So the energy route can be stated as:

```text
p does not divide Norm_{M^+/Q}(Xi_E).
```

The toy check uses the calibrated `D=-5000`, `h=30`, `q=1259` cycle with
`m=6`, `n=5`, and `q=-1 mod 5`, so the CM roots are in the base field but the
relative roots of unity are quadratic packets.  It found:

```text
packet_norms = 707, 68 mod 1259
product_of_packet_norms_mod_q = 234
all_packet_energies_nonzero = 1
```

This is a cleaner p-adic target, not yet a certificate: computing or proving
the p-unit status of `Xi_E` still requires the non-genus autocorrelation
primitive.

## 2026-06-04: packetized relative-content scan without base roots of unity

I added:

```text
p24/packetized_relative_content_scan.py
p24/packetized_relative_content_scan.md
```

This implements the exact finite-field content certificate in the p24 shape:

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1,
```

where `f_a` is an irreducible Frobenius packet factor of `Phi_n` over the
base field.  Unlike the early DFT scans, it does not require `mu_n` in the
base field.

The calibrated `D=-5000`, `h=30`, `m=6`, `n=5`, `q=1259` row has two
quadratic packets and both have:

```text
content_gcd_degree=0
energy_zero=0
packet_norm_zero=0
```

A 50-row summary run found:

```text
packet_rows=126
nonlinear_packets=82
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
```

Side-agent findings agree with the boundary: generic cyclic-code or ordinary
split-CM normality theorems are false, because small reduced-normality and
minimum-weight failures exist.  The positive theorem must be selected-prime
p24 arithmetic, not pure finite-field linear algebra.

## 2026-06-04: energy is not implied by content

I added:

```text
p24/energy_gram_isotropy_boundary.md
p24/energy_isotropy_obstruction_toy.py
```

The energy polynomial satisfies the Gram identity

```text
C(X) = sum_u J_u(X)J_u(X^-1),
```

so harmful all-zero content implies energy zero.  The converse fails in the
same packet algebra.  In the calibrated quadratic packet field

```text
q=1259,
f=X^2+36X+1,
```

the toy finds

```text
y = 3 + 647X,
Norm(y) = -1 mod 1259,
energy(1,y) = Norm(1)+Norm(y) = 0.
```

Thus:

```text
content nonzero does not imply energy nonzero.
```

The degree-8 decomposition-field energy norm remains attractive, but it must
be proved using the specific p24 CM/autocorrelation structure, not by generic
Hermitian linear algebra or as a corollary of the exact content certificate.

## 2026-06-04: Hermitian-positive energy variant

I added:

```text
p24/hermitian_energy_certificate.md
p24/complex_energy_positivity_boundary_toy.py
```

The ordinary energy

```text
E_a = sum_u P_u(a)P_u(-a)
```

is not the positive complex norm of the relative-content vector.  Complex
conjugation sends quotient fiber `u` to the inverse quotient fiber with a
root-of-unity carry:

```text
u* = -u mod m,
c(u) = (u+u*)/m,
conj(P_u(a)) = zeta_n^(a*c(u)) P_{u*}(a).
```

So the positive scalar is

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a)P_{u*}(a) = sum_u |P_u(a)|^2
```

in characteristic zero.  The complex toy confirms the indexing:

```text
max_conjugation_error=3.797e-15
energy_equals_positive=0
positive_equals_abs_square=1
```

I patched `p24/packetized_relative_content_scan.py` to compute this Hermitian
packet scalar too.  The 50-row summary now reports:

```text
packet_rows=126
nonlinear_packets=82
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This gives a third live sufficient certificate target:

```text
prove the degree-8 decomposition-field norm of the p24 Hermitian energy is a
p-unit.
```

It has better characteristic-zero behavior than the ordinary energy, but the
selected-prime p-adic unit gap remains.

## 2026-06-04: Hermitian positivity does not close the p-unit gap

I added:

```text
p24/hermitian_energy_height_gap_audit.py
```

The Hermitian energy is positive in characteristic zero, but the p24
certificate needs a unit at a selected split prime over

```text
p = 10^24 + 7.
```

For the third target the audit reports:

```text
log_p = 55.262042
log_principal_j_bound = 5.076699e12
log_Hermitian_energy_bound = 1.015340e13
real_packet_degree = 194215
decomposition_field_degree = 8
log_one_decomposition_prime_norm_bound = 1.971942e18
one_prime_bound_over_log_p = 3.568349e16
required_one_prime_height_reduction = 2.802417e-17
```

Thus a norm-height lifting proof would need an astronomically strong
structural height cancellation, not a class-invariant constant factor.  The
Hermitian scalar remains the nicest scalar target, but proving it is a p-unit
is still the same selected-prime non-genus arithmetic problem.

I also ran the packetized scan in the low-order CM failure regime:

```text
--max-cases 40 --min-h 2 --max-h 30 --max-abs-D 2000
--max-quotients 4 --min-n 2 --q-stop 50000
```

It found:

```text
packet_rows=70
nonlinear_packets=36
content_failures=0
energy_zero_packets=2
packet_norm_zero_packets=2
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This is a useful prioritization signal: the ordinary scalar energy has natural
small CM failures, while the Hermitian-positive scalar survived the same
scan.  It is still not a theorem, because finite-field Hermitian forms are
isotropic in general.

I made that isotropy/probability statement exact in:

```text
p24/hermitian_isotropy_probability_audit.py
p24/hermitian_isotropy_probability_audit.md
```

For one p24 Hermitian packet,

```text
Q = p^194215,
m = 66254,
H(v)=sum_i v_i v_i^Q.
```

The number of zero vectors in `F_{Q^2}^m` is

```text
Q^(2m-1) + (-1)^m (Q-1)Q^(m-1),
```

so the random failure probability is about `Q^-1`.  The audit reports:

```text
log10_zero_probability≈-4.661160e6
log10_union_bound_8_packets≈-4.661159e6
```

It also brute-force validates the count over `F_9` for `m=1,2,3`.

## 2026-06-04: Hermitian principal dominance proves complex nonzero

I added:

```text
p24/hermitian_principal_dominance_audit.py
p24/hermitian_principal_dominance_theorem.md
```

For the third p24 target, the `u=0` relative fiber

```text
P_0(a) = sum_k zeta_n^(a*k) j_{m*k}
```

contains the principal singular modulus with coefficient `1`.  Every other
term has reduced-form denominator at least `2`, so the standard

```text
||j(tau)| - exp(pi*sqrt(|Delta|)/a)|| <= 2079
```

bound proves principal-term dominance.  The audit reports:

```text
log_principal_lower=5.076699e12
log_fiber_other_sum_upper=2.538350e12
p0_dominance_margin=2.538350e12
log_Hermitian_embedding_lower=1.015340e13
```

Therefore every Hermitian packet is nonzero in characteristic zero by an
overwhelming margin.  This sharpens, but does not solve, the target: the only
remaining issue is whether that huge positive algebraic number is divisible
by the selected split prime above `p`.

## 2026-06-04: Hermitian scalar does not factor through quotient periods

I added:

```text
p24/hermitian_internal_character_boundary.md
p24/hermitian_not_quotient_period_invariant_toy.py
```

This tests whether the preferred Hermitian packet scalar might be computable
from the quotient period vector alone:

```text
y_u = J_u(1).
```

The toy works over `F_101` with `h=10`, `m=2`, `n=5`.  It constructs two
datasets with identical quotient periods:

```text
quotient_periods_a=[1,1]
quotient_periods_b=[1,1]
```

but different nontrivial relative fibers and Hermitian packets:

```text
relative_fibers_a=[1,1]
relative_fibers_b=[1,95]
hermitian_packet_a=96
hermitian_packet_b=88
```

Conclusion: the Hermitian scalar is not determined by the degree-`m` quotient
period polynomial.  It remains a scalar version of the internal order-`n`
relative-character problem.

## 2026-06-04: Correspondence zero-lemma window tested

I added:

```text
p24/correspondence_zero_window_audit.py
p24/correspondence_zero_lemma_window.md
```

Conditional route: if a weighted relative trace along a class element of
order `n` can be realized as a nonzero modular/correspondence function with
pole degree at most `n * delta`, then harmful vanishing on all quotient
fibers would force vanishing on all `h` CM points.  The finite-field zero
lemma would rule this out if

```text
n * delta < h,
```

equivalently, for quotient index `m=h/n`,

```text
delta < m.
```

The audit searches small signed split-prime products for the third p24 trace,
using the squarefree `X0` index as an optimistic lower proxy for `delta`.

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/correspondence_zero_window_audit.py \
  --prime-bound 1000 --max-factors 4 --max-norm 250000 --show 12
```

Output:

```text
hits=16550
zero_lemma_window_hits=0
```

The useful balanced row remains

```text
2 * 463 * 223^(-1):
  delta = 311808
  m = 66254
  delta/m = 4.706252
  n = 3107441
  seeded/sqrt = 0.968925
```

So even the optimistic unoriented degree misses the divisor-counting window;
real orientation costs can only make it worse.  This closes the bounded
split-correspondence zero-lemma shortcut.  The surviving routes remain the
Hermitian p-unit/content theorem or a genuinely new embedded non-genus period
formula.

I later sharpened this by adding:

```text
p24/low_norm_order3107441_search.md
```

The zero-lemma window would require an order-`3107441` class representative
with correspondence degree below `m=66254`, hence at least a norm-`<=66254`
ideal representative.  I ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/composite_split_cycle_audit.py \
  --prime-bound 66254 --max-factors 1 --max-norm 1 \
  --exhaustive-norm 66254 --show 12
```

This computed logs for all `3270` split rational primes up to `66254` and
enumerated signed split-prime-power products of norm at most `66254`.

```text
index_66254: none
```

The small ramified prime `599` has class log `102940198007`, i.e. order `2`,
and including it still gave no index-`66254` hit.  Therefore the zero-lemma
failure is not just a squarefree-search artifact.

I then added:

```text
p24/atkin_zero_window_search.py
p24/atkin_zero_window_boundary.md
```

This applies the most generous squarefree Atkin-Lehner quotient proxy

```text
delta_AL = ceil([SL2:Gamma0(N)] / 2^omega(N)).
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/atkin_zero_window_search.py \
  --prime-bound 100000 --norm-bound 200000 --show 8
```

Output:

```text
index=314:   atkin_zero_window_hits=0, best delta_AL=339
index=422:   atkin_zero_window_hits=0, best delta_AL=690
index=66254: atkin_zero_window_hits=0
```

The index-314 layer is a near miss (`339 > 314`) but still does not make the
zero lemma fire.

## 2026-06-04: Degree-157 refinement isolated as next positive target

Planck's side pass agreed that the best surviving positive route is the
third-trace oriented composite class-character period theorem, not another
bounded local identity.  I added:

```text
p24/degree157_refinement_target.md
```

This isolates the first non-genus step:

```text
G / <g^2>          degree 2       genus layer
G / <g^(2*157)>    degree 314
relative degree    157
```

The exact data is:

```text
h / 2       = 102940198007
h / 314     = 655670051 = 211 * 3107441
p mod 157   = 21
ord_157(p)  = 156
```

The root-of-unity field is cheap.  The missing theorem is an embedded
relative child relation

```text
F_157(Z,Y)
```

of degree `157` in `Y`, paired to the `j`-torsor, without class enumeration.
This is the first odd phase that any successful third-trace quotient tower
must supply.

## 2026-06-04: Larger Hermitian/content packet scan

At Banach's recommendation I ran a broader, still bounded, small-CM scan
focused on nonlinear Frobenius packets:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packetized_relative_content_scan.py \
  --max-cases 120 --min-h 30 --max-h 150 --max-abs-D 50000 \
  --max-quotients 5 --min-n 5 --q-stop 600000 --summary-only
```

Output:

```text
rows=120
packet_rows=272
nonlinear_packets=178
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This is still evidence, not a certificate.  It strengthens the empirical case
that the exact relative-content gcd theorem and the Hermitian packet p-unit
theorem are the right positive statements: the scan includes more nonlinear
packets and finds no failures, while the low-order scan already showed that
ordinary energy can fail where Hermitian energy does not.

## 2026-06-04: CM subfield/tower route sharpened

I added:

```text
p24/cm_subfield_tower_boundary.md
```

This separates the genuinely positive version of the modern CM-subfield idea
from the abstract-tower trap.

The route would solve the p24 construction if it supplied a class invariant
`f` with:

```text
stabilizer in Cl(O_K) = <g^66254>
degree of f-polynomial = 66254
degree in j of recovery relation = 3107441
embedded pairing over F_p between f-roots and j-recovery factors
```

That would be an honest sub-sqrt construction.  But generic CM subfield/tower
support does not allow us to request an arbitrary class subgroup.  The
subfield is determined by the chosen modular function through Shimura
reciprocity and congruence data.  Existing local audits still show:

```text
genus data handles only the top factor 2;
ray/unit distribution does not touch the unramified 157/211 phases;
X0/eta/Atkin edge invariants have full class orbit unless aggregated;
abstract bnrclassfield towers split over F_p but are unpaired with j.
```

I reran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/class_invariant_stabilizer_audit.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/class_invariant_lifting_height_audit.py
```

The stabilizer audit confirms that the p24 desired stabilizer/recovery degrees
are excellent:

```text
stabilizer_size=3107441
quotient_degree=66254
largest_degree_over_sqrt=3.107441e-06
```

but low-level split-prime edge invariants still carry the full class orbit.
The toy calibration has `D=-5000`, `h=30`; all tested X0 edge sums/products
have `30` distinct values, while the subgroup quotient has degree `6` only
after explicit subgroup aggregation.

So CM subfield/tower algorithms remain a precise open target, not a completed
construction: they must identify a p24-specific embedded invariant with the
right stabilizer and relation back to `j`.

I also extended:

```text
p24/ray_kernel_distribution_audit.py
p24/unit_distribution_obstruction.md
```

to check the composite squarefree levels that could have hidden the odd phase:

```text
33127  = 157*211
66254  = 2*157*211
206498 = 2*223*463
103249 = 223*463
```

Their local unit parts contain neither `157` nor `211`; for example

```text
206498: {2:4, 3:4, 7:2, 11:2, 37:2}
```

So composite ray levels tied to the quotient or the oriented split
correspondence also do not supply the unramified `157/211` phases through
ray-kernel distribution.

I also added and ran:

```text
p24/cm_package_subfield_pairing_audit.md
p24/abstract_vs_embedded_quotient_toy.py
p24/abstract_embedded_pairing_non_genus_toy.py
```

The degree-2 toy has abstract roots `[10,93]` and embedded cycle-sum roots
`[4,29]` over `F_103`; the abstract polynomial leaves two possible pairings.
The degree-5 non-genus toy has abstract roots and embedded period sums over
`F_2243`, but no affine or Mobius set map between them.  This supports the
same conclusion: an abstract subfield polynomial or tower is not enough
without an explicit `R(alpha,j)` pairing.

## 2026-06-04: Relative product target is too strong in small CM

I added:

```text
p24/relative_product_too_strong_scan.md
```

A broader natural relative-resolvent scan found no harmful all-fiber
collapses, but did find one individual zero fiber:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/natural_relative_resolvent_scan.py \
  --max-cases 160 --min-h 12 --max-h 120 --max-abs-D 40000 \
  --max-quotients 6 --q-stop 400000 --summary-only
```

Output:

```text
rows=160
quotient_rows=520
relative_characters_tested=2150
relative_fibers_tested=7337
harmful_a_total=0
individual_zero_fiber_total=1
expected_random_zero_fibers=2.908526
all_equivalences_verified=1
```

The row was:

```text
D=-1336, q=1777, ell=5, h=12, m=2, n=6.
```

In that row, the zero occurs for `a=1`:

```text
relative_fibers=[1400, 0]
ordinary_pairing=1746
hermitian=1746
```

So the product certificate fails but the Hermitian scalar remains nonzero.

Conclusion: proving `prod_u P_u(a) != 0` is too strong as a universal CM
theorem.  The exact content theorem remains viable and is better aligned with
the harmful condition.  The Hermitian packet scalar also remains preferred
because the packetized scans have found no Hermitian packet zeros.

## 2026-06-04: Principal dominance is not a p-adic selector

I added:

```text
p24/hermitian_padic_principal_boundary.md
```

This records the p-adic interpretation of the Hermitian principal-dominance
theorem.  Complex principal dominance proves the packet is nonzero over
characteristic zero.  It does not select a prime above `p`, and reducing the
principal singular modulus modulo a completely split prime is equivalent to
choosing one embedded CM root.  Therefore the missing theorem is still a
selected-prime p-unit/content statement, not an archimedean dominance
statement.

## 2026-06-04: Direct ell=2897 degree-157 target calibrated

I added:

```text
p24/direct_degree157_quotient_target.md
```

The first odd non-genus layer can be posed either as the tower refinement

```text
G/<g^2> -> G/<g^(2*157)>
```

or directly via the split prime

```text
ell=2897, order([ell])=1311340102, index([ell])=157.
```

The direct route is a clean theorem toy, but not the best certificate path:

```text
Gamma0(2897) proxy = 2898
direct recovery degree = 1311340102
seeded proxy = 3800263615596 = 3.800264 * sqrt(p)
```

The balanced oriented composite target remains better:

```text
quotient degree = 66254
recovery degree = 3107441
seeded proxy = 968924963328 = 0.968925 * sqrt(p)
```

Fast audits rerun:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/odd_level_invariant_degree_audit.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/seedless_cycle_resultant_audit.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/p24_split_cycle_selector_audit.py --prime-bound 20000
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tower_phase_refinement_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/relative_tower_character_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_pairing_non_genus_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/p24_abstract_classfield_quotient_probe.py
```

The `D=-5000, h=30=2*3*5` tower toy gives a positive shape theorem: once the
embedded cycle is known, a degree-3 child relation above the genus parent is
constructed and equivalent to relative class-character traces.  The
`D=-2239, h=35` non-genus abstract-pairing toy gives the negative control:
abstract quotient roots and embedded period roots both split, but have no
affine or Mobius set pairing.

Socrates the 2nd added another small analogue:

```text
D=-711, q=727, h=20=2*5*2, ell=2.
```

It has a genus parent followed by degree-5 child polynomials:

```text
top_periods=[635, 334]
parent 0 child polynomial=[372, 709, 415, 16, 92, 1]
parent 1 child polynomial=[338, 93, 520, 109, 393, 1]
wrong_parent_cross_zeros=0
```

Again, abstract degree-5 quotient roots do not pair with the embedded child
sets by affine or Mobius maps.

Conclusion: direct `ell=2897` is useful as the minimal first-odd-layer
question, but it does not remove the missing embedded non-genus phase theorem.

## 2026-06-04: Probability lift boundary sharpened

Cicero the 2nd added:

```text
p24/subagent_probability_lift_sidecar.md
```

The statistical verdict is that random/Hermitian models make failure
astronomically unlikely but do not certify the fixed selected prime above
`p=10^24+7`.

For one p24 Hermitian packet,

```text
Q = p^194215
log10 Pr[H_a = 0] ~= -4661160
```

and packetized small-CM scans continue to show:

```text
content_failures=0
hermitian_zero_packets=0
```

But Chebotarev, second moments, concentration, Schwartz-Zippel, and random
Hermitian-form models average over primes, characters, or random packets; they
do not identify the selected finite-field embedding.

The probability-shaped theorem that would actually close the certificate is
therefore a p-unit theorem:

```text
For every nontrivial relative-character Frobenius packet a,
H_a mod P != 0
```

for the selected decomposition prime `P | p`, or the exact vector form

```text
(J_0 mod f_a, ..., J_{m-1} mod f_a) != 0.
```

Any bound of the form

```text
#{sigma : H_a(sigma P) = 0} <= C*h/Q < 1
```

would also suffice, but standard square-root cancellation or density is not
strong enough unless it forces the integer zero count to be zero.

## 2026-06-04: ell=677 component quotient isolated

I added:

```text
p24/ell677_component_quotient_boundary.md
```

The split prime `ell=677` gives the best first-odd-layer fixed-instance
certificate shape:

```text
order([677]) = 655670051 = 211 * 3107441
index([677]) = 314 = 2 * 157
Gamma0(677) proxy = 678
seeded proxy = 444544294578 = 0.444544 * sqrt(p)
```

If the 314 component sums of the horizontal 677-isogeny graph were
constructible without enumerating the CM vertices, that would already be a
sub-sqrt route for p24.  But those components are exactly the quotient
`G/<g^314>`, i.e. genus followed by the first odd `157` refinement.

Fast toys rerun:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/split_cycle_quotient_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/seedless_cycle_elimination_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/period_moment_idempotent_toy.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/non_genus_twisted_trace_level_audit.py
```

The split-cycle toy confirms that whole cycles have the quotient degree but
edge values retain the full orbit.  The elimination toy recovers cycle sums
only when `H_D` is supplied.  The moment toy shows direct period moments are
convolutions of the same high-order character traces.  The modular-form audit
puts non-genus trace formulas at discriminant-scale level.

Conclusion: `ell=677` is the most useful intermediate success criterion, but
it packages the same missing embedded non-genus phase theorem rather than
removing it.

Aristotle the 2nd added the sharper seedless control, which I made
reproducible as:

```text
p24/unfiltered_phi_cycle_toy.py
```

For `D=-87`, `q=103`, `ell=7`, eliminating with `H_D` gives the two target
cycle sums `[4,29]`.  Removing `H_D` and using only universal `Phi_7`
3-cycles gives:

```text
universal_cycle_sums=[4, 9, 28, 29, 50, 55, 65, 76, 80, 88]
CM_cycle_sums=[4, 29]
```

Thus the modular closed-cycle equation contains the target components but does
not select the fixed CM order.  The fixed-order filter is exactly the embedded
relation or class-field phase theorem we still need.

## 2026-06-04: Quotient-spectrum support gate formalized

I revisited the additive support route:

```text
p24/quotient_spectrum_support_theorem.md
p24/quotient_spectrum_support_toy.py
```

The useful restricted theorem is:

```text
If an additive selector is already supported on the quotient characters Q_H,
and quotient-packet nonvanishing lets us cancel A*J=e_H*J on Q_H,
then A=e_H.
```

The larger bounded toy run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/quotient_spectrum_support_toy.py \
  --max-h 36 --max-q 500 --max-q-degree2 101
```

reported:

```text
rows=1600
nonquotient_factor_rows=1205
nonquotient_reduced_rows=0
quotient_factor_rows=395
quotient_reduced_rows=0
```

I added the finite support gate in:

```text
p24/lean/QuotientSupport.lean
```

This is not the missing p24 certificate; it cleanly separates two obligations.
For quotient-factored constructions, the exact relative-content packet
nonvanishing is enough.  For arbitrary sparse Hecke/projector formulas, one
still needs the stronger cyclic-code minimum-weight statement or a proof that
the formula descends to the quotient spectrum.

## 2026-06-04: p-adic unit route reduced to packet norm

Singer the 2nd added:

```text
p24/subagent_padic_unit_sidecar.md
```

The clean scalar theorem is:

```text
Xi_a := Norm_{E^+/M^+}(H_a) is a p-unit at every prime of M^+ above p,
```

where

```text
[E^+ : M^+] = 194215
[M^+ : Q] = 8.
```

This is equivalent to the Hermitian packet residue being nonzero for each of
the eight real Frobenius packets.  Principal complex dominance proves
`H_a != 0` over `C`, but does not select a prime above the completely split
`p`.

The height audit is far too large for a norm-smaller-than-`p` proof:

```text
log_one_decomposition_prime_norm_bound = 1.971942e18
one_prime_bound_over_log_p = 3.568349e16
```

I added a reproducible selected-prime warning:

```text
p24/selected_prime_norm_toy.py
```

For `D=-87`, `q=103`, and `alpha=j-5`, the global norm is a nonzero integer
divisible by `103`; at the selected root `5`, `alpha=0`, while at the selected
root `29`, `alpha=24`.  Thus full norm divisibility says "some split prime",
not "this selected embedding".

Conclusion: the divisor/norm route currently restates the packet p-unit
theorem rather than proving it.  A useful next bounded experiment would scan
small Hermitian packet zeros by selected root and distinguish isolated
selected-prime zeros from structured suborbit/divisor zeros.

## 2026-06-04: Hermitian selected-prime zero distribution scan

I added:

```text
p24/hermitian_selected_prime_zero_scan.py
p24/hermitian_selected_prime_zero_scan.md
```

The scan rotates small split CM cycles through all selected embedded roots and
tests packet scalar zeros.

Hermitian nonlinear packet run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_selected_prime_zero_scan.py \
  --scalar hermitian --max-cases 40 --min-h 12 --max-h 90 \
  --max-abs-D 20000 --max-quotients 4 --min-n 5 \
  --q-stop 250000 --summary-only
```

Output:

```text
rows=40
packet_rows=74
selected_embedding_tests=1456
selected_embedding_zeros=0
selected_vs_packet_norm_mismatches=0
```

Low-order Hermitian control:

```text
rows=40
packet_rows=70
selected_embedding_tests=735
selected_embedding_zeros=0
```

Ordinary-energy control on the same low-order window:

```text
selected_embedding_zeros=16
packet_rows_with_any_selected_zero=2
packet_rows_with_full_orbit_zero=2
```

The two ordinary zero packets were:

```text
D=-304, q=101, h=6,  m=2, n=3, factor_degree=2, zero_count=6
D=-423, q=439, h=10, m=2, n=5, factor_degree=2, zero_count=10
```

Conclusion: the scan detects scalar cancellation, and ordinary energy can
fail by full-orbit cancellation.  Hermitian energy still showed no selected
prime zeros.  This strengthens the Hermitian packet p-unit target as the best
scalar route, but remains evidence rather than proof.

## 2026-06-04: Intermediate trace split inside the tensor factor

I added:

```text
p24/tensor_factor_intermediate_accounting.py
p24/tensor_factor_subfield_trace_audit.py
p24/tensor_factor_intermediate_trace_split.md
```

For p24, one tensor factor has degree:

```text
[B:E]=5549=31*179.
```

The proper intermediate fields have dimensions `31` and `179` over `E`.  This
cannot certify the full axis by itself because:

```text
axis_dim=368 > 31+179=210.
```

But it matches component blocks:

```text
constant + 2 + 157: 158 < 179
211 block:           210 = 31+179
```

The small row `D=-10919, q=11243, m=12` has `[B:E]=6=2*3`.  The audit found
no proper-subfield containment for selected resolvents, but proper traces do
certify the component blocks:

```text
block 4, size 3: trace to degree 3 has rank 3
block 3, size 2: trace to degree 2 has rank 2
axis size 6: joint proper trace rank only 4
```

Conclusion: the intermediate split is real for component-normality, but not a
complete substitute for the one-factor Moore/directness theorem.  The refined
target is trace injectivity on component spans plus full-factor cross-block
directness.

## 2026-06-04: Twisted trace-frame upgrade

I added:

```text
p24/tensor_factor_twisted_trace_frame.md
p24/tensor_factor_twisted_trace_frame_audit.py
p24/tensor_factor_trace_period_identity.py
p24/tensor_factor_trace_period_identity.md
p24/tensor_factor_trace_annihilator_theorem.md
p24/tensor_factor_dual_basis_window_audit.py
p24/tensor_factor_top_coefficient_capacity.py
p24/tensor_factor_top_coefficient_block_split.md
p24/tensor_factor_top_coefficient_fourier_audit.py
p24/tensor_factor_top_coefficient_fourier.md
p24/tensor_factor_trace_frame_probability.py
p24/tensor_factor_trace_frame_probability.md
p24/lean/TraceFrameGate.lean
p24/lean/TraceFrameAnnihilatorGate.lean
```

Plain traces to the p24 proper subfields have only `31+179=210` dimensions,
so they cannot certify all `368` axis resolvents.  The sidecar theorem pass
suggested using a short trace frame:

```text
T_3(x)=(
  Tr_{B/C}(x),
  Tr_{B/C}(theta*x),
  Tr_{B/C}(theta^2*x)
),
C=F_{Q^179}.
```

This has dimension `3*179=537` over `E`, far below the full factor dimension
`5549` but above the axis dimension.

Pinned local audit:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_twisted_trace_frame_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12
```

Output:

```text
[B:E]=6=2*3, axis_dim=6
subdegree 2 ranks by twists: [2,4,6]
subdegree 3 ranks by twists: [3,6]
```

The nearby quotient rows for the same discriminant also recovered full axis
rank by short twisted trace frames.

Conclusion: the new leading theorem target is full `E`-rank of the p24
three-trace frame to the degree-179 subfield.  This is still a selected-prime
determinant theorem, but it is substantially smaller and more structured than
the raw one-factor Moore determinant.

The period-accounting script shows the trace explicitly: for
`a=p^5460 mod n`, `Tr_{B/C}` is the 31-term sum over powers of `a^179`.
Thus the target can be restated as a `3 x 179` grid of decimated H-period
coordinates separating the 368 selected axis resolvents.

The trace-pairing note gives the cleanest theorem form:

```text
W_axis(B) ∩ Ann_3 = {0},
Ann_3 = span_C{1,theta,theta^2}^perp,
dim_C Ann_3 = 28.
```

This is now the best proof target: show that the actual CM axis image avoids
one canonical trace-annihilator subspace in the degree-31 extension `B/C`.
The random-subspace estimate for this avoidance theorem is `~Q^-170`, where
`Q=p^5460`, so a failure would require a highly structured CM annihilator.
The intrinsic finite certificate is the nonzero exterior product
`∧_{s in S_axis} T_3(R_s)` in `Exterior_E^368(C^3)`; coordinate minors are
just Plucker coordinates.

The dual-basis audit sharpens this again: after multiplying by `g'(theta)`,
where `g` is the degree-31 minimal polynomial over the degree-179 subfield,
the three trace coordinates are equivalent to the top three relative
coefficients.  Thus the p24 theorem can be phrased as injectivity of a
top-coefficient map on the axis image.

Component capacity gives:

```text
Top_1 for constant+2+157: dim 158 < 179
Top_2 for 211:            dim 210 < 358
Top_3 for full axis:      dim 368 < 537
```

This is the current split theorem shape: component-normality in leading
coefficients plus cross-block directness in the full three-window map.

I added:

```text
p24/tensor_factor_relative_coefficient_profile.py
p24/tensor_factor_relative_coefficient_profile.md
```

The pinned `D=-10919, m=12` profile shows full relative support after
multiplication by `g'(theta)`:

```text
subdegree=3 axis coeff_ranks=[3,3], support_sizes=[2,2,2,2,2,2]
subdegree=2 axis coeff_ranks=[2,2,2], support_sizes=[3,3,3,3,3,3]
```

So the simple triangular-support/degree-bound proof shape is not visible in
the small analogue; the leading-coefficient theorem remains a true rank
directness problem.

I added the Fourier audit:

```text
p24/tensor_factor_top_coefficient_fourier_audit.py
p24/tensor_factor_top_coefficient_fourier.md
```

It confirms `Top_k(R_s)=DFT_s(r -> Top_k(J_r))` on the pinned row.  But every
output coordinate has dense support on all frequencies:

```text
windows=1, subdegree=3: full_frequency_support_counts=[12,12,12]
windows=2, subdegree=3: full_frequency_support_counts=[12,12,12,12,12,12]
```

So there is no visible coordinate-isolated Vandermonde/block-diagonal
factorization.  The current target is a vector-valued Fourier
anti-annihilator theorem.

Sidecar agreed: the exact factorization is

```text
M_{S,k}=F_{S,Z/m} A_k,
```

with row `r` of `A_k` equal to `Top_k(J_r)`.  Under CRT, component blocks are
DFTs of marginal sums over residue classes.  But rank still depends on the
dense packet-coefficient operator `A_k`; nonzero scalar entries do not suffice.

Local audit:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_dual_basis_window_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 --max-rows 8
```

reported:

```text
rows=5
trace_window_rank_mismatch_targets=0
axis_rows_full_by_tested_window=5
```

After adding component/pair/prefix targets, the `D=-10919` rows also show the
capacity pattern: targets of size at most the intermediate degree are full on
one top coefficient, and larger targets fill once the window capacity reaches
the target dimension.

I added the CRT marginal-rank audit:

```text
p24/tensor_factor_crt_marginal_rank_audit.py
p24/tensor_factor_crt_marginal_rank.md
```

It turns the Fourier component statement into exact affine geometry.  For a
component `c`, the nontrivial component DFT rank equals the affine rank of the
marginals

```text
M_a = sum_{r == a mod c} Top_k(J_r),
```

and the constant-plus-component rank equals the ordinary span rank of the
`M_a`.  The pinned `D=-10919, m=12` audit reports zero rank-identity
mismatches:

```text
windows=1:
  c=4 marg_span=3/3 marg_affine=3/3 dft_nontriv=3 dft_const_plus=3
  c=3 marg_span=3/3 marg_affine=2/2 dft_nontriv=2 dft_const_plus=3
windows=2:
  c=4 marg_span=4/4 marg_affine=3/3 dft_nontriv=3 dft_const_plus=4
  c=3 marg_span=3/3 marg_affine=2/2 dft_nontriv=2 dft_const_plus=3
```

So the p24 proof target is now:

```text
dim_E( E*S_1 + Delta_2^(1) + Delta_157^(1) ) = 158,
dim_E( Delta_211^(2) ) = 210,
dim_E( E*S_3 + Delta_2^(3) + Delta_157^(3) + Delta_211^(3) ) = 368.
```

Here `Delta_c^(k)` is the span of the component marginal differences in
`C^k`.  The DFT/root-of-unity layer has been removed from the hard theorem;
the missing arithmetic input is marginal affine-rank plus directness.

I extended the CRT marginal audit to report combined directness targets.  On
the pinned `D=-10919, m=12` row:

```text
windows=1:
  combined=constantplus4plus3 size=6 rank=3/3
windows=2:
  combined=constantplus4plus3 size=6 rank=6/6
```

So the combined marginal-difference target fills exactly when the top-window
capacity reaches the full axis dimension in the toy analogue.

I added:

```text
p24/tensor_factor_marginal_annihilator_theorem.md
p24/lean/CrtMarginalAnnihilatorGate.lean
```

The theorem note restates rank failure as a structured CRT-axis weight
annihilator:

```text
w(r)=alpha+lambda_2(r mod 2)+lambda_157(r mod 157)+lambda_211(r mod 211),
x_w=sum_r w(r) J_r(theta),
Top_k(x_w)=0.
```

The finite certificate surface is now the three exterior products
`Omega_1`, `Omega_211`, and `Omega_3`.  A stats/probability side pass agreed
that random-subspace estimates do not certify the selected p24 prime; the
productive deterministic lift is a Plucker-content p-unit theorem or an
equivalent relative top-degree noncollapse theorem for these structured
weights.

I added the marginal origin-action audit:

```text
p24/tensor_factor_marginal_origin_action_audit.py
p24/tensor_factor_marginal_origin_product.md
```

It uses the exact origin formula

```text
J'_r(theta) = theta^(-beta) J_{r+alpha}(theta)
```

and tests chosen marginal exterior determinants on the pinned
`D=-10919, m=12` tensor row.  For the square full-axis two-window determinant:

```text
all_shifts count=156 distinct=2 zeros=0
pure_alpha_beta0 count=12 distinct=2 zeros=0
pure_beta_alpha0 count=13 distinct=1 zeros=0
alpha_beta_products count=12 distinct=2 zeros=0
```

For the one-window `4`-component determinant:

```text
all_shifts count=156 distinct=26 zeros=0
pure_alpha_beta0 count=12 distinct=2 zeros=0
pure_beta_alpha0 count=13 distinct=13 zeros=0
alpha_beta_products count=12 distinct=2 zeros=0
```

For the one-window `constant+3` determinant:

```text
all_shifts count=156 distinct=13 zeros=0
pure_alpha_beta0 count=12 distinct=1 zeros=0
pure_beta_alpha0 count=13 distinct=13 zeros=0
alpha_beta_products count=12 distinct=1 zeros=0
```

This supports the formal picture: alpha is a marginal-basis unit, beta is a
real top-coefficient Plucker motion, and the product over beta packages a
coordinate p-unit target with origin-stable zero status.  It remains stronger
than the intrinsic `Omega != 0` theorem and still lacks a class-field norm
formula.

I added beta-complexity and support audits:

```text
p24/tensor_factor_marginal_beta_complexity.py
p24/tensor_factor_marginal_beta_complexity.md
p24/tensor_factor_beta_support_audit.py
p24/tensor_factor_beta_support_boundary.md
```

On the same `D=-10919, m=12` row, the full two-window determinant has
`bm_complexity=1`, but this is a full-space artifact because `coords=6`
equals the whole tensor-factor degree.  The projected marginal determinants
are more p24-like:

```text
target=4, one window:
  distinct_values=13
  additive_period=13
  bm_complexity=7
  q_frobenius_matches=0/13
  Q_invariance_matches=1/13

target=constant+3, one window:
  distinct_values=13
  additive_period=13
  bm_complexity=7
  q_frobenius_matches=0/13
  Q_invariance_matches=1/13
```

For p24, with `O=<p^5460> mod 3107441` and `|O|=5549`, the tensor-factor
sumset audit reports:

```text
O+O:   covered=3090793, missing=16648
O+O+O: covered=3107441, missing=0
```

Thus high-rank exterior Plucker coordinates have full beta-character support
available.  The origin-stable beta-product remains certificate-shaped, but a
small-support recurrence/norm compression is not the proof.

I added:

```text
p24/tensor_factor_beta_recurrence_audit.py
p24/tensor_factor_beta_recurrence_resultant.md
p24/tensor_factor_plucker_spectral_support.md
```

On the projected `D=-10919, target=4` determinant, the beta sequence has an
exact recurrence:

```text
order=7
order_over_n=0.538462
characteristic_divides_T^n_minus_1=1
recurrence_failures_on_doubled_sequence=0
generation_mismatches_on_doubled_sequence=0
periodic_closure_failures=0
```

The `constant+3` determinant has the same degree-7 connection polynomial.
This gives the finite algebraic surface:

```text
Pi_{P,Omega}=prod_beta a_beta
```

is a norm/resultant-type certificate over the spectral-support factor
`E[T]/(chi)`.  For p24 this only improves asymptotically if `chi` is a product
of few degree-5549 Frobenius-orbit factors; the sumset audit says generic
large exterior coordinates should not have that support collapse.

I sharpened the p24 support audit to count whole `O`-cosets:

```text
2O: 557 of 560 nonzero degree-5549 orbit factors covered, zero absent
3O: 560 of 560 nonzero degree-5549 orbit factors covered, zero present
```

The formal support lemma is: a `d x d` Plucker coordinate of beta-shifted
linear entries has character support contained in `dO`.  Since the p24
exterior ranks are `158`, `210`, and `368`, support sparsity is not the
asymptotic certificate; only a CM-specific cancellation/support-collapse or a
full-support p-unit theorem can finish this route.

I added a CM-vs-random support audit:

```text
p24/tensor_factor_marginal_random_support_audit.py
p24/tensor_factor_marginal_random_support.md
```

For the pinned `D=-10919` projected marginal determinants, the CM recurrence
order `7` is exactly what random tensor-factor controls show:

```text
target=4:
  cm_order=7
  random_order_hist={7: 40}

target=constant+3:
  cm_order=7
  random_order_hist={7: 40}
```

So the small-row recurrence compression is representation-generic, not a
visible CM-specific support collapse.  This pushes the route toward a
full-support Plucker p-unit / superregularity theorem, or toward finding a
more special CM-derived coordinate whose support collapse is not shared by
random data.

I added:

```text
p24/tensor_factor_trace_coordinate_support_audit.py
p24/tensor_factor_trace_coordinate_support.md
```

This applies the support calculation directly to p24 trace-frame coordinate
cosets.  The prefix growth is:

```text
size=1 covered=31
size=2 covered=961
size=3 covered=29636
size=4 covered=799428
size=5 covered=3107068 missing=373
size=6 covered=3107441 missing=0
```

and `30/30` random six-coordinate samples had full support.  Since p24
coordinate minors select `158`, `210`, or `368` trace coordinates, ordinary
trace-coordinate minor choice will not yield a small recurrence/resultant
factor.  This further supports the full-support Plucker p-unit /
rank-condenser theorem as the remaining route.

I added a CS/ML theory import note:

```text
p24/cs_ml_theory_imports.md
```

The useful import is primarily from coding theory and algebraic complexity,
not ML.  The current marginal theorem is naturally a subspace-evasive /
rank-condenser statement:

```text
the CM marginal generator map sends every nonzero CRT-axis codeword away from
the trace-annihilator subspace.
```

In this language, the three `Omega` exterior products are Plucker p-unit
certificates for a structured superregularity/rank-condenser theorem.  ML can
help choose candidate minors or discover symbolic patterns, but it cannot
certify the selected p24 prime without graduating to an exact p-unit or
finite-field identity.

I added a sharper CS rank-condenser status note and audit:

```text
p24/cs_rank_condenser_theorem_status.md
p24/tensor_factor_marginal_cs_structure_audit.py
```

The audit treats CRT marginal rows as code-generator matrices and compares the
actual CM matrix to random tensor-factor controls.  On the pinned
`D=-10919, m=12` tensor row:

```text
full two-window axis:
  rows=6 cols=6 rank=6/6
  displacement=cyclic_hankel:6,cyclic_toeplitz:6,hankel:6,toeplitz:6
  random_controls rank_hist={6:80}, all displacement hists {6:80}

constant+4 one-window:
  rows=4 cols=3 rank=3/3
  displacement ranks all 3
  maximal row minors tested=4 zero=0
  random_controls matched

trace-zero component one-window:
  rows=2 cols=3 rank=2/2
  displacement ranks all 2
  maximal column minors tested=3 zero=0
  random_controls matched
```

This fences in the CS import.  Rank-condenser/subspace-evasive language,
PIT/Plucker p-units, and Moore/Gabidulin normality remain useful theorem
surfaces.  But the natural marginal matrices are not visibly
Toeplitz/Hankel/cyclic low-displacement, and their small superregularity
behavior is random-generic.  The live route is therefore still arithmetic:
prove a selected CM Plucker p-unit or a class-field normality identity.

I added the first stable Plucker norm miner:

```text
p24/tensor_factor_plucker_norm_miner.py
p24/tensor_factor_plucker_norm_miner.md
```

It enumerates or samples maximal trace-coordinate Plucker minors, computes
their beta products, takes norms to the base field, and compares CM products
with random tensor-factor controls.  Results:

```text
D=-10919, full two-window axis, shape=6x6:
  cm product degree=2, norm_height=2544
  random best_height_min=56, best_height_max=5598

D=-10919, target=4 without constant, shape=3x6:
  cm zero_free_minors=20/20
  product_subfield_degree_hist={2:20}
  cm best norm_height=331
  random best_height_min=5, best_height_max=857

D=-10919, target=3 with constant, shape=3x6:
  cm zero_free_minors=20/20
  product_subfield_degree_hist={2:20}
  cm best norm_height=342
  random best_height_min=2, best_height_max=735

D=-8711, target=4 without constant, shape=3x3:
  cm product degree=2, norm_height=3347
  random best_height_min=219, best_height_max=4099
```

Conclusion: the first data-mined stable-coordinate-product route is negative.
Natural trace-coordinate Plucker beta products are nonzero but full-degree and
random-looking.  The Plucker p-unit route remains live only in a sharper form:
an intrinsic exterior norm, a CM-adapted basis/coordinate, or a full-support
class-field identity.

I added the Hermitian component Schur audit:

```text
p24/hermitian_component_schur_audit.py
p24/hermitian_component_schur_boundary.md
```

It checks whether the intrinsic Hermitian axis determinant can be reduced to
diagonal CRT component determinants plus a simple correction.  On pinned
`(4,3)` rows:

```text
D=-10919, q=11243:
  full_det=4383, diag_product=1919, correction=6652, max_cross=2

D=-10919, q=14519:
  full_det=8450, diag_product=7806, correction=228, max_cross=2

D=-8711, q=8747:
  full_det=1552, diag_product=3376, correction=8250, max_cross=2

D=-8711, q=10007:
  full_det=4093, diag_product=9377, correction=7602, max_cross=2
```

A broader bounded window reported:

```text
rows=14
full_nonzero_rows=14
full_nonzero_but_singular_diagonal_block_rows=0
correction_ratio_rows=14
distinct_correction_ratios=14
correction_ratio_one_rows=0
```

So component block p-units may remain useful sublemmas, but they do not finish
the determinant.  The Schur correction is nontrivial and coupled; controlling
it is part of the selected Hermitian packet-norm p-unit theorem.

I added the Hermitian double-marginal audit and formula note:

```text
p24/hermitian_double_marginal_audit.py
p24/hermitian_double_marginal_formula.md
```

For the kernel

```text
K(r,s)=Tr_packet(F_r(X)F_s(X^-1)),
```

the component block `U_c x U_d` is the centered CRT double marginal:

```text
M_{c,d}(a,b)-M_{c,d}(a,0)-M_{c,d}(0,b)+M_{c,d}(0,0),
M_{c,d}(a,b)=sum_{r==a mod c, s==b mod d} K(r,s).
```

Pinned rows verified the identity with zero failures:

```text
D=-10919:
  pair_ranks=(4,4):3/3:fail0,(4,3):2/2:fail0,
             (3,4):2/2:fail0,(3,3):2/2:fail0

D=-8711:
  pair_ranks=(4,4):3/3:fail0,(4,3):2/2:fail0,
             (3,4):2/2:fail0,(3,3):2/2:fail0
```

A broader bounded scan reported:

```text
rows=14
constant_component_identity_failures=0
pair_identity_failures=0
pair_rank_mismatch_count=0
```

This gives the Schur correction a clean proof surface.  It is a centered
double-marginal p-unit target for the Hermitian autocorrelation kernel, with
the largest p24 mixed table coming from the `157 x 211` component pair.

I added the Fourier form of the Hermitian double marginal:

```text
p24/hermitian_double_marginal_fourier_audit.py
p24/hermitian_double_marginal_fourier.md
```

For

```text
M_{c,d}(a,b)=sum_{r==a mod c, s==b mod d} K(r,s),
```

the centered trace-zero table has the same rank after adjoining roots of unity
as the nonzero double DFT

```text
H_{c,d}(u,v)
  = sum_{a,b} zeta_c^(u*a) zeta_d^(v*b) M_{c,d}(a,b)
  = sum_{r,s} zeta_c^(u*r) zeta_d^(v*s) K(r,s).
```

Pinned rows:

```text
D=-10919:
  (4,4):base3/ext3/dft3
  (4,3):base2/ext2/dft2
  (3,4):base2/ext2/dft2
  (3,3):base2/ext2/dft2
  rank_mismatches=0

D=-8711:
  same rank pattern, rank_mismatches=0
```

Bounded summary:

```text
rows=9
pair_blocks=36
rank_mismatches=0
max_extension_degree=2
```

So the p24 mixed `157 x 211` Schur correction can now be stated as a
`156 x 210` nonzero K-character Hermitian pairing p-unit.  This is the
class-field-facing form of the coupled correction.

I then tested the CS/coding-theory refinement of this mixed block:

```text
p24/hermitian_mixed_frobenius_orbit_audit.py
p24/hermitian_mixed_moore_circulant_theorem.md
```

Since the Hermitian kernel `K(r,s)` is base-field valued, the double DFT
satisfies

```text
H(q^a*u0, q^b*v0) = H(u0, q^(b-a)*v0)^(q^a).
```

For p24:

```text
ord_157(p)=156, one row orbit
ord_211(p)=35,  six column orbits
```

so the large mixed Schur block is a six-block Moore/Frobenius-circulant
matrix generated by six length-35 seed cycles, not a raw `156 x 210` matrix.

Pinned rows:

```text
D=-10919:
  rows=2
  orbit_blocks=18
  frobenius_identity_failures=0
  nonfull_possible_rank_blocks=0

D=-8711:
  rows=2
  orbit_blocks=18
  frobenius_identity_failures=0
  nonfull_possible_rank_blocks=0
```

Bounded window:

```text
rows=3
orbit_blocks=27
frobenius_identity_failures=0
nonfull_possible_rank_blocks=0
max_block_possible_rank=2
```

The window only reached small orbit blocks, but the formal identity and
full-possible-rank behavior are consistent on actual CM rows.  The sharpened
theorem target is now:

```text
no nonzero skew-linearized convolution operator of p-degree < 156
annihilates all six p24 mixed Hermitian seed cycles.
```

This is the most productive CS import so far: a rank-metric/skew-PIT p-unit
surface for the mixed Schur correction.

I also added and checked:

```text
p24/lean/MixedMooreGate.lean
```

It formalizes the finite gate that an annihilator-free theorem for the six
seed cycles rules out mixed-block rank failure, once rank failure has been
translated into a nonzero skew annihilator.

I sharpened this again with the Lang-normality criterion:

```text
p24/hermitian_mixed_lang_normality_audit.py
p24/hermitian_mixed_lang_normality_theorem.md
```

For a right orbit of length `R`, the semilinear shift

```text
T(s)_b = sigma(s_{b-1})
```

has fixed vectors `u_alpha(b)=sigma^b(alpha)` for
`alpha in F_{q^R}`.  Changing coordinates by this fixed-vector Moore matrix
turns a mixed row orbit into an ordinary Moore matrix.  Hence:

```text
row-orbit rank = min(left orbit length,
                    F_q-rank of transformed seed coordinates).
```

Pinned rows:

```text
D=-10919:
  rows=2
  left_orbit_tests=12
  criterion_mismatches=0
  full_left_orbit_rank_tests=12

D=-8711:
  rows=2
  left_orbit_tests=12
  criterion_mismatches=0
  full_left_orbit_rank_tests=12
```

Bounded window:

```text
rows=3
left_orbit_tests=18
criterion_mismatches=0
full_left_orbit_rank_tests=18
```

For p24 the theorem target is now:

```text
the 210 Lang-trivialized mixed Hermitian seed coordinates have
F_p-span dimension at least 156.
```

This is a significantly smaller and cleaner normality p-unit theorem than the
raw mixed `156 x 210` determinant.

I then separated the p24 coprime-degree consequence:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
p24/hermitian_mixed_left_subfield_identity_toy.py
p24/hermitian_mixed_trace_dual_formula_toy.py
p24/hermitian_mixed_dual_trace_injectivity_toy.py
p24/hermitian_mixed_left_subfield_span_theorem.md
```

Since:

```text
ord_157(p)=156
ord_211(p)=35
gcd(156,35)=1
```

the Lang-trivialized coordinates should land in the left character field
`F_p(mu_157)=F_{p^156}`.  The target is therefore:

```text
dim_Fp span{210 transformed mixed Hermitian periods} = 156.
```

Pinned CM rows:

```text
D=-10919:
  rows=2
  tests=12
  left_subfield_failures=0
  full_left_span_tests=12

D=-8711:
  rows=2
  tests=12
  left_subfield_failures=0
  full_left_span_tests=12
```

The p24-like coprime-degree finite-field toy:

```text
q=2, left=7, right=5
ord_7(2)=3, ord_5(2)=4, gcd=1
```

reported:

```text
left_orbit_tests=40
left_subfield_failures=0
full_left_span_tests=29
max_transformed_fq_rank=3
```

This also corrected an overstrong shortcut: a single normal coordinate is not
enough.  The Moore row rank is the `F_p`-rank of the tuple of 210 transformed
coordinates, so the proof needs a 156-independent subtuple or equivalent
Moore-minor p-unit.

The trace-dual formula toy verified that the transformed coordinates are
intrinsic relative-trace coordinates.  In p24 notation:

```text
E = F_p(mu_157,mu_211),  L = F_p(mu_157),
S_j = H_{157,211}(1,v_j) for the six 211-orbit representatives,
w_{j,i}=Tr_{E/L}(delta_i*S_j).
```

Toy output:

```text
formula_tests=40
trace_dual_mismatches=0
left_subfield_failures=0
full_left_span_tests=29
```

The surviving p-unit theorem is therefore:

```text
dim_Fp span{Tr_{E/L}(delta_i*S_j)} = 156.
```

The dual trace injectivity toy then verified the equivalent map:

```text
L -> R^6,
lambda |-> (Tr_{E/R}(lambda*S_j))_j.
```

Output:

```text
dual_tests=40
rank_mismatches=0
full_span_tests=29
dual_injective_tests=29
```

I also ran a small six-right-orbit toy:

```text
q=2, left=7, right=31
ord_7(2)=3
ord_31(2)=5
(31-1)/5=6 right orbits
```

which reported:

```text
dual_tests=80
rank_mismatches=0
full_span_tests=80
dual_injective_tests=80
```

So the current theorem can also be read as:

```text
no nonzero lambda in F_p(mu_157) is killed by all six right relative traces.
```

I added the equivalent trace-intersection statement:

```text
p24/hermitian_mixed_trace_intersection_theorem.md
p24/lean/MixedTraceIntersectionGate.lean
```

If

```text
W = span_R{S_1,...,S_6} subset E,
```

then the theorem is:

```text
L ∩ W^perp = {0}
```

for the `E/R` trace pairing.  This records the correct transversality target:
`dim_R W <= 6`, so the six periods cannot span `E` over `R`; they only need
their orthogonal complement to avoid the left character field.

I also connected these six periods back to K-character resolvents:

```text
p24/hermitian_mixed_resolvent_pairing_audit.py
p24/hermitian_mixed_resolvent_pairing_formula.md
```

For left/right CRT components:

```text
A_u = sum_r zeta_c^(u*r) F_r,
B_v = sum_s zeta_d^(v*s) F_s,
H_{c,d}(u,v)=<A_u,B_v>.
```

For p24:

```text
S_j = H_{157,211}(1,v_j)=<A_1,B_{v_j}>.
```

Pinned rows verified the conventions:

```text
D=-10919:
  rows=2
  tests=8
  entry_mismatches=0
  rank_mismatch_tests=0
  all_seed_periods_nonzero_tests=8

D=-8711:
  rows=2
  tests=8
  entry_mismatches=0
  rank_mismatch_tests=0
  all_seed_periods_nonzero_tests=8
```

So the current class-field object is not a raw matrix entry; it is the six
mixed Hermitian pairings between one left `157`-character resolvent and the
six right `211`-orbit resolvents.
### 2026-06-05: subspace-polynomial certificate form for mixed trace periods

I sharpened the rank-metric/Gabidulin import one more step.  After the
Lang/trace-dual reduction, the p24 target is that the `210` coordinates

```text
w_{j,i}=Tr_{E/L}(delta_i*S_j) in L=F_p(mu_157)
```

span the `156`-dimensional `F_p`-space `L`.  For any tuple `C` in a finite
field, the monic `q`-linearized subspace polynomial `A_C` has `q`-degree
equal to `dim_Fq span(C)`.  Therefore the p24 target is equivalent to:

```text
A_C(X) = X^(p^156) - X.
```

or equivalently no nonzero `p`-linearized polynomial of `p`-degree `<156`
kills all `210` trace-dual mixed coordinates.  This packages the missing
trace-intersection theorem into a canonical annihilator object rather than an
arbitrary coordinate minor.

Added:

```text
p24/hermitian_mixed_subspace_polynomial_certificate.md
p24/hermitian_mixed_subspace_polynomial_toy.py
p24/lean/MixedSubspacePolynomialGate.lean
```

Toy checks:

```text
q=2,left=7,right=31,trials=20:
  subspace_tests=40
  degree_rank_mismatches=0
  vanish_failures=0
  full_span_tests=40
  full_field_annihilator_tests=40
  forced_low_rank_degree_mismatches=0

q=2,left=7,right=5,trials=20:
  subspace_tests=40
  degree_rank_mismatches=0
  vanish_failures=0
  full_span_tests=29
  full_field_annihilator_tests=29
  forced_low_rank_degree_mismatches=0
```

The new theorem target is now:

```text
For S_j=<A_1,B_vj>, the subspace polynomial of
{Tr_{E/L}(delta_i*S_j)} is X^(p^156)-X.
```

I then integrated residual mining into the actual-CM left-subfield audit.
The recursion records pivot indices and residual norm products, which are
Moore-minor witnesses in disguise.  Pinned `D=-10919` rows report nonzero
base-field pivot norms, for example:

```text
pivotprefix[0, 1]:pivotnorm6471
pivotprefix[0]:pivotnorm50
```

and the summary has:

```text
zero_residual_norms=0
missing_pivot_norm_products=0
max_pivot_count=2
```

This is now the concrete statistics/ML theorem-search hook: look for stable
156-pivot residual norm products in dimension-eligible rows, then try to
identify them as class-field norms/resultants.

### 2026-06-05: centered right-profile form of the mixed theorem

I found a more economical equivalent target.  Write the left-character
profile of the Hermitian double marginal as:

```text
G_s = sum_r zeta_157^r M(r,s) in F_p(mu_157).
```

The nonzero right DFT periods

```text
S_v = H_{157,211}(1,v)
```

are just the right Fourier transform of `G_s` with the `v=0` component
omitted.  Therefore the trace-dual coordinate span is equivalent to the span
of the centered profile:

```text
G_s^0 = G_s - average_t(G_t).
```

The missing p24 theorem can now be stated as:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157).
```

Added:

```text
p24/hermitian_mixed_centered_right_profile_theorem.md
```

and extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

with centered-profile rank diagnostics.  Pinned actual-CM rows `D=-10919` and
`D=-8711` both report:

```text
centered_profile_rank_mismatches=0
centered_profile_subfield_failures=0
```

This does not prove the degree-`156` p24 theorem, but it removes the right
trace-dual basis from the missing theorem and gives a cleaner class-field
profile to attack.

I then observed that, because `p` is primitive modulo `157`, the profile
statement is equivalent to a purely base-field centered-marginal rank theorem:

```text
C(r,s)=M(r,s)-M(r,0)-M(0,s)+M(0,0),
1 <= r < 157, 1 <= s < 211,
rank_Fp C = 156.
```

The audit now reports `centered_base_rank` and compares it to the profile
rank only when the left orbit is the whole nontrivial left character set.
Pinned `D=-10919` rows have:

```text
centered_base_rank_applicable_tests=4
centered_base_profile_rank_mismatches=0
```

### 2026-06-05: right-orbit support strengthening

I recorded a stronger dual trace candidate:

```text
for every nonzero lambda in L,
at least two of the six traces Tr_{E/R}(lambda*S_j) are nonzero.
```

If true, any five of the six right orbit packets already separate `L`.

Added:

```text
p24/hermitian_mixed_right_orbit_support_theorem.md
p24/hermitian_mixed_orbit_support_toy.py
```

The six-right-orbit miniature

```text
q=2, left=7, right=31, trials=40
```

reported:

```text
support_tests=80
full_rank_tests=80
delete_one_full_rank_tests=80
zero_support_failures=0
one_support_strong_failures=0
min_lambda_support=3
```

The one-right-orbit control

```text
q=2, left=7, right=5, trials=40
```

failed as expected:

```text
full_rank_tests=52
zero_support_failures=28
one_support_strong_failures=80
min_lambda_support=0
```

I also added centered-profile Frobenius-stability diagnostics to the actual-CM
audit.  Pinned rows have stability defect `0`, but only at left degree `2`, so
the Galois-stable normal-frame theorem remains a candidate rather than
evidence.

I sharpened the support theorem into a cyclic-code avoidance statement.  For

```text
f_lambda(s)=Tr_{L/F_p}(lambda*G_s^0),
```

the original theorem rules out `f_lambda=0` for `lambda != 0`; the stronger
support theorem rules out `f_lambda` lying in any single 35-dimensional
right-orbit cyclic code.  This gives a more proof-shaped target than generic
rank support:

```text
the 156-dimensional left-twist trace family avoids seven explicit cyclic-code
subspaces of functions on Z/211Z.
```

### 2026-06-05: centered marginal stress rows

I added a cheap class-number/index prefilter:

```text
p24/centered_marginal_candidate_index.py
```

Then I ran two actual-CM stress rows through the centered-profile audit.

`D=-13319` gives a positive left-degree-`3` check:

```text
h=140, q=13463, m=28, n=5, components=[4,7]
max_left_orbit_len=3
max_centered_right_profile_rank=3
centered_profile_rank_mismatches=0
full_left_span_tests=8
```

`D=-6719` gives a useful dimension-boundary check:

```text
h=105, q=6863, m=21, n=5, components=[3,7]
left orbit length=6
packet degree=4
centered_base_rank_applicable_tests=4
centered_base_profile_rank_mismatches=0
full_left_span_tests=2
```

The full-left row `(7,7)` has rank `4 < 6`, exactly as expected from packet
degree `4`.  It also shows why the normal-coordinate idea is insufficient:

```text
centered_profile_max_single_normal_rank=6
centered_profile_stability_defect=2
full=0
```

So p24 must use more than existence of normal coordinates.  It must prove the
actual centered marginal has full row rank; the dimension obstruction is absent
there because `388430 >= 156`.

### 2026-06-05: Delsarte/delete-one rank import

I imported the standard Delsarte trace-code dictionary into the current
right-orbit support theorem.  For the scalar trace word

```text
f_lambda(s)=Tr_{L/F_p}(lambda*G_s^0),
```

the six nonzero right Frobenius orbits are exactly six irreducible cyclic-code
components, with Fourier coefficients

```text
hat f_lambda(p^b v_j)=Tr_{E/R}(lambda*S_j)^(p^b).
```

Thus the stronger support theorem is equivalent to six delete-one rank tests:

```text
for every j,
rank_Fp(lambda |-> (Tr_{E/R}(lambda*S_k))_{k != j}) = 156.
```

I extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

with cheap actual-CM delete-one ranks and small-degree exhaustive trace-support
checks.  On the positive `D=-13319` stress row:

```text
full_left_span_tests=8
delete_one_full_left_span_tests=5
centered_trace_support_checked_tests=2
centered_trace_zero_support_tests=0
centered_trace_one_support_tests=0
min_centered_trace_right_orbit_support=2
```

On the `D=-6719` dimension boundary:

```text
delete_one_full_left_span_tests=0
max_delete_one_min_transformed_rank=0
```

because those stressed components have only one right orbit.  So this is now
the cleanest CS import: standard cyclic-code decomposition plus a new CM
p-unit/delete-one rank theorem, rather than generic BCH/min-weight.

### 2026-06-05: leading delete-one Moore minor candidate

I extended the delete-one diagnostics one step further: each delete-one subset
now also reports its subspace-polynomial annihilator degree, vanish failures,
full-field annihilator count, pivot prefixes, and residual norm products.

For the positive `D=-13319` stress row:

```text
delete_one_annihilator_degree_mismatches=0
delete_one_annihilator_vanish_failures=0
delete_one_zero_residual_norms=0
delete_one_full_field_annihilator_all_tests=5
delete_one_leading_full_tests=5
delete_one_leading_annihilator_degree_mismatches=0
delete_one_leading_annihilator_vanish_failures=0
delete_one_leading_zero_residual_norms=0
delete_one_leading_full_field_annihilator_all_tests=5
```

In the full delete-one cases, the pivot prefixes are leading:

```text
(7,7): deletepivotprefixes [[0,1,2], [0,1,2]]
(4,7): deletepivotprefixes [[0,1], [0,1]]
```

Origin shifts `1,2,3,4` preserve the aggregate delete-one counts, and the
checked shifted verbose row preserves the same leading prefixes in the full
delete-one cases.

This sharpens the p24 certificate candidate again:

```text
For each of the six deleted right orbits, the first 156 coordinates from the
remaining five orbits have nonzero Moore determinant.
```

Equivalently, six explicit residual norm products from the incremental
subspace-polynomial algorithm are p-units.  This removes the existential
minor search from the theorem statement.

### 2026-06-05: leading-erasure incidence form

I recorded the leading-minor candidate as an explicit erasure-incidence
theorem:

```text
p24/hermitian_mixed_leading_erasure_theorem.md
```

For p24, right frequencies modulo `211` have six length-`35` orbits with reps:

```text
1, 2, 4, 8, 16, 29.
```

After deleting one orbit, the leading `156` coordinates are:

```text
4 full right blocks + first 16 coordinates of the fifth kept block.
```

So the omitted coordinates are exactly:

```text
35 coordinates of the deleted orbit + 19 trailing coordinates of the last
kept orbit.
```

The six leading Moore p-unit theorem is therefore equivalent to:

```text
Phi(L) ∩ E_j = {0},    j=1,...,6,
```

where `Phi: L -> F_p^210` is the Delsarte coordinate map and each `E_j` is a
named `54`-dimensional erasure subspace.  The finite implication

```text
leading erasure avoidance => delete-one separation => support >= 2
```

is Lean-checked in `p24/lean/MixedRightOrbitSupportGate.lean`.

I also extended the random right-orbit toy with explicit leading-prefix ranks.
For `q=2,left=7,right=31,trials=40`:

```text
delete_one_full_rank_tests=80
delete_one_leading_full_rank_tests=10
min_delete_one_leading_rank=0
```

So leading-prefix fullness is not a generic consequence of the six-orbit
Delsarte shape.  This demotes the leading-minor route from "probably generic"
to "explicit CM p-unit candidate"; useful because it is named, but it still
needs genuine arithmetic proof.

The leading window now splits into the smaller p24 target:

```text
156 = 4*35 + 16.
```

So each of the six leading Moore minors can be attacked as:

```text
rank(first four kept right blocks)=140,
tail augmentation from first 16 coords of fifth block=16.
```

Dually, four full right-trace kernels should leave a `16`-dimensional residual
subspace of `L`, and the fifth block's first `16` coordinates should separate
that residual.  The actual-CM audit now reports this with:

```text
delete_one_prefix_full_block_counts
delete_one_prefix_tail_lengths
delete_one_prefix_full_block_min_rank
delete_one_prefix_tail_min_augmentation
```

### 2026-06-05: quotient-tail residual p-unit

I extended the subspace-polynomial helper with:

```text
qpoly_extend_profile(initial_annihilator, elements)
```

and used it in the actual-CM audit to compute the tail residual after the
full-block prefix has already been annihilated.  This records:

```text
delete_one_prefix_tail_ann_degrees
delete_one_prefix_tail_pivot_prefixes
delete_one_prefix_full_block_norm_products_base
delete_one_prefix_tail_norm_products_base
delete_one_prefix_full_block_zero_residual_norms
delete_one_prefix_tail_zero_residual_norms
```

For p24 this is the six `16 x 16` quotient determinant candidate:

```text
four full right blocks give rank 140;
the tail residual product for the first 16 coordinates of the fifth block is
nonzero.
```

Pinned `D=-13319` check:

```text
delete_one_prefix_tail_full_all_tests=5
delete_one_prefix_full_block_zero_residual_norms=0
delete_one_prefix_full_block_norm_products_missing=0
delete_one_prefix_tail_zero_residual_norms=0
delete_one_prefix_tail_norm_products_missing=0
max_delete_one_prefix_tail_min_augmentation=2
```

The dimensions are tiny there, but the residual-product convention matches
the intended p24 quotient theorem.  Each leading minor is now represented as
a pair of p-unit factors: the full-block prefix product and the quotient-tail
product.

I added a Lean gate in `p24/lean/MixedSubspacePolynomialGate.lean`:

```text
prefix rank + tail augmentation = full leading rank.
```

Together with the erasure gate in `MixedRightOrbitSupportGate.lean`, this
checks the finite implication chain from the `140+16` p-unit certificate to
right-support `>=2`.

### 2026-06-05: explicit p24 factor manifest

I added:

```text
p24/p24_factorized_certificate_manifest.py
```

It prints the p24 orbit/factor manifest from the actual Frobenius action
`p mod 211 = 114`.  The deleted-orbit rows are:

```text
deleted O1: B={O2,O3,O4,O5}, T=first16(O6)
deleted O2: B={O1,O3,O4,O5}, T=first16(O6)
deleted O3: B={O1,O2,O4,O5}, T=first16(O6)
deleted O4: B={O1,O2,O3,O5}, T=first16(O6)
deleted O5: B={O1,O2,O3,O4}, T=first16(O6)
deleted O6: B={O1,O2,O3,O4}, T=first16(O5)
```

So the factorized certificate has:

```text
5 distinct B prefix p-units,
6 quotient-tail p-units.
```

The prefix `{O1,O2,O3,O4}` is shared by the `O5` and `O6` deletion rows.
This is a small but real compression of the named certificate list.

The manifest now also prints a paired certificate:

```text
deleted O1/O2 share B={O3,O4,O5,O6}, tails O2/O1
deleted O3/O4 share B={O1,O2,O5,O6}, tails O4/O3
deleted O5/O6 share B={O1,O2,O3,O4}, tails O6/O5
```

This uses:

```text
3 distinct B prefix p-units,
6 quotient-tail p-units.
```

The count `3` is optimal for four-block certificates because each four-block
prefix excludes exactly two right orbits and therefore can serve at most two
deletion rows.

I added a random finite-linear paired-tail control:

```text
p24/paired_tail_independence_toy.py
```

For `q=2, block_len=3, tail_len=2, trials=500` it reported:

```text
prefix_full_tests=1174
both_tail_full_tests=188
exactly_one_tail_full_tests=538
neither_tail_full_tests=448
```

For `q=3, block_len=3, tail_len=2, trials=300` it reported:

```text
prefix_full_tests=852
both_tail_full_tests=300
exactly_one_tail_full_tests=407
neither_tail_full_tests=145
```

So a full shared prefix plus one full tail does not force the paired opposite
tail.  The six `T` factors are separate finite-linear obligations unless a new
CM-specific symmetry relates them.

### 2026-06-05: opposite-orbit pairing and conjugate-tail gate

The adjacent paired certificate is optimal for the number of prefix factors,
but it is not adapted to the visible `v -> -v` symmetry.  For p24,

```text
O1 <-> O4,
O2 <-> O5,
O3 <-> O6
```

under right-frequency negation modulo `211`.  I updated:

```text
p24/p24_factorized_certificate_manifest.py
```

to print the opposite-orbit certificate:

```text
deleted O1/O4 share B={O2,O3,O5,O6}, tails O4/O1
deleted O2/O5 share B={O1,O3,O4,O6}, tails O5/O2
deleted O3/O6 share B={O1,O2,O4,O5}, tails O6/O3
```

This still has three distinct `B` prefix factors, and now each prefix is
stable under `v -> -v`.  Therefore the arithmetic target can be sharpened:
if CM conjugation preserves the shared prefix kernels and swaps the first-16
tail windows, then the six tail p-units fall into three conjugate pairs.

There is a coordinate-order caveat.  The natural smallest-representative orbit
orders do not have conjugate first-16 windows:

```text
O1 -> O4 offset 9,
O2 -> O5 offset 9,
O3 -> O6 offset 6.
```

So the opposite manifest uses rotated q-consecutive tail windows.  For
example, the `O4` tail window is `-` the chosen `O1` window rather than the
first sixteen entries of the natural `O4` list.  This keeps the finite
certificate valid while making the conjugation gate point at the right
coordinates.

I then added:

```text
p24/opposite_conjugation_window_audit.py
```

to separate raw seed positions from Lang-coordinate positions.  In p24,
left negation is

```text
-1 = p^78 mod 157,
78 mod 35 = 8.
```

So raw inversion of DFT seeds includes a semilinear shift `T^78`.  The Lang
trivialization satisfies:

```text
seed = U*w  =>  T^a(seed) = U*w^(p^a),
```

so this shift becomes coordinatewise Frobenius and does not move the Lang
coordinate index.  The audit prints, for example:

```text
O1/O4 direct_negation_positions=[9,...,24]
O1/O4 raw_seed_after_left_positions=[1,...,16]
lang_shift_coordinate_mismatches=0
```

Thus the correct conjugation-tail theorem is about direct negation windows in
Lang coordinates, not about the raw shifted seed positions.

I then separated the finite algebra theorem into:

```text
p24/opposite_conjugation_tail_theorem.md
```

The theorem is that in the full cyclotomic product algebra the inversion
automorphism

```text
mu_157 -> mu_157^-1,
mu_211 -> mu_211^-1
```

sends `H(u,v)` to `H(-u,-v)`.  Since left negation is `p^78`-Frobenius on
`L=F_p(mu_157)`, and the right factors are paired by `v -> -v`, the opposite
tail injectivity statements are conjugate after compatible Lang
trivialization.  Together with `ConjugateTailGate.lean`, this reduces the
arithmetic tail proof surface from six `T` p-units to three representative
`T` p-units.

Current sharpest missing theorem:

```text
3 opposite-prefix p-units B
+ 3 representative opposite-tail p-units T
are nonzero modulo p=10^24+7.
```

### 2026-06-05: opposite-prefix Gram boundary

The inversion-stable prefixes suggest a Hermitian Gram determinant route for
the three `B` factors.  I added:

```text
p24/opposite_prefix_gram_toy.py
p24/opposite_prefix_gram_boundary.md
```

The toy confirms the finite-field isotropy obstruction:

```text
q=3, rows=4, cols=8, trials=2000:
  full_row_rank=2000
  full_row_and_full_gram=1398
  full_row_singular_gram=602

q=2, rows=3, cols=6, trials=2000:
  full_row_rank=1991
  full_row_and_full_gram=1040
  full_row_singular_gram=951
```

Therefore a Hermitian Gram determinant p-unit would imply a prefix `B` p-unit,
but it is stronger than prefix rank and not a formal consequence of the
opposite pairing.  The Gram route remains plausible only as a selected-prime
p-adic theorem for the actual CM prefix determinant, not as a positivity or
generic-rank shortcut.

### 2026-06-05: right-unit equivariance compresses to one leading p-unit

The sidecar noticed, and I audited, that multiplication by `2 mod 211` cycles
the six right Frobenius orbit labels:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

I added:

```text
p24/right_orbit_unit_action_audit.py
p24/right_unit_equivariance_theorem.md
p24/lean/UnitOrbitGate.lean
```

The audit reports:

```text
unit=2 perm=(2,3,4,5,6,1)
unit_2_cycles_opposite_pairs=1
unit_2_cycles_opposite_prefixes=1
unit_2_cycles_representative_tails_up_to_inversion=1
```

Thus, in the full cyclotomic product algebra with equivariant Lang bases,
the three opposite-prefix `B` p-units are one unit-orbit class, and the six
tail rows are one unit-orbit class.  The finite gate is only the obvious orbit
logic, but it cleanly separates the issue:

```text
one representative B p-unit + unit equivariance => all three B factors;
one representative T p-unit + unit equivariance => all six T factors.
```

Current sharpest arithmetic target:

```text
1 representative leading Moore p-unit L = B*T.
```

The caveat is important: the automorphism `mu_211 -> mu_211^2` permutes the
six degree-35 right factors.  So this compression is valid for a certificate
phrased in the full product algebra, or for a verifier that explicitly tracks
the factor permutation and compatible Lang-basis determinant factors.  It is
not literal equality of scalar representatives inside one fixed factor.

I updated the manifest to print the representative unit orbit:

```text
p24/p24_factorized_certificate_manifest.py
p24/p24_equivariant_manifest.py
```

under:

```text
equivariant_1B1T_representative_certificate
```

The representative is:

```text
deleted=O4,
B_prefix={O2,O3,O5,O6},
T_tail=O1,
tail_window=first 16 Lang coordinates of O1.
```

Equivalently, the verifier can ask for the single leading residual product

```text
L_rep = B_rep*T_rep
```

for this row.  The split `B_rep,T_rep` is still the best proof strategy, but
the finite certificate only needs `L_rep != 0`.

I added:

```text
p24/moore_residual_product_toy.py
```

to verify the exact finite-field identity between the ordered Moore
determinant and the incremental residual product.  After fixing the toy to
include zero residuals in singular cases, the checks report:

```text
q=3, degree=8, count=6, prefix_count=4:
  determinant_mismatches=0
  split_mismatches=0
  nonzero_mismatches=0

q=2, degree=7, count=5, prefix_count=3:
  determinant_mismatches=0
  split_mismatches=0
  nonzero_mismatches=0
```

Thus the identity `L_rep=B_rep*T_rep` is not just mnemonic; it is the standard
Moore residual product formula.

### 2026-06-05: representative dual obstruction

I added:

```text
p24/representative_dual_obstruction_theorem.md
p24/lean/RepresentativeDualObstructionGate.lean
p24/representative_dual_obstruction_toy.py
```

The one-punit theorem now has an exact dual form.  For the representative row,
`L_rep=0` iff there exists nonzero `lambda in F_p(mu_157)` such that:

```text
a_2(lambda)=a_3(lambda)=a_5(lambda)=a_6(lambda)=0,
pi_16(a_1(lambda))=0.
```

Equivalently, four full right traces cut out a kernel, and the first 16 Lang
coordinates of the `O1` tail must be injective on that kernel.

The toy verifies:

```text
determinant_kernel_mismatches=0
split_mismatches=0
L_nonzero_iff_no_bad_lambda=1
L_nonzero_iff_prefix_full_and_tail_injective=1
```

and also shows that tail injectivity is not formal: in small random tests,
many maps have full prefix rank but tail failure.

Unit `2` propagates this through all six deletion rows.  The unit-equivariant
tail windows differ from the direct-inversion windows by internal Frobenius
rotations in some right factors; after Lang trivialization these are
coordinatewise Frobenius operations and preserve zero predicates.  This is a
coordinate convention, not a new arithmetic p-unit.

The JSON manifest reports:

```text
representative_scalar.name=L_rep
representative_scalar.factorization=B_rep*T_rep
representative_row={deleted:4, prefix:[2,3,5,6], tail:1}
unit2_permutation=[2,3,4,5,6,1]
```

I added the finite gate:

```text
p24/lean/ConjugateTailGate.lean
```

It proves the abstract implication:

```text
prefix preserved by conjugation
+ tailA/tailB zero predicates interchanged by conjugation
+ tailA injective on the prefix kernel
=> tailB injective on the prefix kernel.
```

So the new best proof target is:

```text
3 opposite-prefix p-units B,
3 representative opposite-tail p-units T,
CM conjugation-intertwining for the opposite tail windows.
```

This is strictly a proof-target refinement, not a certificate yet.  If the
first-16 coordinate windows are not conjugation-compatible, the opposite
pairing remains a valid `3B+6T` certificate but gives no tail compression.

### 2026-06-05: representative CS-theory boundary

I added:

```text
p24/representative_cs_theory_candidate_boundary.md
p24/representative_kernel_cs_boundary_audit.py
```

This updates the CS/ML import after the unit-2 equivariance compression to a
single representative leading p-unit:

```text
L_rep = B_rep*T_rep,
K = ker(a_2,a_3,a_5,a_6),
pi_16(a_1)|_K injective.
```

The deterministic p24 metadata rules out the most tempting over-strong tower
claim:

```text
dim_Fp K = 16 is not a subfield dimension of F_{p^156}.
```

The subfield dimensions are:

```text
1,2,3,4,6,12,13,26,39,52,78,156.
```

So `K` cannot literally be `F_{p^16}` or a scalar multiple of a subfield.
A Frobenius-module theorem is still possible, but it would need exact
arithmetic content: for p24,

```text
x^156 - 1 over F_p has irreducible degree histogram {1:2, 2:5, 4:36},
```

and 16-dimensional invariant component sums exist.

Small random controls:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 3 --right-degree 8 --tail-dim 4 --trials 200
```

reported:

```text
prefix_full=198/200
determinant_full=119/200
prefix_full_tail_fail=79/200
shift_stable_counts={1:0, 2:0, 4:0}
```

Tiny p24-shaped controls:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 3 --right-degree 35 --tail-dim 16 --trials 8 --max-enumerate 1000
```

reported:

```text
prefix_full=8/8
determinant_full=2/8
prefix_full_tail_fail=6/8
kernel_dim_hist={16:8}
shift_stable_counts={1:0, 2:0, 4:0}
```

Conclusion: rank-metric/subspace-polynomial theory remains the right CS
language, but tail injectivity is not formal and the exact proof must still
be a class-field p-unit/norm theorem for `L_rep`.  ML/statistics should only
be used to search for equivariant residual norm identities or stable pivot
patterns that can be promoted to such a theorem.

### 2026-06-05: representative shape parameter prefilter

I added:

```text
p24/representative_shape_parameter_prefilter.py
p24/representative_shape_parameter_prefilter.md
```

This is a cheap orbit-arithmetic prefilter for small analogues of the p24
representative shape:

```text
right_orbit_count = 6,
left_degree = 4*right_degree + tail,
tail > 0,
gcd(left_degree,right_degree)=1.
```

For p24:

```text
p mod 157 = 21
p mod 211 = 114
ord_157(p)=156
ord_211(p)=35
156 = 4*35 + 16.
```

The scan:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_shape_parameter_prefilter.py \
  --max-q 31 --max-modulus 400 --tail 16 --limit 20
```

found:

```text
q=5  left=157 L=156 right=211 R=35 shape=4*R+16
q=13 left=313 L=156 right=211 R=35 shape=4*R+16
q=31 left=197 L=196 right=271 R=45 shape=4*R+16
```

The `q=5, left=157, right=211` hit has the exact p24 orbit dimensions and
tail length.  This is useful as a theorem-filter: any claimed identity that
uses only the `157/211` orbit geometry should have a well-defined `q=5`
same-shape analogue.  If the proof really uses the selected p24 CM embedding
or p-unit arithmetic, that dependence must be explicit.

A p24-shaped random control over `q=5`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/representative_kernel_cs_boundary_audit.py \
  --q 5 --right-degree 35 --tail-dim 16 --trials 8 --max-enumerate 1000
```

reported:

```text
prefix_full=8/8
determinant_full=7/8
prefix_full_tail_fail=1/8
kernel_dim_hist={16:8}
shift_stable_counts={1:0, 2:0, 4:0}
```

This is only a baseline, but it supports the current discipline: use random
models to calibrate theorem candidates, then demand an exact class-field
norm/resultant p-unit proof for `L_rep`.

### 2026-06-05: right-unit subspace-orbit boundary

I added:

```text
p24/right_unit_subspace_orbit_toy.py
p24/right_unit_subspace_orbit_boundary.md
```

This checks a tempting shortcut from the unit-2 equivariance theorem.  The
valid statement is:

```text
unit-2 cycles full deletion-row certificate data in the full product algebra.
```

The invalid shortcut would be:

```text
inside one fixed row, the six trace-coordinate subspaces W_j subset L are
all the same W, or are automatically generated by one known operator on L.
```

The finite-field DFT toy with six right orbits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/right_unit_subspace_orbit_toy.py --q 2 --left 11 --right 31
```

reported:

```text
left_degree=10
right_degree=5
right_orbit_count=6
unit_cycle=3
block_ranks=[5,5,5,5,5,5]
unit_edge_join_ranks=[9,9,9,9,8,9]
unit_equal_edges=0/6
unit_frobenius_edge_shifts=[[],[],[],[],[],[]]
unit_frobenius_equal_edges=0/6
all_equal_pairs=0/15
```

So unit label-cycling does not formally collapse the fixed-row subspaces.
A cyclic-subspace theorem could still exist, but it would require extra CM
arithmetic identifying a genuine operator/action on `L`.  The verifier
equivariance still propagates a proved representative p-unit; it does not
prove that p-unit.

### 2026-06-05: relative content versus mixed-rank boundary

I added:

```text
p24/content_vs_mixed_rank_boundary_toy.py
p24/relative_content_to_mixed_rank_boundary.md
```

The surviving relative-content route says, roughly, that right-frequency
packets are not identically zero.  The mixed rank theorem is stronger:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157).
```

The toy constructs a rank-one centered profile whose right Fourier
components are all nonzero:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/content_vs_mixed_rank_boundary_toy.py
```

Output:

```text
nonzero_right_frequency_count=5/5
profile_span_rank=1/5
all_nonzero_right_frequencies=1
mixed_full_rank=0
```

Thus exact packet content does not imply the mixed marginal rank.  To use the
content route, it must be strengthened to a frame theorem:

```text
A_G(X) = X^(p^156)-X
```

for the subspace polynomial of the centered profile values.  This gives a
second possible finite p-unit surface:

```text
centered-profile Moore determinant nonzero
  => rank_Fp C_{157,211}=156.
```

This surface is weaker than `L_rep` because it does not prove delete-one
right support, but it is enough for the mixed marginal rank and may be better
for a direct class-field/lattice proof because it avoids right trace-dual
coordinates.

I also added:

```text
p24/p24_centered_profile_manifest.py
```

It names the alternative scalar:

```text
M_profile_leading =
  det((G_s^0)^(p^i))_{0<=s,i<156}
```

with implication:

```text
M_profile_leading != 0
  => span_Fp{G_s^0}=F_p(mu_157)
  => rank_Fp C_{157,211}=156.
```

### 2026-06-05: centered-profile finite gate and normal-frame route

I added:

```text
p24/lean/CenteredProfileGate.lean
p24/centered_profile_normal_frame_toy.py
```

The Lean gate checks two sufficient finite routes:

```text
M_profile_leading p-unit
  => full profile span
  => mixed centered marginal rank;

profile span contains a normal Frobenius orbit
  => full profile span
  => mixed centered marginal rank.
```

The second route is a useful theorem hook but has a real extra hypothesis.
The toy:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/centered_profile_normal_frame_toy.py --q 3 --degree 8
```

reported:

```text
normal_orbit_rank=8/8
profile_rank_with_one_normal_coordinate=1/8
profile_one_step_stability_defect=1
frobenius_closure_rank=8/8
normal_coordinate_alone_implies_full_span=0
contained_normal_orbit_implies_full_span=1
```

So a normal `G_s^0` value alone is not enough.  A proof must show that its
Frobenius orbit lies in the profile span, or directly prove the
centered-profile Moore p-unit.

### 2026-06-05: centered-profile trace-Gram equivalent

I added:

```text
p24/centered_profile_trace_gram_toy.py
```

For the full square leading profile window, the Moore p-unit is equivalent to
a trace-Gram p-unit:

```text
Gamma_profile_leading =
  det(Tr_{L/F_p}(G_s^0*G_t^0))_{0<=s,t<156}.
```

This may be a better class-field/lattice hook than the raw Moore determinant.
The toy verifies the finite distinction:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/centered_profile_trace_gram_toy.py --q 3 --dim 8 --trials 1000
```

reported:

```text
square_full_rank=552
square_gram_full_rank=552
square_rank_gram_mismatches=0
lower_independent=997
lower_independent_gram_singular=353
```

Thus square full-dimensional trace-Gram is equivalent to basis rank, while
lower-dimensional Gram determinants can still be singular on independent
subspaces.  This avoids the earlier Gram pitfall by using the full
`156 x 156` profile window.

I also reran the small actual-CM centered-profile stress row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_left_subfield_normality_audit.py \
  --only-D -13319 --max-rows 1 --max-h 200 --max-abs-D 14000 \
  --min-n 5 --max-n 5 --q-stop 20000 --max-splitting-primes 1 \
  --max-axis-dim 20 --max-m 40 --min-factor-degree 3 \
  --max-factor-degree 10 --max-extension-degree 8 --include-linear \
  --min-left-orbit-len 3 --summary-only
```

Key output:

```text
full_left_span_tests=8
centered_profile_rank_mismatches=0
centered_profile_subfield_failures=0
max_centered_profile_stability_defect=0
max_centered_profile_single_normal_rank=3
delete_one_full_left_span_tests=5
delete_one_leading_full_tests=5
centered_trace_zero_support_tests=0
centered_trace_one_support_tests=0
```

This is still only a small-degree actual-CM convention/stress check, but it
shows the centered-profile, normal-frame, and delete-one diagnostics agreeing
on a real row.

### 2026-06-05: base-field trace-Gram formula

I added:

```text
p24/centered_profile_trace_formula_toy.py
p24/centered_profile_moore_trace_gram_identity_toy.py
p24/centered_profile_trace_gram_basefield_formula.md
```

For `p24`, `p` is primitive modulo `157`, so:

```text
Tr_{F_p(mu_157)/F_p}(zeta^a) = -1 + 157*[a=0].
```

For centered coefficient vectors the `-1` part cancels, giving:

```text
Tr(G_s^0*G_t^0) = 157 * sum_r a_{r,s} a_{-r,t}.
```

Thus the centered-profile Gram determinant is a base-field determinant:

```text
Gamma_profile_leading = 157 * A_lead^T * J_inv * A_lead,
```

and:

```text
det(Gamma_profile_leading)
  = 157^156 * det(A_lead^T * J_inv * A_lead).
```

Since `157` is a p-unit, the centered-profile certificate can now be stated as:

```text
det(A_lead^T * J_inv * A_lead) != 0 mod p.
```

This is a cleaner class-field/lattice-facing object than the raw Moore
determinant because it uses only the base-field centered Hermitian marginal
coefficients and the explicit left inversion pairing.

Toy outputs:

```text
centered_profile_trace_formula_toy.py:
  trace_formula_mismatches=0
  noncentered_formula_mismatches=100

centered_profile_moore_trace_gram_identity_toy.py:
  identity_mismatches=0
  trace_gram_equals_moore_square=1
  trace_gram_punit_iff_moore_punit=1
```

The p24 arithmetic theorem is still open, but the finite target is now more
concrete:

```text
B_profile_leading =
det(A_lead^T * J_inv * A_lead) is a p-unit.
```

### 2026-06-05: leading difference-minor route

I added a still simpler sufficient base-field scalar:

```text
p24/centered_marginal_difference_minor_theorem.md
p24/centered_marginal_leading_minor_audit.py
```

For the doubly-centered mixed marginal

```text
C(r,s)=M(r,s)-M(r,0)-M(0,s)+M(0,0),
1 <= r < 157, 1 <= s < 211,
```

define:

```text
Delta_C_leading =
  det(C(r,s))_{1 <= r <= 156, 1 <= s <= 156}.
```

Then `Delta_C_leading != 0 mod p` directly implies
`rank_Fp C_{157,211}=156`.  This is not equivalent to the centered-profile
Moore window; it is a sufficient visible-minor route using the first
right-difference columns `G_s-G_0`.

Small actual-CM determinant audits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py --only-D -13319 \
  --max-rows 8 --max-cases 1 --max-h 200 --max-abs-D 14000 \
  --max-composite-quotients 20 --max-axis-dim 50 --max-m 60 \
  --max-n 80 --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py --only-D -6719 \
  --max-rows 8 --max-cases 1 --max-h 200 --max-abs-D 8000 \
  --max-composite-quotients 20 --max-axis-dim 50 --max-m 60 \
  --max-n 80 --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_leading_minor_audit.py --only-D -10919 \
  --max-rows 8 --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-axis-dim 50 --max-m 60 \
  --max-n 80 --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear
```

reported:

```text
D=-13319: full_rank_applicable_pairs=9,  leading_full_pairs=9
D=-6719:  full_rank_applicable_pairs=12, leading_full_pairs=12
D=-10919: full_rank_applicable_pairs=12, leading_full_pairs=12
full_rank_but_leading_zero_pairs=0 in all three runs.
```

Origin shifts `1,2` for `D=-13319` and shift `1` for `D=-6719` preserved
the same zero count.  This supports the CS/cyclic-code theorem candidate:
the leading projection appears to be full whenever the actual small-CM
centered marginal is full.  It remains heuristic evidence, not a certificate.

### 2026-06-05: mixed Cauchy-Binet boundary for Delta_C

I added:

```text
p24/centered_marginal_cauchy_binet_audit.py
p24/centered_marginal_cauchy_binet_boundary.md
```

For component differences `L_a`, selected right differences `R_b`, and the
packet Hermitian trace form `B`, the leading centered marginal window is:

```text
C_lead = A * B * R^t.
```

Therefore:

```text
Delta_C_leading =
  <L_1 wedge ... wedge L_r, R_1 wedge ... wedge R_r>_{wedge B}
  = sum det(A_S) det(B_{S,T}) det(R_T).
```

This is the clean exterior-form identity behind the CS/rank-condenser route.

Audits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_cauchy_binet_audit.py \
  --only-D -6719 --only-left 3 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 8000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_cauchy_binet_audit.py \
  --only-D -13319 --only-left 4 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 14000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 2 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_cauchy_binet_audit.py \
  --only-D -10919 --only-left 4 --only-right 4 \
  --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 1 \
  --max-factor-degree 12 --include-linear
```

reported:

```text
D=-6719,  factor_degree=4,  window_dim=2:
  nonzero_terms=30, off_diagonal_terms=24,
  leading_term=4382, window_det=4733.

D=-13319, factor_degree=4,  window_dim=3:
  nonzero_terms=16, off_diagonal_terms=12,
  leading_term=10420, window_det=554.

D=-10919, factor_degree=12, window_dim=3:
  left_pluecker_nonzero=220/220,
  right_pluecker_nonzero=220/220,
  nonzero_terms=6160, off_diagonal_terms=5940,
  leading_term=7493, window_det=6470.
```

So the natural power-basis Cauchy-Binet expansion is dense.  The easy theorem

```text
Delta_C_leading = unit * leading_left_minor * leading_right_minor
```

is false beyond dimension-reason degeneracies.  The surviving proof target is
the whole exterior trace pairing, or a new basis/filtration that triangularizes
it.

### 2026-06-05: origin-stable product for Delta_C

I added:

```text
p24/centered_marginal_origin_product_audit.py
p24/centered_marginal_origin_product_theorem.md
```

For `h=m*n`, an origin shift decomposes as:

```text
shift == n*alpha + m*beta mod h.
```

The Hermitian pairing cancels the packet monomial shift `beta`, so
`Delta_C_leading` depends only on the CRT-axis translation `alpha`.  This
packages the selected-origin minor into:

```text
Pi_C = prod_{alpha mod m} Delta_C(alpha).
```

For p24 this product would have `m=66254` factors, far below `sqrt(p)` but
still requiring a p-unit theorem or class-field norm identity.

Audits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_origin_product_audit.py \
  --only-D -6719 --only-left 3 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 8000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 1 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_origin_product_audit.py \
  --only-D -13319 --only-left 4 --only-right 7 \
  --max-cases 1 --max-h 200 --max-abs-D 14000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 1 \
  --max-factor-degree 12 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_origin_product_audit.py \
  --only-D -10919 --only-m 12 --only-left 4 --only-right 4 \
  --max-cases 1 --max-h 200 --max-abs-D 12000 \
  --max-composite-quotients 20 --max-m 60 --max-n 80 \
  --q-stop 200000 --max-splitting-primes 1 \
  --max-factor-degree 12 --include-linear
```

reported:

```text
D=-6719:  alpha_zero_count=0, alpha_distinct_count=7,
          alpha_product=1042, beta_distinct_histogram={1:21}.

D=-13319: alpha_zero_count=0, alpha_distinct_count=14,
          alpha_product=3636, beta_distinct_histogram={1:28}.

D=-10919: alpha_zero_count=0, alpha_distinct_count=1,
          alpha_product=11026, beta_distinct_histogram={1:12}.
```

So beta cancellation is exact in the tested rows, and the alpha product is
nonzero in the dimension-eligible rows.  The p24 theorem can now be phrased
as a p-unit theorem for `Pi_C`, or as the stronger factorwise nonvanishing of
all `Delta_C(alpha)`.

I then strengthened the origin-product audit to normalize by the determinant
of left translation on the zero-sum hyperplane:

```text
epsilon_c(alpha)=(-1)^(c-gcd(c,alpha)).
```

After this normalization, the alpha values should depend only on
`alpha mod d`.  The reruns reported:

```text
D=-6719,  pair=(3,7): left_sign_normalized_right_mismatches=0,
                         left_sign_normalized_right_classes=7.

D=-13319, pair=(4,7): left_sign_normalized_right_mismatches=0,
                         left_sign_normalized_right_classes=7.

D=-10919, pair=(4,4): left_sign_normalized_right_mismatches=0,
                         left_sign_normalized_right_classes=4.
```

For p24, `c=157` is odd prime, so `epsilon_157(alpha)=1` for every alpha.
Thus:

```text
Pi_C = prod_{alpha mod 66254} Delta_C(alpha)
     = (prod_{t mod 211} F(t))^314.
```

The current compact product certificate target is therefore a 211-factor
cyclic right-translate product, not a 66254-factor product.

I also added:

```text
p24/centered_marginal_alpha_sequence_complexity.py
p24/centered_marginal_alpha_sequence_complexity.md
```

to test whether the reduced sequence `F(t)` has a small recurrence.  Runs on
the small rows reported full linear complexity:

```text
D=-6719,  pair=(3,7):  sequence_length=7,  complexity=7.
D=-13319, pair=(4,7):  sequence_length=7,  complexity=7.
D=-10919, pair=(3,13): sequence_length=13, complexity=13.
```

This demotes the simple recurrence/resultant shortcut.  The 211-factor p24
target should be treated as a full-support cyclic exterior product unless a
new CM-adapted coordinate system appears.

The product still has a clean algebraic packaging.  I added:

```text
p24/centered_marginal_cyclic_resultant_theorem.md
```

For the right-translation sequence `F(t)`, let `f_C(Y)` interpolate
`F(t)=f_C(omega^t)`.  Then:

```text
Pi_C,right = prod_{t mod 211} F(t)
           = Res_Y(Y^211 - 1, f_C(Y)).
```

Since `ord_211(p)=35`, the 211 translations split into one fixed value and
six nonzero Frobenius orbits of size `35`, giving:

```text
F(0) * product of six size-35 orbit products.
```

This gives a seven-factor finite-field certificate surface.  It is currently
the cleanest p24 formulation of the product route, but the p-unit theorem for
those seven factors remains missing.

I corrected a too-strong interpretation by adding:

```text
p24/centered_marginal_resultant_factor_audit.py
p24/centered_marginal_resultant_factor_boundary.md
```

A base-coefficient interpolant would force `F(q*t)=F(t)`.  The small rows fail
that compatibility and have full DFT support:

```text
D=-6719,  pair=(3,7):  frobenius_compatibility_mismatches=5,
                       dft_support_size=7/7.

D=-13319, pair=(4,7):  frobenius_compatibility_mismatches=4,
                       dft_support_size=7/7.

D=-10919, pair=(3,13): frobenius_compatibility_mismatches=11,
                       dft_support_size=13/13.
```

Thus the seven factors are orbit products of base values, not presently norms
of a base-coefficient cyclic interpolant.

I also tested the natural BCH/cyclic-code shortcut by adding:

```text
p24/centered_marginal_cyclic_code_boundary.py
p24/centered_marginal_cyclic_code_boundary.md
```

The determinant sequence is cyclic, but the row space is not stable under
cyclic right shifts in the small actual-CM analogues:

```text
D=-6719,  pair=(3,7):  row_rank=2, max_shift_span_rank=4,
                       shift_stable_count=0/6.

D=-13319, pair=(4,7):  row_rank=3, max_shift_span_rank=6,
                       shift_stable_count=0/6.

D=-10919, pair=(3,13): row_rank=2, max_shift_span_rank=4,
                       shift_stable_count=0/12.
```

Thus ordinary BCH/Reed-Solomon/cyclic-code theorems are not directly
available.  The cyclic object that remains is the resultant of the determinant
sequence, not an invariant cyclic row code.

I added the dual plateau formulation and uncertainty boundary:

```text
p24/plateau_uncertainty_boundary_toy.py
p24/centered_marginal_plateau_uncertainty_boundary.md
```

For centered marginal point columns `P_b`, a right-window determinant

```text
F(t)=det(P_{t+1}-P_t,...,P_{t+156}-P_t)
```

vanishes if and only if some nonzero dual word

```text
w_lambda(b)=lambda(P_b)
```

is constant on the `157` consecutive positions `t,...,t+156`.  Thus
`Pi_C,right != 0` is equivalent to no nonzero dual trace word having a
157-term cyclic plateau.

Plain prime cyclic uncertainty is not strong enough.  A plateau leaves a word
supported on at most `54` positions after subtracting the constant, forcing
Fourier support at least `158`, while the profile can use all `210` nonzero
frequencies.  The toy over `F_53` of length `13` produced a word with an
8-term plateau, zero frequency absent, and full nonzero Fourier support:

```text
time_support_after_subtracting_constant=5
frequency_support_after_subtracting_constant=12
nonzero_frequency_support_full=1.
```

So the plateau formulation is useful, but the missing theorem is still
CM/exterior-trace arithmetic, not a generic uncertainty theorem.

I added the affine-arc/intersection form:

```text
p24/centered_marginal_plateau_intersection_audit.py
p24/centered_marginal_affine_arc_theorem.md
```

The point columns `P_b in F_p^156` satisfy:

```text
F(t) != 0
  <=> P_t, P_{t+1}, ..., P_{t+156} are affinely independent.
```

So the p24 right-product theorem is exactly that the 211 ordered
centered-marginal points form a cyclic consecutive 157-arc in affine
156-space.

Small actual-CM rows had zero plateau intersections, while both cyclic shift
and Frobenius multiplier permutations enlarged the row span:

```text
D=-6719,  pair=(3,7):  code_rank=2,
                       cyclic_shift_span_rank=4,
                       frobenius_multiplier_span_rank=4,
                       zero_plateau_intersections=7/7.

D=-13319, pair=(4,7):  code_rank=3,
                       cyclic_shift_span_rank=6,
                       frobenius_multiplier_span_rank=6,
                       zero_plateau_intersections=7/7.

D=-10919, pair=(3,13): code_rank=2,
                       cyclic_shift_span_rank=4,
                       frobenius_multiplier_span_rank=4,
                       zero_plateau_intersections=13/13.
```

Thus the affine-arc formulation is exact, but not explained by simple
row-code symmetries.

I tested the stronger full-affine-arc condition with:

```text
p24/centered_marginal_full_arc_audit.py
p24/centered_marginal_full_arc_boundary.md
```

Small actual-CM rows had no zero affine subsets:

```text
D=-6719,  pair=(3,7):  subset_count=35,  zero_subset_count=0.
D=-13319, pair=(4,7):  subset_count=35,  zero_subset_count=0.
D=-10919, pair=(3,13): subset_count=286, zero_subset_count=0.
```

But random baselines were also almost always full arcs:

```text
200/200, 200/200, and 194/200 random full-arc counts.
```

So the full-arc strengthening is consistent but looks generic.  The live
certificate remains the cyclic consecutive 211-factor product unless a
natural class-field proof gives full-arc/MDS strength for free.

I tested whether the full-arc behavior visibly comes from a low-degree
projective curve:

```text
p24/centered_marginal_projective_geometry_audit.py
p24/centered_marginal_projective_geometry_boundary.md
```

Degree-2 and degree-3 homogeneous form nullities matched random baselines
exactly in the tested rows, and coordinate sequences had full
Berlekamp-Massey complexity:

```text
D=-6719, degree 2:  form_nullity=0, random={0:200}.
D=-13319, degree 2: form_nullity=3, random={3:200}.
D=-10919, degree 2: form_nullity=0, random={0:200}.

D=-6719, degree 3:  form_nullity=3,  random={3:100}.
D=-13319, degree 3: form_nullity=13, random={13:100}.
```

So the easy rational-normal/moment-curve MDS explanation is not visible in
the natural coordinates.

I tested the component-character/exterior-DFT version of the right orbit
product:

```text
p24/centered_marginal_exterior_dft_audit.py
p24/centered_marginal_exterior_dft_boundary.md
```

For centered point columns `P_b`, the consecutive determinant has the exact
expansion

```text
F(t)=sum_{|S|=d} det(Q_S) det(zeta^(s*i)-1) zeta^(t*sum S),
```

where `Q_s` are right Fourier coefficients.  The audit verified this identity
with zero reconstruction failures and zero Frobenius-covariance failures in
three pinned actual-CM rows.  But all tested rows were dense:

```text
D=-6719,  pair=(3,7):  nonzero terms 15/15, support 7/7.
D=-13319, pair=(4,7):  nonzero terms 20/20, support 7/7.
D=-10919, pair=(3,13): nonzero terms 66/66, support 13/13.
```

Thus the exterior character expansion is useful theorem language for the
seven p24 orbit products, but not an evaluator: the p24 expansion has
`binom(210,156) ~= 10^50.79` subset terms before using additional CM
arithmetic.  The live proof still needs an embedded class-character trace,
Moore/subspace-polynomial p-unit, or equivalent finite-field identity.

I recorded the productive ML/probability role in:

```text
p24/ml_identity_mining_plan.md
```

The rule is strict: learning may rank exact objects, but a successful output
must become a finite-field identity, Moore determinant p-unit, cyclic
resultant, class-field norm, or explicit anti-annihilator lemma.  The local
`p24/upstream_DANGER3` files contain Montgomery Pomerance triples, not the CM
fibers or class-character periods used by the centered marginal theorem, so
they are useful for calibrating original search heuristics but not for
directly training a proof of the current CM rank certificate.

I added the first concrete Lang/Moore identity-mining audit:

```text
p24/lang_pivot_order_miner.py
p24/lang_pivot_order_mining_boundary.md
```

It tests right-orbit orderings for the representative leading Moore minor and
records full-block/tail residual norm products.  On the pinned positive
actual-CM row

```text
D=-13319, q=13463, pair=(7,7),
```

both delete-one rows had full leading pivots `[0,1,2]`, nonzero base-field
residual products, and zero residual-norm failures.  A three-right-orbit row

```text
D=-5444, q=2657, pair=(3,4)
```

also had robust full pivots, but its right orbits all had length `1`, so it is
not a p24-shaped tail analogue.  Direct richer-row searches with multiple
right orbits of length `>1` were stopped after exceeding the intended
small-job budget; they should be driven by a cheap candidate index before
packet construction.

I added that cheap candidate layer:

```text
p24/lang_tail_shape_index.py
p24/lang_tail_shape_index_boundary.md
```

It uses `qfbclassno`, quotient shapes, `Kronecker(D,q)=1`, Frobenius orbit
lengths, and Hermitian packet degree, but does not build Hilbert roots or
packets.  It reproduces the known non-tail shape

```text
D=-13319, h=140, m=28, n=5, left=7:L3, right=7:orbits[3,3],
```

and the heavy miner now accepts `--only-q` so such candidates can be tested
directly.  Bounded shape-only searches for a true small `full blocks + tail`
analogue found no candidates, including windows up to
`max_h=1000, max_abs_D=180000, q_stop=600000` and a larger 25-second capped
window up to `max_h=5000, max_abs_D=900000, q_stop=1200000`.

I added a unit-orbit transversality boundary:

```text
p24/unit_orbit_transversality_toy.py
p24/unit_orbit_transversality_boundary.md
```

The toy treats the six right blocks as `A_j=A D^j` and tests the
representative p24 shape `four full blocks + one tail slice`.  A cyclic
identity action is perfectly equivariant but fails transversality
identically.  A permutation action often succeeds in small random controls
but not always.  Conclusion: the right-unit theorem is a compression theorem
only.  It propagates one proved representative p-unit to all six deletion
rows, but it does not prove the representative nonvanishing.  The live
arithmetic target remains `L_rep=B_rep*T_rep != 0 mod p`.

The CS sidecar sharpened the coding-theory import to an MSRD/LRS candidate:

```text
p24/msrd_lrs_import_boundary.md
p24/msrd_vs_mds_boundary.md
p24/msrd_metric_boundary.md
p24/lang_arc_strength_audit.py
p24/lang_arc_strength_boundary.md
```

If the 210-coordinate mixed trace-dual code were block-equivalent to an
`[210,156]` linearized Reed-Solomon/MSRD code, its sum-rank distance would be
`55`.  The representative bad support is exactly `35+19=54`, so this would
rule out the bad lambda and prove `L_rep != 0`.

I added the finite Lean gate:

```text
p24/lean/MSRDSupportGate.lean
```

It checks the exact implication and the numeric inequality
`35+19 < 210-156+1`; it does not prove the arithmetic MSRD equivalence.
I then added the metric boundary: the `35+19` count is scalar-coordinate
Hamming support unless a sum-rank expansion is explicitly supplied.  In coarse
six-right-block support, every word has support at most `6`, and Lean checks
that distance `55` would force every word to be zero.  Thus a valid LRS/MSRD
route must specify a rank metric of total length `210`, not merely cite
six-block support.

I tested the stronger ordinary full-Moore-arc proxy on two pinned actual-CM
rows:

```text
D=-13319, q=13463, m=28, pair=(7,7):
  subset_full=20/20, delete_one_leading_full=[1,1],
  random_full_arc_count=199/200.

D=-5444, q=2657, m=12, pair=(3,4):
  subset_full=3/3, delete_one_leading_full=[1,1,1],
  random_full_arc_count=200/200.
```

This keeps the MSRD/LRS proof route plausible, but the random baselines show
the small-row full-arc property is generic at these field sizes.  The actual
missing theorem is still arithmetic: prove a class-field/skew-polynomial
block equivalence or a selected support determinant p-unit identity.

I added a projective-geometry discriminator:

```text
p24/lang_projective_relation_audit.py
p24/lang_projective_relation_boundary.md
```

For the dimension-3 actual-CM row `D=-13319, q=13463, pair=(7,7)`, the six
Lang columns have no conic relation:

```text
relation_degree=2
monomial_count=6
relation_rank=6
relation_nullity=0
random_positive_nullity_count=0/200.
```

So the natural Lang coordinates are full-arc/MDS-like but not visibly
GRS/rational-normal-curve-like.  Any successful LRS/MSRD proof must use
blockwise skew structure or a hidden coordinate equivalence, not the simplest
ordinary projective geometry.

I added a Heegner-support diagnostic for the easy phase-aware divisor route:

```text
p24/phase_divisor_heegner_support_scan.py
p24/phase_divisor_heegner_support_boundary.md
```

It interpolates the packet scalar as a rational function of the selected `j`
root and compares numerator roots with target CM roots and small Heegner roots.
Results:

```text
D=-2239, q=2243, ell=2, m=7, n=5, hermitian:
  rational_degree=18
  numerator_roots=[940,1191]
  target_cm_hits=0
  small_heegner_hits=0/2.

D=-2239, q=2243, ell=2, m=5, n=7, hermitian:
  rational_degree=17
  numerator_roots=[].

D=-5000, q=1259, ell=3, m=10, n=3, hermitian:
  rational_degree=15
  numerator_roots=[285,564]
  target_cm_hits=0
  small_heegner_hits=1/2.
```

The ordinary autocorrelation control on `D=-2239,m=7` has rational degree `0`.
Thus the live Hermitian phase scalar is not a simple plain-`j`
Heegner-supported divisor.  A Borcherds/Schofer proof would need a genuinely
phase-aware divisor construction.

I added a block-subspace-design audit for the CS-theory route:

```text
p24/lang_block_subspace_design_audit.py
p24/lang_block_subspace_design_boundary.md
```

The theorem language is now:

```text
the six right Frobenius blocks W_j subset F_p(mu_157)
have the support-specific array-code profile needed by the representative
row: four full blocks span 140 dimensions and the selected tail contributes
16 more.
```

I also extended:

```text
p24/lean/MixedSubspacePolynomialGate.lean
```

with the exact p24 gate:

```text
prefixRank = 4*35, tailAug = 16 => FullSpan leadingRank 156.
```

Pinned actual-CM rows:

```text
D=-13319, q=13463:
  block_generic=3/3 in the (7,7) and (7,4) rows;
  random_block_generic=200/200.

D=-5444, q=2657:
  block_generic=7/7;
  random_block_generic=200/200;
  random_delete_tail=200/200.
```

The known shape-only `D=-26519` family again failed actual-CM realization in
the block audit:

```text
q=293 rows=0
q=373 rows=0.
```

Conclusion: block-subspace design is a clean CS theorem surface, but the
small data still looks generic and does not supply a special identity.  The
p24 proof still needs a selected support subspace-polynomial p-unit, a valid
metric-preserving LRS/MSRD equivalence, or the equivalent trace-intersection
theorem.

I added the linearized trace-gcd formulation of the representative theorem:

```text
p24/linearized_trace_gcd_certificate_boundary.md
p24/lang_trace_gcd_kernel_audit.py
p24/lean/TraceGcdGate.lean
```

The class-field-facing statement is:

```text
T_j(lambda)=Tr_{E/R}(lambda*S_j),
K = common kernel of the four representative prefix trace blocks,
dim_Fp K = 16,
tail_16 has rank 16 on K.
```

Equivalently:

```text
gcd_p-lin(P_K, tail_16) = X.
```

Lean checks the p24 numerical gate:

```text
kernelDim=16, tailRankOnKernel=16 => trace-gcd degree 0.
```

The pinned `D=-13319` actual-CM row has a nontrivial tail-only analogue:

```text
pair=(4,7), left=L2, right_lengths=[3,3]
omit0: K=2, tailK=2, gcddeg=0, det=2125, match=1.
omit1: K=2, tailK=2, gcddeg=0, det=11423, match=1.
```

The pinned `D=-5444` row has only full-prefix, no-tail cases:

```text
each deletion: K=0, tailK=0, gcddeg=0.
```

This does not prove p24, but it names the arithmetic theorem more cleanly:
prove a selected-prime linearized resultant/nonzero tail determinant on the
actual prefix trace kernel.

I added the finite Schur/Pluecker identity boundary for the trace-gcd
determinant:

```text
p24/kernel_tail_schur_identity_toy.py
p24/kernel_tail_schur_identity_boundary.md
```

The exact Pluecker identity is:

```text
det([A;B]_{X,Y}) = det(A_X) * det(B|_K),
```

so the tail-on-kernel determinant is the quotient of a leading determinant by
a prefix pivot determinant.  This verifies the convention but does not create
a new p24 proof.

The Gram Schur identity is:

```text
det([A;B][A;B]^T) * det(N^T N)
  = det(A A^T) * det(BN)^2.
```

It suggests a possible stronger local-lattice route, but finite-field controls
show it is not formal:

```text
q=3, r=8, s=4, trials=1000:
  full_prefix=995
  full_leading=528
  prefix_rank_gram_singular=368
  gram_mismatches=0.

q=2, r=8, s=4, trials=1000:
  full_prefix=953
  full_leading=278
  prefix_rank_gram_singular=547
  gram_mismatches=0.
```

Conclusion: the direct trace-gcd determinant remains the smallest target.
The Gram route may be useful only if a separate p-adic/local-lattice theorem
proves the relevant prefix/full/kernel Gram p-units.

I added the origin-action audit and boundary for the trace-gcd determinant:

```text
p24/lang_trace_gcd_origin_action_audit.py
p24/lang_trace_gcd_origin_action_boundary.md
```

For an origin shift

```text
shift == n*alpha + m*beta mod h,
```

the pinned actual-CM row:

```text
D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7)
```

reported:

```text
records=280
det_zero_count=0
det_distinct_count=14
gcd_failure_count=0

omitted=0:
  zeros=0, distinct=7, product_all_mod_q=3871
  alpha_fixed_product_distinct=7, period=7
  beta_fixed_product_distinct=1, period=1
  alpha_value_period=7, beta_value_period=1

omitted=1:
  zeros=0, distinct=7, product_all_mod_q=4697
  alpha_fixed_product_distinct=7, period=7
  beta_fixed_product_distinct=1, period=1
  alpha_value_period=7, beta_value_period=1
```

Corrected interpretation: the determinant is invariant along the `beta`
packet/monomial direction and varies along the `alpha` direction, with
period equal to the right component `7` in this toy row.  This points to the
origin-stable p-unit package:

```text
Pi_trace,i = prod_{t mod 211} det(tail_i on K_t) != 0 mod p
```

for p24, rather than an `h`-term class-set product.  This is stronger than
the selected-origin theorem but far smaller than enumeration.  The missing
proof is now a class-field divisor/norm identity for the right-translation
trace-gcd determinant sequence, or a direct proof that all its factors are
p-units.

I promoted the origin-action observation to an explicit finite covariance
theorem:

```text
p24/lang_origin_covariance_theorem.md
p24/lang_origin_covariance_toy.py
p24/lean/TraceOriginProductGate.lean
```

The algebraic statement is:

```text
H'(u,v) = zeta^(-alpha*(u*m/c + v*m/d)) H(u,v),
```

and, after Lang trivialization on a right Frobenius orbit:

```text
W'_O = eta_alpha * C_gamma * W_O.
```

Equivalently, for trace maps:

```text
T_j^(alpha,beta) = V_{j,t} o T_j o U_alpha,  t=alpha mod d,
K_(alpha,beta) = U_alpha^(-1)K_0.
```

The toy checks this DFT/Lang formula on random marginal tables, independent
of CM data.  The pinned runs:

```text
q=5,left=3,right=7
q=2,left=3,right=5
q=3,left=5,right=7
```

all reported `mismatches=0` for every alpha.  The new Lean gate records the
finite implication:

```text
all right-cycle factors good + origin covariance
  => the selected origin trace-gcd determinant is good.
```

Thus the origin-reduction part of the route is now a finite algebra theorem.
The remaining arithmetic target is sharply:

```text
prod_{t mod 211} Delta_i(t) != 0 mod p.
```

I added a sequence-complexity audit for this reduced determinant sequence:

```text
p24/lang_trace_gcd_sequence_complexity.py
p24/lang_trace_gcd_sequence_complexity.md
```

On the same nontrivial actual-CM row:

```text
D=-13319, q=13463, pair=(4,7), right_lengths=[3,3]
```

the reduced right sequences have length `7`, no zeros, and unexpectedly low
complexity:

```text
omitted=0:
  product_mod_q=6352
  linear_complexity_two_periods=3/7
  connection=[1, 6790, 6789, 13462]
  connection_divides_x^7-1=1
  frobenius_compatibility_mismatches=6

omitted=1:
  product_mod_q=6639
  linear_complexity_two_periods=3/7
  connection=[1, 6674, 6673, 13462]
  connection_divides_x^7-1=1
  frobenius_compatibility_mismatches=6
```

The two connection polynomials are the two degree-3 Frobenius factors of
`X^7-1` over `F_13463`.  A degenerate `(4,4)` control row was constant
with complexity `1`.

New theorem candidate:

```text
Delta_i(t) has spectral support in one right Frobenius orbit.
```

For p24 this would reduce the 211-factor determinant sequence to a single
degree-35 right factor:

```text
Delta_i(t) = Tr_{F_{p^35}/F_p}(A_i*zeta_211^t)
```

up to units/conventions.  The remaining p-unit theorem would then be a
Gauss-period norm nonvanishing for `A_i`, rather than a generic 211-term
resultant.

I also added the exterior-support caveat:

```text
p24/lang_trace_gcd_exterior_support.py
```

For the small `(right=7, tail=2)` row, distinct exterior support has size `3`,
so the observed degree-3 recurrence is representation-compatible.  For p24:

```text
right=211, orbit_len=35, tail=16
k=1 distinct_subset_sum_size=35
k=2 distinct_subset_sum_size=210
k=3 distinct_subset_sum_size=211
...
k=16 distinct_subset_sum_size=211
```

Therefore generic p24 exterior support is full.  A degree-35 spectral collapse
would be valuable but must come from the special trace-gcd prefix kernel, not
from the bare right-action representation.

I added the Pluecker spectral boundary for the reduced determinant:

```text
p24/lang_trace_gcd_plucker_spectral_boundary.md
p24/lang_trace_gcd_plucker_spectral_toy.py
```

For the transported tail map `A:K->R`, selected coordinate projection `P`,
and right multiplication `V_t`, the determinant is:

```text
Delta(t)=det(P V_t A).
```

After diagonalizing the right action, Cauchy-Binet gives:

```text
Delta(t)
  = sum_{I subset O, |I|=k}
      det(P_I) det(A_I) zeta^(t*sum(I)).
```

The origin-product target is therefore exactly:

```text
Res_Y(Y^211 - 1, f(Y)) != 0 mod p,
```

where `f` is this Pluecker-Fourier polynomial.  The toy checker verified the
identity with zero mismatches:

```text
right=7, orbit=[1,2,4], k=2:
  possible_support=[3,5,6], actual_support=3.

right=11, orbit=[1,3,9,5,4], k=3:
  possible_support={1,...,10}, actual_support=10.
```

This pins the remaining theorem: either prove special Pluecker cancellations
for the actual trace-gcd `A` so `f` has small Frobenius support, or prove the
full 211-term cyclic resultant is a p-unit.

I added the finite verifier/certificate spec for this target:

```text
p24/lang_trace_gcd_resultant_certificate_spec.md
p24/lang_trace_gcd_resultant_certificate_toy.py
```

The value-based certificate is:

```text
Delta_0,...,Delta_210 in F_p,
Inv_0,...,Inv_210 in F_p,
Delta_t*Inv_t=1 for every t.
```

Equivalently, once the values are trusted or recomputed, a seven-orbit product
certificate checks the six length-35 right Frobenius orbits plus `t=0`.
Because the small actual trace-gcd row has
`frobenius_compatibility_mismatches=6/7`, this is not naturally a
base-coefficient polynomial over `F_p`; the polynomial/resultant form lives
over the split right algebra unless extra Frobenius compatibility is proved.

The toy verified both success and forced-zero failure:

```text
success:     product_resultant_match=1, gcd_degree=0, bezout_unit_certificate=1
force-zero: product_resultant_match=1, gcd_degree=1, bezout_unit_certificate=0.
```

Thus the finite verifier is small.  The remaining producer problem is to
construct the actual `Delta_t` values, Pluecker coefficients, or a p-unit
divisor/norm identity from embedded CM data without enumerating the class set.

I added route accounting across the current certificate surfaces:

```text
p24/certificate_route_accounting.py
p24/certificate_route_accounting.md
```

It reports:

```text
formal_m_plus_n/sqrt = 3.173695e-6.

trace-gcd:
  finite_value_count=211,
  generic_plucker_terms=binom(35,16)=4059928950,
  generic_exterior_support=211.

L1:
  packet_degree=388430,
  axis_dim=368,
  visible_degree_n_plus_partials=1152860611,
  visible_degree_over_sqrt=1.152860611e-3.

centered difference:
  leading_minor_size=156,
  determinant_entries=24336.
```

This ranks `L1` as the most plausible arithmetic producer, because its data is
already organized by the `2`, `157`, and `211` tower layers, even though
trace-gcd remains the smallest finite verifier.

I then sharpened the `L1` theorem target from a 368-dimensional rank statement
to a group-algebra annihilator statement:

```text
p24/l1_axis_annihilator_theorem.md
p24/l1_axis_group_algebra_annihilator_toy.py
```

The axis space is the cyclotomic support:

```text
Q_axis(Z) = Phi_1(Z) Phi_2(Z) Phi_157(Z) Phi_211(Z),
deg Q_axis = 368.
```

For each H-packet vector `beta_a`, axis injectivity is equivalent to:

```text
Ann(beta_a) cap W_axis = {0},
```

or:

```text
gcd(A_a(Z), Q_axis(Z)) = 1,
```

where `A_a` is the product of K-character factors killed by the packet vector.
The split group-algebra toy verified:

```text
full axis components nonzero:
  eval_rank=axis_dim, axis_injective=1.

planted killed axis exponent:
  eval_rank=axis_dim-1, axis_injective=0.
```

So the preferred `L1` finishing theorem is now: every p24 H-packet has nonzero
projection to the constant, 2-axis, 157-axis, and 211-axis cyclotomic
components.

I then pushed the `L1` axis theorem through the tensor-factor and trace-frame
refinements:

```text
p24/trace_frame_split_frontier.md
```

After adjoining `E=F_p(mu_m)`, one degree-388430 H-packet splits into 70
degree-5549 tensor factors.  Since `5549=31*179`, the preferred finite
certificate is now the three-coordinate trace frame

```text
x |-> (Tr_{B/C}(x), Tr_{B/C}(theta*x), Tr_{B/C}(theta^2*x)),
```

where `[C:E]=179` and `[B:C]=31`.  The missing theorem is the exact
trace-annihilator avoidance statement:

```text
W_axis(B) cap span_C{1,theta,theta^2}^perp = {0}.
```

Equivalently, for every nonzero axis weight `w`, the element
`g'(theta)*x_w` has a nonzero `theta^30`, `theta^29`, or `theta^28`
coefficient over `C`.

This compresses the theorem surface from the degree-388430 packet to a
`368`-dimensional rank statement inside `C^3`, whose `E`-dimension is
`3*179=537`.  The formal finite implications are already Lean-gated; the
remaining gap is arithmetic p-unit/noncollapse for these top coefficients.

I then restated the trace-frame target as a flag-transversality theorem:

```text
p24/trace_frame_flag_transversality_theorem.md
```

For the flag

```text
F_j = {x in B : deg_C(g'(theta)*x) <= j},
```

we have `ker Top_k = F_{30-k}`.  Thus the p24 theorem is

```text
W_axis(B) cap F_27 = {0}.
```

The stronger maximum-rank-profile form predicts:

```text
dim_E(W_axis cap F_29)=189,
dim_E(W_axis cap F_28)=10,
dim_E(W_axis cap F_27)=0.
```

I extended `p24/tensor_factor_dual_basis_window_audit.py` to count maximum
rank profile failures.  On the targeted `D=-10919` tensor rows it found:

```text
max_rank_profile_tests=115
max_rank_profile_failures=0.
```

So the next proof target is a selected-prime Schubert-position/p-unit theorem
for the CM axis subspace, not another generic rank scan.

I then tested a stronger sum-rank erasure version of the same trace-frame
code:

```text
p24/trace_frame_sum_rank_erasure_theorem.md
p24/tensor_factor_relative_block_erasure_audit.py
```

After multiplying by `g'(theta)` and expanding over `B/C`, the p24 axis image
is an `E`-linear code:

```text
W_axis(B) subset C^31,
dim_E W_axis(B)=368,
dim_E C=179.
```

The trace-frame certificate only needs one `3`-block projection to be
injective.  The stronger theorem asks every `3`-block projection to be
injective, equivalently no nonzero word is supported on `28` relative
coefficient blocks.  A sum-rank proof would need:

```text
d_sumrank(W_axis) > 28*179 = 5012.
```

The targeted `D=-10919` tensor audit found:

```text
rows=5
targets=44
subset_tests=102
subset_failures=0
top_failures=0.
```

So small tensor data supports the stronger erasure profile.  This does not
prove p24, but it gives a clearer CS/class-field target: prove either the
selected top-three Schubert coordinate is a p-unit, or prove the relative
coefficient code is equivalent to a high-distance sum-rank/LRS object.

I then added exact p24 accounting and a random calibration:

```text
p24/trace_frame_sum_rank_erasure_accounting.py
p24/trace_frame_sum_rank_erasure_accounting.md
p24/tensor_factor_relative_block_erasure_random_baseline.py
```

The p24 relative coefficient code has:

```text
31 blocks,
block dimension 179,
axis dimension 368,
binom(31,3)=4495 possible 3-block projections.
```

An MSRD/LRS proof would have Singleton distance `5182`, while the trace-frame
erasure theorem only needs distance `5013`, leaving slack `169`.

The random-subspace union bound over all `4495` projections still has

```text
log10(failure) ~= -2.227680e7.
```

and random controls for the small `D=-10919` shapes had zero failures in
`200` trials per shape.  So the erasure audit is not proof-like evidence; it
is a consistency check for a possible class-field/LRS/MSRD theorem.

Finally I checked whether the relative coefficient code has a visible
LRS/MSRD signature in the natural basis:

```text
p24/tensor_factor_relative_block_structure_audit.py
p24/trace_frame_lrs_signature_boundary.md
```

For the pinned `D=-10919, m=12` axis analogue, both `subdegree=2` and
`subdegree=3` cases matched random controls exactly on block-rank histograms,
pair-rank histograms, and Toeplitz/Hankel/cyclic displacement ranks.  All
flattened displacement ranks were maximal:

```text
toeplitz=hankel=cyclic_toeplitz=cyclic_hankel=6.
```

So the off-the-shelf visible-LRS route is demoted.  A valid MSRD proof would
need a non-obvious class-field block equivalence, while the selected
top-three Schubert p-unit remains the smallest certificate surface.

I then made the selected top-three certificate surface explicit:

```text
p24/trace_frame_selected_plucker_certificate.md
p24/trace_frame_selected_plucker_accounting.py
```

For one H-packet and one tensor factor, the coordinate-free object is:

```text
Omega_top3 = wedge_{s in S_axis} Top_3(R_s)
             in Exterior_E^368(C^3).
```

The theorem is `Omega_top3 != 0`.  A finite verifier names one Plucker
coordinate:

```text
delta_I != 0 in E,
I subset {1,...,537}, |I|=368.
```

The accounting reports:

```text
tensor_factor_count_over_E=70
tensor_factor_degree_over_E=5549
top_target_dimension=537
log10 binom(537,368)=143.820126
h_packet_count=8.
```

So the smallest current `L1` axis verifier surface is:

```text
one named Plucker coordinate per H-packet,
or a degree-8 product/norm of those selected coordinates.
```

The remaining theorem is a selected-prime class-field p-unit statement for
those coordinates, not a generic rank theorem.

I then sharpened the selected Plucker surface to a named leading-prefix
coordinate:

```text
p24/trace_frame_leading_plucker_pivot_theorem.md
p24/trace_frame_plucker_pivot_audit.py
```

The p24 coordinate candidate is:

```text
I_lead = first 368 coordinates of C^3
       = 179 + 179 + 10.
```

This matches the maximum-rank-profile shape:

```text
rank Top_1 = 179,
rank Top_2 = 358,
rank Top_3 = 368,
```

so the final p24 tail is a `10`-coordinate determinant on `ker Top_2`.

On the pinned actual-CM tensor analogue `D=-10919, m=12`, the new pivot audit
reported leading-prefix pivots across the tested origins:

```text
axis rows:
  rows=40
  full_top_rank_rows=40
  top_rank_failure_rows=0
  subdegree=2 top_count=3 blocks=[0,1,2] count=20
  subdegree=3 top_count=2 blocks=[0,1] count=20

constant_plus_4:
  rows=24
  full_top_rank_rows=24
  pivot columns always [0,1,2,3]

constant_plus_3:
  rows=24
  full_top_rank_rows=24
  pivot columns always [0,1,2]
```

A broader row scan spent time in Hilbert-root setup and was stopped; pinned
structural rows are the right workflow here.  The theorem target is now:

```text
prove delta_lead is a p-unit in every p24 H-packet,
or prove the eight-packet product of delta_lead values is a p-unit.
```

I then added a value-level residual audit:

```text
p24/trace_frame_leading_residual_value_audit.py
```

This computes the actual leading determinant and the Gaussian pivot products
grouped by top block.  On the same pinned full-axis row:

```text
rows=24
nonzero_determinant_rows=24
zero_determinant_rows=0
determinants_in_base_field=0
determinant_norms_available=24
distinct_det_norms=2
zero_det_norms=0
```

The two norms correspond to the two toy intermediate subdegrees:

```text
subdegree=2, top_count=3: det_norm=11069 across tested origins
subdegree=3, top_count=2: det_norm=8644 across tested origins
```

The determinant itself did not descend to the base field; its norm did.  The
individual block residual norms were nonzero but varied with origin.

Important caveat: the stable full-axis norm in the `m=12` toy is likely
dimension-forced, because there:

```text
raw_rank = tensor_factor_degree = 6.
```

That is not p24-shaped, where:

```text
raw_rank = 368 << tensor_factor_degree = 5549.
```

I reran the same audit on lower-rank axis analogues from the same CM row:

```text
m=4: raw_rank=4, tensor_factor_degree=6
m=3: raw_rank=3, tensor_factor_degree=6
```

Both reported:

```text
rows=24
nonzero_determinant_rows=24
zero_det_norms=0
distinct_det_norms=24
```

So the p24-shaped evidence is nonvanishing of the selected leading coordinate,
not free origin-invariance of its norm.

I separated the harmless and hard origin directions in:

```text
p24/trace_frame_leading_origin_covariance.md
```

For an origin shift

```text
u == n*alpha + m*beta mod h,
```

the full-axis frequency sum satisfies:

```text
Sum(S_axis) == m/2 mod m.
```

So alpha shifts multiply the full-axis determinant by `(-1)^alpha`; since
`[E:F_p]=5460` is even, its norm is `1`.  Beta shifts remain the real
arithmetic content:

```text
delta_lead -> det(P_lead * Top_3 * theta^(-beta) | W_axis).
```

Component-plus-constant value runs also had no zero determinant norms, but
their norms varied across origins:

```text
constant_plus_4: rows=24, zero_det_norms=0, distinct_det_norms=24
constant_plus_3: rows=24, zero_det_norms=0, distinct_det_norms=24
```

So the refined p24 target should be stated as a full-axis leading determinant
norm theorem at the selected embedded origin:

```text
Norm_{E/F_p}(delta_lead) != 0
```

or an eight-packet product of those selected-origin norms.  An origin-stable
strengthening would need a beta product over H-translates.  The residual
factorization remains useful bookkeeping for the `179+179+10` tail, but the
small data warns against trying to prove component residual p-units
independently or assuming origin covariance for free.

Synthesis/rabbit-hole audit:

```text
trace-frame/flag surface: still the best L1 theorem surface;
origin-stable norm story: rabbit-hole risk unless it becomes an explicit
  beta-product or class-field norm identity;
leading prefix: verifier-useful coordinate candidate after fixing the
  trace-frame basis/order, not intrinsic Grassmannian magic.
```

The sharp next theorem candidate remains:

```text
For each p24 H-packet, with the fixed trace-frame normal basis/order,
Norm_{E/F_p}(delta_lead(beta_0)) != 0
```

for the selected embedded origin `beta_0`.  The intrinsic way to attack it is
still the flag failure contradiction:

```text
bad packet => exists 0 != w in W_axis with g'(theta)*x_w of relative degree <= 27.
```
