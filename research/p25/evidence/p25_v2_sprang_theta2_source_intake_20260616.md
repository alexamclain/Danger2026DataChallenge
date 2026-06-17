# P25 v2 Sprang Theta2 Source Intake

Updated: 2026-06-16

## Purpose

Ingest the two Sprang arXiv source bundles linked from the Sprang dossier and
screen them against the current exact-P/theta2 support contract. This pass is
narrow: it asks whether Sprang supplies the challenge-legal arithmetic theorem
that emits the accepted theta2/theta2-inverse divisor-additive payload, or
whether it is still support vocabulary.

## Sources Read

- [arXiv 1801.05677](https://arxiv.org/abs/1801.05677),
  `incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex`
- [arXiv 1802.04996](https://arxiv.org/abs/1802.04996),
  `incoming/extracted/sprang_1802_04996/deRhamRealization.tex`

The arXiv pages identify these as Johannes Sprang's Poincare-bundle papers:
`1801.05677` on Eisenstein-Kronecker series and `1802.04996` on the algebraic
de Rham realization of the elliptic polylogarithm.

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/archive/gates/p25_v2_sprang_theta2_source_intake_gate.py
```

The gate returned `p25_v2_sprang_theta2_source_intake_rows=1/1`.
It uses the local `incoming/` extracts when present and otherwise falls back to
the arXiv e-print tarballs in memory, so the archived gate can replay without
committing raw source bundles.

## Positive Support

Sprang `1801.05677` is stronger than generic vocabulary for the D=2 route:

```text
d_not_coprime_to_6_support = yes
p_adic_theta_support = yes
distribution_relation_support = yes
```

The useful support clauses are:

- the Kronecker-section construction reaches logarithmic derivatives of
  Kato-Siegel functions without needing `D` coprime to `6`;
- the p-adic theta theorem relates derivatives of `pthetaD_(a,b)` to
  p-adic Eisenstein-Kronecker series;
- the distribution relation is stated with `N,D,D'` as non-zero-divisors,
  not with a coprime-to-6 restriction.

Sprang `1802.04996` reinforces the de Rham/Kato-Siegel side:

```text
de_rham_kato_siegel_support = yes
```

So the right summary is not "Sprang is irrelevant." It is a real D=2
Poincare/Kronecker/theta support source.

## Missing P25 Payload

The same source scan found none of the accepted p25 theta2 payload markers:

```text
exact_theta2_payload_named = no
p25_bridge_named = no
compact_ksy_payload_named = no
branch_telescoping_named_for_p25 = no
source_stage_closers = 0
```

In current p25 terms, the paper does not emit:

- exact theta2 or theta2-inverse divisor/additive data for the p25 payload;
- the compact `C,D,K,orientation` or KSY center/half/orientation packet;
- the `C_75 x C_169`, `Norm_156(Y_507)`, or support-period-156 bridge;
- branch/root/telescoping data selecting the finite p25 value.

## Verdict

```text
decision = d2_support_source_not_theta2_closer
continue = only if a Sprang/Kronecker specialization is supplied that emits
           exact theta2 or theta2^-1 divisor/additive data for the p25 payload
kill = broad D=2, p-adic theta, de Rham polylog, or distribution vocabulary
       without the exact p25 finite payload
p25_v2_sprang_theta2_source_intake_rows=1/1
```

This improves the source map: Sprang is a legitimate D=2 support source and
may be the right language for a future theta2 theorem, but the local arXiv
sources as written still do not close exact-P, H0, conductor 39, or extraction.
