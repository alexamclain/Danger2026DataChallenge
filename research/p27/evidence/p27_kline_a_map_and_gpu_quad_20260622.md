# P27 K/A Map And GPU Quadratic-Gate Update

Date: 2026-06-22

## Claim

The selected K/Sroot-to-A graph is governed by an exact low-degree source
identity, and the GPU quadratic-gate probe confirms the recurrence formula at
scale.  Together they clarify the current frontier:

```text
confirmed = explicit first-half / d2 source geometry and exact quadratic tower gate
not yet = source-normalized shrink below sqrt(p)
next = legal pullback / quotient sampler, or a gate-coupling law across many gates
```

## CPU Artifacts

Relation screen:

```text
research/p27/archive/gates/p27_kline_a_map_relation_probe.py
research/p27/archive/probe_outputs/p27_kline_a_map_relation_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_kline_a_map_relation_probe_q1607_q1847_q2087_deg16_20260621.txt
research/p27/archive/probe_outputs/p27_kline_a_map_relation_probe_p27_sample_deg16_20260621.txt
```

Relation extraction:

```text
research/p27/archive/gates/p27_kline_a_map_relation_extract.py
research/p27/archive/probe_outputs/p27_kline_a_map_relation_extract_p27_train_heldout_20260621.txt
```

Formula verification:

```text
research/p27/archive/gates/p27_kline_a_map_formula_verify.py
research/p27/archive/probe_outputs/p27_kline_a_map_formula_verify_p27_guard_20260621.txt
```

## Exact K/A Identity

Let `K=x([2]P)` on `E': V^2=U^3+4U` and set `L=K^2`.  The p27 train sample
found a degree-8 `(K,A)` relation with `3` extra nullity; an independent p27
heldout sample had `0` mismatches on all extracted basis relations.

One normalized relation is:

```text
64(A-2)^2(A+2)L^2
+64(A+2)(A+14)(3A+10)L
-(A-2)^4 = 0,

where L = K^2.
```

Equivalently:

```text
-A^4 + 8A^3 - 24A^2 + 32A - 16
+ (192A^3 + 3712A^2 + 15616A + 17920)K^2
+ (64A^3 - 128A^2 - 256A + 512)K^4 = 0.
```

The `Sroot` relation is the same identity after `K=Sroot^2`.  Its first
appearance is at degree `12` in `(Sroot,A)`.

The discriminant in `L` is:

```text
256(A+2)(A+6)^2(A^2+60A+132)^2.
```

So the identity is a very clean first-half source relation after adjoining
`sqrt(A+2)`.  This explains why the K/Sroot fiber profile was perfectly flat.

## Not A D3 Selector

The formula verifier tested whether this identity classifies the next selected
gate among all `d2`-plus candidates.  It does not: the formula vanishes on both
`d3`-plus and `d3`-minus candidates.

Representative p27 heldout counts:

```text
d2_plus = 4000
d3_plus = 2104
d3_minus = 1896
d3_plus_K_zero_1 = 2104
d3_minus_K_zero_1 = 1896
K_classifier_mismatch = 1896
```

Guard fields show the same pattern:

```text
q607:  d3_plus=256, d3_minus=256, formula zero on both
q1607: d3_plus=448, d3_minus=336, formula zero on both
q1847: d3_plus=720, d3_minus=288, formula zero on both
q2087: d3_plus=400, d3_minus=512, formula zero on both
```

Thus the identity is not the missing d3 half-loss.  It is the algebraic base
curve over which the next d3 double cover must be understood.

## GPU Quadratic-Gate Result

External GPU branch:

```text
alexamclain/Danger2026DataChallenge branch codex/add-cuda-p26-search
commit e153fd1 Add p27 quadratic gate GPU probe
```

Local result note:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/results/p27/gpu_quad_20260622T005716Z/README.md
```

Headline result:

```text
checked gates = 7,874,715
gates = 3..8
mismatches = 0
unavailable formula rows after recurrence-coordinate domain = 0
```

The tested recurrence formula was:

```text
A = 2 - c^2
x = r^2
next_gate = chi(r^2 + c*r + 1)
```

The recurrence-coordinate domain is about half of the wider post-d2 prefix
scope:

```text
domain fraction ~= 0.5
conditional depth-13 survivor rate ~= 2x wider post-d2 baseline
target survivors per raw source draw ~= flat or slightly lower
```

So the GPU confirms exactness and real conditional enrichment, but not a
production speedup or below-sqrt source.

## Interpretation

Positive:

```text
The first-half K/A relation is explicit and factorable.
Sroot is the right clean coordinate for the base source.
The quadratic recurrence gate is exact at multi-million-gate GPU scale.
```

Negative for the moonshot:

```text
P(K,A)=0 is a d2/base-source identity, not a d3 selector.
The GPU quadratic precheck finds a half-size domain and doubles conditional
survival, but source-normalized target rate remains flat.
```

This is now a better-shaped problem.  The sqrt-beating target is not another
one-bit precheck.  It is:

```text
1. a direct sampler into the legal recurrence-coordinate domain without paying
   the discovery toll, or
2. a relation coupling many signs chi(r_j^2+c*r_j+1) so the tower does not
   lose an independent factor 2 at every gate.
```

## Continue / Kill

```text
continue = normalize the d3 cover over the explicit K/A base curve
continue = work over P1_Sroot and treat K as the quotient check
continue = search for gate-coupling law across chi(r_j^2+c*r_j+1)
continue = GPU only for legal-pullback sampler telemetry or recurrence coupling

kill = treating P(K,A)=0 as the d3 selector
kill = larger GPU production run from this formula alone
kill = K/Sroot bucket searches without a new quotient or recurrence
kill = fixed-prefix quadratic precheck as sqrt-beating evidence
```

```text
p27_kline_a_map_and_gpu_quad_rows=1/1
```
