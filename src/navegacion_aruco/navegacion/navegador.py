"""
Navegador autónomo — máquina de estados.

Integra Pipeline + MotorDriver + PIDController para guiar
el robot hacia un marcador ArUco destino de forma autónoma.

Estados:
    BUSCANDO  → gira sobre su eje hasta detectar el marcador
    ALINEANDO → PID angular centra el marcador en el frame
    AVANZANDO → PID de distancia avanza hacia el marcador
    LLEGADO   → se detiene al llegar al umbral de distancia

Uso:
    navegador = Navegador()
    exito = navegador.navegar_hacia(id_objetivo=2)
"""

import logging
import time
from enum import Enum, auto

from navegacion_aruco.control.motor_driver import MotorDriver
from navegacion_aruco.control.pid_controller import PIDController
from navegacion_aruco.vision.pipeline import Pipeline

logger = logging.getLogger(__name__)

# ── Parámetros de navegación ──────────────────────────────────────────────────
UMBRAL_LLEGADA_CM = 25.0  # distancia para considerar que llegó
ZONA_MUERTA_ANGULO = 8.0  # grados dentro de los cuales no corregir ángulo
VELOCIDAD_BUSQUEDA = 0.3  # velocidad de giro durante búsqueda (0-1)
GIROS_MAX_BUSQUEDA = 3  # vueltas máximas buscando antes de rendirse
TIEMPO_GIRO_360 = 5.0  # segundos aproximados para girar 360°

# ── Parámetros PID iniciales ──────────────────────────────────────────────────
PID_ANGULO_KP = 0.02
PID_ANGULO_KI = 0.0
PID_ANGULO_KD = 0.003

PID_DISTANCIA_KP = 0.02
PID_DISTANCIA_KI = 0.0
PID_DISTANCIA_KD = 0.003


class Estado(Enum):
    BUSCANDO = auto()
    ALINEANDO = auto()
    AVANZANDO = auto()
    LLEGADO = auto()
    FALLO = auto()


class Navegador:
    """
    Navegador autónomo con máquina de estados.

    Integra visión, control de motores y PID para navegación
    hacia un marcador ArUco destino.
    """

    def __init__(self) -> None:
        self._pipeline = Pipeline()
        self._motores = MotorDriver()
        self._pid_angulo = PIDController(
            kp=PID_ANGULO_KP,
            ki=PID_ANGULO_KI,
            kd=PID_ANGULO_KD,
            setpoint=0.0,
            salida_min=-1.0,
            salida_max=1.0,
        )
        self._pid_distancia = PIDController(
            kp=PID_DISTANCIA_KP,
            ki=PID_DISTANCIA_KI,
            kd=PID_DISTANCIA_KD,
            setpoint=UMBRAL_LLEGADA_CM,
            salida_min=0.0,
            salida_max=1.0,
        )
        logger.info("Navegador inicializado")

    def navegar_hacia(self, id_objetivo: int) -> bool:
        """
        Navega autónomamente hacia el marcador con id_objetivo.

        Returns:
            True si llegó al marcador, False si no lo encontró.
        """
        logger.info("Navegando hacia marcador ID=%d", id_objetivo)
        print(f"\nNavegando hacia marcador ID:{id_objetivo}")
        print("Ctrl+C para detener\n")

        estado = Estado.BUSCANDO
        tiempo_busqueda = 0.0
        tiempo_max_busqueda = GIROS_MAX_BUSQUEDA * TIEMPO_GIRO_360

        self._pid_angulo.reset()
        self._pid_distancia.reset()

        try:
            while estado not in (Estado.LLEGADO, Estado.FALLO):
                obs = self._pipeline.observar(id_objetivo)

                if estado == Estado.BUSCANDO:
                    estado = self._estado_buscando(
                        obs, tiempo_busqueda, tiempo_max_busqueda
                    )
                    tiempo_busqueda += 0.1

                elif estado == Estado.ALINEANDO:
                    estado = self._estado_alineando(obs)

                elif estado == Estado.AVANZANDO:
                    estado = self._estado_avanzando(obs)

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nDetenido por el usuario.")
        finally:
            self._motores.detener()

        if estado == Estado.LLEGADO:
            print(f"Llegado al marcador ID:{id_objetivo}")
            return True
        else:
            print(f"No se encontró el marcador ID:{id_objetivo}")
            return False

    def _estado_buscando(
        self,
        obs,
        tiempo_busqueda: float,
        tiempo_max: float,
    ) -> Estado:
        """Gira buscando el marcador."""
        if obs is not None:
            print(
                f"Marcador detectado — dist:{obs.distancia_cm:.1f}cm ang:{obs.angulo_deg:+.1f}°"
            )
            self._motores.detener()
            return Estado.ALINEANDO

        if tiempo_busqueda >= tiempo_max:
            logger.warning("Tiempo de búsqueda agotado")
            return Estado.FALLO

        self._motores.girar_derecha(VELOCIDAD_BUSQUEDA)
        print(f"\rBuscando... ({tiempo_busqueda:.1f}s)", end="")
        return Estado.BUSCANDO

    def _estado_alineando(self, obs) -> Estado:
        """Alinea el robot con el marcador usando PID angular."""
        if obs is None:
            print("\rMarcador perdido — volviendo a buscar")
            self._motores.detener()
            return Estado.BUSCANDO

        angulo = obs.angulo_deg

        if abs(angulo) <= ZONA_MUERTA_ANGULO:
            self._motores.detener()
            print(f"\rAlineado — dist:{obs.distancia_cm:.1f}cm")
            return Estado.AVANZANDO

        salida = self._pid_angulo.calcular(angulo)

        if salida > 0:
            self._motores.girar_izquierda(abs(salida))
        else:
            self._motores.girar_derecha(abs(salida))

        print(f"\rAlineando — ang:{angulo:+.1f}° salida:{salida:+.3f}", end="")
        return Estado.ALINEANDO

    def _estado_avanzando(self, obs) -> Estado:
        """Avanza hacia el marcador usando PID de distancia."""
        if obs is None:
            print("\rMarcador perdido — volviendo a buscar")
            self._motores.detener()
            return Estado.BUSCANDO

        distancia = obs.distancia_cm
        angulo = obs.angulo_deg

        if distancia <= UMBRAL_LLEGADA_CM:
            self._motores.detener()
            return Estado.LLEGADO

        if abs(angulo) > ZONA_MUERTA_ANGULO * 2:
            print(f"\rDesviado — volviendo a alinear (ang:{angulo:+.1f}°)")
            self._motores.detener()
            return Estado.ALINEANDO

        salida = self._pid_distancia.calcular(distancia)
        self._motores.adelante(salida)

        print(
            f"\rAvanzando — dist:{distancia:.1f}cm "
            f"ang:{angulo:+.1f}° vel:{salida:.2f}",
            end="",
        )
        return Estado.AVANZANDO

    def limpiar(self) -> None:
        """Libera recursos."""
        self._motores.limpiar()
        self._pipeline.liberar()
        logger.info("Navegador liberado")

    def __enter__(self) -> "Navegador":
        return self

    def __exit__(self, *_) -> None:
        self.limpiar()
