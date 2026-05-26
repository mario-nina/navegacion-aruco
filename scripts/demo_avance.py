"""
Demo avance docente: detección ArUco y respuesta básica de motores.

El robot activa los motores según la posición del marcador ArUco
detectado en el frame de la cámara.

Comportamiento:
    - Marcador centrado   → adelante
    - Marcador a la izq  → girar izquierda
    - Marcador a la der  → girar derecha
    - Sin marcador        → detenido

Uso (en la Pi, con chasis elevado):
    python3 scripts/demo_avance.py --id 0

    python3 scripts/demo_avance.py --id 0 --zona-muerta 80
"""

import argparse
import time

from navegacion_aruco.control.motor_driver import MotorDriver
from navegacion_aruco.vision.camara import Camara
from navegacion_aruco.vision.detector import Detector

# Configuración por defecto
ANCHO_FRAME = 640
ZONA_MUERTA_PX = 60   # ±píxeles desde el centro considerados "centrado"
VELOCIDAD = 0.7


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demo: detección ArUco y respuesta básica de motores"
    )
    parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="ID del marcador ArUco a seguir (0-49)",
    )
    parser.add_argument(
        "--zona-muerta",
        type=int,
        default=ZONA_MUERTA_PX,
        help=f"Zona muerta en píxeles (default: {ZONA_MUERTA_PX})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    centro_frame = ANCHO_FRAME // 2
    zona = args.zona_muerta

    print(f"Buscando marcador ID: {args.id}")
    print(f"Zona muerta: ±{zona}px desde el centro ({centro_frame}px)")
    print("Ctrl+C para detener\n")

    with Camara() as cam, MotorDriver() as motores:
        detector = Detector()
        time.sleep(1.0)  # esperar que la cámara se estabilice

        while True:
            frame = cam.leer()
            marcador = detector.detectar_por_id(frame, args.id)

            if marcador is None:
                motores.detener()
                print("\rSin marcador — detenido          ", end="")
                continue

            cx, _ = marcador.centro
            error = cx - centro_frame

            if abs(error) <= zona:
                motores.adelante(VELOCIDAD)
                estado = f"ADELANTE  (centro={cx}px, error={error:+d}px)"
            elif error < 0:
                motores.girar_izquierda(VELOCIDAD)
                estado = f"IZQUIERDA (centro={cx}px, error={error:+d}px)"
            else:
                motores.girar_derecha(VELOCIDAD)
                estado = f"DERECHA   (centro={cx}px, error={error:+d}px)"

            print(f"\r{estado}    ", end="")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDetenido.")
