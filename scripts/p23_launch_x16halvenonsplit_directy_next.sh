#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_path="/tmp/pomerance_directy_next_current"
monitor="0"
preflight="0"
pass_args=()

usage() {
  cat <<EOF
Usage: $0 [options]

Build and launch an explicit direct-y X1(16) nonsplit follow-on shard.

This wrapper does not change the default p23 launcher. It compiles the current
pomerance.c direct-y kernel, records the binary hash, then delegates to:

  scripts/p23_launch_x16halvenonsplit_shard.sh --binary <built-binary>

By default it uses --no-monitor and the underlying guarded launcher refuses to
start while existing p23 pomerance workers are running.

Options:
  --build-path PATH       Binary path to build (default: $build_path)
  --monitor               Use the launcher monitor loop instead of --no-monitor
  --preflight             Build and run launcher preflight only
  --seed-base N           Passed through to the guarded launcher
  --seed-step N           Passed through to the guarded launcher
  --workers N             Passed through to the guarded launcher
  --trials-per-worker N   Passed through to the guarded launcher
  --force                 Passed through; intentionally oversubscribes if active workers exist
  -h, --help              Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build-path) build_path="$2"; shift 2 ;;
    --monitor) monitor="1"; shift ;;
    --preflight) preflight="1"; pass_args+=("$1"); shift ;;
    -h|--help) usage; exit 0 ;;
    *) pass_args+=("$1"); shift ;;
  esac
done

mkdir -p "$(dirname "$build_path")"
gcc -O3 -Wall -Wextra -o "$build_path" "$repo_root/pomerance.c" -lm
chmod +x "$build_path"
binary_sha256="$(shasum -a 256 "$build_path" | awk '{print $1}')"

echo "directy_build_path=$build_path"
echo "directy_binary_sha256=$binary_sha256"

launcher_args=(--binary "$build_path")
if [[ "$preflight" != "1" && "$monitor" != "1" ]]; then
  launcher_args+=(--no-monitor)
fi
launcher_args+=("${pass_args[@]}")

exec "$repo_root/scripts/p23_launch_x16halvenonsplit_shard.sh" "${launcher_args[@]}"
