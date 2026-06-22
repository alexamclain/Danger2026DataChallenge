#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

P="${P:-1000000000000000000000000103}"
SEED_OFFSET="${SEED_OFFSET:-0}"
TRIALS="${TRIALS:-5000000}"
CHUNK_TRIALS="${CHUNK_TRIALS:-$TRIALS}"
BLOCKS="${BLOCKS:-0}"
THREADS="${THREADS:-128}"
CLAIM_BATCH="${CLAIM_BATCH:-64}"
BACKEND="${BACKEND:-u96}"
TARGET_DEPTH="${TARGET_DEPTH:-13}"
BUCKET_BITS="${BUCKET_BITS:-6}"
CUDA_ARCH="${CUDA_ARCH:-sm_89}"
SEED_MODES="${SEED_MODES:-identity splitmix}"
MODES="${MODES:-x16d2probe x16quadprecheckprobe x16quadtelemetryprobe}"
OUT_DIR="${OUT_DIR:-$repo_root/results/p27/gpu_quad_$(date -u +%Y%m%dT%H%M%SZ)}"
BIN="${BIN:-$repo_root/build/pomerance_cuda_quad}"
DRY_RUN="${DRY_RUN:-0}"

usage() {
  cat <<EOF
Usage: $0 [options]

Compile the CUDA probe binary and run bounded p27 quadratic-gate probes.
This is not a production p27 search and does not scan random (R,L) conic-pair
parameters.  The latest legal-incidence screen kills raw random (R,L) as a
source because legal hits are only about constant/q per draw.

Default modes:
  x16d2probe              legal post-d2 baseline
  x16quadprecheckprobe    quadratic-gate short-circuit A/B
  x16quadtelemetryprobe   materialized formula-vs-actual telemetry

TARGET_DEPTH defaults to 13 so telemetry observes gates 3 through 8.

Environment overrides:
  P              prime (default p27 = 10^27 + 103)
  SEED_OFFSET    starting seed offset (default 0)
  TRIALS         accepted rows per run; post-d2 for x16d2probe, recurrence-domain
                 rows for quadratic probes (default 5000000)
  CHUNK_TRIALS   chunk size per kernel launch (default TRIALS)
  BLOCKS         CUDA blocks, 0 lets the binary choose (default 0)
  THREADS        CUDA threads per block (default 128)
  CLAIM_BATCH    accepted-root claim batch (default 64)
  BACKEND        backend, quadratic probes require u96 (default u96)
  TARGET_DEPTH   selected-halving depth threshold (default 13)
  BUCKET_BITS    bucket bits for the x16d2probe baseline (default 6)
  CUDA_ARCH      nvcc arch (default sm_89)
  SEED_MODES     quoted list, e.g. "identity" or "identity splitmix"
  MODES          quoted list of probe modes
  OUT_DIR        output directory for logs
  BIN            binary path
  DRY_RUN        set to 1 to print commands only

Options:
  --dry-run      Print commands without running them
  -h, --help     Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ "$DRY_RUN" != "1" ]]; then
  mkdir -p "$OUT_DIR" "$(dirname "$BIN")"
fi

compile_cmd=(nvcc -O3 -std=c++17 "-arch=$CUDA_ARCH" -o "$BIN" "$repo_root/pomerance_cuda.cu")
echo "compile=${compile_cmd[*]}"
if [[ "$DRY_RUN" != "1" ]]; then
  "${compile_cmd[@]}"
  shasum -a 256 "$BIN" | tee "$OUT_DIR/binary.sha256"
fi

print_config() {
  cat <<EOF
p=$P
seed_offset=$SEED_OFFSET
trials=$TRIALS
chunk_trials=$CHUNK_TRIALS
blocks=$BLOCKS
threads=$THREADS
claim_batch=$CLAIM_BATCH
backend=$BACKEND
target_depth=$TARGET_DEPTH
bucket_bits=$BUCKET_BITS
seed_modes=$SEED_MODES
modes=$MODES
EOF
}

print_config
if [[ "$DRY_RUN" != "1" ]]; then
  print_config > "$OUT_DIR/run_config.txt"
fi

for seed_mode in $SEED_MODES; do
  for mode in $MODES; do
    log="$OUT_DIR/${mode}_seed-${seed_mode}_offset-${SEED_OFFSET}_trials-${TRIALS}.log"
    cmd=("$BIN" "$P" "$SEED_OFFSET" "$TRIALS" "$mode" "$CHUNK_TRIALS"
         "$BLOCKS" "$THREADS" "$CLAIM_BATCH" "$BACKEND"
         "seed=$seed_mode" "target_depth=$TARGET_DEPTH" "bucket_bits=$BUCKET_BITS")
    echo "run_log=$log"
    echo "run=${cmd[*]}"
    if [[ "$DRY_RUN" != "1" ]]; then
      "${cmd[@]}" 2>&1 | tee "$log"
    fi
  done
done

if [[ "$DRY_RUN" != "1" ]]; then
  grep -h '^scope_probe_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^scope_probe_jsonl=//' > "$OUT_DIR/scope_probe_rows.jsonl" || true
  grep -h '^quadprecheck_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^quadprecheck_jsonl=//' > "$OUT_DIR/quad_probe_rows.jsonl" || true
  echo "scope_jsonl=$OUT_DIR/scope_probe_rows.jsonl"
  echo "quad_jsonl=$OUT_DIR/quad_probe_rows.jsonl"
fi
