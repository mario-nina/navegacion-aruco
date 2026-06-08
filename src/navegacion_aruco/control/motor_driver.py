"""
Driver de motores DC para el L298N.

Controla dos motores DC a través del driver L298N conectado
a los pines GPIO de la Raspberry Pi.

Conexiones GPIO:
    Motor izquierdo: IN1=GPIO17, IN2=GPIO18
    Motor derecho:   IN3=GPIO22, IN4=GPIO23
    ENA y ENB con jumper (velocidad máxima)

Uso:
    with MotorDriver() as motores:
        motores.adelante(0.8)
        time.sleep(2)
        motores.detener()
"""

import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

# Pines GPIO
IN1 = 17  # Motor izquierdo dirección 1
IN2 = 18  # Motor izquierdo dirección 2
IN3 = 22  # Motor derecho dirección 1
IN4 = 23  # Motor derecho dirección 2


class MotorDriver:
    """Abstracción del driver L298N para control de dos motores DC."""

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        self.detener()
        logger.info("MotorDriver inicializado")

    def _motor_izquierdo(self, adelante: bool, activo: bool) -> None:
        """Controla el motor izquierdo."""
        if not activo:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
        elif adelante:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
        else:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)

    def _motor_derecho(self, adelante: bool, activo: bool) -> None:
        """Controla el motor derecho."""
        if not activo:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)
        elif adelante:
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
        else:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)

    def adelante(self, velocidad: float = 1.0) -> None:
        """Ambos motores hacia adelante."""
        self._motor_izquierdo(adelante=True, activo=True)
        self._motor_derecho(adelante=True, activo=True)
        logger.debug("Adelante (velocidad=%.1f)", velocidad)

    def atras(self, velocidad: float = 1.0) -> None:
        """Ambos motores hacia atrás."""
        self._motor_izquierdo(adelante=False, activo=True)
        self._motor_derecho(adelante=False, activo=True)
        logger.debug("Atrás (velocidad=%.1f)", velocidad)

    def girar_izquierda(self, velocidad: float = 1.0) -> None:
        """Motor derecho adelante, motor izquierdo atrás (giro en eje propio)."""
        self._motor_izquierdo(adelante=False, activo=True)
        self._motor_derecho(adelante=True, activo=True)
        logger.debug("Girar izquierda (velocidad=%.1f)", velocidad)

    def girar_derecha(self, velocidad: float = 1.0) -> None:
        """Motor izquierdo adelante, motor derecho atrás (giro en eje propio)."""
        self._motor_izquierdo(adelante=True, activo=True)
        self._motor_derecho(adelante=False, activo=True)
        logger.debug("Girar derecha (velocidad=%.1f)", velocidad)

    def detener(self) -> None:
        """Ambos motores apagados."""
        self._motor_izquierdo(adelante=True, activo=False)
        self._motor_derecho(adelante=True, activo=False)
        logger.debug("Motores detenidos")

    def limpiar(self) -> None:
        """Libera los pines GPIO."""
        self.detener()
        GPIO.cleanup()
        logger.info("GPIO liberado")

    def __enter__(self) -> "MotorDriver":
        return self

    def __exit__(self, *_) -> None:
        self.limpiar()
