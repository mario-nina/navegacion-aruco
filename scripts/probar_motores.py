"""
Script de prueba interactiva de motores con control de velocidad.

Uso (en la Pi, con el chasis elevado):
    python3 scripts/probar_motores.py
"""

import time

from navegacion_aruco.control.motor_driver import MotorDriver

DURACION = 2.0


def pedir_velocidad() -> float:
    while True:
        v = input("  Velocidad (0.1 - 1.0, default 0.8): ").strip()
        if v == "":
            return 0.8
        try:
            valor = float(v)
            if 0.1 <= valor <= 1.0:
                return valor
            print("  Ingresa un valor entre 0.1 y 1.0")
        except ValueError:
            print("  Valor inválido")


def menu():
    print("\n=== Prueba de motores ===")
    print("  1 → Adelante")
    print("  2 → Atrás")
    print("  3 → Girar izquierda (eje propio)")
    print("  4 → Girar derecha (eje propio)")
    print("  5 → Solo motor izquierdo adelante")
    print("  6 → Solo motor izquierdo atrás")
    print("  7 → Solo motor derecho adelante")
    print("  8 → Solo motor derecho atrás")
    print("  9 → Prueba de velocidades (25%, 50%, 75%, 100%)")
    print("  S → Detener")
    print("  Q → Salir")
    return input("\nOpción: ").strip().lower()


def prueba_velocidades(motores: MotorDriver) -> None:
    """Prueba progresiva de velocidades en ambos motores."""
    for pct, vel in [(25, 0.25), (50, 0.5), (75, 0.75), (100, 1.0)]:
        print(f"  Velocidad {pct}% por {DURACION}s...")
        motores.adelante(vel)
        time.sleep(DURACION)
        motores.detener()
        time.sleep(0.5)


def main():
    print("Iniciando MotorDriver con PWM...")
    print("ADVERTENCIA: chasis elevado antes de continuar")
    input("Presiona ENTER para continuar...")

    with MotorDriver() as motores:
        while True:
            opcion = menu()

            if opcion == "1":
                vel = pedir_velocidad()
                print(f"Adelante al {int(vel*100)}% por {DURACION}s...")
                motores.adelante(vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "2":
                vel = pedir_velocidad()
                print(f"Atrás al {int(vel*100)}% por {DURACION}s...")
                motores.atras(vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "3":
                vel = pedir_velocidad()
                print(f"Girando izquierda al {int(vel*100)}% por {DURACION}s...")
                motores.girar_izquierda(vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "4":
                vel = pedir_velocidad()
                print(f"Girando derecha al {int(vel*100)}% por {DURACION}s...")
                motores.girar_derecha(vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "5":
                vel = pedir_velocidad()
                print(f"Motor izquierdo adelante al {int(vel*100)}% por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=True, velocidad=vel)
                motores._motor_derecho(adelante=True, activo=False)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "6":
                vel = pedir_velocidad()
                print(f"Motor izquierdo atrás al {int(vel*100)}% por {DURACION}s...")
                motores._motor_izquierdo(adelante=False, activo=True, velocidad=vel)
                motores._motor_derecho(adelante=True, activo=False)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "7":
                vel = pedir_velocidad()
                print(f"Motor derecho adelante al {int(vel*100)}% por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=False)
                motores._motor_derecho(adelante=True, activo=True, velocidad=vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "8":
                vel = pedir_velocidad()
                print(f"Motor derecho atrás al {int(vel*100)}% por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=False)
                motores._motor_derecho(adelante=False, activo=True, velocidad=vel)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "9":
                print("Prueba de velocidades progresiva...")
                prueba_velocidades(motores)

            elif opcion == "s":
                motores.detener()
                print("Detenido.")

            elif opcion == "q":
                print("Saliendo...")
                break

            else:
                print("Opción no válida")


if __name__ == "__main__":
    main()
