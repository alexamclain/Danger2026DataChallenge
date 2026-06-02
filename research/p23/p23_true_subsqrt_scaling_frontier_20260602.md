# p23 True Sub-Sqrt Scaling Frontier

Date: 2026-06-02 PDT

Purpose: separate what we have as a strong practical p23 search improvement
from what would count as a real scaling improvement over generic `sqrt(p)`.

## Current Answer

The active y-filtered nonsplit `X1(16)` run is still the best production bet
for p23. It can find the p23 certificate at a trial count far below
`sqrt(p)` for this fixed prime if the empirical hazard is close to the working
model.

But fixed `X1(16)` plus nonsplit conditioning is a constant-factor improvement,
not an asymptotic proof of sub-sqrt scaling. A true scaling improvement needs
one of the remaining primitives below.

## What Counts

For the p23 run:

```text
sqrt(p) ~= 316.228B
current production budget = 50B accepted nonsplit trials
50B / sqrt(p) ~= 0.158
35B / sqrt(p) ~= 0.111
```

So a verified hit inside 35B-50B accepted nonsplit trials would be a very
strong fixed-prime result. It would not, by itself, prove that the method has
better exponent than `sqrt(p)` as `p` grows.

For true scaling:

```text
fixed prescribed torsion level -> Theta(sqrt(p)) with a better constant
growing torsion/trace information -> possible exponent improvement
```

The question is whether the growing information can be extracted cheaper than
generic modular-curve rootfinding or generic point counting.

## Ruled Out As Scaling Routes

### Generic X1(N) Prescribed Torsion

The literature-backed barrier is:

```text
density gain from X1(N) prescribed torsion ~= N
generic X1(N) fiber/gonality burden ~= N^2
```

For `N = 2^a`, the modular-curve index is:

```text
[SL2(Z):Gamma1(N)] = N^2 * product_{ell|N}(1 - ell^-2)
                  = (3/4) * N^2  for powers of 2
```

Abramovich's gonality lower bound and the Derickx-van Hoeij/Sutherland tables
both point to the same shape: once `N` grows, generic one-parameter sampling
cost grows faster than the density gain.

Local p23 evidence agrees:

```text
X1(32) root-existence floor ~= 0.001855M fibers/s
active nonsplit worker      ~= 0.108M accepted trials/s
ratio                       ~= 58x slower before root extraction/conversion
```

Conclusion:

```text
Generic higher X1(N) rootfinding is not the sub-sqrt route.
```

Backing notes:

```text
notes/prescribed_torsion_scaling_barrier_20260602.md
notes/x1_32_c_rootbench_20260602.md
```

### Trace Residues By Generic SEA / Quotient Rings

Odd trace residues are mathematically attractive because target traces occupy
only two residues modulo each odd prime. The p23 trace-lattice model shows
they stack cleanly at early depths.

The implementation barrier is cost:

```text
active candidate cost ~= 9.259 us
direct-y candidate cost ~= 8.511 us
ell=3 break-even cost ~= 3 us
measured exact ell=3 predicate ~= 72 us
```

Conclusion:

```text
Generic exact trace-residue filters are mathematically real but operationally
too slow by more than an order of magnitude.
```

Backing notes:

```text
notes/p23_trace_lattice_model_20260602.md
notes/p23_trace_filter_break_even_20260602.md
notes/ell3_direct_y_quartic_benchmark_20260602.md
```

### CM Exact-Trace Construction

The two p23 target traces lead to very large discriminants with no hidden
small-class shortcut:

```text
4p - 321963163766^2
  = 2^4 * 3 * 6173744191203913847869

4p - (-227792650122)^2
  = 2^4 * 19 * 2377 * 481741841427711973
```

Conclusion:

```text
CM is ruled out as a p23 exact-trace construction path.
```

Backing note:

```text
notes/cm_exact_trace_audit.md
```

### Short-Certificate Low-Product Frontier

The external `danger3-short-certificate-experiments` repo is useful for
post-hit compression, but its sparse low-product frontier is not a first-hit
route for p23.

Conclusion:

```text
Use after a hit, not before a hit.
```

Backing notes:

```text
notes/danger3_short_certificate_transfer_recap_20260601.md
notes/short_certificate_repo_transfer.md
```

## Still Plausible Scaling Primitives

### Special 2-Power Tower Section

This is the cleanest possible prescribed-torsion route:

```text
grow from X1(16) toward X1(2^m)
avoid generic degree/gonality rootfinding
retain cheap per-candidate generation
```

Status:

```text
not found yet
still mathematically alive, but narrower after first-lift-cover tests
needed for a true higher-torsion scaling result
```

Updated scaling criterion:

```text
If prescribing level N=2^a gives about an N-fold density gain and the sampler
overhead is N^alpha, then total search work is sqrt(p)*N^(alpha-1). A true
sub-sqrt prescribed-torsion route needs alpha < 1.
```

The generic X1(2^a) route has alpha about 2 from index/gonality and from the
observed Sutherland model degrees. The first-lift cover itself is:

```text
z^2 = H(y)
H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

with H squarefree of degree 5, hence genus 2 and not a square in Q(y). Thus
there is no rational section over the X1(16) y-line. This closes the simplest
"special section" hope; any surviving tower construction must be more
structural than choosing a rational z(y).

The latest nearby test scanned cheap sign-invariant characters on the exact
first-lift cover:

```text
z^2 = (y - 1)(y^2 - 2)(y^2 - 2y + 2).
```

Feature family:

```text
chi(Norm(q(y) + z)) = chi(q(y)^2 - H(y))
```

for small linear and quadratic `q(y)`.

p23 result:

```text
50k accepted first-lift-cover rows
base depth-12 survival = 346/50000 = 0.006920
best depth-12 lift = 1.178x
best survivor capture ~= 0.590
```

Conclusion:

```text
Low-degree norm characters on the first-lift cover are ruled out as a cheap
tower-section primitive. A special 2-power route now needs something more
structural than one extra cover Legendre label.
```

Backing note:

```text
notes/two_power_tower_section_obstruction_20260602.md
notes/x16_first_lift_cover_feature_scan_20260602.md
```

### Curve-Level Trace-v2 Label

In the nonsplit family, the marked halving depth equals `v2(#E(Fp))`. The
active search is therefore already testing the right curve-level event.

The missing primitive would be:

```text
a scalar-time label that predicts or determines high v2(p + 1 - t)
cheaper than the active early-abort halving predicate
```

The cost floor is severe because the active predicate fails fast:

```text
average first-d sqrt calls per nonsplit sample ~= 2.005
```

Status:

```text
maybe alive only if the label is Legendre/square-root-level cheap
```

Backing notes:

```text
notes/x16_nonsplit_depth_equals_v2_audit_20260602.md
notes/trace_v2_prefilter_cost_floor_20260602.md
```

### Exact Root-Squareclass Trace Pullback

This is the odd-residue version of the same dream:

```text
derive an exact parameter-level squareclass condition for trace modulo ell
apply it before halving
stack several small ell filters while the p23 trace lattice is still wide
```

Status:

```text
the mathematics is plausible
current exact algorithms are too slow
low-degree fitted proxies failed
```

### Split Component/Orientation Label

Split curves are trace-enriched in exact enumeration, but the marked point is
usually in the wrong component for this p23 halving chain. The 2-torsion
translation audit proved the component idea is real, but still too slow and
too weak under current costs.

Status:

```text
maybe alive only with a cheap orientation/component label
not a production shard today
```

## Operational Consequence

The production decision remains:

```text
1. Keep the active y-filtered nonsplit X1(16) run alive.
2. If a worker prints Verified: PASS, finalize and independently verify.
3. If the active 50B budget cleanly misses, launch the guarded direct-y
   nonsplit follow-on.
4. Do not switch to generic X1(32), split, ell=3 SEA, or low-product search
   without a new exact low-cost primitive.
```

The research decision is:

```text
Focus tomorrow on special 2-power tower sections and exact scalar-time
trace-v2 / trace-residue pullbacks.
```
