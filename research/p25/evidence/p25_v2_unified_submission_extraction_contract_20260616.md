# P25 v2 Unified Submission / Extraction Contract

Updated: 2026-06-16

## Purpose

Turn the current theorem frontier into a submission checklist.  This evidence
page records what a source-stage theorem would still need before it becomes a
DANGER3-ready `(p,A,x0)` certificate.

The gate is intentionally fast: it checks promoted evidence markers and the
small projection/halving arithmetic, rather than rerunning the heavy exact-P
producer screens.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `archive/notes/p25_ksy_y_h0_x18112_bridge_payload_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_halving_certificate_payload_20260614.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_unified_submission_extraction_contract_gate.py
```

The gate returned `p25_v2_unified_submission_extraction_contract_rows=1/1`.

## Evidence Markers

The gate checked these existing promoted or archived markers:

```text
p25_v2_h0_conductor39_unified_target_rows=1/1
p25_v2_exactp_to_unified_target_spine_rows=1/1
H0 theorem-interface contract: all nine gates returned rows=1/1
conductor-39 Yang/H90 interface contract: all seven gates returned rows=1/1
ksy_y_h0_x18112_bridge_payload_contract_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
ksy_y_x1_16_halving_certificate_payload_rows=1/1
ksy_y_danger3_extraction_surface_rows=1/1
ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1
```

## Projection And Halving Arithmetic

```text
p = 10000000000000000000000013
p mod 8 = 5
k = 42
active mode = x16halvenonsplit

8112 = 16 * 507
507^-1 mod 16 = 3
16^-1 mod 507 = 412
P16  = [3*507]R  = [1521]R
Q507 = [412*16]R = [6592]R
1521 + 6592 = 1 mod 8112

start depth = 4
final depth = 42
halving links = 38
x-chain points = 39
```

## Submission Ladder

A theorem hit still has to pass this ladder:

```text
1. source-stage theorem
   accepts: finite value/divisor theorem for one unified support-156
            H0/conductor-39 product, or stronger exact-P upstream theorem
   current: target identified; theorem not found
   missing: source-stage finite value/divisor theorem

2. DANGER3 framing
   accepts: finite-identity/non-CM framing for the theorem hit
   current: boundary defined; no theorem to frame yet
   missing: DANGER3 framing after source theorem

3. same-j X_1(8112) bridge
   accepts: same-curve P16/Q507 pair, or order-8112 generator R with
            P16=[1521]R and Q507=[6592]R
   current: bridge payload contract defined; no live bridge values
   missing: same-j X_1(8112) bridge or equivalent fiber product

4. practical X_1(16) surface
   accepts: X_1(16) y plus model root x, hence A and xP16, or direct A,xP16
   current: active chart contract defined; no extracted A,xP16
   missing: practical X_1(16) chart specialization

5. halving or direct x0
   accepts: 39-point x-coordinate chain x4=xP16 to x42=x0,
            active sqrt-witness chain, or direct A,x0
   current: checkable certificate shape defined; no p25 x-chain/x0
   missing: halving chain or concrete x0

6. official vpp boundary
   accepts: official src/vpp.py verifies concrete p25 (p,A,x0)
   current: submission boundary defined; no verified p25 triple
   missing: official vpp.py verification
```

## Interpretation

The unified H0/conductor-39 theorem and the stronger exact-P upstream theorem
are both still value-stage/theorem-stage wins, not DANGER3 submissions.

The first non-theorem bottleneck is constructive extraction:

```text
same-j X_1(8112)
-> practical X_1(16) y/x/A/xP16 or direct A,xP16
-> 38 halving links / direct x0
-> official vpp.py
```

Current satisfied submission-ladder rows:

```text
current_satisfied_rows = 0
submission_ready_rows_now = 0
```

## Verdict

```text
continue_first_pass_theorem_search = yes
continue_exactp_as_upstream_route = yes
current_submission_ready_payload = no
still_missing_source = finite value/divisor theorem for the unified target,
                       or stronger exact-P theorem
still_missing_extraction = same-j bridge, X_1(16) chart payload, halving/x0,
                           and official vpp.py verification
discard_condition = any claimed theorem hit that cannot enter this ladder
```
