# P27 Conic-Pair D4 Recurrence

Date: 2026-06-21

## Claim

The legal conic-pair coordinates expose an exact non-tautological selector for
the next gate.

On a legal d3-plus conic-pair lift, write:

```text
R = next r-coordinate
a = R - 1/R
L = h - g - 2r
```

where the current one-step pair satisfies:

```text
h^2 = r^2 + c*r + 1
g^2 = r^2 - c*r + 1
R^2 - (h + g)*R + 1 = 0
```

Then in the p27 signature regime:

```text
d4 = chi(R^2 + c*R + 1)
   = chi(-(L+a)(L-a)cR).
```

This is the first exact two-gate formula in the conic-chain coordinates.  It
does not by itself finish the sqrt-beating source, because the selected next
coordinate does not re-enter the original legal label-2/compactD source in the
tested fields.  But it gives a concrete Kummer divisor for the next legal
pullback/quotient test.

## Artifacts

Probes:

```text
research/p27/archive/gates/p27_conic_pair_d4_recurrence_probe.py
research/p27/archive/gates/p27_conic_pair_d4_symbolic_identity.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_d4_recurrence_probe_q607_q1607_q1847_q2087_p27_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_d4_symbolic_identity_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_d4_symbolic_identity.py \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_d4_symbolic_identity_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_d4_recurrence_probe.py \
  --small-primes 607,1607,1847,2087 \
  --raw-cr-limit 700 \
  --p27-target 1000 \
  --p27-heldout-target 1000 \
  --p27-max-draws 1000000 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_d4_recurrence_probe_q607_q1607_q1847_q2087_p27_20260621.txt
```

## Symbolic Identity

Using the conic-pair sampler relation:

```text
a = R - 1/R
r = -(L^2 + a^2)/(4L)
c = (R + 1/R)(L + 2r)/(2r)
```

the symbolic verifier gives:

```text
(R^2+cR+1) / (-(L+a)(L-a)cR)
  = 2*R^2*(R-1)^2*(R+1)^2
    / ((LR-R^2+1)^2*(LR+R^2-1)^2).
```

The quotient is `2` times a square.  Since every p27-signature field here has
`q = 7 mod 8`, and p27 itself has `p = 7 mod 8`, `chi(2)=+1`.  Therefore:

```text
chi(R^2+cR+1) = chi(-(L+a)(L-a)cR).
```

## Guard-Field Results

The exact feature combo was found independently in all nonconstant guard
fields:

```text
q1607:
  d3-plus unique (A,x) = 112
  d4 split = 76 plus / 36 minus
  exact combo = -1 * L+a * L-a * c*R
  selected next coordinate re-enters legal source = 0/224

q1847:
  d3-plus unique (A,x) = 180
  d4 split = 76 plus / 104 minus
  exact combo = -1 * L+a * L-a * c*R
  selected next coordinate re-enters legal source = 0/360

q2087:
  d3-plus unique (A,x) = 100
  d4 split = 72 plus / 28 minus
  exact combo = -1 * L+a * L-a * c*R
  selected next coordinate re-enters legal source = 0/200
```

The q607 field is a sanity check where d4 is constant minus on this slice:

```text
q607:
  exact combo = -1
```

## P27 Sample Results

The same exact combo holds on actual p27 samples:

```text
p27 train:
  sampled pairs = 1000
  d3-plus unique (A,x) = 484
  d4 split = 244 plus / 240 minus
  conic lifts = 15488
  exact combo = -1 * L+a * L-a * c*R

p27 heldout:
  sampled pairs = 1000
  d3-plus unique (A,x) = 526
  d4 split = 232 plus / 294 minus
  conic lifts = 16832
  exact combo = -1 * L+a * L-a * c*R
```

Across the combined q1607/q1847/q2087/p27 train/p27 heldout rows, the same
formula is exact over `46,848` feature rows.

## Interpretation

Positive:

```text
d4 is not an opaque fresh quartic squareclass once the d3 conic-pair lift is
present.
The next selector is a four-factor Kummer character on the current lift:
-(L+a)(L-a)cR.
This gives a concrete divisor for the legal pullback/quotient problem.
```

Negative:

```text
The selected next coordinate did not re-enter the original legal
label-2/compactD source in q1607/q1847/q2087.
So the easy iteration "use the same starting legal sampler again" is killed.
```

## Next Tests

```text
1. Legal pullback with d4 selector:
   add Z^2 = -(L+a)(L-a)cR to the legal conic-pair pullback and compute
   genus/components/quotients.

2. D5 recurrence:
   after adjoining Z, derive the next pair variables and test whether d5 has
   another compact product formula in the same coordinate tower.

3. GPU boundary:
   GPU should log this selector only if it already has the legal conic-pair
   variables.  Do not run free random (R,L), and do not treat this as a
   production path until the legal pullback/source exists.
```

## Continue / Kill

```text
continue = legal pullback plus Z^2 = -(L+a)(L-a)cR
continue = d5 recurrence after adjoining the d4 selector root
continue = expert/CAS review of this Kummer divisor on the conic-pair curve

kill = iterating the original legal label-2/compactD source directly
kill = GPU production from free (R,L)
```

```text
p27_conic_pair_d4_recurrence_rows=1/1
```
