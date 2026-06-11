"""
Navegador autónomo — máquina de estados.

Integra Pipeline + MotorDriver + PIDController para guiar
el robot hacia un marcador ArUco destino de forma autónoma.

Estados:
    BUSCANDO  → gira sobre su eje hasta detectar el marcador
    ALINEANDO → PID angular centra el marcador en el frame
    AVANZANDO → avance proporcional a la distancia
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
UMBRAL_LLEGADA_CM = 35.0
ZONA_MUERTA_ANGULO = 5.0
VELOCIDAD_BUSQUEDA = 0.3
GIROS_MAX_BUSQUEDA = 3
TIEMPO_GIRO_360 = 5.0
DISTANCIA_FRENADO_CM = 60.0   # distancia a la que empieza a frenar

# ── Parámetros PID angular ────────────────────────────────────────────────────
PID_ANGULO_KP = 0.03
PID_ANGULO_KI = 0.0
PID_ANGULO_KD = 0.005


class Estado(Enum):
    BUSCANDO = auto()
    ALINEANDO = auto()
    AVANZANDO = auto()
    LLEGADO = auto()
    FALLO = auto()


class Navegador:
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
        logger.info("Navegador inicializado")

    def navegar_hacia(self, id_objetivo: int) -> bool:
        logger.info("Navegando hacia marcador ID=%d", id_objetivo)
        print(f"\nNavegando hacia marcador ID:{id_objetivo}")
        print("Ctrl+C para detener\n")

        estado = Estado.BUSCANDO
        tiempo_busqueda = 0.0
        tiempo_max_busqueda = GIROS_MAX_BUSQUEDA * TIEMPO_GIRO_360

        self._pid_angulo.reset()

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

    def _estado_buscando(self, obs, tiempo_busqueda, tiempo_max) -> Estado:
        if obs is not None:
            print(
                f"Marcador detectado — dist:{obs.distancia_cm:.1f}cm "
                f"ang:{obs.angulo_deg:+.1f}°"
            )
            return Estado.ALINEANDO

        if tiempo_busqueda >= tiempo_max:
            logger.warning("Tiempo de búsqueda agotado")
            return Estado.FALLO

        self._motores.girar_derecha(VELOCIDAD_BUSQUEDA)
        print(f"\rBuscando... ({tiempo_busqueda:.1f}s)", end="")
        return Estado.BUSCANDO

    def _estado_alineando(self, obs) -> Estado:
        if obs is None:
            print("\rMarcador perdido — volviendo a buscar")
            self._motores.detener()
            return Estado.BUSCANDO

        angulo = obs.angulo_deg

        if abs(angulo) <= ZONA_MUERTA_ANGULO:
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

        # Velocidad proporcional a la distancia — frena suavemente al acercarse
        velocidad = min(1.0, distancia / DISTANCIA_FRENADO_CM)
        velocidad = max(0.25, velocidad)  # velocidad mínima para que los motores giren
        self._motores.adelante(velocidad)

        print(
            f"\rAvanzando — dist:{distancia:.1f}cm "
            f"ang:{angulo:+.1f}° vel:{velocidad:.2f}",
            end="",
        )
        return Estado.AVANZANDO

    def limpiar(self) -> None:
        self._motores.limpiar()
        self._pipeline.liberar()
        logger.info("Navegador liberado")

    def __enter__(self) -> "Navegador":
        return self

    def __exit__(self, *_) -> None:
        self.limpiar()
