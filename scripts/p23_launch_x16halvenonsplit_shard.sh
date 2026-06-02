#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

p="100000000000000000000117"
seed_base="7000000"
seed_step="104729"
workers="10"
trials_per_worker="5000000000"
default_binary="$repo_root/pomerance_nonsplit_yfilter"
binary="$default_binary"
expected_default_sha256="33c9120f7ab39258b4a5da0b1b1cbd13ebe16d15e43409f7a4fe0c1339b271c1"
force="0"
allow_hash_mismatch="0"
preflight="0"
monitor="1"

usage() {
  cat <<EOF
Usage: $0 [options]

Launch a p23 X1(16)-halving shard set using the y-filtered nonsplit sampler.
This is intended for use only after the current shard finishes or misses; by
default it refuses to launch while existing p23 pomerance workers are running.

Options:
  --seed-base N           First worker seed offset (default: $seed_base)
  --seed-step N           Seed increment per worker (default: $seed_step)
  --workers N             Number of workers (default: $workers)
  --trials-per-worker N   Budget per worker (default: $trials_per_worker)
  --binary PATH           Binary to copy into the run dir (default: $binary)
  --allow-hash-mismatch   Allow the default binary hash to differ from the vetted hash
  --preflight             Check binary/guard status without creating a run dir
  --no-monitor            Launch workers, print monitor commands, and return
  --force                 Launch even if pomerance workers are running
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
    --allow-hash-mismatch) allow_hash_mismatch="1"; shift ;;
    --preflight) preflight="1"; shift ;;
    --no-monitor) monitor="0"; shift ;;
    --force) force="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ ! -x "$binary" ]]; then
  echo "Binary is not executable: $binary" >&2
  exit 1
fi

actual_default_sha256=""
if [[ "$binary" == "$default_binary" ]]; then
  actual_default_sha256="$(shasum -a 256 "$binary" | awk '{print $1}')"
  if [[ "$actual_default_sha256" != "$expected_default_sha256" ]] && [[ "$allow_hash_mismatch" != "1" ]]; then
    echo "Refusing to launch because the default nonsplit binary hash changed." >&2
    echo "expected: $expected_default_sha256" >&2
    echo "actual:   $actual_default_sha256" >&2
    echo >&2
    echo "Use --binary PATH for a separately vetted binary, or --allow-hash-mismatch only after revalidating this one." >&2
    exit 1
  fi
fi

running_file="/tmp/p23_running_pomerance.txt"
running_processes="0"
if pgrep -fl "[p]omerance[^[:space:]]*[[:space:]]+$p" >"$running_file" 2>/dev/null; then
  running_processes="$(wc -l < "$running_file" | tr -d ' ')"
fi

if [[ "$preflight" == "1" ]]; then
  echo "preflight=1"
  echo "p=$p"
  echo "binary=$binary"
  echo "binary_executable=1"
  if [[ "$binary" == "$default_binary" ]]; then
    echo "expected_default_sha256=$expected_default_sha256"
    echo "actual_default_sha256=$actual_default_sha256"
  fi
  echo "running_p23_processes=$running_processes"
  if [[ "$running_processes" != "0" && "$force" != "1" ]]; then
    echo "launch_allowed=0"
    echo "reason=active_p23_processes"
    sed 's/^/running: /' "$running_file"
  else
    echo "launch_allowed=1"
  fi
  exit 0
fi

if [[ "$force" != "1" ]] && [[ "$running_processes" != "0" ]]; then
  echo "Refusing to launch because p23 pomerance processes are already running:" >&2
  cat "$running_file" >&2
  echo >&2
  echo "Re-run with --force only if you intentionally want to oversubscribe this machine." >&2
  exit 1
fi

run_dir="$repo_root/runs/p23_x16halvenonsplit_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$run_dir"
cp "$binary" "$run_dir/pomerance_nonsplit"
binary_sha256="$(shasum -a 256 "$binary" | awk '{print $1}')"
copied_sha256="$(shasum -a 256 "$run_dir/pomerance_nonsplit" | awk '{print $1}')"
cd "$run_dir"

echo "$run_dir" > /tmp/p23_run_dir.txt

{
  printf "run_dir=%s\n" "$run_dir"
  printf "p=%s\n" "$p"
  printf "workers=%s\n" "$workers"
  printf "max_trials_per_worker=%s\n" "$trials_per_worker"
  printf "seed_base=%s\n" "$seed_base"
  printf "seed_step=%s\n" "$seed_step"
  printf "mode=x16halvenonsplit\n"
  printf "monitor=%s\n" "$monitor"
  printf "binary_source=%s\n" "$binary"
  printf "binary_sha256=%s\n" "$binary_sha256"
  printf "copied_binary_sha256=%s\n" "$copied_sha256"
} | tee run-info.txt

cat > README.md <<EOF
# p23 X1(16)-Halving Nonsplit Shard

This run uses the y-filtered nonsplit sampler:

\`\`\`text
nonsplit iff Legendre((y^2 - 2)(y^2 - 4y + 2), p) = -1
\`\`\`

Launch command:

\`\`\`bash
scripts/p23_launch_x16halvenonsplit_shard.sh --seed-base $seed_base --workers $workers --trials-per-worker $trials_per_worker
\`\`\`

Target:

\`\`\`text
p = $p
mode = x16halvenonsplit
workers = $workers
max_trials_per_worker = $trials_per_worker
binary_sha256 = $binary_sha256
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
  if [[ "$monitor" == "1" ]]; then
    ./pomerance_nonsplit "$p" "$seed" "$trials_per_worker" x16halvenonsplit > "$log" 2>&1 &
    pid=$!
  else
    pid="$(P23_WORKER_LOG="$log" P23_WORKER_SEED="$seed" python3 - <<PY
import os
import subprocess

log = open(os.environ["P23_WORKER_LOG"], "wb")
proc = subprocess.Popen(
    ["./pomerance_nonsplit", "$p", os.environ["P23_WORKER_SEED"], "$trials_per_worker", "x16halvenonsplit"],
    stdin=subprocess.DEVNULL,
    stdout=log,
    stderr=subprocess.STDOUT,
    start_new_session=True,
)
log.close()
print(proc.pid)
PY
)"
  fi
  echo "$pid $log $seed" | tee -a pids.txt
  pids+=("$pid")
done

sleep 2
for pid in "${pids[@]}"; do
  kill -0 "$pid" 2>/dev/null && echo "alive $pid" || echo "dead $pid"
done

if [[ "$monitor" != "1" ]]; then
  cat <<EOF
monitor=0
run_dir=$run_dir
status_command=$repo_root/scripts/p23_status.sh $run_dir
decision_command=$repo_root/scripts/p23_next_action.sh --run-dir $run_dir
watch_command=$repo_root/scripts/p23_watch_and_verify.sh --run-dir $run_dir --finalize
EOF
  exit 0
fi

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
