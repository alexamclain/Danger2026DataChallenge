#!/usr/bin/env python3
"""Post-scout reduction gate for the p25 KSY-y moonshot.

The five primary-source scouts reduced the broad literature space to a few
precise ways a sub-sqrt moonshot could still win.  This gate makes that
reduction executable: it reruns the scout profiles, checks the closing-theorem
obligation, and emits a ranked target matrix with continue/kill decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_danger3_framing_extraction_primary_source_scout_gate import (
    profile_danger3_framing_extraction_scout,
)
from p25_ksy_y_ksy_exact_p_primary_source_scout_gate import (
    profile_ksy_exact_p_scout,
)
from p25_ksy_y_kubert_lang_mixed_graph_primary_source_scout_gate import (
    profile_kubert_lang_mixed_graph_scout,
)
from p25_ksy_y_primary_source_scout_packet_gate import profile_scout_packet
from p25_ksy_y_siegel_robert_period_value_primary_source_scout_gate import (
    profile_siegel_robert_period_value_scout,
)
from p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate import (
    profile_sprang_kronecker_d2_scout,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    AMBIENT_PERIOD,
    P25,
    RAW_C,
    RAW_D,
    RAW_K,
    SUPPORT_PERIOD,
    profile_closing_theorem_obligation,
)


TRACE_DATA = (
    "t=5808037298190 v2=42 odd=2273736754431; "
    "t=1409990787086 v2=50 odd=8881784197; "
    "t=-2988055724018 v2=42 odd=2273736754433"
)

RAW_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} "
    f"y(C+jD+kK)/y(-C-jD-kK), C={RAW_C}, D={RAW_D}, K={RAW_K}"
)


@dataclass(frozen=True)
class MoonshotReductionTarget:
    priority: int
    name: str
    target_class: str
    output_family: str
    p24_prior: str
    p25_payload: str
    transferable_gate: str
    first_falsifier: str
    positive_artifact: str
    discard_condition: str
    recommendation: str
    local_probe: str
    row_ok: bool


@dataclass(frozen=True)
class PostScoutReductionProfile:
    p: int
    trace_data: str
    raw_product: str
    support_period: int
    ambient_period: int
    scout_packet_ok: bool
    ksy_scout_ok: bool
    kubert_lang_scout_ok: bool
    sprang_scout_ok: bool
    period_value_scout_ok: bool
    danger3_scout_ok: bool
    closing_obligation_ok: bool
    targets: tuple[MoonshotReductionTarget, ...]
    active_theorem_targets: int
    challenge_targets: int
    killed_shadow_targets: int
    direct_source_closing_rows: int
    hypothetical_source_closing_rows: int
    hypothetical_submission_rows: int
    row_ok: bool


def reduction_targets() -> tuple[MoonshotReductionTarget, ...]:
    return (
        MoonshotReductionTarget(
            priority=1,
            name="sprang_or_ksy_exact_theta2_or_p_divisor",
            target_class="theorem",
            output_family="divisor-additive",
            p24_prior=(
                "p24 exact-product/theta2/Kronecker-D2 work: formula language "
                "is useful only when it emits the exact mixed product or divisor"
            ),
            p25_payload=(
                f"{RAW_PRODUCT}; support period {SUPPORT_PERIOD}; "
                "preferred initial focus is the v2=50 trace unless a theorem "
                "chooses another admissible trace"
            ),
            transferable_gate=(
                "exact-product intake, source-parameter hygiene, closing-theorem "
                "obligation, theorem-hit router raw-divisor/raw-additive"
            ),
            first_falsifier=(
                "formula language, dlog/distribution, or class-field generation "
                "without exact P/theta2 mixed-graph data"
            ),
            positive_artifact=(
                "exact P or exact theta2/theta2^-1 divisor data with mixed graph, "
                "orientation, equal weights, and an arithmetic producer"
            ),
            discard_condition=(
                "no exact P/theta2 clause after source theorem and parameter "
                "hygiene are applied"
            ),
            recommendation="continue_first",
            local_probe=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py "
                "--output-type raw-divisor --center-right 47 --center-c 28 "
                "--d-right 22 --d-c 3 --k-multiplier 1"
            ),
            row_ok=True,
        ),
        MoonshotReductionTarget(
            priority=2,
            name="kubert_lang_raw_mixed_product",
            target_class="theorem",
            output_family="raw-product",
            p24_prior=(
                "p24 Kubert-Lang/exponent-matrix work separated necessary "
                "congruence hygiene from the actual mixed graph"
            ),
            p25_payload=(
                "row-labeled C_3 x C_169 pairs, reflection center, and raw "
                "equal-weight K-traced anti-invariant product"
            ),
            transferable_gate=(
                "mixed-graph obligation, source-claim intake, closing-theorem "
                "obligation"
            ),
            first_falsifier=(
                "C169 projection, Kubert-Lang congruence hygiene, or generator "
                "theorem without row labels and arithmetic producer"
            ),
            positive_artifact=(
                "exact row labels/reflection center/raw product plus arithmetic "
                "producer theorem"
            ),
            discard_condition=(
                "only generator/exponent-hygiene language, or mixed graph without "
                "a producer"
            ),
            recommendation="continue_lower_than_exact_divisor",
            local_probe=(
                "p25_ksy_y_kubert_lang_mixed_graph_primary_source_scout_gate.py"
            ),
            row_ok=True,
        ),
        MoonshotReductionTarget(
            priority=3,
            name="siegel_robert_exact_period_value",
            target_class="theorem",
            output_family="period-value",
            p24_prior=(
                "p24 value-side work found that bare values are not enough; "
                "branch/root context must be part of the payload"
            ),
            p25_payload=(
                f"exact finite-field value for P with support period "
                f"{SUPPORT_PERIOD}; ambient period {AMBIENT_PERIOD} is an "
                "11-branch obstruction"
            ),
            transferable_gate=(
                "period-value upgrade, source-claim intake, closing-theorem "
                "obligation, theorem-hit router raw-value with period-156 context"
            ),
            first_falsifier=(
                "class-field generation, bare value identity, or ambient-780 "
                "value without support-period fixedness"
            ),
            positive_artifact=(
                "exact finite-field value identity for P preserving the mixed "
                "graph with period-156 branch/root/telescoping context"
            ),
            discard_condition=(
                "no period-156 context, or source only proves ray-class "
                "generation"
            ),
            recommendation="continue_value_lane_after_divisor_lanes",
            local_probe=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py "
                "--output-type raw-value --center-right 47 --center-c 28 "
                "--d-right 22 --d-c 3 --k-multiplier 1 --period-156-context"
            ),
            row_ok=True,
        ),
        MoonshotReductionTarget(
            priority=4,
            name="danger3_policy_or_extraction_only",
            target_class="challenge",
            output_family="policy-extraction",
            p24_prior=(
                "p24 certificate work proved verifier discipline matters: "
                "theorem-side progress is not a submitted triple"
            ),
            p25_payload=(
                "official DANGER3 surface is a concrete p25 (A,x0) accepted by "
                "vpp.py, with Lean certificate generation after a hit"
            ),
            transferable_gate=(
                "DANGER3 framing, submission-extraction gate, official vpp.py"
            ),
            first_falsifier=(
                "policy-only answer, theorem-only answer, extraction algorithm "
                "without output, or concrete triple failing vpp.py"
            ),
            positive_artifact=(
                "policy yes plus theorem route and extraction, or direct verified "
                "p25 (A,x0)"
            ),
            discard_condition=(
                "no exact theorem to frame and no concrete vpp.py-verified triple"
            ),
            recommendation="continue_only_on_theorem_hit_or_drew_answer",
            local_probe=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py "
                "--p P --A A --x0 X0"
            ),
            row_ok=True,
        ),
        MoonshotReductionTarget(
            priority=5,
            name="broad_generation_shadows",
            target_class="rejected-shadow",
            output_family="field-generation-shadow",
            p24_prior=(
                "p24 drift came from treating nearby CM/Lang/generator facts as "
                "if they were closing payloads"
            ),
            p25_payload=(
                "KSY Theorem 5.3, Schertz/Shin generators, Kubert-Lang generator "
                "theorems, ordinary theta_D at D=2, and generic CM provenance"
            ),
            transferable_gate=(
                "source-claim intake, source-parameter hygiene, DANGER3 framing"
            ),
            first_falsifier=(
                "not exact P, not mixed graph, not period-156 value, or not a "
                "verified triple"
            ),
            positive_artifact="none as a direct closer",
            discard_condition="direct closure attempt through broad generation language",
            recommendation="kill_as_direct_moonshot_target",
            local_probe="classify through the source-claim intake gate before spending time",
            row_ok=True,
        ),
    )


def profile_post_scout_moonshot_reduction() -> PostScoutReductionProfile:
    scout_packet = profile_scout_packet()
    ksy = profile_ksy_exact_p_scout()
    kubert_lang = profile_kubert_lang_mixed_graph_scout()
    sprang = profile_sprang_kronecker_d2_scout()
    period_value = profile_siegel_robert_period_value_scout()
    danger3 = profile_danger3_framing_extraction_scout()
    closing = profile_closing_theorem_obligation()
    targets = reduction_targets()

    active_theorem_targets = sum(
        int(row.target_class == "theorem" and row.recommendation.startswith("continue"))
        for row in targets
    )
    challenge_targets = sum(int(row.target_class == "challenge") for row in targets)
    killed_shadow_targets = sum(int(row.target_class == "rejected-shadow") for row in targets)

    direct_source_closing_rows = (
        ksy.direct_closing_rows
        + kubert_lang.direct_closing_rows
        + sprang.direct_closing_rows
        + period_value.direct_closing_rows
    )
    hypothetical_source_closing_rows = (
        ksy.hypothetical_closing_rows
        + kubert_lang.hypothetical_closing_rows
        + sprang.hypothetical_closing_rows
        + period_value.hypothetical_closing_rows
    )

    expected_names = (
        "sprang_or_ksy_exact_theta2_or_p_divisor",
        "kubert_lang_raw_mixed_product",
        "siegel_robert_exact_period_value",
        "danger3_policy_or_extraction_only",
        "broad_generation_shadows",
    )
    all_inputs_ok = (
        scout_packet.row_ok
        and ksy.row_ok
        and kubert_lang.row_ok
        and sprang.row_ok
        and period_value.row_ok
        and danger3.row_ok
        and closing.row_ok
    )
    row_ok = (
        all_inputs_ok
        and tuple(row.name for row in targets) == expected_names
        and active_theorem_targets == 3
        and challenge_targets == 1
        and killed_shadow_targets == 1
        and direct_source_closing_rows == 0
        and hypothetical_source_closing_rows == 4
        and danger3.hypothetical_submission_rows == 1
        and closing.source_theorem_closed_rows == 4
        and closing.submission_ready_rows == 1
        and all(row.row_ok for row in targets)
    )

    return PostScoutReductionProfile(
        p=P25,
        trace_data=TRACE_DATA,
        raw_product=RAW_PRODUCT,
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        scout_packet_ok=scout_packet.row_ok,
        ksy_scout_ok=ksy.row_ok,
        kubert_lang_scout_ok=kubert_lang.row_ok,
        sprang_scout_ok=sprang.row_ok,
        period_value_scout_ok=period_value.row_ok,
        danger3_scout_ok=danger3.row_ok,
        closing_obligation_ok=closing.row_ok,
        targets=targets,
        active_theorem_targets=active_theorem_targets,
        challenge_targets=challenge_targets,
        killed_shadow_targets=killed_shadow_targets,
        direct_source_closing_rows=direct_source_closing_rows,
        hypothetical_source_closing_rows=hypothetical_source_closing_rows,
        hypothetical_submission_rows=danger3.hypothetical_submission_rows,
        row_ok=row_ok,
    )


def print_target(row: MoonshotReductionTarget) -> None:
    print(
        "  "
        f"priority={row.priority} name={row.name} class={row.target_class} "
        f"family={row.output_family} recommendation={row.recommendation} "
        f"positive={row.positive_artifact} falsifier={row.first_falsifier} "
        f"discard={row.discard_condition} gate={row.transferable_gate}"
    )


def main() -> int:
    profile = profile_post_scout_moonshot_reduction()
    print("p25 KSY-y post-scout moonshot reduction gate")
    print(f"p={profile.p}")
    print(f"trace_data={profile.trace_data}")
    print(f"raw_product={profile.raw_product}")
    print(f"support_period={profile.support_period}")
    print(f"ambient_period={profile.ambient_period}")
    print("completed_inputs")
    print(f"  scout_packet_ok={int(profile.scout_packet_ok)}")
    print(f"  ksy_scout_ok={int(profile.ksy_scout_ok)}")
    print(f"  kubert_lang_scout_ok={int(profile.kubert_lang_scout_ok)}")
    print(f"  sprang_scout_ok={int(profile.sprang_scout_ok)}")
    print(f"  period_value_scout_ok={int(profile.period_value_scout_ok)}")
    print(f"  danger3_scout_ok={int(profile.danger3_scout_ok)}")
    print(f"  closing_obligation_ok={int(profile.closing_obligation_ok)}")
    print("targets")
    for row in profile.targets:
        print_target(row)
    print("counts")
    print(f"  active_theorem_targets={profile.active_theorem_targets}")
    print(f"  challenge_targets={profile.challenge_targets}")
    print(f"  killed_shadow_targets={profile.killed_shadow_targets}")
    print(f"  direct_source_closing_rows={profile.direct_source_closing_rows}")
    print(f"  hypothetical_source_closing_rows={profile.hypothetical_source_closing_rows}")
    print(f"  hypothetical_submission_rows={profile.hypothetical_submission_rows}")
    print("interpretation")
    print("  post_scout_search_is_artifact_gated_not_time_gated=1")
    print("  exact_divisor_or_raw_product_lanes_are_first=1")
    print("  period_value_lane_requires_support_period_156=1")
    print("  broad_generation_shadows_are_killed_as_direct_closers=1")
    print("  verified_vpp_triple_remains_the_challenge_surface=1")
    print(f"ksy_y_post_scout_moonshot_reduction_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-scout moonshot reduction regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
