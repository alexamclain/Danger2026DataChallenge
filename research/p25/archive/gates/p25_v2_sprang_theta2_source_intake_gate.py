#!/usr/bin/env python3
"""Screen Sprang's arXiv sources against the p25 theta2 support contract."""

from __future__ import annotations

import io
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SPRANG_1801 = ROOT / "incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex"
SPRANG_1802 = ROOT / "incoming/extracted/sprang_1802_04996/deRhamRealization.tex"
ARXIV_1801 = "https://arxiv.org/e-print/1801.05677"
ARXIV_1802 = "https://arxiv.org/e-print/1802.04996"


@dataclass(frozen=True)
class SprangTheta2SourceIntake:
    source_files_present: bool
    d_not_coprime_to_6_support: bool
    p_adic_theta_support: bool
    distribution_relation_support: bool
    de_rham_kato_siegel_support: bool
    exact_theta2_payload_named: bool
    p25_bridge_named: bool
    compact_ksy_payload_named: bool
    branch_telescoping_named_for_p25: bool
    source_stage_closers: int
    decision: str
    row_ok: bool


def read_source(path: Path, url: str, member_name: str) -> str:
    if path.exists():
        return path.read_text()

    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        member = archive.extractfile(member_name)
        if member is None:
            return ""
        return member.read().decode()


def build_intake() -> SprangTheta2SourceIntake:
    text_1801 = read_source(SPRANG_1801, ARXIV_1801, "PaperEisensteinPoincare.tex")
    text_1802 = read_source(SPRANG_1802, ARXIV_1802, "deRhamRealization.tex")
    joined = text_1801 + "\n" + text_1802

    source_files_present = bool(text_1801 and text_1802)
    d_not_coprime_to_6_support = (
        "not co-prime to $6$" in text_1801
        and "Kato--Siegel" in text_1801
        and "\\dlog \\thetaD" in text_1801
    )
    p_adic_theta_support = (
        "\\begin{thm}\\label{thm_padictheta}" in text_1801
        and "\\pthetaD_{(a,b)}" in text_1801
        and "p-adic Eisenstein--Kronecker" in text_1801
    )
    distribution_relation_support = (
        "\\begin{thm}\\label{ch_EP_thmdist}" in text_1801
        and "N,D,D'" in text_1801
        and "non-zero-divisors" in text_1801
    )
    de_rham_kato_siegel_support = (
        "\\begin{prop}[{\\cite[Cor. 5.7]{EisensteinPoincare}}]\\label{prop_KatoSiegel}"
        in text_1802
        and "(\\id\\times e)^*\\scan^D=d\\log \\thetaD" in text_1802
    )

    exact_theta2_payload_named = any(
        needle in joined
        for needle in (
            "theta2",
            "theta_2",
            "theta^2",
            "sparse_theta2",
            "theta2_inverse",
        )
    )
    p25_bridge_named = any(
        needle in joined
        for needle in (
            "Norm_156",
            "Y_507",
            "C_75",
            "C_169",
            "support_period",
        )
    )
    compact_ksy_payload_named = all(
        needle in joined
        for needle in ("center_base", "half_shift", "orientation")
    )
    branch_telescoping_named_for_p25 = any(
        needle in joined
        for needle in (
            "period-156",
            "period 156",
            "branch/root/telescoping",
            "branch selection",
            "telescoping context",
        )
    )
    source_stage_closers = 0
    decision = "d2_support_source_not_theta2_closer"
    row_ok = (
        source_files_present
        and d_not_coprime_to_6_support
        and p_adic_theta_support
        and distribution_relation_support
        and de_rham_kato_siegel_support
        and not exact_theta2_payload_named
        and not p25_bridge_named
        and not compact_ksy_payload_named
        and not branch_telescoping_named_for_p25
        and source_stage_closers == 0
    )

    return SprangTheta2SourceIntake(
        source_files_present=source_files_present,
        d_not_coprime_to_6_support=d_not_coprime_to_6_support,
        p_adic_theta_support=p_adic_theta_support,
        distribution_relation_support=distribution_relation_support,
        de_rham_kato_siegel_support=de_rham_kato_siegel_support,
        exact_theta2_payload_named=exact_theta2_payload_named,
        p25_bridge_named=p25_bridge_named,
        compact_ksy_payload_named=compact_ksy_payload_named,
        branch_telescoping_named_for_p25=branch_telescoping_named_for_p25,
        source_stage_closers=source_stage_closers,
        decision=decision,
        row_ok=row_ok,
    )


def main() -> int:
    intake = build_intake()
    print("p25 v2 Sprang theta2 source intake")
    print(f"source_files_present={int(intake.source_files_present)}")
    print(f"d_not_coprime_to_6_support={int(intake.d_not_coprime_to_6_support)}")
    print(f"p_adic_theta_support={int(intake.p_adic_theta_support)}")
    print(f"distribution_relation_support={int(intake.distribution_relation_support)}")
    print(f"de_rham_kato_siegel_support={int(intake.de_rham_kato_siegel_support)}")
    print(f"exact_theta2_payload_named={int(intake.exact_theta2_payload_named)}")
    print(f"p25_bridge_named={int(intake.p25_bridge_named)}")
    print(f"compact_ksy_payload_named={int(intake.compact_ksy_payload_named)}")
    print(f"branch_telescoping_named_for_p25={int(intake.branch_telescoping_named_for_p25)}")
    print(f"source_stage_closers={intake.source_stage_closers}")
    print(f"decision={intake.decision}")
    print(f"p25_v2_sprang_theta2_source_intake_rows={int(intake.row_ok)}/1")
    return 0 if intake.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
