#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/dashboard"

if [ ! -d node_modules ]; then
  echo "Installing dependencies..."
  pnpm install
fi

if [ ! -d dist ] || [ "$(find src -newer dist/index.html 2>/dev/null | head -1)" ]; then
  echo "Building dashboard..."
  pnpm build
fi

echo "Starting Meta-Pipe Dashboard on http://localhost:6666"
exec pnpm serve
