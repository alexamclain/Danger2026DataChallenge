# Correspondence Zero-Lemma Window

This note records a conditional finite-field zero-lemma route and the small
class-group audit that currently rules it out for the useful p24 split
correspondences.

## Conditional theorem shape

Let `G = <beta>` be the target CM class torsor, `|G|=h`, and let a split
class element `b` have

```text
order(b) = n,
index(b) = h/n = m.
```

For a nontrivial character of `<b>`, the relative trace has the form

```text
F_s(j_i) = sum_{k=0}^{n-1} zeta_n^(s*k) j_{i + k*b}.
```

If harmful packet vanishing occurs for every quotient fiber, then by the
character eigenrelation it forces

```text
F_s(j_i) = 0
```

on all `h` CM points.

Suppose optimistically that this weighted trace is realized by a nonzero
modular/correspondence function with pole degree at most

```text
n * delta,
```

where `delta` is the degree/index of one oriented correspondence step.  The
finite-field modular zero lemma would rule out harmful vanishing whenever

```text
n * delta < h,
```

equivalently

```text
delta < m.
```

This is attractive because it would turn a relative character trace into a
certificate without enumerating the class set.

## Audit

I added:

```text
p24/correspondence_zero_window_audit.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/correspondence_zero_window_audit.py \
  --prime-bound 1000 --max-factors 4 --max-norm 250000 --show 12
```

Output:

```text
hits=16550
zero_lemma_window_hits=0

best_ratio_rows
  ratio delta index order norm n_delta_over_h seeded/sqrt signed_terms
   1.500000        3          2    102940198007        2       1.500000    0.308821 (2,)
   2.159236      678        314       655670051      677       2.159236    0.444544 (677,)
   4.706252   311808      66254         3107441   206498       4.706252    0.968925 (2, 463, -223)
   6.540284     2760        422       487868237     1838       6.540284    1.346516 (2, 919)
```

The `delta` used here is only the squarefree `X0` index.  Any honest
orientation cover can only increase it, so this is a generous screen.

## Consequence

The finite-field zero lemma does not certify the p24 relative packet for the
bounded split products in this search window.  The useful balanced row

```text
2 * 463 * 223^(-1)
```

has exactly the right recovery degree

```text
n = 3107441,
m = 66254,
```

but its optimistic correspondence index is

```text
delta = 311808 = 4.706252 * m.
```

Thus its zero-lemma pole bound is already too large before orientation costs.

I later sharpened this with:

```text
p24/low_norm_order3107441_search.md
```

The necessary condition for the zero-lemma window is an ideal representative
of the order-`3107441` class with norm at most `m=66254`, because
`[SL2:Gamma0(N)] > N` for `N>1`.  An exhaustive signed split-prime-power
search using all split rational primes up to `66254` found:

```text
index_66254: none
```

Including the small ramified prime `599` also gave no hits.  Thus the failure
is not an artifact of the earlier squarefree search.

I also checked the closest Atkin-Lehner/Fricke quotient escape in:

```text
p24/atkin_zero_window_boundary.md
p24/atkin_zero_window_search.py
```

Using the optimistic proxy

```text
delta_AL = ceil([SL2:Gamma0(N)] / 2^omega(N)),
```

the scan found no zero-lemma window hits for indices `314`, `422`, or
`66254`.  The closest miss is the index-314 layer:

```text
ell=677
delta_AL=339
needed index=314
```

This does not rule out the Hermitian p-unit/content route, and it does not
rule out a genuinely new embedded period formula.  It does rule out the hope
that the current small split correspondence degrees alone make the relative
vanishing impossible by divisor counting.
