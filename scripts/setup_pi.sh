#!/usr/bin/env bash
# =============================================================================
# setup_pi.sh — Configura el entorno de la Raspberry Pi para navegacion-aruco
#
# Uso:
#   bash scripts/setup_pi.sh
#
# Ejecutar una vez después de clonar el repositorio en la Pi.
# =============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "================================================="
echo " navegacion-aruco: Setup en Raspberry Pi"
echo " Directorio: $REPO_DIR"
echo "================================================="

# ── Dependencias del sistema ──────────────────────────────────────────────────
echo ""
echo "[1/4] Actualizando lista de paquetes..."
sudo apt-get update -qq

echo "[2/4] Instalando dependencias del sistema..."
sudo apt-get install -y -qq \
    python3-pip \
    python3-venv \
    git \
    tmux

echo "Habilitando pigpiod..."
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# ── Entorno virtual Python ────────────────────────────────────────────────────
echo "[3/4] Creando entorno virtual..."
cd "$REPO_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv --system-site-packages
    echo "  Entorno virtual creado en .venv/"
else
    echo "  Entorno virtual ya existe, omitiendo creación"
fi

# ── Dependencias Python ───────────────────────────────────────────────────────
echo "[4/4] Instalando dependencias Python..."
source .venv/bin/activate
pip install -r requirements-pi.txt --quiet

# ── Verificación ──────────────────────────────────────────────────────────────
echo ""
echo "================================================="
echo " Verificación"
echo "================================================="

python3 -c "
import cv2
import numpy
import navegacion_aruco
print(f'  OpenCV  : {cv2.__version__}')
print(f'  NumPy   : {numpy.__version__}')
print(f'  Paquete : navegacion_aruco {navegacion_aruco.__version__}')
"

echo ""
echo "✓ Setup completo."
echo ""
echo "Para activar el entorno virtual:"
echo "  source .venv/bin/activate"
echo ""
echo "Para verificar hardware:"
echo "  pytest tests/integration/ -m hardware -v"
