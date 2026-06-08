"""
Captura imágenes del tablero de ajedrez para calibración de la cámara.

Uso (desde la laptop con la cámara conectada):
    python3 calibracion/capturar_imagenes.py

Instrucciones:
    - Montar la cámara en su posición final en el robot
    - Sostener el tablero frente a la cámara en distintas posiciones
    - ESPACIO para capturar cuando el tablero está detectado
    - Q para terminar
    - Objetivo: 20-25 imágenes válidas

Variedad recomendada:
    - Distintas distancias: 20cm, 40cm, 60cm
    - Distintos ángulos: izquierda, centro, derecha
    - Distintas inclinaciones: recto, ~30° hacia cada lado
    - Tablero en distintas zonas del frame: esquinas y centro
"""

import sys
from pathlib import Path

import cv2

PATRON = (9, 6)  # esquinas internas del tablero (columnas x filas)
CAMARA_INDEX = 0
DIRECTORIO = Path(__file__).parent / "imagenes"
MIN_IMAGENES = 20


def main() -> None:
    DIRECTORIO.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(CAMARA_INDEX)
    if not cap.isOpened():
        print("ERROR: No se pudo abrir la cámara")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print(f"Cámara: {int(cap.get(3))}x{int(cap.get(4))}")
    print(f"Guardando en: {DIRECTORIO}")
    print(f"Objetivo: {MIN_IMAGENES} imágenes válidas")
    print("\nControles:")
    print("  ESPACIO → capturar (solo si el tablero es detectado)")
    print("  Q       → terminar\n")

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        encontrado, corners = cv2.findChessboardCorners(gray, PATRON, None)

        display = frame.copy()

        if encontrado:
            cv2.drawChessboardCorners(display, PATRON, corners, encontrado)
            estado = f"DETECTADO [{count}/{MIN_IMAGENES}] — ESPACIO para capturar"
            color = (0, 200, 0)
        else:
            estado = f"No detectado [{count}/{MIN_IMAGENES}] — reposicionar tablero"
            color = (0, 0, 200)

        cv2.putText(display, estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Calibracion - tablero de ajedrez", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord(" ") and encontrado:
            ruta = DIRECTORIO / f"calib_{count:04d}.jpg"
            cv2.imwrite(str(ruta), frame)
            count += 1
            print(f"  [{count:02d}] Guardada: {ruta.name}")

    cap.release()
    cv2.destroyAllWindows()

    print(f"\nTotal capturadas: {count}")
    if count < MIN_IMAGENES:
        print(f"ADVERTENCIA: se recomiendan al menos {MIN_IMAGENES} imágenes")
    else:
        print("Listo. Ejecutar: python3 calibracion/calibrar_camara.py")


if __name__ == "__main__":
    main()
