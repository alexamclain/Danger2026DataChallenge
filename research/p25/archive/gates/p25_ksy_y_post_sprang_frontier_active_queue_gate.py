#!/usr/bin/env python3
"""Active-queue gate after the Sprang exact-specialization frontier.

Once the current Sprang clauses are drained as direct closers, the moonshot
needs a concrete next lane instead of another broad source reread.  This gate
promotes the Kubert-Lang/KSY exact-product route to the active front door while
keeping Sprang as a watchlist item for a named exact theorem/formula hit.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_kubert_lang_gdz_ocr_boundary_gate import profile_kl_gdz_ocr_boundary
from p25_ksy_y_kubert_lang_v_iwasawa_boundary_gate import profile_kl_v_iwasawa_boundary
from p25_ksy_y_sprang_exact_specialization_frontier_gate import (
    profile_sprang_exact_specialization_frontier,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    profile_exact_product_intake,
)


@dataclass(frozen=True)
class ActiveQueueRow:
    priority: int
    name: str
    role: str
    decision: str
    first_falsifier: str
    required_next_artifact: str
    ok: bool


@dataclass(frozen=True)
class PostSprangFrontierActiveQueueProfile:
    sprang_frontier_ok: bool
    exact_product_intake_ok: bool
    kl_iv_boundary_ok: bool
    kl_v_boundary_ok: bool
    exact_payload_shapes_required: int
    active_rows: tuple[ActiveQueueRow, ...]
    active_first_rows: int
    watchlist_rows: int
    killed_shadow_rows: int
    direct_source_closing_rows_seen: int
    heavy_mixed_graph_stack_required_for_queue_gate: bool
    row_ok: bool


def profile_post_sprang_frontier_active_queue() -> PostSprangFrontierActiveQueueProfile:
    sprang = profile_sprang_exact_specialization_frontier()
    product = profile_exact_product_intake()
    kl_iv = profile_kl_gdz_ocr_boundary()
    kl_v = profile_kl_v_iwasawa_boundary()
    exact_payload_shapes_required = 3

    rows = (
        ActiveQueueRow(
            priority=1,
            name="kubert_lang_ksy_exact_mixed_product",
            role="active_front_door",
            decision="continue_first",
            first_falsifier=(
                "C169 projection, KL congruence hygiene, generator theorem, "
                "or Iwasawa freeness without exact mixed row labels"
            ),
            required_next_artifact=(
                "named theorem/formula hit producing exact row-labeled pairs, "
                "reflection center, or raw equal-weight K-traced product"
            ),
            ok=product.row_ok
            and product.closing_product_claims == exact_payload_shapes_required
            and product.rejected_product_claims == 4
            and kl_iv.direct_closing_rows == 0
            and kl_v.direct_closing_rows == 0,
        ),
        ActiveQueueRow(
            priority=2,
            name="ksy_normalized_y_exact_distribution",
            role="active_companion_front_door",
            decision="continue_second",
            first_falsifier=(
                "single y-value, ray-class generation, or formula language "
                "without all 75 atoms and orientation"
            ),
            required_next_artifact=(
                "exact K-traced normalized-y product/distribution theorem "
                "feeding the theta2/theta2-inverse certificate path"
            ),
            ok=product.row_ok and product.closing_product_claims == 3,
        ),
        ActiveQueueRow(
            priority=3,
            name="sprang_exact_specialization_hit",
            role="watchlist_not_active_broad_reread",
            decision="continue_only_on_new_named_source_hit",
            first_falsifier=(
                "omega^D, kernel/torsion distribution, prime-to-6 theta_D "
                "comparison, or cohomology formula without exact p25 payload"
            ),
            required_next_artifact=(
                "exact mixed row-labeled Sprang theorem/formula emitting the "
                "positive layer, T orientation, and K-traced P/theta2 payload"
            ),
            ok=sprang.row_ok and sprang.shift_active_search_to_kl_without_new_sprang_source,
        ),
        ActiveQueueRow(
            priority=4,
            name="kl_iv_v_direct_source_boundary",
            role="killed_shadow_with_ocr_hook",
            decision="kill_as_direct_closer_continue_only_with_ocr_upgrade",
            first_falsifier=(
                "generic modular-unit generation, multiplicative dependence, "
                "Delta criteria, p-primary tower, or Iwasawa module freeness"
            ),
            required_next_artifact=(
                "OCR/human theorem hit upgraded to exact row labels, "
                "reflection center, or raw product"
            ),
            ok=kl_iv.row_ok
            and kl_v.row_ok
            and kl_iv.direct_closing_rows == 0
            and kl_v.direct_closing_rows == 0
            and kl_iv.ocr_required_rows == 1
            and kl_v.ocr_required_rows == 1,
        ),
    )

    active_first = sum(row.role == "active_front_door" for row in rows)
    watchlist = sum("watchlist" in row.role for row in rows)
    killed = sum(row.role.startswith("killed") for row in rows)
    direct_source_closing = kl_iv.direct_closing_rows + kl_v.direct_closing_rows
    row_ok = (
        sprang.row_ok
        and product.row_ok
        and kl_iv.row_ok
        and kl_v.row_ok
        and exact_payload_shapes_required == 3
        and active_first == 1
        and watchlist == 1
        and killed == 1
        and direct_source_closing == 0
        and tuple(row.decision for row in rows)
        == (
            "continue_first",
            "continue_second",
            "continue_only_on_new_named_source_hit",
            "kill_as_direct_closer_continue_only_with_ocr_upgrade",
        )
        and all(row.ok for row in rows)
    )

    return PostSprangFrontierActiveQueueProfile(
        sprang_frontier_ok=sprang.row_ok,
        exact_product_intake_ok=product.row_ok,
        kl_iv_boundary_ok=kl_iv.row_ok,
        kl_v_boundary_ok=kl_v.row_ok,
        exact_payload_shapes_required=exact_payload_shapes_required,
        active_rows=rows,
        active_first_rows=active_first,
        watchlist_rows=watchlist,
        killed_shadow_rows=killed,
        direct_source_closing_rows_seen=direct_source_closing,
        heavy_mixed_graph_stack_required_for_queue_gate=False,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_sprang_frontier_active_queue()
    print("p25 KSY-y post-Sprang-frontier active-queue gate")
    print("dependency_gates")
    print(f"  sprang_frontier_ok={int(profile.sprang_frontier_ok)}")
    print(f"  exact_product_intake_ok={int(profile.exact_product_intake_ok)}")
    print(f"  kl_iv_boundary_ok={int(profile.kl_iv_boundary_ok)}")
    print(f"  kl_v_boundary_ok={int(profile.kl_v_boundary_ok)}")
    print(f"  exact_payload_shapes_required={profile.exact_payload_shapes_required}")
    print("active_queue")
    for row in profile.active_rows:
        print(
            "  "
            f"priority={row.priority} name={row.name} role={row.role} "
            f"decision={row.decision} ok={int(row.ok)}"
        )
        print(f"    falsifier={row.first_falsifier}")
        print(f"    next={row.required_next_artifact}")
    print("counts")
    print(f"  active_first_rows={profile.active_first_rows}")
    print(f"  watchlist_rows={profile.watchlist_rows}")
    print(f"  killed_shadow_rows={profile.killed_shadow_rows}")
    print(
        "  direct_source_closing_rows_seen="
        f"{profile.direct_source_closing_rows_seen}"
    )
    print(
        "  heavy_mixed_graph_stack_required_for_queue_gate="
        f"{int(profile.heavy_mixed_graph_stack_required_for_queue_gate)}"
    )
    print("interpretation")
    print("  KL_KSY_exact_product_is_now_the_active_front_door=1")
    print("  Sprang_is_watchlist_only_without_new_exact_source_hit=1")
    print("  KL_IV_V_generic_generation_or_iwasawa_language_is_not_a_closer=1")
    print(
        "ksy_y_post_sprang_frontier_active_queue_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Post-Sprang active queue regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
