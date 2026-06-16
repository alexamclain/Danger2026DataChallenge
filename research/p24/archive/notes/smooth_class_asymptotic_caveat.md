# Smooth Class Group Asymptotic Caveat

Date: 2026-06-04 PDT

The third p24 target trace has a strikingly friendly class group:

```text
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = 2 * 157 * 211 * 3107441
```

This is useful fixed-instance arithmetic.  If embedded decomposed-CM equations
for this exact field were available, the final root-finding degree could be
around `3.1e6`, far below `sqrt(p)=1e12`.

But this is not yet an asymptotic speedup for the DANGER3 problem.

## Two Separate Requirements

A strict asymptotic construction would need both:

```text
1. a family or theorem forcing the relevant target class groups to have
   sub-sqrt-smooth quotient structure; and
2. an embedded construction of the quotient invariants and recovery map to j
   in sub-sqrt work.
```

The current p24 data supplies neither theorem.  It only shows that one of the
three target CM fields for this specific p has a smooth-ish class number.

## Fixed-Instance Versus Asymptotic

For this fixed p24 target, a future explicit embedded odd class-field tower
could plausibly beat the raw `sqrt(p)` search yardstick.  That would be a real
certificate strategy for this instance.

For the requested asymptotic speedup, however, an accidental smooth class group
is not enough.  Without a way to predict or force smooth class groups across a
growing family of DANGER targets, the generic CM class-selection entropy
remains `Theta(sqrt(p))`.

## Current Status

The smooth-class lead remains the best p24-specific CM route, but it should be
treated as:

```text
fixed-instance structural lead: yes
verified strict certificate: no
asymptotic speedup: no
```

The missing primitive is still an explicit embedded class-field invariant or
equivalent p-specific selector that recovers a target `j` root without
enumerating the CM class set.
