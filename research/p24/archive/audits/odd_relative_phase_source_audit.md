# Odd Relative Phase Source Audit

This checks whether the odd `157` and `211` tower phases in the third p24
trace are explained by visible cyclotomic, Jacobi-sum, or small-factor
arithmetic.

The target is:

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
    = -599 * 1089874116562502921057
h = 2 * 157 * 211 * 3107441
```

## Result

The quotient roots of unity are cheap enough:

```text
ord_157(p)   = 156
ord_211(p)   = 35
ord_33127(p) = 5460
```

So Fourier/Kummer inversion over the quotient is not the obstacle.

But the small cyclotomic quadratic subfields are not the target CM field:

```text
Q(zeta_157) quadratic subfield: Q(sqrt(157))      real
Q(zeta_211) quadratic subfield: Q(sqrt(-211))
Q(zeta_599) quadratic subfield: Q(sqrt(-599))     genus factor only
```

A Jacobi-sum construction for the actual target field would need conductor
divisible by `|D_K|`.  The root-of-unity extension degrees then jump to:

```text
ord_q(p), q = 1089874116562502921057:
  49539732571022860048

ord_|D_K|(p):
  14812380038735835154352
```

These are far beyond the `sqrt(p) = 10^12` yardstick.

The odd class factors also do not align with the obvious arithmetic values:

```text
gcd(157*211*3107441, p-1) = 1
gcd(157*211*3107441, p+1) = 1
gcd(157*211*3107441, q-1) = 1
gcd(157*211*3107441, q+1) = 1
```

## Interpretation

The degree-2 genus layer is real and cheap, but it is only the
`Q(sqrt(-599))` split.  The smaller audit

```text
p24/small_genus_cm_factor_audit.py
```

also shows that `D=-599` is nonprincipal over `F_p`: it has Kronecker symbol
`+1`, but no solution to the CM norm equation and therefore no trace/seed
curve over `F_p`.

The odd `157` and `211` relative phases are not coming from a low-conductor
Jacobi-sum identity or from a visible Kummer alignment with `p`, `D_K`, or the
target group order.

Thus the remaining constructive primitive is still the horizontal
relative-period lemma:

```text
compute embedded non-genus class-character traces for the 157 and 211 layers
without enumerating the p24 class group or constructing H_D.
```

Script:

```text
p24/odd_relative_phase_source_audit.py
p24/jacobi_sum_cm_field_barrier.py
p24/small_genus_cm_factor_audit.py
```
