#!/usr/bin/env python3
"""Guard the p25 first-class-run v2 operating shape.

This is a lightweight policy gate, not a theorem replay.  It checks that the
canonical cockpit still says the practical fleet is primary, H0 and conductor
39 are the only first-pass theorem fronts, exact-P is second-pass, and support
microscopes remain subordinate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


MARKER = "p25_v2_first_class_run_v2_plan_guard_rows=1/1"


@dataclass(frozen=True)
class RequiredText:
    path: str
    snippets: tuple[str, ...]


@dataclass(frozen=True)
class PlanGuard:
    required_snippets_ok: int
    required_snippets_total: int
    private_public_boundary_ok: bool
    row_ok: bool


REQUIRED_TEXT = (
    RequiredText(
        "frontier.md",
        (
            "Practical search",
            "only concrete route to a",
            "10-worker `x16halvenonsplit`",
            "H0",
            "Conductor 39",
            "first-pass moonshot fronts",
            "same four finite targets",
            "No `vpp.py`-verified p25 triple exists yet.",
            "support microscopes inside",
        ),
    ),
    RequiredText(
        "operations/run-status.md",
        (
            "mode = x16halvenonsplit",
            "workers = 10",
            "src/launch_fleet_detached.py",
            "src/launch_status_heartbeat.py",
            "next_seed_base = 27094580",
            "Do not start a separate manual watcher",
            "partial unexplained termination, not exhausted and not a hit",
        ),
    ),
    RequiredText(
        "lanes/practical-search.md",
        (
            "`x16halvenonsplit` remains the best practical route",
            "10-worker fleet",
            "p mod 8 = 5",
            "no p24 square-root",
            "partial unexplained termination",
            "seed_base=27094580",
            "at least `0.85x`",
            "clears the `1.75x` break-even",
        ),
    ),
    RequiredText(
        "lanes/h0.md",
        (
            "one of the two best first-pass moonshot targets",
            "finite divisor/additive",
            "Hilbert-90 boundary",
            "Norm_156(Y_507)",
            "Source certification alone",
            "identical to the conductor-39 legal sparse",
            "zero current theorem instances",
        ),
    ),
    RequiredText(
        "lanes/conductor39.md",
        (
            "other first-pass moonshot target",
            "U_chi",
            "chi_3 tensor chi_13",
            "Yang lift",
            "finite divisor/additive theorem",
            "Prime projections",
            "identical to the H0/H0-translate finite target",
            "Conductor-39 source language still has to feed one of those finite routes",
        ),
    ),
    RequiredText(
        "lanes/exact-p.md",
        (
            "heavier upstream route",
            "75 atoms are fixed payload factors, not 75 independent tries",
            "75 -> 300 -> 12 -> 312 -> 156",
            "not reversible from unified support-156",
            "exact-P source payloads at zero",
        ),
    ),
    RequiredText(
        "concepts/transfer-matrix.md",
        (
            "Literal p24 CM/Lang transfer is dead",
            "p25-specific support microscopes",
            "tied to H0, conductor 39, or exact-P",
        ),
    ),
    RequiredText(
        "AGENTS.md",
        (
            "public",
            "mirror",
            "operations/practical-search, H0",
            "support microscope",
            "Lane A killed",
            "Lane B and Lane C",
        ),
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text()


def has_snippet(text: str, snippet: str) -> bool:
    compact_text = re.sub(r"\s+", " ", text)
    compact_snippet = re.sub(r"\s+", " ", snippet)
    return compact_snippet in compact_text


def build_guard(root: Path) -> PlanGuard:
    ok = 0
    total = 0
    for required in REQUIRED_TEXT:
        text = read(root, required.path)
        for snippet in required.snippets:
            total += 1
            ok += int(has_snippet(text, snippet))

    agents = read(root, "AGENTS.md")
    boundary_ok = (
        (
            "Treat `research/p25` in this workspace as the live private cockpit"
            in agents
            and "public `Danger2026DataChallenge/research/p25` copy as a mirror"
            in agents
        )
        or (
            "Treat the local private p25 workspace as the live cockpit" in agents
            and "public `Danger2026DataChallenge/research/p25` copy as a mirror"
            in agents
        )
    )
    row_ok = ok == total and boundary_ok
    return PlanGuard(
        required_snippets_ok=ok,
        required_snippets_total=total,
        private_public_boundary_ok=boundary_ok,
        row_ok=row_ok,
    )


def main() -> int:
    guard = build_guard(research_root())
    print("p25 first-class-run v2 plan guard")
    print(f"required_snippets_ok={guard.required_snippets_ok}/{guard.required_snippets_total}")
    print(f"private_public_boundary_ok={int(guard.private_public_boundary_ok)}")
    print(f"{MARKER if guard.row_ok else 'p25_v2_first_class_run_v2_plan_guard_rows=0/1'}")
    return 0 if guard.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
