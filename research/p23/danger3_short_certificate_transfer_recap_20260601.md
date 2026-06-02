# danger3-short-certificate Transfer Recap

Date: 2026-06-01

External repo:

```text
../danger3-short-certificate-experiments
remote = https://github.com/alexamclain/danger3-short-certificate-experiments.git
HEAD = 33a582584ac51d6fc03b5b1cd22dcdab64f3552f
status = clean
```

Main question:

```text
Can any technique from the short-certificate experiments improve the p23
Pomerance triple search for p = 10^23 + 117?
```

## Production-Relevant Transfer

The only production-relevant transfer remains the discriminant class:

```text
split    iff chi(A^2 - 4) =  1
nonsplit iff chi(A^2 - 4) = -1
```

The short-certificate repo uses this as a split-first constant-factor ranking
inside a low-product certificate frontier. For p23, the same mathematical axis
pulls in the opposite operational direction: the high-depth X1(16) search is
best served by a nonsplit filter because the exact `v2 = k = 39` target lives
naturally in the cyclic rational 2-Sylow case.

The exact X1(16) pullback is already recorded in
`notes/x16_split_nonsplit_pullback_proof.md`:

```text
chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2)).
```

Thus the vetted future-shard predicate is:

```text
nonsplit iff chi((y^2 - 2)(y^2 - 4y + 2)) = -1.
```

Latest concordance audit:

```text
./scripts/audit_short_certificate_transfer.py --samples 512

accepted_y = 512
roots_checked = 1024
mismatches = 0
split_roots = 464
nonsplit_roots = 560
status = PASS
```

Operational implication:

```text
Do not restart the active all-X1 shard.
If the active 50B shard misses, launch the guarded y-filtered nonsplit shard.
Keep the nonsplit shard staged and bounded, with fallback/accounting, rather
than treating nonsplit as a complete replacement for all possible p23 hits.
```

## Direct Low-Product Frontier Is Not Viable At p23

The external repo's low-product frontier is excellent for shortening some
current-verifier certificates, but it is not a p23 first-hit method.

Using the repo's sparse-grid null model `lambda ~= 2.571` and the tested
frontier shape:

```text
2 <= x0 <= X
A*x0 <= c*p/log(p)
```

the p23 scale is:

```text
p = 100000000000000000000117
sqrt(p) ~= 3.16227766016e11
log(p) ~= 52.959457
p/lambda ~= 3.89e22 checks for one expected hit in the sparse-grid model
```

For the pp20-like frontier:

```text
X = 64
c = 1.25
candidate_budget ~= 8.836691088734751839703e21
expected_hits ~= 0.227
candidate_budget / sqrt(p) ~= 2.79440708197e10
```

Even an optimistic 2x split-discriminant lift remains far worse than the
current X1(16) p23 route. Therefore:

```text
low-product frontier search = no-go for p23 production
possible use = post-hit certificate minimization only
```

## Fixed-A Inverse Tree / MITM

The external inverse-tree identity is mathematically real:

```text
f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1))
y = x + 1/x
f_A(x) = (y^2 - 4) / (4*(y + A))

f_A(x) = t can be inverted by:
  y = 2*t +/- 2*sqrt(t^2 + A*t + 1)
  x = (y +/- sqrt(y^2 - 4))/2
```

For fixed `A`, this enumerates or intersects valid `x0` values. For p23, it
does not choose rare trace-compatible `A`, which is the hard part. In the local
X1(16) setting it mostly recovers the same inverse-doubling formula already
used by successive halving.

Local diagnostics:

```text
inverse-gate branch selector:
  mathematically correct
  no p23 survival lift over natural first branch
  adds Legendre work
  production verdict = no-go

bounded lookahead:
  depth-2 lookahead captured most all-branch lift at depth 12/14
  cost was about 2.1x half calls for about 1.24x-1.38x survival lift
  production verdict = no-go unless compressed into a much cheaper feature
```

Research-only next tests:

```text
compressed child-mass or tower-section feature:
  gate = recover >=80% of lookahead lift with <=1.2x half-call cost

volcano/orientation label:
  gate = survivor/sec beats y-filtered nonsplit on paired p23 holdout

higher X1(2^n) or X0(32):
  gate = depth-12/14 survivor/sec beats y-filtered nonsplit, not merely
         accepted-trial hazard
```

## Rejected Transfers

```text
Legendre(x0^2 + A*x0 + 1, p):
  duplicates the first halving radicand gate already paid by the halving loop

quartic refinement of the nonsplit y-character:
  diagnostics did not show enough retained deep-survival signal

simple residue-class sieves:
  external held-out tests rejected them; local y-feature scans also weak

naive SEA / Atkin trace filters:
  exact ell=3 C benchmark was much too slow for the rejection obtained;
  no odd-prime trace y-pullback was found beyond unstable enrichment features

CM exact-trace construction:
  target discriminants have conductor 4 and huge fundamental parts near 1e22
```

## Current Production Policy

```text
1. Continue active all-X1(16) x16halve shard.
2. If a Verified: PASS appears, finalize and verify immediately.
3. If the active 50B budget completes with no hit, launch the guarded
   y-filtered nonsplit X1(16) shard.
4. Keep all other short-certificate repo ideas as diagnostics or post-hit
   certificate-minimization tools, not production replacements.
```

## Link Recheck During Live Run

The linked GitHub repo was rechecked while the p23 shard was active:

```text
GitHub URL:
  https://github.com/alexamclain/danger3-short-certificate-experiments

local clone:
  ../danger3-short-certificate-experiments

remote HEAD:
  33a582584ac51d6fc03b5b1cd22dcdab64f3552f

local HEAD:
  33a582584ac51d6fc03b5b1cd22dcdab64f3552f

local status:
  clean
```

The fresh scaling calculation using the external repo's sparse-grid model
`lambda = 2.571` gives:

```text
p = 100000000000000000000117
sqrt_floor = 316227766016
log(p) = 52.95945713886305
p/lambda ~= 3.8895e22

X = 32, c = 1.00:
  candidates = 5775163418720384728397
  expected_hits = 0.148479
  hit_probability = 0.137982
  candidates / sqrt(p) ~= 1.826e10

X = 64, c = 1.25:
  candidates = 8836691088734751839703
  expected_hits = 0.227191
  hit_probability = 0.203232
  candidates / sqrt(p) ~= 2.794e10

X = 64, c = 5.50:
  candidates = 38881440790432906524312
  expected_hits = 0.999642
  hit_probability = 0.631989
  candidates / sqrt(p) ~= 1.230e11
```

Fresh application verdict:

```text
The repo contributes one production-relevant axis, Legendre(A^2 - 4, p).
For its low-product short-certificate frontier the useful direction is split.
For the p23 X1(16) deep-halving search the useful direction is nonsplit.

The low-product scan, split-first frontier order, inverse MITM, and
Legendre(x0^2 + A*x0 + 1, p) add-on do not replace the current p23 production
strategy. The last of these is the same first halving radicand already tested
locally by inverse-gate diagnostics.
```

## Subagent Consensus

Six first-wave read-only subagents, two second-wave read-only subagents, and
four fresh linked-repo recheck subagents checked independent transfer angles:

```text
broad transfer audit
split/nonsplit character audit
fixed-A inverse-tree/MITM audit
low-product frontier scaling audit
literature-style technique audit
implementation/policy audit
odd-prime trace-congruence pullback audit
tower-section/branch-selector audit
fresh low-product frontier p23 scaling audit
fresh split/inverse-tree algebra transfer audit
fresh search-order/MITM/residue leftover audit
fresh post-hit short-certificate minimization audit
```

Consensus:

```text
1. The discriminant axis is the only production-relevant transfer from the
   external repo, and it is already operationalized as y-filtered nonsplit
   X1(16).

2. Direct low-product frontier search is not p23-viable.

3. Fixed-A inverse trees are formula-valid but do not solve rare target-trace A
   selection at p23 scale.

4. No cheap odd-prime SEA/Atkin trace congruence predicate was found.

5. No compressed tower-section branch rule currently beats the nonsplit
   fallback in effective production terms.

6. The next operational action remains unchanged:
   keep the active all-X1(16) shard running; if it misses 50B, launch the
   guarded y-filtered nonsplit X1(16) shard.

7. After a p23 hit, the external repo's low-product machinery can be treated as
   an optional certificate-prettifying/minimization side quest, not as a path to
   the first hit. The p23-scale frontier budgets are far too large for a
   production discovery run.
```
