"""
Detección e identificación de marcadores ArUco en frames de video.

Usa el diccionario DICT_4X4_50: 50 marcadores únicos de cuadrícula 4×4.
Elegido por su velocidad de detección y robustez a distancias cortas.

Uso:
    detector = Detector()
    marcadores = detector.detectar(frame)
    for m in marcadores:
        print(m.id, m.centro)
"""

import logging
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

DICCIONARIO_ARUCO = cv2.aruco.DICT_4X4_50


@dataclass
class MarcadorDetectado:
    """Marcador ArUco detectado en un frame."""

    id: int
    esquinas: np.ndarray  # shape (4, 2), coordenadas en píxeles
    centro: tuple[int, int]  # (x, y) centro del marcador en la imagen


class Detector:
    """Detecta e identifica marcadores ArUco en frames de la cámara."""

    def __init__(self) -> None:
        self._diccionario = cv2.aruco.getPredefinedDictionary(DICCIONARIO_ARUCO)
        self._parametros = cv2.aruco.DetectorParameters()
        self._detector = cv2.aruco.ArucoDetector(self._diccionario, self._parametros)
        logger.debug("Detector inicializado (DICT_4X4_50)")

    def detectar(self, frame: np.ndarray) -> list[MarcadorDetectado]:
        """
        Detecta todos los marcadores ArUco visibles en el frame.

        Args:
            frame: imagen BGR capturada por Camara.leer()

        Returns:
            Lista de MarcadorDetectado. Vacía si no hay marcadores.
        """
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        esquinas_lista, ids, _ = self._detector.detectMarkers(gris)

        if ids is None:
            logger.debug("Sin marcadores detectados")
            return []

        resultados = []
        for esquinas, marker_id in zip(esquinas_lista, ids.flatten()):
            pts = esquinas[0].astype(int)
            cx = int(np.mean(pts[:, 0]))
            cy = int(np.mean(pts[:, 1]))
            resultados.append(
                MarcadorDetectado(
                    id=int(marker_id),
                    esquinas=pts,
                    centro=(cx, cy),
                )
            )

        logger.debug(
            "Detectados %d marcadores: %s",
            len(resultados),
            [m.id for m in resultados],
        )
        return resultados

    def detectar_por_id(
        self, frame: np.ndarray, id_objetivo: int
    ) -> Optional[MarcadorDetectado]:
        """
        Busca un marcador específico por ID.

        Args:
            frame: imagen BGR capturada por Camara.leer()
            id_objetivo: ID del marcador a buscar

        Returns:
            MarcadorDetectado si está visible, None si no.
        """
        for marcador in self.detectar(frame):
            if marcador.id == id_objetivo:
                return marcador
        return None
