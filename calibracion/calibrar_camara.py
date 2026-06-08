"""
Calibración de la cámara usando las imágenes del tablero de ajedrez.

Uso:
    python3 calibracion/calibrar_camara.py

Genera config/camera_calibration.npz con los parámetros intrínsecos.
"""

import glob
import sys
from pathlib import Path

import cv2
import numpy as np

PATRON = (9, 6)
TAMANO_CUADRO_MM = 26.0
DIRECTORIO_IMAGENES = Path(__file__).parent / "imagenes"
ARCHIVO_SALIDA = Path(__file__).parent.parent / "config" / "camera_calibration.npz"


def calibrar() -> None:
    # Puntos 3D del tablero en el mundo real (z=0)
    objp = np.zeros((PATRON[0] * PATRON[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : PATRON[0], 0 : PATRON[1]].T.reshape(-1, 2)
    objp *= TAMANO_CUADRO_MM

    objpoints = []
    imgpoints = []

    imagenes = sorted(glob.glob(str(DIRECTORIO_IMAGENES / "*.jpg")))
    if not imagenes:
        print(f"ERROR: No se encontraron imágenes en {DIRECTORIO_IMAGENES}")
        sys.exit(1)

    print(f"Procesando {len(imagenes)} imágenes...")
    img_shape = None
    validas = 0

    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for ruta in imagenes:
        img = cv2.imread(ruta)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_shape = gray.shape[::-1]

        encontrado, corners = cv2.findChessboardCorners(gray, PATRON, None)

        if not encontrado:
            print(f"  SKIP: {Path(ruta).name}")
            continue

        corners_refinadas = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criterio
        )
        objpoints.append(objp)
        imgpoints.append(corners_refinadas)
        validas += 1
        print(f"  OK: {Path(ruta).name}")

    if validas < 10:
        print(f"\nERROR: Solo {validas} imágenes válidas. Se necesitan al menos 10.")
        sys.exit(1)

    print(f"\nCalibrando con {validas} imágenes...")
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )

    # Calcular error de reproyección
    error_total = 0.0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs
        )
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        error_total += error
    error_medio = error_total / len(objpoints)

    print(f"\n{'='*50}")
    print(f"Error de reproyección medio: {error_medio:.4f} px")
    if error_medio < 0.5:
        print("Calibración EXCELENTE")
    elif error_medio < 1.0:
        print("Calibración BUENA")
    else:
        print("ADVERTENCIA: error alto — considerar recapturar imágenes")
    print(f"{'='*50}")
    print(f"\nMatriz de cámara:\n{camera_matrix}")
    print(f"\nCoeficientes de distorsión:\n{dist_coeffs}")

    ARCHIVO_SALIDA.parent.mkdir(exist_ok=True)
    np.savez(
        str(ARCHIVO_SALIDA),
        camera_matrix=camera_matrix,
        dist_coeffs=dist_coeffs,
        reprojection_error=error_medio,
    )
    print(f"\nGuardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    calibrar()
