# Conexiones eléctricas

## Diagrama general
Batería Li-Po
│
├──────────────────► L298N (VCC motores)
│
└──► Buck converter 5V
│
└──► Raspberry Pi 3B (5V/3A)
## Raspberry Pi 3B → L298N

| L298N | GPIO Pi | Función |
|---|---|---|
| IN1 | GPIO 17 | Motor A dirección 1 |
| IN2 | GPIO 18 | Motor A dirección 2 |
| IN3 | GPIO 22 | Motor B dirección 1 |
| IN4 | GPIO 23 | Motor B dirección 2 |
| ENA | GPIO 12 | Motor A velocidad (PWM) |
| ENB | GPIO 13 | Motor B velocidad (PWM) |
| GND | GND | Tierra común |

## Notas importantes

- El buck converter debe ajustarse a exactamente 5V antes de conectar la Pi
- Verificar con multímetro antes de encender
- GND de la Pi y GND del L298N deben estar conectados (tierra común)
- ENA y ENB requieren pines PWM hardware de la Pi (GPIO 12 y 13)

## Cámara USB

Conectada directamente al puerto USB de la Raspberry Pi.
Índice OpenCV: `0` (primera cámara USB detectada).
Verificar con: `ls /dev/video*`
