#!/usr/bin/env python3
"""Boundary between right-resolvent and paired-profile H-potentials.

The p24 H-coboundary target is a statement about the mixed right profile

    G_s = <A_1, B_s> in L.

A stronger sufficient theorem would construct a right-resolvent potential

    B_s = Z_s - Z_{128 s}

before pairing.  This toy records that the stronger theorem is not equivalent:
the vector-valued right resolvent can have H-trace leakage inside the kernel of
the pairing map, while the paired profile still has the required potential.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
Q = 1009
SOURCE_DIM = 3
TARGET_DIM = 2

Vector = tuple[int, ...]
Profile = list[Vector]


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("generator is not primitive")
    return logs


def h_cosets(logs: dict[int, int]) -> list[list[int]]:
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % H_STEP == residue],
            key=logs.__getitem__,
        )
        for residue in range(H_STEP)
    ]


def zero(dim: int) -> Vector:
    return tuple(0 for _ in range(dim))


def add(left: Vector, right: Vector) -> Vector:
    return tuple((a + b) % Q for a, b in zip(left, right))


def sub(left: Vector, right: Vector) -> Vector:
    return tuple((a - b) % Q for a, b in zip(left, right))


def random_vector(rng: random.Random, dim: int = SOURCE_DIM) -> Vector:
    return tuple(rng.randrange(Q) for _ in range(dim))


def random_profile(rng: random.Random, dim: int = SOURCE_DIM) -> Profile:
    profile = [zero(dim) for _ in range(RIGHT)]
    for value in range(1, RIGHT):
        profile[value] = random_vector(rng, dim)
    return profile


def coboundary(potential: Profile, gamma: int) -> Profile:
    dim = len(potential[1])
    profile = [zero(dim) for _ in range(RIGHT)]
    for value in range(1, RIGHT):
        profile[value] = sub(potential[value], potential[gamma * value % RIGHT])
    return profile


def profile_add(left: Profile, right: Profile) -> Profile:
    return [add(a, b) for a, b in zip(left, right)]


def project(profile: Profile) -> Profile:
    return [entry[:TARGET_DIM] for entry in profile]


def relative_traces(profile: Profile, cosets: list[list[int]]) -> list[Vector]:
    traces: list[Vector] = []
    for coset in cosets:
        total = zero(len(profile[1]))
        for value in coset:
            total = add(total, profile[value])
        traces.append(total)
    return traces


def trace_zero(profile: Profile, cosets: list[list[int]]) -> bool:
    return all(all(coord == 0 for coord in trace) for trace in relative_traces(profile, cosets))


def kernel_trace_leak(cosets: list[list[int]]) -> Profile:
    profile = [zero(SOURCE_DIM) for _ in range(RIGHT)]
    leak = (0, 0, 1)
    for coset in cosets:
        profile[coset[0]] = leak
    return profile


def any_nonzero(profile: Profile) -> bool:
    return any(any(coord != 0 for coord in entry) for entry in profile[1:])


def main() -> None:
    logs = log_table()
    gamma = pow(GEN, H_STEP, RIGHT)
    cosets = h_cosets(logs)
    rng = random.Random(20260606)

    vector_potential = random_profile(rng)
    vector_coboundary = coboundary(vector_potential, gamma)
    projected_coboundary = project(vector_coboundary)

    paired_only_source = profile_add(coboundary(random_profile(rng), gamma), kernel_trace_leak(cosets))
    paired_only_profile = project(paired_only_source)

    source_trace_zero = trace_zero(paired_only_source, cosets)
    profile_trace_zero = trace_zero(paired_only_profile, cosets)
    source_trace_leak = any_nonzero(relative_traces(paired_only_source, cosets))
    projected_trace_leak = any_nonzero(relative_traces(paired_only_profile, cosets))

    p_mod = P24 % RIGHT
    p_log = logs[p_mod]

    print("Trace-GCD fixed-frequency order-7 paired-potential boundary toy")
    print(f"field_q={Q}")
    print(f"right={RIGHT}")
    print(f"primitive_root={GEN}")
    print(f"p24_p_mod_211={p_mod}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"h_generator=2^{H_STEP}_mod_211={gamma}")
    print(f"source_dim={SOURCE_DIM}")
    print(f"target_dim={TARGET_DIM}")
    print(f"right_resolvent_coboundary_trace_zero={int(trace_zero(vector_coboundary, cosets))}")
    print(f"projected_profile_trace_zero={int(trace_zero(projected_coboundary, cosets))}")
    print(f"projected_profile_nonzero={int(any_nonzero(projected_coboundary))}")
    print(f"paired_only_source_trace_zero={int(source_trace_zero)}")
    print(f"paired_only_profile_trace_zero={int(profile_trace_zero)}")
    print(f"kernel_trace_leak_survives_before_pairing={int(source_trace_leak)}")
    print(f"kernel_trace_leak_killed_by_pairing={int(not projected_trace_leak)}")
    print(f"separating_identity_projection_detects_leak={int(not source_trace_zero)}")
    print("interpretation")
    print("  right_resolvent_coboundary_implies_profile_coboundary=1")
    print("  paired_profile_coboundary_does_not_imply_right_resolvent_coboundary=1")
    print("  full_right_resolvent_potential_is_sufficient_but_stronger_than_needed=1")
    print("  p24_needed_theorem_is_paired_L_potential_not_full_B_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_paired_potential_boundary_toy")

    if (p_mod, p_log, gamma) != (114, 198, 128):
        raise SystemExit(1)
    if not trace_zero(vector_coboundary, cosets):
        raise SystemExit(1)
    if not trace_zero(projected_coboundary, cosets) or not any_nonzero(projected_coboundary):
        raise SystemExit(1)
    if source_trace_zero or not profile_trace_zero:
        raise SystemExit(1)
    if not source_trace_leak or projected_trace_leak:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
