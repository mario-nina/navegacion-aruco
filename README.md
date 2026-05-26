# navegacion-aruco

Robot móvil autónomo con navegación por marcadores ArUco y visión artificial en Raspberry Pi 3B.

## Descripción

Robot móvil físico capaz de navegar hacia puntos específicos dentro de un ambiente
controlado, utilizando marcadores ArUco como referencias visuales y una cámara web
como único sensor de percepción.

## Hardware

- Raspberry Pi 3B
- Cámara web USB
- Driver de motores L298N
- Chasis con tracción diferencial
- Batería Li-Po + buck converter 5V

## Stack

- Python 3.11
- OpenCV 4.x
- pigpio

## Estructura
src/navegacion_aruco/
├── vision/        — Cámara, detección ArUco, estimación de pose
├── control/       — Driver L298N, controlador PID
├── navegacion/    — Lógica de navegación autónoma
└── comunicacion/  — Recepción de comandos desde laptop

## Setup

### Laptop (desarrollo)

```bash
git clone git@github.com:mario-nina/navegacion-aruco.git
cd navegacion-aruco
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

### Raspberry Pi

```bash
git clone git@github.com:mario-nina/navegacion-aruco.git ~/navegacion-aruco
cd ~/navegacion-aruco
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements-pi.txt
```

## Tests

```bash
# Tests unitarios (laptop o Pi, sin hardware)
pytest tests/unit/ -v

# Tests de integración (solo Pi, con cámara conectada)
pytest tests/integration/ -m hardware -v
```

## Uso

```bash
# Desde la laptop, conectada a la red WiFi de la Pi:
ssh malber@192.168.0.15 "cd ~/navegacion-aruco && python3 scripts/run_robot.py --target-id 3"
```

## Fases de desarrollo

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Infraestructura y GitHub | ✅ |
| 1 | Verificación de cámara | ✅ |
| 2 | Calibración de cámara | 🔄 |
| 3 | Detección ArUco | ⏳ |
| 4 | Estimación de pose | ⏳ |
| 5 | Validación con métricas | ⏳ |
| 6 | Pipeline de visión integrado | ⏳ |
| 7 | Driver de motores | ⏳ |
| 8 | Controlador PID | ⏳ |
| 9 | Navegación completa | ⏳ |
| 10 | Interfaz de comando | ⏳ |
| 11 | Pruebas y ajuste PID | ⏳ |
| 12 | Preparación para demo | ⏳ |

## Licencia

MIT
