# First-Trace Order-19 Certificate Spec

Date: 2026-06-05

This note records the simplest non-genus p24 certificate surface found so
far.  It uses the first strict trace rather than the more balanced third
trace.

## Target

```text
p = 10^24 + 7
t = 1020608380936
order discriminant Delta = t^2 - 4p
  = -2958358532763196711763932
fundamental D_K = -739589633190799177940983
conductor = 2
h = 278733727154 = 2 * 19 * 7335098083
sqrt(p) = 1000000000000
```

The strict DANGER condition accepts this trace or its twist sign; the
post-root projection is the same cheap step recorded in:

```text
p24/post_cm_root_projection_boundary.md
```

## Order-19 Quotient

The split prime:

```text
ell = 19
```

has class order:

```text
order([ell]) = h / 19 = 14670196166
index([ell]) = 19.
```

Since:

```text
p mod 19 = -1
ord_19(p) = 2,
```

the root-of-unity side for order-19 relative characters is only quadratic.
The hard part is embedded CM phase, not adjoining `mu_19`.

Let `G = Cl(O_Delta)` and let `a` be the class of a prime above `19`.
The quotient periods are:

```text
Y_i = sum_{k=0}^{14670196165} j_{i + 19*k},
      i mod 19
```

after choosing the embedded `a`-cycle orientation.  The quotient polynomial is:

```text
Q_19(Y) = product_{i=0}^{18} (Y - Y_i).
```

For one selected quotient root `Y_0`, the recovery polynomial is:

```text
R_0(J) = product_{k=0}^{14670196165} (J - j_{0 + 19*k}).
```

## Finite Certificate Payload

The explicit quotient/recovery certificate can carry:

```text
1. Q_19(Y), degree 19;
2. one selected recovery polynomial R_0(J), degree 14670196166;
3. roots Y_0, J_0;
4. a nonsingular Montgomery A above J_0;
5. an x0 produced by odd-part projection.
```

Coefficient count, excluding monic leading coefficients:

```text
19 + 14670196166 = 14670196185
14670196185 / sqrt(p) = 0.014670196185.
```

This is much larger than the third-trace norm-compressed scalar surface, but
it is still asymptotically below the `sqrt(p)` yardstick for this p24 target.

The generic finite implication is Lean-gated in:

```text
p24/lean/QuotientRecoveryCertificateGate.lean
```

## Producer Soundness Theorem

The certificate is only valid if the producer theorem proves the quotient and
recovery objects are embedded and paired with the actual conductor-2 CM
torsor:

```text
Q_19 is the quotient-period polynomial for the order-19 quotient;
R_0 is the recovery fiber above the supplied quotient root Y_0;
J_0 is a root of R_0;
J_0 is on the strict trace t = 1020608380936 branch.
```

This is exactly the missing non-genus phase problem.  Abstract degree-19
class-field equations are not enough unless their roots are paired with the
embedded `j` recovery fibers.

## Why This Route Matters

The third trace remains the best balanced target:

```text
quotient degree = 66254
recovery degree = 3107441
formal ratio = 3.17e-6 * sqrt(p).
```

But the first trace is a cleaner theorem experiment:

```text
single non-genus quotient degree = 19
single recovery degree = 14670196166.
```

So it isolates the core missing theorem:

```text
Can one compute embedded quotient periods for a small non-genus quotient
without enumerating the CM class set?
```

Small `ell=index` analogues were tested in:

```text
p24/norm_equals_index_local_phi_toy.py
p24/quotient_period_low_degree_feature_audit.py
p24/all_trace_period_frontier.md
```

They do not reveal a local formula from `Phi_ell` data.  Linear formulas fail,
degree `<= 3` low-degree feature formulas fail on larger small examples, and
degree `4` only appears once the feature matrix has full row rank.  So this
surface still needs a genuine class-field/period identity.  But it is the
smallest visible non-genus quotient surface for p24.
