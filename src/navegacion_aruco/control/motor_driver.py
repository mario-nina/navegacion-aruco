"""
Driver de motores DC para el L298N con control de velocidad PWM.

Controla dos motores DC a través del driver L298N conectado
a los pines GPIO de la Raspberry Pi.

Conexiones GPIO:
    Motor izquierdo: IN1=GPIO17, IN2=GPIO18, ENA=GPIO12
    Motor derecho:   IN3=GPIO22, IN4=GPIO23, ENB=GPIO13

Uso:
    with MotorDriver() as motores:
        motores.adelante(0.8)
        time.sleep(2)
        motores.detener()
"""

import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

# Pines de dirección
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23

# Pines PWM (velocidad)
ENA = 12
ENB = 13

FRECUENCIA_PWM = 100  # Hz


class MotorDriver:
    """Abstracción del driver L298N con control de velocidad PWM."""

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pines de dirección
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        # Pines PWM
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(ENB, GPIO.OUT)

        self._pwm_izq = GPIO.PWM(ENA, FRECUENCIA_PWM)
        self._pwm_der = GPIO.PWM(ENB, FRECUENCIA_PWM)
        self._pwm_izq.start(0)
        self._pwm_der.start(0)

        self.detener()
        logger.info("MotorDriver inicializado con PWM")

    def _velocidad(self, valor: float) -> float:
        """Convierte velocidad 0.0-1.0 a duty cycle 0-100."""
        return max(0.0, min(1.0, valor)) * 100

    def _motor_izquierdo(
        self, adelante: bool, activo: bool, velocidad: float = 1.0
    ) -> None:
        if not activo:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            self._pwm_izq.ChangeDutyCycle(0)
        elif adelante:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            self._pwm_izq.ChangeDutyCycle(self._velocidad(velocidad))
        else:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            self._pwm_izq.ChangeDutyCycle(self._velocidad(velocidad))

    def _motor_derecho(
        self, adelante: bool, activo: bool, velocidad: float = 1.0
    ) -> None:
        if not activo:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)
            self._pwm_der.ChangeDutyCycle(0)
        elif adelante:
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            self._pwm_der.ChangeDutyCycle(self._velocidad(velocidad))
        else:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            self._pwm_der.ChangeDutyCycle(self._velocidad(velocidad))

    def adelante(self, velocidad: float = 1.0) -> None:
        """Ambos motores hacia adelante."""
        self._motor_izquierdo(adelante=True, activo=True, velocidad=velocidad)
        self._motor_derecho(adelante=True, activo=True, velocidad=velocidad)
        logger.debug("Adelante (velocidad=%.2f)", velocidad)

    def atras(self, velocidad: float = 1.0) -> None:
        """Ambos motores hacia atrás."""
        self._motor_izquierdo(adelante=False, activo=True, velocidad=velocidad)
        self._motor_derecho(adelante=False, activo=True, velocidad=velocidad)
        logger.debug("Atrás (velocidad=%.2f)", velocidad)

    def girar_izquierda(self, velocidad: float = 1.0) -> None:
        """Motor derecho adelante, motor izquierdo atrás (giro en eje propio)."""
        self._motor_izquierdo(adelante=False, activo=True, velocidad=velocidad)
        self._motor_derecho(adelante=True, activo=True, velocidad=velocidad)
        logger.debug("Girar izquierda (velocidad=%.2f)", velocidad)

    def girar_derecha(self, velocidad: float = 1.0) -> None:
        """Motor izquierdo adelante, motor derecho atrás (giro en eje propio)."""
        self._motor_izquierdo(adelante=True, activo=True, velocidad=velocidad)
        self._motor_derecho(adelante=False, activo=True, velocidad=velocidad)
        logger.debug("Girar derecha (velocidad=%.2f)", velocidad)

    def detener(self) -> None:
        """Ambos motores apagados."""
        self._motor_izquierdo(adelante=True, activo=False)
        self._motor_derecho(adelante=True, activo=False)
        logger.debug("Motores detenidos")

    def limpiar(self) -> None:
        """Libera los pines GPIO y PWM."""
        self.detener()
        self._pwm_izq.stop()
        self._pwm_der.stop()
        GPIO.cleanup()
        logger.info("GPIO y PWM liberados")

    def __enter__(self) -> "MotorDriver":
        return self

    def __exit__(self, *_) -> None:
        self.limpiar()
