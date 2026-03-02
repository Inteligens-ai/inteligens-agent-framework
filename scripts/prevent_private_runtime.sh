#!/usr/bin/env bash
set -e

echo "🔍 Checking for private runtime leaks..."

BLOCKED_FILES=(
  ".agents/runtime/products.json"
  ".agents/runtime/hardware_profile.json"
)

for f in "${BLOCKED_FILES[@]}"; do
  if git diff --cached --name-only | grep -q "^$f$"; then
    echo "❌ BLOCKED: Attempt to commit private runtime file: $f"
    echo "👉 Use *.example.json for public repo."
    exit 1
  fi
done

echo "✅ Runtime check passed."