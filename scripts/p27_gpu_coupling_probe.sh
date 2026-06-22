#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

P="${P:-1000000000000000000000000103}"
SEED_OFFSET="${SEED_OFFSET:-0}"
RAW_DRAWS="${RAW_DRAWS:-100000000}"
CHUNK_DRAWS="${CHUNK_DRAWS:-$RAW_DRAWS}"
BLOCKS="${BLOCKS:-0}"
THREADS="${THREADS:-128}"
CLAIM_BATCH="${CLAIM_BATCH:-1}"
BACKEND="${BACKEND:-u96}"
CUDA_ARCH="${CUDA_ARCH:-sm_89}"
GATE_MAX="${GATE_MAX:-12}"
WORD_BITS="${WORD_BITS:-6}"
SEED_MODES="${SEED_MODES:-identity splitmix}"
OUT_DIR="${OUT_DIR:-$repo_root/results/p27/gpu_coupling_$(date -u +%Y%m%dT%H%M%SZ)}"
BIN="${BIN:-$repo_root/build/pomerance_cuda_coupling}"
DRY_RUN="${DRY_RUN:-0}"

usage() {
  cat <<EOF
Usage: $0 [options]

Compile the CUDA binary and run bounded p27 recurrence-coupling telemetry.
This is not a production p27 certificate search.  RAW_DRAWS is the raw
X1(16) y-source denominator used for source-normalized reporting.

The probe follows recurrence-domain rows and records selected quadratic-gate
signs:

  A = 2 - c^2
  x_j = r_j^2
  s_j = chi(r_j^2 + c*r_j + 1)

Defaults test gates 3..12.  Set GATE_MAX=16 for the stretch run if the 3..12
run is cheap.

Environment overrides:
  P            prime (default p27 = 10^27 + 103)
  SEED_OFFSET  starting seed offset (default 0)
  RAW_DRAWS    raw y-source draws per seed order (default 100000000)
  CHUNK_DRAWS  raw draws per kernel launch (default RAW_DRAWS)
  BLOCKS       CUDA blocks, 0 lets the binary choose (default 0)
  THREADS      CUDA threads per block (default 128)
  BACKEND      backend, probe requires u96 (default u96)
  CUDA_ARCH    nvcc arch (default sm_89)
  GATE_MAX     last selected gate to observe, max 16 (default 12)
  WORD_BITS    short sign-word bucket length, max 8 (default 6)
  SEED_MODES   quoted list, e.g. "identity" or "identity splitmix"
  OUT_DIR      output directory for logs
  BIN          binary path
  DRY_RUN      set to 1 to print commands only

Options:
  --dry-run    Print commands without running them
  -h, --help   Show this help
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
raw_draws=$RAW_DRAWS
chunk_draws=$CHUNK_DRAWS
blocks=$BLOCKS
threads=$THREADS
claim_batch=$CLAIM_BATCH
backend=$BACKEND
gate_max=$GATE_MAX
word_bits=$WORD_BITS
seed_modes=$SEED_MODES
EOF
}

print_config
if [[ "$DRY_RUN" != "1" ]]; then
  print_config > "$OUT_DIR/run_config.txt"
fi

for seed_mode in $SEED_MODES; do
  log="$OUT_DIR/x16quadcouplingprobe_seed-${seed_mode}_offset-${SEED_OFFSET}_raw-${RAW_DRAWS}_gates-3-${GATE_MAX}.log"
  cmd=("$BIN" "$P" "$SEED_OFFSET" "$RAW_DRAWS" x16quadcouplingprobe
       "$CHUNK_DRAWS" "$BLOCKS" "$THREADS" "$CLAIM_BATCH" "$BACKEND"
       "seed=$seed_mode" "gate_max=$GATE_MAX" "word_bits=$WORD_BITS")
  echo "run_log=$log"
  echo "run=${cmd[*]}"
  if [[ "$DRY_RUN" != "1" ]]; then
    "${cmd[@]}" 2>&1 | tee "$log"
  fi
done

if [[ "$DRY_RUN" != "1" ]]; then
  grep -h '^coupling_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^coupling_jsonl=//' > "$OUT_DIR/coupling_rows.jsonl" || true
  grep -h '^coupling_bucket_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^coupling_bucket_jsonl=//' > "$OUT_DIR/coupling_bucket_rows.jsonl" || true
  grep -h '^coupling_pair_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^coupling_pair_jsonl=//' > "$OUT_DIR/coupling_pair_rows.jsonl" || true
  grep -h '^coupling_lag_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^coupling_lag_jsonl=//' > "$OUT_DIR/coupling_lag_rows.jsonl" || true
  grep -h '^coupling_sample_jsonl=' "$OUT_DIR"/x16*.log |
    sed 's/^coupling_sample_jsonl=//' > "$OUT_DIR/coupling_sample_rows.jsonl" || true
  echo "coupling_jsonl=$OUT_DIR/coupling_rows.jsonl"
  echo "bucket_jsonl=$OUT_DIR/coupling_bucket_rows.jsonl"
  echo "pair_jsonl=$OUT_DIR/coupling_pair_rows.jsonl"
  echo "lag_jsonl=$OUT_DIR/coupling_lag_rows.jsonl"
  echo "sample_jsonl=$OUT_DIR/coupling_sample_rows.jsonl"
fi
