"""
Configuración global del proyecto.

Las variables de entorno se leen con valores por defecto seguros.
En desarrollo: definir en .env (laptop).
En la Pi:      exportar en la terminal antes de correr el robot.
"""

import logging
import os

# ── Variables de entorno ──────────────────────────────────────────────────────

ROBOT_LOG_LEVEL = os.getenv("ROBOT_LOG_LEVEL", "DEBUG")
MARKER_SIZE_MM = float(os.getenv("MARKER_SIZE_MM", "80.0"))
TARGET_FPS = int(os.getenv("TARGET_FPS", "30"))
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))

# ── Constantes físicas del robot ──────────────────────────────────────────────

# Distancia en cm para considerar que el robot llegó al marcador
ARRIVAL_THRESHOLD_CM = 15.0

# Ángulo en grados dentro del cual no se corrige la dirección
ANGLE_DEAD_ZONE_DEG = 3.0

# Velocidad de rotación durante la búsqueda del marcador (0.0 - 1.0)
SEARCH_ROTATION_SPEED = 0.25

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=getattr(logging, ROBOT_LOG_LEVEL.upper(), logging.DEBUG),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
