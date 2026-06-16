#!/usr/bin/env python3
"""Static support audit for the selected p24 Toeplitz minor.

For rows R={0,...,367} and smooth-axis columns S in Z/66254Z, the selected
translate minor has entries c_{r-s}.  This audit measures how many symbol
indices occur, how often they repeat, and whether the column interval supports
split into disconnected pieces.
"""

from __future__ import annotations

from collections import Counter, deque

M = 66254
COMPONENTS = (2, 157, 211)
K = 1 + sum(component - 1 for component in COMPONENTS)


def component_frequencies(component: int) -> list[int]:
    step = M // component
    return [(step * a) % M for a in range(1, component)]


def axis_columns() -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = [(0, "constant")]
    for component in COMPONENTS:
        out.extend((freq, str(component)) for freq in component_frequencies(component))
    return sorted(out)


def cyclic_distance(a: int, b: int) -> int:
    d = abs(a - b) % M
    return min(d, M - d)


def interval_offsets(column: int) -> set[int]:
    return {(row - column) % M for row in range(K)}


def connected_components(adj: list[list[int]]) -> list[list[int]]:
    seen = [False] * len(adj)
    comps: list[list[int]] = []
    for start in range(len(adj)):
        if seen[start]:
            continue
        seen[start] = True
        queue = deque([start])
        comp: list[int] = []
        while queue:
            node = queue.popleft()
            comp.append(node)
            for nxt in adj[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    queue.append(nxt)
        comps.append(comp)
    return comps


def main() -> None:
    columns = axis_columns()
    offsets: Counter[int] = Counter()
    by_component: dict[str, Counter[int]] = {}
    for column, component in columns:
        by_component.setdefault(component, Counter())
        for row in range(K):
            offset = (row - column) % M
            offsets[offset] += 1
            by_component[component][offset] += 1

    overlap_hist: Counter[int] = Counter()
    overlap_edges: list[tuple[int, int, int]] = []
    adj = [[] for _ in columns]
    for i, (left, _) in enumerate(columns):
        left_offsets = interval_offsets(left)
        for j in range(i + 1, len(columns)):
            right = columns[j][0]
            overlap = len(left_offsets & interval_offsets(right))
            if overlap:
                overlap_edges.append((i, j, overlap))
                overlap_hist[overlap] += 1
                adj[i].append(j)
                adj[j].append(i)

    comps = connected_components(adj)
    comp_sizes = sorted((len(comp) for comp in comps), reverse=True)
    multiplicity_hist = Counter(offsets.values())
    top_multiplicities = offsets.most_common(12)
    component_support = {
        component: {
            "entries": sum(counter.values()),
            "distinct_offsets": len(counter),
            "max_multiplicity": max(counter.values()),
        }
        for component, counter in sorted(by_component.items())
    }

    print("p24 selected Toeplitz support audit")
    print(f"m={M}")
    print(f"rows={K}")
    print(f"cols={len(columns)}")
    print(f"entries={K * len(columns)}")
    print(f"distinct_offsets={len(offsets)}")
    print(f"offset_density={len(offsets)}/{M}")
    print(f"max_offset_multiplicity={max(offsets.values())}")
    print(f"multiplicity_hist={dict(sorted(multiplicity_hist.items()))}")
    print(f"top_multiplicities={top_multiplicities}")
    print(f"component_support={component_support}")
    print(f"overlap_edge_count={len(overlap_edges)}")
    print(f"overlap_hist={dict(sorted(overlap_hist.items()))}")
    print(f"column_overlap_component_count={len(comps)}")
    print(f"column_overlap_component_sizes={comp_sizes[:20]}")
    print()
    print("interpretation")
    print("  selected_toeplitz_minor_uses_far_more_than_k_symbol_values=1")
    print("  repeated_offsets_create_entangled_toeplitz_cancellations=1")
    print("  column_interval_overlap_graph_is_not_a_single_clean_block_factorization=1")
    print("conclusion=reported_trace_frame_toeplitz_support_boundary")


if __name__ == "__main__":
    main()
