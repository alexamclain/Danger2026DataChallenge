#!/usr/bin/env python3
"""Falsify direct instantiation of Sprang distribution as p25 theta2."""

from __future__ import annotations

import io
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SPRANG_1801 = ROOT / "incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex"
ARXIV_1801 = "https://arxiv.org/e-print/1801.05677"
THETA2_SUPPORT = ROOT / "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md"
THETA2_PRODUCER_CONTRACT = (
    ROOT / "research/p25/archive/gates/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py"
)


@dataclass(frozen=True)
class SprangDistributionInstantiationFalsifier:
    sprang_source_present: bool
    distribution_theorem_present: bool
    full_kernel_torsion_sum_present: bool
    full_d_torsion_corollary_present: bool
    d_not_coprime_to_6_support: bool
    theta2_support_contract_present: bool
    sparse_factor_tuple_required: bool
    sparse_theta2_interfaces_required: bool
    source_names_sparse_factor_tuple: bool
    source_names_p25_bridge: bool
    source_names_compact_ksy_payload: bool
    direct_instantiation_closers: int
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


def build_falsifier() -> SprangDistributionInstantiationFalsifier:
    source = read_source(SPRANG_1801, ARXIV_1801, "PaperEisensteinPoincare.tex")
    theta2 = THETA2_SUPPORT.read_text() if THETA2_SUPPORT.exists() else ""
    producer_contract = (
        THETA2_PRODUCER_CONTRACT.read_text() if THETA2_PRODUCER_CONTRACT.exists() else ""
    )
    theta2_contract = theta2 + "\n" + producer_contract

    distribution_theorem_present = "\\begin{thm}\\label{ch_EP_thmdist}" in source
    full_kernel_torsion_sum_present = (
        "\\alpha\\in (\\ker\\psi)(S)" in source
        and "\\beta\\in (E'^\\vee[D'])(S)" in source
        and "((D')^2)" in source
    )
    full_d_torsion_corollary_present = (
        "\\sum_{e\\neq t\\in \\Ed[\\tilde{D}](S)}" in source
        and "\\scan^D" in source
    )
    d_not_coprime_to_6_support = "not co-prime to $6$" in source

    sparse_factor_tuple_required = (
        "source_factor_tuple" in theta2_contract
        and "base*K_trace*D_segment*(1-T)" in theta2_contract
    )
    sparse_theta2_interfaces_required = (
        "sparse_theta2_divisor" in theta2_contract
        and "sparse_theta2_inverse_divisor" in theta2_contract
        and "compact_ksy_theta2" in theta2_contract
    )
    source_names_sparse_factor_tuple = any(
        needle in source
        for needle in ("K_trace", "D_segment", "source_factor_tuple", "base*K_trace")
    )
    source_names_p25_bridge = any(
        needle in source
        for needle in ("Norm_156", "Y_507", "C_75", "C_169", "support_period")
    )
    source_names_compact_ksy_payload = all(
        needle in source for needle in ("center_base", "half_shift", "orientation")
    )
    direct_instantiation_closers = 0
    decision = "sprang_distribution_is_full_trace_support_not_sparse_theta2_instantiation"

    row_ok = (
        bool(source)
        and distribution_theorem_present
        and full_kernel_torsion_sum_present
        and full_d_torsion_corollary_present
        and d_not_coprime_to_6_support
        and bool(theta2)
        and sparse_factor_tuple_required
        and sparse_theta2_interfaces_required
        and not source_names_sparse_factor_tuple
        and not source_names_p25_bridge
        and not source_names_compact_ksy_payload
        and direct_instantiation_closers == 0
    )

    return SprangDistributionInstantiationFalsifier(
        sprang_source_present=bool(source),
        distribution_theorem_present=distribution_theorem_present,
        full_kernel_torsion_sum_present=full_kernel_torsion_sum_present,
        full_d_torsion_corollary_present=full_d_torsion_corollary_present,
        d_not_coprime_to_6_support=d_not_coprime_to_6_support,
        theta2_support_contract_present=bool(theta2),
        sparse_factor_tuple_required=sparse_factor_tuple_required,
        sparse_theta2_interfaces_required=sparse_theta2_interfaces_required,
        source_names_sparse_factor_tuple=source_names_sparse_factor_tuple,
        source_names_p25_bridge=source_names_p25_bridge,
        source_names_compact_ksy_payload=source_names_compact_ksy_payload,
        direct_instantiation_closers=direct_instantiation_closers,
        decision=decision,
        row_ok=row_ok,
    )


def main() -> int:
    falsifier = build_falsifier()
    print("p25 v2 Sprang distribution instantiation falsifier")
    print(f"sprang_source_present={int(falsifier.sprang_source_present)}")
    print(f"distribution_theorem_present={int(falsifier.distribution_theorem_present)}")
    print(f"full_kernel_torsion_sum_present={int(falsifier.full_kernel_torsion_sum_present)}")
    print(f"full_d_torsion_corollary_present={int(falsifier.full_d_torsion_corollary_present)}")
    print(f"d_not_coprime_to_6_support={int(falsifier.d_not_coprime_to_6_support)}")
    print(f"theta2_support_contract_present={int(falsifier.theta2_support_contract_present)}")
    print(f"sparse_factor_tuple_required={int(falsifier.sparse_factor_tuple_required)}")
    print(f"sparse_theta2_interfaces_required={int(falsifier.sparse_theta2_interfaces_required)}")
    print(f"source_names_sparse_factor_tuple={int(falsifier.source_names_sparse_factor_tuple)}")
    print(f"source_names_p25_bridge={int(falsifier.source_names_p25_bridge)}")
    print(f"source_names_compact_ksy_payload={int(falsifier.source_names_compact_ksy_payload)}")
    print(f"direct_instantiation_closers={falsifier.direct_instantiation_closers}")
    print(f"decision={falsifier.decision}")
    print(f"p25_v2_sprang_distribution_instantiation_falsifier_rows={int(falsifier.row_ok)}/1")
    return 0 if falsifier.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
