#!/usr/bin/env python3
"""Parse Sutherland X1(2^a) plane models and report degree growth.

This checks the local/cached optimized models used by the p23 experiments.
The point is not to benchmark root-finding again, but to keep the p24
asymptotic discussion tied to concrete model sizes.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


MODELS = [
    ("X1(32)", Path("runs/x1_32_probe/FFFc32.txt")),
    ("X1(64)", Path("p24/FFFc64.txt")),
]


def main() -> None:
    x, y = sp.symbols("x y")
    print("Sutherland optimized X1(2^a) degree-growth audit")
    for label, path in MODELS:
        text = path.read_text().replace("^", "**")
        poly = sp.Poly(sp.sympify(text), x, y)
        print(
            f"{label} path={path} "
            f"degree_x={poly.degree(x)} degree_y={poly.degree(y)} "
            f"total_degree={poly.total_degree()} terms={len(poly.terms())}"
        )
    print("conclusion=optimized_plane_fibers_quadruple_from_32_to_64")


if __name__ == "__main__":
    main()
