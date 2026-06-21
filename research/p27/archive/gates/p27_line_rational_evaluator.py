#!/usr/bin/env python3
"""Named rational-function evaluator for p27 trace/norm line bits.

The p27 transfer gate compressed the active structure to two bits on the
quotient line of

    C: b^2 = 16 - a^4

and the elliptic model

    E: v^2 = u^3 - u,  u = 4/a^2.

This harness accepts named formulas R(a,u) and tests whether chi(R) matches
either line bit.  It is intended for theorem-shaped candidates from a
divisor/theta/additive identity, not for broad interpolation.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import importlib.util
from pathlib import Path
import sys
from typing import Any


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
P = transfer.P

ALLOWED_VARS = (
    "a",
    "a2",
    "a4",
    "u",
    "u2",
    "phi0",
    "phi0_2",
    "phi1",
    "phi1_2",
    "phim1",
    "phim1_2",
)

DEFAULT_EXPRESSIONS = (
    ("a", "a"),
    ("a_minus_2", "a-2"),
    ("a_plus_2", "a+2"),
    ("a2_minus_4", "a2-4"),
    ("a2_plus_4", "a2+4"),
    ("u", "u"),
    ("u_minus_1", "u-1"),
    ("u_plus_1", "u+1"),
    ("u2_minus_1", "u2-1"),
    ("u2_plus_1", "u2+1"),
    ("phi0", "phi0"),
    ("phi0_branch", "phi0_2+4"),
    ("phi1", "phi1"),
    ("phi1_branch", "phi1_2-6*phi1+1"),
    ("phim1", "phim1"),
    ("phim1_branch", "phim1_2+6*phim1+1"),
)


class ModularExpression:
    def __init__(self, source: str):
        self.source = source
        self.tree = ast.parse(source, mode="eval")
        self._validate(self.tree)

    def _validate(self, node: ast.AST) -> None:
        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Name,
            ast.Constant,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Pow,
            ast.Mod,
            ast.USub,
            ast.UAdd,
            ast.Load,
        )
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"unsupported syntax in {self.source!r}: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in ALLOWED_VARS:
            raise ValueError(f"unknown variable {node.id!r}; allowed: {', '.join(ALLOWED_VARS)}")
        if isinstance(node, ast.Constant) and not isinstance(node.value, int):
            raise ValueError("only integer constants are allowed")
        for child in ast.iter_child_nodes(node):
            self._validate(child)

    def eval(self, env: dict[str, int]) -> int:
        return self._eval(self.tree.body, env) % P

    def _eval(self, node: ast.AST, env: dict[str, int]) -> int:
        if isinstance(node, ast.Constant):
            return int(node.value) % P
        if isinstance(node, ast.Name):
            return env[node.id] % P
        if isinstance(node, ast.UnaryOp):
            value = self._eval(node.operand, env)
            if isinstance(node.op, ast.USub):
                return -value % P
            if isinstance(node.op, ast.UAdd):
                return value
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left, env)
            right = self._eval(node.right, env)
            if isinstance(node.op, ast.Add):
                return (left + right) % P
            if isinstance(node.op, ast.Sub):
                return (left - right) % P
            if isinstance(node.op, ast.Mult):
                return left * right % P
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError
                return left * transfer.inv(right) % P
            if isinstance(node.op, ast.Mod):
                if right == 0:
                    raise ZeroDivisionError
                return left % right
            if isinstance(node.op, ast.Pow):
                if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
                    raise ValueError("exponents must be integer constants")
                exponent = int(node.right.value)
                if exponent < 0:
                    return pow(transfer.inv(left), -exponent, P)
                return pow(left, exponent, P)
        raise ValueError(f"unsupported expression node {type(node).__name__}")


def parse_exprs(raw_exprs: list[str]) -> list[tuple[str, ModularExpression]]:
    if not raw_exprs:
        return [(name, ModularExpression(expr)) for name, expr in DEFAULT_EXPRESSIONS]
    out: list[tuple[str, ModularExpression]] = []
    for raw in raw_exprs:
        if "=" not in raw:
            raise SystemExit(f"--expr must be name=FORMULA, got {raw!r}")
        name, expr = raw.split("=", 1)
        out.append((name.strip(), ModularExpression(expr.strip())))
    return out


def env_for_a(a: int) -> dict[str, int] | None:
    a %= P
    if a == 0:
        return None
    a2 = a * a % P
    a4 = a2 * a2 % P
    u = 4 * transfer.inv(a2) % P
    u2 = u * u % P
    phi0 = (u - transfer.inv(u)) % P if u != 0 else 0
    phi1 = (u * (u + 1) % P * transfer.inv(u - 1) - 2) % P if u != 1 else 0
    phim1 = (u * (u - 1) % P * transfer.inv(u + 1) + 2) % P if u != P - 1 else 0
    return {
        "a": a,
        "a2": a2,
        "a4": a4,
        "u": u,
        "u2": u2,
        "phi0": phi0,
        "phi0_2": phi0 * phi0 % P,
        "phi1": phi1,
        "phi1_2": phi1 * phi1 % P,
        "phim1": phim1,
        "phim1_2": phim1 * phim1 % P,
    }


def collect_line_records(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_records: int,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], Counter[str]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)
    domain_by_a: dict[int, int] = {}
    for y, w in points:
        coords = transfer.quotient_coordinates(y, w)
        if coords is None:
            stats["domain_quotient_undefined"] += 1
            continue
        a, b = coords
        if (b * b - (16 - pow(a, 4, P))) % P != 0:
            stats["domain_quotient_relation_fail"] += 1
            continue
        target = transfer.chi(transfer.f_value(y))
        if target == 0:
            continue
        old = domain_by_a.get(a)
        if old is None:
            domain_by_a[a] = target
        elif old != target:
            stats["domain_inconsistent"] += 1

    quotient_rows, quotient_stats = transfer.collect_quotient_rows(points)
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    target_by_a: dict[int, int] = {}
    for a, b, target in quotient_rows:
        line_target = transfer.normalized_line_target(a, b, target, "p26_Tline")
        if line_target is None or line_target == 0:
            stats["target_line_unusable"] += 1
            continue
        old = target_by_a.get(a)
        if old is None:
            target_by_a[a] = line_target
        elif old != line_target:
            stats["target_line_inconsistent"] += 1

    domain_records = sorted(domain_by_a.items())
    target_records = sorted(target_by_a.items())
    if max_records:
        domain_records = domain_records[:max_records]
        target_records = target_records[:max_records]
    stats["domain_records"] = len(domain_records)
    stats["target_records"] = len(target_records)
    return domain_records, target_records, stats


def summarize(label: str, records: list[tuple[int, int]], name: str, expr: ModularExpression) -> None:
    signs: list[int] = []
    targets: list[int] = []
    zero_eval = eval_errors = 0
    for a, target in records:
        env = env_for_a(a)
        if env is None:
            zero_eval += 1
            continue
        try:
            value = expr.eval(env)
        except ZeroDivisionError:
            eval_errors += 1
            signs.append(0)
            targets.append(target)
            continue
        sign = transfer.chi(value)
        if sign == 0:
            zero_eval += 1
        signs.append(sign)
        targets.append(target)
    rows = len(targets)
    target_plus = sum(1 for target in targets if target == 1)
    baseline = target_plus / rows if rows else 0.0
    exact_plus = int(rows > 0 and zero_eval == 0 and all(sign == target for sign, target in zip(signs, targets)))
    exact_minus = int(rows > 0 and zero_eval == 0 and all(-sign == target for sign, target in zip(signs, targets)))
    best_orientation = "none"
    best_good = best_total = 0
    best_lift = 0.0
    for orientation, multiplier in (("plus", 1), ("minus", -1)):
        selected = [target for sign, target in zip(signs, targets) if multiplier * sign == 1]
        if not selected or baseline == 0.0:
            continue
        good = sum(1 for target in selected if target == 1)
        lift = (good / len(selected)) / baseline
        if lift > best_lift:
            best_orientation = orientation
            best_good = good
            best_total = len(selected)
            best_lift = lift
    print(
        " ".join(
            (
                "expr_summary",
                f"scope={label}",
                f"name={name}",
                f"rows={rows}",
                f"zero_eval={zero_eval}",
                f"eval_errors={eval_errors}",
                f"target_plus={target_plus}",
                f"exact_plus={exact_plus}",
                f"exact_minus={exact_minus}",
                f"best_orientation={best_orientation}",
                f"best_good={best_good}",
                f"best_total={best_total}",
                f"best_lift={best_lift:.9f}",
            )
        )
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-records", type=int, default=8192)
    parser.add_argument("--expr", action="append", default=[])
    args = parser.parse_args(argv[1:])

    expressions = parse_exprs(args.expr)
    domain_records, target_records, stats = collect_line_records(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_records=args.max_records,
    )

    print("p27_line_rational_evaluator")
    print(f"p={P}")
    print("variables: a, a2, a4, u=4/a^2, u2, phi0, phi1, phim1")
    print("two_isogeny_x:")
    print("  phi0 = u - 1/u")
    print("  phi1 = u*(u+1)/(u-1) - 2")
    print("  phim1 = u*(u-1)/(u+1) + 2")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "domain_records",
        "target_records",
        "domain_inconsistent",
        "target_line_inconsistent",
    ):
        print(f"  {key}={stats[key]}")
    for name, expr in expressions:
        summarize("domain_line", domain_records, name, expr)
        summarize("target_line", target_records, name, expr)
    print("p27_line_rational_evaluator_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
