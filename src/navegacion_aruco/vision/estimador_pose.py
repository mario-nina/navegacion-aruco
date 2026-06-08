"""
Estimación de posición y ángulo relativo al marcador ArUco.

Transforma la posición del marcador de píxeles a coordenadas
físicas en mm usando los parámetros de calibración de la cámara.

Coordenadas de salida:
    distancia_cm  → distancia real al marcador en centímetros
    angulo_deg    → ángulo horizontal en grados
                    0  = marcador centrado (frente al robot)
                    +  = marcador a la derecha
                    -  = marcador a la izquierda
    tvec          → vector de traslación [x, y, z] en mm
"""

import logging
import math
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from navegacion_aruco.vision.detector import MarcadorDetectado

logger = logging.getLogger(__name__)

CALIBRACION_PATH = (
    Path(__file__).parent.parent.parent.parent / "config" / "camera_calibration.npz"
)
TAMANO_MARCADOR_MM = 80.0


@dataclass
class ResultadoPose:
    """Resultado de la estimación de pose para un marcador."""

    distancia_cm: float
    angulo_deg: float
    tvec: np.ndarray  # [x, y, z] en mm
    rvec: np.ndarray


class ErrorCalibracion(Exception):
    """No se encontró el archivo de calibración."""


class EstimadorPose:
    def __init__(self, tamano_marcador_mm: float = TAMANO_MARCADOR_MM) -> None:
        """
        Args:
            tamano_marcador_mm: tamaño del lado del marcador impreso en mm.
                                Medir con regla sobre el papel impreso.
        """
        ruta = CALIBRACION_PATH.resolve()
        if not ruta.exists():
            raise ErrorCalibracion(
                f"Archivo de calibración no encontrado: {ruta}\n"
                "Ejecutar primero: python3 calibracion/calibrar_camara.py"
            )

        datos = np.load(str(ruta))
        self._matriz_camara = datos["camera_matrix"]
        self._dist_coeffs = datos["dist_coeffs"]
        self._tamano = tamano_marcador_mm

        # Esquinas 3D del marcador en su sistema local (z=0, origen en centro)
        mitad = tamano_marcador_mm / 2.0
        self._puntos_objeto = np.array(
            [
                [-mitad, mitad, 0.0],
                [mitad, mitad, 0.0],
                [mitad, -mitad, 0.0],
                [-mitad, -mitad, 0.0],
            ],
            dtype=np.float32,
        )

        logger.info("EstimadorPose listo (tamano_marcador=%.1f mm)", tamano_marcador_mm)

    def estimar(self, marcador: MarcadorDetectado) -> ResultadoPose:
        """
        Calcula distancia y ángulo al marcador detectado.

        Args:
            marcador: MarcadorDetectado del Detector

        Returns:
            ResultadoPose con distancia_cm y angulo_deg
        """
        puntos_imagen = marcador.esquinas.astype(np.float32)

        exito, rvec, tvec = cv2.solvePnP(
            self._puntos_objeto,
            puntos_imagen,
            self._matriz_camara,
            self._dist_coeffs,
            flags=cv2.SOLVEPNP_IPPE_SQUARE,
        )

        if not exito:
            raise RuntimeError(f"solvePnP falló para marcador ID={marcador.id}")

        tvec_flat = tvec.flatten()
        x_mm = float(tvec_flat[0])
        z_mm = float(tvec_flat[2])

        distancia_cm = round(float(np.linalg.norm(tvec_flat)) / 10.0, 1)
        angulo_deg = round(math.degrees(math.atan2(x_mm, z_mm)), 2)

        logger.debug(
            "Marcador ID=%d  dist=%.1f cm  angulo=%+.1f°",
            marcador.id,
            distancia_cm,
            angulo_deg,
        )

        return ResultadoPose(
            distancia_cm=distancia_cm,
            angulo_deg=angulo_deg,
            tvec=tvec_flat,
            rvec=rvec.flatten(),
        )
