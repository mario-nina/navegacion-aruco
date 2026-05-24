"""
Genera imágenes PNG de marcadores ArUco para imprimir.

Uso:
    python3 scripts/generar_marcadores.py

Los marcadores se guardan en marcadores/
Imprimir al 100% de escala, sin ajuste de página.
"""

from pathlib import Path

import cv2

DICCIONARIO = cv2.aruco.DICT_4X4_50
IDS = [0, 1, 2, 3, 4, 5]
TAMANO_PX = 300
BORDE_PX = 50
DIRECTORIO = Path(__file__).parent.parent / "marcadores"


def generar_marcadores() -> None:
    DIRECTORIO.mkdir(exist_ok=True)
    aruco_dict = cv2.aruco.getPredefinedDictionary(DICCIONARIO)

    for marker_id in IDS:
        imagen = cv2.aruco.generateImageMarker(aruco_dict, marker_id, TAMANO_PX)

        # Agregar borde blanco para mejor detección
        imagen_con_borde = cv2.copyMakeBorder(
            imagen,
            BORDE_PX,
            BORDE_PX,
            BORDE_PX,
            BORDE_PX,
            cv2.BORDER_CONSTANT,
            value=255,
        )

        ruta = DIRECTORIO / f"marcador_{marker_id:02d}.png"
        cv2.imwrite(str(ruta), imagen_con_borde)
        print(f"Generado: {ruta.name}")

    print(f"\nTotal: {len(IDS)} marcadores en {DIRECTORIO}")
    print("Imprimir al 100% de escala, sin ajuste de página.")


if __name__ == "__main__":
    generar_marcadores()
