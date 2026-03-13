#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONTRACTS_DIR="$ROOT_DIR/contracts"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is not available. Install Node.js to run schema validation."
  exit 1
fi

validate() {
  local schema="$1"
  local data="$2"
  echo "Validating $data against $schema"
  npx --yes ajv-cli@5 validate --strict=false -s "$schema" -d "$data"
}

validate "$CONTRACTS_DIR/task-charter.schema.json" "$CONTRACTS_DIR/examples/task-charter.example.json"
validate "$CONTRACTS_DIR/handoff-packet.schema.json" "$CONTRACTS_DIR/examples/handoff-packet.example.json"
validate "$CONTRACTS_DIR/result-packet.schema.json" "$CONTRACTS_DIR/examples/result-packet-cipher.example.json"
validate "$CONTRACTS_DIR/result-packet.schema.json" "$CONTRACTS_DIR/examples/result-packet-clawver.example.json"
validate "$CONTRACTS_DIR/session-record.schema.json" "$CONTRACTS_DIR/examples/session-record.example.json"
validate "$CONTRACTS_DIR/knowledge-card.schema.json" "$CONTRACTS_DIR/examples/knowledge-card.example.json"
validate "$CONTRACTS_DIR/ambiguity-report.schema.json" "$CONTRACTS_DIR/examples/ambiguity-report.example.json"

echo "All contract examples validated successfully."
