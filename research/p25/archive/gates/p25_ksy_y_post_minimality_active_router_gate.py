#!/usr/bin/env python3
"""Active moonshot router after the conductor-39 minimality checkpoint.

The Sprang frontier promotes the Kubert-Lang/KSY exact mixed product as the
active exact-product door.  The Yang conductor-39 compression, strengthened by
doubling-orbit minimality, gives an even smaller global first target.  This
gate reconciles those queues so future work does not oscillate between them.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    profile_conductor39_source_theorem_intake,
)
from p25_ksy_y_post_conductor39_source_queue_gate import (
    profile_post_conductor39_source_queue,
)
from p25_ksy_y_post_sprang_frontier_active_queue_gate import (
    profile_post_sprang_frontier_active_queue,
)
from p25_ksy_y_yang_y507_conductor39_doubling_orbit_minimality_gate import (
    profile_yang_y507_conductor39_doubling_orbit_minimality,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    profile_closing_theorem_obligation,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate import (
    profile_mixed_graph_obligation,
)


@dataclass(frozen=True)
class ActiveRouteRow:
    priority: int
    name: str
    role: str
    decision: str
    accepted_payload: str
    first_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class PostMinimalityActiveRouter:
    conductor39_queue_ok: bool
    conductor39_intake_ok: bool
    doubling_minimality_ok: bool
    post_sprang_queue_ok: bool
    mixed_graph_obligation_ok: bool
    closing_obligation_ok: bool
    routes: tuple[ActiveRouteRow, ...]
    primary_rows: int
    companion_rows: int
    follow_on_rows: int
    watchlist_rows: int
    helper_rows: int
    killed_rows: int
    proper_suborbit_killed: bool
    direct_submission_control_rows: int
    row_ok: bool


def profile_post_minimality_active_router() -> PostMinimalityActiveRouter:
    conductor_queue = profile_post_conductor39_source_queue()
    conductor_intake = profile_conductor39_source_theorem_intake()
    minimality = profile_yang_y507_conductor39_doubling_orbit_minimality()
    post_sprang = profile_post_sprang_frontier_active_queue()
    mixed_graph = profile_mixed_graph_obligation()
    closing = profile_closing_theorem_obligation()

    routes = (
        ActiveRouteRow(
            priority=1,
            name="conductor39_full_doubling_orbit_norm",
            role="primary_front_door",
            decision="continue_first",
            accepted_payload=(
                "theorem emits Q=prod_{i=0..11} [2]^i(E_7/E_1), equivalently "
                "U_chi=1_{7<2>}-1_{<2>}, then W=6*U_chi and Yang's 13-fiber lift"
            ),
            first_falsifier=(
                "seed ratio alone, proper doubling suborbit, conductor-3/13 "
                "projection, additive separation, or level-507 story without "
                "the conductor-39 lift"
            ),
            next_action=(
                "route through conductor-39 intake; require full orbit norm, "
                "mixed tensor signs, Yang lift, and Frobenius/Hilbert-90 descent"
            ),
            ok=(
                conductor_queue.row_ok
                and conductor_intake.row_ok
                and minimality.row_ok
                and conductor_intake.doubling_orbit_minimality_ok
                and minimality.full_orbit_forced_by_yang_yu
                and minimality.proper_legal_rows == 0
                and conductor_queue.rows[0].name == "mixed_x1_39_unit_plus_yang_distribution"
            ),
        ),
        ActiveRouteRow(
            priority=2,
            name="conductor39_period156_hilbert90_descent",
            role="follow_on_front_door",
            decision="continue_after_source_or_with_value_theorem",
            accepted_payload=(
                "finite-field value or divisor theorem for the conductor-39 "
                "source with ratio, twisted trace, Hilbert-90 boundary, or "
                "legal support-156 sparse Yang-lift potential and period-156 "
                "branch context"
            ),
            first_falsifier=(
                "bare exact value, naive degree-6 norm, or ambient period-780 "
                "value without the support-period context"
            ),
            next_action=(
                "keep only value-side claims that preserve the full source "
                "object and remove the period/root ambiguity"
            ),
            ok=(
                conductor_queue.rows[1].name == "hilbert90_period156_value_descent"
                and conductor_queue.rows[1].ok
                and conductor_intake.hilbert90_ok
                and conductor_intake.hilbert90_sparse_yang_lift_ok
                and conductor_intake.conditional_rows == 3
            ),
        ),
        ActiveRouteRow(
            priority=3,
            name="kubert_lang_ksy_exact_mixed_product",
            role="active_companion_front_door",
            decision="continue_parallel",
            accepted_payload=(
                "exact row-labeled pairs, reflection center, or raw equal-weight "
                "75-atom K-traced anti-invariant normalized-y product with orientation"
            ),
            first_falsifier=(
                "C169 projection, KL congruence hygiene, field generation, "
                "single y-value, nonuniform atom weights, or missing mixed graph"
            ),
            next_action=(
                "route theorem hits through mixed-graph obligation and closing "
                "theorem obligation; product/value output still needs DANGER3 "
                "framing and extraction"
            ),
            ok=(
                post_sprang.row_ok
                and mixed_graph.row_ok
                and closing.row_ok
                and post_sprang.active_first_rows == 1
                and mixed_graph.finite_obligation_rows == 4
                and mixed_graph.arithmetic_closing_rows == 1
                and closing.source_theorem_closed_rows == 4
            ),
        ),
        ActiveRouteRow(
            priority=4,
            name="sprang_exact_specialization_hit",
            role="watchlist",
            decision="continue_only_on_new_named_exact_hit",
            accepted_payload=(
                "new Sprang theorem or formula emitting the exact mixed "
                "row-labeled p25 payload"
            ),
            first_falsifier=(
                "omega^D, kernel/torsion distribution, theta_D comparison, "
                "or cohomology formula without exact p25 payload"
            ),
            next_action="do not broad-reread Sprang without a new named exact clause",
            ok=post_sprang.watchlist_rows == 1 and post_sprang.row_ok,
        ),
        ActiveRouteRow(
            priority=5,
            name="koo_shin_2010_root_descent_helper",
            role="helper",
            decision="keep_as_helper_after_independent_mixed_producer",
            accepted_payload=(
                "constant-product/root-descent context only after another "
                "theorem has preserved the mixed source"
            ),
            first_falsifier="Theorem 5.2 alone, or prime-level projection as payload",
            next_action="cite only inside a later mixed-source proof",
            ok=(
                conductor_queue.rows[3].name == "koo_shin_2010_theorem52_root_descent"
                and conductor_queue.rows[3].ok
            ),
        ),
        ActiveRouteRow(
            priority=6,
            name="projection_hygiene_generation_shadows",
            role="killed_shadow",
            decision="kill",
            accepted_payload="none",
            first_falsifier=(
                "proper pushforwards of U_chi vanish, while exact-product "
                "screens without row labels do not satisfy the mixed graph"
            ),
            next_action=(
                "reject unless upgraded to the full conductor-39 orbit norm or "
                "the exact KL/KSY mixed product payload"
            ),
            ok=(
                conductor_queue.killed_rows == 1
                and mixed_graph.rejected_rows == 3
                and closing.rejected_rows == 2
                and conductor_queue.rows[4].name == "prime13_or_c169_projection_closer"
            ),
        ),
    )

    primary_rows = sum(row.role == "primary_front_door" for row in routes)
    companion_rows = sum(row.role == "active_companion_front_door" for row in routes)
    follow_on_rows = sum(row.role == "follow_on_front_door" for row in routes)
    watchlist_rows = sum(row.role == "watchlist" for row in routes)
    helper_rows = sum(row.role == "helper" for row in routes)
    killed_rows = sum(row.role == "killed_shadow" for row in routes)
    proper_suborbit_killed = minimality.proper_rows == 27 and minimality.proper_legal_rows == 0
    row_ok = (
        conductor_queue.row_ok
        and conductor_intake.row_ok
        and minimality.row_ok
        and post_sprang.row_ok
        and mixed_graph.row_ok
        and closing.row_ok
        and primary_rows == 1
        and companion_rows == 1
        and follow_on_rows == 1
        and watchlist_rows == 1
        and helper_rows == 1
        and killed_rows == 1
        and proper_suborbit_killed
        and closing.submission_ready_rows == 1
        and tuple(row.decision for row in routes)
        == (
            "continue_first",
            "continue_after_source_or_with_value_theorem",
            "continue_parallel",
            "continue_only_on_new_named_exact_hit",
            "keep_as_helper_after_independent_mixed_producer",
            "kill",
        )
        and all(row.ok for row in routes)
    )
    return PostMinimalityActiveRouter(
        conductor39_queue_ok=conductor_queue.row_ok,
        conductor39_intake_ok=conductor_intake.row_ok,
        doubling_minimality_ok=minimality.row_ok,
        post_sprang_queue_ok=post_sprang.row_ok,
        mixed_graph_obligation_ok=mixed_graph.row_ok,
        closing_obligation_ok=closing.row_ok,
        routes=routes,
        primary_rows=primary_rows,
        companion_rows=companion_rows,
        follow_on_rows=follow_on_rows,
        watchlist_rows=watchlist_rows,
        helper_rows=helper_rows,
        killed_rows=killed_rows,
        proper_suborbit_killed=proper_suborbit_killed,
        direct_submission_control_rows=closing.submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_minimality_active_router()
    print("p25 KSY-y post-minimality active router gate")
    print("dependency_gates")
    print(f"  conductor39_queue_ok={int(profile.conductor39_queue_ok)}")
    print(f"  conductor39_intake_ok={int(profile.conductor39_intake_ok)}")
    print(f"  doubling_minimality_ok={int(profile.doubling_minimality_ok)}")
    print(f"  post_sprang_queue_ok={int(profile.post_sprang_queue_ok)}")
    print(f"  mixed_graph_obligation_ok={int(profile.mixed_graph_obligation_ok)}")
    print(f"  closing_obligation_ok={int(profile.closing_obligation_ok)}")
    print("active_routes")
    for row in profile.routes:
        print(
            "  "
            f"priority={row.priority} name={row.name} role={row.role} "
            f"decision={row.decision} ok={int(row.ok)}"
        )
        print(f"    accepts={row.accepted_payload}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  primary_rows={profile.primary_rows}")
    print(f"  follow_on_rows={profile.follow_on_rows}")
    print(f"  companion_rows={profile.companion_rows}")
    print(f"  watchlist_rows={profile.watchlist_rows}")
    print(f"  helper_rows={profile.helper_rows}")
    print(f"  killed_rows={profile.killed_rows}")
    print(f"  proper_suborbit_killed={int(profile.proper_suborbit_killed)}")
    print(f"  direct_submission_control_rows={profile.direct_submission_control_rows}")
    print("interpretation")
    print("  global_primary_is_conductor39_full_orbit_norm_plus_Yang_lift=1")
    print("  KL_KSY_exact_mixed_product_remains_active_companion_front_door=1")
    print("  Sprang_and_KooShin_are_not_active_broad_reread_targets=1")
    print("  projection_hygiene_generation_shadows_are_killed=1")
    print(f"ksy_y_post_minimality_active_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-minimality active router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
