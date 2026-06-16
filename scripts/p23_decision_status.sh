#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${1:-$(cat /tmp/p23_run_dir.txt)}"
p="100000000000000000000117"
budget_total="50000000000"

if [[ ! -d "$run_dir" ]]; then
  echo "Run directory not found: $run_dir" >&2
  exit 1
fi

hit_line="$(grep -H "Verified: PASS" "$run_dir"/worker*.log 2>/dev/null | head -n 1 || true)"
if [[ -n "$hit_line" ]]; then
  log="${hit_line%%:*}"
  echo "decision=verify_hit"
  echo "run_dir=$run_dir"
  echo "worker_log=$log"
  echo "next_command=$repo_root/scripts/finalize_pomerance_hit.sh --log $log"
  exit 0
fi

alive=0
if [[ -f "$run_dir/pids.txt" ]]; then
  while read -r pid _rest; do
    [[ -n "${pid:-}" ]] || continue
    if kill -0 "$pid" 2>/dev/null; then
      alive=$((alive + 1))
    fi
  done < "$run_dir/pids.txt"
fi

total=0
for f in "$run_dir"/worker*.log; do
  [[ -e "$f" ]] || continue
  progress_line="$(awk '/trials=/ { line = $0 } END { print line }' "$f")"
  trials="$(printf "%s\n" "$progress_line" | sed -n 's/.*trials=\([0-9][0-9]*\).*/\1/p')"
  if [[ -n "$trials" ]]; then
    total=$((total + trials))
  fi
done

echo "run_dir=$run_dir"
echo "p=$p"
echo "alive_workers=$alive"
echo "aggregate_latest_trials=$total"
awk -v t="$total" -v b="$budget_total" 'BEGIN {
  printf "fraction_of_50B_budget=%.4f\n", t / b
}'

if [[ "$alive" -gt 0 ]]; then
  echo "decision=keep_waiting"
  echo "next_command=$repo_root/scripts/p23_status.sh $run_dir"
  exit 0
fi

if [[ "$total" -ge "$budget_total" ]]; then
  echo "decision=launch_nonsplit_next_shard"
  echo "next_command=$repo_root/scripts/p23_launch_x16halvenonsplit_directy_next.sh"
  exit 0
fi

echo "decision=manual_review"
echo "reason=workers_not_alive_but_budget_not_exhausted"
echo "next_command=$repo_root/scripts/p23_status.sh $run_dir"
