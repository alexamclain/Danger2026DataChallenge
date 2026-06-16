# P25 KSY-y Conductor-39 Degree-6 Value-Descent Packet

Updated: 2026-06-14 14:05 PDT

## Purpose

The conductor-`39` source route is now narrow enough that the value-side
shortcuts can be made explicit.  A theorem cannot simply evaluate the source
with a primitive order-`39` root or a `sqrt(-39)` scalar inside `F_p`.

The viable value theorem must use one of these shapes:

```text
degree-6 cyclotomic orbit + conjugate/norm descent back to F_p
Hilbert-90 or ratio boundary + finite value/divisor identity
```

If the theorem outputs a finite value, it must also carry the period-`156`
branch/root/telescoping context before it can close the source stage.

## Arithmetic

```text
p_order_mod39                         = 6
p^3 = -1 mod 39                       = 1
primitive_39_roots_first_in_degree_6  = 1
sqrt(-39) not in F_p                  = 1
Q satisfies Frob_p(Q)=Q^-1            = 1
W=Q^6 satisfies the same inverse form  = 1
balanced_h90_support                  = 24
sparse_h90_support                    = 12
```

These facts kill the two tempting direct shortcuts:

```text
direct F_p primitive order-39 root  -> reject
sqrt(-39) scalar in F_p             -> reject
```

## Route Rows

```text
direct_fp_order39_root:
  decision = reject_direct_Fp_order39_root_shortcut
  falsifier = ord_39(p)=6, so no primitive order-39 root lies in F_p

sqrt_minus39_scalar:
  decision = reject_sqrt_minus39_scalar_shortcut
  falsifier = (-39/p)=-1

degree6_orbit_no_descent:
  decision = conditional_degree6_orbit_without_descent_to_Fp
  missing  = conjugate/norm descent back to F_p

hilbert90_boundary_no_value:
  decision = helper_only_hilbert90_boundary_value_theorem_missing
  missing  = finite-field value identity or divisor/additive theorem

degree6_norm_descent_bare_value:
  decision = conditional_value_theorem_missing_period156_context
  missing  = period-156 branch/root/telescoping context

degree6_norm_descent_period156_value:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

hilbert90_ratio_period156_value:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing
```

## Counts

```text
route_count                  = 7
rejected_shortcut_rows       = 2
conditional_rows             = 2
helper_only_rows             = 1
source_theorem_closing_rows  = 2
period156_closing_rows       = 2
```

## Interpretation

The p25 moonshot theorem target is sharper than "prove the 75-atom product":

```text
smallest live source = conductor-39 mixed character object
value-side field     = degree-6 cyclotomic orbit or Hilbert-90 ratio boundary
required context     = period 156
remaining boundary   = DANGER3 framing, extraction, official vpp.py
```

This is still a subsqrt route because the finite payloads are tiny.  It is not
a DANGER3 submission until it produces a concrete `(p,A,x0)` triple and passes
the official verifier.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_degree6_value_descent_packet_gate.py
```

Marker:

```text
ksy_y_conductor39_degree6_value_descent_packet_rows=1/1
```
