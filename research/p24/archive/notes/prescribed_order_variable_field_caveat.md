# Prescribed-Order Algorithms Do Not Fix p24

This note records a literature sanity check around a tempting objection:

```text
There are efficient algorithms for constructing elliptic curves of prescribed
order.  Do they construct the p24 fixed trace curve directly?
```

No.  The efficient prescribed-order CM algorithms gain their speed by choosing
a suitable finite field and a small auxiliary discriminant.  The p24 challenge
fixes the field

```text
p = 10^24 + 7
```

and the verifier forces one of a few exact Hasse traces.  That fixes the large
CM discriminants already audited in this folder.

## Primary-Source Check

Bröker and Stevenhagen's prime-order construction says the input is a prime
group order `N`, and the output is:

```text
a prime p and an elliptic curve E/F_p with #E(F_p)=N.
```

They explicitly note that the algorithm will typically construct curves over
prime fields different from `F_N`.  This field choice is the source of the
small-discriminant speedup.

The same paper also states the fixed-field obstruction.  If `p` is fixed and
`N=p+1-t`, then the relevant CM order has discriminant

```text
Delta = t^2 - 4p.
```

For most traces, the field discriminant has the same scale as `p`, and the
Hilbert class polynomial degree/height makes the ordinary CM algorithm large.
The p24 strict traces are exactly in this fixed-field, large-discriminant
case.

Reference:

```text
Bröker-Stevenhagen, Constructing elliptic curves of prime order,
https://pub.math.leidenuniv.nl/~stevenhagenp/primeorder.pdf
```

Relevant local audits:

```text
p24/waterhouse_mestre_fixed_trace_barrier.py
p24/fixed_trace_cm_root_toy.md
p24/hybrid_trace_verifier_boundary.md
```

## p24 Consequence

For p24, the accepted trace classes have fundamental discriminants:

```text
-739589633190799177940983
-998443569409526507503607
-652834595820939249713143
```

Their class degrees are constant multiples of `sqrt(p)`, with the best
certificate-oriented trace still requiring embedded class-field selection:

```text
h = 205880396014 = 66254 * 3107441.
```

Thus prescribed-order algorithms are not a direct asymptotic speedup for the
fixed p24 prime.  They are a variable-field construction method, not a
fixed-field selector for the required DANGER3 trace.
