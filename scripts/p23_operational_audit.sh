#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${P23_RUN_DIR:-$(cat /tmp/p23_run_dir.txt 2>/dev/null || true)}"
include_probability="1"
include_preflight="1"
include_transfer="1"
transfer_samples="64"

usage() {
  cat <<EOF
Usage: $0 [options]

Print a read-only p23 operational audit:
  - decision gate
  - worker progress
  - probability window
  - nonsplit fallback preflight
  - short-certificate transfer audit

Options:
  --run-dir DIR       Run directory to inspect (default: /tmp/p23_run_dir.txt)
  --no-probability    Skip probability-window helper
  --no-preflight      Skip nonsplit fallback preflight
  --no-transfer       Skip short-certificate transfer audit
  --transfer-samples N
                      X1(16) y-character concordance samples (default: 64)
  -h, --help          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) run_dir="$2"; shift 2 ;;
    --no-probability) include_probability="0"; shift ;;
    --no-preflight) include_preflight="0"; shift ;;
    --no-transfer) include_transfer="0"; shift ;;
    --transfer-samples) transfer_samples="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$run_dir" || ! -d "$run_dir" ]]; then
  echo "Run directory not found: ${run_dir:-<empty>}" >&2
  exit 1
fi

section() {
  printf "\n== %s ==\n" "$1"
}

printf "p23_operational_audit=1\n"
printf "timestamp="
date
printf "run_dir=%s\n" "$run_dir"

section "decision"
"$repo_root/scripts/p23_decision_status.sh" "$run_dir"

section "status"
"$repo_root/scripts/p23_status.sh" "$run_dir"

if [[ "$include_probability" == "1" ]]; then
  section "probability"
  "$repo_root/scripts/p23_probability_window.py" "$run_dir"
fi

if [[ "$include_preflight" == "1" ]]; then
  section "nonsplit_fallback_preflight"
  "$repo_root/scripts/p23_launch_x16halvenonsplit_shard.sh" --preflight
fi

if [[ "$include_transfer" == "1" ]]; then
  section "short_certificate_transfer"
  "$repo_root/scripts/audit_short_certificate_transfer.py" --samples "$transfer_samples"
fi
