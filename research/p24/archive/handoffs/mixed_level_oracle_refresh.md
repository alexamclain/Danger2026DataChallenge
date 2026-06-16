# Mixed-Level Oracle Refresh

This note records a wider rerun of the mixed odd/2-adic reverse-SEA idea.

## Question

Can one combine a shallower 2-adic condition with odd trace residues or mixed
torsion divisors to isolate the six strict p24 traces at modular cost below
the square-root scale?

The optimistic model is deliberately generous:

```text
1. exact trace residues modulo the chosen level are granted as an oracle;
2. cost is priced only by Gamma0 index, not by the richer marked/eigenvalue
   data a constructive method would actually need;
3. residual Hasse-trace survivors are charged linearly.
```

If even this model stays at constant times `sqrt(p)`, then mixed levels do
not give an asymptotic route.

## Reruns

```text
python3 p24/mixed_crt_trace_residue_optimizer.py \
  --prime-bound 97 --max-odd-part 200000 --min-depth 24 --max-depth 42 --top 20

python3 p24/reverse_sea_level_tradeoff_audit.py \
  --depths 22 24 26 28 30 32 34 36 38 40 \
  --max-ell 1000 --max-steps 16 --max-initial-count 1000000

python3 p24/mixed_level_index_audit.py
python3 p24/mixed_torsion_divisor_audit.py
```

## Output

The wider CRT optimizer tested `80940` levels.  The best proxy remained pure
`2^40`:

```text
depth=40
odd_part=1
level=1099511627776
target_residue_count=2
survivors=6
gamma0_over_sqrt=1.649267
proxy_over_sqrt=1.649267
```

Odd levels can isolate the strict traces from shallower 2-adic prefixes, but
their Gamma0 proxy is larger:

```text
depth=36, ell=71: gamma0/sqrt=7.421703
depth=38, ell=23: gamma0/sqrt=9.895605
```

The reverse-SEA lower-bound column explains why.  On a fixed 2-adic branch,
trace residues repeat unless the odd modulus exceeds the branch distance to a
boundary.  The optimistic Gamma0 lower bound stays at several `sqrt(p)` for
shallower prefixes:

```text
depth=24: gamma0_lower/sqrt=4.767640
depth=32: gamma0_lower/sqrt=4.773856
depth=36: gamma0_lower/sqrt=4.844723
depth=38: gamma0_lower/sqrt=4.947802
```

The mixed divisor audit agrees.  Among divisors of target orders above
`sqrt(p)`, the cheapest largest-prime-factor choice is the pure `2^40`
divisor; odd alternatives introduce large levels.

## Boundary

Mixed odd levels are useful as exact trace-residue bookkeeping, but not as an
asymptotic selector.  In every tested optimistic model they either:

```text
1. keep the pure 2^40/Gamma0 scale;
2. add odd-level index that outweighs the shallower 2-adic prefix; or
3. require richer marked/eigenvalue data closer to Gamma1, which is much worse.
```

This closes the current mixed-level branch unless a new construction supplies
odd trace residues at much lower cost than their modular level index.
