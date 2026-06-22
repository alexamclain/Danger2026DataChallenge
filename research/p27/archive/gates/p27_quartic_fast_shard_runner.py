#!/usr/bin/env python3
"""Run the fast C quartic chunk oracle over a full B/K target in shards."""

from __future__ import annotations

import argparse
import math
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from p27_quartic_target_export import COORDS, export_rows


SCRIPT_DIR = Path(__file__).resolve().parent
FAST_C = SCRIPT_DIR / "p27_quartic_chunk_fast.c"


def compile_binary(out_dir: Path) -> Path:
    binary = out_dir / "p27_quartic_chunk_fast"
    cmd = ["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-o", str(binary), str(FAST_C)]
    subprocess.run(cmd, check=True)
    return binary


def load_target(coordinate: str, packet_path: str | None, field: int, family: str) -> dict:
    default_packet, loader, target_lookup, _row_key = COORDS[coordinate]
    packet = loader(packet_path or default_packet)
    return target_lookup(packet, field, family)


def write_rows(out_dir: Path, coordinate: str, target: dict) -> Path:
    _default_packet, _loader, _target_lookup, row_key = COORDS[coordinate]
    rows_path = out_dir / f"{coordinate}_{target['field']}_{target['family']}_rows.txt"
    rows_path.write_text(export_rows(target, row_key))
    return rows_path


def parse_stats(text: str) -> dict[str, int | float | str]:
    stats: dict[str, int | float | str] = {}
    for line in text.splitlines():
        if " = " not in line:
            continue
        key, value = line.split(" = ", 1)
        key = key.strip()
        value = value.strip()
        if key in {"elapsed_seconds", "throughput_triples_per_second"}:
            stats[key] = float(value)
        else:
            try:
                stats[key] = int(value)
            except ValueError:
                stats[key] = value
    return stats


def run_shard(
    binary: Path,
    rows_path: Path,
    out_dir: Path,
    start: int,
    count: int,
    sample_limit: int,
    write_shard_logs: bool,
) -> tuple[int, int, dict[str, int | float | str], str]:
    cmd = [str(binary), str(rows_path), str(start), str(count), str(sample_limit)]
    proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
    end = start + count
    log_path = out_dir / f"shard_{start}_{end}.log"
    if write_shard_logs or proc.returncode != 0:
        log_path.write_text(proc.stdout + proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"shard failed start={start} count={count}: {log_path}")
    return start, count, parse_stats(proc.stdout), proc.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coordinate", choices=sorted(COORDS), required=True)
    parser.add_argument("--packet")
    parser.add_argument("--field", type=int, required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=50_000_000)
    parser.add_argument("--max-triples", type=int, default=0)
    parser.add_argument("--sample-limit", type=int, default=8)
    parser.add_argument("--write-shard-logs", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = load_target(args.coordinate, args.packet, args.field, args.family)
    q = int(target["field"])
    full_total = q**3
    total = min(full_total, args.max_triples) if args.max_triples else full_total
    chunks = [
        (start, min(args.chunk_size, total - start))
        for start in range(0, total, args.chunk_size)
    ]

    binary = compile_binary(out_dir)
    rows_path = write_rows(out_dir, args.coordinate, target)
    summary_path = out_dir / "SUMMARY.txt"

    print("p27 quartic fast shard runner")
    print(f"coordinate = {args.coordinate}")
    print(f"field = {args.field}")
    print(f"family = {args.family}")
    print(f"rows = {target['row_count']}")
    print(f"plus = {target['plus_count']}")
    print(f"minus = {target['minus_count']}")
    print(f"total_triples = {total}")
    print(f"full_triples = {full_total}")
    print(f"workers = {args.workers}")
    print(f"chunk_size = {args.chunk_size}")
    print(f"chunks = {len(chunks)}")
    print(f"out_dir = {out_dir}")

    wall_start = time.time()
    triples = 0
    exact = 0
    polarity_1 = 0
    polarity_minus_1 = 0
    hit_samples: list[str] = []
    completed = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                run_shard,
                binary,
                rows_path,
                out_dir,
                start,
                count,
                args.sample_limit,
                args.write_shard_logs,
            )
            for start, count in chunks
        ]
        for future in as_completed(futures):
            start, count, stats, stdout = future.result()
            completed += 1
            triples += int(stats.get("triples_scanned", 0))
            exact += int(stats.get("exact_quartics", 0))
            polarity_1 += int(stats.get("polarity_1_hits", 0))
            polarity_minus_1 += int(stats.get("polarity_-1_hits", 0))
            for line in stdout.splitlines():
                if line.startswith("hit_sample ") and len(hit_samples) < args.sample_limit:
                    hit_samples.append(line)
            if completed == 1 or completed == len(chunks) or completed % max(1, math.ceil(len(chunks) / 20)) == 0:
                elapsed = time.time() - wall_start
                rate = triples / elapsed if elapsed > 0 else 0.0
                print(
                    "progress "
                    f"{completed}/{len(chunks)} chunks "
                    f"triples={triples} exact={exact} "
                    f"wall_rate={rate:.3f}/s"
                )

    wall_seconds = time.time() - wall_start
    wall_rate = triples / wall_seconds if wall_seconds > 0 else 0.0
    summary_lines = [
        "p27 quartic fast shard summary",
        f"coordinate = {args.coordinate}",
        f"field = {args.field}",
        f"family = {args.family}",
        f"rows = {target['row_count']}",
        f"plus = {target['plus_count']}",
        f"minus = {target['minus_count']}",
        f"total_triples = {total}",
        f"full_triples = {full_total}",
        f"triples_scanned = {triples}",
        f"polarity_-1_hits = {polarity_minus_1}",
        f"polarity_1_hits = {polarity_1}",
        f"exact_quartics = {exact}",
        f"wall_seconds = {wall_seconds:.6f}",
        f"wall_throughput_triples_per_second = {wall_rate:.3f}",
        "hit_samples:",
        *(f"  {line}" for line in hit_samples),
        "p27_quartic_fast_shard_runner_rows=1/1",
    ]
    text = "\n".join(summary_lines) + "\n"
    summary_path.write_text(text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
