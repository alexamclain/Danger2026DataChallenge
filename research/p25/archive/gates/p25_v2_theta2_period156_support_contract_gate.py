#!/usr/bin/env python3
"""Replay the v2 theta2 period-156 support contract.

This is a deep support check, not the lightweight cockpit check. It restores
the archive/harness import path, reruns the Lane B theta2 finite-side gates,
and records the exact boundary: period-156 theta2 data is an accepted support
payload, but still needs a challenge-legal arithmetic source theorem.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for path in (GATE_DIR, HARNESS_DIR):
    sys.path.insert(0, str(path))

from p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate import (  # noqa: E402
    profile_arithmetic_producer_contract,
)
from p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate import (  # noqa: E402
    profile_d2_theorem_obligation,
)
from p25_laneB_robert_ksy_theta2_factor_period_certificate_gate import (  # noqa: E402
    profile_factor_period_certificate,
)


@dataclass(frozen=True)
class Theta2Period156SupportContract:
    factor_period_ok: bool
    support_period: int
    period_scale: tuple[int, int]
    factor_support_budget: int
    expanded_period_budget: int
    proper_divisors_fail: bool
    arithmetic_contract_ok: bool
    accepted_interfaces: tuple[str, ...]
    value_branch_count: int
    value_unit_without_branch_rejected: bool
    d2_obligation_ok: bool
    accepted_obligations: tuple[str, ...]
    rejected_shortcuts: tuple[str, ...]
    current_arithmetic_producers: int
    row_ok: bool


def build_contract() -> Theta2Period156SupportContract:
    period = profile_factor_period_certificate()
    contract = profile_arithmetic_producer_contract()
    d2 = profile_d2_theorem_obligation()

    accepted_interfaces = tuple(row.name for row in contract.accepted_interfaces)
    accepted_obligations = tuple(row.name for row in d2.accepted_obligations)
    rejected_shortcuts = tuple(row.name for row in d2.rejected_shortcuts)
    value_rejected = any(
        row.name == "theta2_value_unit_without_branch" and not row.finite_verifier_accepts
        for row in contract.rejected_or_conditional_interfaces
    )
    current_arithmetic_producers = 0

    row_ok = (
        period.row_ok
        and period.support_period == 156
        and period.period_scale == (61, 1)
        and period.factor_support_budget == 31
        and period.telescoping_period_subcheck_budget == 900
        and period.proper_divisors_all_fail_to_fix_theta2
        and contract.row_ok
        and "sparse_theta2_divisor" in accepted_interfaces
        and "sparse_theta2_inverse_divisor" in accepted_interfaces
        and "compact_ksy_theta2" in accepted_interfaces
        and contract.value_branch_count == 11
        and value_rejected
        and d2.row_ok
        and "divisor_theta2_or_inverse" in accepted_obligations
        and "compact_ksy_center_half_orientation" in accepted_obligations
        and "source_packet_or_factor_shadow" in accepted_obligations
        and "value_unit_without_branch" in rejected_shortcuts
        and current_arithmetic_producers == 0
    )

    return Theta2Period156SupportContract(
        factor_period_ok=period.row_ok,
        support_period=period.support_period,
        period_scale=period.period_scale,
        factor_support_budget=period.factor_support_budget,
        expanded_period_budget=period.telescoping_period_subcheck_budget,
        proper_divisors_fail=period.proper_divisors_all_fail_to_fix_theta2,
        arithmetic_contract_ok=contract.row_ok,
        accepted_interfaces=accepted_interfaces,
        value_branch_count=contract.value_branch_count,
        value_unit_without_branch_rejected=value_rejected,
        d2_obligation_ok=d2.row_ok,
        accepted_obligations=accepted_obligations,
        rejected_shortcuts=rejected_shortcuts,
        current_arithmetic_producers=current_arithmetic_producers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    print("p25 v2 theta2 period-156 support contract")
    print(f"factor_period_ok={int(contract.factor_period_ok)}")
    print(f"support_period={contract.support_period}")
    print(f"period_scale={contract.period_scale}")
    print(f"factor_support_budget={contract.factor_support_budget}")
    print(f"expanded_period_budget={contract.expanded_period_budget}")
    print(f"proper_divisors_fail={int(contract.proper_divisors_fail)}")
    print(f"arithmetic_contract_ok={int(contract.arithmetic_contract_ok)}")
    print("accepted_interfaces")
    for name in contract.accepted_interfaces:
        print(f"  {name}")
    print(f"value_branch_count={contract.value_branch_count}")
    print(f"value_unit_without_branch_rejected={int(contract.value_unit_without_branch_rejected)}")
    print(f"d2_obligation_ok={int(contract.d2_obligation_ok)}")
    print("accepted_obligations")
    for name in contract.accepted_obligations:
        print(f"  {name}")
    print("rejected_shortcuts")
    for name in contract.rejected_shortcuts:
        print(f"  {name}")
    print(f"current_arithmetic_producers={contract.current_arithmetic_producers}")
    print(f"p25_v2_theta2_period156_support_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
