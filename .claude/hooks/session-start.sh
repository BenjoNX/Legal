#!/bin/bash
# Hook de démarrage : s'assure que l'environnement Python est prêt
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip
    "$VENV_DIR/bin/pip" install --quiet -e "$SCRIPT_DIR"
fi
