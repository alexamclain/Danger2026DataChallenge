# Trace-Frame Hidden-MSRD Invariant Boundary

Date: 2026-06-05

This note follows up the CS/probability synthesis:

```text
Could the trace-frame code be secretly block-equivalent to an MSRD/LRS code?
```

## Invariant Audit

I added:

```text
p24/trace_frame_msrd_invariant_audit.py
```

It computes invariants preserved by any block-diagonal equivalence of the
relative coefficient blocks:

```text
projection ranks to block subsets;
shortened dimensions on block subsets;
generalized block-support weights.
```

For an MSRD-profile code these have the MDS-like values:

```text
rank(proj_S) = min(k, |S| * subdegree)
dim(shorten_S) = max(0, k - (nblocks - |S|) * subdegree).
```

Thus any defect would immediately falsify the hidden-MSRD strengthening on
that toy row.

## Pinned Results

Pinned command shape:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_msrd_invariant_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --include-linear --only-m 12 --random-trials 40
```

The tested rows were:

```text
target=axis, subdegree=2:
  rows=6, relative_degree=3, subdegree=2
  msrd_profile_ok=1
  generalized_block_weights=(1,1,2,2,3,3)
  random_controls: same signature 40/40

target=constant_plus_4, subdegree=2:
  rows=4, relative_degree=3, subdegree=2
  msrd_profile_ok=1
  generalized_block_weights=(2,2,3,3)
  random_controls: same signature 40/40

target=constant_plus_4, subdegree=3:
  rows=4, relative_degree=2, subdegree=3
  msrd_profile_ok=1
  generalized_block_weights=(1,2,2,2)
  random_controls: same signature 40/40

target=constant_plus_3, subdegree=2:
  rows=3, relative_degree=3, subdegree=2
  msrd_profile_ok=1
  generalized_block_weights=(2,3,3)
  random_controls: same signature 40/40

target=constant_plus_3, subdegree=3:
  rows=3, relative_degree=2, subdegree=3
  msrd_profile_ok=1
  generalized_block_weights=(2,2,2)
  random_controls: same signature 40/40
```

## Consequence

This does **not** falsify hidden MSRD/LRS.  The necessary block-support
profiles hold in the pinned CM rows.

But it also does not explain the p-unit theorem: random matrices with the
same shape pass the same invariant every time in these small fields.  So the
support profile is too coarse to be the certificate engine.

The hidden-MSRD route now needs a stronger arithmetic object:

```text
an explicit p-unit block-equivalence to a known LRS/MSRD normal form,
or an invariant beyond support profiles that distinguishes the CM code from
generic random high-distance subspaces.
```

Absent that explicit equivalence, the smaller theorem remains the direct
Fitting/Schubert local-unit statement:

```text
delta_all in A_all^*
```

equivalently:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }
  = {0}.
```

The full `F_27` annihilator avoidance is only a necessary consequence of this
selected-leading statement.

## Practical Boundary

Useful computation can continue to falsify hidden MSRD by testing sharper
block-equivalence invariants, such as normalized Plucker cross-ratios when
the toy dimensions allow them.  However, plain projection/shortening profiles
should no longer be treated as evidence for a p24 certificate; they are
generic in the small rows tested here.

The block-moduli follow-up is:

```text
p24/trace_frame_block_moduli_boundary.md
```

It explains why the pinned three-block rows do not have enough projective
moduli for a cross-ratio test.  A meaningful block-equivalence falsifier needs
at least four relative blocks, or an explicit class-field block equivalence to
test directly.
