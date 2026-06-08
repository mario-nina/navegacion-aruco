#!/usr/bin/env bash
# =============================================================================
# send_command.sh — Envía comando de navegación al robot desde la laptop
#
# Uso:
#   bash scripts/send_command.sh <marker_id>
#
# Ejemplo:
#   bash scripts/send_command.sh 2
# =============================================================================

set -euo pipefail

MARKER_ID="${1:?'Uso: send_command.sh <marker_id>'}"
PI_HOST="malber@marionina.local"
PI_DIR="~/navegacion-aruco"

echo "Enviando comando al robot..."
echo "  Destino: marcador ID $MARKER_ID"
echo "  Host: $PI_HOST"
echo ""

ssh "$PI_HOST" "cd $PI_DIR && source .venv/bin/activate && python3 scripts/run_robot.py --id $MARKER_ID"
