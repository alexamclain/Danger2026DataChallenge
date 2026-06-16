# Conductor-2 Nonsplit Gate

This is a sharpened local theorem candidate for the strict p24 traces.

## Statement

Let `p == 7 mod 8`, let `u` be the actual trace of an ordinary elliptic curve
`E/F_p` with `u == 0 mod 8`, and suppose

```text
u^2 - 4p = 4D
```

with `D < 0` a fundamental discriminant, so `D == 1 mod 8`.  This excludes
the supersingular edge `p=7, u=0`.  Put `K = Q(sqrt(D))`, `O = O_K`,
`O_2 = Z + 2O`, and

```text
pi = u/2 + sqrt(D).
```

Then `Z[pi] = O_2`.  In this ordinary isogeny class there are only two
possible endomorphism rings:

```text
O              maximal order
O_2            Frobenius/conductor-2 order.
```

The intrinsic gate is:

```text
End(E) = O       iff  dim_F2 E[2](F_p) = 2
End(E) = O_2     iff  dim_F2 E[2](F_p) = 1
```

For any nonsingular Montgomery model `B*y^2 = x^3 + A*x^2 + x`, this becomes

```text
A^2 - 4 is a square     split
A^2 - 4 is a nonsquare  nonsplit.
```

## Proof Sketch

The finite group lemma is:

```text
Frobenius acts trivially on E[2]  iff  pi - 1 is in 2*End(E).
```

This uses that `[2]` is separable: an endomorphism kills `E[2]` exactly when it
factors through `[2]`.

Now write `omega = (1 + sqrt(D))/2`, so `sqrt(D) = 2omega - 1`.  Since
`u == 0 mod 8`,

```text
pi - 1 = u/2 - 1 + sqrt(D)
       = 2 * (omega + u/4 - 1).
```

The factor `omega + u/4 - 1` lies in `O` but not in `O_2`, because its
`omega` coefficient is odd.

Thus:

```text
pi - 1 in 2O
pi - 1 not in 2O_2.
```

If `End(E)=O`, Frobenius is the identity on `E[2]`, so all three nonzero
2-torsion points are rational.  If `End(E)=O_2`, Frobenius has characteristic
polynomial `(X-1)^2 mod 2` but is not the identity on `E[2]`; it is the
nontrivial unipotent element, so its fixed space has dimension one.

That proves the split/nonsplit separation.

Replacing `u` by `-u`, or conjugating `pi`, gives the same divisibility
conclusion.  No special `j=0` or `j=1728` exception is needed under these
ordinary hypotheses because those CM fields are incompatible with
`D == 1 mod 8`.

## Scan Evidence

I added:

```text
p24/conductor2_nonsplit_gate_scan.py
p24/fixed_trace_nonsplit_component_identity_scan.py
```

Bounded run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/conductor2_nonsplit_gate_scan.py --max-p 800 --max-h 40 --max-rows 30
```

Output summary:

```text
tested_rows=30
failures=0
all_gate_ok=1
```

Every scanned row had the same shape:

```text
maximal_nonsplit=0
conductor2_split=0
other=0
```

and the counts matched the expected bounded-degree Montgomery projection:
maximal roots have four split `A`-preimages per `j`, conductor-2 roots have
two nonsplit `A`-preimages per `j` in the generic rows.

The scan deliberately starts at `t=8`, so it does not test the supersingular
edge `p=7, t=0`.  It classifies endomorphism rings by the roots of `H_D` and
`H_{4D}` rather than independently computing endomorphism rings; under the
ordinary hypotheses above, that is the intended test.

The fixed-field version of the same statement is:

```text
S_ns(t) = { j(A) : trace(E_A) = +/-t and A^2-4 is nonsquare }
        = roots(H_{4D} mod p).
```

The component identity scan verifies this and then checks that restricting
`Phi_ell` to `S_ns(t)` gives the same component sums as restricting it to
`H_{4D}` roots:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/fixed_trace_nonsplit_component_identity_scan.py \
  --max-p 800 --max-h 40 --max-ell 17 --max-component-size 6 --max-rows 20
```

Output summary:

```text
rows=20
root_set_failures=0
component_failures=0
all_passed=1
```

This is a positive identity, not a construction shortcut: enumerating
`S_ns(t)` by scanning Montgomery `A` is still trace-bucket scale.

## p24 2-Adic Consequence

I also added:

```text
p24/p24_split_2adic_branch_audit.py
```

It computes the two split-prime valuations of `pi-1` on the maximal branch:

```text
trace             v2(#E)   split valuations   split exponent
1020608380936     42       (1, 41)            41
-78903246840      40       (1, 39)            39
-1178414874616    41       (1, 40)            40
```

The conductor-2/nonsplit branch has cyclic rational 2-Sylow, so its x-only
exponent keeps the full displayed `v2(#E)`.  The split maximal branch loses the
small valuation branch and has exponent equal to the larger valuation.

For the current best third trace, the maximal branch still reaches the
verifier depth `k=40`, while the conductor-2 branch reaches `41`.  For the
middle trace, the maximal branch would miss `k=40`, but the conductor-2 branch
would pass.

## Impact on the Missing Theorem

The embedded component-sum theorem should be stated for the Frobenius-order
roots `H_{4D}` or should include this nonsplit gate after a fixed-trace root is
constructed.  This is not itself the asymptotic speedup: for p24 the
conductor-2 ring-class multiplier is `1`, so the class number and non-genus
phase problem remain the same scale.

More precisely, the standard ring-class exact sequence gives

```text
1 -> (O_K / 2O_K)^* / (Z/2Z)^* image -> Pic(Z+2O_K) -> Pic(O_K) -> 1.
```

Since `D == 1 mod 8`, the prime `2` splits and

```text
#kernel = 2 * (1 - (D/2)/2) = 1.
```

Thus `Pic(Z+2O_K) -> Pic(O_K)` is an isomorphism.  Odd ideals, including the
split-prime ideals used in the `ell=677` route, keep their class orders under
extension/contraction.  The component quotient can therefore be transported to
the conductor-2/nonsplit branch without changing the degrees:

```text
G / <677>   degree 314
<677> / H   degree 211
H           recovery degree 3107441
```

The third p24 trace check gives the same exact data on both sides:

```text
D_K = -652834595820939249713143
h(D_K) = h(4D_K) = 205880396014
Pic invariant factors: (205880396014,) for both orders
ord_D([677]) = ord_4D([677]) = 655670051
index = 314
```

The caveat is that this is an abstract Picard-group identification.  It does
not select an embedded root or produce the `314` component sums over `F_p`;
that remains the missing non-genus class-field identity.

It does remove one ambiguity.  Fixed-trace conductor-2 roots are not junk
introduced by an overbroad filter; they are the natural nonsplit Montgomery
branch for the x-only certificate.
