# p24 Strict DANGER3 Frontier

Date: 2026-06-04 PDT

Target:

```text
p = 10^24 + 7
k = 40
2^k = 1099511627776
sqrt_floor(p) = 1000000000000
```

There are now two broad, fast certificates for this prime:

```text
p24/pocklington_p24.py
p24/near_square_ecpp_certificate.py
```

Those certify primality / a broad elliptic Pomerance-style condition with
polylog or small-CM work.  They do not satisfy the strict DANGER3 verifier,
which requires a Montgomery `A` and x-coordinate of exact x-only order `2^40`.

## Strict Trace Target

The verifier can only accept curves or twists with signed trace in:

```text
-1178414874616
-1020608380936
-78903246840
 78903246840
 1020608380936
 1178414874616
```

On the curve side this is the Hasse lift of:

```text
t == p + 1 mod 2^40
```

so the hard part is not finding a large point after a curve is known.  It is
constructing or sampling a curve in one of these trace classes without paying
the `sqrt(p)` trace entropy.

The post-trace audit confirms this separation at small exact scale: after a
target-trace `A` is known, group projection finds an accepted `x0` in constant
expected trials, while target-trace `A` counts remain `Theta(sqrt(p))`.

## Broad Certificates Already Found

Pocklington:

```text
p - 1 = 2 * 7 * 29 * 2463054187192118226601
2463054187192118226601 > sqrt(p)
```

The recursive certificate in `p24/pocklington_p24_certificate.json` verifies.

Near-square ECPP:

```text
p = (10^12)^2 + 7
D = -7
j = -3375
trace = 2000000000000
order = 2^3 * 7 * 250698247 * 71229627932369
71229627932369 > sqrt(p)
```

This gives a cheap elliptic certificate, and it can be converted to Montgomery
form, but both the curve and twist have only `v2 = 3`; no DANGER3 bridge.
Low-degree correspondence audit: isogenies preserve this trace, twists only
give `+/-2n` for `j=-3375`, and bounded-degree non-isogenous recipes only
change the target-class entropy by constants.

## Public Lead Scan

The public/local sidecar

```text
p24/public_lead_scan_20260604.md
```

found no posted strict p24 triple or asymptotic construction.  The official
DANGER3 README still lists the p22 and p23 successes and then asks for
`p = 10^24 + 7`; the public Alexa and Ruehle forks only record the already
incorporated constant-factor / sqrt-scale approaches.  Exact web hits for
`1000000000000000000000007` outside the challenge context were primality or
sequence references, not verifier-compatible certificates.

## Strict Routes Closed So Far

CM exact trace:

```text
target fundamental discriminants have class-size estimates 2.06e11 to 8.33e11
exact PARI class groups:
  trace 1020608380936 has cyclic class group of order `2*19*7335098083`
  trace -78903246840 has invariants `[2*104129401043,2,2]`
  trace -1178414874616 has cyclic class group of order
    `2*157*211*3107441`
for the third trace, small split-prime class actions are favorable:
  prime `23` generates the full class group; primes `2897` and `14057`
  generate subgroups of index `157` and `211`; this supports a possible
  odd class-field tower description but still does not supply the seed/root
decomposed CM tradeoff: the third target admits the attractive split
  `h=66254*3107441`, so embedded decomposed equations would leave only
  degree-`3107441` root-finding over F_p; known methods still spend
  sqrt-scale CRT/class-orbit work constructing those embedded equations, and
  abstract class-field equations do not map back to `j`
odd-level invariant degree audit: levels `23,157,211,2897,14057,3107441`
  all have X0 recovery degree far below sqrt(p), but using them requires an
  embedded modular relation or a seed target vertex; class factorization alone
  provides neither
embedded decomposition calibration: small model `D=-5000`, `h=30`, `q=1259`
  decomposes a degree-30 CM root problem into degree 6 plus degree 5, but only
  after computing a seed root and the embedded `j`-root isogeny cycle; this
  demonstrates exactly what the p24 smooth-class lead is missing
seedless 23-cycle / quotient-cycle audit: the small split prime `23` generates
  the cyclic class group, but imposing this without a seed means an
  `X0(23^h)`-type fixed-point condition with
  `log10(degree) ~= 2.803531e11`; the observed quotient subgroup cycles via
  primes `2897`, `14057`, `677`, and `7349` still have log-degrees around
  `1.86e9` to `4.54e9`, and even a hypothetical prime-level generator for
  the order-`3107441` subgroup has `log10(degree) >= 9.35433e5`.  Thus the
  attractive `66254*3107441` decomposed-CM split only helps after embedded
  orbit sums / quotient invariants / a seed root are already available.
class-invariant stabilizer audit: fixed/low-level Weber/Atkin/eta/X0
  invariants have stabilizers bounded by their modular/ray symmetries and the
  map degree back to `j`, not by arbitrary large odd subgroups of the Hilbert
  class group.  Locally, `D=-5000,h=30` shows a generator-level `X0(3)` edge
  invariant has 30 distinct edge sums/products; the degree-6 quotient only
  appears after explicit embedded coset sums.  Thus no free stabilizer of size
  `3107441` or `66254` has been identified for the smooth p24 lead.
Atkin-Lehner / Fricke quotient limit audit: full `X0(N)/W_N` quotient saves
  only `2^omega(N)`.  For relevant odd levels, this changes constants and can
  put a huge fixed-instance level such as `157*211*3107441` at quotient degree
  `13010859654 < sqrt(p)`, but it is still proportional to the class scale and
  is not the desired smooth class-subgroup stabilizer (`3107441` or `66254`).
  The missing ingredient remains an embedded quotient invariant and recovery
  map, not a normalizer symmetry.
smooth-class asymptotic caveat: this is a fixed-instance structural lead, not
  an asymptotic speedup unless one can also force smooth target class groups
  and build embedded quotient invariants/recovery maps in sub-sqrt work
smooth quotient-invariant refresh: Sutherland-style decomposed/tower CM can
  use `h = m*n` to reduce final root degrees, but it constructs embedded
  fixed-field and recovery polynomials by enumerating `G`-orbits of CM roots.
  Directly modulo p24 this needs a seed target root; via CRT, known methods
  enumerate roots over auxiliary splitting primes.  For the best third-target
  split `h=66254*3107441`, the quotient degree is attractive but the generic
  recovery degree `3107441` is already above `sqrt(h) ~= 453740`, and no
  Weber/eta/Atkin/generalized invariant is known that realizes this arbitrary
  odd quotient with cheap recovery to `j`.
smooth-class arithmetic relation audit: the class factors are coprime to the
  target odd cofactor and to `D_K`; `gcd(h,p-1)=gcd(h,p+1)=2`, so there is no
  visible Kummer/radical or group-order shortcut tying the smooth class group
  to p24 field arithmetic
conductor in Z[pi] is only 2
one-root CM/root-finding does not help: Montgomery A is bounded-degree over j,
  root finding still has a p^(1/2) term once H_D is available, and H_D itself has |D| ~= p
split-prime-over-2 relation cannot occur before norm 2^78
ray/orientation audit reduces to the same X0-to-X1 gap; X0(2^41) index is 3.30*sqrt(p)
genus quotient saves only 1, 3, and 1 bits
non-scalar principal relation norm is > 1.6e23
small split-prime cycle audit: the best split-prime cycle relations through
  ell<=200 still have composite degree at least 2.39e11*sqrt(p), and keeping
  them as local cycle equations leaves billions of cycles without a seed root
ramified primes, including 4973929, are nonprincipal genus data, not self-loops
class-number-one / exceptional-j CM traces do not hit strict depth; D=-7 has v2=3
near-square seed modular-neighbor audit: the smooth third target has the
  tempting congruence `23 | n + t/2` for `p=n^2+7`, and norm `23` generates
  its target class group, but `Phi_23(-3375,Y) mod p` has only the seed
  `j=-3375` as an F_p root; the only new tested F_p neighbor is the level-2
  conductor-2 root `j=16581375` in the same `Q(sqrt(-7))` CM field, still
  with trace `+/-2n` and `v2=3`
small genus CM factor audit: `-211`, `-599`, `-7*4973929`, and
  `-211*4973929` split at p but are nonprincipal over F_p; only `D=-7`
  gives a principal small-CM trace and it has depth 3
cyclotomic/Jacobi-sum quadratic-subfield audit: cheap p-1 subfields give only
  D=-7 depth 3 and D=-203 depth 0 traces; cheap p+1 unitary-character
  subfields are inert/nonprincipal over F_p; no strict Jacobi-sum trace
higher-order Jacobi/hypergeometric CM-field barrier: an elliptic Jacobi-sum
  trace still has a quadratic CM field.  The strict target conductors share
  only tiny genus factors with `p-1` (`29`, `7`, or `1`), none with `p+1`,
  do not divide `p^2-1`, and do not divide `p^f-1` for any `f<=64`; so
  higher-order characters do not expose the target CM fields cheaply.
fixed-prime prescribed-order construction is the same large-discriminant CM problem
fixed-trace algorithm sidecar: known exact fixed-field prescribed-trace/order
  constructions reduce to CM/root selection for
  `Q(sqrt(t^2-4p))`; variable-field prescribed-order methods spend their
  freedom choosing a friendly field/discriminant, and flexible subgroup
  methods do not prescribe the exact trace.  For p24, the strict traces have
  `|D_K|/p ~= 0.65..1.00` and conductor only 2, so the known toolbox gives
  no sub-sqrt fixed-trace constructor.
Waterhouse/Mestre fixed-trace audit: Waterhouse/Rueck/Voloch supply
  existence and group-structure criteria, while Tate identifies fixed trace
  with a fixed elliptic isogeny class.  The constructive prescribed-subgroup
  route still computes `H_D`, finds a root mod p, and chooses the right twist.
  For the three strict absolute traces the `H_D` degrees are
  `0.278734`, `0.833035`, and `0.205880` times `sqrt(p)`, respectively.
  Mestre/Cremona-Sutherland is useful for point counting, not for selecting a
  fixed p24 isogeny-class representative.
conductor-2 CM root sidecar: the principal norm representation proves the
  target CM roots split over F_p, but does not select one among about 1e11
  residual classes after genus data
principal CM root torsor audit: in the toy `D=-5000,h=30,q=1259` calibration,
  all 30 CM roots are fixed by Frobenius and any root can be labeled
  "principal" after rotating the abstract class-group coordinate; the p24
  principal norm representation likewise gives splitting, not a class-field
  embedding/root selector
ramified-factor tradeoff: small ramified primes, including the tempting `-7`
  component in the middle discriminant, are only genus quotients and still
  leave about 1e11 residual classes
Redei 4-rank audit: all three target discriminants have 4-rank zero, so the
  2-primary class structure stops exactly at genus; no hidden 4/8/... layers
root-only CM sidecar: known CRT/p-adic/class-invariant/prescribed-order
  algorithms still compute a class object, require a seed root/curve in the
  target isogeny class, or choose a friendlier field/discriminant; none names
  one p24 strict root among the residual odd class group for free
CM/class-field subagent audit: the norm equation makes Frobenius at `p`
  trivial in the target ring class field, so all class-field quotients see
  complete splitting but do not distinguish a prime/root above `p`; fixed
  class invariants and genus/ray quotients only give constant-bit labels,
  leaving about `1e11` residual odd classes
CM ray-class orientation degree audit: adding the strict `2^40` x-coordinate
  orientation to CM honestly gives degree `h*phi(2^40)/2 = h*2^38`;
  for the three target traces this is `5.66e10` to `2.29e11` times
  `sqrt(p)`.  Even the dream third-target quotient `66254` becomes
  `66254*2^38 = 1.82e4*sqrt(p)` when marked by the ray.
higher-dimensional factor audit: genus-2/Jacobian, product, gluing, Weil
  restriction, and small-CM abelian-surface wrappers do not bypass the
  elliptic target selector.  If the strict elliptic factor is present, the
  construction has already encoded the same target quadratic CM field/isogeny
  class; extension traces multiply `t^2-4p` by a square and keep the
  fundamental CM field unchanged.
reverse canonical-lift / Serre-Tate audit: Satoh/AGM/canonical-lift machinery
  counts or describes Frobenius after an ordinary curve is chosen.  Running it
  backward with `lambda == 1 mod 2^40` is just the prime-to-p trace
  congruence; in p24 it leaves the same six traces, and fixed `(p,t)` is the
  CM locus for `t^2-4p`.  The near-square identity supplies only the
  `D=-7`, trace `+/-2n`, depth-3 curves.
public lead scan: no public p24 verifier-compatible triple or asymptotic
  strict-DANGER shortcut found in the official DANGER3 repo, Ruehle's repo,
  Alexa's fork, the p23 PR, GitHub code/issue/commit search, or exact-integer
  web search.  Public p23 remains an `X1(16)` constant-factor method.
```

So neither class polynomial construction, genus characters, nor low-degree CM
cycles give a sub-sqrt target-class construction.

Growing `X1(2^a)`:

```text
density gain from level N is about N
gonality / optimized-model fiber cost grows like N^2
X1(32) degree_y = 10
X1(64) degree_y = 40
```

Fixed `X1(16)` is a good constant-factor tactic, but growing generic `X1`
does not improve the exponent.
Exact partial-oriented sampler counts give beta about 0.97-0.98 for X1 depth,
essentially rejection-style; X0 has beta 0 only because it omits orientation.

`X0(2^a)` / isogeny-chain compression:

```text
X0 trace image size for p == 7 mod 16 is 2^(a-3)
DANGER target residue has four eigenvalue preimages
only two are true X1 orientations at level 2^a
two-adic trace inversion sidecar: Satoh/AGM/theta/Landen inversion has to
  choose the same ray tail, so it is X1 construction rather than a free inverse
conditioned X0-to-X1 character scan finds only the A±2 constant branch gate
orientation cover degree is phi(2^a)/2, so the missing X1 information grows with level
half-level X0 splits the entropy into 2^(k-d) trace-lift bits and 2^(d-2)
  orientation bits; their product is still 2^(k-2)
intermediate diamond quotient audit: for `2^40`, the diamond group modulo
  sign is cyclic of size `2^38`; every subgroup quotient only trades modular
  index against the same residual orientation fiber, with best quotient index
  already `Gamma0(2^40)=1.649267*sqrt(p)` and no strict lift supplied
X1 tower MITM audit: starting from the cheap `X1(16)` base, a rejection-style
  lift to `X1(2^h)` costs `2^(h-4)` and the residual tail costs `2^(40-h)`,
  so the product is always `2^36`; a true split would require a sampler for
  nested quadratic lifts with exponent `beta<1`.  Balanced branch enumeration
  still leaves positive-dimensional parameter families, and base-parameter
  MITM subsets have size about `p/2^(h/2)`, far worse than sqrt for `h<=40`.
inverse-tower curve-intersection audit: splitting the exact depth-40 equation
  at a middle coordinate gives curves of degrees `2^a` and `2^(40-a)` in the
  `(A,x)` plane; Bezout product is always `2^40 = 1.099512*sqrt(p)`.  A
  balanced `20+20` split lowers the largest single degree to `1048576`, but
  the resultant/intersection still has sqrt-scale entropy.
parallel modular sidecar: Atkin/Elkies statuses, Fricke/Atkin-Lehner
  involutions, volcano orientation, and CRT factorization only quotient by
  constants or reintroduce the missing 2-adic eigenvalue tail
```

Thus `X0` gives an 8x trace-residue constant, not a growing gain.  The missing
orientation is exactly the hard `X1` cover.

Odd trace residues and Atkin status:

```text
exact odd residues can isolate the six traces as a free oracle
exact trace-residue oracle tradeoff: even if a construction could impose the
  exact union of target trace residues modulo `N` for only `Gamma0(N)` cost,
  level only trades against residual Hasse lifts.  Sampled optimum is
  `N=2^40`, six survivors, proxy `1.649267*sqrt(p)`; no exponent gain.
mixed CRT trace-residue optimizer: searching `N=2^d*R` with `R` a squarefree
  product of small odd primes up to 47 and `R<=20000` again selects pure
  `2^40` as the best generous oracle (`gamma0/sqrt=1.649267`, `survivors=6`);
  odd CRT residue information breaks the threefold `2^40` target-trace
  collision and worsens constants in this window.
Atkin status gives only a few cheap half-bits
reverse-SEA exact-residue construction has Gamma0 lower bound >4.76*sqrt for every d<40
mixed odd/2 divisors above the DANGER bound have best Gamma0 index 1.53*sqrt(p)
mixed odd/2 divisors above the Hasse width have best Gamma0 index 3.05*sqrt(p)
low-degree chi(q(A,n)) labels give at best the known A±2 terminal-branch gate
statistical lift baselines: exact small `p=n^2+7` runs give oriented-depth
  rare-event beta about one (`aggregate_fitted_beta_x1=1.038291` on larger
  rows), low-degree character labels with best aggregate lift `1.485`, and
  dyadic A/j buckets whose lift increases only as capture collapses
upstream DANGER3 dataset audit: Sutherland's `pp12`, `pp16A`, and `pp24`
  data were cloned under `p24/upstream_DANGER3` and scanned.  The one-witness
  `pp24` file is almost entirely nonsplit zero-terminal
  (`1074967/1077869` nonsplit), but `pp16A` all-prefix data is much closer to
  balanced and has `#good A / sqrt(p)` bounded by constants organized by the
  number of Hasse target orders.  In the p24-relevant `p % 8 == 7` slice the
  strongest cheap character gate is the fixed terminal-branch fact
  `chi(A+2)=+1`, `chi(A-2)=-1` with about `1.498x` lift; terminal-branch
  audits explain this as a constant sign-pattern mixture, not a growing
  trace selector.  Upstream witnesses also do not hide a simple inverse
  branch code: their last zero-branch predecessor is split essentially evenly
  between `+1` and `-1`.
upstream good-A projection audit: exact `pp16A` good prefixes through `2^16`
  do not compress under natural Montgomery projections by more than constant
  degree.  On the p24-relevant `p % 8 == 7` upper-half slice, `A^2` has
  mean image/good `0.500033`, `j` has `0.381146` with max fiber at most 4 in
  the run, and terminal sign-pairs collapse only to the already-known fixed
  branch buckets.  No tested projection gives growing fibers or a lower-scale
  selector.
upstream one-witness selection audit: comparing `pp20`/`pp24` one-prime
  witnesses against `pp12` all triples through `2^12` gives
  mean triple-rank quantile `0.500923`, mean good-A-rank quantile `0.499635`,
  and only `2/560` first lexicographic triples.  The witness files have a
  constant nonsplit/zero-terminal bias but do not expose a low-rank
  deterministic generator rule.
full small-triple x0/halving-word audit: exact `pp12` has `3,083,880` triples
  and `80,263` prefixes; accepted x-fibers are structured
  (`x_per_A` quantiles `16,16,32,32,64,128`) and have exact reciprocal plus
  `(A,x)->(-A,-x)` 4-orbit symmetry, but these quotient only by constants.
  x-specific characters are balanced, while the known `A±2` terminal branch
  captures about `0.67`.  Inverse branch-word prefixes decay like uniform
  choices after the first terminal degeneracy: in all `pp12`, the best
  four-symbol prefix captures are about
  `0.335,0.0846,0.0212,0.00547,0.00143,0.000372`; the `p % 8 == 7` tail
  behaves the same.  No hidden growing branch-code selector is visible.
larger upstream one-witness stream audit: the linked `pp28`, `pp30`, and
  `pp32` archives are ordered extensions from the same generator; local
  `pp24` is exactly their prefix, and the first `1,300,000` rows are identical
  across the larger files.  Streaming all of `pp28` reproduces the same
  nonsplit/zero-terminal branch artifact with uniform-looking `A/p` and
  `x0/p`.  In the closest p24-shaped family `p=n^2+7, n==0 mod 8`, the
  one-witness representatives all satisfy
  `(chi(A+2),chi(A-2),chi(A^2-4))=(1,-1,-1)`, but the all-prefix `pp16A`
  slice captures only about `0.48` of good `A` values in that gate, including
  the `target_orders=3` rows.  This is a representative-selection artifact,
  not a growing selector.
trace-distribution/equidistribution sidecar: the six signed p24 target traces
  have discrete Sato-Tate mass about `1.70e-12`, so the trace-level expected
  search is about `5.89e11`; known probabilistic trace tools describe this
  rarity and validate constant gates but do not name a rare Montgomery `A`
class-group probability audit: Pollard rho, birthday, hidden-shift, expander
  walks, and random self-reducibility become useful only after an embedded
  class-action oracle or seed CM root exists.  For the smooth third target,
  `sqrt(h)=453740 << sqrt(p)`, but the abstract class group samples labels,
  not `F_p` `j` values; no seed/no embedded invariant means no finite-field
  state space for the random walk.
smooth-class Kummer/radical audit: the third target's cyclic class group
  `h=2*157*211*3107441` is smooth, but its odd factors do not divide `p-1`;
  direct Kummer radicals are not available in `F_p`.  The largest factor
  would need roots of unity over an extension of degree `388430`, and the
  full odd part has root-of-unity extension degree `30297540`; the
  defining embedded subfield polynomials/recovery maps are still the missing
  class-field object.  Smooth abstract class group does not imply seedless
  radical descent to one CM root.
stacking cheap character gates plateaus near a 2.1x holdout lift
additive Fourier/residue scans show no stable low-frequency or small-modulus selector
multiplicative A/j spectra show only random-sized coefficients and unstable low-order coset lifts
odd-character residual entropy scan: after conditioning on the known
  low-degree Legendre sign, low-order odd multiplicative cosets of
  `A`, `A±2`, `A^2±n`, `A^2-4`, and `A^2±nA+1` give only row-local
  lifts; leave-one-out median holdout lift is `1.003`
dyadic A/j residues show only constant/random bucket lifts: in exact
  `p=n^2+7` rows through 500k, best broad bucket is just parity
  (`j mod 2`, lift 1.034, capture 0.517), while high-lift `2^12` buckets
  capture about 0.1% of hits
moment/Hankel audit shows only A -> -A symmetry, random-sized low-degree moments, and full moment rank
constructing the residue intersection means growing modular level
```

As rejection filters, these do not change the probability that a random curve
has the target trace.  As construction data, they reintroduce the same
growing-level cost.

Inverse chains:

```text
classical halving from the universal 2-torsion starts with explicit formulas:
  `2Q=(0,0)` gives `x(Q)=±1`, and one more `x=1` inverse has
  `A=((u^2-1)^2-4u(u^2+1))/(4u^2)` with
  `A+2=(u-1)^4/(4u^2)`.  Extending this to 39 halvings is exactly
  a marked `X1(2^40)/±` point, not a separate shortcut.
geometric, arithmetic, LFT, LFT-geometric, s-coordinate, edge-coordinate,
power-map, and quadratic-recurrence section ansaetze all collapse to
degenerate or constant orbits
second-order linear Chebyshev/Lucas recurrence ansatz
  `x_{i+1}=a*x_i+b*x_{i-1}` on the universal 2-torsion terminal branch has
  compatibility gcd 1 over Q and over F_p24 through depths 3..6; no
  one-parameter hidden-torus section.  A p24 resultant check for the first
  three compatibilities gives only `a*(a-1)^9`, i.e. invalid/constant
  terminal cases.
inverse MITM mass ranking is only a partial 2-adic depth filter, not an A selector
inverse-chain MITM split audit: partial-depth stage cost times residual full-depth
  cost stays equal to the full-depth cost for X1 and X0 conditioning
inverse-chain state entropy audit: exact small-field rows confirm that
  partial oriented depth and residual rarity are reciprocal; for p24, every
  algebraic split `a+(40-a)` has Bezout product `2^40 = 1.099512*sqrt(p)`.
  Balanced MITM lowers the largest single degree to `2^20`, but not the total
  orientation entropy.
pair-level verifier relation audit finds full rank through total degree 10 / bidegree (5,5)
literal verifier audit matches exact-order curve/twist prediction on exact small fields
post-trace audit: x0 construction is cheap after A is known; target-trace A selection is the bottleneck
x-projection concentration audit: accepted pairs project densely but flatly to
  x; fixed simple x values have only constant-sized A fibers even when the
  fixed-x division polynomial has degree 65535 at depth 9
high-dimensional inverse-chain sidecar: adding recurrence states, transfer
  matrices, EDS variables, or MITM/elimination coordinates repackages the same
  X1(2^40) ray-orientation condition unless it carries a new p-specific label
modular/tower subagent audit: X1, X0-to-X1, Landen/AGM/canonical-lift
  inversion, and extension-field torsion all still need the same
  Frobenius-fixed ray `lambda == +/-1 mod 2^40`; extension-field descent loses
  2-adic order unless the strict orientation was already present
division-polynomial splitting barrier: `Z_k(A,x)=0` projects to essentially
  every nonsingular `A` over `Fbar_p`; the verifier condition is the
  arithmetic splitting/Frobenius condition that an exact-order factor has an
  `F_p` root, again the same X1 ray orientation
```

Backward enumeration is useful once `A` is known, but it does not choose the
rare trace-compatible `A` values.

Near-square low-height sections:

```text
no low-height LFT in n found for A, A^2, j through coefficient bound 12
fresh small-family rerun with bundled NumPy: for small `p=n^2+7`, A-line and
  j-line LFTs of coefficient bound 6 died by row 4 over 24 rows, and Landen
  coordinate LFTs died by row 3 over 18 rows; top hit counts match random
  bucket behavior rather than a near-square section
no low-height LFT in n found for upstream X1(16) y, y^2, or u=(y^2-2)/(y-1)
no low-height LFT in n found for split root r, Legendre lambda, or Landen coordinate
no low-height degree-2 rational formula in n found for those X1/Legendre coordinates
no low-height implicit quadratic equation in A over Q(n) found
no low-height implicit cubic equation in A over Q(n) found at the smallest height
no low-degree moment, small-height power-sum, or short-recurrence structure in exact good-A buckets
bounded-degree explicit j-line families only change constants; p^(1/4) trials would need degree about 7.6e5
Edwards / complete-Edwards audit: complete Edwards with nonsquare d is exactly
  the nonsplit Montgomery half via A=2*(1+d)/(1-d); exact small rows gave
  strict-density lift 1.00287x, a constant not a selector
bounded-height constant A, A^2, or j values through height 200 have no exact near-square survivors after 3 calibration primes
near-singular torus-coordinate LFTs A=+/-(r+1/r), r=(a*n+b)/(c*n+d), have no survivors through height 16
finite-field identity sidecar: the real D=-7 near-square CM selector has only v2=3 for p24;
  the strict target traces have conductor 2 and fundamental discriminant comparable to p
near-square radical relation barrier: the middle target's `-7` discriminant
  factor gives an explicit square root of the quotient modulo p, but this is
  only genus splitting; all strict target CM fields are distinct from
  Q(sqrt(-7)), so an ordinary target curve cannot inherit the D=-7
  endomorphism
trace-lattice low-height audit: with `n=10^12` and `M=2^40`, the three
  curve-side target traces are exactly
  `p+1-M*(909494701772+j)`.  The best small linear relation through
  coefficient bound 64 is the shared approximation
  `t_j = 45*n - (40+j)*M + 1073491976`, whose residual is still about
  `1.07e9`; small-coefficient quadratic searches in `n,M` for the target
  fundamental discriminants leave residuals around `1e21`.  No exact
  low-height near-square identity is visible.
split-2 strict-orientation audit: the strict trace residue gives four
  2-adic eigenvalue roots modulo `2^40`, two true X1 orientations and two
  X0-only orientations.  But the split ideal above 2 has exact class orders
  `278733727154`, `208258802086`, and `102940198007` for the three targets;
  after the 40th power the remaining orders are still about `1e11`.  The
  known 2-adic eigenvalue root is a ray condition, not a seed CM-root
  selector.
```

Thus the identity `p = n^2 + 7` gives the broad `D=-7` certificate, but not a
visible low-height strict-DANGER section in the tested coordinates.

Certificate-format relaxations:

```text
Pomerance type-2 can add at most one independent factor of 2 because v2(p-1)=1
mixed odd/2 divisors still leave the best strict route at 2^40
odd-cofactor orientation audit: forcing a large odd divisor first is tempting
  because the third target has `2^41*454747350887`, and some `X0(m)` indices
  are below sqrt.  But `X0(m)` only gives a stable cyclic subgroup; the
  condition `m | #E(F_p)` requires the odd Frobenius orientation
  `lambda=1` (or the dual branch).  Across target odd divisors, the product
  of the x-only orientation cover `phi(m)/2` and the residual Hasse trace
  count remains sqrt-scale; the best p24 row is `m=21` at
  `1.142857*sqrt(p)`, while large prime cofactors have generic `Gamma1(m)`
  index far above sqrt.
consecutive cofactors q,q+1,q+2 are just the 2^40 trace progression, not a selector:
  factor-chain facts such as `454747350887-1 = 2*29*71*110429177` support
  recursive ECPP/cofactor certification after a curve exists, but cyclotomic,
  q-isogeny, and odd-eigenvalue interpretations still require the same
  orientation cover to construct the target `A`
the q+2 target has prime odd part after its extra factor of 2, but this only
  makes odd-part projection pleasant after the target isogeny class is found
target cofactor embedding audit: the high-2-power side large cofactors do not
  have small embedding degree over `F_p`; e.g. the third target prime cofactor
  `454747350887` has embedding degree `454747350886`.  The prime cofactor is
  pleasant for post-construction projection, not an MNT/pairing-friendly
  fixed-field constructor.
singular torus limits have only v2(p-1)=1 and v2(p+1)=3 and are rejected
actual p24 X1(16)->X1(32) tail shard behaves randomly: 100k accepted rows gave hit24=0
```

## Remaining Live Shape

For the strict verifier, the missing object would have to be genuinely
p-specific arithmetic, not a known generic modular-curve sampler:

```text
1. a special finite-field identity that forces Frobenius eigenvalue 1 mod 2^k;
2. a cheap curve-level trace-v2 label that is constructive, not just rejecting;
3. a non-generic inverse-chain section outside the low-dimensional families
   already tested.
4. an explicit odd class-field quotient/tower for the third target
   `D_K=-652834595820939249713143` that uses its smooth-ish class number
   `2*157*211*3107441` to recover a CM j-root over F_p without enumerating
   the full class set.  See `p24/smooth_class_tower_route_note.md` and
   `p24/embedded_classfield_tower_worklog.md`.
```

Everything found so far that is rigorous and fast either certifies `p` outside
the DANGER3 format, or gives only a constant-factor improvement inside it.

The latest embedded-tower sharpening confirms the abstract class-field layers
for quotient degrees `2`, `157`, `211`, `66254`, and `3107441`; the degree-2
layer is `x^2 + 599`.  This does not yet select a CM `j` root: the missing
object is an embedded invariant or finite-field identity with a recovery
relation to `j`.  A toy D=-5000 selector search found no low-degree plain-`j`
identity before the generic rational interpolation threshold.

The newest theorem attempt sharpens the best embedded candidate to split-prime
cycle quotients.  In the D=-5000 toy, an `ell=11` class of order `3` partitions
the 30 CM roots into ten 3-cycles; X0 edge values have full orbit, but
whole-cycle sums give the quotient degree.  For p24, `ell=7349` gives
`class_order=487868237` and `cycle_count=422`, while `ell=677` gives
`class_order=655670051` and `cycle_count=314`; all formal degrees are far below
`sqrt(p)`.  The missing object is now a seedless way to construct or select one
target split-prime cycle over `F_p`.

This can be stated more cleanly as a class-character period problem.  The
cycle periods are inverse DFTs of twisted traces
`T_chi=sum chi(a)j(a)` for characters of `Cl(O)/H`.  For p24 the DFT layer is
small (`422` traces with root-of-unity extension degree `35`, or `314` traces
with extension degree `156`).  What is not known is a sublinear formula for
these high-order non-genus twisted traces.  A tiny `D=-87` elimination recovers
the cycle-sum quotient from `H_D` and `Phi_7`, but using `H_D` at p24 is already
the degree-`205880396014` class-polynomial barrier.

The all-target split-cycle audit found a cleaner target in the first strict
trace:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 2 * 19 * 7335098083
ell=19:
  cycle_count = 19
  cycle_length = 14670196166
  X0 degree = 20
  seeded_walk_proxy = 293403923320 = 0.293404*sqrt(p)
  root_of_unity_extension_degree = 2
```

This is now the cleanest period-selector theorem experiment: compute an
embedded order-19 class-character period quotient and recover a `j` root
without `H_D` or class enumeration.  It is not the best certificate target by
itself because the recovery degree is still `14670196166`; the third trace's
composite `2 * 463 * 223^(-1)` cycle remains the best balanced certificate
target with recovery degree `3107441`.

The latest period-selector audit closes three tempting variants of that idea.
Quotient power sums are convolutions of the same high-order traces, so moment
methods still need the subgroup idempotent.  Product/norm periods are valid
quotient coordinates only if one can compute the full relative norm; global or
genus norms erase the quotient phase.  Abstract `bnrclassfield` equations also
split over `F_p` without pairing their roots to embedded `j` recovery factors:
in a `D=-87` toy, `x^2+3` roots `[10,93]` and embedded cycle-sum roots `[4,29]`
are unpaired until a relation to `j` is supplied.  The standard non-genus
twisted-trace modular-form route has level `|D_K|` and a Sturm/index proxy
about `5.45e10*sqrt(p)`, not the small quotient degree `314` or `422`.
A small complete-CM period scan also found full linear complexity in every
tested quotient-period sequence, including the calibrated `D=-5000` row, so no
short recurrence/sparse-spectrum lift is visible at toy scale.

Composite split ideals sharpen the formal CM candidate.  The product
`2 * 919` has class index `422`, improving the old single-prime `ell=7349`
correspondence norm.  More importantly, the balanced product
`2 * 463 * 223^(-1)` has index `66254` and order `3107441`; its norm is
`206498`, its `X0` index proxy is `311808`, and the crude seeded-walk proxy is
`968924963328 = 0.968925*sqrt(p)`.  This is the best formal embedded object
so far, but it still needs the seedless quotient/period theorem.
It also needs orientation: the plain unoriented `X0(206498)` sign choices
generate only an index-2 subgroup with recovery degree `102940198007`, so an
unoriented composite modular equation loses the balanced split.
Adding orientation as a literal level structure is not a walk-level escape:
binary sign labels give a seeded proxy `7.75*sqrt(p)`, while full
X1/Gamma1-style marking is thousands of `sqrt(p)`.  The composite target is
therefore only useful if a non-walk embedded period theorem constructs the
oriented quotient directly.

An oriented-relation toy models the inverse-SEA obstruction.  For
`D=-5000,h=30`, split-prime logs satisfy `log(3)+log(11)+log(43)=0 mod 30`;
the corresponding relation word fixes all 30 CM roots, not one root.  Likewise
`11^3` closes at every root while producing ten 3-cycles.  Oriented Elkies
relations are equivariant Cayley-graph data unless an origin/period selector
has already been supplied.

The newest selector-theorem pass adds several sharper closures.  Abstract
class-field quotients reduce modulo `p` to torsors of primes above the ordinary
prime of `K`; pairing those roots with embedded `j` periods is extra data, not
provided by `bnrclassfield`.  The consolidated admissible-selector theorem now
rules out bounded local coordinates, sparse additive Hecke projectors under
reduced normality, bare abstract towers, seedless child sections, and
genus-only labels.  Hecke-correlation and moment formulas diagonalize to the
same class-character traces (`T_s T_{-s}` in the second-moment case), so they
are bookkeeping unless a new projector onto `H` is supplied.  Fast powering or
resultants of split-prime correspondences likewise keep the full orbit or have
exponential correspondence degree; the quotient appears only after
whole-subgroup aggregation.

The p-specific reduced-normality loophole was tested at toy scale by computing
`gcd(sum_i j_i T^i, T^h-1)` for complete split CM cycles.  A 40-row scan found
`normal_rows=40`, `nonnormal_rows=0`, and full quotient DFT support in every
row where the quotient roots of unity lived in the base field.  This is not a
p24 proof, but it gives no evidence for a helpful one-prime class-character
collapse.  The remaining p24 theorem would need nonvanishing of the relevant
odd non-genus resolvents modulo the fixed split prime, or a direct formula for
them.
The newest tightening makes the finite-field gap exact: split/separable CM
roots do not imply reduced normality (a degree-5 `F_11` toy has vanished DFT
components), and any p24 vanishing would propagate across the split-prime
torsor and across Frobenius character orbits.  For the third quotient, a
primitive odd collapse would erase `5460` spectral components.  This is rigid
but not impossible by current height bounds.
The packet formulation compresses the third quotient to only 28 irreducible
Frobenius packets (`2` degree-1, `12` degree-35, `2` degree-156, `12`
degree-5460), but computing one packet residue is still the embedded
non-genus period problem.  Toy cyclic-code tests show that even an artificial
one-packet annihilator need not lower the subgroup-projector support; the
broader small-CM scan found `reduced_weight_rows=0/8`.

The modular-unit/ray-distribution exception is also closed for the odd layers.
Distribution relations collapse ray-kernel/local-unit directions, whose image
in the ordinary class group is trivial.  For `ell=157` and `ell=211`,
`Kronecker(D_K,ell)=-1` and `|(O_K/ell)^*|` has no `ell`-factor; the first
`ell`-primary ray factors occur only in the ramified `ell^2 -> ell`
filtration.  The p24 `157` and `211` layers are conductor-one unramified
Hilbert-class layers, so modular-unit distribution does not supply their
relative phase.

The smooth class group was also separated from first-root discovery.  It gives
excellent formal decomposed degrees for the third trace (`66254 * 3107441` and
sum `3173695`), but random target-trace discovery remains `Theta(sqrt(p))`.
Smooth BSGS/Pohlig-Hellman navigation helps only after a seed CM root,
embedded quotient root, or equivalent class-action domain is already known.

The Montgomery trace-function route was also refreshed.  The exact convolution

```text
t(A) = - sum_c chi(c^2 - 4) chi(A + c)
```

is useful for small-field experiments.  Its additive transform has the exact
Kloosterman factorization

```text
sum_A t(A) psi(-hA) = -chi(-h) G(chi) Kl(-4, -h^2/4),  h != 0.
```

A direct check on six small near-square rows matched this formula to relative
error below `2.8e-11`.  Thus additive sparsity would require many exact zeros
in this Kloosterman family.  In the tested p-shaped rows the transform has full
support.  The median energy in the top 256 frequencies was only `0.039016`,
and the strict bucket's low-frequency energy remained around one percent or
less.  Low-order multiplicative cosets in `A` or `j` gave only unstable
constant lifts.  No sparse hypergeometric transform selector is visible.

Latest strict status:

```text
no verifier-compatible p24 triple found locally or publicly
no asymptotic strict-DANGER speedup found
```

2026-06-08 no-CM/admissibility refresh:

```text
fixed-frequency ordinary gate rerun:
  stable supports after descent = 1260
  supports after hypothetical no-fixed-defect theorem = 35
  mixed supports still pass descent and Vandermonde; only the missing
  arithmetic tail-in-prefix theorem rejects them.

greedy exact trace-residue oracle at d=28:
  ell=199,191,37 isolate the six target traces
  selected_product=1406333
  gamma0(2^28*1406333)/sqrt = 587.551526

exact trace-residue level pricing:
  best sampled level = 2^40
  gamma0/sqrt = 1.649267
  oracle_proxy/sqrt = 1.649267

mixed CRT trace-residue optimizer:
  best remains pure 2^40
  proxy/sqrt = 1.649267

small additive/residue rerun in p=n^2+7, n=0 mod 8:
  conclusion=no_stable_low_frequency_or_small_residue_selector_visible
```

Thus if the no-CM rule is binding, the currently known strict-admissible path
is not a better sampler or a stack of cheap rejection filters.  It would have
to be a new constructive finite-field identity forcing the target trace or the
strict `2^40` Frobenius orientation.  The local data does not currently expose
such an identity.

## Reduced-normality correction

The reduced-normality obstruction is now sharper, and the too-broad version is
false.  A new audit found actual small split CM failures:

```text
D=-216 q=103 h=6 zero_order=3
D=-300 q=139 h=6 zero_order=2
```

So one cannot prove p24 reduced normality from split ordinary CM structure
alone.  For additive selectors the exact condition is the affine cyclic-code
minimum

```text
min_{B in Ann(J)} wt(e_H + B) = |H|.
```

Full reduced normality is the clean sufficient condition.  Quotient-packet
nonvanishing only suffices once a construction has already descended to the
`G/H` quotient.  The third-trace support target remains `|H|=3107441`; the
missing theorem is now specifically a p24 p-adic unit/nonvanishing statement
for the high-order non-genus packets, or the direct minimum-weight proof.

Partial oriented-composite windows are also closed.  The theorem in
`p24/partial_orbit_invariance_theorem.md` says an unordered subset aggregate
along a cyclic recovery orbit is `H`-invariant only when the subset is the full
orbit.  The `D=-5000` toy confirms that window polynomials of lengths `1..4`
retain all `30` starts, while length `5` collapses to the `6` quotient
components.  Thus the p24 oriented composite move still requires the full
degree-`3107441` recovery orbit, not a short local arc.
