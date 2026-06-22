# P27 B-Line / K-Line Bridge

Date: 2026-06-22

## Claim

The B-line and signed-doubling K-line quartic packets are not independent
target classes.  They are two coordinates for the same descended d3/d4 bits.

The explicit relation

```text
K^2 = (B - 2)^4 / (8*B*(B + 2)^2)
```

maps every legal B target row to a present signed K class in q1471, q1607,
q1847, and q2087.  The target sign agrees for both d3 and d4 in every tested
row.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_kline_bridge_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_kline_bridge_probe_q1471_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_kline_bridge_probe.py \
  --small-primes 1471,1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_kline_bridge_probe_q1471_q1607_q1847_q2087_20260622.txt
```

## Results

For d3:

```text
q1471: B_rows=50, K_roots_2=50, K_present_1=50, target_match=50
q1607: B_rows=49, K_roots_2=49, K_present_1=49, target_match=49
q1847: B_rows=63, K_roots_2=63, K_present_1=63, target_match=63
q2087: B_rows=57, K_roots_2=57, K_present_1=57, target_match=57
```

For d4 after d3:

```text
q1471: B_rows=28, K_roots_2=28, K_present_1=28, target_match=28
q1607: B_rows=28, K_roots_2=28, K_present_1=28, target_match=28
q1847: B_rows=45, K_roots_2=45, K_present_1=45, target_match=45
q2087: B_rows=25, K_roots_2=25, K_present_1=25, target_match=25
```

No bridge mismatches, missing K classes, or mixed signed K target classes
appeared.

## Interpretation

Positive:

```text
The B-line and K-line reductions are now coherently connected.
Any quartic hit in one coordinate should be interpreted as evidence about the
same underlying descended Kummer class.
The bridge gives a way to compare or translate future branch-class output.
```

Negative:

```text
B-line and K-line quartic positives should not be counted as independent
confirmation merely because they use different coordinates.
Running both is still useful, but as coordinate alternatives: one might expose
a low-degree source class that is hidden or higher-degree in the other.
```

## Consequence For GPU

Treat the B-line and K-line quartic screens as one coordinated suite:

```text
primary question = does the descended d3 class have a visible genus-1 quartic
                   model in either B or K?

promotion = stable q1847/q1607/q1471 or q1847/q2087 hit in one coordinate,
            then translate/compare through K^2=(B-2)^4/(8B(B+2)^2)

kill = no stable B-line or K-line quartic hit in the decisive promotion fields
       closes the visible genus-1 coordinate route
```

After a positive, the next step is not production search.  It is constructing
the double cover `z^2=f(B)` or `z^2=f(K)`, checking genus/sourceability, and
comparing the pullback across the B/K bridge.

Follow-up:
[P27 B/K Signed-Root Relation Screen](p27_b_kline_signed_root_relation_20260622.md)
checks whether the chosen signed K root over each B is itself a low-degree
plane-curve shortcut.  It is not: the selected sheet has no positive extra
low-degree relation beyond the inherited two-root bridge cover through the
meaningful degrees in q1471/q1607/q1847/q2087.

```text
p27_b_kline_bridge_rows=1/1
```
