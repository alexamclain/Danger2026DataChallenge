# P25 KSY-y Conductor-39 Expert-Query Packet

Updated: 2026-06-14 14:11 PDT

## Purpose

This is the compact packet for expert conversations at the current p25
subsqrt moonshot frontier.  It turns the conductor-`39` route into exact
questions whose answers can be routed through local gates.

The live source is:

```text
U_chi = -chi_3 * chi_13 on X_1(39)
W = 6 * U_chi
Norm_156(Y_507) = distribution_lift_39_to_507(W)
```

## Arithmetic Boundary

```text
p_order_mod39                   = 6
p^3 = -1 mod 39                 = 1
sqrt(-39) in F_p                = 0
gcd(4^156 - 1, p - 1)           = 1
gcd(4^780 - 1, p - 1)           = 11
count_ladder                    = 75 -> 300 -> 12 -> 312 -> 156
max_current_budget              = 46800
max_current_budget < sqrt(p)    = 1
```

So the live source is compact, but the direct `F_p` shortcuts are dead.

## Four Source-Closing Yes Shapes

### 1. Conductor-39 Value Or Divisor Identity

Question:

```text
Is there a finite-field value identity or divisor/additive identity for
U_chi=-chi_3*chi_13, W=6*U_chi, or
Norm_156(Y_507)=distribution_lift_39_to_507(W)?
```

Advances if it preserves the mixed tensor, includes the Yang `13`-fiber lift,
and supplies period-`156` context for value outputs.

Expected local decision:

```text
source_theorem_closed_policy_or_framing_missing
```

### 2. Degree-6 Cyclotomic Norm Descent

Question:

```text
If the identity naturally lives over F_{p^6}, does it give a conjugate
product, norm, trace, or Hilbert-90 descent back to F_p?
```

Advances only with explicit descent to `F_p` and period-`156` branch context
for values.  A degree-6 computation by itself is not enough.

### 3. Hilbert-90 / H0 Ratio Identity

Question:

```text
Is there a Hilbert-90 or ratio theorem evaluating canonical H0 or a legal
<2>-translate with (1-Frob_p)H0 = Norm_156(Y_507)?
```

Advances if the theorem supplies a legal sparse Yang-fiber `H0`, the exact
boundary to `Norm_156(Y_507)`, and a finite value/divisor identity.

### 4. Period-156 Branch Control

Question:

```text
For any value theorem, is the branch fixed at support period 156 rather than
the ambient period 780?
```

This matters because period `156` gives a unique `F_p^*` branch, while ambient
period `780` leaves a `mu_11` ambiguity.

## Two Downstream Questions

```text
DANGER3 policy/framing:
  Would DANGER3 accept the result as a concrete finite-field identity?
  A yes unblocks framing but still needs extraction and vpp.py.

X_1(8112) / X_1(16) extraction:
  Can the odd-level Y_507/H0/U_chi theorem emit A, xP16, and a halving chain?
  A yes still needs a concrete x0 and official vpp.py verification.
```

## Three Guardrails

```text
direct F_p primitive order-39 root:
  reject; ord_39(p)=6

sqrt(-39) scalar in F_p:
  reject; (-39/p)=-1

ray-class generator, C169 projection, or prime-axis theorem only:
  reject/upstream; it loses the mixed chi_3 tensor chi_13 source
```

## Submission Boundary

Only this is submission-ready:

```text
concrete p25 (p,A,x0) triple verified by official DANGER3 vpp.py
```

Everything else, even a source-closing theorem, remains upstream of DANGER3
framing, extraction, and verifier success.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_expert_query_packet_gate.py
```

Marker:

```text
ksy_y_conductor39_expert_query_packet_rows=1/1
```
