#!/usr/bin/env python3
"""Chunked reference runner for the p27 K-line quartic screen."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p27_kline_quartic_verify import DEFAULT_PACKET, load_packet, target_entry


@dataclass(frozen=True)
class Hit:
    polarity: int
    coeffs: tuple[int, int, int, int]


def first_bit(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for value in range(1, p):
        table[value] = 1 if pow(value, (p - 1) // 2, p) == 1 else -1
    return table


def shifted_masks(p: int) -> dict[int, list[int]]:
    table = legendre_table(p)
    masks = {1: [], -1: []}
    for sign in (1, -1):
        for offset in range(p):
            mask = 0
            for d in range(p):
                if table[(d + offset) % p] == sign:
                    mask |= 1 << d
            masks[sign].append(mask)
    return masks


def decode_index(index: int, q: int) -> tuple[int, int, int]:
    a = index // (q * q)
    rem = index - a * q * q
    b = rem // q
    c = rem - b * q
    return a, b, c


def scan_chunk(target: dict, start: int, count: int, sample_limit: int) -> tuple[dict[str, int], list[Hit]]:
    q = int(target["field"])
    rows = [(int(row["K"]) % q, int(row["sign"])) for row in target["rows"]]
    powers = [(K, K * K % q, K * K % q * K % q, pow(K, 4, q)) for K, _ in rows]
    masks = shifted_masks(q)
    full_d = (1 << q) - 1
    end = min(start + count, q * q * q)
    stats = {
        "field": q,
        "rows": len(rows),
        "start": start,
        "requested_count": count,
        "end": end,
        "triples_scanned": 0,
        "polarity_1_hits": 0,
        "polarity_-1_hits": 0,
        "exact_quartics": 0,
    }
    hits: list[Hit] = []
    for index in range(start, end):
        a, b, c = decode_index(index, q)
        stats["triples_scanned"] += 1
        for polarity in (1, -1):
            intersection = full_d
            for (_K, target_sign), (K, K2, K3, K4) in zip(rows, powers):
                desired = polarity * target_sign
                offset = (K4 + a * K3 + b * K2 + c * K) % q
                intersection &= masks[desired][offset]
                if not intersection:
                    break
            if intersection:
                hit_count = intersection.bit_count()
                stats[f"polarity_{polarity}_hits"] += hit_count
                stats["exact_quartics"] += hit_count
                while intersection and len(hits) < sample_limit:
                    d = first_bit(intersection)
                    hits.append(Hit(polarity=polarity, coeffs=(a, b, c, d)))
                    intersection &= intersection - 1
    return stats, hits


def print_stats(stats: dict[str, int]) -> None:
    print("chunk_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=DEFAULT_PACKET)
    parser.add_argument("--field", type=int, required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    target = target_entry(packet, args.field, args.family)
    stats, hits = scan_chunk(target, args.start, args.count, args.sample_limit)
    print("p27 K-line quartic chunk probe")
    print(f"packet = {args.packet}")
    print(f"field = {args.field}")
    print(f"family = {args.family}")
    print_stats(stats)
    print("hit_samples:")
    for hit in hits:
        a, b, c, d = hit.coeffs
        print(f"  polarity={hit.polarity} coeffs={a},{b},{c},{d}")
    print("p27_kline_quartic_chunk_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
