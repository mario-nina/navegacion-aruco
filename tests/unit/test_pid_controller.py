"""
Tests unitarios del controlador PID.

No requieren hardware — usan simulación matemática.
Ejecutar en laptop:
    pytest tests/unit/test_pid_controller.py -v
"""

from navegacion_aruco.control.pid_controller import PIDController


def test_pid_converge_al_setpoint():
    """El PID debe converger al setpoint en una simulación simple."""
    pid = PIDController(kp=0.5, ki=0.1, kd=0.05, setpoint=0.0)
    posicion = 30.0
    dt = 0.05

    for _ in range(100):
        salida = pid.calcular(posicion, dt=dt)
        posicion += salida

    assert abs(posicion) < 2.0, f"No convergió: posición final = {posicion:.2f}"


def test_pid_respeta_limites_de_salida():
    """La salida nunca debe superar los límites configurados."""
    pid = PIDController(
        kp=10.0,
        ki=0.0,
        kd=0.0,
        setpoint=0.0,
        salida_min=-0.5,
        salida_max=0.5,
    )
    salida = pid.calcular(100.0, dt=0.1)
    assert -0.5 <= salida <= 0.5


def test_pid_anti_windup():
    """El integrador no debe acumular error cuando la salida está saturada."""
    pid = PIDController(
        kp=0.1,
        ki=5.0,
        kd=0.0,
        setpoint=0.0,
        salida_min=-1.0,
        salida_max=1.0,
    )
    for _ in range(1000):
        pid.calcular(100.0, dt=0.05)

    salida_despues = pid.calcular(0.1, dt=0.05)
    assert salida_despues < 0.5, "Anti-windup falló: integrador acumuló demasiado"


def test_pid_reset():
    """Después de reset el estado interno debe ser cero."""
    pid = PIDController(kp=0.5, ki=0.5, kd=0.05, setpoint=0.0)
    for _ in range(20):
        pid.calcular(10.0, dt=0.05)

    pid.reset()
    salida = pid.calcular(0.0, dt=0.05)
    assert abs(salida) < 0.01, "Después de reset la salida debería ser ~0"


def test_pid_setpoint_cero_sin_error():
    """Con medición igual al setpoint la salida debe ser cercana a cero."""
    pid = PIDController(kp=0.5, ki=0.0, kd=0.0, setpoint=0.0)
    salida = pid.calcular(0.0, dt=0.05)
    assert abs(salida) < 0.01


def test_pid_responde_a_error_positivo():
    """Con error positivo la salida debe ser positiva (P solo)."""
    pid = PIDController(kp=0.5, ki=0.0, kd=0.0, setpoint=0.0)
    salida = pid.calcular(-10.0, dt=0.05)
    assert salida > 0


def test_pid_responde_a_error_negativo():
    """Con error negativo la salida debe ser negativa (P solo)."""
    pid = PIDController(kp=0.5, ki=0.0, kd=0.0, setpoint=0.0)
    salida = pid.calcular(10.0, dt=0.05)
    assert salida < 0
