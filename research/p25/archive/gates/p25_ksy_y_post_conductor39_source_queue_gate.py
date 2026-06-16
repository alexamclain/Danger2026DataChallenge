#!/usr/bin/env python3
"""Post-conductor-39 queue for the p25 KSY-y/Yang moonshot.

The Yang distribution-lift checkpoint changes the shape of the first theorem
target.  Instead of treating the level-507 period norm as a primitive mystery,
the queue now starts with a mixed X_1(39) unit U_chi=-chi_3*chi_13 plus Yang
distribution to X_1(507).

This gate records that reroute without forgetting the old exact-product and
period-value doors.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_koo_shin_conductor39_distribution_bridge_gate import (
    profile_koo_shin_conductor39_distribution_bridge,
)
from p25_ksy_y_post_local_source_exact_product_queue_gate import (
    profile_post_local_source_exact_product_queue,
)
from p25_ksy_y_post_local_source_value_side_queue_gate import (
    profile_post_local_source_value_side_queue,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_frobenius_orbit_gate import (
    profile_yang_y507_conductor39_frobenius_orbit,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (
    profile_sparse_hilbert90_yang_lift,
)


@dataclass(frozen=True)
class PostConductor39QueueRow:
    priority: int
    name: str
    role: str
    decision: str
    accepted_payload: str
    first_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class PostConductor39SourceQueue:
    distribution_lift_ok: bool
    frobenius_orbit_ok: bool
    hilbert90_ok: bool
    sparse_hilbert90_yang_lift_ok: bool
    koo_shin_bridge_ok: bool
    exact_product_queue_ok: bool
    value_side_queue_ok: bool
    rows: tuple[PostConductor39QueueRow, ...]
    front_door_rows: int
    helper_rows: int
    killed_rows: int
    conductor39_priority_rows: int
    row_ok: bool


def queue_rows(
    lift,
    frobenius,
    hilbert90,
    sparse_lift,
    koo_bridge,
    exact_queue,
    value_queue,
) -> tuple[PostConductor39QueueRow, ...]:
    return (
        PostConductor39QueueRow(
            priority=1,
            name="mixed_x1_39_unit_plus_yang_distribution",
            role="front_door",
            decision="continue_first",
            accepted_payload=(
                "source theorem emits U_chi, V_bal, or W on X_1(39), preserves "
                "the chi_3 tensor chi_13 row/column signs, and applies Yang's "
                "13-fiber distribution to X_1(507)"
            ),
            first_falsifier=(
                "conductor-3-only, conductor-13-only, additive-separated, "
                "prime-projection, or level-507 story that does not descend to "
                "the constant 13-fiber lift"
            ),
            next_action=(
                "route any Yang/Kubert-Lang/KSY source hit through the "
                "conductor-39 primitive unit, mixed-tensor, legality, and "
                "distribution-lift gates"
            ),
            ok=(
                lift.row_ok
                and lift.source_level == 39
                and lift.target_level == 507
                and lift.lift_length == 13
                and lift.primitive_support == 24
            ),
        ),
        PostConductor39QueueRow(
            priority=2,
            name="hilbert90_period156_value_descent",
            role="front_door",
            decision="continue_second",
            accepted_payload=(
                "finite-field value/divisor theorem for the conductor-39 source "
                "using a ratio, twisted trace, Hilbert-90 boundary, or one of "
                "the legal support-156 sparse Yang-lift potentials, with "
                "period-156 branch context"
            ),
            first_falsifier=(
                "naive degree-6 norm of the pure conductor-39 character, bare "
                "value without period-156 context, or ambient period-780 value"
            ),
            next_action=(
                "accept only value-side claims that keep the exact source object "
                "and pass the period-value/router gates"
            ),
            ok=(
                frobenius.row_ok
                and hilbert90.row_ok
                and sparse_lift.row_ok
                and frobenius.pure_character_degree6_norm_cancels
                and hilbert90.balanced_support == 24
                and hilbert90.sparse_support == 12
                and sparse_lift.min_legal_lifted_potential_support == 156
                and sparse_lift.sparse_lift_halves_boundary_support
                and value_queue.row_ok
                and value_queue.active_closing_target_rows == 1
            ),
        ),
        PostConductor39QueueRow(
            priority=3,
            name="ksy_kl_exact_75_atom_product",
            role="front_door",
            decision="continue_as_companion",
            accepted_payload=(
                "exact K-traced normalized-y/theta2 product P with mixed graph, "
                "equal weights, orientation, arithmetic producer, and DANGER3 "
                "framing"
            ),
            first_falsifier=(
                "formula language, field generation, KL congruence hygiene, "
                "single y-value, or exact product missing the mixed graph"
            ),
            next_action=(
                "if a source theorem emits P directly, route through exact "
                "product intake and closing-theorem obligation"
            ),
            ok=exact_queue.row_ok and exact_queue.router_rows_present == 3,
        ),
        PostConductor39QueueRow(
            priority=4,
            name="koo_shin_2010_theorem52_root_descent",
            role="helper",
            decision="keep_as_helper",
            accepted_payload=(
                "prime-level constant-product/root-descent context after an "
                "independent mixed conductor-39 or exact-product producer exists"
            ),
            first_falsifier=(
                "using Theorem 5.2 alone, or using a prime-13/C169 projection, "
                "as the p25 payload"
            ),
            next_action=(
                "cite only inside a later proof that already preserves the "
                "mixed row-sign tensor"
            ),
            ok=koo_bridge.row_ok and not koo_bridge.theorem52_closes_distribution_source,
        ),
        PostConductor39QueueRow(
            priority=5,
            name="prime13_or_c169_projection_closer",
            role="killed_shadow",
            decision="kill",
            accepted_payload="none",
            first_falsifier=(
                "proper pushforwards of U_chi to mod 3 and mod 13 vanish; the "
                "projection erases the source object"
            ),
            next_action="reject unless the claim restores the mixed conductor-39 tensor",
            ok=(
                koo_bridge.row_ok
                and koo_bridge.prime13_projection_support == 0
                and koo_bridge.mod3_projection_support == 0
            ),
        ),
    )


def profile_post_conductor39_source_queue() -> PostConductor39SourceQueue:
    lift = profile_yang_y507_conductor39_distribution_lift()
    frobenius = profile_yang_y507_conductor39_frobenius_orbit()
    hilbert90 = profile_yang_y507_conductor39_hilbert90_boundary()
    sparse_lift = profile_sparse_hilbert90_yang_lift()
    koo_bridge = profile_koo_shin_conductor39_distribution_bridge()
    exact_queue = profile_post_local_source_exact_product_queue()
    value_queue = profile_post_local_source_value_side_queue()
    rows = queue_rows(lift, frobenius, hilbert90, sparse_lift, koo_bridge, exact_queue, value_queue)

    front_doors = sum(row.role == "front_door" for row in rows)
    helpers = sum(row.role == "helper" for row in rows)
    killed = sum(row.role == "killed_shadow" for row in rows)
    conductor39_priority = sum(row.name == "mixed_x1_39_unit_plus_yang_distribution" for row in rows)
    row_ok = (
        lift.row_ok
        and frobenius.row_ok
        and hilbert90.row_ok
        and sparse_lift.row_ok
        and koo_bridge.row_ok
        and exact_queue.row_ok
        and value_queue.row_ok
        and front_doors == 3
        and helpers == 1
        and killed == 1
        and conductor39_priority == 1
        and rows[0].name == "mixed_x1_39_unit_plus_yang_distribution"
        and all(row.ok for row in rows)
    )
    return PostConductor39SourceQueue(
        distribution_lift_ok=lift.row_ok,
        frobenius_orbit_ok=frobenius.row_ok,
        hilbert90_ok=hilbert90.row_ok,
        sparse_hilbert90_yang_lift_ok=sparse_lift.row_ok,
        koo_shin_bridge_ok=koo_bridge.row_ok,
        exact_product_queue_ok=exact_queue.row_ok,
        value_side_queue_ok=value_queue.row_ok,
        rows=rows,
        front_door_rows=front_doors,
        helper_rows=helpers,
        killed_rows=killed,
        conductor39_priority_rows=conductor39_priority,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_conductor39_source_queue()
    print("p25 KSY-y post-conductor-39 source queue gate")
    print("inputs")
    print(f"  distribution_lift_ok={int(profile.distribution_lift_ok)}")
    print(f"  frobenius_orbit_ok={int(profile.frobenius_orbit_ok)}")
    print(f"  hilbert90_ok={int(profile.hilbert90_ok)}")
    print(f"  sparse_hilbert90_yang_lift_ok={int(profile.sparse_hilbert90_yang_lift_ok)}")
    print(f"  koo_shin_bridge_ok={int(profile.koo_shin_bridge_ok)}")
    print(f"  exact_product_queue_ok={int(profile.exact_product_queue_ok)}")
    print(f"  value_side_queue_ok={int(profile.value_side_queue_ok)}")
    print("queue_rows")
    for row in profile.rows:
        print(
            "  "
            f"priority={row.priority} name={row.name} role={row.role} "
            f"decision={row.decision} ok={int(row.ok)}"
        )
        print(f"    accepts={row.accepted_payload}")
        print(f"    falsifier={row.first_falsifier}")
    print("counts")
    print(f"  front_door_rows={profile.front_door_rows}")
    print(f"  helper_rows={profile.helper_rows}")
    print(f"  killed_rows={profile.killed_rows}")
    print(f"  conductor39_priority_rows={profile.conductor39_priority_rows}")
    print("interpretation")
    print("  first_theorem_target_is_mixed_X1_39_unit_plus_Yang_distribution=1")
    print("  period156_Hilbert90_value_descent_is_second_front_door=1")
    print("  exact_75_atom_product_remains_companion_front_door=1")
    print("  prime13_or_c169_projection_closer_is_killed=1")
    print(f"ksy_y_post_conductor39_source_queue_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-conductor-39 source queue regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
