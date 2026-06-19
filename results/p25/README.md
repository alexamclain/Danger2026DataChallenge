# DANGER3 p25 Result

This directory records a verified Pomerance triple found for

```text
p  = 10000000000000000000000013
A  = 5863342488035851054212447
x0 = 9636258147581954669181726
```

The result was found by an Alexa-run, Codex-assisted experimental search using
Sutherland `X1(16)` prescribed torsion, a y-level nonsplit Montgomery
discriminant filter, and first-branch successive halving in the cyclic
nonsplit rational 2-Sylow case.

The successful 10-worker `x16halvenonsplit` run found the triple after about
196.34B aggregate accepted trials. Including the earlier 266.467B partial
no-hit chunk, the full p25 practical campaign used about 462.81B accepted
trials.

The core practical technique did not materially change from the p24/p23
`X1(16)` nonsplit route. For p25, `p mod 8 = 5`, so the p24 square-root patch
for `p mod 8 = 7` was not needed.

Files:

- `triple.txt`: one-line triple for DANGER3 `vpp.py`.
- `p25-success-summary.txt`: compact run summary and provenance.
- `p25-verification.txt`: verifier, primality, and independent doubling replay output.
- `p25-worker08-tail.txt`: final tail of the successful worker log.
- `pomerance_10000000000000000000000013.lean`: generated Lean certificate file; included for convenience.
