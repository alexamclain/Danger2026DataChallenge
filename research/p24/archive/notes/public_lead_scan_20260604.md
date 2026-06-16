# Public Lead Scan For p24

Date: 2026-06-04 PDT

Target:

```text
p = 1000000000000000000000007 = 10^24 + 7
strict DANGER3 verifier target: Montgomery (p, A, x0) with x-only depth 2^40
```

Queries checked locally and publicly:

- local repo exact/fuzzy `rg`: `1000000000000000000000007`, `10^24+7`, `DANGER3`, `Pomerance`, `vpp.py`
- sibling local repo `/Users/agent/Documents/Codex/danger3-short-certificate-experiments` with the same terms
- GitHub connector code search for exact p24 constant and DANGER3/Pomerance terms
- GitHub connector branch/issue/commit search in:
  - `AndrewVSutherland/DANGER3`
  - `alexamclain/Danger2026DataChallenge`
  - `ruehlef/Danger2026DataChallenge`
- web search for exact p24 constant plus `DANGER3`, `Pomerance`, and `vpp.py`

Evidence found:

- Official DANGER3 README currently lists p22 and p23 successes, then asks for a triple for `p=10^24+7`; no p24 certificate is posted there.
  - https://github.com/AndrewVSutherland/DANGER3
- Public Alexa fork records p22 and p23 verified triples and explicitly describes the p23 method as a constant-factor fixed-prime win, not an asymptotic sub-sqrt proof.
  - https://github.com/alexamclain/Danger2026DataChallenge
- The public p23 pull request to Ruehle's fork contains the same `X1(16)`
  nonsplit result, not a p24 certificate.
  - https://github.com/ruehlef/Danger2026DataChallenge/pull/1
- Public short-certificate repo records low-product, split-discriminant, and inverse-tree heuristics for shorter current-verifier witnesses in small bundled slices.  Its own README says these are not closed-form, not asymptotic, and not evidence for the large p22 search method.
  - https://github.com/alexamclain/danger3-short-certificate-experiments
- Ruehle fork documents the original 2-Sylow projection search, including that it reduces to about sqrt(p) trials and does not achieve the requested sqrt-scaling beat.
  - https://github.com/ruehlef/Danger2026DataChallenge
- Exact p24 web hits outside the challenge context are primality/sequence references only, not DANGER3 certificates.
  - https://oeis.org/A159031/internal

Strict verifier status:

No public/current strict verifier-compatible p24 triple or asymptotic construction was found in this scan.  The useful leads found are already incorporated locally as constant-factor or post-trace/inverse-tree diagnostics; none supplies the missing target-trace `A` selector for p24.

Follow-up public sidecar:

```text
exact challenge/repo/integer searches on GitHub and the public web found no
p24 certificate text, no p24 issue/commit/PR hit, and no current fixed-prime
prescribed-high-2-power-torsion algorithm that changes the strict exponent.
The strongest public practical lead remains the p23 X1(16) nonsplit/halving
method, which is still explicitly a constant-factor method.
```
