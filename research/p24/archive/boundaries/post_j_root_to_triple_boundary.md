# Post-j-Root To Triple Boundary

Date: 2026-06-05

This note packages the final finite tail:

```text
embedded conductor-2 CM j-root
  -> Montgomery A
  -> DANGER3 x0 by odd-part projection.
```

It is deliberately not a root selector.  Its purpose is to show that the
decomposed-CM route only has to produce the right `j` root; the rest is small
finite algebra.

## p24 Shape

For the best third trace:

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = h(4D_K) = 205880396014
p + 1 - t = 2^41 * 454747350887
verifier depth k = 40
```

The conductor-2/nonsplit gate says the strict Montgomery branch is the
conductor-2 CM root branch.  Once a `j` root on that branch is known, a
certificate may supply `A` and `x0`, and a verifier checks:

```text
j = 256*(A^2 - 3)^3/(A^2 - 4) mod p,
A^2 - 4 != 0,
literal DANGER3 x-only replay accepts x0.
```

Optionally it can also check the nonsplit branch:

```text
Legendre(A^2 - 4) = -1.
```

## Toy

I added:

```text
p24/post_j_root_to_triple_toy.py
```

Default run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/post_j_root_to_triple_toy.py --trials 200
```

uses the small conductor-2 analogue:

```text
p = 103
|t| = 8
D = -348
H_D roots = [4,44,62,63,85,86].
```

It reported:

```text
root_count=6
total_strict_A=12
total_found_triples=12
conclusion=conductor2_j_roots_lift_to_montgomery_triples_in_toy
```

Each conductor-2 `j` root had two nonsplit Montgomery parameters, one for
each sign/twist side, and both produced a literal verifier-passing `x0` by
odd-part projection.  Example:

```text
j=86 A_count=2 strict_A_count=2
  trace=8  split=-1 side=curve seed_x=5 odd=3 x0=75 verify=1
  trace=-8 split=-1 side=twist seed_x=2 odd=3 x0=92 verify=1
```

## Consequence

The p24 certificate chain can be stated cleanly:

```text
1. produce one embedded conductor-2 j-root for the third trace;
2. choose/verify a Montgomery A above it on the nonsplit branch;
3. project to x0 using the odd part 454747350887;
4. run the official x-only verifier.
```

Steps 2-4 are finite and small once step 1 is supplied.  The unresolved
asymptotic theorem is therefore exactly the embedded CM `j` producer:

```text
construct the p24 conductor-2 j-root through the degree-66254 quotient and
degree-3107441 recovery object without class-set enumeration.
```
