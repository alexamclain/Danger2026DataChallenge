#!/usr/bin/env python3
"""Trace/norm D_plus cover equation probe for p27.

This turns the C-side trace/norm D prefilter into one explicit squareclass
after the domain square root is present.  The point is not to promote the
current filter implementation; it is to name the source-cover equation that a
direct sampler or Magma/Sage quotient pass would have to exploit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from pathlib import Path
import sys


def load_gate(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


transfer = load_gate("p27_trace_norm_transfer_gate.py")
tline = load_gate("p27_tline_component_descent_gate.py")
P = transfer.P


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def dplus_core(y: int, w: int) -> tuple[int, dict[str, int]] | None:
    y %= P
    w %= P
    t = (y - 1) % P
    if t == 0:
        return None
    z = transfer.sqrt_mod(transfer.f_value(y))
    if z is None:
        return None
    C = (t * t + 2 * t - 1) % P
    B = (t * t + 1) % P
    eps_h = transfer.chi(t)
    eps_v = transfer.chi(y * C)
    if eps_h == 0 or eps_v == 0:
        return None
    hcore = (C * B + eps_h * 2 * t * z) % P
    vcore = (2 * C % P * t % P * t + eps_v * z % P * w) % P
    core = (1 - t * t) % P
    core = core * B % P
    core = core * C % P
    core = core * y % P
    core = core * vcore % P
    core = core * hcore % P
    return core, {
        "t": t,
        "z": z,
        "B": B,
        "C": C,
        "eps_h": eps_h,
        "eps_v": eps_v,
        "hcore": hcore,
        "vcore": vcore,
    }


def collect_rows(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_rows: int,
) -> tuple[Counter[str], list[tuple[int, int, dict[str, int]]]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)
    rows: list[tuple[int, int, dict[str, int]]] = []
    for y, w in points:
        comps = tline.component_values(y, w)
        if comps is None:
            stats["component_unusable"] += 1
            continue
        core_pack = dplus_core(y, w)
        if core_pack is None:
            stats["core_unusable"] += 1
            continue
        core, core_parts = core_pack
        core_chi = transfer.chi(core)
        predicted_d = -core_chi if core_chi else 0
        stats["usable_rows"] += 1
        stats[f"D_{sign_name(comps['D'])}"] += 1
        stats[f"core_{sign_name(core_chi)}"] += 1
        stats[f"eps_h_{sign_name(core_parts['eps_h'])}"] += 1
        stats[f"eps_v_{sign_name(core_parts['eps_v'])}"] += 1
        stats[f"orientation_{sign_name(core_parts['eps_h'])}_{sign_name(core_parts['eps_v'])}"] += 1
        if predicted_d != comps["D"]:
            stats["D_core_mismatch"] += 1

        relation_d = comps["T_line"] * comps["line_norm"] * comps["y"]
        if relation_d != comps["D"]:
            stats["D_Tline_relation_mismatch"] += 1

        # Because p27 is 3 mod 4, -core is square exactly when core is
        # nonsquare, i.e. exactly when D=+1 after the leading sign above.
        dplus_cover_chi = transfer.chi((-core) % P)
        if dplus_cover_chi == 1:
            stats["dplus_cover_square"] += 1
        elif dplus_cover_chi == -1:
            stats["dplus_cover_nonsquare"] += 1
        else:
            stats["dplus_cover_zero"] += 1
        if (dplus_cover_chi == 1) != (comps["D"] == 1):
            stats["dplus_cover_mismatch"] += 1

        rows.append((y, w, {**comps, **core_parts, "core": core}))
        if max_rows and len(rows) >= max_rows:
            break
    return stats, rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-rows", type=int, default=0)
    args = parser.parse_args()

    stats, _rows = collect_rows(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )

    print("p27_trace_norm_dplus_cover_probe")
    print(f"p={P}")
    print("formula:")
    print("  t=y-1")
    print("  B=t^2+1")
    print("  C=t^2+2t-1")
    print("  z^2=t*C*B")
    print("  eps_h=chi(t)")
    print("  eps_v=chi((t+1)*C)")
    print("  hcore=C*B+eps_h*2*t*z")
    print("  vcore=2*C*t^2+eps_v*z*w")
    print("  core=(1-t^2)*B*C*(t+1)*vcore*hcore")
    print("  D=-chi(core)")
    print("  D_plus iff -core is square, since p27 is 3 mod 4")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "component_unusable",
        "core_unusable",
        "usable_rows",
        "D_+1",
        "D_-1",
        "core_+1",
        "core_-1",
        "dplus_cover_square",
        "dplus_cover_nonsquare",
        "dplus_cover_zero",
        "D_core_mismatch",
        "D_Tline_relation_mismatch",
        "dplus_cover_mismatch",
    ):
        print(f"  {key}={stats[key]}")
    print("orientation_counts:")
    for eh in ("+1", "-1"):
        for ev in ("+1", "-1"):
            key = f"orientation_{eh}_{ev}"
            print(f"  {key}={stats[key]}")
    print("verdict:")
    print(f"  D_core_exact={int(stats['D_core_mismatch'] == 0 and stats['usable_rows'] > 0)}")
    print(f"  D_Tline_relation_exact={int(stats['D_Tline_relation_mismatch'] == 0 and stats['usable_rows'] > 0)}")
    print(f"  dplus_cover_exact={int(stats['dplus_cover_mismatch'] == 0 and stats['usable_rows'] > 0)}")
    print("p27_trace_norm_dplus_cover_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
