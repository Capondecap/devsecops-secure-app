#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "Building containers..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Running containers:"
docker-compose ps
