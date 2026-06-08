"""
Validación de precisión de la estimación de pose.

Mide el error real de distancia y ángulo comparando las estimaciones
del sistema contra medidas físicas reales con regla.

Uso:
    python3 calibracion/validar_pose.py

Genera docs/registro_validacion_pose.md con los resultados.
Requiere: config/camera_calibration.npz (ejecutar calibrar_camara.py primero)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from navegacion_aruco.vision.camara import Camara
from navegacion_aruco.vision.detector import Detector
from navegacion_aruco.vision.estimador_pose import EstimadorPose

ID_MARCADOR = 0
N_MUESTRAS = 30
TAMANO_MARCADOR_MM = 39.0

DISTANCIAS_CM = [20, 30, 40, 50, 60]
ANGULOS_DEG = [-15, -10, 0, 10, 15]
DISTANCIA_FIJA_ANGULOS = 40

# Resultados de distancia capturados previamente
RESULTADOS_DISTANCIA_PREVIOS = [
    {"dist_real": 20, "dist_media": 24.76, "error": +4.76, "dist_std": 0.15},
    {"dist_real": 30, "dist_media": 34.01, "error": +4.01, "dist_std": 0.14},
    {"dist_real": 40, "dist_media": 46.06, "error": +6.06, "dist_std": 0.45},
    {"dist_real": 50, "dist_media": 53.02, "error": +3.02, "dist_std": 0.27},
    {"dist_real": 60, "dist_media": 63.06, "error": +3.06, "dist_std": 0.27},
]


def medir_posicion(
    cam: Camara,
    detector: Detector,
    estimador: EstimadorPose,
    descripcion: str,
) -> dict | None:
    print(f"\n  Posicionar: {descripcion}")
    print("  Cuando el marcador esté en posición, presiona ESPACIO para medir.")
    print("  Q para saltar esta posición.\n")

    while True:
        frame = cam.leer()
        marcador = detector.detectar_por_id(frame, ID_MARCADOR)
        display = frame.copy()

        if marcador is not None:
            cv2.polylines(display, [marcador.esquinas], True, (0, 255, 0), 2)
            cx, cy = marcador.centro
            cv2.circle(display, (cx, cy), 5, (0, 0, 255), -1)
            try:
                pose = estimador.estimar(marcador)
                cv2.putText(
                    display,
                    f"Dist: {pose.distancia_cm:.1f}cm  Ang: {pose.angulo_deg:+.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )
            except RuntimeError:
                pass
            cv2.putText(
                display,
                "DETECTADO - ESPACIO para medir",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )
        else:
            cv2.putText(
                display,
                "Sin marcador...",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 200),
                2,
            )

        cv2.putText(
            display,
            descripcion[:50],
            (10, display.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        cv2.imshow("Validacion de pose", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            return None
        elif key == ord(" ") and marcador is not None:
            break

    distancias = []
    angulos = []
    intentos = 0

    print(f"  Capturando {N_MUESTRAS} lecturas", end="", flush=True)

    while len(distancias) < N_MUESTRAS and intentos < N_MUESTRAS * 5:
        frame = cam.leer()
        marcador = detector.detectar_por_id(frame, ID_MARCADOR)
        intentos += 1

        if marcador is None:
            continue

        try:
            pose = estimador.estimar(marcador)
            distancias.append(pose.distancia_cm)
            angulos.append(pose.angulo_deg)
            print(".", end="", flush=True)
        except RuntimeError:
            continue

    print()

    if len(distancias) < 10:
        print(f"  ERROR: solo {len(distancias)} lecturas válidas")
        return None

    return {
        "descripcion": descripcion,
        "dist_media": round(float(np.mean(distancias)), 2),
        "dist_std": round(float(np.std(distancias)), 2),
        "ang_media": round(float(np.mean(angulos)), 2),
        "ang_std": round(float(np.std(angulos)), 2),
        "n": len(distancias),
    }


def generar_reporte(resultados_angulo: list) -> str:
    lineas = [
        "# Registro de validación de pose\n",
        f"Marcador ID: {ID_MARCADOR} | "
        f"Tamaño: {TAMANO_MARCADOR_MM}mm | "
        "Diccionario: DICT_4X4_50\n",
        "## Validación de distancia\n",
        "Marcador centrado frente a la cámara.\n",
        "| Real (cm) | Medido (cm) | Error (cm) | σ (cm) |",
        "|-----------|-------------|------------|--------|",
    ]

    for r in RESULTADOS_DISTANCIA_PREVIOS:
        lineas.append(
            f"| {r['dist_real']} | {r['dist_media']} "
            f"| {r['error']:+.2f} | {r['dist_std']} |"
        )

    lineas += [
        "\n## Validación de ángulo\n",
        f"Marcador a {DISTANCIA_FIJA_ANGULOS}cm de distancia.\n",
        "| Real (°) | Medido (°) | Error (°) | σ (°) |",
        "|----------|------------|-----------|-------|",
    ]

    for r, ang_real in zip(resultados_angulo, ANGULOS_DEG):
        if r is None:
            lineas.append(f"| {ang_real:+d} | ERROR | — | — |")
            continue
        error = round(r["ang_media"] - ang_real, 2)
        lineas.append(
            f"| {ang_real:+d} | {r['ang_media']:+.2f} | {error:+.2f} | {r['ang_std']} |"
        )

    return "\n".join(lineas) + "\n"


def main() -> None:
    print("=" * 60)
    print(" Validación de ángulo — continuación")
    print("=" * 60)
    print(f"\nMarcador a usar: ID {ID_MARCADOR}")
    print(f"Tamaño del marcador: {TAMANO_MARCADOR_MM}mm")
    print(f"Distancia fija: {DISTANCIA_FIJA_ANGULOS}cm")
    print(f"Ángulos a medir: {ANGULOS_DEG}")

    input("\nPresiona ENTER para comenzar...")

    try:
        cam = Camara()
        detector = Detector()
        estimador = EstimadorPose(TAMANO_MARCADOR_MM)
    except Exception as e:
        print(f"ERROR al inicializar: {e}")
        sys.exit(1)

    resultados_angulo = []

    print("\n" + "=" * 60)
    print(" PRUEBAS DE ÁNGULO")
    print(f" Mantener el marcador a {DISTANCIA_FIJA_ANGULOS}cm de distancia")
    print("=" * 60)

    for ang in ANGULOS_DEG:
        if ang == 0:
            desc = f"Marcador CENTRADO a {DISTANCIA_FIJA_ANGULOS}cm (0°)"
        elif ang < 0:
            desc = f"Marcador {abs(ang)}° a la IZQUIERDA a {DISTANCIA_FIJA_ANGULOS}cm"
        else:
            desc = f"Marcador {ang}° a la DERECHA a {DISTANCIA_FIJA_ANGULOS}cm"

        r = medir_posicion(cam, detector, estimador, desc)
        resultados_angulo.append(r)
        if r:
            error = round(r["ang_media"] - ang, 2)
            print(
                f"  Real: {ang:+d}° → Medido: {r['ang_media']:+.2f}° "
                f"| Error: {error:+.2f}° | σ={r['ang_std']}°"
            )

    cv2.destroyAllWindows()
    cam.liberar()

    reporte = generar_reporte(resultados_angulo)
    ruta_reporte = Path(__file__).parent.parent / "docs" / "registro_validacion_pose.md"
    ruta_reporte.write_text(reporte)

    print("\n" + "=" * 60)
    print(f" Reporte guardado en: {ruta_reporte}")
    print("=" * 60)
    print(reporte)


if __name__ == "__main__":
    main()
