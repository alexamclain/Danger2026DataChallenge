# DANGER3 p23 Result

This directory records a verified Pomerance triple found for

```text
p  = 100000000000000000000117
A  = 24163028207499560363686
x0 = 64911014007772963770218
```

The result was found by an Alexa-run, Codex-assisted experimental search using
Sutherland `X1(16)` prescribed torsion, a y-level nonsplit Montgomery
discriminant filter, and first-branch successive halving in the cyclic
nonsplit rational 2-Sylow case.

The successful nonsplit shard found the triple after about 31.05B aggregate
accepted trials in just over 8 hours. Including the earlier 50B all-`X1(16)`
miss, the full p23 discovery campaign used about 81.05B accepted trials.

Files:

- `triple.txt`: one-line triple for DANGER3 `vpp.py`.
- `p23-success-summary.txt`: compact run summary and provenance.
- `p23-verification.txt`: verifier, primality, and independent doubling replay output.
- `p23-worker03-tail.txt`: final tail of the successful worker log.
- `pomerance_100000000000000000000117.lean`: generated Lean certificate file; included for convenience.
