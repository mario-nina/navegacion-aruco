"""
Stream de video en tiempo real desde la cámara de la Pi.

Uso (en la Pi):
    python3 scripts/stream_camara.py

Ver en la laptop:
    Abrir navegador en http://192.168.0.15:8080

Solo para desarrollo — no usar durante operación autónoma del robot.
"""

import cv2
from flask import Flask, Response

from navegacion_aruco.vision.camara import Camara
from navegacion_aruco.vision.detector import Detector

app = Flask(__name__)


def generar_frames():
    """Genera frames MJPEG con detección de marcadores superpuesta."""
    with Camara() as cam:
        detector = Detector()
        while True:
            frame = cam.leer()
            marcadores = detector.detectar(frame)

            # Dibujar marcadores detectados
            for m in marcadores:
                cv2.polylines(frame, [m.esquinas], True, (0, 255, 0), 2)
                cx, cy = m.centro
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"ID:{m.id}", (cx + 8, cy - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Línea central de referencia
            h, w = frame.shape[:2]
            cv2.line(frame, (w // 2, 0), (w // 2, h), (100, 100, 100), 1)

            _, buffer = cv2.imencode(".jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )


@app.route("/")
def index():
    return """
    <html>
    <head><title>Camara Pi</title></head>
    <body style="background:#000;margin:0">
    <img src="/video" style="width:100%;max-width:640px;display:block;margin:auto">
    </body>
    </html>
    """


@app.route("/video")
def video():
    return Response(
        generar_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    print("Stream disponible en: http://192.168.0.15:8080")
    app.run(host="0.0.0.0", port=8080, debug=False)
