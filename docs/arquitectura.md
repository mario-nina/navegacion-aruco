# Arquitectura del sistema

## Visión general
┌─────────────────────────────────────────────────────┐
│                  Raspberry Pi 3B                    │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐   │
│  │  vision  │───▶│navegacion│───▶│   control    │   │
│  │          │    │          │    │              │   │
│  │ Camara   │    │ Navigator│    │ MotorDriver  │   │
│  │ Detector │    │          │    │ PIDController│   │
│  │ Pose     │    │          │    │              │   │
│  └──────────┘    └──────────┘    └──────────────┘   │
│       ▲                                  │          │
│       │                                  ▼          │
│  Cámara USB                          L298N          │
└─────────────────────────────────────────────────────┘
│
Motores DC


## Módulos

### vision
Responsable de toda la percepción visual del robot.
- `camara.py` — abstracción de la cámara USB
- `detector.py` — detección e identificación de marcadores ArUco
- `pose_estimator.py` — estimación de distancia y ángulo al marcador
- `pipeline.py` — interfaz de alto nivel que integra los tres módulos anteriores

### control
Responsable del movimiento físico del robot.
- `motor_driver.py` — abstracción del driver L298N (adelante, atrás, girar, parar)
- `pid_controller.py` — controlador PID genérico para ángulo y distancia

### navegacion
Lógica de navegación autónoma.
- `navigator.py` — máquina de estados: búsqueda → alineación → avance → llegada

### comunicacion
Recepción de comandos desde la laptop.
- `receptor_comandos.py` — recibe el ID del marcador destino vía SSH

## Flujo de navegación
Laptop envía ID del marcador destino vía SSH
Robot inicia búsqueda — gira sobre su eje
Al detectar el marcador → calcula ángulo y distancia
PID angular → alinea el robot con el marcador
PID de distancia → avanza hacia el marcador
Al llegar al umbral de distancia → se detiene

## Hardware

| Componente | Función |
|---|---|
| Raspberry Pi 3B | Computadora principal del robot |
| Cámara USB | Único sensor de percepción |
| L298N | Driver de motores DC |
| Motores DC | Tracción diferencial |
| Batería Li-Po | Alimentación principal |
| Buck converter 5V | Regulador de voltaje para la Pi |
