#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_path=""
out_dir=""
lean="1"

usage() {
  cat <<EOF
Usage: $0 --log workerNN.log [options]

Create persistent artifacts for a verified Pomerance worker hit:
  - triple.txt
  - verification.txt
  - worker.log
  - worker-tail.txt
  - pomerance_<p>.lean, unless --no-lean is supplied

Options:
  --log PATH       Worker log containing a Verified: PASS triple
  --out-dir DIR    Output artifact directory
  --no-lean        Skip Lean certificate generation
  -h, --help       Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --log) log_path="$2"; shift 2 ;;
    --out-dir) out_dir="$2"; shift 2 ;;
    --no-lean) lean="0"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$log_path" ]]; then
  usage >&2
  exit 1
fi

if [[ ! -f "$log_path" ]]; then
  echo "Worker log not found: $log_path" >&2
  exit 1
fi

triple="$(
  awk '
    /^[[:space:]]*[0-9]+[[:space:]]+[0-9]+[[:space:]]+[0-9]+[[:space:]]*$/ { last=$0 }
    /Verified: PASS/ { print last; found=1; exit }
    END { if (!found) exit 2 }
  ' "$log_path"
)" || {
  echo "Could not extract a triple before Verified: PASS in $log_path" >&2
  exit 1
}

read -r p A x0 <<<"$triple"

if [[ -z "$out_dir" ]]; then
  out_dir="$(dirname "$log_path")/hit-${p}-$(basename "$log_path" .log)"
fi

mkdir -p "$out_dir"

printf "%s %s %s\n" "$p" "$A" "$x0" > "$out_dir/triple.txt"
cp "$log_path" "$out_dir/worker.log"
tail -n 120 "$log_path" > "$out_dir/worker-tail.txt"

verify_args=(--log "$log_path")
if [[ "$lean" == "1" ]]; then
  verify_args+=(--lean-out "$out_dir/pomerance_${p}.lean")
fi

{
  date
  printf "source_worker_log=%s\n" "$log_path"
  printf "artifact_dir=%s\n" "$out_dir"
  printf "triple=%s %s %s\n\n" "$p" "$A" "$x0"
  "$repo_root/scripts/verify_pomerance_triple.py" "${verify_args[@]}"
} | tee "$out_dir/verification.txt"

cat > "$out_dir/README.md" <<EOF
# Pomerance Hit Artifact

Triple:

\`\`\`text
$p $A $x0
\`\`\`

Files:

- \`triple.txt\`: one-line triple for DANGER3 \`vpp.py\`.
- \`verification.txt\`: independent replay, primality check, and DANGER3 verifier transcript.
- \`worker.log\`: full worker log copied from the run directory.
- \`worker-tail.txt\`: final worker log tail.
EOF

if [[ "$lean" == "1" ]]; then
  cat >> "$out_dir/README.md" <<EOF
- \`pomerance_${p}.lean\`: generated Lean certificate artifact.
EOF
fi

printf "finalized_hit_dir=%s\n" "$out_dir"
