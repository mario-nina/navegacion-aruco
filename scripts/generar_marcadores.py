"""
Genera una hoja de marcadores ArUco lista para imprimir en hoja carta.

Uso:
    python3 scripts/generar_marcadores.py

Genera en marcadores/:
  - marcador_XX.png     → cada marcador individual
  - hoja_marcadores.png → todos en una hoja carta (2x3)

Imprimir al 100% de escala, sin ajuste de página.
Recortar por las líneas guía dejando el borde blanco.
"""

from pathlib import Path

import cv2
import numpy as np

DICCIONARIO = cv2.aruco.DICT_4X4_50
IDS = [0, 1, 2, 3, 4, 5]
DIRECTORIO = Path(__file__).parent.parent / "marcadores"

# Hoja carta a 300 DPI: 8.5" x 11" = 2550 x 3300 px
HOJA_ANCHO = 2550
HOJA_ALTO = 3300
COLUMNAS = 2
FILAS = 3
MARGEN = 150
ESPACIO = 100
BORDE_BLANCO = 180


def generar_marcador_individual(aruco_dict, marker_id: int, tamano: int) -> np.ndarray:
    """Genera imagen del marcador con borde blanco."""
    patron = cv2.aruco.generateImageMarker(aruco_dict, marker_id, tamano)
    return cv2.copyMakeBorder(
        patron,
        BORDE_BLANCO,
        BORDE_BLANCO,
        BORDE_BLANCO,
        BORDE_BLANCO,
        cv2.BORDER_CONSTANT,
        value=255,
    )


def dibujar_esquinas_corte(hoja: np.ndarray, x: int, y: int, tam: int) -> None:
    """Dibuja marcas de corte en las 4 esquinas del marcador."""
    largo = 60
    grosor = 3
    color = 150

    esquinas = [
        (x, y),
        (x + tam, y),
        (x, y + tam),
        (x + tam, y + tam),
    ]
    offsets = [
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1),
    ]

    for (ex, ey), (ox, oy) in zip(esquinas, offsets):
        cv2.line(hoja, (ex, ey), (ex + ox * largo, ey), color, grosor)
        cv2.line(hoja, (ex, ey), (ex, ey + oy * largo), color, grosor)


def main() -> None:
    DIRECTORIO.mkdir(exist_ok=True)
    aruco_dict = cv2.aruco.getPredefinedDictionary(DICCIONARIO)

    celda_ancho = (HOJA_ANCHO - MARGEN * 2 - ESPACIO * (COLUMNAS - 1)) // COLUMNAS
    celda_alto = (HOJA_ALTO - MARGEN * 2 - ESPACIO * (FILAS - 1) - FILAS * 80) // FILAS
    celda = min(celda_ancho, celda_alto)
    tamano_patron = celda - BORDE_BLANCO * 2

    hoja = np.ones((HOJA_ALTO, HOJA_ANCHO), dtype=np.uint8) * 255

    for i, marker_id in enumerate(IDS):
        fila = i // COLUMNAS
        col = i % COLUMNAS

        x = MARGEN + col * (celda + ESPACIO)
        y = MARGEN + fila * (celda + ESPACIO + 80)

        marcador = generar_marcador_individual(aruco_dict, marker_id, tamano_patron)
        hoja[y : y + celda, x : x + celda] = marcador

        dibujar_esquinas_corte(hoja, x, y, celda)
        cv2.rectangle(hoja, (x, y), (x + celda, y + celda), 180, 3)

        font = cv2.FONT_HERSHEY_SIMPLEX
        texto = f"ID: {marker_id}"
        (tw, _), _ = cv2.getTextSize(texto, font, 1.8, 3)
        cv2.putText(
            hoja, texto, (x + (celda - tw) // 2, y + celda + 55), font, 1.8, 0, 3
        )

        ruta = DIRECTORIO / f"marcador_{marker_id:02d}.png"
        cv2.imwrite(str(ruta), marcador)
        print(f"Generado: {ruta.name}")

    ruta_hoja = DIRECTORIO / "hoja_marcadores.png"
    cv2.imwrite(str(ruta_hoja), hoja)
    print(f"\nHoja completa: {ruta_hoja.name}")
    print(f"Tamaño del patrón en imagen: {tamano_patron}px")
    print("Medir con regla después de imprimir para obtener el tamaño real en mm.")


if __name__ == "__main__":
    main()
