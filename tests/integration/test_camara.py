"""
Test de integración: verificar que la cámara USB funciona correctamente.

Requiere hardware. Ejecutar en la Pi:
    pytest tests/integration/test_camara.py -m hardware -v

El frame capturado se guarda en /tmp/test_frame.jpg para inspección visual:
    scp malber@192.168.0.15:/tmp/test_frame.jpg ~/Desktop/
"""

import cv2
import numpy as np
import pytest

from navegacion_aruco.vision.camara import Camara

pytestmark = pytest.mark.hardware


def test_camara_abre():
    """La cámara debe abrirse sin error."""
    with Camara() as cam:
        assert cam.ancho >= 320
        assert cam.alto >= 240
        assert cam.fps > 0


def test_camara_lee_frame_valido():
    """El frame debe ser un array numpy de shape (alto, ancho, 3)."""
    with Camara() as cam:
        frame = cam.leer()
        assert isinstance(frame, np.ndarray)
        assert frame.ndim == 3
        assert frame.shape[2] == 3
        assert frame.shape[:2] == (cam.alto, cam.ancho)


def test_frame_no_es_negro():
    """El frame no debe ser completamente negro."""
    with Camara() as cam:
        for _ in range(5):
            frame = cam.leer()
        brillo_medio = np.mean(frame)
        assert brillo_medio > 5.0, f"Frame parece negro (brillo: {brillo_medio:.1f})"


def test_guardar_frame_muestra():
    """Guarda un frame para inspección visual desde la laptop."""
    with Camara() as cam:
        frame = cam.leer()
        ruta = "/tmp/test_frame.jpg"
        cv2.imwrite(ruta, frame)
    print(f"\nFrame guardado en {ruta}")
    print("Para ver: scp malber@192.168.0.15:/tmp/test_frame.jpg ~/Desktop/")
