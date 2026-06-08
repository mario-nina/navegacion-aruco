"""
Pipeline de visión de alto nivel.

Integra Camara + Detector + EstimadorPose en una interfaz limpia
para el módulo de navegación.

El módulo de navegación no necesita conocer OpenCV ni la calibración —
solo llama pipeline.observar(id) y recibe distancia y ángulo.

Uso:
    with Pipeline() as pipeline:
        observacion = pipeline.observar(0)
        if observacion:
            print(f"Dist: {observacion.distancia_cm}cm")
            print(f"Angulo: {observacion.angulo_deg}°")
"""

import logging
from dataclasses import dataclass
from typing import Optional

from navegacion_aruco.vision.camara import Camara
from navegacion_aruco.vision.detector import Detector
from navegacion_aruco.vision.estimador_pose import EstimadorPose

logger = logging.getLogger(__name__)

TAMANO_MARCADOR_MM = 39.0


@dataclass
class ObservacionMarcador:
    """Observación de un marcador: ID, distancia y dirección."""

    id: int
    distancia_cm: float
    angulo_deg: float


class Pipeline:
    """
    Pipeline de visión completo.

    Encapsula la cámara, el detector ArUco y el estimador de pose
    en una interfaz de alto nivel para el módulo de navegación.
    """

    def __init__(self, tamano_marcador_mm: float = TAMANO_MARCADOR_MM) -> None:
        self._camara = Camara()
        self._detector = Detector()
        self._estimador = EstimadorPose(tamano_marcador_mm)
        logger.info("Pipeline de visión inicializado")

    def observar(self, id_objetivo: int) -> Optional[ObservacionMarcador]:
        """
        Captura un frame y busca el marcador con id_objetivo.

        Returns:
            ObservacionMarcador si el marcador es visible, None si no.
        """
        frame = self._camara.leer()
        marcador = self._detector.detectar_por_id(frame, id_objetivo)

        if marcador is None:
            return None

        try:
            pose = self._estimador.estimar(marcador)
        except RuntimeError as e:
            logger.warning("Error estimando pose para ID=%d: %s", id_objetivo, e)
            return None

        logger.debug(
            "Observacion ID=%d  dist=%.1fcm  angulo=%+.1f°",
            id_objetivo,
            pose.distancia_cm,
            pose.angulo_deg,
        )

        return ObservacionMarcador(
            id=id_objetivo,
            distancia_cm=pose.distancia_cm,
            angulo_deg=pose.angulo_deg,
        )

    def observar_todos(self) -> list[ObservacionMarcador]:
        """
        Captura un frame y retorna observaciones de todos los
        marcadores visibles.
        """
        frame = self._camara.leer()
        marcadores = self._detector.detectar(frame)
        resultados = []

        for marcador in marcadores:
            try:
                pose = self._estimador.estimar(marcador)
                resultados.append(
                    ObservacionMarcador(
                        id=marcador.id,
                        distancia_cm=pose.distancia_cm,
                        angulo_deg=pose.angulo_deg,
                    )
                )
            except RuntimeError as e:
                logger.warning("Error estimando pose para ID=%d: %s", marcador.id, e)

        return resultados

    def liberar(self) -> None:
        self._camara.liberar()
        logger.info("Pipeline liberado")

    def __enter__(self) -> "Pipeline":
        return self

    def __exit__(self, *_) -> None:
        self.liberar()
