#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

p="100000000000000000000117"
seed_base="5000000"
seed_step="104729"
workers="10"
trials_per_worker="5000000000"
binary="$repo_root/pomerance_halve"
force="0"

usage() {
  cat <<EOF
Usage: $0 [options]

Launch a p23 X1(16)-halving shard set. This is intended for use only after the
current shard finishes or misses; by default it refuses to launch while any
pomerance_halve process is still running.

Options:
  --seed-base N           First worker seed offset (default: $seed_base)
  --seed-step N           Seed increment per worker (default: $seed_step)
  --workers N             Number of workers (default: $workers)
  --trials-per-worker N   Budget per worker (default: $trials_per_worker)
  --binary PATH           Binary to copy into the run dir (default: $binary)
  --force                 Launch even if pomerance_halve processes are running
  -h, --help              Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --seed-base) seed_base="$2"; shift 2 ;;
    --seed-step) seed_step="$2"; shift 2 ;;
    --workers) workers="$2"; shift 2 ;;
    --trials-per-worker) trials_per_worker="$2"; shift 2 ;;
    --binary) binary="$2"; shift 2 ;;
    --force) force="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ ! -x "$binary" ]]; then
  echo "Binary is not executable: $binary" >&2
  exit 1
fi

if [[ "$force" != "1" ]] && pgrep -fl "[p]omerance_halve" >/tmp/p23_running_pomerance.txt 2>/dev/null; then
  echo "Refusing to launch because pomerance_halve processes are already running:" >&2
  cat /tmp/p23_running_pomerance.txt >&2
  echo >&2
  echo "Re-run with --force only if you intentionally want to oversubscribe this machine." >&2
  exit 1
fi

run_dir="$repo_root/runs/p23_x16halve_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$run_dir"
cp "$binary" "$run_dir/pomerance_halve"
cd "$run_dir"

echo "$run_dir" > /tmp/p23_run_dir.txt

{
  printf "run_dir=%s\n" "$run_dir"
  printf "p=%s\n" "$p"
  printf "workers=%s\n" "$workers"
  printf "max_trials_per_worker=%s\n" "$trials_per_worker"
  printf "seed_base=%s\n" "$seed_base"
  printf "seed_step=%s\n" "$seed_step"
  printf "mode=x16halve\n"
  printf "binary_source=%s\n" "$binary"
} | tee run-info.txt

cat > README.md <<EOF
# p23 X1(16)-Halving Shard

This run was launched by:

\`\`\`bash
scripts/p23_launch_x16halve_shard.sh --seed-base $seed_base --workers $workers --trials-per-worker $trials_per_worker
\`\`\`

Target:

\`\`\`text
p = $p
mode = x16halve
workers = $workers
max_trials_per_worker = $trials_per_worker
\`\`\`

Monitor with:

\`\`\`bash
"$repo_root/scripts/p23_status.sh" "$run_dir"
\`\`\`

Verify a hit with:

\`\`\`bash
"$repo_root/scripts/verify_pomerance_triple.py" --log "$run_dir"/workerNN.log
\`\`\`
EOF

pids=()
for ((i=0; i<workers; i++)); do
  seed=$((seed_base + i * seed_step))
  log=$(printf "worker%02d.log" "$i")
  ./pomerance_halve "$p" "$seed" "$trials_per_worker" x16halve > "$log" 2>&1 &
  pid=$!
  echo "$pid $log $seed" | tee -a pids.txt
  pids+=("$pid")
done

sleep 2
for pid in "${pids[@]}"; do
  kill -0 "$pid" 2>/dev/null && echo "alive $pid" || echo "dead $pid"
done

start=$(date +%s)
while true; do
  if grep -H "Verified: PASS" worker*.log >/tmp/p23_hit_lines.txt 2>/dev/null; then
    echo "HIT detected"
    cat /tmp/p23_hit_lines.txt
    for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done
    wait || true
    break
  fi

  alive=0
  for pid in "${pids[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then alive=$((alive + 1)); fi
  done

  now=$(date +%s)
  elapsed=$((now - start))
  echo "monitor elapsed=${elapsed}s alive=${alive}"
  for log in worker*.log; do
    printf "%s: " "$log"
    tail -n 1 "$log" || true
  done

  if [[ "$alive" == "0" ]]; then
    echo "All workers exited without a detected hit."
    wait || true
    break
  fi
  sleep 30
done
