# All strict trace period frontier

This note broadens the period-selector search from the smooth third trace to
all strict p24 CM traces.

## Target Summary

```text
p = 1000000000000000000000007
sqrt(p) = 1000000000000
```

The strict verifier accepts traces:

```text
±1020608380936
±78903246840
±1178414874616
```

The CM root selector only depends on `t^2`, so there are three CM fields.

## Split-Cycle Audit

I added:

```text
p24/all_target_split_cycle_audit.py
```

Running

```text
python3 p24/all_target_split_cycle_audit.py --prime-bound 250000 --show 12
```

finds these formal targets.

### Trace `1020608380936`

```text
D_K = -739589633190799177940983
h = 278733727154 = 2 * 19 * 7335098083
Cl(O_K) cyclic
```

Best split-prime cycles:

```text
ell=19:
  order = 14670196166 = 2 * 7335098083
  cycle_count = 19
  X0 degree = 20
  seeded_walk_proxy = 293403923320 = 0.293404 * sqrt(p)
  quotient root-of-unity extension degree = 2

ell=107:
  order = 7335098083
  cycle_count = 38 = 2 * 19
  X0 degree = 108
  seeded_walk_proxy = 792190592964 = 0.792191 * sqrt(p)
  quotient root-of-unity extension degree = 2
```

This is now the cleanest small-character theorem target: an order-19 non-genus
period problem with quotient degree only `19` or `38`.  It is not the best
certificate target by itself, because the recovery degree is still
`14670196166` or `7335098083`.

### Trace `-78903246840`

```text
D_K = -998443569409526507503607
h = 833035208344 = 8 * 104129401043
Cl(O_K) = (208258802086, 2, 2)
```

Best split-prime cycles:

```text
ell=2:
  order = 208258802086 = 2 * 104129401043
  cycle_count = 4
  X0 degree = 3
  seeded_walk_proxy = 624776406258 = 0.624776 * sqrt(p)

ell=11:
  order = 104129401043
  cycle_count = 8
  X0 degree = 12
  seeded_walk_proxy = 1249552812516 = 1.249553 * sqrt(p)
```

These quotients are tiny, but they are essentially 2-primary/genus-level
quotients with very large recovery degree.  They do not yet provide an
embedded recovery polynomial or a root.

### Trace `-1178414874616`

```text
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
Cl(O_K) cyclic
```

Best single-prime and composite cycles:

```text
ell=677:
  order = 655670051 = 211 * 3107441
  cycle_count = 314 = 2 * 157
  X0 degree = 678
  seeded_walk_proxy = 444544294578 = 0.444544 * sqrt(p)

composite ideal 2 * 463 * 223^(-1):
  order = 3107441
  cycle_count = 66254 = 2 * 157 * 211
  norm = 206498
  X0 index proxy = 311808
  seeded_walk_proxy = 968924963328 = 0.968925 * sqrt(p)
```

This remains the most balanced formal tower target, but it requires order-157
and order-211 period data.

## Updated Target Split

The first trace should be the primary theorem-toy target:

```text
Compute the degree-19 embedded split-cycle period quotient for
D_K = -739589633190799177940983 and ell=19, then recover one j-root from the
cycle of length 14670196166, without H_D or class enumeration.
```

Equivalently:

```text
compute order-19 non-genus class-character traces T_chi embedded relative to j.
```

This is a much smaller quotient-character problem than the smooth third trace.
However, the same obstruction remains: standard high-order class-character
trace formulas still live at level `|D_K|`, and abstract class-field equations
do not pair their roots with embedded `j` recovery factors.

For an actual p24 certificate path, the best balanced formal target remains the
third trace's composite ideal:

```text
2 * 463 * 223^(-1):
  quotient_degree = 66254
  recovery_degree = 3107441
  correspondence_degree_proxy = 311808
```

The first trace is better for isolating the missing theorem; the third trace is
better if that theorem can actually construct the embedded quotient/recovery
objects.

The composite target must be oriented.  Plain `X0(2*223*463)` sees all sign
choices of the split primes.  The p24 sign-choice audit shows:

```text
desired oriented product:
  index = 66254
  order = 3107441

unoriented X0(206498) sign-choice subgroup:
  index = 2
  order = 102940198007
```

Thus the low recovery degree belongs to the oriented class
`2 * 463 * 223^(-1)`, not to an unoriented composite modular equation.

## Wider Composite Check

A bounded rerun

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/all_trace_composite_order_search.py \
  --prime-bound 500 --max-factors 4 --max-norm 1000000 --show 10
```

did not find a better formal target.  The global best by balanced
quotient/recovery degree remains:

```text
trace = -1178414874616
norm = 206498
x0_index = 311808
index = 66254
order = 3107441
max/sqrt = 3.107e-06
seeded/sqrt = 9.689e-01
terms = (2, 463, -223)
```

The clean first-trace theorem toy also remains unchanged:

```text
trace = 1020608380936
ell = 19
index = 19
order = 14670196166
seeded/sqrt = 2.934e-01
```

The finite certificate surface for this first-trace route is now separated in:

```text
p24/first_trace_order19_certificate_spec.md
p24/lean/QuotientRecoveryCertificateGate.lean
```

It carries the degree-19 quotient polynomial and one selected
degree-14670196166 recovery polynomial, for a coefficient count

```text
14670196185 = 0.014670196185 * sqrt(p).
```

So the target split is stable: first trace for the smallest non-genus theorem
experiment, third trace for the best certificate-oriented balance.

## Norm Equals Index Toy Check

I added:

```text
p24/norm_equals_index_local_phi_toy.py
p24/quotient_period_low_degree_feature_audit.py
```

This tests the `ell=index` coincidence in small CM examples.  With

```text
python3 p24/norm_equals_index_local_phi_toy.py \
  --max-abs-d 30000 --max-h 120 --min-ell 3 --max-ell 31 --max-cases 5
```

the script found odd examples:

```text
D=-743,  h=21, ell=3, order=7,  index=3
D=-2239, h=35, ell=5, order=7,  index=5
D=-2423, h=33, ell=3, order=11, index=3
D=-5391, h=50, ell=5, order=10, index=5
D=-8079, h=50, ell=5, order=10, index=5
```

For each, it compared the horizontal cycle period with local symmetric data
from `Phi_ell(j,Y)` at the surface vertices.  In all five examples:

```text
linear_local_formula_exists=0
```

This is not a proof against all identities, but it says the norm=index
coincidence alone does not make the period a simple local `Phi_ell` invariant.

The follow-up low-degree audit tested the same shape on larger small examples:

```text
D=-12279, h=60, ell=5, index=5
D=-18199, h=91, ell=7, index=7
```

For a generous local feature vector including `j`, the total neighbor sum, the
horizontal neighbor sum/product, and the descending sum, degrees `1`, `2`, and
`3` do not recover the quotient period.  Degree `4` only succeeds when the
feature matrix reaches full row rank, so it is interpolation rather than a
bounded selector.

## Status

No certificate has been found.  The frontier has improved: the cleanest
missing theorem experiment is now order-19 embedded period computation for the
first strict trace, while the third trace's balanced composite cycle remains
the best certificate-oriented target.
