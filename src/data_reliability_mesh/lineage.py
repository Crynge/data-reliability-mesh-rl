from __future__ import annotations

from collections import defaultdict, deque

from .models import LineageEdge


def propagate_impact(edges: list[LineageEdge], start_asset: str) -> list[dict[str, float | str]]:
    graph: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for edge in edges:
        graph[edge.source].append((edge.target, edge.propagation_probability))

    queue = deque([(start_asset, 1.0)])
    seen = {start_asset: 1.0}
    results: list[dict[str, float | str]] = []

    while queue:
        current, current_prob = queue.popleft()
        for child, edge_prob in graph.get(current, []):
            propagated = round(current_prob * edge_prob, 4)
            if propagated <= seen.get(child, 0):
                continue
            seen[child] = propagated
            queue.append((child, propagated))
            results.append({"asset_id": child, "impact_probability": propagated, "upstream": current})

    results.sort(key=lambda row: row["impact_probability"], reverse=True)
    return results


def reverse_root_causes(edges: list[LineageEdge], target_asset: str) -> list[dict[str, float | str]]:
    reverse_graph: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for edge in edges:
        reverse_graph[edge.target].append((edge.source, edge.propagation_probability))

    queue = deque([(target_asset, 1.0)])
    seen = {target_asset: 1.0}
    roots: list[dict[str, float | str]] = []

    while queue:
        current, current_prob = queue.popleft()
        for parent, edge_prob in reverse_graph.get(current, []):
            propagated = round(current_prob * edge_prob, 4)
            if propagated <= seen.get(parent, 0):
                continue
            seen[parent] = propagated
            queue.append((parent, propagated))
            roots.append({"asset_id": parent, "root_cause_probability": propagated, "downstream": current})

    roots.sort(key=lambda row: row["root_cause_probability"], reverse=True)
    return roots

