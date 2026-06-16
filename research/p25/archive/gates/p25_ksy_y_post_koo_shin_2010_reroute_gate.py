#!/usr/bin/env python3
"""Post-Koo-Shin-2010 reroute for the p25 KSY-y moonshot.

The actual Koo-Shin 2010 Theorem 5.2 text is now known.  It gives prime-level
Siegel-product rigidity and l-th-root descent, but it does not emit the mixed
p25 product P.  This gate converts that source result into the next queue:

* Koo-Shin 2010 Theorem 5.2 is a helper lemma, not a target.
* C169/prime-level projection alone is killed because it loses the row graph
  and T edge.
* Sprang/Kronecker D=2 exact-product specialization and Kubert-Lang mixed
  exponent/product search remain the first theorem doors.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_gate import (
    profile_actual_theorem52_verdict,
)
from p25_ksy_y_sprang_even_d_specialization_contract_gate import (
    profile_sprang_even_d_specialization_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    profile_kl_exponent_matrix_screen,
)


@dataclass(frozen=True)
class RerouteRow:
    priority: int
    name: str
    role: str
    decision: str
    positive_use: str
    first_falsifier: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class PostKooShin2010RerouteProfile:
    koo_shin_actual_ok: bool
    sprang_even_d_ok: bool
    kl_exponent_screen_ok: bool
    rows: tuple[RerouteRow, ...]
    continue_rows: int
    helper_rows: int
    killed_rows: int
    direct_koo_shin_closer_killed: bool
    prime_projection_killed: bool
    exact_product_front_doors: int
    row_ok: bool


def reroute_rows(koo_shin, sprang, kl) -> tuple[RerouteRow, ...]:
    return (
        RerouteRow(
            priority=1,
            name="sprang_kronecker_d2_exact_product_specialization",
            role="front_door",
            decision="continue_first",
            positive_use=(
                "Sprang even-D/Kronecker surface is still live; a source theorem "
                "that emits exact P or theta2/theta2^-1 closes the theorem lane."
            ),
            first_falsifier=(
                "formula language, dlog, distribution, or cohomology class "
                "without the exact C,D,K product and orientation"
            ),
            next_action=(
                "instantiate any Sprang D=2 hit through exact-product intake "
                "and the anti-invariant producer contract"
            ),
            row_ok=(
                sprang.row_ok
                and sprang.direct_closing_rows == 0
                and sprang.hypothetical_closing_rows == 1
            ),
        ),
        RerouteRow(
            priority=2,
            name="kubert_lang_mixed_exponent_product_search",
            role="front_door",
            decision="continue_second",
            positive_use=(
                "Exact source packet and theta2 footprints survive the "
                "Kubert-Lang congruence screen at mixed levels 507/12675."
            ),
            first_falsifier=(
                "C169 projection, exponent hygiene, or generator theorem without "
                "the mixed C3 row graph and T edge"
            ),
            next_action=(
                "search only for a theorem-legal mixed-level lift/product and "
                "run it through the KL exponent screen plus theorem-hit router"
            ),
            row_ok=(
                kl.row_ok
                and kl.exact_payloads_survive_congruence_screen
                and kl.source_packet_profile.support == 6
                and kl.theta2_inverse_profile.support == 300
                and kl.theta2_profile.support == 300
            ),
        ),
        RerouteRow(
            priority=3,
            name="ksy_normalized_y_exact_distribution",
            role="front_door",
            decision="continue_if_exact_product",
            positive_use=(
                "The finite target is literally a normalized-y product, so KSY-y "
                "formula language remains useful if upgraded to exact product."
            ),
            first_falsifier=(
                "single y-value, ray-class generation, or formula y(Q) language "
                "without the full 75-atom distribution"
            ),
            next_action=(
                "accept only exact P/theta2 divisor-additive output with mixed "
                "graph, equal weights, orientation, and arithmetic producer"
            ),
            row_ok=(
                koo_shin.row_ok
                and sprang.row_ok
                and kl.row_ok
                and not koo_shin.normalized_y_product_emitted
            ),
        ),
        RerouteRow(
            priority=4,
            name="koo_shin_2010_theorem52_root_descent",
            role="helper",
            decision="keep_as_helper_not_target",
            positive_use=(
                "Use as constant-product rigidity and l-th-root descent context "
                "after a separate mixed-level producer is found."
            ),
            first_falsifier=(
                "trying to close through prime-level products modulo +/- without "
                "mixed C3 x C169 data"
            ),
            next_action=(
                "do not spend a lane on Theorem 5.2 alone; cite it only inside "
                "a future mixed-product theorem proof"
            ),
            row_ok=(
                koo_shin.row_ok
                and koo_shin.intake_decision == "reject_prime_power_only_missing_mixed_lift"
                and not koo_shin.exact_p25_product_emitted
                and not koo_shin.mixed_c3_c169_graph_emitted
            ),
        ),
        RerouteRow(
            priority=5,
            name="c169_or_prime_level_projection_closer",
            role="killed_shadow",
            decision="kill_projection_only",
            positive_use=(
                "Projection can be used as a necessary congruence/root-descent "
                "screen, never as a p25 payload."
            ),
            first_falsifier=(
                "prime-power projection loses right row data, the mixed graph, "
                "and the T=(2,113) edge"
            ),
            next_action=(
                "reject unless the claim restores the mixed-level lift and exact "
                "p25 finite intake"
            ),
            row_ok=kl.row_ok and kl.prime_power_projection_is_finite_insufficient,
        ),
    )


def profile_post_koo_shin_2010_reroute() -> PostKooShin2010RerouteProfile:
    koo_shin = profile_actual_theorem52_verdict()
    sprang = profile_sprang_even_d_specialization_contract()
    kl = profile_kl_exponent_matrix_screen()
    rows = reroute_rows(koo_shin, sprang, kl)

    continue_rows = sum(row.role == "front_door" for row in rows)
    helper_rows = sum(row.role == "helper" for row in rows)
    killed_rows = sum(row.role == "killed_shadow" for row in rows)
    direct_koo_shin_killed = (
        koo_shin.row_ok
        and koo_shin.intake_decision == "reject_prime_power_only_missing_mixed_lift"
        and not koo_shin.exact_p25_product_emitted
    )
    prime_projection_killed = kl.row_ok and kl.prime_power_projection_is_finite_insufficient
    exact_front_doors = sum(
        row.name
        in {
            "sprang_kronecker_d2_exact_product_specialization",
            "kubert_lang_mixed_exponent_product_search",
            "ksy_normalized_y_exact_distribution",
        }
        for row in rows
    )

    expected_names = (
        "sprang_kronecker_d2_exact_product_specialization",
        "kubert_lang_mixed_exponent_product_search",
        "ksy_normalized_y_exact_distribution",
        "koo_shin_2010_theorem52_root_descent",
        "c169_or_prime_level_projection_closer",
    )
    row_ok = (
        koo_shin.row_ok
        and sprang.row_ok
        and kl.row_ok
        and tuple(row.name for row in rows) == expected_names
        and continue_rows == 3
        and helper_rows == 1
        and killed_rows == 1
        and direct_koo_shin_killed
        and prime_projection_killed
        and exact_front_doors == 3
        and all(row.row_ok for row in rows)
    )
    return PostKooShin2010RerouteProfile(
        koo_shin_actual_ok=koo_shin.row_ok,
        sprang_even_d_ok=sprang.row_ok,
        kl_exponent_screen_ok=kl.row_ok,
        rows=rows,
        continue_rows=continue_rows,
        helper_rows=helper_rows,
        killed_rows=killed_rows,
        direct_koo_shin_closer_killed=direct_koo_shin_killed,
        prime_projection_killed=prime_projection_killed,
        exact_product_front_doors=exact_front_doors,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_koo_shin_2010_reroute()
    print("p25 KSY-y post-Koo-Shin-2010 reroute gate")
    print("inputs")
    print(f"  koo_shin_actual_ok={int(profile.koo_shin_actual_ok)}")
    print(f"  sprang_even_d_ok={int(profile.sprang_even_d_ok)}")
    print(f"  kl_exponent_screen_ok={int(profile.kl_exponent_screen_ok)}")
    print("reroute_rows")
    for row in profile.rows:
        print(
            "  "
            f"priority={row.priority} name={row.name} role={row.role} "
            f"decision={row.decision} ok={int(row.row_ok)} "
            f"falsifier={row.first_falsifier}"
        )
    print("counts")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  helper_rows={profile.helper_rows}")
    print(f"  killed_rows={profile.killed_rows}")
    print(f"  exact_product_front_doors={profile.exact_product_front_doors}")
    print(f"  direct_koo_shin_closer_killed={int(profile.direct_koo_shin_closer_killed)}")
    print(f"  prime_projection_killed={int(profile.prime_projection_killed)}")
    print("interpretation")
    print("  koo_shin_2010_theorem52_is_helper_not_target=1")
    print("  c169_prime_projection_alone_is_killed=1")
    print("  first_doors_are_sprang_D2_KL_mixed_and_KSY_exact_product=1")
    print(f"ksy_y_post_koo_shin_2010_reroute_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-Koo-Shin-2010 reroute regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
