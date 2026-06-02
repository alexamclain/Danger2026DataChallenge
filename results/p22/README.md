# DANGER3 p22 Result

This directory records a Pomerance triple found for

```text
p  = 10000000000000000000009
A  = 9992566338662824267458
x0 = 3694769590833803032125
```

The result was found by an Alexa-run, Codex-assisted local performance fork of
Ruehle's 2-Sylow projection search. The search used 10 independent
single-thread worker processes. The quoted production rate of about 1.03M
trials/sec is aggregate across those 10 workers, not a single-thread rate.

Files:

- `p22-success-summary.txt`: compact run summary and provenance.
- `p22-verification.txt`: verifier, primality, and independent doubling replay output.
- `p22-worker07-tail.txt`: tail of the successful worker log.
- `p22-benchmark-comparison.txt`: same-machine benchmark against fresh upstream.
- `pomerance_10000000000000000000009.lean`: generated Lean certificate file; included for convenience but not locally checked in this environment because Mathlib was unavailable.
