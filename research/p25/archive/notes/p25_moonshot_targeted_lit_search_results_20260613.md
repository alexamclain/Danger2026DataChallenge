# p25 Moonshot Targeted Lit Search Results

Updated: 2026-06-13

## Executive Read

The literature search produced two live first-class probes and one Robert/Siegel
producer refinement:

- HD/GK: reflection alone on the naive Jacobi gamma divisor leaves a signed
  two-cell residue on `(1,2)` and `(2,1)`.  Continue narrowly only if the
  Hasse-Davenport multiplication/unit step removes the false positive and
  accounts for the free `U(169)` symbol.  Semiprimitive cubic purity rewrites
  `U(169)` and `U(338)` to `1`, but by itself still leaves the signed two-cell
  scalar residue.
- Barnes/hypergeometric: the support-only gate kills order-3-only
  Helversen-Pasotto product deltas, keeps the full `C_507` seed-exponent point
  delta `q=138` support-live, and kills `p^2` orbit-closed deltas as too large.
  McCarthy's well-poised exceptional character delta now numerically realizes
  this single-point target over `F_2029`: `LHS-main_sum` is supported exactly at
  `q_exp=138`, and the singleton maps to the existing raw-Y payload closure.
  The powered quotient is now sharpened to the pointwise unit
  `U(q)=1+(zeta_39^5-1)*e_138(q)` with order `39`; after normalization it is
  exactly `e_138`, but all three of `e_138`, `U-1`, and `U` are Fourier-dense
  on `C_507`.  Continue only with theorem endpoint/delta production or an
  equivalent arithmetic unit quotient, not with a cheap Fourier-filter story.
  A new endpoint harness lets theorem hits emit sparse `q coeff` pairs in
  either projector form `138 1` or unit-minus-one form `138 1375`.  A new
  multiplicative-route falsifier shows why support-only theorem hits are not
  enough: the invalid additive routes are also singleton-supported but have the
  wrong coefficient/order.  A GK/HD projection-legitimacy scout found no
  standard theorem that licenses post-hoc `R -> R^2029`; treat the power step
  as suspect unless a quotient-level cancellation or modulo-`mu_2029`
  interpretation is found.  An auxiliary-prime invariance probe strengthens
  this downgrade: `R(138)^2029` lands in `mu_39` only in the minimal auxiliary
  field, not at the next two primes containing the same required roots.  A
  theorem-factor normalization scan then kills the easy missing-prefactor
  explanation: visible McCarthy denominator/prefactor/Gauss factors do not
  repair the auxiliary-prime failure.
- Robert/Siegel: translated odd quotients remain live only in the exact
  `base*K_trace*D_segment*(1-T)` skeleton.  Point quotients, inverse edges,
  even/squared edge symmetrizations, and missing kernel trace are killed.  The
  visible quotient factorization is rigid: `D=(1,3)` up to reversal and
  `T=(2,113)`.  Raw representative freedom is exactly kernel gauge:
  forward and reversed segments each have `25^3` exact gauges, and simple
  non-kernel right/C shifts fail.  The literal Kato/Robert subgroup-divisor
  quotient is killed because the required `D_segment` is not subgroup/coset
  support; weighted `y`, Siegel/Klein, differential, or finite-difference
  quotients remain live.

## A. HD/GK Unit Phase

Best sources:

- Gross and Koblitz, Gross-Koblitz formula:
  https://annals.math.princeton.edu/1979/109-3/p06
- Robert, digit-cycle / Stickelberger formulation:
  https://www.numdam.org/article/RSMUP_2001__105__157_0.pdf
- McCarthy, Hasse-Davenport and `p`-adic gamma identities:
  https://www.math.ttu.edu/~mccarthy/publications/SuperRV.pdf
- Long-Ramakrishna-style reflection identities:
  https://arxiv.org/pdf/1611.10188
- Keith Conrad, lifted Jacobi sums and Hasse-Davenport:
  https://kconrad.math.uconn.edu/blurbs/gradnumthy/LfunctionGaussJacobi.pdf

First gate:

```text
D = sum_{k=0}^{38} U(p^{2k+1}v) - sum_{k=0}^{38} U(p^{2k}v)
```

Build this formal `Gamma_p` divisor on `Z/507` after subtracting the
Stickelberger carry valuation.  Reduce using only reflection plus
Hasse-Davenport multiplication for `m=2,3,13`.

Pass condition:

```text
residual = pure sign/Teichmuller factors
character table nontrivial only at (2,1)
```

Kill condition:

```text
free Gamma_p symbols remain
or (1,2) receives the same residual phase as (2,1)
```

Recommendation: continue narrowly.  The `p^39 = -1 mod 507` orbit swap plus
quadratic Hasse-Davenport is a real unit-phase route.

Completed reflection precheck:

```text
(1,2):  +234 * U(169)
(2,1):  -234 * U(169)
all other seed cells: 0
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py
```

Consequence: reflection alone is killed as a complete explanation.  The
remaining HD/GK multiplication gate must remove the `(1,2)` false positive and
turn the remaining `U(169)` residue into a genuine unit phase or point
correction.

Completed semiprimitive cubic unit rewrite:

```text
p == -1 mod 3
p^39 == -1 mod 507
f = 78 = 2 * 39
U(169) -> 1
U(338) -> 1

after rewrite:
  (1,2): +234
  (2,1): -234
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py
```

Consequence: the free `U(169)` symbol is no longer the main obstruction.
Semiprimitive purity alone is still killed because the `(1,2)` false-positive
scalar remains; a further HD/triplication/endpoint relation must remove it.

## B. Barnes / Hypergeometric Delta

Best sources:

- Helversen-Pasotto / Sole, finite Barnes first lemma:
  https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C613ED7568AE9F24BC8F7DCFA58C8B9/S0008439500013035a.pdf/barnes_first_lemma_and_its_finite_analogue.pdf
- McCarthy, finite-field well-poised hypergeometric transformations:
  https://www.math.ttu.edu/~mccarthy/publications/Hyp%20Trans.pdf
- Greene, finite-field hypergeometric functions:
  https://www.d.umn.edu/~jgreene/papers/Hypergeometric_Trans.pdf
- Fuselier, Long, Ramakrishna, Swisher, and Tu:
  https://arxiv.org/pdf/1510.02575
- Li and Soto-Andrade, finite Barnes identities and `GL(2)`:
  https://eudml.org/doc/152567

First gate:

```text
support-only exponent test
```

Encode candidate correction predicates on `C_3 x C_169`, average under the
`p^2` orbit with the proposed odd/even carry weights, then apply the
`O*(1-E)` target screen.

Pass condition:

```text
support exactly (h,t) = (2,1)
outer S-image exactly {138,310,482}
```

Kill condition:

```text
Helversen-Pasotto delta fires on any other orbit member
```

If HP-only fails, test Greene/FLRST endpoint and point-delta terms before
killing the wider hypergeometric route.

Completed support-only result:

```text
order-3 HP product delta       -> killed
full C507 seed-exponent delta  -> support-live
p^2 orbit-closed delta         -> killed
```

Details:

```text
order-3 target line count = 8
unique target lines = 4
minimum extra cells = 2
exact order-3 target lines = 0
full seed delta q=138 support = (2,1)
outer S image = {138,310,482}
p^2 mod 507 = 373
p^2 orbit length = 39
p^2 orbit outer S support = 117 quotient classes
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_barnes_delta_support_gate.py
```

Recommendation: continue narrowly only for a full `C_507` seed-exponent
point/endpoint delta, or an equivalent Greene/FLRST correction.  Kill HP-only
if it only sees order-3 product parameters, and kill any version that closes
under the full `p^2` orbit before the point correction appears.

Completed McCarthy well-poised delta contract:

```text
character delta = delta(A_0^-1 * A_{n-1} * A_n)
a_0 - a_{n-1} - a_n = 138 mod 507
delta support = (138,)
outer S image = (138,310,482)
order-3-only support size = 169, killed
p^2 orbit outer S support size = 117, killed
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py
```

Completed McCarthy well-poised numeric delta:

```text
field = F_2029
character group order = 2028 = 4*507
auxiliary value field = F_20574061
n = 2
x = 2
A_1 = trivial
A_0 = omega^(4*138)
A_2(q_exp) = omega^(4*q_exp)
lower 1F0 factor = 1
delta support = (138,)
transformed difference support = (138,)
exceptional support = (138,)
theorem mismatch count = 0
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py
```

Consequence: the McCarthy exceptional term is now a genuine finite-field
point-delta producer before orbit closure.  The next falsifier is mapping that
`q_exp=138` point through the outer `S` image into the p25 raw-Y / bridge
payload without introducing a dense scalar background or raw-kernel failure.

Completed McCarthy numeric delta raw-Y bridge:

```text
mccarthy_support = (138,)
mccarthy_exceptional_support = (138,)
outer S image = (138,310,482)
frobenius projected anomaly terms = (138,310,482)
raw_y_length = 12675
raw_y_nonzero = 6300
raw_y_harness_ok = True
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py
```

Consequence: the finite support and payload gap is closed at the model level.
The remaining gap is parameter normalization as an actual p25 local
Jacobi/Barnes unit phase, without dense scalar repair.

Completed McCarthy normalization-density gate:

```text
q=43*(h+1)+9*t=138 selects exactly (h,t)=(2,1)
order-3 shadow selects the whole h=2 row
outer S image = (138,310,482)
outer S mod 169 values = (138,141,144)
LHS support count = 507
main_sum support count = 507
LHS Fourier support count = 507
main_sum Fourier support count = 507
support(LHS-main_sum) = (138,)
normalized degree-zero scalar balance support = 507
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_normalization_density_gate.py
```

Consequence: McCarthy parameters really do align with the p25 anomaly seed,
but the singleton is produced by theorem-level cancellation of two dense
hypergeometric packets.  Continue the Barnes/McCarthy lane only if the
candidate realizes the transformed difference, or an equivalent unit identity,
before raw lift.  Kill candidates that use only one McCarthy side, repair
degree by dense scalar background, or omit the explicit `S` trace.

Completed McCarthy transformed unit-quotient gate:

```text
R(q) = LHS(q) / main_sum(q)
main_sum has no zero on C_507
support(R(q)-1) = (138,)
outer S image = (138,310,482)
R(138) = 1790844
R(138)-1 = 1790843
ord(R(138)) = 79131 = 39 * 2029
ord(R(138)-1) = 20574060
R(138) not in mu_507 or mu_2028
ord(R(138)^39) = 2029
ord(R(138)^2029) = 39
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_unit_quotient_gate.py
```

Consequence: theorem cancellation does have a sparse multiplicative quotient
form, which is the most unit-shaped McCarthy artifact so far.  But the
exceptional value has a nontrivial additive-root component from the auxiliary
value field.  The direct character-valued unit phase is killed unless a
further identity cancels the `2029` component, descends the quotient to the p25
raw-Y coefficient field, or replaces it with an equivalent character-valued
quotient.

Completed McCarthy quotient power-descent gate:

```text
support(R(q)^2029 - 1) = (138,)
R(138)^2029 = zeta_39^5
ord(R(138)^2029) = 39
R(138)^2029 - 1 has order 20574060

control:
  R(138)^39 has order 2029
  R(q)^(39*2029) - 1 is zero everywhere
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_descent_gate.py
```

Consequence: the additive-root component can be killed by a natural power
descent while preserving singleton support.  The best current
Barnes/McCarthy target is now an order-39 powered quotient:

```text
R(q)^2029
```

Continue only if a theorem or producer can justify the `2029`th power before
raw lift, avoid arbitrary normalization of `zeta_39^5 - 1`, and connect the
order-39 singleton to the existing p25 raw-Y closure.

Completed McCarthy powered coefficient transport/raw-Y gate:

```text
F_2029 primitive root = 2
zeta_39 = 2^52 = 1358
zeta_39^5 = 1376
zeta_39^5 - 1 = 1375
(zeta_39^5 - 1)^-1 = 636

unnormalized:
  anomaly_projector_coefficient = 1375
  corrected seed payload at (2,1) = 656
  quotient_packet_exact = False
  raw_y_harness_ok = False

normalized by 636:
  anomaly_projector_coefficient = 1
  corrected seed payload = all ones
  quotient_packet_exact = True
  raw_y_nonzero = 6300
  raw_y_harness_ok = True
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate.py
```

Consequence: coefficient-field descent and finite raw-Y closure are now closed
conditional on the powered quotient.  The remaining Barnes/McCarthy debt is
purely arithmetic: justify `R^2029` and the determined normalization by
`(zeta_39^5 - 1)^-1` inside the producer while preserving the explicit `S`
trace and kernel-trivial raw lift.

Completed McCarthy power-cost ledger:

```text
sqrt_floor = 3162277660168
power exponent = 2029
binary exponentiation multiplications = 18

2029 * S-trace support          = 6087
2029 * quotient packet support  = 511308
2029 * dense C_507 twist space  = 1028703
2029 * raw-Y support            = 12782700
2029 * full raw order           = 25717575

sqrt_floor // (2029 * full raw order) = 122961
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_cost_ledger_gate.py
```

Consequence: the powered normalized McCarthy route is not killed by sub-sqrt
size accounting, even under a deliberately pessimistic `2029 * full raw order`
bound.  Continue only on theorem legitimacy: produce or justify the powered
normalized quotient as an arithmetic unit/Barnes/McCarthy/HD-GK identity.

Completed McCarthy q-power projection gate:

```text
F_20574061^* order = 20574060
q-power = 2029
q-power kernel size = 2029
q-power image size = 10140

root action:
  mu_2028 fixed
  mu_39 fixed
  mu_2029 killed
  mu_5 sent to fourth power

target decomposition:
  R(138) = zeta_39^5 * additive_root^1475
  R(138)^2029 = zeta_39^5
```

Control:

```text
q-power is multiplicative but not additive:
  (2+3)^2029 = 18369750
  2^2029 + 3^2029 = 91572
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_q_power_projection_gate.py
```

Consequence: the `2029`th power is a precise multiplicative projection onto
the character-root component, not a field-Frobenius operation on the dense
hypergeometric identity.  Continue only with a theorem that first produces a
multiplicative unit quotient and then permits q-power projection plus the
determined coefficient normalization.

Completed McCarthy additive-character gauge gate:

```text
gauges checked: u = 1, 2, 13, -1
Gauss transform checked across all 2028 character exponents:
  g_u(A) = conjugate(A)(u) * g_1(A)

for each checked gauge:
  R(129) = 1
  R(138) = 1790844
  R(147) = 1
  R(138)^2029 = 12801419 = zeta_39^5
  ord(R(138)) = 79131
  ord(R(138)^2029) = 39
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_additive_gauge_gate.py
```

Consequence: the powered order-39 McCarthy target is not an artifact of the
chosen auxiliary additive character.  Continue to search for theorem
legitimacy of the multiplicative quotient/projection, not for a different
additive gauge.

Completed McCarthy idempotent-unit gate:

```text
U(q) = 1 + (zeta_39^5 - 1) * e_138(q) over functions on C_507 / F_2029
zeta_39^5 = 1376
zeta_39^5 - 1 = 1375
(zeta_39^5 - 1)^-1 = 636
support(e_138) = 1
e_138^2 = e_138
support(U - 1) = 1
order(U) = 39
(U - 1)/(zeta_39^5 - 1) = e_138
DFT support(e_138) = 507
DFT support(U - 1) = 507
DFT support(U) = 507
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_idempotent_unit_gate.py
```

Consequence: the current McCarthy target is sparse only as a theorem endpoint
or pointwise function; it is dense as an ordinary `C_507` Fourier filter.  The
moonshot should now ask literature/subagents for an identity that produces the
endpoint quotient or exceptional delta directly, then permits q-power
projection and the determined coefficient normalization.

Completed McCarthy endpoint candidate harness:

```text
accepted sparse endpoint formats:
  projector:        q coeff, e.g. 138 1
  unit-minus-one:   q coeff, e.g. 138 1375

positive controls:
  target projector roundtrip passes
  target U-1 roundtrip passes

endpoint checks:
  coefficient field = F_2029
  support(e_138) = 1
  support(U - 1) = 1
  order(U) = 39
  DFT support(e_138) = 507
  DFT support(U - 1) = 507
  raw-Y transport closes = true
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py
```

Candidate-mode controls:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py \
  --sparse-projector <(printf '138 1\n')

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py \
  --sparse-unit-minus-one <(printf '138 1375\n')
```

Consequence: a theorem-first hit can now be tested at the `C_507` endpoint
layer before anyone spends effort lifting to raw `C_12675`.  Passing this
harness verifies finite shape and raw-Y consequence only; the producer still
owes the arithmetic identity.

Completed McCarthy multiplicative-route falsifier:

```text
valid route:
  R(q) = LHS(q) / main_sum(q)
  R(q)^2029 - 1
  support = (138,)
  R(138)^2029 = 12801419
  ord(R(138)^2029) = 39

invalid additive routes:
  (LHS-main)^2029:
    support = (138,)
    target = 19995471
    order = 507

  LHS^2029 - main^2029:
    support = (138,)
    target = 6688559
    order = 5143515
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_multiplicative_route_falsifier_gate.py
```

Consequence: a theorem attempt must produce a multiplicative quotient before
q-power projection.  Additive powering and Frobenius-style subtraction are
killed even though they appear to preserve singleton support.

Completed GK/HD projection-legitimacy scout:

```text
found:
  x -> x^2029 is a precise local multiplicative projection:
    fixes mu_2028 and mu_39
    kills mu_2029
    sends R(138)=zeta_39^5*additive_root^1475 to zeta_39^5

not found:
  Gross-Koblitz / Hasse-Davenport / Davenport-Hasse / Greene / McCarthy theorem
  that licenses applying x -> x^2029 after the quotient already contains a
  mu_2029 component

normalization:
  (zeta_39^5-1)^-1 = 636 is canonical after accepting U
  but was not found as a theorem-forced GK/HD normalization before U exists
```

Consequence: continue the McCarthy route only if the additive component
cancels before projection, if the arithmetic object naturally lives modulo
`mu_2029`, or if a theorem directly produces the endpoint `U`/`e_138`.  The
next probe is auxiliary-prime invariance of the quotient/projection behavior.

Completed McCarthy auxiliary-prime invariance probe:

```text
same setup, target q=138, auxiliary primes ell = 1 mod 2029*2028*5

ell = 20574061:
  LHS-main = 2028
  ord(R) = 79131
  ord(R^2029) = 39
  R^2029 in mu_39 = true
  mu_39 exponent = 5

ell = 82296241:
  LHS-main = 2028
  ord(R) = 10287030
  ord(R^2029) = 5070
  R^2029 in mu_39 = false

ell = 144018421:
  LHS-main = 2028
  ord(R) = 48006140
  ord(R^2029) = 23660
  R^2029 in mu_39 = false
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe.py
```

Consequence: the McCarthy exceptional delta remains real, but the powered
quotient projection is not auxiliary-prime invariant.  The current route is a
strong finite diagnostic; it is not yet a credible certificate producer unless
the extra root components are removed by theorem-level structure.

Completed McCarthy theorem-factor normalization scan:

```text
scanned across auxiliary multipliers (1,4,7):
  raw quotient mu_39 hits = (true,false,false)

single visible factors, exponents +/-1,+/-2:
  denominator, prefactor, main_sum, main_term, lhs,
  g(a0), g(-a0), g(a0)g(-a0)
  scanned = 32
  repair-all count = 0
  repair-any count = 0

small Gauss monomials:
  g(a0)^i g(-a0)^j g(0)^k, exponents -2..2
  scanned = 124
  repair-all count = 0

small theorem monomials:
  denominator^i prefactor^j g(a0)^k g(-a0)^l, exponents -1..1
  scanned = 80
  repair-all count = 0
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan.py
```

Consequence: the powered McCarthy route is now useful mainly as a diagnostic
target.  To revive it as a certificate producer, we need a nontrivial identity
that removes the extra root components before projection, not a simple missing
prefactor.

Completed McCarthy projection literature scout:

```text
sources_checked = McCarthy Theorem 1.7, Greene finite-field hypergeometric
                  identities, Gross-Koblitz, Hasse-Davenport
verdict = no theorem-level license for post-hoc R(q)^2029 projection
first_falsifier = auxiliary-prime invariance of R(138)^2029
tested_orders = 39, 5070, 23660
recommendation = diagnostic_only_unless_new_endpoint_or_quotient_identity
```

Consequence: McCarthy remains a useful way to recognize the desired singleton
payload, but it should not consume certificate-search effort unless a candidate
produces uniform auxiliary-prime cancellation, a natural quotient modulo the
extra `mu_2029` roots, or a direct endpoint identity for `U`/`e_138`.

## C. Robert / Siegel Oriented Unit

Best sources:

- Sprang, Kato-Siegel theta divisor and differential formulas:
  https://arxiv.org/pdf/1802.04996
- Koo, Shin, and Yoon, ray-class fields from torsion/Siegel quotients:
  https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf
- Kubert and Lang, Siegel/Klein generators:
  https://eudml.org/doc/162977
- Streng, Klein/Siegel root-level behavior:
  https://www.numdam.org/item/10.5802/ahl.160.pdf
- Schertz, elliptic-unit ray-class quotients:
  https://www.numdam.org/item/JTNB_1997__9_2_383_0/
- Koo and Yoon, smaller Siegel-Ramachandra quotients:
  https://arxiv.org/abs/1407.5713

First gates:

```text
U_T(P) = Dtheta(P+T) / Dtheta(P-T)
Y_T(P) = y(P+T) / y(P-T)
T = (2,113) in C_3 x C_169
```

Emit a row-major `C_75 x C_169` source matrix, kernel-trace it, and run the
Robert source-matrix and bridge-edge quotient gates.

Pass condition:

```text
coupled D-segment/K-trace support
nonzero active odd projection
edge translation (2,113)
no rank-one C_169 separation
```

Kill condition:

```text
x-only even table
12N-power symmetrization before edge formation
right-trace times C-axis selector
plain C_169 character or sign tag
non-kernel raw representative shift
```

Recommendation: continue with Kato-Siegel translated quotient plus the
Koo-Shin-Yoon `y`/differential quotient first.  Use Schertz/Koo-Yoon quotients
as computational shortcuts only after the primary gates pass.

Completed finite skeleton:

```text
K_trace * (1 - T) only:
  raw support = 50, quotient support = 2, killed

K_trace * D_segment * (1 - T):
  raw support = 150, quotient support = 6, exact bridge

K_trace * D_segment * (1 - T^-1):
  raw support = 150, quotient support = 6, wrong orientation, killed

K_trace * D_segment * (1 - T)(1 - T^-1):
  raw support = 225, quotient support = 9, killed

K_trace * D_segment * (1 - T)^2:
  raw support = 225, quotient support = 9, killed

D_segment * (1 - T) without K_trace:
  raw support = 6, all 25 kernel modes, raw relation mismatch, killed
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_skeleton_gate.py
```

Consequence: the arithmetic producer must emit the coupled `D_segment` and
`K_trace` before the translated odd edge is formed.  Symmetrizing the quotient
before this stage destroys the bridge.

Completed quotient rigidity scan:

```text
positive layer = (0,31), (1,25), (2,28)
negative layer = (0,138), (1,141), (2,144)

factorizations:
  base=(1,25), D=(1,3),   T=(2,113)
  base=(0,31), D=(2,166), T=(2,113)
```

The second factorization is just the reversal of the first.  There is no other
visible AP segment and no other translated edge.

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_rigidity_gate.py
```

Completed raw-gauge scan:

```text
kernel shift K = (57,0)
forward raw gauges = 25^3
reverse raw gauges = 25^3
total exact raw gauges = 31250
simple non-kernel right/C shifts of base, D, or T fail
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py
```

Consequence: raw coordinates can be normalized by the kernel gauge `K=(57,0)`,
but a candidate cannot hide a different raw edge or AP segment outside that
gauge.

Hilbert-90 corner sign-candidate intake:

```text
candidate may emit only:
  eps a

where:
  eps = primitive D-unit sign in {+1,-1}
  a   = branch coefficient in {+1,-1}

forced expansion:
  orientation_mask = 1 if eps=+1, else 6
  recorded direction = 197 if a=-1, else 310
  row-labeled low/fiber triangle is forced
  raw support ladder = 75 -> 100 -> 150
  signed S-layer bridge image = +(25,197,369) -(138,310,482)
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness.py
```

Consequence: after the McCarthy powered route downgrade, the bridge lane has a
compact theorem-hit interface.  A Robert/Siegel/Hilbert-90 candidate should
first explain the two signs; only then should it expand to sparse source
triples or raw payloads.

Hilbert-90 corner sign-to-sparse-source intake:

```text
eps,a
  -> row-labeled source triangle
  -> quotient corner chain
  -> Hilbert-90 first boundary
  -> inversion boundary
  -> signed S-layer bridge
  -> 25-point K-trace sparse source triples in C_75 x C_169
  -> existing Robert sparse-source bridge harness
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness.py
```

Observed controls:

```text
all four sign pairs pass
quotient support ladder = 3 -> 4 -> 6
raw sparse support = 150
sparse entries equal target = true
existing Robert sparse-source harness ok = true
--eps 1 --branch -1 -> pass
--eps 0 --branch 1 -> fail
```

Consequence: the bridge lane now has a two-sign intake that promotes all the
way to the sparse-source contract without relaxing the bridge verifier.  The
remaining producer debt is the primitive `C_169` source/trace mechanism that
supplies the signs and row-labeled triangle.

Hilbert-90 corner triangle-candidate intake:

```text
candidate may emit three row-labeled points:
  row low fiber [coefficient]

rows = exactly 0,1,2
low,fiber in C_13
optional coefficients must match the branch sign
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness.py
```

Observed controls:

```text
all four active triangles pass
quotient support ladder = 3 -> 4 -> 6
raw sparse support = 150
explicit positive triangle ((0,0),(3,0),(1,11)) with coeff -1 -> pass
one-fiber-wrong control -> fail
```

Consequence: a Robert/Siegel/Hilbert-90 theorem hit can now be tested at the
primitive triangle layer before it explains the two signs or emits the full
sparse-source table.  This is still only an intake; the hard producer problem
is the primitive `C_169` triangle/sign mechanism.

Completed Robert/Kato-Siegel primitive `C_169` scout:

```text
continue = normalized odd y/wp' or Kato-Siegel dlog translated finite difference
kill = pure x, plain characters, literal subgroup divisors, split C13 x C13
finite_shadow = base * K_trace * D_segment * (1 - T)
base=(25,25), K=(57,0), D=(22,3), T=(38,113)
canonical_probe = eps=+1, branch=-1
triangle = row0=(0,0), row1=(3,0), row2=(1,11), coeff=-1
```

Best source-level target:

```text
Phi(P) = y(P+T)/y(P-T)
```

or

```text
dlog Dtheta(P+T) - dlog Dtheta(P-T)
```

where Koo-Shin-Yoon's normalized odd coordinate is

```text
y(r1,r2) = -g(2r1,2r2) / g(r1,r2)^4
```

Consequence: the bridge lane's first-class positive route is no longer a
generic Robert/Siegel quotient.  It is specifically a primitive level-`169`
odd-coordinate or Kato-Siegel logarithmic-derivative finite difference that can
emit the two signs, the row-labeled triangle, or the exact sparse triples.

Completed KSY-y / Kato-Siegel `dlog` route gate:

```text
accepted = base * K_trace * D_segment * (1 - T)
accepted_support = 150
accepted_bridge_contract = true

killed_controls:
  edge-only translated quotient -> support 50 / quotient support 2
  missing K trace               -> all 25 kernel modes, 12 raw mismatches
  inverse T                     -> wrong orientation
  even/x-like T                 -> scalar leak, wrong signed bridge
  D-boundary-only               -> support 100 / quotient support 4
  split C13 shadow of T         -> wrong trace, not primitive C169 edge
  literal subgroup divisor      -> cannot supply D segment
  split low/fiber triangle      -> fails triangle intake
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_dlog_route_gate.py
```

Consequence: the Robert lane now has an executable route matrix.  A proposed
KSY normalized `y/wp'` or Kato-Siegel `dlog` identity must hit the accepted
finite shadow or one of the smaller sign/triangle/sparse-source intakes; the
nearby lower-effort explanations are recorded as killed controls.

Completed KSY-y half-edge footprint gate:

```text
bridge edge T = (38,113)
half-edge H = (19,141), 2H = T
accepted symmetric quotient = y(P-H) / y(P+H), center base = base + H

controls:
  using +H                 -> inverse orientation, fail
  using T as half-shift    -> edge 2T, fail

normalized-y Siegel exponent footprint:
  y(Q) = -g(2Q)/g(Q)^4
  support = 300
  degree = 0
  coefficient counts = (-4,75), (-1,75), (1,75), (4,75)
  quotient support = 12
  bridge payload ok = false
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_half_edge_footprint_gate.py
```

Consequence: the analytic odd quotient must use the half-edge convention, and
the expanded normalized-`y` Siegel divisor must not be fed directly as the
sparse bridge payload.  A successful theorem route has to use the `y` values
or `dlog` identity before emitting signs, the primitive triangle, or sparse
triples.

Completed KSY-y projection/cancellation gate:

```text
normalized-y footprint = double_pushforward(bridge) - 4*bridge

layers:
  abs(coeff)=4, scaled by -1/4 -> exact 150-cell bridge, pass
  abs(coeff)=1                 -> doubled bridge, support 150, wrong trace
  coefficient-blind footprint  -> support 300, quotient support 12, fail
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_projection_gate.py
```

Consequence: normalized `y` is not merely a dead 300-cell footprint.  It
contains the bridge as a theorem-side coefficient layer, but a certificate
route still has to explain separation or cancellation of the doubled `g(2Q)`
layer.  This is the next concrete target for a Kato-Siegel `dlog` or
distribution identity.

Completed KSY-y doubling-distribution gate:

```text
doubling on C_75 x C_169:
  kernel size = 1
  source order = 780

doubled bridge:
  support = 150
  trace = wrong

full doubling orbit:
  union support = 11700
  orbit sum support = 7800
  orbit sum coefficients = +/-10
  alternating orbit sum = 0

lambda scan:
  normalized_y + lambda*doubled, -5 <= lambda <= 5
  only lambda=-1 reduces support to 150
  lambda=-1 gives -4*bridge; exact divide by -4 recovers bridge
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_doubling_distribution_gate.py
```

Consequence: the doubled `g(2Q)` layer is not killed by ordinary doubling
distribution or orbit averaging.  The live KSY/dlog theorem target is now
quite precise: provide exact doubled-layer subtraction, or an equivalent
logarithmic-derivative cancellation, before emitting the bridge payload.

Completed KSY/Kato-Siegel `dlog` chain gate:

```text
dlog footprint = 2*double_pushforward(bridge) - 4*bridge
support = 300
coefficient counts = (-4,75), (-2,75), (2,75), (4,75)

layers:
  abs(coeff)=4, scaled by -1/4 -> exact bridge
  abs(coeff)=2, scaled by 1/2  -> doubled bridge, wrong trace

lambda scan:
  dlog_footprint + lambda*doubled, -6 <= lambda <= 6
  only lambda=-2 reduces support to 150
  lambda=-2 gives -4*bridge; exact divide by -4 recovers bridge
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_dlog_chain_gate.py
```

Consequence: the chain-rule factor in a `dlog` route is not enough.  It doubles
the bad layer's coefficient but leaves the same cancellation debt: a real
Kato-Siegel identity must remove the `g(2Q)` contribution or keep it from
surviving as payload.

Robert/Kato-Siegel lit-scout synthesis:

The exact classical model for the finite footprint is the Weierstrass sigma
duplication identity recorded as DLMF 23.10.10:
`wp'(z) = -sigma(2z)/sigma(z)^4`, up to normalization.  DLMF 23.10.3 gives the
addition identity controlling `y(P+h)/y(P-h)`, but it moves the obstruction to
the doubled arguments rather than removing them.

The closest Kato-Siegel formulation is the theta-function shape
`theta_D = Theta(u)^D^2 / Theta(Du)`, with distribution/norm identities in the
Kato/Scholl/Sprang literature.  The problem is exactly the uncomfortable case:
the natural `theta_2` inverse would isolate `g(Q)^4/g(2Q)`, but the standard
Euler-system norm laws inspected by the scout are stated in prime-to-6
settings, so `D=2` is not a free theorem import.

Transfer gate: continue only with a direct even-`D`/`theta_2` finite identity,
or with a half-trace/square-root normalization that explains the chain-factor
residue.  First falsifier is already local: any true `dlog` identity must pass
the `2*double_pushforward(bridge) - 4*bridge` chain-rule gate above.

Completed even-`D` / `theta_2` finite gate:

```text
theta2 inverse footprint = double_pushforward(bridge) - 4*bridge
theta2 footprint         = 4*bridge - double_pushforward(bridge)
support                  = 300
coefficient counts       = (-4,75), (-1,75), (1,75), (4,75)

[2] kernel on C_75 x C_169 = 1
theta2 norm over [2] kernel = theta2, still failing
inverse-doubling transport  = support 300, still failing

theta2 integral square root         = false
theta2 inverse integral square root = false
dlog integral half                  = true, but support 300

half_dlog + lambda*doubled:
  only lambda=-1 reduces support to 150
  lambda=-1 gives -2*bridge; exact divide by -2 recovers bridge
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_even_gate.py
```

Consequence: the even-`D` route is a precise target but not a free repair.  A
formal `[2]` norm, `[2]` transport, integral square root, or half-dlog
normalization does not remove the doubled `g(2Q)` layer.  Continue only for a
real extra even-2 identity.

Completed theta2 doubling-resolvent gate:

```text
theta2 = (4 - [2]) * bridge
[2] order on C_75 x C_169 = 780

(4 - [2])^-1 =
  (4^779 + 4^778[2] + ... + [2]^779) / (4^780 - 1)

denominator bit length       = 1560
denominator nonzero mod p25  = true
theta2 support               = 300
shifted theta2 term budget   = 234000
shifted theta2 union support = 11700
weighted numerator support   = 150
resolvent(theta2)            = bridge
resolvent(theta2_inverse)    = -bridge
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_resolvent_gate.py
```

Consequence: this is a positive finite artifact.  If a theorem can emit the
arithmetic `theta2` object, the doubled `g(2Q)` layer can be removed by a
sub-sqrt finite resolvent rather than by hand cancellation.  The remaining
debt is arithmetic production of `theta2` and legitimate normalization by
`4^780-1` or its p25 scalar inverse.

Completed theta2 support-period resolvent gate:

```text
ambient [2] order on C_75 x C_169 = 780
bridge/theta2 orbit period        = 156

active inverse:
  (4^155 + 4^154[2] + ... + [2]^155) / (4^156 - 1)

denominator bit length            = 312
gcd(4^156 - 1, p25 - 1)           = 1
shifted theta2 term budget        = 46800
shifted theta2 union support      = 11700
weighted exponent bit budget      = 7300800
proper period-divisor shortcuts   = all fail
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_support_resolvent_gate.py
```

Consequence: the active theta2 filter should use support period `156`, not
ambient order `780`.  This cuts the term budget by factor `5` and removes the
old `F_p^*` value-level root ambiguity for this filter.

Completed theta2 telescoping-certificate gate:

```text
compact KSY recipe:
  center_base = (44, 166)
  half_shift  = (56, 28)
  period      = 156

certificate identities:
  theta2 = (4 - [2]) * bridge
  [2]^156 bridge = bridge
  [2]^156 theta2 = theta2
  proper period-divisor shortcuts fail

orbit skeleton:
  touched doubling orbits = 27
  ambient orbit lengths   = 15 of length 156, 12 of length 780
  global [2]^156 identity = false
  support [2]^156 identity = true

cost:
  compact linear cell checks = 975
  expanded resolvent terms   = 46800
  improvement factor         = 48
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_telescoping_certificate_gate.py
```

Consequence: if a theorem emits the compact KSY theta2 object, the bridge
recovery can be certified by telescoping before expanding the full resolvent.
This is a verifier/certificate skeleton, not yet an arithmetic theta2
producer.

Completed theta2 factor-period certificate gate:

```text
bridge factor word:
  base * K_trace * D_segment * (1 - T)

period-156 source scale:
  [2]^156 = (61, 1) on C_75 x C_169

factor action:
  base=(25,25) fixed
  K=(57,0) maps to 11K, gcd(11,25)=1
  D=(22,3) drifts by 10K
  T=(38,113) drifts by 15K
  K_trace absorbs both drifts

period subcheck budget:
  factor support budget     = 31
  expanded subcheck budget  = 900
  floor improvement factor  = 29
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_period_certificate_gate.py
```

Consequence: the support-period identity is now explained by the p24-derived
bridge factors, not only by expanded support-orbit observation.  This is a
period/fixedness certificate inside the telescoping verifier; it is still not
an arithmetic theta2 producer.

Completed theta2 factor-certificate intake harness:

```text
accepted theorem output:
  base_right base_c
  K_right    K_c
  D_right    D_c
  T_right    T_c

target:
  base = (25, 25)
  K    = (57, 0)
  D    = (22, 3)
  T    = (38, 113)

derived KSY recipe:
  H           = T/2      = (19, 141)
  center_base = base + H = (44, 166)
  half_shift  = -H       = (56, 28)

checks:
  factor product passes bridge contract
  compact theta2^-1 and theta2 both pass
  period-156 K_trace absorption passes
  base -> base + K gauge passes
  wrong D, wrong T, collapsed K fail
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_certificate_harness.py
```

Candidate mode:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_certificate_harness.py \
  --base-right 25 --base-c 25 \
  --k-right 57 --k-c 0 \
  --d-right 22 --d-c 3 \
  --t-right 38 --t-c 113
```

Consequence: this is the smallest current finite verifier target for the
KSY/theta lane.  A future theorem/literature hit can emit the factor tuple
rather than sparse triples.  The missing object is still the arithmetic
producer that justifies this factor tuple/theta2 identity in challenge-legal
terms.

Completed theta2 factor-gauge normal-form gate:

```text
K subgroup:
  size 25 right-mod-3 kernel in C_75, C-coordinate 0
  primitive generators = 20

full coordinate presentations:
  20 primitive K generators
  25 independent base shifts
  25 independent D shifts
  25 independent T shifts
  accepted total = 312500

quotient target in (C_75/K) x C_169:
  base = (1, 25)
  D    = (1, 3)
  T    = (2, 113)

controls:
  K -> 2K passes
  mixed base/D/T K-gauge passes
  K -> 5K fails
  wrong D quotient class fails
  wrong T quotient class fails
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_gauge_normal_form_gate.py
```

Consequence: the finite verifier target is quotient-level factor data plus a
primitive generator of the `K` subgroup, not literal source coordinates.  This
is the cleanest current contract for a KSY/theta theorem producer.

Completed theta2 quotient-factor certificate harness:

```text
accepted theorem output:
  base class in (C_75/K) x C_169
  D class in (C_75/K) x C_169
  T class in (C_75/K) x C_169
  primitive K multiplier modulo 25

target:
  base = (1, 25)
  D    = (1, 3)
  T    = (2, 113)

default lifted section for K=(57,0):
  base        = (1, 25)
  D           = (1, 3)
  T           = (2, 113)
  H=T/2       = (1, 141)
  center_base = (2, 166)
  half_shift  = (74, 28)

controls:
  target candidate passes
  K multiplier 2 passes
  K multiplier 5 fails
  wrong base/D/T quotient classes fail
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness.py
```

Candidate mode:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness.py \
  --base-right-class 1 --base-c 25 \
  --d-right-class 1 --d-c 3 \
  --t-right-class 2 --t-c 113 \
  --k-multiplier 1
```

Consequence: the smallest current finite verifier intake is three quotient
classes plus a primitive `K` multiplier.  The arithmetic producer debt remains.

Completed theta2 source-quotient packet harness:

```text
accepted theorem output:
  six cells in source quotient coordinates (right mod 3, c)
  primitive K multiplier modulo 25

target packet:
  (1, 25)  +1
  (2, 28)  +1
  (0, 31)  +1
  (0, 138) -1
  (1, 141) -1
  (2, 144) -1

meaning:
  base * (1 + D + D^2) * (1 - T)
  base=(1,25), D=(1,3), T=(2,113)

controls:
  primitive K multiplier 2 passes
  nonprimitive K multiplier 5 fails
  positive-only packet fails
  wrong c packet fails
  normalized q-cycle six-cell packet fails
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_source_quotient_packet_harness.py
```

Consequence: a theorem/literature hit may aim for a direct six-cell source
quotient divisor packet.  Coordinate convention matters: this is not the older
normalized `q`-cycle packet.

Completed Hilbert-90 to KSY packet adapter:

```text
active Hilbert-90 signs:
  (-1,-1), (-1,+1), (+1,-1), (+1,+1)

all emit the same q-cycle bridge:
  (0, 46)  -1
  (0, 123) +1
  (1, 47)  -1
  (1, 121) +1
  (2, 48)  -1
  (2, 122) +1

coordinate conversion:
  q -> (q mod 3, q mod 169)

converted source quotient packet:
  (0, 31)  +1
  (0, 138) -1
  (1, 25)  +1
  (1, 141) -1
  (2, 28)  +1
  (2, 144) -1
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_hilbert90_packet_adapter_gate.py
```

Consequence: a finite theorem hit may arrive as Hilbert-90 two-sign data or as
the KSY six-cell source packet.  The adapter is coordinate bookkeeping, not an
arithmetic producer proof.

Completed Robert KSY/Hilbert-90 minimal producer spine gate:

```text
verified finite spine:
  Hilbert-90 signs
    -> source quotient packet
    -> quotient factor classes
    -> source factor tuple
    -> compact KSY theta2
    -> support-period/telescoping bridge recovery

budgets:
  source packet support         = 6
  quotient factor input cells   = 3
  factor support budget         = 31
  telescoping compact budget    = 975
  support resolvent term budget = 46800

controls:
  q-cycle/source-coordinate confusion rejected
  nonprimitive K rejected
  wrong quotient D rejected
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py
```

Consequence: the current moonshot target is no longer a broad Robert/Jacobi
shape search.  It is a challenge-legal arithmetic producer for one verified
finite spine: Hilbert-90 two-sign data, the six-cell source quotient packet,
the quotient factor classes, the source factor word, or compact KSY theta2
data.  The spine gate is a ledger and falsifier; it does not itself provide
the missing producer.

Completed Robert KSY/Hilbert-90 arithmetic-producer contract gate:

```text
accepted verifier interfaces:
  hilbert90_two_signs             size 2
  source_quotient_packet          size 6
  quotient_factor_classes         size 3
  source_factor_tuple             size 31
  sparse_theta2_divisor           size 300
  sparse_theta2_inverse_divisor   size 300
  compact_ksy_theta2              size 975

rejected or conditional shortcuts:
  theta2_value_unit_without_branch
  plain_bridge_as_theta2
  q_cycle_packet_as_source_packet
  nonprimitive_k_multiplier
  wrong_quotient_d_class
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py
```

Consequence: lit/proof hits now have an executable accept/reject contract.
Divisor/additive theta2 payloads may use the resolvent normalization; value
level multiplicative unit payloads are not enough unless the theorem supplies
root/branch selection, because `gcd(4^780-1,p-1)=11` leaves eleven value
branches and the finite bridge contract cannot choose one.  This keeps the
moonshot focused on a real arithmetic producer, not a finite-support mirage.

Completed Robert KSY/Hilbert-90 universal producer intake:

```text
supported candidate modes:
  hilbert90-signs
  source-packet
  quotient-factor
  source-factor
  compact-theta2
  theta2-sparse

positive controls:
  all accepted finite interfaces pass

negative controls:
  invalid signs fail
  q-cycle/source-coordinate confusion fails
  nonprimitive K fails
  wrong quotient D fails
  collapsed source-factor K fails
  plain bridge-as-theta2 fails
  wrong compact theta2 fails
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py
```

Candidate smoke test:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode hilbert90-signs --eps 1 --branch -1
```

Consequence: future theorem or literature hits can be fed to one front-door
harness and dispatched to the specialized verifier.  A pass means the finite
payload matches an accepted spine interface; the arithmetic-origin debt remains
separate.

Completed Robert KSY/Hilbert-90 payload fixture export:

```text
fixture directory:
  research/p25/producer_payload_fixtures

positive fixtures:
  source_packet_target.txt                  6 lines
  theta2_sparse_target.txt                300 lines
  theta2_inverse_sparse_target.txt        300 lines

reject fixtures:
  source_packet_q_cycle_reject.txt          6 lines
  theta2_sparse_plain_bridge_reject.txt   150 lines
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_payload_fixture_export.py
```

Verified universal-intake commands:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode source-packet \
  --packet research/p25/producer_payload_fixtures/source_packet_target.txt \
  --k-multiplier 1

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode theta2-sparse \
  --sparse-source research/p25/producer_payload_fixtures/theta2_sparse_target.txt
```

Consequence: future theorem/lit comparisons no longer need a manual
translation step for the file-based payload modes.  Compare against the stable
fixture files first, then decide whether the source identity is challenge-legal.

Completed Robert KSY/Kato-Siegel D=2 theorem-obligation gate:

```text
accepted theorem outputs:
  exact theta2 or theta2^-1 divisor payload
  compact KSY center_base=(44,166), half_shift=(56,28), orientation
  source packet or quotient factor shadow

rejected or conditional shortcuts:
  normalized-y footprint as bridge
  coefficient abs-4 layer filter by itself
  Kato-Siegel dlog chain-rule alone
  formal [2] norm or inverse-doubling transport
  square-root or half-dlog escape
  value-level unit payload without branch selection
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate.py
```

Consequence: the sharp theory target is now a challenge-legal `D=2` theta2
identity emitting one accepted payload.  Direct bridge recovery still needs
theorem-side doubled-layer cancellation, or else the accepted theta2
resolvent/certificate path.  A value-level multiplicative unit route still
needs root/branch selection.

Completed Robert KSY normalized-y product source-law gate:

```text
source law:
  y(Q) = -g(2Q)/g(Q)^4
  prod_{A in base*K_trace*D_segment} y(A)/y(A+T)

source data:
  base = (25,25)
  K    = (57,0), length 25
  D    = (22,3), length 3
  T    = (38,113)

finite output:
  forward quotient -> theta2^-1
  reversed quotient -> theta2
  support = 300
  compact KSY data = center_base=(44,166), half_shift=(56,28)

controls rejected:
  missing K
  collapsed K
  truncated D
  wrong D
  wrong T
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_normalized_y_product_gate.py
```

Consequence: the KSY `D=2` target is now formula-shaped, not merely an abstract
theta2 payload.  The missing proof is arithmetic legality of this normalized-y
product as a challenge-legal object.

Completed Robert KSY product-to-certificate chain:

```text
forward product:
  prod_A y(A)/y(A+T) = theta2^-1
  finite resolvent recovers -bridge

reversed product:
  prod_A y(A+T)/y(A) = theta2
  finite resolvent recovers bridge

budgets:
  source parameter budget       = 31
  theta2 payload support        = 300
  bridge support                = 150
  support-resolvent term budget = 46800
  support-resolvent union       = 11700
  compact telescoping budget    = 975
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_product_certificate_chain_gate.py
```

Consequence: a proof of the normalized-y product identity would now have a
complete finite certificate route to the bridge.  The remaining missing piece
is arithmetic legality of the product, not finite payload transport.

Completed normalized-y arithmetic-shape gate:

```text
quotient data:
  base class = (1,25)
  D class    = (1,3)
  T class    = (2,113)
  packet     = (1,25),(2,28),(0,31) positive and
               (0,138),(1,141),(2,144) negative

honest finite structure:
  K = (57,0), order 25
  K_trace size = 25
  K_trace is trivial in the quotient

non-norm theorem debt:
  D = (22,3)
  raw order(D)     = 12675
  visible order(D) = 507
  3D               = (66,9)
  visible 3D       = (0,9)
```

Payload count:

```text
centers                  = 75
y evaluation points      = 150
expanded g-divisor terms = 300
coefficient counts       = (-4,75), (-1,75), (1,75), (4,75)
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_normalized_y_arithmetic_shape_gate.py
```

Consequence: future theorem/lit scouts should not try to repackage the
length-3 `D_segment` as a hidden subgroup norm.  The viable target is a
challenge-legal KSY/Siegel-unit identity for the normalized-y product over a
true `K` trace, a short non-subgroup `D` segment, and the nontrivial `T` edge.

Completed normalized-y theorem-interface gate:

```text
primary theorem targets:
  prod_A y(A)/y(A+T) = theta2^-1
  prod_A y(A+T)/y(A) = theta2
  compact KSY center_base=(44,166), half_shift=(56,28), orientation

finite-only payloads:
  six-cell source quotient packet
  quotient factor classes base=(1,25), D=(1,3), T=(2,113)
  exact 300-term sparse theta2/theta2^-1 divisor footprint

conditional value routes:
  ambient 780 denominator: gcd(4^780 - 1, p - 1) = 11
  support-period 156 denominator: gcd(4^156 - 1, p - 1) = 1
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_theorem_interface_gate.py
```

Consequence: do not discard all value-level theorem hits automatically.  A
bare ambient-order value claim still needs branch selection, but a value-level
theta2 identity with the support-period fixedness/telescoping context has a
unique `F_p` root.  The lit-search brief is therefore: find a Kubert-Lang /
Siegel-unit / KSY distribution identity for the normalized-y product over a
true `K` trace and short non-subgroup `D` segment, with period-156
telescoping available if the theorem emits values rather than divisors.

Completed normalized-y theorem-source screen:

```text
continue:
  Sprang / Kronecker D=2
    highest-value D=2 differential or value-level theta2 source
  Kubert-Lang Siegel exponent matrix
    continue only as exact six-cell packet or 300-term theta2 search
  Koo-Shin-Yoon normalized wp-prime / y
    continue as value/differential source, not generic CM transfer

conditional:
  Kubert-Lang Siegel-Robert class-field units
    viable only with period-156 fixedness/telescoping or branch control

kill as direct shortcuts:
  ordinary Kato theta_D direct route for D=2
  literal Robert finite-subgroup support for D_segment
```

Primary source URLs:

```text
Sprang:
  https://arxiv.org/pdf/1802.04996
Scholl/Kato-Robert exposition:
  https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf
Kubert-Lang modular/Siegel units:
  https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_2
  https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4
  https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_11
Koo-Shin-Yoon:
  https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_theorem_source_screen_gate.py
```

Consequence: the next theory probe should not be a broad CM/Lang reread.  It
should either try to turn Sprang/Kronecker `D=2` differential/value data into
the period-156 theta2 interface, or solve a Kubert-Lang Siegel exponent-matrix
problem whose divisor is already known.

Completed Kubert-Lang exponent-matrix precheck:

```text
source packet at common level 507:
  support             = 6
  coefficient counts  = (-1,3), (1,3)
  sum mod 12          = 0
  quadratic right     = 0 mod 507
  quadratic c         = 0 mod 507
  quadratic mixed     = 0 mod 507

theta2 / theta2^-1 at raw level 12675:
  support             = 300
  coefficient counts  = (-4,75), (-1,75), (1,75), (4,75)
  sum mod 12          = 0
  quadratic right     = 0 mod 12675
  quadratic c         = 0 mod 12675
  quadratic mixed     = 0 mod 12675
```

Controls rejected:

```text
truncated D
wrong D
wrong T
positive-only packet
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate.py
```

Consequence: the Kubert-Lang/Siegel exponent-matrix route survives the first
quadratic congruence screen.  The level-`169` prime-power C-axis projection
also passes congruences but loses the right classes and `T` edge, so it is
finite-insufficient.  The remaining debt is a theorem-legal mixed-level
lift/product keeping the row-3 data, `T=(2,113)`, and the period-156 theta2
certificate.

Completed Kubert-Lang CRT-coupling refinement:

```text
common-level convention:
  q = 169 * right + 3 * c  mod 507

accepted graph lift:
  positive: (1,25) q=244 -> (2,28) q=422 -> (0,31) q=93
  negative: (0,138) q=414 -> (1,141) q=85 -> (2,144) q=263

visible steps:
  D = (1,3),    q_step = 178, order 507, 3D_q = 27
  T = (2,113),  q_step = 170, order 507
```

Projection and row-lift falsifiers:

```text
C169 row lifts with the same six projected cells = 729
KL congruence row lifts                          = 261
balanced KL row lifts                            = 93
D-segment/T-edge lifts                           = 9
fixed T=(2,113) lifts                            = 3
exact base + D + T lift                          = 1
full C169 pullback support                       = 18, not 6
row x C-projection product support               = 0
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate.py
```

Consequence: literature scouts should not accept a prime-power C169
Siegel-unit congruence as a producer.  A viable Kubert-Lang/Sprang/Robert
theorem source has to preserve the mixed `C_3 x C_169` graph selector
`(1,25)->(2,28)->(0,31)` and its `T=(2,113)` translate, or replace it with an
equivalent branch/period/differential mechanism.

Completed primitive-D crosswalk:

```text
D=(1,3)       -> D_q = 178, D_q^-1 = 94 mod 507
T=(2,113)     -> T_q = 170 = 263 * D_q
base=(1,25)   -> q = 244 = 121 * D_q

KL source packet =
  z^121*(1 + z + z^2)*(1 - z^263)

base-normalized packet =
  (1 + z + z^2)*(1 - z^263)
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate.py
```

Consequence: the Kubert-Lang graph packet is the existing primitive bridge
word under the `D`-coordinate change.  The prior primitive-product rigidity
scan already found only the forward signed `2 x 3` product and its reverse.
The theorem search target has not branched; it has three equivalent finite
interfaces: mixed source graph, primitive word, or KSY theta2 payload with the
period-156 certificate.

Completed KL inversion-pair decomposition:

```text
legal KL atoms inside the six target cells:
  z^121 - z^386
  z^122 - z^385
  z^123 - z^384

number of legal target-support subpackets:
  2^3 - 1 = 7
```

The natural KSY product uses three parallel `T` edges:

```text
z^121 - z^384
z^122 - z^385
z^123 - z^386
```

Only the middle `T` edge is itself KL-legal.  The elementary KL/Siegel
congruence screen sees anti-invariant inversion pairs `z^a-z^-a`, not three
independent `T`-edge units.

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_inversion_pair_gate.py
```

Consequence: theorem search should prefer sources for anti-invariant
Siegel/Robert pair quotients and then prove the identification with the KSY
`T=(2,113)` normalized-y product plus period-156 theta2 certificate.  Reject a
claim whose only KL explanation is three separately legal `T` edges.

Completed KL reflection bridge:

```text
base = (1,25)
D    = (1,3)
C    = base + D = (2,28)
T    = (2,113)

T    = -2C
T/2  = -C = (1,141)
```

The positive segment is:

```text
C-D = (1,25)
C   = (2,28)
C+D = (0,31)
```

The KSY `T` denominators are:

```text
C-D+T = -C-D = (0,138)
C+T   = -C   = (1,141)
C+D+T = -C+D = (2,144)
```

The inversion-pair denominators are the same set, with the outer two swapped:

```text
-(C-D) = -C+D = (2,144)
-C     = -C   = (1,141)
-(C+D) = -C-D = (0,138)
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_bridge_gate.py
```

Consequence: anti-invariant Siegel/Robert pair quotients can feed the KSY
theta2 payload if the theorem also proves the symmetric center law `T=-2C`.
This converts the new KL clue into a concrete theorem brief:

```text
produce anti-invariant pairs over C-D,C,C+D
use T=-2C to identify them with the KSY T-edge product
retain the K trace and period-156 theta2 certificate
```

Completed raw K-trace reflection lift:

```text
base = (25,25)
D    = (22,3)
K    = (57,0)
C    = base + D = (47,28)
T    = (38,113)

-2C        = (56,113)
T - (-2C) = (57,0) = K
```

So the raw relation is:

```text
T = -2C + K
```

For raw centers `A = C + jD + kK`, with `j=-1,0,1` and `k=0..24`:

```text
A + T = -C + jD + (k+1)K
```

This equals the inverse of the reflected numerator `C-jD+k'K` when
`k'=-k-1 mod 25`.  Thus the raw `T`-edge source packet and raw inversion-pair
source packet agree only after the full `K` trace.

Measured payloads:

```text
center support                    = 75
raw source packet support          = 150
normalized-y theta2 footprint      = 300
kernel-shifted -2C representatives = 25/25 accepted
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_gate.py
```

Consequence: the KL reflection clue now reaches the real raw KSY source law.
Literature/proof scouts can target anti-invariant pair quotients, but must
produce the full `K`-traced object; sparse K sections, truncated D segments,
and non-kernel `T` shifts are first falsifiers.

Completed anti-invariant normalized-y intake:

```text
accepted compact theorem interface:
  C = (47,28)
  K = (57,0)
  D = (22,3)
  orientation = forward or reverse

source centers:
  A = C + jD + kK,  j=-1,0,1; k=0..24
```

Forward product:

```text
prod_A y(A) / y(-A)
```

emits exact `theta2^-1` and recovers `-bridge`.

Reverse product:

```text
prod_A y(-A) / y(A)
```

emits exact `theta2` and recovers `bridge`.

Budgets:

```text
compact parameter cells       = 3
center support                = 75
theta2 payload support        = 300
bridge support after resolvent = 150
support-resolvent term budget = 46800
shifted union support         = 11700
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate.py
```

Consequence: this is the cleanest finite KL/KSY theorem target so far.  Search
for a challenge-legal modular/Siegel/Robert identity producing the raw
K-traced anti-invariant normalized-y product.  First falsifiers are missing or
collapsed `K`, truncated `D`, wrong `D`, or shifted center.

Completed raw exponent-saturation check:

```text
raw level = 12675

target raw anti-invariant source packet:
  support            = 150
  coefficient counts = (-1,75), (1,75)
  exponent sum       = 0 mod 12
  quadratic right    = 0 mod 12675
  quadratic c        = 0 mod 12675
  quadratic mixed    = 0 mod 12675
```

But the same elementary KL exponent screen is also passed by:

```text
missing K       support 6
collapsed K     support 6, coefficients +/-25
truncated D     support 100
wrong D         support 150
shifted center  support 150
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_exponent_saturation_gate.py
```

Consequence: raw exponent congruences are necessary hygiene but not a theorem
selector for the anti-invariant route.  A literature/proof hit must satisfy
the finite intake geometry and theta2 certificate path, not merely the raw
Kubert-Lang sums.

Completed anti-invariant selector-rigidity scan:

```text
quotient group = C_3 x C_169
centers scanned = 507
D steps scanned = 507
pairs scanned = 257049

forward theta2^-1 matches:
  C=(2,28), D=(1,3)
  C=(2,28), D=(2,166)

reverse theta2 matches:
  C=(1,141), D=(1,3)
  C=(1,141), D=(2,166)
```

The support-only scan gives exactly the same four quotient packets and no
extra unsigned matches; `D=0` never matches.  Raw validation confirms the four
survivors as `(47,28), +/-D -> theta2^-1` and `(28,141), +/-D -> theta2`.

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate.py
```

Consequence: the theorem target is rigid up to center inversion/orientation and
`D` reversal.  Future Robert/Siegel/Kubert-Lang claims must emit this specific
`C,D,K` packet, or an exactly equivalent theta2 payload; broad
anti-invariant/exponent-balanced packet families are not enough.

Completed D-slice weight-rigidity scan:

```text
fixed raw geometry:
  C = (47,28)
  K = (57,0)
  D = (22,3)
  offsets = -1,0,1

slice supports = 100,100,100
pairwise intersections = 0,0,0
union support = 300
```

Bounded audit over `{-2,-1,0,1,2}^3`:

```text
(-1,-1,-1) -> theta2,    recovered sign +1
( 1, 1, 1) -> theta2^-1, recovered sign -1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_gate.py
```

Consequence: the theorem target cannot be weakened to a weighted subproduct on
the accepted geometry.  The full equal-weight length-three `D` segment is
forced, up to global orientation.

Completed atomic weight-rigidity scan:

```text
fixed raw geometry:
  C = (47,28)
  K = (57,0)
  D = (22,3)
  atoms = C + jD + kK, j=-1,0,1; k=0..24

atom count = 75
support per atom = 4
pairwise intersecting atoms = 0
union support = 300
rank = 75
nullity = 0
```

Exact coefficient read-off gives:

```text
theta2^-1 target -> all 75 atom weights are +1
theta2 target    -> all 75 atom weights are -1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate.py
```

Consequence: no nonuniform `K` trace, missing-factor repair, or atomic-weight
null direction exists inside the accepted geometry.  A theorem hit must produce
the exact equal-weight K-traced anti-invariant product, or a genuinely
different accepted theta2 payload.

Completed anti-invariant producer-contract integration:

```text
compact theorem payload:
  C = (47,28)
  D = (22,3)
  K = (57,0), primitive trace
  orientation = forward or reverse

derived factor data:
  base = C-D   = (25,25)
  T    = -2C+K = (38,113)

quotient data:
  C      = (2,28)
  base   = (1,25)
  D      = (1,3)
  T=-2C  = (2,113)
  T/2=-C = (1,141)
```

The integration gate replays anti-invariant intake, selector rigidity, D-slice
weight rigidity, atomic weight rigidity, quotient factor intake, source packet
intake, and the raw-exponent-saturation non-selector check.

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate.py
```

Consequence: the current Robert/Siegel/Kubert-Lang/KSY moonshot target is an
exact theorem contract, not a pattern family.  Prove the challenge-legal
identity for the equal-weight K-traced anti-invariant normalized-y product, or
produce a genuinely different accepted theta2 payload.  First falsifiers:
raw KL exponent balance alone, missing/collapsed/nonprimitive `K`, truncated or
reweighted `D`, shifted center without matching orientation, nonuniform atom
weights, and q-cycle/source-coordinate confusion.

Completed anti-invariant source-boundary screen:

```text
continue:
  Sprang/Kronecker D=2 exact anti-invariant product
  exact Kubert-Lang equal-weight exponent matrix
  Koo-Shin-Yoon normalized-y/wp-prime exact product

conditional:
  Siegel-Robert value units with branch/root or period-156 fixedness data

kill:
  ordinary Kato theta_D direct proof
  literal Robert subgroup/coset support
  raw KL exponent balance alone
  nonuniform weighted product variants
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_gate.py
```

Consequence: the next proof/lit probe should instantiate a formula, not run a
broad reread.  Either instantiate a `D=2` Kronecker/KSY normalized-y formula or
an exact Kubert-Lang exponent matrix, then run the anti-invariant
producer-contract gate.

Completed Kubert-Lang graph row-law scan:

```text
C169 projection:
  positive cells = 25,28,31
  negative cells = 138,141,144

sign-affine row lifts scanned = 27
KL congruence laws            = 27
balanced laws                 = 21
D-segment/T-edge laws         = 9
fixed-T laws                  = 3
exact base/D/T laws           = 1
```

Unique accepted row law:

```text
slope = 1
positive_base_row = 1
negative_base_row = 0
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_graph_row_law_gate.py
```

Consequence: an exact Kubert-Lang/Siegel theorem must supply the sign-affine
row graph and base-row anchor.  The `C_169` projection plus KL congruences does
not select the p25 packet; even fixed `T` leaves three row translates, two of
which fail the source-packet contract.

Completed Kubert-Lang graph separability scan:

```text
target columns     = 25,28,31,138,141,144
target matrix rank = 3
row-only masks     = 7
row-only ranks     = rank 1: 7
source hits        = 0
```

Target row-by-C matrix:

```text
row 0: 0 0 1 -1 0 0
row 1: 1 0 0 0 -1 0
row 2: 0 1 0 0 0 -1
```

Positive remaining payload:

```text
row 0: c31 - c138
row 1: c25 - c141
row 2: c28 - c144
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_graph_separability_gate.py
```

Consequence: a row-only character, mask, or phase applied to the `C_169`
projection is rank-one and fails.  A theorem source must create the mixed
row-C graph, or directly emit the three row-labeled anti-invariant pairs.

Completed row-labeled pair contract gate:

```text
accepted payload:
  row 0: c31 - c138
  row 1: c25 - c141
  row 2: c28 - c144

support            = 6
coefficient counts = (-1,3),(1,3)
C-axis projection  = 1,1,1,-1,-1,-1
K-lift support     = 150
source contract    = pass
```

Rejected controls:

```text
wrong fixed-T row translates             fail
row-only C_169 projection shortcuts      fail
wrong pairings with same C-axis projection fail
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate.py
```

Candidate intake:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate.py \
  --packet PATH
```

Consequence: a targeted theorem/literature hit now has an executable landing
pad.  It must emit the exact row-labeled pair packet, or a stronger object that
reduces to it before the primitive-K source lift.

Completed row-pair permutation rigidity scan:

```text
row permutations scanned = 36
C-axis projection hits   = 36
KL congruence hits       = 36
balanced hits            = 36
D-segment/T-edge hits    = 9
fixed-T hits             = 3
source-contract hits     = 1
trace-correct hits       = 1
```

The fixed-`T` survivors are exactly:

```text
positive_by_row=(25,28,31), negative_by_row=(141,144,138) -> fail
positive_by_row=(28,31,25), negative_by_row=(144,138,141) -> fail
positive_by_row=(31,25,28), negative_by_row=(138,141,144) -> pass
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_gate.py
```

Consequence: one signed pair per row plus the correct C-axis projection is
still too weak.  A theorem source must recover the exact cyclic row translate
selected by the primitive-K source contract.

Completed reflection-anchor scan:

```text
fixed-T cyclic translates = 3
shared C-axis midpoint    = c28
reflection-anchor hits    = 1
source-contract hits      = 1
```

Fixed-`T` centers:

```text
positive_by_row=(25,28,31), negative_by_row=(141,144,138)
  center=(1,28), -2C=(1,113), source fail

positive_by_row=(28,31,25), negative_by_row=(144,138,141)
  center=(0,28), -2C=(0,113), source fail

positive_by_row=(31,25,28), negative_by_row=(138,141,144)
  center=(2,28), -2C=(2,113), source pass
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_anchor_gate.py
```

Consequence: the theorem-facing row anchor is `C=-T/2` in `C_3 x C_169`.
Explaining only the C-axis midpoint `c=28`, fixed `T`, or KL congruences is
not enough.

Completed reflection-center contract gate:

```text
accepted compact payload:
  C=(2,28)
  D=(1,3)
  primitive K

derived:
  base=C-D=(1,25)
  T=-2C=(2,113)
  T/2=-C=(1,141)
```

Controls:

```text
primitive K multiplier 2      pass
nonprimitive K multiplier 5   fail
wrong center row C=(0,28)     fail, derives T=(0,113)
wrong center row C=(1,28)     fail, derives T=(1,113)
wrong center c C=(2,29)       fail, derives T=(2,111)
wrong D=(1,4)                 fail
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate.py
```

Candidate intake:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate.py \
  --center-right-class 2 --center-c 28 --d-right-class 1 --d-c 3 \
  --k-multiplier 1
```

Consequence: the smallest quotient-level formula payload is now
`C,D,primitive K`; `base` and `T` are derived.  This is cleaner than asking a
theorem source to emit all six cells, but still strict enough to kill wrong row
anchors.

Completed raw reflection-gauge contract gate:

```text
accepted raw payload:
  C=(47,28)+aK
  D=+/-(22,3)+bK
  K primitive
  a,b mod 25

center kernel gauges              = 25
forward D kernel gauges           = 25
reversed D kernel gauges          = 25
oriented D gauges                 = 50
combined center/D oriented gauges = 1250
primitive K multipliers           = 20
raw parameter presentations       = 25000
```

Controls:

```text
primitive K multiplier 2                   pass
D reversal                                 pass
nonprimitive/collapsed K                   fail
center plus D / C-axis / right-axis shifts fail
D plus C-axis / right-axis shifts          fail
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_gate.py
```

Candidate intake:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 --k-multiplier 1
```

Consequence: formula sources may choose different raw representatives without
being false positives.  Kernel shifts of `C`, kernel shifts or reversal of
`D`, and primitive K generator changes are harmless; non-kernel shifts are not.

Completed raw reflection-orientation contract gate:

```text
C,  y(A)/y(-A) -> theta2 inverse
C,  y(-A)/y(A) -> theta2
-C, y(A)/y(-A) -> theta2
-C, y(-A)/y(A) -> theta2 inverse
```

Raw centers:

```text
C  = (47,28)
-C = (28,141)
```

Counts:

```text
presentations per branch       = 25000
theta2-inverse presentations   = 50000
theta2 presentations           = 50000
total accepted raw presentations = 100000
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate.py
```

Consequence: do not reject a formula hit merely because it emits theta2 rather
than theta2-inverse, or uses the inverse center with the opposite product
orientation.  It must land in one of the four oriented raw branches.

Completed raw orientation certificate-router gate:

```text
C,  y(A)/y(-A) -> theta2 inverse -> sign -1 -> -bridge
C,  y(-A)/y(A) -> theta2         -> sign +1 ->  bridge
-C, y(A)/y(-A) -> theta2         -> sign +1 ->  bridge
-C, y(-A)/y(A) -> theta2 inverse -> sign -1 -> -bridge
```

For all four routes:

```text
theta2 candidate harness      = pass
normalized bridge contract    = pass
support-resolvent term budget = 46800
support-resolvent union       = 11700
```

Controls:

```text
wrong center   -> emits neither theta2 nor theta2 inverse
wrong D        -> emits neither theta2 nor theta2 inverse
nonprimitive K -> emits neither theta2 nor theta2 inverse
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py
```

Consequence: a theorem/lit product hit now has a complete finite handoff:
raw oriented product, theta2/theta2-inverse classification, support-period
finite resolvent, normalized bridge contract.

Completed raw orientation value-route gate:

```text
support period                         = 156
bit length of 4^156 - 1                = 312
gcd(4^156 - 1, p - 1)                  = 1
gcd(4^156 - 1, p + 1)                  = 3
proper period shortcuts                = all fail

ambient period                         = 780
gcd(4^780 - 1, p - 1)                  = 11
ambient F_p branches                   = 11
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py
```

Consequence: divisor/additive product hits route through the current
certificate router.  Finite-field unit-value hits are viable only if they
provide period-156 theta2 fixedness/telescoping; otherwise the ambient value
route keeps the `mu_11` ambiguity.

Completed theorem-hit router gate:

```text
accepted output types:
  finite spine payload, with arithmetic-source debt
  raw divisor/additive product, routed through certificate path
  raw finite-field value product, only with period-156 theta2 context

rejected or not-yet-instantiated:
  ambient 780-period value only
  wrong raw center/D/nonprimitive K
  raw KL exponent balance only
  generic Robert/Siegel/KSY source-family claim
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py
```

Candidate smoke checks:

```text
raw-divisor C=(47,28), D=(22,3), K=1              -> accepted
raw-value same data with --period-156-context     -> accepted
raw-value same data without period-156 context    -> rejected
raw-divisor with center C=(47,29)                 -> rejected
ambient-value same raw data                       -> rejected
```

Consequence: future theorem/literature hits should be classified by output
type before falsification.  A divisor/additive identity, value identity, finite
payload, and broad source-family theorem have different obligations.

Completed primary-source exactness gate:

```text
continue:
  Sprang/Kronecker D-variant differential -> raw-divisor-or-additive
  Koo-Shin-Yoon normalized y              -> raw-value with period-156 context
  Kubert-Lang exact Siegel matrix         -> finite-spine verifier target

conditional:
  Siegel-Robert value units               -> raw-value with branch/period data

kill:
  ordinary Kato-Siegel theta_D direct D=2 proof
  generic Koo-Shin-Yoon ray-class generation
  raw KL exponent balance only
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_primary_source_exactness_gate.py
```

Consequence: the next theory move must instantiate an exact formula and then
route its actual output type.  Primary-source family membership alone no longer
counts as progress.

Completed KSY normalized-y Siegel formula gate:

```text
y(Q) = -g(2Q) / g(Q)^4

y(A)/y(-A) =
  g(2A)      coeff +1   support 75
  g(A)^-4    coeff -4   support 75
  g(-2A)^-1  coeff -1   support 75
  g(-A)^4    coeff +4   support 75
```

For `C=(47,28)`, `D=(22,3)`, primitive `K=(57,0)`, the four layers are
disjoint.  Their union has support `300`, coefficient counts
`(-4,75),(-1,75),(1,75),(4,75)`, matches the anti-invariant theta2-inverse
footprint, passes the KL exponent screen, and routes as raw divisor/additive
data to the theta2-inverse certificate path.  If emitted as finite-field
values, it still needs period-`156` theta2 context.

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate.py
```

Consequence: the KSY lane now has an exact four-layer Siegel payload.  Generic
ray-class generation or a single y-value is still insufficient; the remaining
debt is theorem legality for this exact product or period-156 context for value
output.

Completed KSY-y period-context gate:

```text
exact KSY-y footprint support period = 156
[2]^156 fixes formula payload         = true
proper period divisors fail           = true
gcd(4^156 - 1, p - 1)                 = 1
ambient F_p value branches            = 11
compact telescoping witness budget    = 975
factor-period witness budget          = 31
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate.py
```

Consequence: the value-route obligation for the exact KSY-y formula is now
executable.  A value theorem must carry this period-156 context; otherwise it
falls back to the ambient `mu_11` ambiguity.

Completed KSY-y theorem-legality boundary:

```text
accepted complete routes:
  exact KSY-y divisor/additive identity
  exact KSY-y value identity with period-156 context

conditional:
  exact value identity without period context
  finite spine payload without arithmetic source
  CM/Lang field generation without exact finite-field identity

rejected:
  ambient 780-period value only
  wrong C/D/K geometry or orientation
  generic KSY ray-class generation
  raw Kubert-Lang exponent balance only
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_gate.py
```

Consequence: the moonshot is narrowly viable.  The finite payload and branch
context are executable; the missing object is a challenge-legal arithmetic
theorem for this exact product.

Completed KSY-y closure-theorem template:

```text
formal product:
  P = prod_{j=-1..1} prod_{k=0..24}
      y(C+jD+kK) / y(-C-jD-kK)
  C=(47,28), D=(22,3), K=(57,0)
  y(Q)=-g(2Q)/g(Q)^4

closing theorem shapes:
  exact divisor/additive identity for P
  exact value identity for P with period-156 context

non-closing shadows:
  exact value without period context
  finite spine without arithmetic source
  generic class-field or KSY generation
  ambient 780-period values or KL exponent hygiene alone
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py
```

Consequence: the first-class source question is now exact enough to hand to
literature scouts or Drew.  The finite side is sub-sqrt and executable; the
open item is a source theorem matching one of the two closing shapes.

Completed KSY-y primary-source clause audit:

```text
closing source rows     = 0
conditional source rows = 4
rejected source rows    = 1

KSY:
  missing exact C/D/K product identity for P
Siegel-Robert:
  missing period-156 branch/root/telescoping data
Sprang/Kronecker:
  missing D=2 differential/additive identity for exact P
Kubert-Lang:
  missing mixed C_75 x C_169 graph selector
ordinary field generation / ambient values:
  rejected unless reframed as a closure-template theorem
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_gate.py
```

Consequence: source relevance no longer counts as progress by itself.  A live
hit must supply one named missing clause from the audit.

Completed KSY-y primary-source anchor packet:

```text
conditional anchors:
  KSY Theorem 5.3 / ray-class generation
  KSY normalized-y / Siegel formula
  Siegel-Robert value units
  Sprang Proposition 5.4 / Kato-Siegel dlog
  Kubert-Lang Siegel functions are generators

policy anchor:
  DANGER3 finite-field identity / no-CM boundary

rejected:
  generic field generation / ambient value shadows
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_gate.py
```

Consequence: a source/lit hit must name one anchor row and supply its missing
closure-template clause before it counts as moonshot progress.

Completed KSY-y period-value upgrade gate:

```text
denominators:
  support period                 = 156
  gcd(4^156 - 1, p - 1)          = 1
  ambient period                 = 780
  gcd(4^780 - 1, p - 1)          = 11
  ambient F_p value branches     = 11

upgrade rows:
  closing value shapes           = 2
  conditional value shapes       = 3
  rejected value shadows         = 2
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py
```

Consequence: period-156 context is necessary for value-route hits, but it is
not sufficient by itself.  A closing value theorem must also emit exact `P`,
preserve the mixed graph, and prove a finite-field identity.  Ambient `780`
values and generic KSY ray-class generation remain rejected.

Completed KSY-y exact-product intake:

```text
regression counts:
  closing product claims     = 3
  conditional product claims = 3
  rejected product claims    = 4

closing:
  KSY exact divisor/additive identity for P
  Sprang/Kronecker D=2 exact additive identity for P
  Kubert-Lang exact mixed product identity for P

conditional:
  formula language without product proof
  finite theta2 verifier payload without source theorem
  exact product with DANGER3 policy/framing unknown

rejected:
  generic ray-class generation
  literal subgroup support
  KL exponent hygiene alone
  nonuniform weighted product variants
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py
```

Consequence: the divisor/additive route is now a separate executable target
from the value route.  It closes only when a source emits exact `P`, the mixed
graph, equal atom weights, orientation, finite intake geometry, arithmetic
producer status, and DANGER3-legal framing.

Completed KSY-y source-claim intake:

```text
regression counts:
  closing claims     = 2
  conditional claims = 1
  policy-only claims = 1
  rejected claims    = 3

closing:
  exact divisor/additive identity for P
  exact value identity for P with period-156 context

non-closing:
  exact value without period-156 context
  DANGER3 policy acceptance without a theorem
  generic field generation
  Kubert-Lang exponent hygiene alone
  unnamed relevant source
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py
```

Consequence: incoming theorem snippets or Drew answers now have an executable
router.  Policy yes helps, but only a closure-template theorem closes the
moonshot route.

Completed KSY-y DANGER3 framing gate:

```text
official surface:
  p                                = 10000000000000000000000013
  DANGER3 remote HEAD checked       = a65658b7b194546957fa62f40d60ca63efc37f93
  final submission surface          = concrete (p,A,x0) triple verified by vpp.py / lean_vpp.py
  README no-CM ban observed         = true

regression counts:
  submission-ready verified triples = 1
  policy-unblocked theorem routes   = 2
  policy-only rows                  = 1
  conditional rows                  = 2
  rejected rows                     = 2
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate.py
```

Consequence: Drew/DANGER3 policy acceptance is useful, but it is not by
itself a certificate.  A finite-field identity for exact `P` would unblock the
theorem route only if accepted as challenge-legal framing, and the route still
has to derive a concrete `(p,A,x0)` and pass official `vpp.py`.  Generic CM or
Lang provenance without a finite-field identity remains rejected.

Completed KSY-y source-parameter hygiene gate:

```text
safe notational rows:
  KSY [2] in y(Q)=-g(2Q)/g(Q)^4
  raw D=(22,3), quotient D=(1,3)

conditional source rows:
  Sprang/Kronecker even-D differential/additive route
  Kubert-Lang C169 prime-power projection
  Kubert-Lang mixed levels 507/12675

rejected misread:
  ordinary Kato-Siegel Dtheta with D=2

counts:
  safe_notational_rows    = 2
  conditional_source_rows = 3
  rejected_misread_rows   = 1
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate.py
```

Consequence: the source ask is now notation-safe.  KSY's `[2]` remains a live
normalized-y formula operator, and raw `D` remains finite p25 geometry, but
neither imports the ordinary Kato-Siegel `Dtheta` theorem at `D=2`.  A
Sprang/Kronecker hit must explicitly supply an even-`D` identity for exact
`P`.  A Kubert-Lang hit must preserve the mixed row graph; C169 congruence
hygiene is only a screen.

Completed KSY-y mixed-graph obligation gate:

```text
accepted finite graph shapes:
  exact row-labeled pairs
    row 0: c31 - c138
    row 1: c25 - c141
    row 2: c28 - c144

  quotient reflection center
    C = (2,28)
    D = (1,3)
    base = C-D = (1,25)
    T = -2C = (2,113)

  raw equal-weight product
    raw C = (47,28) up to K-gauge
    raw D = +/-(22,3) up to K-gauge
    K primitive, orientation recorded

rejected or conditional:
  C169 projection alone                         rejected
  KL exponent/congruence hygiene alone          rejected
  one signed pair per row with wrong pairing    rejected
  fixed-T cyclic translate without base anchor  conditional

regression counts:
  finite_obligation_rows  = 4
  arithmetic_closing_rows = 1
  conditional_rows        = 1
  rejected_rows           = 3
```

Local audit gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py
```

Candidate mode was smoke-tested on three source-claim shapes:

```text
C169-only claim:
  decision = reject_c169_or_kl_screen_without_mixed_graph
  expected exit = 1

reflection-center claim:
  decision = finite_mixed_graph_met_by_reflection_center
  expected exit = 0

raw product theorem claim:
  decision = closing_raw_product_with_arithmetic_producer
  expected exit = 0
```

Consequence: the `C_3 x C_169` graph is now nonoptional.  A theorem hit may
arrive as exact row-labeled pairs, reflection-center data, or the stronger raw
K-traced product.  The raw product plus an arithmetic producer theorem is the
closing source shape; anything weaker is finite payload evidence only.

Completed KSY-y submission-extraction gate:

```text
dependency gates:
  universal finite intake      = pass
  arithmetic producer contract = pass
  DANGER3 framing              = pass

vpp regression:
  known p24 triple             = True
  p24 x0+1 control             = rejected

regression rows:
  finite payload only
  source theorem without policy/extraction
  policy-unblocked theorem without extraction
  extraction algorithm without output
  concrete triple failing vpp.py
  verified concrete triple

counts:
  finite_live_rows             = 5
  source_closed_rows           = 4
  submission_ready_rows        = 1
  conditional_rows             = 4
  rejected_rows                = 1
```

Local audit gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py
```

Concrete triple candidate mode:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py \
  --p P --A A --x0 X0
```

Consequence: the moonshot now has a clean final handoff.  Finite payload
acceptance, source theorem closure, policy unblocking, extraction, and
submission are distinct.  Anything before a concrete `vpp.py`-verified triple
is progress, not a p25 submission.

Completed KSY-y closing-theorem obligation gate:

```text
minimal theorem contract:
  P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
  C = (47,28), D = (22,3), K = (57,0)
  y(Q) = -g(2Q)/g(Q)^4
  quotient anchor: C=(2,28), D=(1,3), T=-2C=(2,113), T/2=-C=(1,141)

required source-theorem clauses:
  exact P
  mixed C_3 x C_169 row graph or reflection-center payload
  equal weights on all 75 K-traced atoms
  orientation branch
  challenge-legal arithmetic source theorem
  divisor/additive product identity, or period-156 finite-field value identity

counts:
  source_theorem_closed_rows = 4
  danger3_unblocked_rows     = 3
  extraction_ready_rows      = 2
  submission_ready_rows      = 1
  conditional_rows           = 5
  rejected_rows              = 2
```

Local audit gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py
```

Candidate-mode examples:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name c169_projection --source-family Kubert-Lang \
  --exact-p --equal-weight --orientation --output-kind divisor-additive

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name full_theorem_ready --source-family KSY-KL \
  --exact-p --mixed-graph --equal-weight --orientation --arithmetic-source \
  --output-kind divisor-additive --finite-identity --danger3-framing --extraction

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name verified_triple_state --source-family DANGER3 \
  --exact-p --mixed-graph --equal-weight --orientation --arithmetic-source \
  --output-kind divisor-additive --finite-identity --danger3-framing \
  --extraction --vpp-verified-triple
```

Markers:

```text
robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_candidate_rows=1/1
```

Consequence: the KSY-y route is now theorem-bottlenecked in one exact place.
Finite verifier payloads, `C169` projection, KL congruence hygiene, generic
KSY field generation, and unextracted exact identities are still useful
diagnostics, but they no longer count as closure.  The next meaningful positive
artifact is an exact source theorem for this `P`, followed by DANGER3 framing,
`(A,x0)` extraction, and official `vpp.py` verification.

Completed KSY-y primary-source scout packet:

```text
source-gated jobs:
  ksy_normalized_y_exact_p
  kubert_lang_mixed_graph_product
  sprang_kronecker_d2_additive
  siegel_robert_period_value
  danger3_framing_extraction

counts:
  contract_rows                  = 5
  exact_product_contracts        = 4
  value_contracts                = 2
  policy_or_extraction_contracts = 1
```

Source handles checked:

```text
Koo-Shin-Yoon arXiv:1007.2307
Sprang arXiv:1801.05677
Kubert-Lang EUDML doc 162977 / Modular Units
Schertz EUDML doc 248002 and Shin arXiv:1009.2253
AndrewVSutherland/DANGER3
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_primary_source_scout_packet_gate.py
```

Marker:

```text
ksy_y_primary_source_scout_packet_rows=1/1
```

Consequence: subagents or fresh agents should not perform broad literature
surveys.  Each scout must inspect one named source handle, report exact
theorem/lemma/equation numbers, match or miss the closing clauses, run or name
the local classifier, and recommend continue/kill.

Completed KSY exact-P primary-source scout:

```text
source:
  Koo-Shin-Yoon, arXiv:1007.2307

observations:
  Equation (3.4) normalized y/Siegel formula
    decision = conditional_missing_exact_product

  Theorem 5.3 ray-class generation
    decision = reject_not_closure_theorem

  Corollary 6.4 single-y-value generator
    decision = conditional_missing_exact_product

  hypothetical exact-P value without period
    decision = conditional_missing_period_156_context

  hypothetical exact-P divisor/additive identity
    decision = closing_divisor_or_additive_identity

counts:
  formula_language_rows     = 1
  direct_closing_rows       = 0
  conditional_rows          = 3
  rejected_rows             = 1
  hypothetical_closing_rows = 1
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ksy_exact_p_primary_source_scout_gate.py
```

Candidate probe matching Theorem 5.3:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name ksy_theorem_5_3_generation_only \
  --anchor ksy_theorem_5_3_ray_class_generation \
  --output-kind field-generation
```

Marker:

```text
ksy_y_ksy_exact_p_primary_source_scout_rows=1/1
```

Consequence: KSY remains useful as normalized-y formula vocabulary and possible
future product/distribution source, but Theorem `5.3` and Corollary `6.4` are
killed as direct p25 closing theorems.

Completed Kubert-Lang mixed-graph primary-source scout:

```text
source:
  Kubert-Lang, EuDML doc 162977 / GDZ LOG_0038

verified handle:
  Math. Ann. 227 (1977), 223-242
  GDZ article PDF: https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0227/LOG_0038.pdf

observations:
  generator theorem / Siegel-function framework
    source decision = reject_exponent_hygiene_only
    mixed decision  = reject_c169_or_kl_screen_without_mixed_graph

  C169 projection / KL congruence screen
    mixed decision = reject_c169_or_kl_screen_without_mixed_graph

  fixed-T without base anchor
    mixed decision = conditional_fixed_t_without_base_row_anchor

  exact row-labeled pairs hypothetical
    mixed decision = finite_mixed_graph_met_by_row_labeled_pairs

  raw product plus arithmetic producer hypothetical
    source decision = closing_divisor_or_additive_identity
    mixed decision  = closing_raw_product_with_arithmetic_producer

counts:
  generator_language_rows   = 1
  direct_closing_rows       = 0
  finite_payload_rows       = 1
  conditional_rows          = 1
  rejected_rows             = 2
  hypothetical_closing_rows = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_mixed_graph_primary_source_scout_gate.py
```

Candidate probes:

```text
kl77_generator_theorem_handle -> reject_exponent_hygiene_only
kl77_c169_projection_screen -> reject_c169_or_kl_screen_without_mixed_graph
kl77_exact_row_labeled_pairs_hypothetical -> finite_mixed_graph_met_by_row_labeled_pairs
```

Marker:

```text
ksy_y_kubert_lang_mixed_graph_primary_source_scout_rows=1/1
```

Consequence: Kubert-Lang remains useful as the modular-unit language for the
right source family, but direct closure now requires exact mixed row labels,
the reflection-center payload, or the raw equal-weight K-traced product with an
arithmetic producer.  Generator theorem language, exponent hygiene, and C169
projection alone are killed as direct closers.

Completed Sprang/Kronecker D=2 primary-source scout:

```text
source:
  Sprang, arXiv:1801.05677

observations:
  even-D Kronecker-section route
    parameter decision = conditional_needs_even_D_kronecker_clause
    product decision   = conditional_formula_language_without_product_proof

  Corollary 5.7 omega_D construction
    parameter decision = conditional_needs_even_D_kronecker_clause
    product decision   = conditional_missing_exact_product

  Appendix A distribution relation
    product decision = conditional_missing_exact_product

  ordinary Kato-Siegel theta_D at D=2
    parameter decision = reject_ordinary_kato_theta_2_prime_to_6_violation

  exact-P additive identity hypothetical
    product decision = closing_exact_product_identity

counts:
  even_d_live_rows          = 2
  direct_closing_rows       = 0
  conditional_rows          = 3
  rejected_rows             = 1
  hypothetical_closing_rows = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate.py
```

Candidate probes:

```text
sprang_even_d_kronecker_section -> conditional_formula_language_without_product_proof
sprang_exact_p_additive_identity_hypothetical -> closing_exact_product_identity
```

Marker:

```text
ksy_y_sprang_kronecker_d2_primary_source_scout_rows=1/1
```

Consequence: Sprang remains a serious live route, but only if the source hit
instantiates an even-`D` differential/additive identity for exact `P`, exact
theta2/theta2-inverse divisor data, or the compact KSY theorem payload.  Generic
Kronecker-section, dlog, or distribution language is not enough.

Completed Siegel-Robert period-value primary-source scout:

```text
sources:
  Schertz, EuDML doc 248002 / Numdam JTNB 9 (1997), 383-394
  Shin, arXiv:1009.2253

observations:
  Schertz Klein-form quotient / elliptic-unit generator
    value decision  = reject_field_generation_not_value_theorem
    source decision = reject_not_closure_theorem

  Shin Siegel-Ramachandra generator
    value decision  = reject_field_generation_not_value_theorem
    source decision = reject_not_closure_theorem

  bare exact Siegel-Robert value
    value decision  = conditional_missing_period_156_context
    source decision = conditional_missing_period_156_context

  ambient period-780 value
    value decision  = reject_ambient_780_mu11_branch
    source decision = reject_not_closure_theorem

  exact value with period-156 context hypothetical
    value decision  = closing_value_identity_with_period_156
    source decision = closing_value_identity_with_period_156

denominators:
  support period = 156
  gcd(4^156 - 1, p - 1) = 1
  ambient period = 780
  gcd(4^780 - 1, p - 1) = 11

counts:
  direct_closing_rows       = 0
  conditional_rows          = 1
  rejected_rows             = 3
  hypothetical_closing_rows = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_siegel_robert_period_value_primary_source_scout_gate.py
```

Marker:

```text
ksy_y_siegel_robert_period_value_primary_source_scout_rows=1/1
```

Consequence: the Siegel-Robert/Siegel-Ramachandra lane is still viable only as
a value theorem for exact `P` with mixed graph and period-`156` context.
Class-field generation, generic invariant language, and ambient period-`780`
values are killed as direct closers.

Completed DANGER3 framing/extraction primary-source scout:

```text
source:
  AndrewVSutherland/DANGER3

remote:
  HEAD = a65658b7b194546957fa62f40d60ca63efc37f93

local source surface:
  src/vpp.py available locally       = true
  src/lean_vpp.py available locally  = false
  official lean_vpp.py observed      = true

observations:
  official DANGER3 submission surface
    missing = concrete p25 (A,x0) passing official vpp.py

  finite identity theorem, policy unknown
    submission decision = source_theorem_but_policy_or_extraction_missing
    framing decision    = conditional_policy_or_framing_missing

  policy-unblocked theorem, no extraction
    submission decision = policy_unblocked_but_extraction_missing
    framing decision    = policy_unblocked_theorem_route_not_submission

  extraction algorithm without output
    submission decision = extraction_algorithm_needs_concrete_vpp_output

  policy yes only
    framing decision = policy_only_not_theorem

  generic CM/Lang generation
    framing decision = reject_cm_provenance_without_finite_identity

  claimed triple failing vpp
    submission decision = reject_concrete_triple_fails_vpp
    framing decision    = reject_unverified_triple

  verified p25 triple hypothetical
    submission decision = closing_vpp_verified_submission
    framing decision    = closing_verified_pomerance_triple

counts:
  direct_submission_rows       = 0
  conditional_rows             = 3
  policy_only_rows             = 1
  rejected_rows                = 2
  hypothetical_submission_rows = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_framing_extraction_primary_source_scout_gate.py
```

Marker:

```text
ksy_y_danger3_framing_extraction_primary_source_scout_rows=1/1
```

Consequence: the full five-job primary-source scout packet is now artifacted.
The moonshot has one remaining theorem-side target and one challenge-side
target: produce exact `P` / exact theta2 / exact period-value data, then derive
or submit a concrete `(A,x0)` that passes official `vpp.py`.

Post-scout reduction:

```text
ranked targets:
  1. Sprang/KSY exact theta2-or-P divisor/additive identity
  2. Kubert-Lang raw mixed product with arithmetic producer
  3. Siegel-Robert exact P value with period-156 context
  4. DANGER3 policy/extraction only after theorem hit or Drew answer
  5. broad class-field/generator shadows killed as direct closers

counts:
  active_theorem_targets           = 3
  challenge_targets                = 1
  killed_shadow_targets            = 1
  direct_source_closing_rows       = 0
  hypothetical_source_closing_rows = 4
  hypothetical_submission_rows     = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_scout_moonshot_reduction_gate.py
```

Marker:

```text
ksy_y_post_scout_moonshot_reduction_rows=1/1
```

Priority-1 exact divisor checkpoint:

```text
conversion clauses:
  Sprang/Kronecker D=2 exact additive identity -> closing_exact_product_identity
  KSY normalized-y exact product/distribution identity -> closing_exact_product_identity

non-closers:
  compact finite payload only
  KSY Equation (3.4) formula language only
  Sprang distribution/dlog language without exact P specialization

killed:
  KSY single-y or ray-class generation
  ordinary Kato theta_D at D=2
  nonuniform/partial products
  missing/collapsed K trace
  wrong D or wrong T

counts:
  direct_source_closing_rows = 0
  theorem_hit_hypotheticals  = 2
  conditional_rows           = 2
  finite_only_rows           = 1
  rejected_rows              = 5
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_exact_divisor_lane_gate.py
```

Marker:

```text
ksy_y_priority1_exact_divisor_lane_rows=1/1
```

Priority-1 Sprang source split:

```text
arXiv:1801.05677:
  title  = Eisenstein-Kronecker series via the Poincare bundle
  role   = Kronecker-section / Eisenstein-Kronecker construction surface
  status = conditional_formula_language_without_product_proof

arXiv:1802.04996:
  title  = The algebraic de Rham realization of the elliptic polylogarithm via the Poincare bundle
  role   = algebraic de Rham polylogarithm / differential-form surface
  status = conditional_formula_language_without_product_proof

ordinary Kato theta_D at D=2:
  status = reject_ordinary_kato_theta_2_prime_to_6_violation

exact D=2 p25 product identity:
  status = closing_exact_product_identity

counts:
  conditional_source_handles = 2
  rejected_imports           = 1
  closing_hypotheticals      = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_sprang_source_split_gate.py
```

Marker:

```text
ksy_y_priority1_sprang_source_split_rows=1/1
```

Priority-1 KSY source split:

```text
Equation (3.4):
  role   = normalized-y/Siegel formula language y(Q)=-g(2Q)/g(Q)^4
  status = conditional_formula_language_without_product_proof

Theorem 5.3:
  role   = ray-class generation by torsion data
  status = reject_field_generation_not_product_identity

Theorem 6.2 / Corollary 6.4:
  role   = single normalized-y value / ray-class invariant statement
  status = conditional_missing_exact_product

exact K-traced normalized-y product/distribution theorem:
  status = closing_exact_product_identity

counts:
  formula_language_rows         = 1
  generation_rejected_rows      = 1
  single_value_conditional_rows = 1
  closing_hypotheticals         = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_ksy_source_split_gate.py
```

Marker:

```text
ksy_y_priority1_ksy_source_split_rows=1/1
```

Priority-1 theorem query packet:

```text
closing queries:
  Sprang arXiv:1801.05677 exact Kronecker/distribution product
  Sprang arXiv:1802.04996 exact de Rham differential product
  KSY arXiv:1007.2307 Equation (3.4) exact K-traced normalized-y product

non-closing rows:
  KSY Theorem 5.3 generation shadow -> reject_field_generation_not_product_identity
  KSY Theorem 6.2 / Corollary 6.4 single-y value -> conditional_missing_exact_product

counts:
  source_query_rows    = 5
  closing_query_rows   = 3
  context_only_rows    = 1
  rejected_shadow_rows = 1
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_theorem_query_packet_gate.py
```

Marker:

```text
ksy_y_priority1_theorem_query_packet_rows=1/1
```

Completed theta2 resolvent-normalization gate:

```text
additive/divisor normalization:
  denominator bit length = 1560
  denominator nonzero mod p25    = true
  denominator nonzero mod 126751 = true
  denominator nonzero mod 2029   = true
  exact integer division recovers bridge
  additive scaling mod p25/126751/2029 recovers bridge
  weighted exponent bit budget = 182520000 < sqrt(p)

multiplicative-unit normalization:
  gcd(4^780 - 1, p25 - 1)    = 11
  gcd(4^780 - 1, p25 + 1)    = 3
  gcd(4^780 - 1, 126751 - 1) = 12675
  gcd(4^780 - 1, 2029 - 1)   = 507
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_resolvent_normalization_gate.py
```

Consequence: a theorem hit should be classified by output type.  If it emits a
divisor/additive coefficient object, the resolvent normalization is legitimate.
If it emits only multiplicative unit values, it must also provide the
`4^780-1` root/branch selection; exponent inversion is not available for free.

Completed theta2 root-ambiguity gate:

```text
value-level kernel:
  gcd(4^780 - 1, p25 - 1) = 11
  F_p has 11 distinct mu_11 branches killed by the denominator power

divisor-level footprint:
  scalar divisor support        = 0
  distinct branch divisor masks = 1
  bridge contract still passes  = true
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_root_ambiguity_gate.py
```

Consequence: the `mu_11` ambiguity is harmless if the theorem emits a
divisor-level theta2 object, because global scalar branches do not change the
bridge source mask.  It remains real if the theorem emits only normalized
finite-field unit values; the finite bridge contract cannot choose the branch.

Completed theta2 sparse candidate harness:

```text
accepted theorem output:
  right_log c_log coefficient triples on C_75 x C_169
  exact theta2 or theta2^-1 divisor footprint

positive controls:
  theta2 support         = 300
  theta2^-1 support      = 300
  coefficient counts     = (-4,75), (-1,75), (1,75), (4,75)
  resolvent(theta2)      = bridge
  resolvent(theta2^-1)   = -bridge
  shifted union support  = 11700
  shifted term budget    = 46800

negative control:
  plain 150-term bridge is not accepted as theta2
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_candidate_harness.py
```

Theorem-output intake:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_candidate_harness.py \
  --sparse-source PATH
```

Consequence: future Robert/Kato-Siegel work can aim for exact theta2 divisor
triples instead of the final bridge triples.  The finite deconvolution and
bridge audit are now executable.

Completed theta2 compact parameter harness:

```text
accepted compact recipe:
  center_base = (44,166) = base + H
  half_shift  = (56,28)  = -H
  H           = (19,141), 2H = T
  T           = (38,113)

orientations:
  no inversion -> theta2^-1 -> resolvent gives -bridge
  --invert     -> theta2    -> resolvent gives bridge

controls rejected:
  wrong half orientation
  full bridge edge used as half shift
  half edge without center shift
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_compact_harness.py
```

Compact candidate intake:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_compact_harness.py \
  --center-right 44 --center-c 166 --half-right 56 --half-c 28
```

Consequence: future Robert/Kato-Siegel work can aim at the compact
center/half-edge/orientation data.  The local harness expands it to theta2,
applies the resolvent, and audits the final bridge.

CM/Lang transfer lit-scout synthesis:

The literal `K=Q(sqrt(-42))` selected-CM route fails its first p25 arithmetic
selector.  Independent Cornacchia check for `p = x^2 + 42y^2` gives no
solution: the sqrt-minus-42 root exists, but the Euclidean stop is
`x=1588702171268` with `(p-x^2) mod 42 = 19`.  Thus `d=42` has no principal
trace selector over `F_p` for this p.

Consequence: CM/Ray-class material is demoted to checksum/scaffolding unless
the challenge accepts a symmetric full-orbit trace identity.  Weber/eta,
Lang-Schertz/Siegel-Ramachandra, Hasse-Weber, singular-moduli trace, and
isogeny-transfer routes all still face either selected-root ambiguity or a
full-orbit trace that does not emit a finite-field certificate payload.

Fixed-frequency/Jacobi lit-scout synthesis:

The fixed-`k=42` Jacobi lane is now mostly diagnostic.  Verified p25 arithmetic:

```text
sqrt_floor = 3162277660168
p mod 42 = 23
ord_42(p) = 6
gcd(42,p-1) = 2
gcd(42,p+1) = 6
ord_150(p) = 20
max modulus with Carmichael exponent dividing 42 = 151704
floor(p^(1/3)) = 215443469
```

The theorem shapes found by the scout are real but not payload-compressing:
van Wamelen gives a fixed 42-coefficient Jacobi-sum determination over
`F_{p^6}`; Davenport-Hasse diagnoses lower order-6 and order-14 factors but
does not assemble full order `42`; Gross-Koblitz/Stickelberger gives
valuation/ideal data without the unit payload; period/cyclotomic matrices keep
large native value scale; and APRCL/Cohen-Lenstra style fixed-42 quotients do
not reach even the `p^(1/3)` threshold.

Consequence: keep Jacobi/Gauss-period work only as a fixed-dimension oracle,
sign/ideal diagnostic, or verifier-side checksum unless a new external symmetry
produces a genuine small quotient payload.

Sparse-source intake:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py \
  --sparse-source PATH
```

Consequence: a Robert/Siegel or modular-unit hit can return only nonzero
`right_log c_log coefficient` triples.  The local harness will coalesce them in
`C_75 x C_169`, CRT-convert to raw `C_12675`, and apply the bridge candidate
contract.

Completed Kato/Robert subgroup-support falsifier:

```text
visible D=(1,3) has order 507, not 3
3D=(0,9), not 0
raw D=(22,3) has order 12675
raw K_trace*D_segment has C-support (25,28,31)
any raw subgroup of order 75 has trivial C-projection
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_kato_subgroup_support_falsifier_gate.py
```

Consequence: the literal `rho_H(P+T)/rho_H(P-T)` finite-subgroup divisor is
killed as a complete producer.  Continue only if the quotient supplies a
weighted or non-subgroup `D_segment`, such as a `y`, `wp'`, Siegel/Klein,
differential, or finite-difference quotient.
