"""
Genera el tablero de ajedrez para calibración de la cámara.

Uso:
    python3 calibracion/generar_tablero.py

El archivo resultante se guarda en calibracion/tablero_calibracion.png
Imprimir al 100% de escala, sin ajuste de página ni 'encajar en hoja'.
Medir con regla el tamaño real de un cuadro en mm y anotar en SQUARE_SIZE_MM.
"""

import cv2
import numpy as np
from pathlib import Path

CUADROS_X = 10
CUADROS_Y = 7
TAM_CUADRO = 100  # píxeles por cuadro en la imagen generada
SALIDA = Path(__file__).parent / "tablero_calibracion.png"


def generar_tablero() -> None:
    ancho = CUADROS_X * TAM_CUADRO
    alto = CUADROS_Y * TAM_CUADRO

    tablero = np.zeros((alto, ancho), dtype=np.uint8)

    for y in range(CUADROS_Y):
        for x in range(CUADROS_X):
            if (x + y) % 2 == 0:
                tablero[
                    y * TAM_CUADRO : (y + 1) * TAM_CUADRO,
                    x * TAM_CUADRO : (x + 1) * TAM_CUADRO,
                ] = 255

    cv2.imwrite(str(SALIDA), tablero)
    print(f"Tablero guardado en: {SALIDA}")
    print(f"Cuadros: {CUADROS_X} x {CUADROS_Y}")
    print("Imprimir al 100% de escala, sin ajuste de página.")
    print("Medir un cuadro con regla y anotar el tamaño en mm.")


if __name__ == "__main__":
    generar_tablero()
