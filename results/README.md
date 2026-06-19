# DANGER3 Result Artifacts

This directory records verified Pomerance triples and compact reproducibility
artifacts for the local Codex-assisted DANGER3 runs.

## p25 Result

The p25 artifacts are in `p25/`.

```text
p  = 10000000000000000000000013
A  = 5863342488035851054212447
x0 = 9636258147581954669181726
```

The p25 run used y-filtered nonsplit `X1(16)` first-branch halving and found
the triple after about 196.34B aggregate accepted trials in the successful
production run. Including the earlier partial no-hit chunk, the full practical
campaign used about 462.81B accepted trials. See `p25/README.md` for details.

## p23 Result

The p23 artifacts are in `p23/`.

```text
p  = 100000000000000000000117
A  = 24163028207499560363686
x0 = 64911014007772963770218
```

The successful p23 shard used y-filtered nonsplit `X1(16)` first-branch
halving and found the triple after about 31.05B aggregate accepted trials. See
`p23/README.md` for details.

## p22 Result

The p22 artifacts are in `p22/`.

```text
p  = 10000000000000000000009
A  = 9992566338662824267458
x0 = 3694769590833803032125
```

The p22 run used a local performance fork of Ruehle's 2-Sylow projection
search and found the triple after about 58.65B aggregate observed trials. See
`p22/README.md` for details.
