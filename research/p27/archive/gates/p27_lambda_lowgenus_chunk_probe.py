#!/usr/bin/env python3
"""Chunked reference runner for lambda monic cubic/quartic screens."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p27_lambda_lowgenus_verify import DEFAULT_PACKET, load_packet, target_entry


@dataclass(frozen=True)
class Hit:
    polarity: int
    coeffs: tuple[int, ...]


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
            for constant in range(p):
                if table[(constant + offset) % p] == sign:
                    mask |= 1 << constant
            masks[sign].append(mask)
    return masks


def decode_index(index: int, q: int, degree: int) -> tuple[int, ...]:
    coeffs = []
    for power in range(degree - 1):
        divisor = q ** (degree - 2 - power)
        coeff = index // divisor
        coeffs.append(coeff)
        index -= coeff * divisor
    return tuple(coeffs)


def scan_chunk(
    target: dict,
    degree: int,
    start: int,
    count: int,
    sample_limit: int,
) -> tuple[dict[str, int], list[Hit]]:
    q = int(target["field"])
    rows = [(int(row["lambda"]) % q, int(row["sign"])) for row in target["rows"]]
    powers = [
        [pow(lam, power, q) for power in range(degree + 1)]
        for lam, _sign in rows
    ]
    masks = shifted_masks(q)
    full_constant = (1 << q) - 1
    search_size = q ** (degree - 1)
    end = min(start + count, search_size)
    stats = {
        "field": q,
        "degree": degree,
        "rows": len(rows),
        "start": start,
        "requested_count": count,
        "end": end,
        "tuples_scanned": 0,
        "polarity_1_hits": 0,
        "polarity_-1_hits": 0,
        "exact_polynomials": 0,
    }
    hits: list[Hit] = []
    for index in range(start, end):
        coeffs = decode_index(index, q, degree)
        stats["tuples_scanned"] += 1
        for polarity in (1, -1):
            intersection = full_constant
            for (_lam, target_sign), row_powers in zip(rows, powers):
                desired = polarity * target_sign
                offset = row_powers[degree]
                for coeff, power in zip(coeffs, range(degree - 1, 0, -1)):
                    offset = (offset + coeff * row_powers[power]) % q
                intersection &= masks[desired][offset]
                if not intersection:
                    break
            if intersection:
                hit_count = intersection.bit_count()
                stats[f"polarity_{polarity}_hits"] += hit_count
                stats["exact_polynomials"] += hit_count
                while intersection and len(hits) < sample_limit:
                    constant = first_bit(intersection)
                    hits.append(Hit(polarity=polarity, coeffs=(*coeffs, constant)))
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
    parser.add_argument("--degree", type=int, choices=(3, 4), required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    target = target_entry(packet, args.field, args.family)
    stats, hits = scan_chunk(target, args.degree, args.start, args.count, args.sample_limit)
    print("p27 lambda low-genus chunk probe")
    print(f"packet = {args.packet}")
    print(f"field = {args.field}")
    print(f"family = {args.family}")
    print(f"degree = {args.degree}")
    print_stats(stats)
    print("hit_samples:")
    for hit in hits:
        print(f"  polarity={hit.polarity} coeffs={','.join(str(c) for c in hit.coeffs)}")
    print("p27_lambda_lowgenus_chunk_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
