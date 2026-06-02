#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${P23_RUN_DIR:-$(cat /tmp/p23_run_dir.txt 2>/dev/null || true)}"
execute="0"

usage() {
  cat <<EOF
Usage: $0 [options]

Decide the next p23 operational action from the current logs.

By default this is a dry run. It prints the decision and proposed command but
does not finalize a hit or launch a new shard. Use --execute to run the action.

Options:
  --run-dir DIR   Run directory to inspect (default: /tmp/p23_run_dir.txt)
  --execute       Execute finalize/launch/status action
  -h, --help      Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) run_dir="$2"; shift 2 ;;
    --execute) execute="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$run_dir" || ! -d "$run_dir" ]]; then
  echo "Run directory not found: ${run_dir:-<empty>}" >&2
  exit 1
fi

decision_output="$("$repo_root/scripts/p23_decision_status.sh" "$run_dir")"
printf "%s\n" "$decision_output"

decision="$(printf "%s\n" "$decision_output" | sed -n 's/^decision=//p' | tail -n 1)"
worker_log="$(printf "%s\n" "$decision_output" | sed -n 's/^worker_log=//p' | tail -n 1)"
next_command="$(printf "%s\n" "$decision_output" | sed -n 's/^next_command=//p' | tail -n 1)"

if [[ "$execute" != "1" ]]; then
  echo "dry_run=1"
  echo "would_run=$next_command"
  exit 0
fi

case "$decision" in
  verify_hit)
    if [[ -z "$worker_log" || ! -f "$worker_log" ]]; then
      echo "Decision requested hit verification, but worker log is missing: ${worker_log:-<empty>}" >&2
      exit 1
    fi
    echo "executing=finalize_hit"
    exec "$repo_root/scripts/finalize_pomerance_hit.sh" --log "$worker_log"
    ;;
  keep_waiting)
    echo "executing=status"
    exec "$repo_root/scripts/p23_status.sh" "$run_dir"
    ;;
  launch_nonsplit_next_shard)
    echo "executing=launch_directy_nonsplit_next_shard"
    exec "$repo_root/scripts/p23_launch_x16halvenonsplit_directy_next.sh"
    ;;
  manual_review)
    echo "executing=status_for_manual_review"
    exec "$repo_root/scripts/p23_status.sh" "$run_dir"
    ;;
  *)
    echo "Unknown decision: ${decision:-<empty>}" >&2
    exit 1
    ;;
esac
