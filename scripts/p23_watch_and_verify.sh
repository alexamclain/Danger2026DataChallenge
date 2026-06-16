#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${P23_RUN_DIR:-$(cat /tmp/p23_run_dir.txt 2>/dev/null || true)}"
interval="30"
once="0"
log_path=""
out_path=""
finalize="0"
artifact_dir=""
lean="1"

usage() {
  cat <<EOF
Usage: $0 [options]

Watch a p23 run directory for a worker "Verified: PASS" line and run local
verification on the winning log. With --finalize, create the full persistent
hit artifact bundle.

This does not manage worker processes.

Options:
  --run-dir DIR       Run directory to watch (default: /tmp/p23_run_dir.txt)
  --log PATH          Verify this worker log immediately instead of watching
  --out PATH          Transcript output path for the watcher/finalizer command
  --finalize          Run finalize_pomerance_hit.sh instead of verify only
  --artifact-dir DIR  Artifact directory for --finalize
  --no-lean           Skip Lean generation when using --finalize
  --interval SEC      Poll interval while watching (default: $interval)
  --once              Check once and exit if no hit is present
  -h, --help          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) run_dir="$2"; shift 2 ;;
    --log) log_path="$2"; shift 2 ;;
    --out) out_path="$2"; shift 2 ;;
    --finalize) finalize="1"; shift ;;
    --artifact-dir) artifact_dir="$2"; shift 2 ;;
    --no-lean) lean="0"; shift ;;
    --interval) interval="$2"; shift 2 ;;
    --once) once="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

verify_log() {
  local log="$1"
  local out="$2"
  mkdir -p "$(dirname "$out")"
  {
    date
    printf "worker_log=%s\n" "$log"
    printf "transcript=%s\n\n" "$out"
    "$repo_root/scripts/verify_pomerance_triple.py" --log "$log"
  } | tee "$out"
}

finalize_log() {
  local log="$1"
  local out="$2"
  local -a args=(--log "$log")
  if [[ -n "$artifact_dir" ]]; then
    args+=(--out-dir "$artifact_dir")
  fi
  if [[ "$lean" != "1" ]]; then
    args+=(--no-lean)
  fi
  mkdir -p "$(dirname "$out")"
  {
    date
    printf "worker_log=%s\n" "$log"
    printf "transcript=%s\n" "$out"
    if [[ -n "$artifact_dir" ]]; then
      printf "artifact_dir=%s\n" "$artifact_dir"
    fi
    printf "\n"
    "$repo_root/scripts/finalize_pomerance_hit.sh" "${args[@]}"
  } | tee "$out"
}

if [[ -n "$log_path" ]]; then
  if [[ ! -f "$log_path" ]]; then
    echo "Worker log not found: $log_path" >&2
    exit 1
  fi
  if [[ -z "$out_path" ]]; then
    if [[ "$finalize" == "1" ]]; then
      out_path="$(dirname "$log_path")/finalize-$(basename "$log_path" .log).txt"
    else
      out_path="$(dirname "$log_path")/verification-$(basename "$log_path" .log).txt"
    fi
  fi
  if [[ "$finalize" == "1" ]]; then
    finalize_log "$log_path" "$out_path"
  else
    verify_log "$log_path" "$out_path"
  fi
  exit 0
fi

if [[ -z "$run_dir" || ! -d "$run_dir" ]]; then
  echo "Run directory not found: ${run_dir:-<empty>}" >&2
  exit 1
fi

echo "watching_run_dir=$run_dir"
while true; do
  hit_line="$(grep -H "Verified: PASS" "$run_dir"/worker*.log 2>/dev/null | head -n 1 || true)"
  if [[ -n "$hit_line" ]]; then
    log="${hit_line%%:*}"
    if [[ -z "$out_path" ]]; then
      if [[ "$finalize" == "1" ]]; then
        out_path="$run_dir/finalize-$(basename "$log" .log).txt"
      else
        out_path="$run_dir/verification-$(basename "$log" .log).txt"
      fi
    fi
    if [[ "$finalize" == "1" ]]; then
      finalize_log "$log" "$out_path"
    else
      verify_log "$log" "$out_path"
    fi
    exit 0
  fi

  if [[ "$once" == "1" ]]; then
    echo "No worker PASS found in $run_dir"
    exit 2
  fi

  sleep "$interval"
done
