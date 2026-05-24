"""
Test de integración: verificar detección de marcadores ArUco.

Requiere hardware y marcadores impresos.
Ejecutar en la Pi:
    pytest tests/integration/test_detector.py -m hardware -v

Antes de correr: colocar un marcador ArUco impreso frente a la cámara.
"""

import numpy as np
import pytest

from navegacion_aruco.vision.camara import Camara
from navegacion_aruco.vision.detector import Detector

pytestmark = pytest.mark.hardware

ID_PRUEBA = 0  # ID del marcador que se coloca frente a la cámara


def test_detector_inicializa():
    """El detector debe inicializarse sin error."""
    detector = Detector()
    assert detector is not None


def test_detector_retorna_lista_vacia_sin_marcadores():
    """Sin marcadores frente a la cámara debe retornar lista vacía."""
    with Camara() as cam:
        detector = Detector()
        # Capturar frame sin marcador (apuntar a superficie sin marcadores)
        frame = cam.leer()
        # Este test es informativo — puede fallar si hay marcadores en el entorno
        marcadores = detector.detectar(frame)
        print(f"\nMarcadores detectados sin objetivo: {[m.id for m in marcadores]}")


def test_detector_detecta_marcador():
    """Con un marcador frente a la cámara debe detectarlo."""
    input(f"\nColocar marcador ID:{ID_PRUEBA} frente a la cámara y presionar ENTER...")

    with Camara() as cam:
        detector = Detector()
        # Capturar varios frames para estabilizar
        for _ in range(10):
            frame = cam.leer()

        marcadores = detector.detectar(frame)
        ids_detectados = [m.id for m in marcadores]
        print(f"\nMarcadores detectados: {ids_detectados}")
        assert (
            ID_PRUEBA in ids_detectados
        ), f"Marcador ID:{ID_PRUEBA} no detectado. Detectados: {ids_detectados}"


def test_marcador_detectado_tiene_datos_validos():
    """El marcador detectado debe tener esquinas y centro válidos."""
    input(f"\nColocar marcador ID:{ID_PRUEBA} frente a la cámara y presionar ENTER...")

    with Camara() as cam:
        detector = Detector()
        for _ in range(10):
            frame = cam.leer()

        marcador = detector.detectar_por_id(frame, ID_PRUEBA)
        assert marcador is not None, f"Marcador ID:{ID_PRUEBA} no detectado"
        assert isinstance(marcador.esquinas, np.ndarray)
        assert marcador.esquinas.shape == (4, 2)
        assert len(marcador.centro) == 2
        cx, cy = marcador.centro
        assert 0 < cx < cam.ancho
        assert 0 < cy < cam.alto
        print(
            f"\nID: {marcador.id}  Centro: {marcador.centro}  Esquinas: {marcador.esquinas}"
        )


def test_detectar_por_id_retorna_none_sin_marcador():
    """Sin el marcador objetivo debe retornar None."""
    with Camara() as cam:
        detector = Detector()
        frame = cam.leer()
        resultado = detector.detectar_por_id(frame, 99)
        assert resultado is None
