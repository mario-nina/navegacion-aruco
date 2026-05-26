"""
Abstracción de la cámara USB.

Encapsula la apertura, configuración y lectura de frames de OpenCV.

Uso:
    with Camara() as cam:
        frame = cam.read()
"""

import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ErrorCamara(Exception):
    """Error irrecuperable de cámara."""


class Camara:
    def __init__(
        self,
        indice: int = 0,
        ancho: int = 640,
        alto: int = 480,
        fps: int = 30,
    ) -> None:
        self._cap = cv2.VideoCapture(indice)
        if not self._cap.isOpened():
            raise ErrorCamara(f"No se pudo abrir la cámara (índice {indice})")

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)
        self._cap.set(cv2.CAP_PROP_FPS, fps)

        self.ancho = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.alto = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self._cap.get(cv2.CAP_PROP_FPS)

        logger.info(
            "Cámara abierta: %dx%d @ %.1f fps", self.ancho, self.alto, self.fps
        )

    def leer(self) -> np.ndarray:
        """Lee el frame más reciente. Lanza ErrorCamara si falla."""
        ret, frame = self._cap.read()
        if not ret or frame is None:
            raise ErrorCamara("Fallo al leer frame de la cámara")
        return frame

    def liberar(self) -> None:
        """Libera el recurso de la cámara."""
        if self._cap.isOpened():
            self._cap.release()
            logger.debug("Cámara liberada")

    def __enter__(self) -> "Camara":
        return self

    def __exit__(self, *_) -> None:
        self.liberar()

