#!/usr/bin/env python3
"""Compare formal period-selector targets against sqrt(p).

The first strict trace gives an attractive order-19 quotient, but its recovery
cycle is still 14.7 billion.  The third trace's composite split ideal has a
larger quotient, but recovery degree only 3,107,441.  This script keeps those
two notions separate:

* theorem simplicity: small quotient / small character order;
* certificate practicality: small recovery degree and sub-sqrt correspondence.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)

TARGETS = [
    {
        "label": "first_trace_ell19",
        "trace": 1020608380936,
        "D_K": -739589633190799177940983,
        "class_number": 278733727154,
        "quotient": 19,
        "recovery": 14670196166,
        "correspondence_degree": 20,
        "root_unity_extension": 2,
        "note": "cleanest character-period theorem target",
    },
    {
        "label": "first_trace_ell107",
        "trace": 1020608380936,
        "D_K": -739589633190799177940983,
        "class_number": 278733727154,
        "quotient": 38,
        "recovery": 7335098083,
        "correspondence_degree": 108,
        "root_unity_extension": 2,
        "note": "smaller recovery than ell19 but still sqrt-scale",
    },
    {
        "label": "third_trace_composite_2_463_223inv",
        "trace": -1178414874616,
        "D_K": -652834595820939249713143,
        "class_number": 205880396014,
        "quotient": 66254,
        "recovery": 3107441,
        "correspondence_degree": 311808,
        "root_unity_extension": 5460,
        "note": "best balanced certificate target found so far",
    },
    {
        "label": "middle_trace_ell2_genus",
        "trace": -78903246840,
        "D_K": -998443569409526507503607,
        "class_number": 833035208344,
        "quotient": 4,
        "recovery": 208258802086,
        "correspondence_degree": 3,
        "root_unity_extension": 1,
        "note": "partial genus quotient; easy but huge recovery",
    },
    {
        "label": "middle_trace_ell11_principal_genus",
        "trace": -78903246840,
        "D_K": -998443569409526507503607,
        "class_number": 833035208344,
        "quotient": 8,
        "recovery": 104129401043,
        "correspondence_degree": 12,
        "root_unity_extension": 1,
        "note": "principal genus quotient; still recovery-scale",
    },
    {
        "label": "third_trace_unoriented_X0_206498",
        "trace": -1178414874616,
        "D_K": -652834595820939249713143,
        "class_number": 205880396014,
        "quotient": 2,
        "recovery": 102940198007,
        "correspondence_degree": 311808,
        "root_unity_extension": 1,
        "note": "plain X0 product after forgetting orientations",
    },
    {
        "label": "third_trace_ell677",
        "trace": -1178414874616,
        "D_K": -652834595820939249713143,
        "class_number": 205880396014,
        "quotient": 314,
        "recovery": 655670051,
        "correspondence_degree": 678,
        "root_unity_extension": 156,
        "note": "small quotient but large recovery",
    },
]


def main() -> None:
    print("p24 period target tradeoff audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print()
    print(
        "label quotient recovery correspondence seeded_proxy "
        "max_degree max_over_sqrt root_unity_ext note"
    )
    for target in TARGETS:
        seeded = target["recovery"] * target["correspondence_degree"]
        max_degree = max(target["quotient"], target["recovery"], target["correspondence_degree"])
        print(
            f"{target['label']:36s} "
            f"{target['quotient']:9d} {target['recovery']:12d} "
            f"{target['correspondence_degree']:14d} {seeded:14d} "
            f"{max_degree:12d} {max_degree / SQRT_P:13.6e} "
            f"{target['root_unity_extension']:14d} {target['note']}"
        )
    print()
    print("interpretation")
    print("  first_trace_ell19_has_smallest_character_order=1")
    print("  first_trace_recovery_degree_is_still_sqrt_scale_for_a_certificate=1")
    print("  third_trace_composite_has_best_balanced_formal_degrees=1")
    print("  unoriented_composite_X0_merges_good_cycles_into_index_2_components=1")
    print("  seedless_embedded_quotient_construction_remains_missing_for_all_targets=1")
    print("conclusion=third_trace_composite_is_best_certificate_target; first_trace_ell19_is_best_toy_theorem_target")


if __name__ == "__main__":
    main()
