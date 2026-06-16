# P25 KSY-y Post-Minimality Active Router

Updated: 2026-06-14 11:15 PDT

## Purpose

After the conductor-`39` doubling-orbit minimality checkpoint, the moonshot
has two live theorem-facing doors that need to be coordinated:

```text
global primary: full 12-step conductor-39 orbit norm plus Yang 13-fiber lift
active companion: Kubert-Lang / KSY exact mixed 75-atom product
```

This router prevents drift between the post-conductor-`39` queue and the
post-Sprang exact-product queue.

## Active Routes

```text
1. conductor39_full_doubling_orbit_norm
   role      = primary front door
   continue  = theorem emits Q=prod_i [2]^i(E_7/E_1), equivalently U_chi,
               then W=6*U_chi and Yang's 13-fiber lift
   reject    = seed ratio alone, proper suborbit, conductor-3/13 projection,
               additive separation, or level-507 story without the lift

2. conductor39_period156_hilbert90_descent
   role      = follow-on front door
   continue  = value/divisor theorem for the conductor-39 source with ratio,
               twisted trace, Hilbert-90 boundary, or legal support-156 sparse
               Yang-lift potential; current normal form is the canonical
               78-over-78 Yang-fiber product, up to <2>-translate, with
               period-156 context
   reject    = bare value, naive degree-6 norm, or ambient period-780 branch

3. kubert_lang_ksy_exact_mixed_product
   role      = active companion front door
   continue  = exact row-labeled pairs, reflection center, or raw equal-weight
               75-atom K-traced anti-invariant normalized-y product
   reject    = C169 projection, KL hygiene, generation, single y-value,
               nonuniform atom weights, or missing mixed graph

4. sprang_exact_specialization_hit
   role      = watchlist only
   continue  = new named exact mixed row-labeled theorem/formula hit

5. koo_shin_2010_root_descent_helper
   role      = helper only after an independent mixed producer exists

6. projection_hygiene_generation_shadows
   role      = killed shadow
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_minimality_active_router_gate.py
```

Expected marker:

```text
ksy_y_post_minimality_active_router_rows=1/1
```
