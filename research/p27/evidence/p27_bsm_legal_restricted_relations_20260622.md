# P27 BSM Legal-Restricted Relation Screen

Date: 2026-06-22

## Claim

Restricting the BSM surface to legal `B` values is still not enough to expose a
cheap source selector for canonical d3-plus rows.

The legal-B-restricted surface keeps the useful staging equation

```text
m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)
```

but the target rows do not satisfy an additional low-degree relation in the
screened coordinates.  Across q1607/q1847/q2087, every tested pair system has
`target_minus_legal_extra=0` through total degree `12`, and the triple system
`(B,s,m)` has exactly the inherited degree-4 BSM relation on both the full
legal surface and the target subset.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_bsm_legal_restricted_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_bsm_legal_restricted_relation_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_bsm_legal_restricted_relation_probe_q1607_q1847_q2087_deg12_pair_deg4_triple_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_bsm_legal_restricted_relation_probe.py \
  --small-primes 607 \
  --pair-degrees 2,4 \
  --triple-degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_bsm_legal_restricted_relation_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_bsm_legal_restricted_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --pair-degrees 2,4,6,8,10,12 \
  --triple-degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_bsm_legal_restricted_relation_probe_q1607_q1847_q2087_deg12_pair_deg4_triple_20260622.txt
```

## Results

Legal-B-restricted surface sizes:

```text
q1607: legal_B = 49, legal_surface_rows = 77368, target_rows = 896
q1847: legal_B = 63, legal_surface_rows = 116872, target_rows = 1440
q2087: legal_B = 57, legal_surface_rows = 119224, target_rows = 800
```

The target fibers are small and uniform once canonical legal rows are already
present:

```text
q1607: target_rows_per_B_32 = 28
q1847: target_rows_per_B_32 = 45
q2087: target_rows_per_B_32 = 25
```

Pair relation screens:

```text
systems = (B,s), (B,m), (s,m)
degrees = 2,4,6,8,10,12
fields = q1607, q1847, q2087
result = target_minus_legal_extra is always 0
```

Triple relation screen:

```text
system = (B,s,m)
degrees = 2,4
fields = q1607, q1847, q2087
degree 2: legal_extra = 0, target_extra = 0
degree 4: legal_extra = 1, target_extra = 1, target_minus_legal_extra = 0
```

The degree-4 triple relation is the BSM surface equation itself.  It does not
separate the canonical d3-plus target rows from the legal-B-restricted surface.

## Interpretation

Positive:

```text
The BSM surface remains a compact CAS coordinate after imposing legal B.
The canonical d3-plus target subset is cleanly visible inside that surface.
The target fiber over each target B is uniform at 32 rows in the guard fields.
```

Negative:

```text
No screened low-degree relation selects target rows beyond the BSM equation.
Legal B is still the sparse source denominator.
The BSM surface plus legal-B restriction is not a GPU sampler or bucket law.
```

So this branch should not be promoted to a production GPU run.  The next
useful math step is actual legal-cover normalization or the next Kummer
selector on top of this staged surface, not more low-degree relation scans in
the same `(B,s,m)` coordinates.

Update: the next-selector version of this test is also negative:
[P27 BSM Next-Selector Relation Screen](p27_bsm_next_selector_relation_20260622.md).
It tests `d4+` after `d3+` in `(B,s)`, `(B,m)`, `(s,m)`, and `(B,s,m)`.
Across q1607/q1847/q2087, `d4plus_minus_d3` is always zero in the screened
pair systems through degree `12`, and the degree-4 triple relation is again
only the inherited BSM equation shared by legal, `d3+`, `d4+`, and `d4-`.
Thus the BSM surface does not visibly couple two selected gates.

## Continue / Kill

```text
continue = legal B-cover/function-field normalization over the BSM surface
continue = next Kummer selector after imposing the legal cover
continue = use BSM as a handoff equation for CAS/expert review

kill = GPU sampling of legal-B-restricted BSM without a legal-B source
kill = low-degree relation scans in (B,s), (B,m), (s,m), or (B,s,m)
kill = treating the inherited degree-4 BSM equation as a target selector
kill = BSM next-selector low-degree relation for d4+ in the screened coordinates
```

```text
p27_bsm_legal_restricted_relations_rows=1/1
```
