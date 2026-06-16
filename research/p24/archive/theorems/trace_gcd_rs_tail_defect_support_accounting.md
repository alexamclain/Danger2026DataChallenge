# RS-Tail Defect Support Accounting

Date: 2026-06-06

## Point

The cyclic-section descent gate says the defect selector support must be
Frobenius-stable.  For p24 this is a very small finite condition on
`Z/35Z`, but it is easy to overstate.

## P24 Frobenius Orbits

For p24:

```text
p mod 35 = 22.
```

The action `a -> 22a mod 35` has:

```text
7 fixed singleton orbits;
7 length-4 orbits.
```

A stable defect support of size `16` can therefore be one of two types:

```text
0 fixed singletons + 4 length-4 orbits:   35 choices;
4 fixed singletons + 3 length-4 orbits:   1225 choices.
```

So descent alone leaves:

```text
1260
```

stable selector supports.

## Consequence

The earlier useful slogan “the selector should be four length-4 orbits” needs
one extra arithmetic input:

```text
fixed frequencies are ordinary, i.e. no fixed frequency is a defect line.
```

With that theorem, the support search drops from `1260` stable supports to
`35` pure length-4 supports.  Without it, mixed supports with four fixed
frequencies are compatible with base-field descent.

## Check

The finite accounting is in:

```text
p24/trace_gcd_rs_tail_defect_support_accounting.py
```

It verifies:

```text
stable size-16 supports are exactly the two types above;
four length-4 orbits is not forced by descent alone;
a no-fixed-defect theorem would reduce 1260 supports to 35.
```
