#!/usr/bin/env bash
set -euo pipefail

run_dir="${1:-$(cat /tmp/p23_run_dir.txt)}"

if [[ ! -d "$run_dir" ]]; then
  echo "Run directory not found: $run_dir" >&2
  exit 1
fi

echo "run_dir=$run_dir"
date
echo

if grep -H "Verified: PASS" "$run_dir"/worker*.log 2>/dev/null; then
  echo
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
total=0
count=0
for f in "$run_dir"/worker*.log; do
  [[ -e "$f" ]] || continue
  tail_line="$(tail -n 1 "$f" || true)"
  progress_line="$(awk '/trials=/ { line = $0 } END { print line }' "$f")"
  if [[ -n "$progress_line" ]]; then
    printf "%s\n" "$progress_line" >> "$tmp"
  else
    printf "%s\n" "$tail_line" >> "$tmp"
  fi
  printf "%s: %s\n" "$(basename "$f")" "$tail_line"
  if [[ -n "$progress_line" && "$progress_line" != "$tail_line" ]]; then
    printf "%s latest_progress: %s\n" "$(basename "$f")" "$progress_line"
  fi
  trials="$(printf "%s\n" "$progress_line" | sed -n 's/.*trials=\([0-9][0-9]*\).*/\1/p')"
  if [[ -n "$trials" ]]; then
    total=$((total + trials))
    count=$((count + 1))
  fi
done

echo
printf "latest_tail_workers=%d\n" "$count"
printf "aggregate_latest_trials=%d\n" "$total"
awk -v t="$total" 'BEGIN { printf "aggregate_latest_billions=%.3f\n", t/1000000000 }'
awk -v t="$total" 'BEGIN { printf "fraction_of_sqrt_p=%.6f\n", t/316227766016 }'
awk -v t="$total" 'BEGIN { printf "fraction_of_50B_budget=%.4f\n", t/50000000000 }'
awk -v t="$total" '
  {
    for (i = 1; i <= NF; i++) {
      if ($i ~ /^elapsed=/) { split($i, a, "="); elapsed_sum += a[2]; elapsed_count++ }
      if ($i ~ /^rate_Mps=/) { split($i, r, "="); rate_sum += r[2] }
    }
  }
  END {
    if (elapsed_count > 0 && rate_sum > 0) {
      avg_elapsed = elapsed_sum / elapsed_count
      printf "avg_worker_elapsed_seconds=%.1f\n", avg_elapsed
      printf "aggregate_rate_Mps=%.3f\n", rate_sum
      targets[1] = 35000000000
      names[1] = "35B"
      targets[2] = 45000000000
      names[2] = "45B"
      targets[3] = 50000000000
      names[3] = "50B"
      for (j = 1; j <= 3; j++) {
        remaining = targets[j] - t
        if (remaining < 0) remaining = 0
        seconds = remaining / (rate_sum * 1000000)
        printf "eta_to_%s_hours=%.2f\n", names[j], seconds / 3600
      }
    }
    # X1(16) probability model from notes: E[trials] ~= 34.6B / L.
    e1 = 34600000000
    e080 = 43300000000
    e067 = 51700000000
    printf "model_no_hit_prob_L1.00=%.4f\n", exp(-t / e1)
    printf "model_no_hit_prob_L0.80=%.4f\n", exp(-t / e080)
    printf "model_no_hit_prob_L0.67=%.4f\n", exp(-t / e067)
  }
' "$tmp"
