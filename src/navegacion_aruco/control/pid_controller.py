"""
Controlador PID genérico con anti-windup y límites de salida.

Se usa en dos instancias para la navegación:
    - PID angular:    controla el ángulo al marcador → girar izquierda/derecha
    - PID distancia:  controla la distancia al marcador → adelante

Uso:
    pid = PIDController(kp=0.4, ki=0.0, kd=0.05, setpoint=0.0)
    salida = pid.calcular(medicion=15.0, dt=0.05)
"""

import logging
import time

logger = logging.getLogger(__name__)


class PIDController:
    """
    Controlador PID con anti-windup y límites de salida.

    Args:
        kp: ganancia proporcional
        ki: ganancia integral
        kd: ganancia derivativa
        setpoint: valor objetivo (default 0.0)
        salida_min: límite inferior de salida (default -1.0)
        salida_max: límite superior de salida (default 1.0)
    """

    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        setpoint: float = 0.0,
        salida_min: float = -1.0,
        salida_max: float = 1.0,
    ) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.salida_min = salida_min
        self.salida_max = salida_max

        self._integral = 0.0
        self._error_anterior = 0.0
        self._ultimo_tiempo = time.monotonic()

        logger.debug(
            "PIDController: kp=%.3f ki=%.3f kd=%.3f setpoint=%.2f",
            kp,
            ki,
            kd,
            setpoint,
        )

    def calcular(self, medicion: float, dt: float | None = None) -> float:
        """
        Calcula la salida del PID dado el valor actual medido.

        Args:
            medicion: valor actual del sistema (ángulo o distancia)
            dt: intervalo de tiempo en segundos. Si es None, se calcula
                automáticamente desde la última llamada.

        Returns:
            Salida del controlador entre salida_min y salida_max.
        """
        ahora = time.monotonic()
        if dt is None:
            dt = ahora - self._ultimo_tiempo
        self._ultimo_tiempo = ahora

        if dt <= 0:
            dt = 1e-6

        error = self.setpoint - medicion

        # Término proporcional
        p = self.kp * error

        # Término integral con anti-windup
        self._integral += error * dt
        i = self.ki * self._integral
        salida_sin_limitar = p + i + self.kd * (error - self._error_anterior) / dt

        # Anti-windup: si la salida está saturada, no acumular más integral
        if salida_sin_limitar > self.salida_max or salida_sin_limitar < self.salida_min:
            self._integral -= error * dt

        # Término derivativo
        d = self.kd * (error - self._error_anterior) / dt
        self._error_anterior = error

        # Salida final limitada
        salida = max(
            self.salida_min, min(self.salida_max, p + self.ki * self._integral + d)
        )

        logger.debug(
            "PID: error=%.2f P=%.3f I=%.3f D=%.3f salida=%.3f",
            error,
            p,
            self.ki * self._integral,
            d,
            salida,
        )

        return salida

    def reset(self) -> None:
        """Reinicia el estado interno del controlador."""
        self._integral = 0.0
        self._error_anterior = 0.0
        self._ultimo_tiempo = time.monotonic()
        logger.debug("PIDController reiniciado")

    def set_setpoint(self, setpoint: float) -> None:
        """Cambia el valor objetivo y reinicia el estado."""
        self.setpoint = setpoint
        self.reset()
        logger.debug("Setpoint cambiado a %.2f", setpoint)
