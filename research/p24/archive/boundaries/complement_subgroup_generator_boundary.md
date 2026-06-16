# Complement Subgroup Generator Boundary

Date: 2026-06-06

This note records the current low-norm split-prime search inside the balanced
complement subgroup:

```text
h = m*n
m = 66254 = 2*157*211
n = 3107441
K = <g^n>, |K| = m.
```

## Question

Could the selected-chain or full-relative-tower producer use a small explicit
split-prime word inside `K` to generate the `157` and `211` relative layers?

Such a word would not by itself solve the embedded phase problem, but it would
give a much more concrete Shimura/Hecke handle on the relative fibers.

## Audit

The script:

```text
p24/complement_subgroup_generator_audit.py
```

enumerates signed split-prime-power products up to a rational norm bound and
keeps only those whose class log lies in `K`.  I ran the full current
threshold:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/complement_subgroup_generator_audit.py \
  --norm-bound 66254 --prime-bound 66254 --max-hits-per-order 4
```

Output:

```text
visited_products=32080

target_order=2 hits_recorded=0
target_order=157 hits_recorded=0
target_order=211 hits_recorded=0
target_order=314 hits_recorded=0
target_order=422 hits_recorded=0
target_order=33127 hits_recorded=0
target_order=66254 hits_recorded=0
```

So no split-prime-power word of norm at most `66254` lands in the balanced
complement with any of the useful target orders.

## Relation To Visible Split Primes

The small-prime action probe still finds good global navigators:

```text
ell=23     full class group
ell=2      index 2
ell=2897   index 157
ell=14057  index 211
ell=677    index 314
ell=7349   index 422
```

These are not elements of the balanced complement `K`; they generate large
subgroups whose quotients have the desired indices.  They help describe the
global class action, but they do not provide a short internal generator for
the relative child fibers after quotienting by `H`.

## Consequence

The selected-chain theorem cannot currently be reduced to:

```text
walk inside K by a low-norm split-prime generator,
then take a short modular-polynomial relation.
```

The producer must instead construct one of:

```text
embedded relative child/Kummer data directly;
the full embedded relative morphism;
a phase-aware p-unit/divisor identity.
```

This matches the recovery-class low-norm boundary in:

```text
p24/low_norm_order3107441_search.md
```

There is no low-norm split-prime-power shortcut for either the selected
recovery class or the balanced complement's visible relative factors.
