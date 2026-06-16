#!/usr/bin/env python3
"""Fast falsifier harness for the p24 trace-GCD theorem candidates.

This is intentionally a coordinator, not a new large search.  It runs cheap
checks that exercise the current theorem interfaces:

* operator-norm/product/resultant identity on split finite-field toys;
* norm-triangle identity tying exterior expansion, orbit product, and
  block-cycle Fitting determinant;
* block-cycle/Fitting zero-detection with singular controls;
* determinant-line basis-change invariance for the block-cycle Fitting norm;
* diamond/right-unit determinant-line p-unit scaling;
* full-product determinant-line transport with p24 six-step Frobenius closure;
* p24 principal-Hilbert versus cyclotomic-semilinear Frobenius split;
* p24 unit-2 action on right Frobenius orbit labels;
* p24 exterior-support sanity check showing sparse support is not generic;
* dual-sparse uncertainty gate and the centered-difference DFT bridge;
* actual-CM square coinvariant determinant bridge to trace pairing and
  residual products;
* Gaussian-DFT plus Reed-Solomon-tail form of the fixed square determinant;
* RS-tail semilinear-core/Hilbert-90 descent for the fixed square determinant;
* actual-CM rank audit for the explicit RS-tail Hilbert-90 fixed columns;
* p24 scale-discipline accounting separating quotient/recovery-scale payloads
  from constant-factor sqrt-scale seeded correspondences;
* centered full-origin phase-sensitivity gate showing unordered recovery
  fibers do not determine the centered Chow product;
* centered full-origin oriented-edge boundary rejecting a bounded one-edge
  low-bidegree producer for that product;
* centered full-origin short-path boundary rejecting bounded low-degree
  two-edge/three-edge local producers below generic interpolation;
* centered actual-CM orbit-Fitting block-cycle audit checking the
  crossed-product determinant-line plumbing;
* frequency-resultant packaging for the RS-tail local Plucker/residue gates;
* cyclic-section descent guardrail rejecting post-fit splitting-field
  interpolants;
* p24 Frobenius-stable size-16 defect-support accounting;
* fixed-frequency ordinary/no-fixed-defect support reduction gate;
* fixed-frequency trace-annihilator bridge for the tail-in-prefix theorem;
* cyclic 7-section syzygy packaging for the fixed-frequency relations;
* fixed-frequency order-5 collapse showing the fixed relation lives in the
  7-part of the length-35 right orbit;
* fixed-frequency right-symmetry boundary showing centering/sign symmetry is
  insufficient for the six nontrivial order-7 fixed frequencies;
* fixed-frequency order-7 character-projection gate identifying the exact
  right-profile vanishing theorem behind the augmentation candidate;
* fixed-frequency multiplicative-resolvent bridge rewriting the same
  vanishing as orthogonality against six right order-7 multiplicative
  resolvents, and rejecting a Frobenius-only proof mirage;
* fixed-frequency class-character expansion gate expressing that
  orthogonality as packet cancellation among non-genus relative
  class-character resolvents;
* fixed-frequency p24 semilinear factor-cycle gate separating the scalar
  geometric shadow from the real covariance-plus-descent implication;
* fixed-frequency p24 complete-factor descent gate showing the proof must use
  all 70 idempotent tensor factors, not a representative cycle;
* fixed-frequency p24 internal-trace gate showing that the raw p^780 action
  has order 38843 and must first be traced/normed over the internal degree
  5549 factor before the length-7 Hilbert-90 potential applies;
* fixed-frequency p24 nested internal-trace gate splitting that internal
  degree 5549 stage as B/C degree 31 followed by C/E degree 179, and rejecting
  either partial trace as insufficient;
* fixed-frequency p24 raw-coboundary transfer gate showing that a raw
  full-order CM/Lang twisted coboundary formally descends through the nested
  internal trace to the quotient Hilbert-90 potential, while solving the
  potential after zero is circular;
* fixed-frequency p24 product-coboundary Leibniz gate showing that left
  covariance plus a matching right-resolvent coboundary is sufficient to
  construct the raw product coboundary;
* fixed-frequency p24 matching-twist bookkeeping gate making the product
  coboundary twist explicit: alpha=1 and raw epsilon_k=zeta_7^k;
* fixed-frequency p24 right-coboundary obstruction gate showing formal
  right-character covariance is the obstruction eigenspace, so extra CM/Lang
  internal-trace cancellation is needed;
* fixed-frequency p24 right-coboundary internal-trace gate showing matching
  right coboundary is equivalent to nested internal-trace zero;
* fixed-frequency p24 internal-trace stage target gate showing the minimal
  target is the final C/E trace of the B/C trace, not B/C trace zero;
* fixed-frequency p24 internal-trace Gaussian functional gate identifying
  the final trace as weighted Gaussian-period cancellation, not content;
* fixed-frequency p24 period-coset balance gate inverting that Gaussian
  functional to coefficient-side balance on the 560 <p^5460>-cosets;
* fixed-frequency p24 affine quotient-profile gate repackaging the 48
  recombined equations as column offsets independent of the right H-coset;
* fixed-frequency p24 right-difference affine gate eliminating those offsets
  via cyclic right derivatives and recovering them by averaging;
* fixed-frequency p24 right-difference trace gate restating adjacent
  right-derivative identities as degree-8 decomposition-field trace zeros;
* fixed-frequency p24 right-difference covariance-telescope gate reducing
  those trace zeros to rho-covariance plus one descended anchor;
* fixed-frequency p24 right-difference trace covariance functorial gate
  deriving rho-covariance from pointwise Frobenius functoriality of P_i;
* fixed-frequency p24 adjacent-anchor descent gate rewriting the one
  remaining trace anchor as six nontrivial rho-projector vanishings;
* fixed-frequency p24 adjacent-difference operator gate showing that this
  adjacent anchor is the invertible finite difference of the right-axis
  anchor on the nonfixed quotient;
* fixed-frequency p24 internal-character filter gate identifying the same
  target as zero trivial C/E character support after the B/C trace;
* fixed-frequency actual-CM internal-character boundary showing that ordinary
  CM period packets do not satisfy that filter generically;
* fixed-frequency p24 right Gauss weighted-polynomial gate identifying the
  right obstruction as a named weighted relative CM polynomial;
* fixed-frequency p24 right-axis spectrum gate showing the internal trace
  fixes the right 211-axis, so the remaining identity is no order-7
  multiplicative spectrum after tracing;
* fixed-frequency actual-CM right-axis covariance boundary showing formal
  additive covariance and Gauss-normalized fixedness can coexist with nonzero
  quotient projections, so anchor descent is a real extra theorem;
* fixed-frequency actual-CM adjacent-anchor boundary showing covariance and
  telescope do not force the descended adjacent anchor generically;
* fixed-frequency actual-CM left-paired H-coboundary boundary showing that
  inserting a nontrivial left character still does not force the paired
  H-potential in the closest small-CM right-axis clone;
* fixed-frequency paired-kernel criterion gate showing the paired
  H-potential is exactly left-kernel membership of the H-trace leakage;
* fixed-frequency DANGER anchor-condition boundary showing the strict
  2-adic order condition alone does not force trace-defect H-coset equality;
* fixed-frequency actual-CM right-combo internal trace boundary showing the
  right-combo shape alone does not generically force internal trace zero;
* fixed-frequency p24 twisted Hilbert-90 payload gate reformulating the
  factor-cycle descent input as construction of a coboundary potential for
  each Gauss-normalized seed;
* fixed-frequency p24 Gauss-normalization boundary showing formal additive
  Frobenius covariance is only the Gauss-sum eigenvalue;
* fixed-frequency p24 idempotent covariance circularity boundary showing
  descended idempotent covariance with nontrivial eigenvalue is just
  vanishing unless proved before recombination;
* fixed-frequency p24 right/C bidegree support gate identifying the exact
  forbidden Fourier slots: right nontrivial x C/E trivial;
* fixed-frequency p24 Stickelberger bidegree boundary showing plain cyclic
  and right-axis Stickelberger distributions leak in all six forbidden slots,
  so any Jacobi-sum proof must produce C/E-centering from the weighted packet;
* fixed-frequency p24 Jacobi-carry C-centering gate showing a carry with one
  right-trivial C/E character has the forbidden bidegrees killed, while
  generic Jacobi carries still leak;
* fixed-frequency p24 admissible Jacobi-carry span boundary showing the
  termwise-safe carry family has p24 rank 621, while the broader rank-625
  C-axis family includes leaky directions;
* fixed-frequency p24 Jacobi-carry Fourier formula gate explaining the four
  dual Fourier families symbolically from the sawtooth carry formula;
* fixed-frequency p24 admissible Jacobi spectral boundary identifying the
  rank-621 span as conjugate C-pair compatibility with cumulative increments
  1, 7, ..., 7, 4;
* fixed-frequency p24 admissible Jacobi dual-conditions gate turning the
  rank-621 span into four explicit Fourier equation families;
* fixed-frequency p24 dual-conditions value-side gate translating the four
  Fourier families into three packet-facing identities;
* fixed-frequency p24 value-identity strength gate showing C-zero plus
  inversion-complement structure leaves only three global balances;
* fixed-frequency p24 selected-defect value producer gate reducing the
  packet-facing identities to raw complement plus selected affine balance;
* fixed-frequency p24 multiplicative producer dictionary gate translating the
  raw identities into pair-product and selected row-product-ratio constancy;
* fixed-frequency Jacobi-sum product-formula probe showing honest raw Jacobi
  sums supply the off-C-zero inversion complement but not the selected
  row-product ratio;
* fixed-frequency Jacobi-sum row-ratio miner showing the remaining
  right-mixed row-ratio defect is a universal non-cyclotomic right-zero
  anchor scalar, while all six nonzero right rows already agree;
* fixed-frequency Jacobi-sum anchor-correction gate showing that normalizing
  only the degenerate J(1,1)=q-2 value repairs both C-zero pair-products and
  selected row-product ratios in literal right-mixed Jacobi packets;
* fixed-frequency symbolic Hasse-Davenport gate showing the corrected
  Jacobi product formula follows from residue/Gauss-symbol accounting for
  all p24 c=179 right-mixed admissible pairs;
* fixed-frequency reduced-anchor fingerprint gate identifying the selected
  additive effect of the single anchor correction as the punctured right-zero
  row, including its Fourier and right-difference profiles;
* fixed-frequency reduced-anchor adjacent bridge gate identifying the old
  adjacent-anchor descent obstruction as the invertible right-difference of
  the reduced anchor's C/E-trivial row-sum leak;
* fixed-frequency reduced-anchor C-slice decomposition gate separating that
  C/E-trivial row-sum leak from the C/E-nontrivial residual the CM/Lang unit
  must still realize;
* Lean value-side dual-conditions gate composing those three identities into
  the admissible-span/verifier pipeline;
* Lean admissible Jacobi dual-conditions gate composing those four families
  into the existing forbidden-bidegree/product-coboundary/H-coset pipeline;
* fixed-frequency actual-CM admissible Jacobi-span boundary showing nearby
  projector/right-combo CM packets do not generically land in even the broad
  carry span;
* limited fixed-frequency relation-shape index showing no cheap small-CM row
  currently calibrates the p24 right_len=35, q mod 35 = 22 geometry;
* fixed-frequency packet-inversion boundary showing Hermitian/inversion
  packet stability pairs the product terms but does not cancel them without
  an extra anti-invariance or termwise vanishing theorem;
* fixed-frequency order-7 H-coboundary gate reformulating the vanishing as an
  additive Hilbert-90 potential for the order-30 subgroup of `(Z/211Z)^*`;
* fixed-frequency order-7 H-Bezout operator gate making that potential
  canonical once the H-coset trace identities are proved;
* fixed-frequency H-coboundary base-field gate identifying the exact
  Gaussian-period marginal row-sum identity;
* fixed-frequency p24 H-coset sum verifier recording the exact 1092 scalar
  equations that a tower-native proof must supply;
* fixed-frequency p24 character payload contract showing that ordinary
  centering plus the six nontrivial L-valued order-7 character sums are
  equivalent to those seven H-coset equations per left coordinate;
* fixed-frequency p24 anchor-vs-C-centering boundary showing trace-defect
  anchor zero and C/E-trivial bidegree zero are distinct arithmetic inputs;
* fixed-frequency left-descent marginal gate identifying C P_H=0 with
  descent of each right H-period leakage to the left-constant component;
* fixed-frequency p24 section-choice obstruction showing quotient trace
  averages alone do not determine the anchor without selected-child data;
* fixed-frequency p24 right-axis anchor projector gate spelling the anchor
  descent target as six explicit rho-eigenprojector vanishings;
* fixed-frequency p24 right-axis projector-character bridge tying those
  projectors to the six nontrivial H-quotient character equations;
* fixed-frequency p24 projector/internal-character target gate showing the
  six projector channels must have zero trivial C/E component after B/C trace;
* fixed-frequency H-coset selector boundary showing the quotient-character
  selectors have full additive Fourier support;
* fixed-frequency paired-potential boundary showing that a potential after
  Hermitian pairing is the exact target, while a full right-resolvent
  potential is only a stronger sufficient condition;
* fixed-frequency rank-compatibility and actual-CM unit-symmetry boundary
  gates for the order-7 augmentation route;
* fixed-frequency order-7 augmentation gate showing the stronger augmentation
  plus negation covariance gives an explicit syzygy;
* fixed-frequency order-7 Lean handoff proving that augmentation plus
  negation covariance and prefix Plucker p-units removes fixed defects;
* full Plucker-chart scalar Cauchy and block/skew displacement-rank gates;
* full prefix-plus-tail coinvariant square-map target;
* crossed coinvariant norm target for one nonzero orbit;
* actual-CM square coinvariant block-cycle check for that crossed norm;
* safe 14-field and conditional unit-2 4-field orbit payload schemas;
* one pinned actual-CM spectral row that previously exposed the trace-GCD
  right-origin sequence shape.

The point is to keep computation useful as a theorem microscope while avoiding
sqrt(p)-scale or class-set enumeration jobs.
"""

from __future__ import annotations

import argparse
import concurrent.futures
from dataclasses import dataclass
import gzip
import os
from pathlib import Path
import subprocess
import sys
import time


REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parent


@dataclass(frozen=True)
class Task:
    label: str
    argv: tuple[str, ...]
    timeout: float
    must_contain: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaskResult:
    label: str
    returncode: int | None
    elapsed: float
    timed_out: bool
    stdout: str
    stderr: str
    must_contain_missing: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return (
            not self.timed_out
            and self.returncode == 0
            and not self.must_contain_missing
        )


def danger3_dirs() -> list[Path]:
    candidates = [
        REPO / "external" / "DANGER3",
        WORKSPACE / "danger3-short-certificate-experiments" / "external" / "DANGER3",
    ]
    return [path for path in candidates if path.exists()]


def cheap_line_count(path: Path, limit_bytes: int = 32_000_000) -> int | None:
    if path.stat().st_size > limit_bytes:
        return None
    opener = gzip.open if path.suffix == ".gz" else open
    mode = "rt"
    with opener(path, mode, encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def print_danger3_inventory() -> None:
    print("DANGER3 local data inventory")
    dirs = danger3_dirs()
    if not dirs:
        print("  found=0")
        return
    for directory in dirs:
        print(f"  directory={directory}")
        for path in sorted(directory.glob("pp*.txt*")):
            line_count = cheap_line_count(path)
            line_text = "large_or_skipped" if line_count is None else str(line_count)
            print(
                f"    file={path.name} size_bytes={path.stat().st_size} "
                f"cheap_line_count={line_text}"
            )
    print("  note=DANGER3 Pomerance triples are calibration data, not direct CM trace-GCD rows")


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    old_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(REPO / "p24")
        if not old_pythonpath
        else str(REPO / "p24") + os.pathsep + old_pythonpath
    )
    return env


def run_task(task: Task) -> TaskResult:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            task.argv,
            cwd=REPO,
            env=base_env(),
            text=True,
            capture_output=True,
            timeout=task.timeout,
            check=False,
        )
        elapsed = time.monotonic() - start
        missing = tuple(token for token in task.must_contain if token not in proc.stdout)
        return TaskResult(
            label=task.label,
            returncode=proc.returncode,
            elapsed=elapsed,
            timed_out=False,
            stdout=proc.stdout,
            stderr=proc.stderr,
            must_contain_missing=missing,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - start
        return TaskResult(
            label=task.label,
            returncode=None,
            elapsed=elapsed,
            timed_out=True,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            must_contain_missing=task.must_contain,
        )


def default_tasks(
    include_spectral: bool,
    include_actual_cm_triangle: bool,
    include_actual_cm_unit_action: bool,
    include_two_resultant_holdouts: bool,
    include_phase_divisor_holdout: bool,
    include_simple_root_boundary: bool,
    include_selected_tail_tensor_factors: bool,
) -> list[Task]:
    python = sys.executable
    tasks = [
        Task(
            label="operator_norm_q337_right7_k2",
            argv=(
                python,
                "p24/lang_trace_gcd_operator_norm_toy.py",
                "--field-q",
                "337",
                "--right",
                "7",
                "--orbit-generator",
                "2",
                "--k",
                "2",
                "--trials",
                "10",
            ),
            timeout=20.0,
            must_contain=("identity_mismatches=0",),
        ),
        Task(
            label="operator_norm_q2113_right11_k3",
            argv=(
                python,
                "p24/lang_trace_gcd_operator_norm_toy.py",
                "--field-q",
                "2113",
                "--right",
                "11",
                "--orbit-generator",
                "3",
                "--k",
                "3",
                "--trials",
                "10",
            ),
            timeout=20.0,
            must_contain=("identity_mismatches=0",),
        ),
        Task(
            label="p24_exterior_support",
            argv=(python, "p24/lang_trace_gcd_exterior_support.py"),
            timeout=10.0,
            must_contain=("k=3 repeated_sum_size=211",),
        ),
        Task(
            label="axis_crt_strong_rayleigh_obstruction",
            argv=(python, "p24/axis_crt_strong_rayleigh_obstruction_toy.py"),
            timeout=10.0,
            must_contain=(
                "all_ones parts=[2, 2, 2]",
                "witness parts=[2, 2, 3]",
                "strong_rayleigh_violated=1",
                "conclusion=reported_axis_crt_strong_rayleigh_obstruction_toy",
            ),
        ),
        Task(
            label="p24_principal_cyclotomic_split",
            argv=(python, "p24/trace_gcd_principal_cyclotomic_split_audit.py"),
            timeout=10.0,
            must_contain=(
                "hilbert_class_frobenius_order=1",
                "ordinary_base_polynomial_descent_is_not_forced=1",
                "crossed_product_orbit_norm_is_the_honest_phase_payload=1",
            ),
        ),
        Task(
            label="p24_two_resultant_theorem_manifest",
            argv=(python, "p24/trace_gcd_two_resultant_theorem_manifest.py"),
            timeout=10.0,
            must_contain=(
                '"field_elements": 4',
                '"ratio_to_sqrt_floor": 4e-12',
                '"bad_support_size": 54',
                '"Xi_O0"',
                '"Xi_O1"',
                '"missing_theorem"',
            ),
        ),
        Task(
            label="orbit_norm_certificate_verifier_schema",
            argv=(python, "p24/trace_gcd_orbit_norm_certificate_verifier.py", "--schema"),
            timeout=10.0,
            must_contain=(
                "expected_payload_field_elements=14",
                "expected_payload_over_sqrt_floor=1.4e-11",
                "producer_honesty_required",
            ),
        ),
        Task(
            label="orbit_norm_certificate_verifier_unit2_schema",
            argv=(
                python,
                "p24/trace_gcd_orbit_norm_certificate_verifier.py",
                "--unit2-schema",
            ),
            timeout=10.0,
            must_contain=(
                "expected_payload_field_elements=4",
                "expected_payload_over_sqrt_floor=4e-12",
                "diamond_equivariance_required=1",
            ),
        ),
        Task(
            label="p24_unit2_orbit_compression",
            argv=(python, "p24/trace_gcd_unit2_orbit_compression_audit.py"),
            timeout=10.0,
            must_contain=(
                "unit=2",
                "zero_orbit_fixed=1",
                "nonzero_cycle_covers_all_nonzero_orbits=1",
                "conclusion=reported_trace_gcd_unit2_orbit_compression",
            ),
        ),
        Task(
            label="p24_diamond_support_transport",
            argv=(python, "p24/diamond_support_transport_audit.py"),
            timeout=10.0,
            must_contain=(
                '"deleted_cycle_covers_all_nonzero_orbits": true',
                '"tail_cycle_covers_all_nonzero_orbits": true',
                '"all_prefixes_have_four_blocks": true',
                '"all_tail_windows_frobenius_contiguous": true',
                '"final_window_frobenius_contiguous": true',
                '"final_window_rotation_start": 17',
            ),
        ),
        Task(
            label="full_product_determinant_transport",
            argv=(python, "p24/full_product_determinant_transport_toy.py"),
            timeout=20.0,
            must_contain=(
                "p24_unit6_equals_frobenius17=1",
                "commuting_square_failures=0",
                "determinant_formula_failures=0",
                "zero_status_mismatches=0",
                "punit_edges=480/480",
                "final_identifies_to_representative=80/80",
                "internal_rotation_det_punit=80/80",
                "full_product_commuting_square_implies_determinant_line_transport=1",
                "conclusion=reported_full_product_determinant_transport_toy",
            ),
        ),
        Task(
            label="tensor_factor_trace_period_identity",
            argv=(python, "p24/tensor_factor_trace_period_identity.py"),
            timeout=10.0,
            must_contain=(
                "ord_m(p)=5460",
                "ord_n(p)=388430",
                "tensor_factor_count_over_E=70",
                "tensor_factor_degree_over_E=5549",
                "E_frobenius_multiplier_a=p^ord_m_mod_n=209035",
                "C_degree_over_E=179",
                "B_degree_over_C=31",
                "trace_subgroup_generator_a^179_mod_n=1293662",
                "trace_subgroup_order=31",
                "quotient_orbit_length=179",
                "trace_cosets_partition_factor_orbit=True",
                "coordinate_count_over_E=537",
                "selected_axis_rank_target=368",
                "conclusion=reported_tensor_factor_trace_period_identity",
            ),
        ),
        Task(
            label="tensor_factor_dual_basis_window_audit_pinned",
            argv=(
                python,
                "p24/tensor_factor_dual_basis_window_audit.py",
                "--only-D",
                "-10919",
                "--min-h",
                "1",
                "--max-h",
                "200",
                "--only-m",
                "12",
                "--max-n",
                "200",
                "--max-factor-degree",
                "20",
                "--max-extension-degree",
                "8",
                "--max-tensor-factor-degree",
                "12",
                "--max-rows",
                "8",
                "--max-windows",
                "4",
            ),
            timeout=30.0,
            must_contain=(
                "rows=1",
                "target=axis",
                "2:trace=[2, 4, 6] window=[2, 4, 6]",
                "3:trace=[3, 6] window=[3, 6]",
                "trace_window_rank_mismatch_targets=0",
                "axis_rows_full_by_tested_window=1",
                "max_rank_profile_failures=0",
                "p24_target_can_be_stated_as_top_three_relative_coefficients_nonzero=1",
                "conclusion=reported_tensor_factor_dual_basis_window_audit",
            ),
        ),
        Task(
            label="tensor_factor_crt_marginal_rank_audit_pinned_w1",
            argv=(
                python,
                "p24/tensor_factor_crt_marginal_rank_audit.py",
                "--only-D",
                "-10919",
                "--min-h",
                "1",
                "--max-h",
                "200",
                "--only-m",
                "12",
                "--max-n",
                "200",
                "--max-factor-degree",
                "20",
                "--max-extension-degree",
                "8",
                "--max-tensor-factor-degree",
                "12",
                "--subdegree",
                "3",
                "--windows",
                "1",
                "--max-rows",
                "8",
            ),
            timeout=30.0,
            must_contain=(
                "windows=1",
                "c=  4 marg_span=  3/  3 marg_affine=  3/  3",
                "c=  3 marg_span=  3/  3 marg_affine=  2/  2",
                "combined=constantplus4plus3   size=  6 rank=  3/  3",
                "rank_identity_mismatches=0",
                "component_capacity_failures=0",
                "combined_capacity_failures=0",
                "conclusion=reported_tensor_factor_crt_marginal_rank_audit",
            ),
        ),
        Task(
            label="tensor_factor_crt_marginal_rank_audit_pinned_w2",
            argv=(
                python,
                "p24/tensor_factor_crt_marginal_rank_audit.py",
                "--only-D",
                "-10919",
                "--min-h",
                "1",
                "--max-h",
                "200",
                "--only-m",
                "12",
                "--max-n",
                "200",
                "--max-factor-degree",
                "20",
                "--max-extension-degree",
                "8",
                "--max-tensor-factor-degree",
                "12",
                "--subdegree",
                "3",
                "--windows",
                "2",
                "--max-rows",
                "8",
            ),
            timeout=30.0,
            must_contain=(
                "windows=2",
                "c=  4 marg_span=  4/  4 marg_affine=  3/  3",
                "combined=constantplus4        size=  4 rank=  4/  4",
                "combined=constantplus4plus3   size=  6 rank=  6/  6",
                "rank_identity_mismatches=0",
                "component_capacity_failures=0",
                "combined_capacity_failures=0",
                "conclusion=reported_tensor_factor_crt_marginal_rank_audit",
            ),
        ),
        Task(
            label="relative_trace_normal_basis_toy",
            argv=(python, "p24/trace_frame_relative_trace_normal_basis_toy.py"),
            timeout=10.0,
            must_contain=(
                "positive_implication_failures=0",
                "nonnormal_controls=2",
                "normal_theta_implies_relative_trace_period_normal_basis=1",
                "relative_trace_normality_is_not_automatic=1",
                "conclusion=reported_trace_frame_relative_trace_normal_basis_toy",
            ),
        ),
        Task(
            label="relative_kummer_payload_accounting",
            argv=(python, "p24/relative_kummer_payload_accounting.py"),
            timeout=10.0,
            must_contain=(
                "r=157",
                "ord_r_p=156",
                "r=211",
                "ord_r_p= 35",
                "kummer_normal_form_slots=3107811",
                "degree_211_cross_orbit_glue_extension_objects=5",
                "degree_211_cross_orbit_glue_base_slots=175",
                "kummer_with_glue_extension_object_slots=3107816",
                "kummer_with_glue_conservative_base_slots=3107986",
                "glue_extension_object_count_is_5_but_base_field_slot_count_is_175=1",
                "conclusion=reported_relative_kummer_phase_payload_accounting",
            ),
        ),
        Task(
            label="p24_subsqrt_scale_discipline_gate",
            argv=(python, "p24/p24_subsqrt_scale_discipline_gate.py"),
            timeout=10.0,
            must_contain=(
                "m_times_n_equals_h=1",
                "hcoset_verifier_scalars=1092",
                "trace_plus_child_payload=132508",
                "selected_chain_payload=3107811",
                "full_relative_table_payload=3174011",
                "composite_seeded_proxy=968924963328",
                "composite_seeded_proxy_over_sqrt=9.689249633280e-01",
                "composite_seeded_proxy_over_selected_chain=3.117708777426e+05",
                "hcoset_equations_are_verifier_scalars_not_producer_scale=1",
                "trace_plus_child_is_anchor_payload_not_full_j_certificate=1",
                "selected_chain_and_full_relative_table_are_genuine_subsqrt_surfaces_for_p24=1",
                "h_sized_class_table_is_rejected_even_though_h_less_than_sqrt_for_this_p=1",
                "composite_seeded_correspondence_is_constant_factor_sqrt_scale=1",
                "asymptotic_speedup_requires_quotient_recovery_or_punit_producer_not_seeded_walk=1",
                "conclusion=reported_p24_subsqrt_scale_discipline_gate",
            ),
        ),
        Task(
            label="oriented_recovery_cycle_payload_gate",
            argv=(python, "p24/oriented_recovery_cycle_payload_gate.py"),
            timeout=10.0,
            must_contain=(
                "recovery_order_n=3107441",
                "oriented_composite_path=(2, 463, -223)",
                "selected_chain_slots=3107811",
                "oriented_cycle_plus_A_x0_slots=9322325",
                "cycle_plus_tail_plus_dense_phi_slots=9589191",
                "oriented_cycle_payload_is_larger_than_selected_chain_but_subsqrt=1",
                "modular_polynomial_tables_are_canonical_not_h_sized=1",
                "producer_still_must_find_one_target_cycle_or_final_A_x0=1",
                "this_surface_does_not_remove_the_seedless_cycle_problem=1",
                "conclusion=reported_oriented_recovery_cycle_payload_gate",
            ),
        ),
        Task(
            label="relative_kummer_multi_orbit_ambiguity_gate",
            argv=(python, "p24/relative_kummer_multi_orbit_ambiguity_gate.py", "--trials", "3"),
            timeout=30.0,
            must_contain=(
                "one_orbit_kummer_powers_select_child_polynomial=1",
                "multi_orbit_kummer_powers_do_not_select_child_polynomial=1",
                "cross_orbit_glue_restores_child_selection=1",
                "p24_211_layer_needs_cross_orbit_phase_glue=1",
                "conclusion=relative_Kummer_minpolys_need_cross_orbit_glue_for_multi_orbit_child_selection",
            ),
        ),
        Task(
            label="tower_kummer_glue_complexity_scan_small",
            argv=(
                python,
                "p24/tower_kummer_glue_complexity_scan.py",
                "--max-cases",
                "3",
                "--max-h",
                "100",
                "--q-stop",
                "80000",
                "--max-rows-per-case",
                "4",
                "--summary-only",
            ),
            timeout=30.0,
            must_contain=(
                "good_distinct_nonzero_rows=3",
                "glue_coordinate_slots=8",
                "full_degree_coordinates=8",
                "low_degree_coordinates=0",
                "full_frobenius_degree_glue_values=21",
                "proper_frobenius_descent_glue_values=0",
                "nonsplit_full_frobenius_degree_glue_values=3",
                "nonsplit_proper_frobenius_descent_glue_values=0",
                "conclusion=reported_tower_kummer_glue_complexity_scan",
            ),
        ),
        Task(
            label="factorized_trace_frame_schubert_accounting",
            argv=(python, "p24/trace_frame_factorized_schubert_accounting.py"),
            timeout=10.0,
            must_contain=(
                "forced_intersection_dim=10",
                "residual_tail_dim=10",
                "one_factor_all_H_packets_Fp_slots_over_sqrt=4.768283520000e-03",
                "all_70_factors_all_H_packets_Fp_slots_over_sqrt=3.337798464000e-01",
                "decomposition_field_relative_degree8_punits_with_tensor_symmetry=4",
                "factorized_punits=A_component,B_component,B_mod_A_intersection,residual_tail",
                "conclusion=reported_factorized_trace_frame_schubert_accounting",
            ),
        ),
        Task(
            label="trace_frame_prefix_intersection_audit_pinned",
            argv=(
                python,
                "p24/trace_frame_prefix_intersection_audit.py",
                "--only-D",
                "-10919",
                "--min-h",
                "1",
                "--max-h",
                "200",
                "--max-n",
                "200",
                "--max-m",
                "40",
                "--max-factor-degree",
                "20",
                "--max-extension-degree",
                "8",
                "--max-tensor-factor-degree",
                "12",
                "--max-top-count",
                "4",
                "--include-linear",
                "--only-m",
                "12",
                "--max-cases",
                "1",
            ),
            timeout=20.0,
            must_contain=(
                "component_full=1 intersection_minimal=1 prefix_max_rank=1",
                "conclusion=reported_trace_frame_prefix_intersection_audit",
            ),
        ),
        Task(
            label="trace_frame_leading_residual_value_audit_pinned",
            argv=(
                python,
                "p24/trace_frame_leading_residual_value_audit.py",
                "--only-D",
                "-10919",
                "--min-h",
                "1",
                "--max-h",
                "200",
                "--max-n",
                "200",
                "--max-m",
                "40",
                "--max-factor-degree",
                "20",
                "--max-extension-degree",
                "8",
                "--max-tensor-factor-degree",
                "12",
                "--max-top-count",
                "3",
                "--include-linear",
                "--only-m",
                "12",
                "--max-cases",
                "1",
                "--max-rows",
                "12",
            ),
            timeout=20.0,
            must_contain=(
                "nonzero_determinant_rows=2",
                "zero_determinant_rows=0",
                "zero_det_norms=0",
                "conclusion=reported_trace_frame_leading_residual_value_audit",
            ),
        ),
        Task(
            label="trace_frame_lead_prefix_tail_toy",
            argv=(python, "p24/trace_frame_lead_prefix_tail_toy.py"),
            timeout=10.0,
            must_contain=(
                "tail_separates_kernel=1",
                "full_lead_nonzero=1",
                "full_rank_impossible_when_prefix_rank_below_3=1",
                "conclusion=full_lead_nonzero_forces_prefix_rank_and_tail_injectivity",
            ),
        ),
        Task(
            label="selected_tail_resultant_equivalence_toy",
            argv=(
                python,
                "p24/selected_tail_resultant_equivalence_toy.py",
                "--m",
                "6",
                "--head-dim",
                "3",
                "--trials",
                "200",
            ),
            timeout=10.0,
            must_contain=(
                "tail_kernel_matches_tail=1",
                "equivalence_mismatches=0",
            ),
        ),
        Task(
            label="trace_frame_schubert_descent_toy",
            argv=(python, "p24/trace_frame_schubert_descent_toy.py"),
            timeout=10.0,
            must_contain=(
                "canonical_all_nonzero=1",
                "unit_twist_zero_compatible=1",
                "spliced_all_nonzero=1",
                "no_single_fixed_minor_nonzero=1",
                "conclusion=fixed_sections_descend_packetwise_pivots_do_not",
            ),
        ),
        Task(
            label="lean_trace_frame_leading_norm_gate",
            argv=("lean", "p24/lean/TraceFrameLeadingNormGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_denominator_safe_lead_gate",
            argv=("lean", "p24/lean/TraceFrameDenominatorSafeLeadGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_selected_lead_failure_gate",
            argv=("lean", "p24/lean/TraceFrameSelectedLeadFailureGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_prefix_intersection_gate",
            argv=("lean", "p24/lean/TraceFramePrefixIntersectionGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_residual_tail_gate",
            argv=("lean", "p24/lean/TraceFrameResidualTailGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_selected_tail_crossed_product_gate",
            argv=("lean", "p24/lean/TraceFrameSelectedTailCrossedProductGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_selected_tail_tensor_factor_gate",
            argv=("lean", "p24/lean/TraceFrameSelectedTailTensorFactorGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_semilinear_eigen_descent_gate",
            argv=("lean", "p24/lean/TraceGcdSemilinearEigenDescentGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_axis_anchor_descent_gate",
            argv=("lean", "p24/lean/TraceGcdRightAxisAnchorDescentGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_anchor_trace_average_payload_gate",
            argv=("lean", "p24/lean/TraceGcdAnchorTraceAveragePayloadGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_selected_tail_phase_producer_gate",
            argv=("lean", "p24/lean/TraceFrameSelectedTailPhaseProducerGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_kummer_cross_orbit_glue_gate",
            argv=("lean", "p24/lean/KummerCrossOrbitGlueGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_selected_tail_borcherds_gate",
            argv=("lean", "p24/lean/TraceFrameSelectedTailBorcherdsGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_prefix_tail_crossed_package_gate",
            argv=("lean", "p24/lean/TraceFramePrefixTailCrossedPackageGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_annihilator_gate",
            argv=("lean", "p24/lean/TraceFrameAnnihilatorGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_schubert_equivariant_descent_gate",
            argv=("lean", "p24/lean/SchubertEquivariantDescentGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_frame_schubert_packet_norm_gate",
            argv=("lean", "p24/lean/TraceFrameSchubertPacketNormGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_dual_sparse_bridge_gate",
            argv=("lean", "p24/lean/TraceGcdDualSparseBridgeGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_pairing_subspace_bridge_gate",
            argv=("lean", "p24/lean/TraceGcdTracePairingSubspaceBridgeGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_residual_prefix_tail_gate",
            argv=("lean", "p24/lean/TraceGcdResidualPrefixTailGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_prefix_adjoint_gate",
            argv=("lean", "p24/lean/TraceGcdPrefixAdjointGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_prefix_syndrome_resultant_bridge_gate",
            argv=("lean", "p24/lean/TraceGcdPrefixSyndromeResultantBridgeGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_prefix_coinvariant_fitting_gate",
            argv=("lean", "p24/lean/TraceGcdPrefixCoinvariantFittingGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_full_coinvariant_tail_gate",
            argv=("lean", "p24/lean/TraceGcdFullCoinvariantTailGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_plucker_displacement_handoff_gate",
            argv=("lean", "p24/lean/TraceGcdPluckerDisplacementHandoffGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_crossed_coinvariant_norm_gate",
            argv=("lean", "p24/lean/TraceGcdCrossedCoinvariantNormGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="centered_plateau_factor_support_gate",
            argv=(
                python,
                "p24/centered_plateau_factor_support_audit.py",
                "--q",
                "5",
                "--right",
                "211",
                "--left",
                "157",
                "--start",
                "0",
                "--zero-position",
                "0",
            ),
            timeout=10.0,
            must_contain=(
                "plateau_subspace_dim=54",
                "nonzero_factor_blocks=7/7",
                "all_blocks_nonzero_means_no_small_block_support_shortcut=1",
                "conclusion=reported_centered_plateau_factor_support_audit",
            ),
        ),
        Task(
            label="centered_marginal_full_origin_phase_sensitivity_gate",
            argv=(python, "p24/centered_marginal_full_origin_phase_sensitivity_gate.py"),
            timeout=30.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "pair=(4,7)",
                "cyclic_origin_shift_product_preserved=4/4",
                "fiber_multisets_preserved_by_shuffle=8/8",
                "fiber_shuffle_alpha_product_changed=8/8",
                "fiber_shuffle_right_sequence_changed=8/8",
                "fiber_shuffle_right_factorization_failed=0/8",
                "fiber_shuffle_zero_products=0/8",
                "cyclic_origin_shift_preserves_the_full_origin_product=1",
                "unordered_recovery_fibers_do_not_determine_centered_full_origin_product=1",
                "full_origin_borcherds_producer_must_be_phase_aware=1",
                "closed_divisor_formula_cannot_be_replaced_by_unordered_fiber_data=1",
                "conclusion=reported_centered_marginal_full_origin_phase_sensitivity_gate",
            ),
        ),
        Task(
            label="centered_marginal_full_origin_edge_shape_boundary",
            argv=(python, "p24/centered_marginal_full_origin_edge_shape_boundary.py"),
            timeout=30.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "pair=(4,7)",
                "sample_count=140",
                "distinct_edge_pairs=140",
                "first_polynomial_bidegree_leq_4=None",
                "first_rational_bidegree_leq_4=None",
                "random_repeated_alpha_polynomial_hits=0/8",
                "random_repeated_alpha_rational_hits=0/8",
                "centered_full_origin_product_is_not_bounded_oriented_edge_function=1",
                "bounded_local_correspondence_norm_needs_more_than_one_edge=1",
                "phase_aware_fitting_divisor_still_required=1",
                "conclusion=reported_centered_marginal_full_origin_edge_shape_boundary",
            ),
        ),
        Task(
            label="centered_marginal_full_origin_path_shape_boundary",
            argv=(python, "p24/centered_marginal_full_origin_path_shape_boundary.py"),
            timeout=45.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "pair=(4,7)",
                "path_vertices=3",
                "poly_monomials_at_cap=120",
                "first_polynomial_total_degree=None",
                "rat_monomials_at_cap=56",
                "first_rational_total_degree=None",
                "path_vertices=4",
                "poly_monomials_at_cap=126",
                "rat_monomials_at_cap=35",
                "random_repeated_alpha_polynomial_hits=0/8",
                "random_repeated_alpha_rational_hits=0/8",
                "short_oriented_paths_have_no_subgeneric_low_degree_formula=1",
                "local_correspondence_norm_must_use_richer_phase_or_direct_fitting_divisor=1",
                "conclusion=reported_centered_marginal_full_origin_path_shape_boundary",
            ),
        ),
        Task(
            label="centered_marginal_orbit_fitting_block_cycle_audit",
            argv=(python, "p24/centered_marginal_orbit_fitting_block_cycle_audit.py"),
            timeout=30.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "pair=(4,7)",
                "right=7",
                "q_mod_right=2",
                "affine_window_det_mismatches=0",
                "orbit_count=3",
                "determinant_mismatches=0",
                "direct_sum_mismatches=0",
                "zero_detection_failures=0",
                "full_rank_iff_failures=0",
                "singular_control_failures=0",
                "actual_centered_orbit_product_equals_direct_sum_fitting_det=1",
                "actual_centered_orbit_product_equals_signed_block_cycle_fitting_det=1",
                "block_cycle_zero_detects_orbit_schubert_zero=1",
                "crossed_product_fitting_plumbing_is_not_the_missing_arithmetic=1",
                "conclusion=reported_centered_marginal_orbit_fitting_block_cycle_audit",
            ),
        ),
        Task(
            label="difference_dft_bridge_audit",
            argv=(python, "p24/trace_gcd_difference_dft_bridge_audit.py"),
            timeout=20.0,
            must_contain=(
                "dft_difference_mismatches=0",
                "nonzero_multiplier_failures=0",
                "direct_rowspace_equal=0/1",
                "conclusion=reported_trace_gcd_difference_dft_bridge_audit",
            ),
        ),
        Task(
            label="lambda_profile_bridge_audit",
            argv=(python, "p24/trace_gcd_lambda_profile_bridge_audit.py"),
            timeout=20.0,
            must_contain=(
                "profile_dft_mismatches=0",
                "lambda_fourier_trace_mismatches=0",
                "lang_reconstruction_mismatches=0",
                "lang_zero_equivalence_failures=0",
                "remaining_bridge_is_plateau_vanishing_for_bad_lambda=1",
                "conclusion=reported_trace_gcd_lambda_profile_bridge_audit",
            ),
        ),
        Task(
            label="lambda_plateau_rowspace_audit",
            argv=(python, "p24/trace_gcd_lambda_plateau_rowspace_audit.py"),
            timeout=20.0,
            must_contain=(
                "rowspace_containment_failures=0",
                "nonvacuous_containments=0",
                "vacuous_full_leading_rank=10/10",
                "full_leading_rank_rows_support_punit_but_do_not_prove_bridge_identity=1",
                "conclusion=reported_trace_gcd_lambda_plateau_rowspace_audit",
            ),
        ),
        Task(
            label="lambda_plateau_det_ratio_audit",
            argv=(python, "p24/trace_gcd_lambda_plateau_det_ratio_audit.py"),
            timeout=20.0,
            must_contain=(
                "both_nonzero=2/2",
                "rowspace_equal=2/2",
                "distinct_nonzero_ratios=2",
                "varying_ratios_mean_no_obvious_universal_scalar_comparison=1",
                "conclusion=reported_trace_gcd_lambda_plateau_det_ratio_audit",
            ),
        ),
        Task(
            label="trace_pairing_subspace_bridge_audit",
            argv=(python, "p24/trace_gcd_trace_pairing_subspace_bridge_audit.py"),
            timeout=20.0,
            must_contain=(
                "trace_rank_mismatches=0",
                "nonzero_event_mismatches=0",
                "missing_residual_norm_products=0",
                "full_rank_rows=10/10",
                "residual_norm_product_detects_the_same_punit_event=1",
                "conclusion=reported_trace_gcd_trace_pairing_subspace_bridge_audit",
            ),
        ),
        Task(
            label="trace_pairing_subspace_bridge_toy",
            argv=(python, "p24/trace_gcd_trace_pairing_subspace_bridge_toy.py"),
            timeout=10.0,
            must_contain=(
                "rank_mismatches=0",
                "event_mismatches=0",
                "low_rank_zero_products=2",
                "all_coordinate_residual_product_detects_dependent_coordinates=1",
                "conclusion=reported_trace_gcd_trace_pairing_subspace_bridge_toy",
            ),
        ),
        Task(
            label="actual_cm_square_coinvariant_bridge_audit",
            argv=(python, "p24/trace_gcd_actual_cm_square_coinvariant_audit.py"),
            timeout=20.0,
            must_contain=(
                "gram_relation_failures=0",
                "nonzero_event_mismatches=0",
                "prefix_tail_event_mismatches=0",
                "full_rank_rows=6/10",
                "singular_control_rows=4/10",
                "actual_nontrivial_prefix_tail_rows=4/10",
                "square_coinvariant_determinant_is_trace_pairing_adjoint_up_to_gram_unit=1",
                "conclusion=reported_trace_gcd_actual_cm_square_coinvariant_audit",
            ),
        ),
        Task(
            label="full_gaussian_rs_tail_toy",
            argv=(python, "p24/trace_gcd_full_gaussian_rs_tail_toy.py"),
            timeout=10.0,
            must_contain=(
                "rank_mismatches=0",
                "tail_reconstruction_failures=0",
                "full_rank_rows=1",
                "low_rank_controls=2",
                "truncated_tail_becomes_degree_lt_tail_dim_RS_subspace=1",
                "conclusion=reported_trace_gcd_full_gaussian_rs_tail_toy",
            ),
        ),
        Task(
            label="actual_cm_gaussian_rs_tail_audit",
            argv=(python, "p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py"),
            timeout=20.0,
            must_contain=(
                "rank_mismatches=0",
                "tail_reconstruction_failures=0",
                "full_rank_rows=6/10",
                "singular_control_rows=4/10",
                "actual_prefix_plus_tail_rows=4/10",
                "actual_cm_lang_blocks_match_gaussian_dft_rs_tail_rank=1",
                "conclusion=reported_trace_gcd_actual_cm_gaussian_rs_tail_audit",
            ),
        ),
        Task(
            label="actual_cm_rs_tail_semilinear_core_audit",
            argv=(
                python,
                "p24/trace_gcd_actual_cm_rs_tail_semilinear_core_audit.py",
            ),
            timeout=20.0,
            must_contain=(
                "explicit_column_count_mismatches=0",
                "rank_mismatches=0",
                "full_rank_rows=6/10",
                "singular_control_rows=4/10",
                "actual_prefix_plus_tail_rows=4/10",
                "actual_cm_rs_tail_fixed_columns_match_time_rank=1",
                "actual_cm_hilbert90_fixed_relation_shape_survives=1",
                "actual_cm_rs_tail_schur_split_measured=1",
                "conclusion=reported_trace_gcd_actual_cm_rs_tail_semilinear_core_audit",
            ),
        ),
        Task(
            label="rs_tail_semilinear_core_toy",
            argv=(python, "p24/trace_gcd_rs_tail_semilinear_core_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=random_good",
                "case=forced_prefix_fixed_core",
                "case=forced_rs_tail_fixed_core",
                "global_kernel_equals_semilinear_core=1",
                "hilbert90_descent_match=1",
                "zero_core_iff_no_nonzero_T_fixed_RS_tail_relation=1",
                "forced_rs_tail_fixed_core_detected=1",
                "p24_fixed_relation_shape_Fp28_plus_K28_plus_Fp16_to_L=1",
                "conclusion=reported_trace_gcd_rs_tail_semilinear_core_toy",
            ),
        ),
        Task(
            label="rs_tail_fixed_adjoint_toy",
            argv=(python, "p24/trace_gcd_rs_tail_fixed_adjoint_toy.py"),
            timeout=10.0,
            must_contain=(
                "pairing_mismatches=0",
                "case=random_good",
                "case=forced_prefix_fixed_relation",
                "case=forced_rs_tail_fixed_relation",
                "rs_tail_fixed_adjoint_pairing_formula_verified=1",
                "rs_tail_fixed_relation_injective_iff_adjoint_syndrome_surjective=1",
                "p24_syndrome_shape_Fp28_plus_K28_plus_Fp16=1",
                "conclusion=reported_trace_gcd_rs_tail_fixed_adjoint_toy",
            ),
        ),
        Task(
            label="rs_tail_syndrome_moore_schur_toy",
            argv=(python, "p24/trace_gcd_rs_tail_syndrome_moore_schur_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=random_prefix_full_tail_quotient_full",
                "case=forced_prefix_relation",
                "case=forced_tail_inside_prefix_span",
                "prefix_full_plus_tail_quotient_full_iff_full_syndrome_unit=1",
                "prefix_failure_and_tail_quotient_failure_controls_detected=1",
                "p24_rs_tail_full_coordinate_count=156",
                "conclusion=reported_trace_gcd_rs_tail_syndrome_moore_schur_toy",
            ),
        ),
        Task(
            label="rs_tail_block_support_profile_toy",
            argv=(python, "p24/trace_gcd_rs_tail_block_support_profile_toy.py"),
            timeout=10.0,
            must_contain=(
                "selected_block_support_profile_gate_passes_random_direct_control=1",
                "selected_block_support_profile_detects_prefix_relation=1",
                "selected_block_support_profile_detects_tail_inside_prefix=1",
                "selected_square_pass_is_compatibility_not_lrs_evidence=1",
                "full_210_column_moduli_needed_for_positive_hidden_lrs_evidence=1",
                "p24_selected_block_support_profile_subsets=31",
                "conclusion=reported_trace_gcd_rs_tail_block_support_profile_toy",
            ),
        ),
        Task(
            label="rs_tail_full_plucker_chart_cauchy_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "scalar_grs_plucker_chart_cauchy_invariant_detected=1",
                "row_and_column_scaled_grs_chart_preserves_inverse_rank=1",
                "random_full_source_plucker_chart_rejected=1",
                "full_210_unused_columns_give_real_visible_grs_moduli=1",
                "hidden_lrs_still_requires_block_or_classfield_equivalence=1",
                "p24_plucker_chart_entries=8424",
                "conclusion=reported_trace_gcd_rs_tail_full_plucker_chart_cauchy_toy",
            ),
        ),
        Task(
            label="rs_tail_block_skew_cauchy_displacement_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "scalar_cauchy_is_displacement_rank_one=1",
                "scalar_entrywise_inverse_rank_is_shadow_of_displacement_rank=1",
                "block_resolvent_has_low_sylvester_displacement_rank=1",
                "transported_basis_changes_preserve_low_displacement_rank=1",
                "random_chart_rejected_by_block_skew_displacement_rank=1",
                "actual_p24_work_is_to_identify_transported_CM_operators_A_and_B=1",
                "conclusion=reported_trace_gcd_rs_tail_block_skew_cauchy_displacement_toy",
            ),
        ),
        Task(
            label="plucker_displacement_handoff_toy",
            argv=(python, "p24/trace_gcd_plucker_displacement_handoff_toy.py"),
            timeout=10.0,
            must_contain=(
                "low_rank_operator_boundary_implies_low_rank_plucker_displacement=1",
                "scalar_vandermonde_boundary_is_rank_one=1",
                "block_resolvent_boundary_survives_selected_basis_change=1",
                "random_chart_rejected_by_fixed_arithmetic_operators=1",
                "postfit_operators_are_not_certificate_evidence=1",
                "conclusion=reported_trace_gcd_plucker_displacement_handoff_toy",
            ),
        ),
        Task(
            label="rs_tail_shift_displacement_boundary_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "invariant_full_code_gives_low_shift_displacement=1",
                "random_graph_same_split_rejected_by_shift_displacement=1",
                "riccati_identity_is_exact_for_shift_invariant_graph=1",
                "p24_candidate_A_B_are_selected_and_omitted_shift_blocks=1",
                "p24_small_residue_should_come_from_two_tail_cut_edges=1",
                "conclusion=reported_trace_gcd_rs_tail_shift_displacement_boundary_toy",
            ),
        ),
        Task(
            label="rs_tail_cyclic_operator_boundary_toy",
            argv=(python, "p24/trace_gcd_rs_tail_cyclic_operator_boundary_toy.py"),
            timeout=10.0,
            must_contain=(
                "cyclic_lang_operator_gives_tail_split_boundary_rank_two=1",
                "whole_deleted_block_contributes_no_boundary=1",
                "random_omitted_columns_fail_fixed_cyclic_operator_boundary=1",
                "postfit_selected_operator_again_not_certificate_evidence=1",
                "p24_operator_work_is_to_construct_common_cyclic_Lang_T_integrally=1",
                "conclusion=reported_trace_gcd_rs_tail_cyclic_operator_boundary_toy",
            ),
        ),
        Task(
            label="rs_tail_frequency_defect_gate_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_frequency_defect_gate_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "frequency_defect_gate_proves_selected_basis_without_chart_assumption=1",
                "local_frequency_plucker_punits_are_the_missing_arithmetic=1",
                "defect_tail_residue_punits_are_the_missing_arithmetic=1",
                "cyclic_invariance_alone_does_not_imply_selected_punit=1",
                "tail_invisible_eigenline_gives_omitted_support_kernel=1",
                "cyclic_shift_displacement_becomes_non_circular_after_this_gate=1",
                "conclusion=reported_trace_gcd_rs_tail_frequency_defect_gate_toy",
            ),
        ),
        Task(
            label="rs_tail_basis_free_frequency_gate_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_basis_free_frequency_gate_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "basis_free_local_projection_ranks_suffice=1",
                "defect_tail_residue_is_prefix_to_prefix_tail_rank_jump=1",
                "ordinary_prefix_rank_failure_detected=1",
                "arbitrary_row_basis_changes_do_not_change_gate=1",
                "p24_basis_free_frequency_gate_factors=35_prefix_rank_gates_plus_16_tail_rank_jumps",
                "conclusion=reported_trace_gcd_rs_tail_basis_free_frequency_gate_toy",
            ),
        ),
        Task(
            label="rs_tail_frequency_moore_schur_factor_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_frequency_moore_schur_factor_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "local_plucker_product_is_frequency_form_of_prefix_moore_factor=1",
                "defect_tail_residues_are_frequency_form_of_quotient_tail_moore_factor=1",
                "selected_det_factors_as_prefix_times_tail_quotient=1",
                "cyclic_invariance_alone_still_allows_both_controls=1",
                "conclusion=reported_trace_gcd_rs_tail_frequency_moore_schur_factor_toy",
            ),
        ),
        Task(
            label="rs_tail_frequency_resultant_gate_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_frequency_resultant_gate_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "frequency_resultants_package_all_local_gates=1",
                "plucker_resultant_zero_gives_ordinary_frequency_failure=1",
                "tail_support_resultant_zero_gives_defect_residue_failure=1",
                "defect_selector_size_mismatch_rejected=1",
                "resultant_gate_reduces_35_local_checks_to_global_cyclic_units=1",
                "p24_needs_cm_identification_of_plucker_tail_selector_sections=1",
                "conclusion=reported_trace_gcd_rs_tail_frequency_resultant_gate_toy",
            ),
        ),
        Task(
            label="rs_tail_cyclic_section_descent_toy",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "frobenius_compatible_values_descend_to_base_cyclic_section=1",
                "arbitrary_postfit_splitting_field_interpolant_is_rejected=1",
                "frobenius_stable_defect_support_gives_base_selector=1",
                "nonstable_defect_support_has_no_base_selector=1",
                "p24_resultant_gate_needs_semilinear_CM_section_descent=1",
                "conclusion=reported_trace_gcd_rs_tail_cyclic_section_descent_toy",
            ),
        ),
        Task(
            label="rs_tail_defect_support_accounting",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_defect_support_accounting.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_frobenius_stable_16_supports_are_exactly_two_types=1",
                "four_length4_orbits_is_not_forced_by_descent_alone=1",
                "no_fixed_defect_theorem_would_reduce_supports_from_1260_to_35=1",
                "mixed_supports_require_four_fixed_frequencies_plus_three_length4_orbits=1",
                "p24_defect_selector_still_needs_arithmetic_support_identification=1",
                "conclusion=reported_trace_gcd_rs_tail_defect_support_accounting",
            ),
        ),
        Task(
            label="rs_tail_fixed_frequency_ordinary_gate",
            argv=(
                python,
                "p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "fixed_frequency_ordinarity_is_exact_no_fixed_defect_condition=1",
                "no_fixed_defect_plus_descent_reduces_supports_to_35=1",
                "mixed_fixed_support_control_still_descends_and_has_vandermonde_unit=1",
                "mixed_support_rejected_only_by_fixed_ordinarity_not_by_descent=1",
                "p24_next_arithmetic_lemma_is_fixed_tail_inside_prefix=1",
                "conclusion=reported_trace_gcd_rs_tail_fixed_frequency_ordinary_gate",
            ),
        ),
        Task(
            label="fixed_frequency_annihilator_bridge_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_annihilator_bridge_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "annihilator_inclusion_iff_tail_in_prefix=1",
                "fixed_tail_in_prefix_removes_fixed_defect_line=1",
                "prefix_plucker_unit_is_separate_from_tail_in_prefix=1",
                "p24_dual_target_is_fixed_prefix_annihilator_kills_tail=1",
                "p24_primal_target_is_seven_fixed_frequency_linear_relations=1",
                "conclusion=reported_trace_gcd_fixed_frequency_annihilator_bridge_toy",
            ),
        ),
        Task(
            label="fixed_frequency_relation_section_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_relation_section_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "relation_section_implies_tail_in_prefix_at_all_fixed_frequencies=1",
                "valid_relation_section_removes_all_fixed_defects=1",
                "corrupted_fixed_relation_creates_fixed_defect=1",
                "prefix_plucker_unit_remains_separate_from_relation_section=1",
                "p24_relation_section_target_has_28_base_coefficients=1",
                "relation_section_must_be_constructed_intrinsically_not_postfit=1",
                "conclusion=reported_trace_gcd_fixed_frequency_relation_section_toy",
            ),
        ),
        Task(
            label="fixed_frequency_cyclic_syzygy_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_cyclic_syzygy_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "cyclic_7_syzygy_packages_seven_fixed_relations=1",
                "pointwise_relations_interpolate_because_p24_p_is_1_mod_7=1",
                "single_failed_fixed_relation_blocks_cyclic_syzygy=1",
                "prefix_plucker_full_rank_remains_separate_from_cyclic_syzygy=1",
                "p24_needs_intrinsic_cyclic_syzygy_not_postfit_coefficients=1",
                "conclusion=reported_trace_gcd_fixed_frequency_cyclic_syzygy_toy",
            ),
        ),
        Task(
            label="fixed_frequency_cramer_bezout_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_cramer_bezout_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "cramer_bezout_certificate_implies_relation_section=1",
                "denominator_unit_is_selected_prefix_plucker_gate=1",
                "full_vector_identity_detects_post_projection_corruption=1",
                "zero_divisor_denominator_rejected_before_division=1",
                "p24_fixed_frequency_certificate_surface=one_R7_unit_denominator_plus_four_numerators",
                "conclusion=reported_trace_gcd_fixed_frequency_cramer_bezout_toy",
            ),
        ),
        Task(
            label="fixed_frequency_order5_collapse_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order5_collapse_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "fixed_frequency_sections_depend_only_on_order5_collapsed_sums=1",
                "fixed_only_audit_needs_7th_roots_not_35th_roots=1",
                "nonfixed_frequencies_are_not_determined_by_order5_collapse=1",
                "p24_fixed_relation_can_be_tested_in_the_7_part=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order5_collapse_toy",
            ),
        ),
        Task(
            label="fixed_frequency_order7_coset_dictionary_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_coset_dictionary_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "order5_collapsed_six_orbit_sums_are_order7_coset_sums=1",
                "ordinary_centering_is_only_the_trivial_quotient_character=1",
                "order7_augmentation_kills_all_C7_quotient_characters=1",
                "p24_augmentation_theorem_is_a_gaussian_period_vanishing_statement=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_coset_dictionary_toy",
            ),
        ),
        Task(
            label="fixed_frequency_order7_character_projection_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_character_projection_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "orbit_character_weight_mismatches=0",
                "gauss_sum_equivalence_mismatches=0",
                "ordinary_centering_only_nontrivial_zeroes=0/6",
                "forced_projection_zeroes=6/6",
                "order7_augmentation_is_character_projection_vanishing=1",
                "generic_centering_does_not_prove_order7_augmentation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_character_projection_toy",
            ),
        ),
        Task(
            label="fixed_frequency_multiplicative_resolvent_bridge",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_multiplicative_resolvent_bridge.py",
            ),
            timeout=10.0,
            must_contain=(
                "bridge_pairing_equals_gauss_times_projection_mismatches=0",
                "ordinary_centering_nonzero_multiplicative_projections=96/96",
                "forced_h_coset_zero_projection_zeroes=96/96",
                "p156_gauss_eigenvalue_mismatches=0",
                "p156_frobenius_eigenvalue_is_carried_by_gauss_sum=1",
                "frobenius_covariance_alone_does_not_prove_h_coboundary=1",
                "conclusion=reported_trace_gcd_fixed_frequency_multiplicative_resolvent_bridge",
            ),
        ),
        Task(
            label="fixed_frequency_class_character_expansion_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_class_character_expansion_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "pairing_factor_mismatches=0",
                "projection_expansion_mismatches=0",
                "random_projection_nonzeroes=12/12",
                "random_all_product_terms_nonzeroes=12/12",
                "right_neutral_projection_zero=1",
                "multiplicative_resolvent_target_expands_into_packet_product_sum=1",
                "p24_needs_packet_cancellation_or_stronger_right_combo_vanishing=1",
                "conclusion=reported_trace_gcd_fixed_frequency_class_character_expansion_toy",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_right_combo_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_right_combo_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "right_multiplicative_packet_combos_nonzero=4/4",
                "packet_projection_nonzero=1",
                "right_neutral_control_combo_failures=0",
                "actual_cm_refutes_generic_termwise_right_combo_vanishing=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_factor_cycle_cancellation_candidate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate.py",
            ),
            timeout=10.0,
            must_contain=(
                "tensor_factor_count_over_E=70",
                "rho_factor_step_mod_70=10",
                "rho_factor_cycle_length=7",
                "covariant_character_sums_zero=6/6",
                "remaining_theorem_is_p24_factor_cycle_covariance_plus_descent=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_semilinear_factor_cycle_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_order_on_E=7",
                "rho_factor_cycle_length=7",
                "twisted_projection_ranks=[1, 1, 1, 1, 1, 1]",
                "twisted_fixed_intersection_dimensions=[0, 0, 0, 0, 0, 0]",
                "semilinear_covariance_alone_does_not_force_zero=1",
                "descent_to_rho_fixed_left_field_forces_zero=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_complete_factor_descent_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_complete_factor_descent_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "tensor_factor_count_over_E=70",
                "rho_order_on_E=7",
                "rho_factor_step_mod_70=10",
                "factor_covariance_failures=0",
                "complete_covariant_sums_nonzero=36/36",
                "complete_covariant_sums_not_fixed=36/36",
                "constructed_descended_zero_sum_nonzero_components=6/6",
                "complete_70_factor_recombination_is_the_descent_input=1",
                "remaining_arithmetic_is_complete_idempotent_factor_covariance=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_complete_factor_descent_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_internal_trace_then_hilbert90_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_order_mod_n=38843",
                "rho7_order_mod_n=5549",
                "full_trace_equals_quotient_trace_after_internal_trace_failures=0",
                "naive_quotient_trace_on_raw_seed_mismatches=48/48",
                "seven_cycle_hilbert90_requires_internal_trace_to_E_seed=1",
                "cm_lang_target_must_supply_internal_trace_or_full_order_coboundary=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_nested_internal_trace_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_nested_internal_trace_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_C_degree_over_E=179",
                "p24_B_over_C_degree=31",
                "nested_internal_trace_equals_direct_failures=0",
                "full_trace_equals_quotient_after_nested_internal_failures=0",
                "quotient_after_B_over_C_only_mismatches=48/48",
                "quotient_after_C_over_E_only_mismatches=48/48",
                "cm_lang_target_is_nested_internal_trace_then_quotient_potential=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_nested_internal_trace_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_raw_coboundary_transfer_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "raw_coboundary_transfer_failures=0",
                "quotient_trace_nonzero_after_transfer=0/48",
                "transferred_seed_not_quotient_fixed=0/48",
                "random_nested_seed_not_forced_coboundary=47/48",
                "nested_internal_trace_commutes_with_twisted_coboundary=1",
                "raw_cm_lang_coboundary_would_supply_quotient_potential=1",
                "solving_potential_after_zero_is_hilbert90_circular=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_product_coboundary_leibniz_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_product_coboundary_leibniz_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "product_coboundary_identity_failures=0",
                "product_full_twisted_trace_nonzero=0/48",
                "nested_quotient_trace_nonzero=0/48",
                "product_coboundary_leibniz_identity_holds=1",
                "left_covariance_plus_matching_right_coboundary_suffices=1",
                "p24_candidate_source_is_right_resolvent_coboundary_with_matching_twist=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_product_coboundary_leibniz_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_matching_twist_bookkeeping_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_matching_twist_bookkeeping_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_rho_mod_157=1",
                "rho_raw_h_quotient_shift=6",
                "rho_normalized_h_quotient_shift=3",
                "left_covariance_alpha_is_trivial=1",
                "raw_matching_epsilon_exponent_is_k=1",
                "matching_right_resolvent_twist_is_now_explicit=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_matching_twist_bookkeeping_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_coboundary_obstruction_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "right_resolvent_covariance_failures=0",
                "matching_twist_trace_zeroes=0/6",
                "matching_twist_coboundary_memberships=0/6",
                "opposite_twist_coboundary_memberships=6/6",
                "internal_gaussian_period_nonzeroes=8/8",
                "formal_right_covariance_is_coboundary_obstruction_not_potential=1",
                "remaining_theorem_needs_cm_lang_internal_trace_cancellation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_coboundary_internal_trace_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_coboundary_internal_trace_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "membership_iff_internal_trace_zero_failures=0",
                "random_internal_trace_zeroes=0/24",
                "forced_internal_trace_zeroes=24/24",
                "forced_coboundary_memberships=24/24",
                "matching_right_coboundary_equiv_nested_internal_trace_zero=1",
                "internal_trace_identity_is_the_non_circular_cm_lang_target=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_coboundary_internal_trace_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_internal_trace_stage_target_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_internal_trace_stage_target_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "b_over_c_trace_rank_on_quotient_eigenpackets=5",
                "nested_trace_rank_on_quotient_eigenpackets=1",
                "p24_B_over_C_trace_rank_target=179",
                "p24_nested_trace_rank_target=1",
                "forced_nested_zero_b_trace_nonzero=48/48",
                "B_over_C_trace_zero_is_sufficient_but_too_strong=1",
                "nested_internal_trace_zero_is_the_minimal_stage_target=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_stage_target_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_internal_trace_gaussian_functional_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_internal_trace_gaussian_functional_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "orbit_trace_pairing_identity_failures=0",
                "forced_trace_zero_and_all_primitive_evals_nonzero=36/36",
                "p24_internal_q_generator=p^5460_mod_n=209035",
                "p24_sample_gaussian_period_nonzeroes=8/8",
                "nested_internal_trace_is_gaussian_period_pairing=1",
                "augmentation_nonvanishing_does_not_imply_internal_trace_zero=1",
                "remaining_theorem_is_cm_lang_weighted_period_cancellation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_gaussian_functional_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_period_coset_balance_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_period_coset_balance_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "toy_period_matrix_rank=6/6",
                "trace_zero_iff_U_coset_balanced_failures=0",
                "random_unbalanced_trace_nonzero=48/48",
                "forced_balanced_trace_zero=48/48",
                "recombined_trace_zero_iff_W_coset_balanced_failures=0",
                "recombined_forced_balanced_trace_zero=48/48",
                "p24_internal_q_generator=p^5460_mod_n=209035",
                "p24_internal_order_check=5549",
                "p24_internal_coset_count=560",
                "p24_recombined_coset_count=8",
                "p24_recombined_scalar_equations=48",
                "p24_recombined_nontrivial_octic_equations=42",
                "p24_recombined_anchor_equations=6",
                "p24_recombined_compressed_values_with_c0=54",
                "quotient_gaussian_period_matrix_is_full_rank=1",
                "p24_per_factor_trace_target_equiv_to_560_coset_balance=1",
                "p24_recombined_trace_target_equiv_to_8_coset_balance=1",
                "recombined_balance_splits_into_42_octic_plus_6_anchor_equations=1",
                "recombined_theorem_is_weighted_CM_sequence_p_coset_balance=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_period_coset_balance_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_recombined_mixed_spectrum_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_recombined_mixed_spectrum_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "balance_equivalence_failures=0",
                "mixed_expansion_failures=0",
                "anchor_expansion_failures=0",
                "random_balanced_count=0/48",
                "forced_balanced_count=48/48",
                "forced_mixed_spectrum_zero=48/48",
                "forced_anchor_zero=48/48",
                "p24_mixed_octic_equations=42",
                "p24_anchor_equations=6",
                "p24_recombined_scalar_equations=48",
                "recombined_balance_iff_mixed_octic_spectrum_plus_anchor=1",
                "nontrivial_octic_equations_are_right_order7_by_relative_octic_mixed_sums=1",
                "trivial_octic_equations_are_trace_defect_anchors=1",
                "remaining_theorem_is_specific_cm_lang_mixed_spectrum_vanishing=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_recombined_mixed_spectrum_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_affine_profile_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_affine_profile_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "affine_equivalence_failures=0",
                "random_direct_payload_true=0/96",
                "forced_affine_direct_payload_true=96/96",
                "forced_affine_mixed_plus_anchor_true=96/96",
                "mixed_only_anchor_false=96/96",
                "mixed_only_direct_payload_false=96/96",
                "anchor_only_mixed_false=96/96",
                "anchor_only_direct_payload_false=96/96",
                "p24_affine_direct_equations=48",
                "p24_mixed_equations=42",
                "p24_anchor_equations=6",
                "direct_48_payload_iff_affine_right_profile_decomposition=1",
                "direct_48_payload_iff_mixed_spectrum_plus_anchor=1",
                "arithmetic_target_is_column_offsets_independent_of_right_H_coset=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_affine_profile_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_difference_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_difference_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "right_difference_equivalence_failures=0",
                "right_average_recovery_failures=0",
                "random_right_difference_true=0/96",
                "forced_affine_right_difference_true=96/96",
                "forced_affine_right_average_reconstructs=96/96",
                "column_sum_only_right_difference_false=96/96",
                "row_defect_right_difference_false=96/96",
                "p24_redundant_right_difference_equations=56",
                "p24_independent_right_difference_equations=48",
                "affine_profile_iff_right_difference_matches_selected_child=1",
                "offsets_recovered_by_right_average_when_differences_match=1",
                "arithmetic_target_can_be_stated_without_characters_or_offsets=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_difference_trace_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_difference_trace_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "toy_period_matrix_rank=8/8",
                "right_difference_trace_equivalence_failures=0",
                "random_right_difference_trace_zero=0/72",
                "forced_right_difference_trace_zero=72/72",
                "forced_right_difference_balanced=72/72",
                "single_defect_trace_nonzero=72/72",
                "single_defect_balance_false=72/72",
                "p24_redundant_adjacent_trace_equations=56",
                "p24_independent_adjacent_trace_equations=48",
                "adjacent_right_difference_balance_iff_decomposition_trace_zero=1",
                "right_difference_polynomials_are_the_new_trace_zero_targets=1",
                "proof_target_is_explicit_degree8_trace_zero_for_each_adjacent_right_difference=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_trace_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_difference_covariance_telescope_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_difference_covariance_telescope_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_rho_right_shift_mod7=6",
                "positive_covariance_failures=0",
                "positive_sum_zero=96/96",
                "positive_all_equal=96/96",
                "positive_all_zero=96/96",
                "covariance_plus_telescope_nonzero=96/96",
                "covariance_plus_telescope_anchor_not_descended=96/96",
                "descent_plus_telescope_nonzero=96/96",
                "descent_plus_telescope_covariance_fails=96/96",
                "covariance_plus_descent_without_telescope_nonzero_equal=96/96",
                "covariance_plus_anchor_descent_plus_telescope_forces_trace_zero=1",
                "covariance_plus_telescope_alone_does_not_force_zero=1",
                "descent_plus_telescope_alone_does_not_force_zero=1",
                "p24_shift6_is_coprime_to_7_and_cycles_adjacent_differences=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_covariance_telescope_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_difference_trace_covariance_functorial_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_difference_trace_covariance_functorial_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "inside_point_covariance_failures=0",
                "inside_same_coset_trace_covariance_failures=0",
                "random_same_coset_trace_covariant=0/64",
                "outside_one_step_same_coset_trace_fails=64/64",
                "outside_one_step_permuted_trace_covariance_failures=0",
                "pointwise_semilinear_covariance_with_multiplier_inside_trace_subgroup_implies_trace_covariance=1",
                "multiplier_inside_trace_subgroup_keeps_decomposition_trace_cosets_fixed=1",
                "multiplier_outside_trace_subgroup_only_gives_permuted_coset_covariance=1",
                "remaining_covariance_theorem_is_pointwise_cm_lang_frobenius_functoriality_for_P_i=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_trace_covariance_functorial_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_adjacent_anchor_descent_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_descent_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "projector_idempotent_failures=0",
                "projector_sum_failures=0",
                "rho_projector_eigen_failures=0",
                "anchor_descended_iff_nontrivial_rho_projectors_zero_failures=0",
                "covariance_orbit_failures=0",
                "covariance_plus_telescope_without_anchor_leaks=64/64",
                "covariance_plus_anchor_without_telescope_leaks=42/42",
                "fixed_anchor_telescope_forces_zero=43/43",
                "p24_raw_hcoset_equations=1092",
                "p24_compressed_right_difference_equations=48",
                "p24_single_adjacent_anchor_projectors=6",
                "single_anchor_descent_is_rho_fixedness_of_T0=1",
                "single_anchor_projectors_are_the_remaining_descent_target=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_anchor_descent_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "fixed_iff_phi7_divisible_rows=512/512",
                "projectors_zero_iff_phi7_divisible_rows=512/512",
                "random_phi7_divisible=0/512",
                "random_projector_zero=0/512",
                "forced_fixed_phi7_divisible_rows=512/512",
                "forced_nonfixed_not_phi7_divisible_rows=512/512",
                "p24_single_adjacent_anchor_projectors=6",
                "p24_single_adjacent_anchor_cyclic_remainder_degree=6",
                "single_anchor_descent_iff_phi7_divisibility=1",
                "six_projectors_compress_to_one_cyclic_remainder_mod_phi7=1",
                "adjacent_anchor_divisibility_is_finite_algebra_not_the_cm_lang_producer=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_adjacent_difference_operator_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_adjacent_difference_operator_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_right_shift_mod7=6",
                "derivative_operator=rho^6_minus_1",
                "derivative_rank=6",
                "derivative_kernel_dim=1",
                "telescope_failures=0",
                "derivative_projector_factor_failures=0",
                "nontrivial_projector_equivalence_failures=0",
                "right_axis_anchor_iff_adjacent_anchor_failures=0",
                "equal_profile_iff_zero_adjacent_differences_failures=0",
                "adjacent_anchor_is_invertible_difference_on_nonfixed_quotient=1",
                "adjacent_anchor_descent_equivalent_to_right_axis_anchor_descent=1",
                "remaining_arithmetic_is_same_equal_H_coset_sum_theorem_for_selected_packet=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_difference_operator_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_mixed_spectrum_resolvent_bridge",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_mixed_spectrum_resolvent_bridge.py",
            ),
            timeout=20.0,
            must_contain=(
                "gauss_bridge_failures=0",
                "random_all_additive_resolvents_nonzero=24/24",
                "random_normal_like_mixed_nonzero=24/24",
                "forced_mixed_zero_with_all_additive_resolvents_nonzero=24/24",
                "forced_additive_resolvent_zero_with_mixed_nonzero=24/24",
                "mixed_spectrum_is_gauss_weighted_additive_resolvent_combination=1",
                "mixed_spectrum_is_not_a_single_class_character_resolvent=1",
                "additive_reduced_normality_does_not_imply_mixed_spectrum_nonzero=1",
                "additive_reduced_normality_does_not_imply_mixed_spectrum_zero=1",
                "remaining_theorem_needs_stickelberger_or_cm_lang_relation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_mixed_spectrum_resolvent_bridge",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_mixed_spectrum_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_mixed_spectrum_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "D=-4751",
                "q=4787",
                "h=91",
                "right_quotient=3",
                "relative_quotient=4",
                "mixed_equations_per_shift=6",
                "anchor_equations_per_shift=2",
                "balance_equations_per_shift=8",
                "shift0_mixed_zeroes=0/6",
                "shift0_anchor_zeroes=0/2",
                "shift0_balance_passes=0/8",
                "full_mixed_zero_shifts=0/91",
                "full_anchor_zero_shifts=0/91",
                "full_recombined_balance_shifts=0/91",
                "best_mixed_zeroes_any_shift=0/6",
                "best_balance_passes_any_shift=0/8",
                "actual_cm_both_axes_nontrivial_boundary=1",
                "actual_cm_mixed_spectrum_vanishing_is_not_generic=1",
                "actual_cm_origin_shift_does_not_rescue_mixed_balance=1",
                "p24_needs_specific_trace_gcd_cm_lang_relation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_mixed_spectrum_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_anchor_trace_defect_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "anchor_defect_projection_mismatches=0",
                "anchor_zero_iff_trace_defect_h_coset_equal_failures=0",
                "random_anchor_nonzero=48/48",
                "forced_trace_defect_equal_cosets=48/48",
                "forced_anchor_zero=48/48",
                "p24_anchor_equations=6",
                "anchor_equation_equals_relative_trace_defect_character_projection=1",
                "six_anchors_zero_iff_trace_defect_has_equal_H_coset_sums=1",
                "p24_anchor_is_not_constant_term_bookkeeping=1",
                "p24_anchor_target_is_relative_trace_defect_order7_spectrum_zero=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_anchor_vs_c_centering_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_anchor_vs_c_centering_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "right_degree=7",
                "c_degree=179",
                "b_over_c_degree=31",
                "internal_size=5549",
                "packet_realization_failures=0",
                "random_anchor_and_bidegree_both_pass=0/32",
                "random_anchor_and_bidegree_both_fail=32/32",
                "forced_anchor_pass_bidegree_fail=32/32",
                "forced_bidegree_pass_anchor_fail=32/32",
                "forced_anchor_and_bidegree_both_pass=32/32",
                "trace_defect_anchor_zero_does_not_imply_C_trivial_bidegree_zero=1",
                "C_trivial_bidegree_zero_does_not_imply_trace_defect_anchor_zero=1",
                "selected_section_subtraction_can_mask_forbidden_bidegree=1",
                "proof_must_control_selected_child_right_profile_or_C_centering=1",
                "anchor_and_C_centering_are_distinct_arithmetic_inputs=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_anchor_vs_c_centering_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_trace_average_anchor_payload_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "profile_decomposition_failures=0",
                "random_trace_average_anchor_passes=0/48",
                "forced_defect_h_sums_equal=48/48",
                "fake_equal_h_sum_payloads_pass=48/48",
                "p24_defect_hcoset_sum_payload=7",
                "p24_full_trace_average_plus_child_payload=132508",
                "p24_full_trace_average_plus_child_payload_over_sqrt=1.325080000000e-07",
                "anchor_can_be_verified_from_seven_defect_H_coset_sums=1",
                "full_trace_average_plus_child_profile_is_subsqrt_for_p24=1",
                "equal_sum_payload_requires_producer_honesty=1",
                "trace_average_route_still_needs_embedded_child_or_morphism=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_section_choice_obstruction_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "same_trace_profile_counterexample=1",
                "same_trace_child0_anchor_passes=1",
                "same_trace_child1_anchor_passes=0",
                "random_child_shift_changes_defect_sums=48/48",
                "actual_cm_global_child_shift_anchor_zeroes=0/5",
                "actual_cm_global_child_shift_distinct_defects=5/5",
                "actual_cm_distinct_child_coefficients=5/5",
                "p24_trace_only_profile_payload=66254",
                "p24_trace_plus_child_profile_payload=132508",
                "p24_trace_plus_child_profile_payload_over_sqrt=1.325080000000e-07",
                "quotient_trace_profile_alone_does_not_determine_anchor=1",
                "selected_child_section_is_arithmetic_data_not_bookkeeping=1",
                "unordered_relative_trace_coefficients_do_not_authenticate_defect=1",
                "p24_anchor_producer_must_be_section_aware=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_internal_character_filter_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_internal_character_filter_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_order_mod_n=38843",
                "internal_generator=p^(780*7)_mod_n=209035",
                "b_over_c_order=31",
                "c_over_e_order=179",
                "raw_twist_survives_seven_steps_failures=0",
                "random_order7_packets_internal_trace_nonzero=36/36",
                "forced_zero_trivial_c_component_internal_trace_zero=36/36",
                "nontrivial_c_character_packets_internal_trace_zero=36/36",
                "order7_quotient_twist_dies_after_internal_generator=1",
                "nested_internal_trace_zero_is_zero_trivial_C_character_component=1",
                "remaining_theorem_is_no_trivial_C_character_in_B_over_C_obstruction=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_internal_character_filter_gate",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_internal_character_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_internal_character_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-5000",
                "q=3851",
                "class_number=30",
                "rows_checked=60",
                "trivial_C_projection_zeroes=0/60",
                "all_nontrivial_C_projections_nonzero=60/60",
                "ordinary_cm_periods_do_not_satisfy_internal_character_filter=1",
                "internal_filter_needs_specific_obstruction_not_raw_j_cycle=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_internal_character_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_gauss_weighted_polynomial_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_gauss_weighted_polynomial_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "field_q=8863",
                "right=211",
                "gauss_identity_failures=0",
                "residue_zero_additive_sums=6/6",
                "right_resolvent_to_weighted_polynomial_failures=0",
                "random_weighted_polynomial_internal_trace_nonzero=12/12",
                "forced_weighted_polynomial_internal_trace_zero=12/12",
                "right_obstruction_is_gauss_sum_times_weighted_relative_polynomial=1",
                "weighted_polynomial_internal_trace_zero_is_not_formal=1",
                "remaining_theorem_is_internal_trace_zero_for_this_weighted_cm_polynomial=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_gauss_weighted_polynomial_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_axis_spectrum_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_axis_spectrum_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_log_mod_order7_quotient=2",
                "rho_log_mod_order7_quotient=6",
                "internal_log_base2_mod_211=0",
                "random_profiles_with_order7_leak=48/48",
                "forced_equal_H_coset_sums_projection_zero=48/48",
                "projection_zero_iff_H_coset_sums_equal_failures=0",
                "p5460_internal_trace_fixes_right_211_axis=1",
                "internal_trace_does_not_average_right_H_cosets=1",
                "target_is_no_order7_multiplicative_spectrum_on_traced_right_axis=1",
                "equivalently_H_coset_sums_equal_on_F211_star=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_spectrum_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_axis_covariance_descent_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_axis_covariance_descent_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_fixes_left157=1",
                "rho_log_base2_mod_211=90",
                "rho_log_mod_order7_quotient=6",
                "internal_log_base2_mod_211=0",
                "covariance_alone_order7_leak=48/48",
                "covariance_alone_equal_H_coset_sums=0/48",
                "descent_alone_order7_leak=48/48",
                "descent_alone_equal_H_coset_sums=0/48",
                "covariance_plus_descent_projection_zero=48/48",
                "covariance_plus_descent_equal_H_coset_sums=48/48",
                "covariant_projection_zero_iff_anchor_descends_failures=0",
                "projection_zero_iff_equal_H_coset_sums_failures=0",
                "under_covariance_one_anchor_descent_is_equivalent_to_H_coset_equality=1",
                "right_axis_covariance_plus_descent_forces_H_coset_sums_equal=1",
                "remaining_arithmetic_is_covariance_and_descent_for_traced_G_chi_profile=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_covariance_descent_gate",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_right_axis_covariance_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "D=-6719",
                "q=6863",
                "h=105",
                "m=21",
                "n=5",
                "rho_left_mod_left=1",
                "rho_right_log_mod_quotient=2",
                "internal_right_mod_right=1",
                "additive_resolvent_covariance_failures=0",
                "anchor_coset_descended=0/2",
                "equal_H_coset_sums=0/2",
                "gauss_normalized_nonzero_projections=4/4",
                "gauss_normalized_projection_rho_fixed=4/4",
                "actual_cm_additive_resolvent_covariance_holds=1",
                "gauss_normalized_projection_can_be_rho_fixed_and_nonzero=1",
                "covariance_plus_gauss_normalization_does_not_imply_anchor_descent=1",
                "p24_still_needs_section_aware_anchor_descent_or_equal_H_coset_sums=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_adjacent_anchor_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_adjacent_anchor_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "D=-6719",
                "q=6863",
                "h=105",
                "m=21",
                "n=5",
                "rho_left_mod_left=1",
                "rho_right_shift_mod_quotient=2",
                "adjacent_difference_covariance_failures=0",
                "adjacent_difference_telescope_zero=2/2",
                "adjacent_anchor_descended=0/2",
                "adjacent_anchor_nonzero=2/2",
                "adjacent_differences_all_zero=0/2",
                "covariance_telescope_do_not_force_adjacent_anchor_in_actual_cm=1",
                "actual_cm_adjacent_anchor_descent_not_generic=1",
                "p24_needs_specific_trace_gcd_adjacent_packet=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_adjacent_anchor_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_left_paired_h_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_left_paired_h_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "D=-6719",
                "q=6863",
                "h=105",
                "m=21",
                "n=5",
                "rho_left_mod_left=1",
                "rho_right_log_mod_quotient=2",
                "covariance_failures_by_left_frequency=[0, 0, 0]",
                "equal_H_coset_sums_by_left_frequency=[0, 0, 0]",
                "anchor_descended_by_left_frequency=[0, 0, 0]",
                "gauss_normalized_nonzero_by_left_frequency=[4, 4, 4]/[4, 4, 4]",
                "gauss_normalized_fixed_by_left_frequency=[4, 4, 4]/[4, 4, 4]",
                "nontrivial_left_equal_H_coset_sums=0/4",
                "nontrivial_left_anchor_descended=0/4",
                "nontrivial_left_gauss_normalized_nonzero=8/8",
                "nontrivial_left_gauss_normalized_fixed=8/8",
                "actual_cm_left_pairing_preserves_covariance=1",
                "nontrivial_left_pairing_does_not_force_H_coboundary=1",
                "paired_profile_theorem_needs_trace_gcd_weighted_product_structure=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_left_paired_h_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_danger_anchor_condition_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_danger_anchor_condition_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "testable_danger_cm_cases=10",
                "case 1: p=359 A=1 trace=-24 k=5 D=-860 h=14 ell=3",
                "case 10: p=983 A=1 trace=24 k=6 D=-3356 h=33 ell=3",
                "danger_anchor_decompositions_with_any_passing_section=0/19",
                "danger_anchor_global_section_passes=0/385",
                "strict_danger_2adic_order_condition_does_not_force_anchor_descent=1",
                "small_danger_cm_rows_have_no_global_section_anchor_passes=1",
                "p24_anchor_theorem_needs_more_than_curve_order_congruence=1",
                "conclusion=reported_trace_gcd_fixed_frequency_danger_anchor_condition_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_axis_fixed_field_refinement_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_axis_fixed_field_refinement_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_log_mod_order7_quotient=6",
                "right_model_ord_211_q=35",
                "right_model_q_frobenius_power_for_rho=15",
                "rho_order_on_right_model=7",
                "right_model_rho_fixed_dimension=5",
                "p24_left_degree=156",
                "p24_right_rho_fixed_degree=5",
                "p24_rho_fixed_E_degree=780",
                "pure_H_period_covariance_failures=0",
                "pure_H_period_anchor_fixed=0",
                "pure_H_period_nontrivial_projection_leaks=6/6",
                "rho_fixed_field_is_larger_than_left_mu157_field=1",
                "anchor_descent_to_rho_fixed_field_is_the_exact_finite_need=1",
                "traced_G_chi_must_cancel_the_nonfixed_right_period_part=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_fixed_field_refinement_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_axis_anchor_projector_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_axis_anchor_projector_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_log_mod_order7_quotient=6",
                "projector_model_q=43",
                "projector_model_degree=7",
                "period_control_field_q=8863",
                "projector_idempotent_failures=0",
                "anchor_fixed_iff_nontrivial_projectors_zero_failures=0",
                "random_anchor_fixed_count=0/24",
                "forced_anchor_fixed_count=24/24",
                "forced_anchor_nontrivial_projectors_zero=24/24",
                "pure_H_anchor_fixed=0",
                "pure_H_anchor_equal_cosets=0",
                "pure_H_anchor_nontrivial_projectors_nonzero=6/6",
                "anchor_fixedness_is_six_rho_eigenprojector_vanishings=1",
                "pure_H_periods_show_the_missing_theorem_is_real_cancellation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_anchor_projector_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_axis_projector_character_bridge",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_axis_projector_character_bridge.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_log_mod_order7_quotient=6",
                "rho_shift_inverse_mod7=6",
                "anchor_projector_to_quotient_character_index_map=[0, 6, 5, 4, 3, 2, 1]",
                "bridge_identity_failures=0",
                "nontrivial_anchor_zero_iff_nontrivial_quotient_zero_failures=0",
                "random_nonzero_anchor_projectors=32/32",
                "random_nonzero_quotient_projections=32/32",
                "anchor_projectors_are_relabelled_H_quotient_characters_under_covariance=1",
                "p24_shift6_pairs_projector_indices_1_6_2_5_3_4=1",
                "proving_six_anchor_projectors_zero_is_same_as_1092_nontrivial_payload=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_projector_character_bridge",
            ),
        ),
        Task(
            label="fixed_frequency_p24_projector_internal_character_target_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_projector_internal_character_target_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_log_mod_order7_quotient=6",
                "rho_order_mod_n=38843",
                "internal_order=5549",
                "b_over_c_order=31",
                "c_over_e_order=179",
                "projector_idempotent_failures=0",
                "projector_commutes_with_B_over_C_trace_failures=0",
                "random_projected_packets_final_internal_trace_nonzero=143/144",
                "forced_nontrivial_C_character_final_trace_zero=6/6",
                "forced_nontrivial_C_character_B_trace_nonzero=6/6",
                "forced_trivial_C_character_final_trace_nonzero=6/6",
                "forced_trivial_C_character_detected_by_projection=6/6",
                "quotient_projectors_commute_with_internal_B_over_C_trace=1",
                "quotient_projector_alone_does_not_force_final_internal_trace_zero=1",
                "nontrivial_C_character_support_would_force_final_trace_zero=1",
                "p24_missing_theorem_is_no_trivial_C_component_in_each_projector_channel=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_projector_internal_character_target_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_right_c_bidegree_support_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_right_c_bidegree_support_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "toy_gcd_C7_C5=1",
                "p24_gcd_C7_C179=1",
                "bidegree_projector_commutation_failures=0",
                "final_trace_iff_no_trivial_C_bidegree_failures=0",
                "random_packets_with_trivial_C_leakage=48/48",
                "forced_no_trivial_C_bidegree_passes=48/48",
                "graph_nontrivial_C_support_final_trace_zero=1",
                "trivial_C_support_leaks=1",
                "trivial_C_forbidden_bidegrees_nonzero=6/6",
                "final_internal_trace_zero_is_absence_of_right_nontrivial_C_trivial_bidegrees=1",
                "p24_has_no_nontrivial_group_hom_from_C7_to_C179=1",
                "bidegree_support_separation_must_come_from_weighted_packet_not_group_hom=1",
                "remaining_theorem_is_vanishing_of_right_nontrivial_C_trivial_bidegrees=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_right_c_bidegree_support_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_stickelberger_bidegree_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_stickelberger_bidegree_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "right_degree=7",
                "c_degree=179",
                "gcd_right_c=1",
                "cyclic_stickelberger_forbidden_nonzero=6/6",
                "cyclic_centered_stickelberger_forbidden_nonzero=6/6",
                "right_axis_stickelberger_forbidden_nonzero=6/6",
                "right_axis_centered_stickelberger_forbidden_nonzero=6/6",
                "c_axis_centered_stickelberger_forbidden_nonzero=0/6",
                "centered_product_forbidden_nonzero=0/6",
                "plain_cyclic_stickelberger_leaks_forbidden_bidegrees=1",
                "plain_right_axis_stickelberger_leaks_forbidden_bidegrees=1",
                "successful_jacobi_sum_proof_must_explain_C_centering_from_weighted_packet=1",
                "generic_stickelberger_slogan_is_not_the_missing_anchor_theorem=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_stickelberger_bidegree_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_jacobi_carry_c_centering_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "field_q=32579",
                "right_degree=7",
                "c_degree=179",
                "plain_stickelberger_forbidden_nonzero=6/6",
                "sample_c_axis_jacobi_forbidden_coefficients=[0, 0, 0, 0, 0, 0]",
                "c_axis_jacobi_forbidden_zero=48/48",
                "both_c_axis_jacobi_forbidden_zero=48/48",
                "generic_jacobi_forbidden_leaks=48/48",
                "c_axis_pure_right_partner_leaks=48/48",
                "c_axis_sum_pure_right_leaks=48/48",
                "jacobi_carry_with_C_axis_input_kills_forbidden_bidegrees=1",
                "generic_jacobi_carry_still_leaks_forbidden_bidegrees=1",
                "jacobi_sum_route_must_use_C_axis_character_support=1",
                "positive_proof_target_is_C_axis_jacobi_carry_decomposition=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_jacobi_carry_span_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "broad_rank_formula_matches=5/5",
                "admissible_rank_formula_matches=5/5",
                "admissible_support_zero=5/5",
                "leaky_controls_forbidden_nonzero=5/5",
                "admissible_carry_span_strict_subspace=5/5",
                "p24_broad_c_axis_carry_rank_formula=625",
                "p24_admissible_c_axis_carry_rank_formula=621",
                "p24_broad_minus_admissible_rank=4",
                "p24_origin_normalized_no_forbidden_dim=1246",
                "broad_C_axis_rank_625_includes_leaky_directions=1",
                "p24_positive_target_is_rank_621_admissible_C_axis_carry_subspace=1",
                "weighted_packet_must_land_in_specific_admissible_jacobi_carry_span=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_jacobi_carry_fourier_formula_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "formula_matches=3/3",
                "lambda_formula_matches=3/3",
                "dual_condition_rows_match=3/3",
                "c_zero_fiber_rows_match=3/3",
                "p24_pair_sum_lambda_rational=-2/(179-1)=-1/89",
                "sawtooth_dft_formula_matches_brute_dft=1",
                "admissible_carry_pair_sum_lambda_is_minus_2_over_c_minus_1=1",
                "conjugate_skew_comes_from_sawtooth_pair_sum_cancellation=1",
                "global_balances_come_from_c_zero_fiber_vanishing=1",
                "finite_dual_conditions_are_symbolic_jacobi_carry_identities=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_admissible_jacobi_spectral_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "spectral_pattern_matches=3/3",
                "p24_conjugate_C_pair_count=89",
                "p24_spectral_rank_formula=1+7*88+4=621",
                "admissible_span_has_conjugate_C_pair_rank_8_not_14=1",
                "p24_rank_621_has_spectral_formula_1_plus_7_times_88_plus_4=1",
                "proof_target_is_pair_compatibility_not_only_forbidden_support=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_admissible_jacobi_dual_conditions_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "dual_condition_matches=3/3",
                "p24_conjugate_C_pair_count=89",
                "p24_dual_condition_count=6+6*89+89+3=632",
                "p24_dual_solution_dim=1253-632=621",
                "admissible_span_equals_explicit_four_family_fourier_conditions=1",
                "pair_skew_conditions_are_F_a_b_plus_F_minus_a_minus_b_zero=1",
                "three_global_balances_are_sum_b_F_minus_a_b_minus_F_a_b_zero=1",
                "p24_membership_target_is_explicit_632_equation_fourier_system=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_dual_conditions_value_side_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "value_dual_equivalence_random_checks=3/3",
                "value_dual_rank_matches=3/3",
                "admissible_carries_satisfy_value_conditions=3/3",
                "random_controls_reject_both=3/3",
                "four_dual_fourier_families_equal_three_value_side_packet_identities=1",
                "value_identity_1_C_row_sums_independent=1",
                "value_identity_2_C_zero_fiber_vanishes=1",
                "value_identity_3_inversion_complement_constant_off_C_zero=1",
                "selected_packet_proof_can_target_value_side_identities=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_value_identity_strength_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_value_identity_strength_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "rank_matches=3/3",
                "p24_zero_plus_inversion_rank=7*89+6=629",
                "p24_full_value_rank=7*89+9=632",
                "p24_row_sum_extra_after_zero_plus_inversion=3",
                "p24_value_solution_dim=1253-632=621",
                "verifier_minimal_row_sum_identity_has_rank_6=1",
                "c_zero_plus_inversion_constant_leave_three_global_balances=1",
                "value_side_identities_are_stronger_than_verifier_minimal_trace_zero=1",
                "arithmetic_proof_can_split_into_structural_symmetry_plus_three_balances=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_value_identity_strength_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_selected_defect_value_producer_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "selected_defect_producer_equivalence=3/3",
                "forced_raw_producer_hits=3/3",
                "selected_defect_only_controls=3/3",
                "inversion_only_controls=3/3",
                "affine_only_controls=3/3",
                "selected_defect_automatically_gives_C_zero_fiber=1",
                "raw_two_level_inversion_plus_selected_affine_balance_iff_value_identities=1",
                "raw_inversion_without_affine_balance_leaks_row_sums=1",
                "raw_affine_balance_without_inversion_leaks_structural_symmetry=1",
                "selected_defect_producer_target_is_raw_complement_plus_affine_balance=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_multiplicative_producer_dictionary_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "multiplicative_additive_equivalence=3/3",
                "forced_product_formula_hits=3/3",
                "inversion_product_without_row_ratio_controls=3/3",
                "row_ratio_without_inversion_product_controls=3/3",
                "raw_complement_law_is_pair_product_constancy=1",
                "selected_affine_balance_is_selected_row_product_ratio_constancy=1",
                "product_formula_producer_target_matches_additive_selected_defect_target=1",
                "product_complement_without_row_ratio_leaks_balances=1",
                "row_ratio_without_product_complement_leaks_structural_symmetry=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_sum_product_formula_probe",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe.py",
            ),
            timeout=20.0,
            must_contain=(
                "raw_off_c_pair_product_rows=3/3",
                "raw_two_level_pair_product_rows=0/3",
                "raw_row_ratio_rows=0/3",
                "c_zero_normalized_row_ratio_rows=0/3",
                "right_mixed_no_row_ratio_rows=3/3",
                "right_mixed_no_c_zero_normalized_row_ratio_rows=3/3",
                "honest_jacobi_sums_supply_off_c_inversion_product_complement=1",
                "degenerate_c_zero_fiber_needs_selected_normalization=1",
                "row_product_ratio_is_not_automatic_for_raw_jacobi_sums=1",
                "product_formula_target_needs_extra_distribution_or_selected_ratio=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_sum_row_ratio_miner",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_sum_row_ratio_miner.py",
            ),
            timeout=30.0,
            must_contain=(
                "right_mixed_no_constant_row_ratio_rows=3/3",
                "right_mixed_nonzero_right_constant_row_ratio_rows=3/3",
                "right_mixed_non_cyclotomic_defect_rows=3/3",
                "right_mixed_universal_anchor_defect_rows=3/3",
                "right_mixed_anchor_defect_formula_rows=3/3",
                "row_ratio_defect_is_not_small_root_of_unity_multiplier=1",
                "right_mixed_jacobi_sums_have_constant_nonzero_right_row_ratio=1",
                "remaining_row_ratio_defect_is_the_right_zero_anchor=1",
                "anchor_defect_is_universal_across_sampled_admissible_pairs=1",
                "anchor_defect_equals_q_minus_2_to_minus_c_minus_1=1",
                "selected_anchor_ratio_needs_genuine_unit_or_distribution_correction=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_row_ratio_miner",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_sum_anchor_correction_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py",
            ),
            timeout=30.0,
            must_contain=(
                "raw_full_pair_failure_rows=3/3",
                "raw_row_ratio_failure_rows=3/3",
                "exhaustive_right_mixed_pairs=72",
                "exhaustive_right_mixed_pairs=540",
                "exhaustive_right_mixed_pairs=792",
                "expected_zero_fiber_degeneracy_rows=3/3",
                "single_anchor_correction_rows=3/3",
                "corrected_pair_product_rows=3/3",
                "corrected_row_ratio_rows=3/3",
                "corrected_product_formula_rows=3/3",
                "anchor_scale_formula_rows=3/3",
                "raw_right_mixed_jacobi_packet_fails_only_by_degenerate_anchor=1",
                "correcting_single_J_1_1_anchor_by_q_minus_2_inverse_fixes_pair_products=1",
                "correcting_single_J_1_1_anchor_by_q_minus_2_inverse_fixes_row_ratio=1",
                "anchor_correction_scale_is_inverse_of_mined_delta=1",
                "punctured_hasse_davenport_plus_single_anchor_gives_product_formula=1",
                "p24_selected_packet_needs_analogue_of_single_anchor_unit=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_sum_anchor_scalar_search",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search.py",
            ),
            timeout=30.0,
            must_contain=(
                "exhaustive_anchor_scalar_search_rows=3/3",
                "valid_anchor_scalars_are_plus_minus_one_rows=3/3",
                "reduced_packet_plus_one_anchor_rows=3/3",
                "raw_q_minus_2_anchor_rejected_rows=3/3",
                "finite_jacobi_anchor_scalar_search_space_collapses_to_two_signs=1",
                "plus_one_is_the_reduced_jdagger_anchor_used_by_cyclotomic_residual=1",
                "minus_one_is_a_remaining_scalar_sign_ambiguity_not_a_new_divisor_shape=1",
                "p24_anchor_search_should_focus_on_cm_lang_realization_plus_sign_normalization=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_anchor_residual_factor_search",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_anchor_residual_factor_search.py",
            ),
            timeout=10.0,
            must_contain=(
                "plus_one_branch_has_no_base_field_residual_split_rows=3/3",
                "minus_one_branch_has_no_base_field_residual_split_rows=3/3",
                "no_valid_sign_has_base_field_residual_split_rows=3/3",
                "c_power_root_criterion_rows=3/3",
                "row_sum_slice_times_R_c_residual_requires_c_th_root_of_anchor_scalar=1",
                "finite_jacobi_value_field_has_no_such_root_for_either_valid_sign=1",
                "residual_unit_should_be_handled_divisorially_or_after_norm_extension=1",
                "base_field_separate_slice_factorization_is_a_dead_end=1",
                "p24_cm_lang_proof_must_use_integral_norm_or_divisor_language_for_R_179=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_anchor_residual_factor_search",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_anchor_kummer_descent_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "kummer_selected_descent_rows=6/6",
                "kummer_Rc_exponent_unique_e_one_rows=6/6",
                "kummer_row_sum_and_residual_nonbase_rows=6/6",
                "kummer_no_base_field_split_rows=6/6",
                "p24_kummer_auxiliary_degree=179",
                "p24_R179_exponent_for_selected_correction=1",
                "adjoining_beta_with_beta_c_equals_selected_scalar_splits_anchor_slices=1",
                "row_sum_slice_and_R_c_residual_product_descends_to_base_correction=1",
                "selected_correction_forces_R_c_exponent_e_equals_1=1",
                "p24_target_is_auxiliary_kummer_or_norm_descent_for_R_179_with_sign=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate",
            ),
        ),
        Task(
            label="fixed_frequency_jacobi_sum_symbolic_hd_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "symbolic_pair_count_rows=6/6",
                "symbolic_admissible_rows=6/6",
                "symbolic_pair_product_rows=6/6",
                "symbolic_row_ratio_rows=6/6",
                "symbolic_reduced_anchor_rows=6/6",
                "symbolic_producer_rows=6/6",
                "p24_symbolic_right_mixed_pairs=189036",
                "row_ratio_gauss_factors_cancel_to_c_axis_product=1",
                "reduced_jacobi_packet_satisfies_symbolic_product_formula=1",
                "p24_c179_symbolic_hasse_davenport_conditions_hold=1",
                "remaining_p24_input_is_cm_lang_realization_of_reduced_packet=1",
                "conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_fingerprint_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "anchor_selected_defect_rows=6/6",
                "anchor_support_rows=6/6",
                "anchor_fourier_profile_rows=6/6",
                "anchor_forbidden_c_trivial_leak_rows=6/6",
                "anchor_right_difference_profile_rows=6/6",
                "anchor_row_sum_profile_rows=6/6",
                "p24_anchor_nonzero_entries=178",
                "single_anchor_correction_becomes_punctured_right_zero_row=1",
                "anchor_fingerprint_has_all_right_frequencies_and_fixed_c_profile=1",
                "anchor_fingerprint_alone_leaks_forbidden_c_trivial_bidegrees=1",
                "anchor_fingerprint_right_difference_is_two_adjacent_punctured_rows=1",
                "p24_cm_lang_anchor_must_supply_this_selected_defect_fingerprint=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_adjacent_bridge_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "b0_slice_matches_row_sum_rows=6/6",
                "anchor_b0_forbidden_leak_rows=6/6",
                "adjacent_difference_multiplier_rows=6/6",
                "adjacent_difference_nonfixed_invertible_rows=6/6",
                "anchor_diff_telescope_rows=6/6",
                "opposite_raw_leak_cancel_rows=6/6",
                "mismatched_anchor_leak_control_rows=6/6",
                "p24_anchor_b0_nontrivial_projectors=6",
                "adjacent_anchor_sees_c_trivial_slice_of_reduced_anchor=1",
                "reduced_anchor_row_sum_profile_generates_all_six_nonfixed_right_channels=1",
                "right_difference_is_invertible_on_that_nonfixed_slice=1",
                "old_adjacent_anchor_target_is_cancellation_of_reduced_anchor_b0_leak=1",
                "full_punctured_anchor_still_requires_cm_lang_realization_not_just_b0_slice=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_slice_decomposition_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "slice_reconstruction_rows=6/6",
                "c_trivial_slice_profile_rows=6/6",
                "c_nontrivial_slice_profile_rows=6/6",
                "c_nontrivial_rowsum_zero_rows=6/6",
                "c_nontrivial_spatial_formula_rows=6/6",
                "old_adjacent_anchor_invisible_c_nontrivial_rows=6/6",
                "full_remaining_nontrivial_channel_rows=6/6",
                "p24_remaining_c_nontrivial_fourier_channels=1246",
                "adjacent_bridge_accounts_only_for_c_trivial_row_sum_slice=1",
                "c_nontrivial_slice_has_zero_row_sums_and_is_invisible_to_old_adjacent_anchor=1",
                "cm_lang_unit_must_realize_full_punctured_row_not_only_b0_slice=1",
                "remaining_p24_anchor_realization_has_1246_c_nontrivial_fourier_channels=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_cyclotomic_divisor_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "integral_residual_matches_cyclotomic_divisor_rows=6/6",
                "cyclotomic_residual_degree_zero_rows=6/6",
                "cyclotomic_residual_spatial_formula_rows=6/6",
                "cyclotomic_residual_fourier_profile_rows=6/6",
                "principal_cyclotomic_divisor_profile_rows=6/6",
                "cyclotomic_residual_channel_count_rows=6/6",
                "p24_cyclotomic_residual_divisor_degree_zero=1",
                "p24_residual_integral_fourier_channels=1246",
                "c_nontrivial_residual_clears_to_integral_degree_zero_divisor=1",
                "c_nontrivial_residual_is_cyclotomic_principal_divisor_after_clearing_c=1",
                "candidate_unit_R_c_equals_Phi_c_over_X_minus_1_power_c_minus_1=1",
                "p24_candidate_unit_is_R_179_equals_Phi_179_over_X_minus_1_power_178=1",
                "p24_remaining_arithmetic_is_cm_lang_specialization_and_p_integrality=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_diamond_norm_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "diamond_norm_divisor_rows=6/6",
                "diamond_norm_polynomial_rows=6/6",
                "diamond_norm_fourier_profile_rows=6/6",
                "diamond_norm_orbit_size_rows=6/6",
                "diamond_norm_full_unit_orbit_rows=6/6",
                "p24_diamond_norm_orbit_size=178",
                "p24_diamond_norm_residual_fourier_channels=1246",
                "R_c_residual_is_diamond_norm_of_single_point_divisor=1",
                "product_over_nonzero_c_multipliers_gives_Phi_c_over_X_minus_1_power=1",
                "this_is_diamond_norm_not_cyclic_C_over_E_trace_norm=1",
                "p24_candidate_is_diamond_norm_of_one_p_integral_cm_lang_factor=1",
                "p24_then_needs_auxiliary_kummer_sign_descent_for_selected_anchor=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "cyclic_translation_trace_zero_rows=6/6",
                "cyclic_product_telescopes_rows=6/6",
                "diamond_norm_residual_rows=6/6",
                "diamond_product_residual_rows=6/6",
                "cyclic_translation_not_residual_rows=6/6",
                "cyclic_and_diamond_orbit_sizes_distinct_rows=6/6",
                "p24_cyclic_translation_orbit_size=179",
                "p24_diamond_orbit_size=178",
                "cyclic_C_over_E_translation_norm_of_one_point_factor_is_trivial=1",
                "diamond_unit_norm_of_one_point_factor_is_the_R_c_residual=1",
                "ordinary_cyclic_trace_norm_erases_the_selected_anchor_residual=1",
                "p24_producer_must_use_diamond_norm_not_cyclic_C_over_E_norm=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "single_point_elliptic_nonprincipal_rows=6/6",
                "miller_c_power_principal_rows=6/6",
                "nonzero_subgroup_sum_zero_rows=6/6",
                "diamond_subgroup_residual_principal_rows=6/6",
                "diamond_subgroup_matches_cyclotomic_residual_rows=6/6",
                "miller_diamond_is_c_times_residual_rows=6/6",
                "direct_subgroup_divisor_target_rows=6/6",
                "p24_subgroup_order=179",
                "p24_nonzero_subgroup_divisor_degree=178",
                "individual_one_point_divisor_is_not_an_elliptic_unit_divisor=1",
                "miller_c_multiple_is_principal_but_its_diamond_norm_is_R_c_to_c=1",
                "whole_nonzero_subgroup_divisor_is_principal_for_odd_c=1",
                "p24_target_can_be_direct_diamond_subgroup_divisor_not_single_point_factor=1",
                "remaining_problem_is_cm_lang_specialization_and_p_integrality_of_this_subgroup_divisor=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_kernel_polynomial_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "actual_kernel_root_pair_rows=6/6",
                "actual_kernel_paired_x_rows=6/6",
                "actual_kernel_subgroup_sum_zero_rows=6/6",
                "actual_kernel_pole_order_rows=6/6",
                "actual_kernel_divisor_degree_zero_rows=6/6",
                "formal_kernel_degree_rows=6/6",
                "formal_kernel_pole_order_rows=6/6",
                "formal_kernel_divisor_degree_zero_rows=6/6",
                "formal_velu_x_denominator_degree_rows=6/6",
                "p24_kernel_polynomial_degree=89",
                "p24_kernel_divisor_pole_order=178",
                "kernel_polynomial_has_exact_subgroup_residual_divisor=1",
                "unsquared_kernel_polynomial_matches_R_c_not_R_c_squared=1",
                "velu_x_coordinate_denominator_is_the_square_of_the_kernel_polynomial=1",
                "p24_target_can_be_kernel_polynomial_for_selected_179_subgroup=1",
                "remaining_problem_is_constructing_selected_cm_lang_kernel_polynomial_without_class_enumeration=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_local_unit_criterion_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "cyclotomic_diamond_product_identity_rows=6/6",
                "cyclotomic_local_unit_criterion_rows=6/6",
                "cyclotomic_unit_count_rows=6/6",
                "kernel_local_unit_criterion_rows=4/4",
                "kernel_unit_count_rows=4/4",
                "kernel_zero_pole_count_rows=4/4",
                "p24_forbidden_cyclotomic_anchor_count=179",
                "R_c_specialization_is_unit_iff_coordinate_avoids_mu_c=1",
                "K_H_specialization_is_unit_iff_point_avoids_H_and_O=1",
                "p24_producer_must_prove_selected_cm_lang_coordinate_avoids_forbidden_anchor_locus=1",
                "local_unit_criterion_is_finite_algebra_not_the_cm_lang_producer=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_resultant_avoidance_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "scalar_resultant_criterion_rows=6/6",
                "scalar_unit_count_rows=6/6",
                "quotient_component_unit_rows=8/8",
                "quotient_xc_minus_one_resultant_rows=8/8",
                "quotient_bezout_rows=8/8",
                "quotient_combined_criterion_rows=8/8",
                "p24_c_degree=179",
                "p24_forbidden_polynomial_degree=179",
                "p24_kernel_polynomial_degree=89",
                "R_c_unit_iff_X_power_c_minus_one_is_unit_in_selected_algebra=1",
                "resultant_nonzero_equiv_forbidden_locus_avoidance=1",
                "bezout_identity_equiv_resultant_unit_certificate=1",
                "criterion_works_without_adjoining_all_c_roots_of_unity=1",
                "p24_reduced_anchor_can_be_certified_by_one_resultant_or_bezout_punit=1",
                "resultant_avoidance_is_finite_algebra_not_the_cm_lang_producer=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_kernel_generator_invariance_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_generator_invariance_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "actual_generator_invariance_rows=6/6",
                "actual_root_pair_count_rows=6/6",
                "formal_generator_invariance_rows=6/6",
                "formal_root_pair_count_rows=6/6",
                "p24_oriented_one_point_diamond_choices=178",
                "p24_x_coordinate_generator_pairs=89",
                "p24_kernel_polynomial_generator_orbits=1",
                "p24_conditional_kernel_search_cases=2",
                "changing_the_generator_of_H_does_not_change_K_H=1",
                "p24_178_diamond_one_point_choices_collapse_to_one_kernel_polynomial=1",
                "p24_conditional_search_after_kernel_generator_collapse_is_two_signs=1",
                "constructing_the_selected_cm_lang_subgroup_polynomial_remains_the_producer_problem=1",
                "conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_kernel_generator_invariance_gate",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_kernel_final_curve_guardrail",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_final_curve_guardrail.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_c_degree=179",
                "p24_c_divides_selected_group_order=0",
                "p24_c_frobenius_discriminant_legendre=-1",
                "p24_c_frobenius_roots_mod_c=[]",
                "p24_c_final_curve_rational_isogeny_available=0",
                "p24_mu_c_field_degree_over_Fp=89",
                "p24_179_kernel_is_not_rational_torsion_on_final_curve=1",
                "p24_179_kernel_is_not_an_Fp_rational_Velu_isogeny=1",
                "do_not_enumerate_final_curve_179_subgroups_as_the_compressed_search=1",
                "kernel_polynomial_target_must_live_in_auxiliary_cm_lang_or_cyclotomic_layer=1",
                "conclusion=reported_trace_gcd_reduced_anchor_kernel_final_curve_guardrail",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_kernel_section_pairing_guardrail",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_section_pairing_guardrail.py",
            ),
            timeout=10.0,
            must_contain=(
                "actual_toy_parent_sum_unique_rows=2/2",
                "same_sum_ambiguous=1",
                "first_layer_log10_unordered_child_subsets=93.176548",
                "first_layer_log10_expected_same_trace_subsets=69.176548",
                "second_layer_log10_local_child_subsets=616.781509",
                "kernel_generator_invariance_collapses_generators_inside_a_fixed_fiber=1",
                "kernel_generator_invariance_does_not_pair_the_fiber_with_the_selected_section=1",
                "trace_sum_alone_is_not_an_asymptotic_section_selector=1",
                "p24_first_layer_trace_sum_entropy_guardrail=1",
                "selected_auxiliary_kernel_still_needs_section_pairing_or_relative_traces=1",
                "conclusion=reported_trace_gcd_reduced_anchor_kernel_section_pairing_guardrail",
            ),
        ),
        Task(
            label="fixed_frequency_reduced_anchor_low_moment_pairing_window",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_reduced_anchor_low_moment_pairing_window.py",
            ),
            timeout=30.0,
            must_contain=(
                "actual_toy_degree_1_matching_counts=[1, 1]",
                "random_degree_1_matching_count=1820",
                "random_degree_2_matching_count=20",
                "random_degree_3_matching_count=1",
                "first_layer_moments_for_random_unique=4",
                "second_layer_moments_for_random_unique=26",
                "p24_low_moment_pairing_constraints=30",
                "bounded_power_sums_can_act_like_subset_hashes_in_random_controls=1",
                "first_layer_four_moment_window_is_plausible_by_entropy=1",
                "second_layer_twenty_six_moment_window_is_plausible_by_entropy=1",
                "low_moment_window_is_not_a_proof_without_cm_anti_collision=1",
                "constructing_these_selected_moments_remains_a_producer_theorem=1",
                "conclusion=reported_trace_gcd_reduced_anchor_low_moment_pairing_window",
            ),
        ),
        Task(
            label="low_moment_cm_selector_sweep",
            argv=(
                python,
                "p24/trace_gcd_low_moment_cm_selector_sweep.py",
            ),
            timeout=20.0,
            must_contain=(
                "rows=19",
                "rows_all_unique_within_degree_bound=19",
                "rows_unique_at_degree_one=14",
                "rows_unique_no_later_than_random_entropy=16",
                "first_layer_random_unique_moments=4",
                "second_layer_random_unique_moments=26",
                "total_low_moment_pairing_constraints=30",
                "actual_cm_towers_can_be_tested_for_low_moment_child_selection=1",
                "low_moment_collision_behavior_is_a_theorem_microscope_not_a_certificate=1",
                "intrinsic_moment_construction_and_cm_anti_collision_remain_required=1",
                "conclusion=reported_trace_gcd_low_moment_cm_selector_sweep",
            ),
        ),
        Task(
            label="low_moment_sparse_relation_gate",
            argv=(
                python,
                "p24/trace_gcd_low_moment_sparse_relation_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "degree=1 matches=1820 min_reduced_collision_size=2",
                "degree=2 matches=20 min_reduced_collision_size=3",
                "first_layer_union_over_two_parents_log10=-2.522422",
                "second_layer_union_over_314_parents_log10=-4.721562",
                "equal_moment_subsets_are_sparse_signed_moment_curve_relations=1",
                "newton_identities_forbid_reduced_collisions_of_size_at_most_k=1",
                "observed_nontrivial_collisions_respect_the_newton_boundary=1",
                "p24_low_moment_theorem_is_cm_sparse_relation_avoidance=1",
                "p24_union_entropy_still_favors_4_plus_26_moments=1",
                "conclusion=reported_trace_gcd_low_moment_sparse_relation_gate",
            ),
        ),
        Task(
            label="low_moment_relative_trace_gate",
            argv=(
                python,
                "p24/trace_gcd_low_moment_relative_trace_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "full_newton_recovery_rows=2/2",
                "degree_one_low_moment_unique_rows=2/2",
                "moment_parent_interpolation_rows=3/3",
                "p24_first_layer_low_relative_traces=4",
                "p24_second_layer_low_relative_traces=26",
                "p24_selected_path_low_relative_traces=30",
                "p24_parent_field_trace_coefficients=8172",
                "child_power_sums_are_relative_traces_of_quotient_period_powers=1",
                "all_relative_degree_many_traces_recover_child_polynomial_by_newton=1",
                "low_traces_plus_sparse_relation_avoidance_can_replace_full_child_polynomial=1",
                "moment_values_are_parent_field_elements_not_postfit_subset_labels=1",
                "p24_low_moment_constructor_target_is_30_selected_relative_traces=1",
                "conclusion=reported_trace_gcd_low_moment_relative_trace_gate",
            ),
        ),
        Task(
            label="low_moment_function_complexity_gate",
            argv=(
                python,
                "p24/trace_gcd_low_moment_function_complexity_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "p1_parent_identity_rows=25/25",
                "nontrivial_parent_ge3_rows=40",
                "nontrivial_full_interp_rows=100",
                "nontrivial_parent_ge3_low_interp_rows=0",
                "p24_selected_path_nominal_low_moments=30",
                "p24_selected_path_nontrivial_new_low_moments=28",
                "first_relative_trace_power_sum_is_the_parent_period=1",
                "p24_low_moment_payload_has_two_automatic_P1_values=1",
                "higher_relative_trace_moments_do_not_show_a_generic_low_degree_parent_formula=1",
                "producer_must_construct_nontrivial_higher_moments_by_class_field_or_trace_formula=1",
                "conclusion=reported_trace_gcd_low_moment_function_complexity_gate",
            ),
        ),
        Task(
            label="low_moment_automatic_p1_entropy_gate",
            argv=(
                python,
                "p24/trace_gcd_low_moment_automatic_p1_entropy_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "random_control=F_101_20_choose_10 q=101 universe=20 child_size=10 max_degree=3 p1_only=1820 higher_only=17 full_with_p1=1",
                "D=-239_parent3_child5 D=-239",
                "higher_only=4 full_with_p1=1",
                "first_layer_higher_only_target_collision_log10=21.176548",
                "first_layer_with_parent_p1_target_collision_log10=-2.823452",
                "second_layer_higher_only_target_collision_log10=16.781509",
                "second_layer_with_parent_p1_target_collision_log10=-7.218491",
                "automatic_P1_is_not_a_new_producer_value=1",
                "automatic_P1_remains_a_selector_constraint=1",
                "p24_higher_only_entropy_is_not_enough_for_random_unique_selection=1",
                "p24_full_selector_still_uses_30_constraints_but_only_28_new_values=1",
                "conclusion=reported_trace_gcd_low_moment_automatic_p1_entropy_gate",
            ),
        ),
        Task(
            label="low_moment_truncated_polynomial_gate",
            argv=(
                python,
                "p24/trace_gcd_low_moment_truncated_polynomial_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "random_control=F_101_20_choose_10 q=101 universe=20 child_size=10 k=3 newton_match=1 power_matches=1 elementary_matches=1",
                "D=-5000_parent3_child5 D=-5000",
                "newton_match=1 power_matches=1 elementary_matches=1",
                "p24_first_layer_new_coefficients=e2_to_e4_count=3",
                "p24_second_layer_new_coefficients=e2_to_e26_count=25",
                "p24_selected_path_new_coefficients=28",
                "low_power_sums_equivalent_to_truncated_child_polynomial_by_newton=1",
                "first_coefficient_e1_is_the_parent_period=1",
                "p24_low_moment_producer_can_target_28_new_child_polynomial_coefficients=1",
                "selector_still_uses_30_constraints_including_parent_e1=1",
                "conclusion=reported_trace_gcd_low_moment_truncated_polynomial_gate",
            ),
        ),
        Task(
            label="abstract_embedded_pairing_low_bidegree_scan",
            argv=(
                python,
                "p24/abstract_embedded_pairing_low_bidegree_scan.py",
            ),
            timeout=35.0,
            must_contain=(
                "D= -2239 q= 2243 ell= 2 n= 7 orient=1121 dx= 2 dy= 1 support= 6 actual=   0/5040 random_controls_with_found=0/5",
                "D= -2239 q= 2243 ell= 2 n= 7 orient=1123 dx= 1 dy= 2 support= 6 actual=   0/5040 random_controls_with_found=0/5",
                "D= -2239 q= 2243 ell= 2 n= 7 orient=1121 dx= 2 dy= 2 support= 9 actual=5040/5040 random_controls_with_found=5/5",
                "actual_low_support_rows_with_pairing=0",
                "support_le_quotient_size_pairing_would_be_non_generic_phase_evidence=1",
                "abstract_quotient_coordinate_did_not_show_low_support_pairing_if_actual_low_support_rows_with_pairing_is_zero=1",
                "conclusion=reported_abstract_embedded_pairing_low_bidegree_scan",
            ),
        ),
        Task(
            label="p24_compressed_search_readiness",
            argv=(
                python,
                "p24/trace_gcd_p24_compressed_search_readiness.py",
            ),
            timeout=10.0,
            must_contain=(
                "p_mod_8=7",
                "danger_k=40",
                "selected_trace=-1178414874616",
                "selected_order_odd_part=454747350887",
                "x16_p23_sampler_available_for_p24=0",
                "p24_symbolic_right_mixed_pairs=189036",
                "p24_admissible_jacobi_rank=621",
                "p24_broad_jacobi_rank=625",
                "p24_diamond_orbit_size=178",
                "p24_oriented_one_point_diamond_choices=178",
                "p24_x_coordinate_generator_pairs=89",
                "p24_kernel_polynomial_generator_orbits=1",
                "p24_diamond_norm_matches_cyclotomic_residual=1",
                "p24_kummer_selected_e_values=[1]",
                "p24_h_coset_equations=1092",
                "p24_compressed_independent_equations=48",
                "p24_low_moment_pairing_constraints=30",
                "conditional_punit_payload_field_elements=4",
                "selected_chain_slots=3107811",
                "compressed_surface_ready_if_selected_cm_lang_factor_is_supplied=1",
                "p24_178_diamond_one_point_choices_collapse_to_one_kernel_polynomial=1",
                "p24_conditional_search_after_kernel_generator_collapse_is_two_signs=1",
                "p24_kernel_polynomial_target_is_auxiliary_not_final_curve_179_isogeny=1",
                "low_moment_selector_hypothesis_is_now_testable_on_controls=1",
                "low_moment_constraints_are_not_a_producer_without_intrinsic_moments=1",
                "without_that_factor_there_is_no_honest_compressed_root_search_to_run=1",
                "conclusion=compressed_search_surface_ready_but_producer_missing",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_projector_internal_character_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-5000",
                "q=3851",
                "class_number=30",
                "top_quotient=2",
                "toy_C_degree=5",
                "toy_B_over_C_degree=3",
                "origins_checked=30",
                "projected_B_over_C_trace_nonzeroes=30/30",
                "projected_final_trace_zeroes=0/30",
                "projected_final_trace_nonzeroes=30/30",
                "raw_top_final_trace_zeroes=0/60",
                "nontrivial_top_projector_does_not_force_internal_trace_zero=1",
                "actual_cm_projector_channel_can_have_trivial_C_component=1",
                "p24_needs_specific_weighted_G_chi_packet_not_generic_projector=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_right_combo_internal_trace_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_right_combo_internal_trace_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "internal_q_order=2",
                "right_combo_orbit_count=2",
                "right_combo_terms_all_nonzero=2/2",
                "right_combo_internal_trace_zeroes=0/2",
                "actual_cm_right_combo_internal_trace_zeroes_are_not_generic=1",
                "p24_needs_specific_211_axis_H_coset_equality_after_internal_trace=1",
                "right_combo_shape_alone_does_not_prove_trace_zero=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_internal_trace_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_right_combo_anchor_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "recombined_q_order=4",
                "recombined_nontrivial_quotient_equations=0",
                "recombined_anchor_equations=1",
                "anchor_balance_holds=0",
                "anchor_defect_nonzero=1",
                "weighted_polynomial_recombined_trace_zero=0",
                "right_combo_recombined_trace_zero=0",
                "small_actual_cm_recombined_balance_is_anchor_only=1",
                "actual_cm_right_combo_anchor_balance_is_not_generic=1",
                "p24_anchor_needs_specific_weighted_G_chi_or_explicit_potential=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_right_combo_anchor_section_scan",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_section_scan.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "h=140",
                "m=28",
                "n=5",
                "origin_sections_checked=140",
                "anchor_zero_sections=0/140",
                "anchor_nonzero_sections=140/140",
                "actual_cm_right_combo_anchor_not_rescued_by_origin_section=1",
                "selected_section_choice_alone_does_not_prove_anchor_balance=1",
                "p24_anchor_still_needs_specific_weighted_G_chi_or_explicit_potential=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_section_scan",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_product_internal_trace_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_product_internal_trace_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "D=-13319",
                "q=13463",
                "m=28",
                "n=5",
                "internal_q_order=2",
                "product_internal_orbit_count=2",
                "product_terms_all_nonzero=2/2",
                "product_internal_trace_zeroes=0/2",
                "recombined_q_order=4",
                "recombined_product_orbit_count=1",
                "recombined_product_trace_zeroes=0/1",
                "product_full_projection_zero=0",
                "actual_cm_weighted_product_internal_trace_zeroes_are_not_generic=1",
                "actual_cm_weighted_product_recombined_trace_zeroes_are_not_generic=1",
                "product_packet_shape_alone_does_not_prove_trace_zero=1",
                "p24_needs_specific_weighted_G_chi_packet_or_explicit_potential=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_product_internal_trace_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_actual_cm_admissible_jacobi_span_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary.py",
            ),
            timeout=150.0,
            must_contain=(
                "projector_row",
                "no_forbidden_projected_origins=0/30",
                "admissible_span_origins=0/30",
                "broad_span_origins=0/30",
                "right_combo_row",
                "profile=right_combo_resolvent",
                "profile=weighted_coefficients",
                "profile=selected_defect_coefficients",
                "no_forbidden_projected_origins=0/140",
                "admissible_span_origins=0/140",
                "broad_span_origins=0/140",
                "actual_cm_projector_packets_are_not_generically_admissible_jacobi=1",
                "actual_cm_right_combo_packets_are_not_generically_admissible_jacobi=1",
                "actual_cm_weighted_coefficient_packets_are_not_generically_admissible_jacobi=1",
                "actual_cm_selected_defect_packets_are_not_generically_admissible_jacobi=1",
                "p24_still_needs_selected_weighted_packet_or_explicit_cm_lang_decomposition=1",
                "conclusion=reported_trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary",
            ),
        ),
        Task(
            label="lean_trace_gcd_product_coboundary_gate",
            argv=("lean", "p24/lean/TraceGcdProductCoboundaryGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_projector_trace_pipeline_gate",
            argv=("lean", "p24/lean/TraceGcdProjectorTracePipelineGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_c_bidegree_support_gate",
            argv=("lean", "p24/lean/TraceGcdRightCBidegreeSupportGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_admissible_jacobi_decomposition_gate",
            argv=("lean", "p24/lean/TraceGcdAdmissibleJacobiDecompositionGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_admissible_jacobi_dual_conditions_gate",
            argv=("lean", "p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_dual_conditions_value_side_gate",
            argv=("lean", "p24/lean/TraceGcdDualConditionsValueSideGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_recombined_mixed_spectrum_gate",
            argv=("lean", "p24/lean/TraceGcdRecombinedMixedSpectrumGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_affine_profile_gate",
            argv=("lean", "p24/lean/TraceGcdAffineProfileGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_difference_gate",
            argv=("lean", "p24/lean/TraceGcdRightDifferenceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_difference_trace_gate",
            argv=("lean", "p24/lean/TraceGcdRightDifferenceTraceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_difference_covariance_telescope_gate",
            argv=("lean", "p24/lean/TraceGcdRightDifferenceCovarianceTelescopeGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_right_difference_trace_covariance_functorial_gate",
            argv=("lean", "p24/lean/TraceGcdRightDifferenceTraceCovarianceFunctorialGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_adjacent_anchor_descent_gate",
            argv=("lean", "p24/lean/TraceGcdAdjacentAnchorDescentGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_adjacent_anchor_cyclic_divisibility_gate",
            argv=("lean", "p24/lean/TraceGcdAdjacentAnchorCyclicDivisibilityGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_adjacent_difference_operator_gate",
            argv=("lean", "p24/lean/TraceGcdAdjacentDifferenceOperatorGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_adjacent_bridge_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorAdjacentBridgeGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_slice_decomposition_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorSliceDecompositionGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_cyclotomic_divisor_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorCyclotomicDivisorGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_diamond_norm_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorDiamondNormGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_cyclic_vs_diamond_norm_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorCyclicVsDiamondNormGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_elliptic_subgroup_divisor_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorEllipticSubgroupDivisorGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_kernel_polynomial_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorKernelPolynomialGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_local_unit_criterion_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorLocalUnitCriterionGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_resultant_avoidance_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorResultantAvoidanceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_kernel_generator_invariance_gate",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorKernelGeneratorInvarianceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_kernel_final_curve_guardrail",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorKernelFinalCurveGuardrail.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_kernel_section_pairing_guardrail",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorKernelSectionPairingGuardrail.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_reduced_anchor_low_moment_pairing_window",
            argv=("lean", "p24/lean/TraceGcdReducedAnchorLowMomentPairingWindow.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_low_moment_sparse_relation_gate",
            argv=("lean", "p24/lean/TraceGcdLowMomentSparseRelationGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_low_moment_relative_trace_gate",
            argv=("lean", "p24/lean/TraceGcdLowMomentRelativeTraceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_low_moment_automatic_p1_gate",
            argv=("lean", "p24/lean/TraceGcdLowMomentAutomaticP1Gate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_low_moment_truncated_polynomial_gate",
            argv=("lean", "p24/lean/TraceGcdLowMomentTruncatedPolynomialGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_anchor_kummer_descent_gate",
            argv=("lean", "p24/lean/TraceGcdAnchorKummerDescentGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_prerecombination_covariance_gate",
            argv=("lean", "p24/lean/TraceGcdPreRecombinationCovarianceGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="lean_trace_gcd_paired_kernel_criterion_gate",
            argv=("lean", "p24/lean/TraceGcdPairedKernelCriterionGate.lean"),
            timeout=10.0,
        ),
        Task(
            label="fixed_frequency_p24_twisted_hilbert90_payload_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_factor_cycle_count=10",
                "rho_factor_cycle_length=7",
                "twisted_trace_ranks=[1, 1, 1, 1, 1, 1]",
                "twisted_coboundary_ranks=[6, 6, 6, 6, 6, 6]",
                "twisted_hilbert90_image_equals_trace_kernel=1",
                "p24_payload_can_be_stated_as_factor_cycle_coboundary=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate",
            ),
        ),
        Task(
            label="fixed_frequency_p24_gauss_normalization_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_gauss_normalization_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_h_raw_log_shift=6",
                "rho_h_orbit_position_shift=3",
                "additive_resolvent_eigen_mismatches=0",
                "gauss_sum_eigen_mismatches=0",
                "normalized_projection_fixed_mismatches=0",
                "random_normalized_projection_nonzero=96/96",
                "ordinary_centered_normalized_projection_nonzero=96/96",
                "p24_idempotent_covariance_must_be_gauss_normalized_extra_identity=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_gauss_normalization_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_idempotent_covariance_circularity_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_order_on_E=7",
                "rho_factor_step_mod_70=10",
                "descended_eigenvalue1_failures=0",
                "random_descended_nonzero=24/24",
                "random_descended_fail_nontrivial_covariance=24/24",
                "nontrivial_idempotent_covariance_is_equivalent_to_vanishing_after_descent=1",
                "noncircular_proof_must_establish_covariance_on_trace_terms_before_recombination=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_normalized_covariance_obstruction_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "rho_mod_157=1",
                "rho_right_log_mod7=6",
                "raw_right_lambda_exponents=[6, 5, 4, 3, 2, 1]",
                "gauss_sum_lambda_exponents=[6, 5, 4, 3, 2, 1]",
                "normalized_right_exponents=[0, 0, 0, 0, 0, 0]",
                "normalized_product_exponents=[0, 0, 0, 0, 0, 0]",
                "nontrivial_normalized_covariance_failures=6/6",
                "nontrivial_plus_trivial_covariance_forces_zero_checks=6/6",
                "gauss_normalized_product_covariance_is_trivial_under_factor_shift=1",
                "proof_target_should_be_internal_trace_or_right_coboundary_not_normalized_covariance=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate",
            ),
        ),
        Task(
            label="fixed_frequency_relation_shape_index_limited",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_relation_shape_index.py",
                "--max-discriminants",
                "250",
                "--max-abs-D",
                "80000",
                "--q-stop",
                "50000",
                "--max-q-tests-per-D",
                "12",
                "--min-h",
                "100",
                "--max-h",
                "30000",
                "--max-component",
                "300",
                "--max-left-len",
                "120",
                "--max-rows",
                "8",
            ),
            timeout=20.0,
            must_contain=(
                "hits=0",
                "right_component_cases=0",
                "hit_has_non_tail_only_prefix_tail_shape=0",
                "conclusion=reported_trace_gcd_fixed_frequency_relation_shape_index",
            ),
        ),
        Task(
            label="fixed_frequency_packet_inversion_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_packet_inversion_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "inversion_even_nonzero_sums=16/16",
                "paired_multiplier_product_plus_one_nonzero_sums=16/16",
                "anti_inversion_nonzero_sums=0/16",
                "termwise_right_zero_nonzero_sums=0/16",
                "packet_inversion_symmetry_pairs_terms_but_does_not_cancel_them=1",
                "p24_packet_cancellation_needs_more_than_hermitian_packet_stability=1",
                "conclusion=reported_trace_gcd_fixed_frequency_packet_inversion_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_order7_h_coboundary_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_h_coboundary_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "h_coboundary_implies_order7_augmentation=1",
                "order7_augmentation_equivalent_to_h_coboundary_potential=1",
                "ordinary_centering_is_not_an_h_coboundary_condition=1",
                "p24_sufficient_theorem_is_explicit_H_potential_for_right_profile=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_h_coboundary_toy",
            ),
        ),
        Task(
            label="fixed_frequency_order7_h_bezout_operator_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_h_bezout_operator_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "universal_operator_satisfies_one_minus_T_times_U_equals_one_minus_eH=1",
                "h_trace_zero_gives_deterministic_potential_Y_equals_U_G=1",
                "p24_remaining_arithmetic_theorem_is_eH_G_equals_zero=1",
                "no_sampling_needed_once_h_coset_sums_vanish=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_h_bezout_operator_toy",
            ),
        ),
        Task(
            label="fixed_frequency_order7_paired_potential_boundary_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_paired_potential_boundary_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "right_resolvent_coboundary_implies_profile_coboundary=1",
                "paired_profile_coboundary_does_not_imply_right_resolvent_coboundary=1",
                "full_right_resolvent_potential_is_sufficient_but_stronger_than_needed=1",
                "p24_needed_theorem_is_paired_L_potential_not_full_B_potential=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_paired_potential_boundary_toy",
            ),
        ),
        Task(
            label="fixed_frequency_h_coboundary_basefield_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_h_coboundary_basefield_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "ordinary_centering_has_h_coset_leak=1",
                "forced_h_trace_zero_all_zero=1",
                "h_trace_zero_reconstructs_rowwise_coboundary=1",
                "h_coset_sum_zero_entries=0/6",
                "actual_cm_analogue_refutes_generic_h_coboundary=1",
                "conclusion=reported_trace_gcd_fixed_frequency_h_coboundary_basefield_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_p24_h_coset_sum_verifier",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_h_coset_sum_verifier.py",
            ),
            timeout=10.0,
            must_contain=(
                "p24_scalar_equations=1092",
                "sqrt_floor_div_scalar_equations=915750915",
                "forced_h_coset_zero_accepted=1",
                "corrupted_marginal_rejected=1",
                "verifier_does_not_compute_cm_class_set=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_h_coset_sum_verifier",
            ),
        ),
        Task(
            label="fixed_frequency_p24_character_payload_contract",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_p24_character_payload_contract.py",
            ),
            timeout=10.0,
            must_contain=(
                "character_matrix_rank=7",
                "nontrivial_plus_center_rank=7",
                "six_nontrivial_L_equations_scalar_count=936",
                "p24_scalar_equations=1092",
                "ordinary_centering_plus_six_character_sums_equiv_h_coset_zero=1",
                "full_marginal_materialization_is_not_a_subsqrt_certificate=1",
                "conclusion=reported_trace_gcd_fixed_frequency_p24_character_payload_contract",
            ),
        ),
        Task(
            label="fixed_frequency_h_kernel_inclusion_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_h_kernel_inclusion_gate.py",
            ),
            timeout=10.0,
            must_contain=(
                "h_indicator_rank=7",
                "h_orthogonal_random_matrix_rank=156",
                "centered_control_h_leak_rank=6",
                "h_kernel_inclusion_is_compatible_with_full_156_rank=1",
                "p156_multiplier_invariance_would_imply_h_kernel_inclusion=1",
                "conclusion=reported_trace_gcd_fixed_frequency_h_kernel_inclusion_gate",
            ),
        ),
        Task(
            label="fixed_frequency_left_descent_marginal_gate",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_left_descent_marginal_gate.py",
            ),
            timeout=20.0,
            must_contain=(
                "random_equivalence_failures=0",
                "forced_left_descent_passes=24/24",
                "forced_centered_H_kernel_passes=24/24",
                "D=-13319",
                "q=13463",
                "h=140",
                "m=28",
                "n=5",
                "actual_centered_H_sum_zeroes=0/6",
                "actual_left_descent_failures=6/6",
                "actual_equivalence_failures=0",
                "centered_H_kernel_equiv_left_descent_of_period_leakage=1",
                "left_descent_is_geometric_form_of_CPH_zero=1",
                "actual_cm_marginal_refutes_generic_left_descent=1",
                "p24_must_prove_left_descent_for_trace_gcd_weighted_packet=1",
                "conclusion=reported_trace_gcd_fixed_frequency_left_descent_marginal_gate",
            ),
        ),
        Task(
            label="fixed_frequency_h_coset_selector_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_h_coset_selector_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "h_constraints_extra_rank_over_centering=6",
                "quotient_character_nonzero_additive_supports=[210, 210, 210, 210, 210, 210]",
                "nontrivial_quotient_characters_have_full_nonzero_additive_support=1",
                "h_coboundary_is_not_a_sparse_right_frequency_shortcut=1",
                "conclusion=reported_trace_gcd_fixed_frequency_h_coset_selector_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_order7_rank_compatibility_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_rank_compatibility_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "augmentation_extra_rank_over_centering=6",
                "augmentation_rank_margin=47",
                "order7_augmentation_is_compatible_with_156_rank_fixed_square=1",
                "full_rank_and_unit2_transport_do_not_prove_order7_augmentation=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_rank_compatibility_toy",
            ),
        ),
        Task(
            label="fixed_frequency_unit_symmetry_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_unit_symmetry_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "synthetic_multiplier_invariance_failures=0",
                "actual_multiplier_invariance_failures=18",
                "actual_projection_nonzero=1",
                "actual_cm_packet_refutes_generic_multiplier_invariance=1",
                "right_unit_action_is_not_a_free_class_torsor_automorphism=1",
                "conclusion=reported_trace_gcd_fixed_frequency_unit_symmetry_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_symmetry_boundary",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_symmetry_boundary.py",
            ),
            timeout=10.0,
            must_contain=(
                "orbit_containing_minus_one_is_the_omitted_full_block=1",
                "centering_plus_sign_symmetry_forces_only_trivial_fixed_frequency=1",
                "nontrivial_order7_fixed_frequencies_need_extra_cm_lang_arithmetic=1",
                "easy_right_orbit_symmetry_is_not_the_missing_cyclic_syzygy=1",
                "conclusion=reported_trace_gcd_fixed_frequency_symmetry_boundary",
            ),
        ),
        Task(
            label="fixed_frequency_order7_augmentation_toy",
            argv=(
                python,
                "p24/trace_gcd_fixed_frequency_order7_augmentation_toy.py",
            ),
            timeout=10.0,
            must_contain=(
                "order7_augmentation_plus_negation_gives_explicit_syzygy=1",
                "one_plus_yminus2_is_unit_in_R7=1",
                "centering_only_does_not_control_nontrivial_order7=1",
                "augmentation_without_negation_covariance_does_not_give_formula=1",
                "p24_next_theorem_can_be_order7_augmentation_vanishing=1",
                "conclusion=reported_trace_gcd_fixed_frequency_order7_augmentation_toy",
            ),
        ),
        Task(
            label="lean_trace_gcd_fixed_frequency_order7_gate",
            argv=("lean", "p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean"),
            timeout=10.0,
        ),
        Task(
            label="actual_cm_full_plucker_chart_boundary",
            argv=(
                python,
                "p24/trace_gcd_actual_cm_full_plucker_chart_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "actual_cm_full_plucker_chart_columns_measured=1",
                "actual_cm_full_chart_has_no_nontrivial_basis_calibration_row=1",
                "p24_full_chart_requires_selected_basis_of_ambient=1",
                "current_small_actual_rows_do_not_test_visible_scalar_grs_chart=1",
                "conclusion=reported_trace_gcd_actual_cm_full_plucker_chart_boundary",
            ),
        ),
        Task(
            label="actual_cm_frequency_defect_boundary",
            argv=(
                python,
                "p24/trace_gcd_actual_cm_frequency_defect_boundary.py",
            ),
            timeout=20.0,
            must_contain=(
                "actual_cm_frequency_profile_columns_measured=1",
                "tail_only_rows_are_not_frequency_defect_calibrations=1",
                "prefix_plus_tail_singular_rows_fail_local_frequency_gate=1",
                "p24_frequency_defect_punit_theorem_still_needs_new_arithmetic=1",
                "conclusion=reported_trace_gcd_actual_cm_frequency_defect_boundary",
            ),
        ),
        Task(
            label="actual_cm_basis_free_section_audit",
            argv=(
                python,
                "p24/trace_gcd_actual_cm_basis_free_section_audit.py",
            ),
            timeout=20.0,
            must_contain=(
                "rank_profile_frobenius_covariant_rows=10/10",
                "basis_free_section_candidate_rows=0/10",
                "prefix_tail_wrong_defect_size_rows=4/4",
                "current_actual_rows_do_not_supply_basis_free_section_candidate=1",
                "obstruction_is_defect_support_size_not_descent=1",
                "conclusion=reported_trace_gcd_actual_cm_basis_free_section_audit",
            ),
        ),
        Task(
            label="rs_tail_visible_lrs_signature_toy",
            argv=(python, "p24/trace_gcd_rs_tail_visible_lrs_signature_toy.py"),
            timeout=10.0,
            must_contain=(
                "synthetic_visible_grs_signature_detected=1",
                "random_rs_tail_visible_grs_signature_rejected=1",
                "hidden_lrs_route_needs_nontrivial_punit_block_equivalence=1",
                "p24_erasure_columns=54",
                "conclusion=reported_trace_gcd_rs_tail_visible_lrs_signature_toy",
            ),
        ),
        Task(
            label="residual_prefix_tail_bridge_audit",
            argv=(python, "p24/trace_gcd_residual_prefix_tail_bridge_audit.py"),
            timeout=20.0,
            must_contain=(
                "product_mismatches=0",
                "event_mismatches=0",
                "prefix_failure_controls=1",
                "tail_failure_controls=1",
                "full_residual_product_factors_as_prefix_times_tail=1",
                "conclusion=reported_trace_gcd_residual_prefix_tail_bridge_audit",
            ),
        ),
        Task(
            label="residual_moore_chow_toy",
            argv=(python, "p24/trace_gcd_residual_moore_chow_toy.py"),
            timeout=10.0,
            must_contain=(
                "full_residual_mismatches=0",
                "full_chow_mismatches=0",
                "norm_chow_mismatches=0",
                "tail_image_mismatches=0",
                "forced_prefix_zero=1",
                "forced_tail_zero=1",
                "full_moore_equals_basis_unit_times_chow_coordinate_det=1",
                "tail_residual_product_equals_moore_of_prefix_annihilator_images=1",
                "conclusion=reported_trace_gcd_residual_moore_chow_toy",
            ),
        ),
        Task(
            label="residual_schur_complement_toy",
            argv=(python, "p24/trace_gcd_residual_schur_complement_toy.py"),
            timeout=10.0,
            must_contain=(
                "determinant_mismatches=0",
                "prefix_zero_mismatches=0",
                "tail_zero_mismatches=0",
                "full_zero_mismatches=0",
                "forced_prefix_no_pivot=1",
                "forced_tail_schur_zero=1",
                "tail_quotient_moore_nonzero_iff_schur_complement_nonzero=1",
                "conclusion=reported_trace_gcd_residual_schur_complement_toy",
            ),
        ),
        Task(
            label="prefix_adjoint_trace_toy",
            argv=(python, "p24/trace_gcd_prefix_adjoint_trace_toy.py"),
            timeout=10.0,
            must_contain=(
                "prefix_adjoint_rank_mismatches=0",
                "surjective_adjoint_event_mismatches=0",
                "pairing_mismatches=0",
                "found_positive_kernel_surjective=1",
                "forced_dependent_not_surjective=1",
                "conclusion=reported_trace_gcd_prefix_adjoint_trace_toy",
            ),
        ),
        Task(
            label="prefix_hilbert90_toy",
            argv=(python, "p24/trace_gcd_prefix_hilbert90_toy.py"),
            timeout=10.0,
            must_contain=(
                "hilbert90_match_failures=0",
                "trace_nonintersection_event_mismatches=0",
                "found_hilbert90_nonintersection=1",
                "forced_coboundary_intersection_detected=1",
                "forced_period_dependence_detected=1",
                "conclusion=reported_trace_gcd_prefix_hilbert90_toy",
            ),
        ),
        Task(
            label="full_coinvariant_tail_toy",
            argv=(python, "p24/trace_gcd_full_coinvariant_tail_toy.py"),
            timeout=10.0,
            must_contain=(
                "duality_mismatches=0",
                "coinvariant_mismatches=0",
                "found_full_coinvariant_unit=1",
                "forced_tail_inside_prefix_span_detected=1",
                "full_prefix_tail_trace_gcd_injective_iff_square_coinvariant_unit=1",
                "conclusion=reported_trace_gcd_full_coinvariant_tail_toy",
            ),
        ),
        Task(
            label="crossed_coinvariant_norm_toy",
            argv=(python, "p24/trace_gcd_crossed_coinvariant_norm_toy.py"),
            timeout=10.0,
            must_contain=(
                "determinant_mismatches=0",
                "zero_detection_failures=0",
                "full_rank_detection_failures=0",
                "found_all_full_coinvariant_cycle=1",
                "forced_singular_coinvariant_cycle_detected=1",
                "crossed_norm_of_square_coinvariant_maps_detects_any_local_singularity=1",
                "conclusion=reported_trace_gcd_crossed_coinvariant_norm_toy",
            ),
        ),
        Task(
            label="prefix_normal_basis_toy",
            argv=(python, "p24/trace_gcd_prefix_normal_basis_toy.py"),
            timeout=10.0,
            must_contain=(
                "dual_pairing_failures=0",
                "dual_reconstruction_failures=0",
                "basis_rank_mismatches=0",
                "found_normal_coefficient_independent=1",
                "forced_repeated_coefficient_dependence=1",
                "conclusion=reported_trace_gcd_prefix_normal_basis_toy",
            ),
        ),
        Task(
            label="prefix_gaussian_normal_basis_toy",
            argv=(python, "p24/trace_gcd_prefix_gaussian_normal_basis_toy.py"),
            timeout=10.0,
            must_contain=(
                "gaussian_period_rank=3",
                "frobenius_cycle_failures=0",
                "dual_pairing_failures=0",
                "dual_reconstruction_failures=0",
                "basis_rank_mismatches=0",
                "found_gaussian_coefficient_independent=1",
                "p24_ord_211_p=35",
                "p24_gaussian_type=6",
                "p24_coset_cover_size=210",
                "p24_right_field_has_type6_gaussian_normal_basis=1",
                "conclusion=reported_trace_gcd_prefix_gaussian_normal_basis_toy",
            ),
        ),
        Task(
            label="prefix_gaussian_dft_boundary_toy",
            argv=(python, "p24/trace_gcd_prefix_gaussian_dft_boundary_toy.py"),
            timeout=10.0,
            must_contain=(
                "original_collapsed_fp_rank=1",
                "dft_collapsed_fp_rank=2",
                "original_tensor_k_rank=1",
                "dft_tensor_k_rank=1",
                "collapsed_extension_coefficient_dft_can_change_base_rank=1",
                "tensor_product_dft_preserves_scalar_extended_rank=1",
                "p24_gaussian_dft_must_stay_in_L_tensor_K=1",
                "conclusion=reported_trace_gcd_prefix_gaussian_dft_boundary_toy",
            ),
        ),
        Task(
            label="prefix_unit_scaling_pitfall_toy",
            argv=(python, "p24/trace_gcd_prefix_unit_scaling_pitfall_toy.py"),
            timeout=10.0,
            must_contain=(
                "original_fp_rank=2",
                "target_unit_scaled_fp_rank=1",
                "base_scalar_scaled_fp_rank=2",
                "target_unit_column_scaling_can_change_base_rank=1",
                "base_scalar_column_scaling_preserves_base_rank=1",
                "gaussian_Ga_units_are_not_individually_divisible_for_full_rank=1",
                "conclusion=reported_trace_gcd_prefix_unit_scaling_pitfall_toy",
            ),
        ),
        Task(
            label="prefix_tensor_component_rank_toy",
            argv=(python, "p24/trace_gcd_prefix_tensor_component_rank_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=transverse_kernels component_ranks=[1, 1]",
                "case=aligned_kernels component_ranks=[1, 1]",
                "same_component_rank_profile_different_global_rank=1",
                "global_full_rank_iff_component_kernel_intersection_zero=1",
                "p24_prefix_tensor_components_require_kernel_transversality=1",
                "conclusion=reported_trace_gcd_prefix_tensor_component_rank_toy",
            ),
        ),
        Task(
            label="prefix_component_frobenius_toy",
            argv=(python, "p24/trace_gcd_prefix_component_frobenius_toy.py"),
            timeout=10.0,
            must_contain=(
                "component_mismatches=0",
                "relation_reindex_mismatches=0",
                "p24_p_mod_35=22",
                "p24_ord_35_p=4",
                "component_r_sees_frequency_p_power_r_times_a=1",
                "relation_coefficients_conjugate_with_component=1",
                "p24_frequency_orbits_bookkeep_components_not_blocks=1",
                "conclusion=reported_trace_gcd_prefix_component_frobenius_toy",
            ),
        ),
        Task(
            label="prefix_semilinear_core_toy",
            argv=(python, "p24/trace_gcd_prefix_semilinear_core_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=random_good",
                "global_kernel_equals_semilinear_core=1",
                "case=forced_fixed_frequency_core",
                "p24_semilinear_T_order=4",
                "p24_first_component_kernel_dim_lower_bound=101",
                "global_relation_iff_T_orbit_stays_in_first_component_kernel=1",
                "first_component_kernel_large_but_semilinear_core_must_be_zero=1",
                "forced_fixed_frequency_core_detected=1",
                "conclusion=reported_trace_gcd_prefix_semilinear_core_toy",
            ),
        ),
        Task(
            label="prefix_semilinear_descent_toy",
            argv=(python, "p24/trace_gcd_prefix_semilinear_descent_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=random_good",
                "case=forced_fixed_frequency_core",
                "semilinear_descent_core_kdim_equals_fixed_kernel_fpdim=1",
                "zero_core_iff_no_nonzero_T_fixed_relation=1",
                "p24_fixed_frequency_variables=28",
                "p24_length4_K_variables=28",
                "p24_fixed_source_fp_dimension=140",
                "p24_fixed_relation_shape_Fp28_plus_K28_to_L=1",
                "conclusion=reported_trace_gcd_prefix_semilinear_descent_toy",
            ),
        ),
        Task(
            label="prefix_semilinear_fixed_adjoint_toy",
            argv=(python, "p24/trace_gcd_prefix_semilinear_fixed_adjoint_toy.py"),
            timeout=20.0,
            must_contain=(
                "pairing_mismatches=0",
                "case=random_good",
                "case=forced_fixed_frequency_relation",
                "primal_rank=6",
                "adjoint_rank=6",
                "primal_rank=5",
                "adjoint_rank=5",
                "fixed_adjoint_pairing_formula_verified=1",
                "fixed_relation_injective_iff_adjoint_syndrome_surjective=1",
                "p24_syndrome_shape_Fp28_plus_K28=1",
                "conclusion=reported_trace_gcd_prefix_semilinear_fixed_adjoint_toy",
            ),
        ),
        Task(
            label="prefix_syndrome_moore_toy",
            argv=(python, "p24/trace_gcd_prefix_syndrome_moore_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=random_good",
                "coordinate_rank=6",
                "trace_matrix_rank=6",
                "residual_product_zero=0",
                "case=forced_fixed_frequency_relation",
                "coordinate_rank=5",
                "trace_matrix_rank=5",
                "residual_product_zero=1",
                "syndrome_coordinate_elements_represent_fixed_adjoint=1",
                "trace_pairing_rank_equals_coordinate_span_rank=1",
                "syndrome_moore_residual_nonzero_iff_full_rank=1",
                "conclusion=reported_trace_gcd_prefix_syndrome_moore_toy",
            ),
        ),
        Task(
            label="prefix_syndrome_resultant_bridge_toy",
            argv=(python, "p24/trace_gcd_prefix_syndrome_resultant_bridge_toy.py"),
            timeout=10.0,
            must_contain=(
                "case=good_prefix_good_tail",
                "prefix_surjective=1",
                "tail_injective_on_kernel=1",
                "full_residual_nonzero=1",
                "case=dependent_prefix",
                "prefix_surjective=0",
                "case=good_prefix_bad_tail",
                "tail_injective_on_kernel=0",
                "case=good_prefix_one_tail_direction",
                "tail_rank_on_kernel=1",
                "prefix_syndrome_surjective_gives_kernel_dim_16=1",
                "tail_resultant_nonzero_iff_tail_injective_on_kernel=1",
                "full_140_plus_16_residual_nonzero_iff_prefix_and_tail=1",
                "conclusion=reported_trace_gcd_prefix_syndrome_resultant_bridge_toy",
            ),
        ),
        Task(
            label="actual_cm_orbit_norm_miner_pinned",
            argv=(python, "p24/trace_gcd_actual_cm_orbit_norm_miner.py"),
            timeout=30.0,
            must_contain=(
                "profile=pinned",
                "matrix_rows=1",
                "zero_or_bad_orbits=0",
                "conclusion=reported_trace_gcd_actual_cm_orbit_norm_miner",
            ),
        ),
        Task(
            label="block_cycle_fitting_zero_detection_toy",
            argv=(
                python,
                "p24/block_cycle_fitting_zero_detection_toy.py",
                "--trials",
                "100",
            ),
            timeout=10.0,
            must_contain=(
                "p24_sign_positive=1",
                "determinant_mismatches=0",
                "zero_detection_failures=0",
                "full_rank_iff_failures=0",
                "conclusion=reported_block_cycle_fitting_zero_detection_toy",
            ),
        ),
        Task(
            label="block_cycle_determinant_line_invariance",
            argv=(
                python,
                "p24/block_cycle_determinant_line_invariance_toy.py",
                "--trials",
                "100",
            ),
            timeout=10.0,
            must_contain=(
                "scale_failures=0",
                "zero_mismatches=0",
                "basis_changes_scale_block_cycle_by_units=1",
            ),
        ),
        Task(
            label="diamond_equivariance_toy",
            argv=(
                python,
                "p24/trace_gcd_diamond_equivariance_toy.py",
                "--trials",
                "100",
            ),
            timeout=10.0,
            must_contain=(
                "punit_edges=600/600",
                "determinant_mismatches=0",
                "singular_zero_mismatches=0",
                "conclusion=reported_trace_gcd_diamond_equivariance_toy",
            ),
        ),
        Task(
            label="norm_triangle_q337_right7_k2",
            argv=(
                python,
                "p24/trace_gcd_norm_triangle_toy.py",
                "--q",
                "337",
                "--right",
                "7",
                "--multiplier",
                "2",
                "--k",
                "2",
            ),
            timeout=10.0,
            must_contain=(
                "value_mismatches=0",
                "product_equals_signed_block_cycle=1",
                "product_equals_exterior_norm=1",
            ),
        ),
        Task(
            label="norm_triangle_q2113_right11_k3",
            argv=(
                python,
                "p24/trace_gcd_norm_triangle_toy.py",
                "--q",
                "2113",
                "--right",
                "11",
                "--multiplier",
                "3",
                "--k",
                "3",
            ),
            timeout=10.0,
            must_contain=(
                "value_mismatches=0",
                "product_equals_signed_block_cycle=1",
                "product_equals_exterior_norm=1",
            ),
        ),
    ]
    if include_spectral:
        tasks.append(
            Task(
                label="pinned_actual_cm_spectral_row_D13319",
                argv=(
                    python,
                    "p24/lang_trace_gcd_spectral_scan.py",
                    "--only-D",
                    "-13319",
                    "--only-q",
                    "13463",
                    "--q-start",
                    "13463",
                    "--q-stop",
                    "13464",
                    "--only-m",
                    "28",
                    "--only-left",
                    "4",
                    "--only-right",
                    "7",
                    "--include-linear",
                    "--max-factor-degree",
                    "8",
                    "--max-extension-degree",
                    "8",
                    "--min-left-orbit-len",
                    "2",
                    "--require-square-tail",
                    "--require-prime-right",
                    "--min-tail-len",
                    "1",
                    "--max-rows",
                    "8",
                ),
                timeout=60.0,
                must_contain=("zeros=0", "single_orbit=1"),
            )
        )
    if include_actual_cm_triangle:
        tasks.append(
            Task(
                label="actual_cm_norm_triangle_D13319",
                argv=(python, "p24/trace_gcd_actual_cm_norm_triangle_audit.py"),
                timeout=45.0,
                must_contain=(
                    "product_equals_signed_block_cycle=1",
                    "product_equals_split_norm=1",
                    "failures=0",
                ),
            )
        )
    if include_actual_cm_unit_action:
        tasks.append(
            Task(
                label="actual_cm_unit_action_falsifier",
                argv=(python, "p24/trace_gcd_actual_cm_unit_action_falsifier.py"),
                timeout=45.0,
                must_contain=(
                    "literal_equal_edges=0/",
                    "punit_ratio_edges=4/4",
                    "conclusion=reported_trace_gcd_actual_cm_unit_action_falsifier",
                ),
            )
        )
    if include_two_resultant_holdouts:
        tasks.append(
            Task(
                label="two_resultant_holdout_audit",
                argv=(python, "p24/trace_gcd_two_resultant_holdout_audit.py"),
                timeout=75.0,
                must_contain=(
                    "selected_two_punit_groups=4/4",
                    "punit_transport_edges=8/8",
                    "literal_equal_nonzero_edges=0/8",
                    "split_norm_matches=12/12",
                    "naive_base_polynomial_groups=0/4",
                    "conclusion=reported_trace_gcd_two_resultant_holdout_audit",
                ),
            )
        )
        tasks.append(
            Task(
                label="actual_cm_square_coinvariant_block_cycle_audit",
                argv=(
                    python,
                    "p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py",
                ),
                timeout=60.0,
                must_contain=(
                    "p24_target=skew_reduced_norm_of_transported_square_coinvariant_maps",
                    "block_cycle_matches=12/12",
                    "block_cycle_full_rank_detection_matches=12/12",
                    "full_rank_orbits=12/12",
                    "square_coinvariant_block_cycle_is_skew_reduced_norm=1",
                    "nonzero_side_can_target_transported_square_coinvariant_maps=1",
                    "conclusion=reported_trace_gcd_actual_cm_square_coinvariant_block_cycle_audit",
                ),
            )
        )
    if include_phase_divisor_holdout:
        tasks.append(
            Task(
                label="phase_divisor_identity_holdout",
                argv=(python, "p24/trace_gcd_phase_divisor_identity_holdout.py"),
                timeout=45.0,
                must_contain=(
                    "nonrandom_span_hits=0",
                    "full_rank_interpolation_hits=4",
                    "coordinate_payload_zero_detection_failure=1",
                    "conclusion=reported_trace_gcd_phase_divisor_identity_holdout",
                ),
            )
        )
    if include_simple_root_boundary:
        tasks.append(
            Task(
                label="cm_simple_root_different_boundary",
                argv=(python, "p24/cm_simple_root_different_boundary.py"),
                timeout=45.0,
                must_contain=(
                    "class_polynomial_split_squarefree=1",
                    "zero_derivative_count=0",
                    "control_det_zero=1",
                    "conclusion=reported_cm_simple_root_different_boundary",
                ),
            )
        )
    if include_selected_tail_tensor_factors:
        selected_tail_cases = (
            ("selected_tail_tensor_factor_D10919_m12_axis", "-10919", "12", "200"),
            ("selected_tail_tensor_factor_D1559_m3_axis", "-1559", "3", "100"),
            ("selected_tail_tensor_factor_D2207_m3_axis", "-2207", "3", "100"),
        )
        for label, discriminant, m_value, max_h in selected_tail_cases:
            tasks.append(
                Task(
                    label=label,
                    argv=(
                        python,
                        "p24/trace_frame_selected_tail_tensor_factor_equivariance_audit.py",
                        "--only-D",
                        discriminant,
                        "--min-h",
                        "1",
                        "--max-h",
                        max_h,
                        "--only-m",
                        m_value,
                        "--max-n",
                        "200",
                        "--max-factor-degree",
                        "20",
                        "--max-extension-degree",
                        "8",
                        "--max-tensor-factor-degree",
                        "12",
                        "--max-top-count",
                        "4",
                        "--target",
                        "axis",
                        "--max-rows",
                        "40",
                        "--include-linear",
                    ),
                    timeout=20.0,
                    must_contain=(
                        "tail_zero_status_uniform=1",
                        "selected_tail_transport_survives=1",
                        "conclusion=reported_trace_frame_selected_tail_tensor_factor_equivariance_audit",
                    ),
                )
            )
    return tasks


def print_result(result: TaskResult, verbose: bool) -> None:
    status = "ok" if result.ok else "FAIL"
    timeout = " timeout=1" if result.timed_out else ""
    print(
        f"task={result.label} status={status} "
        f"elapsed={result.elapsed:.3f}s returncode={result.returncode}{timeout}"
    )
    if result.must_contain_missing:
        print(f"  missing_tokens={list(result.must_contain_missing)}")
    interesting_prefixes = (
        "field_q=",
        "right=",
        "k=",
        "support_size_",
        "all_ones parts=",
        "min_rayleigh_delta=",
        "witness parts=",
        "rayleigh_delta=",
        "strong_rayleigh_violated=",
        "zero_product_count=",
        "identity_mismatches=",
        "value_mismatches=",
        "product_equals_",
        "block_size=",
        "invertible_controls=",
        "singular_controls=",
        "p24_sign_positive=",
        "ord_m(p)=",
        "ord_n(p)=",
        "tensor_factor_count_over_E=",
        "tensor_factor_degree_over_E=",
        "E_frobenius_multiplier_a=",
        "C_degree_over_E=",
        "B_degree_over_C=",
        "trace_subgroup_generator_a^179_mod_n=",
        "trace_subgroup_order=",
        "quotient_orbit_length=",
        "trace_cosets_partition_factor_orbit=",
        "coordinate_count_over_E=",
        "selected_axis_rank_target=",
        "positive_implication_failures=",
        "nonnormal_controls=",
        "normal_theta_implies_relative_trace_period_normal_basis=",
        "relative_trace_normality_is_not_automatic=",
        "forced_intersection_dim=",
        "residual_tail_dim=",
        "one_factor_all_H_packets_Fp_slots_over_sqrt=",
        "all_70_factors_all_H_packets_Fp_slots_over_sqrt=",
        "decomposition_field_relative_degree8_punits_with_tensor_symmetry=",
        "component_full=",
        "intersection_minimal=",
        "prefix_max_rank=",
        "nonzero_determinant_rows=",
        "zero_determinant_rows=",
        "zero_det_norms=",
        "tail_separates_kernel=",
        "full_lead_nonzero=",
        "full_rank_impossible_when_prefix_rank_below_3=",
        "canonical_all_nonzero=",
        "unit_twist_zero_compatible=",
        "spliced_all_nonzero=",
        "no_single_fixed_minor_nonzero=",
        "zero_detection_failures=",
        "full_rank_iff_failures=",
        "fixed_minor_zeros=",
        "cm_minor_zeros=",
        "coeff_support_size=",
        "sign_positive=",
        "scale_failures=",
        "zero_mismatches=",
        "basis_changes_scale_block_cycle_by_units=",
        "punit_edges=",
        "determinant_mismatches=",
        "singular_zero_edges=",
        "singular_zero_mismatches=",
        "left_plateau_length=",
        "ord_right_q=",
        "plateau_subspace_dim=",
        "factor_count=",
        "nonzero_factor_blocks=",
        "case=",
        "global_relation_iff_T_orbit_stays_in_first_component_kernel=",
        "first_component_kernel_large_but_semilinear_core_must_be_zero=",
        "forced_fixed_frequency_core_detected=",
        "p24_semilinear_T_order=",
        "p24_first_component_kernel_dim_lower_bound=",
        "source_dim_over_k=",
        "fixed_vector_count_expected=",
        "p24_fixed_frequency_count=",
        "p24_length4_frequency_orbit_count=",
        "p24_fixed_frequency_variables=",
        "p24_prefix_blocks=",
        "p24_tail_dim=",
        "p24_fixed_prefix_variables=",
        "p24_length4_K_variables=",
        "p24_fixed_source_fp_dimension=",
        "semilinear_descent_core_kdim_equals_fixed_kernel_fpdim=",
        "zero_core_iff_no_nonzero_T_fixed_relation=",
        "zero_core_iff_no_nonzero_T_fixed_RS_tail_relation=",
        "p24_fixed_relation_shape_Fp28_plus_K28_to_L=",
        "p24_fixed_relation_shape_Fp28_plus_K28_plus_Fp16_to_L=",
        "global_relation_iff_T_orbit_stays_in_RS_tail_kernel=",
        "forced_prefix_fixed_core_detected=",
        "forced_rs_tail_fixed_core_detected=",
        "source_size=",
        "lambda_count=",
        "pairing_mismatches=",
        "p24_fixed_adjoint_scalar_tests=",
        "p24_fixed_adjoint_K_tests=",
        "p24_fixed_adjoint_target_fp_dimension=",
        "fixed_adjoint_pairing_formula_verified=",
        "fixed_relation_injective_iff_adjoint_syndrome_surjective=",
        "p24_syndrome_shape_Fp28_plus_K28=",
        "coordinate_count=",
        "coordinate_rank=",
        "trace_matrix_rank=",
        "residual_product_zero=",
        "residual_norm=",
        "p24_syndrome_coordinate_count=",
        "syndrome_coordinate_elements_represent_fixed_adjoint=",
        "trace_pairing_rank_equals_coordinate_span_rank=",
        "syndrome_moore_residual_nonzero_iff_full_rank=",
        "prefix_surjective=",
        "tail_rank_on_kernel=",
        "tail_injective_on_kernel=",
        "full_residual_nonzero=",
        "p24_prefix_syndrome_target_dim=",
        "p24_residual_kernel_dim=",
        "prefix_syndrome_surjective_gives_kernel_dim_16=",
        "tail_resultant_nonzero_iff_tail_injective_on_kernel=",
        "full_140_plus_16_residual_nonzero_iff_prefix_and_tail=",
        "dft_difference_mismatches=",
        "nonzero_multiplier_failures=",
        "direct_rowspace_tests=",
        "direct_rowspace_equal=",
        "direct_rowspace_combined_ranks=",
        "lambda_basis=",
        "profile_dft_mismatches=",
        "lambda_fourier_trace_mismatches=",
        "lang_reconstruction_mismatches=",
        "lang_zero_equivalence_failures=",
        "checked_right_frequencies=",
        "checked_orbit_vectors=",
        "source_dim=",
        "coord_rank=",
        "trace_rank=",
        "trace_det=",
        "ann_q_degree=",
        "pivots=",
        "residual_norm_product=",
        "rank_match=",
        "event_match=",
        "rank_mismatches=",
        "prefix_adjoint_rank_mismatches=",
        "surjective_adjoint_event_mismatches=",
        "pairing_mismatches=",
        "found_positive_kernel_surjective=",
        "forced_dependent_not_surjective=",
        "hilbert90_match_failures=",
        "trace_nonintersection_event_mismatches=",
        "found_hilbert90_nonintersection=",
        "forced_coboundary_intersection_detected=",
        "forced_period_dependence_detected=",
        "event_mismatches=",
        "low_rank_zero_products=",
        "prefix_len=",
        "tail_len=",
        "full_rank=",
        "prefix_rank=",
        "adjoint_rank=",
        "kernel_dim=",
        "codomain_dim=",
        "domain_dim=",
        "phi_rank=",
        "domain_kernel=",
        "intersection=",
        "nonintersection=",
        "coboundary_rank=",
        "trace_kernel_dim=",
        "coboundary_trace_failures=",
        "tail_dim=",
        "phi_rank=",
        "coinv_rank=",
        "coinvariant_rank=",
        "intersection=",
        "primal_full=",
        "adjoint_full=",
        "coinv_full=",
        "duality_match=",
        "coinv_match=",
        "duality_mismatches=",
        "coinvariant_mismatches=",
        "found_full_coinvariant_unit=",
        "forced_tail_inside_prefix_span_detected=",
        "local_full=",
        "block_det=",
        "expected=",
        "determinant_match=",
        "zero_detection=",
        "full_rank_detection=",
        "local_dets=",
        "found_all_full_coinvariant_cycle=",
        "forced_singular_coinvariant_cycle_detected=",
        "tail_pivots=",
        "full_product=",
        "prefix_product=",
        "tail_product=",
        "prefix_count=",
        "tail_count=",
        "random_trials=",
        "basis_moore_norm=",
        "full_residual_mismatches=",
        "full_chow_mismatches=",
        "norm_chow_mismatches=",
        "prefix_moore_mismatches=",
        "tail_image_mismatches=",
        "prefix_tail_mismatches=",
        "full_zero_coordinate_zero_mismatches=",
        "forced_prefix_zero=",
        "forced_tail_zero=",
        "pivot_rows=",
        "prefix_zero_mismatches=",
        "tail_zero_mismatches=",
        "full_zero_mismatches=",
        "forced_prefix_no_pivot=",
        "forced_tail_schur_zero=",
        "product_match=",
        "prefix_nonzero=",
        "tail_nonzero=",
        "product_mismatches=",
        "prefix_failure_controls=",
        "tail_failure_controls=",
        "nontrivial_prefix_rows=",
        "plateau_rank=",
        "leading_rank=",
        "combined_rank=",
        "bad_dim=",
        "bad_not_plateau_rank=",
        "rowspace_containment_failures=",
        "nonvacuous_containments=",
        "vacuous_full_leading_rank=",
        "max_bad_not_plateau_rank=",
        "det_plateau=",
        "det_leading=",
        "ratio=",
        "both_nonzero=",
        "rowspace_equal=",
        "distinct_nonzero_ratios=",
        "trace_rank_mismatches=",
        "nonzero_event_mismatches=",
        "missing_residual_norm_products=",
        "full_rank_rows=",
        "explicit_column_count_mismatches=",
        "fixed_freqs=",
        "moving_freq_orbits=",
        "fixed_prefix_cols=",
        "moving_prefix_cols=",
        "tail_cols=",
        "explicit_cols=",
        "psi_rank=",
        "actual_cm_rs_tail_fixed_columns_match_time_rank=",
        "actual_cm_hilbert90_fixed_relation_shape_survives=",
        "right_class_det_mismatches=",
        "split_eval_mismatches=",
        "naive_base_polynomial_possible=",
        "orbit_norm_nonzero=",
        "p_mod_right=",
        "hilbert_class_frobenius_order=",
        "ordinary_base_polynomial_descent_is_not_forced=",
        "crossed_product_orbit_norm_is_the_honest_phase_payload=",
        "profile=",
        "matrix_rows=",
        "orbit_rows=",
        "nonzero_orbits=",
        "zero_or_bad_orbits=",
        "zero_norm_orbits=",
        "unit=",
        "unit_action_mapping=",
        "zero_orbit_fixed=",
        "nonzero_cycle=",
        "nonzero_cycle_covers_all_nonzero_orbits=",
        "literal_equal_edges=",
        "punit_ratio_edges=",
        "p24_target=",
        "selected_two_punit_groups=",
        "all_nonzero_groups=",
        "punit_transport_edges=",
        "literal_equal_nonzero_edges=",
        "split_norm_matches=",
        "naive_base_polynomial_groups=",
        "p24_square_dim=",
        "p24_nonzero_orbit_len=",
        "p24_block_cycle_sign_positive=",
        "block_cycle_matches=",
        "block_cycle_full_rank_detection_matches=",
        "full_rank_orbits=",
        "singular_control_orbits=",
        "square_coinvariant_block_cycle_is_skew_reduced_norm=",
        "nonzero_side_can_target_transported_square_coinvariant_maps=",
        "p24_still_needs_punit_theorem_for_the_actual_skew_norm=",
        "quotient_cycle_unit=",
        "quotient_cycle_covers_nonzero=",
        "selected_nonzero_crossed_norm_punit=",
        "expected_payload_field_elements=",
        "expected_payload_over_sqrt_floor=",
        "producer_honesty_required",
        "diamond_equivariance_required",
        "orbit_len=",
        "tail=",
        "columns:",
        "D=",
        "row ",
        "totals",
        "  rows=",
        "  zero_rows=",
        "  product_mod_q=",
        "conclusion=",
    )
    for line in result.stdout.splitlines():
        stripped = line.lstrip()
        if verbose or stripped.startswith(interesting_prefixes) or stripped.startswith("-"):
            print(f"  {line}")
    if result.stderr.strip():
        print("  stderr:")
        for line in result.stderr.splitlines()[-12:]:
            print(f"    {line}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--skip-spectral", action="store_true")
    parser.add_argument("--include-actual-cm-triangle", action="store_true")
    parser.add_argument("--include-actual-cm-unit-action", action="store_true")
    parser.add_argument("--include-two-resultant-holdouts", action="store_true")
    parser.add_argument("--include-phase-divisor-holdout", action="store_true")
    parser.add_argument("--include-simple-root-boundary", action="store_true")
    parser.add_argument("--include-selected-tail-tensor-factors", action="store_true")
    parser.add_argument("--no-danger3-inventory", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not args.no_danger3_inventory:
        print_danger3_inventory()

    tasks = default_tasks(
        include_spectral=not args.skip_spectral,
        include_actual_cm_triangle=args.include_actual_cm_triangle,
        include_actual_cm_unit_action=args.include_actual_cm_unit_action,
        include_two_resultant_holdouts=args.include_two_resultant_holdouts,
        include_phase_divisor_holdout=args.include_phase_divisor_holdout,
        include_simple_root_boundary=args.include_simple_root_boundary,
        include_selected_tail_tensor_factors=args.include_selected_tail_tensor_factors,
    )
    print("fast trace-GCD falsifier tasks")
    print(f"  task_count={len(tasks)}")
    print(f"  workers={args.workers}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_task, task) for task in tasks]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    for result in sorted(results, key=lambda item: item.label):
        print_result(result, verbose=args.verbose)

    failures = [result.label for result in results if not result.ok]
    print("summary")
    print(f"  passed={len(results) - len(failures)}")
    print(f"  failed={len(failures)}")
    print(f"  failures={failures}")
    print("  conclusion=fast_falsifier_completed")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
