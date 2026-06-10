"""
Script de prueba interactiva de motores.

Uso (en la Pi, con el chasis elevado):
    python3 scripts/probar_motores.py

Permite probar cada movimiento del robot de forma manual.
"""

import time

from navegacion_aruco.control.motor_driver import MotorDriver

DURACION = 2.0


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
    print("  S → Detener")
    print("  Q → Salir")
    return input("\nOpción: ").strip().lower()


def main():
    print("Iniciando MotorDriver...")
    print("ADVERTENCIA: chasis elevado antes de continuar")
    input("Presiona ENTER para continuar...")

    with MotorDriver() as motores:
        while True:
            opcion = menu()

            if opcion == "1":
                print(f"Adelante por {DURACION}s...")
                motores.adelante()
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "2":
                print(f"Atrás por {DURACION}s...")
                motores.atras()
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "3":
                print(f"Girando izquierda por {DURACION}s...")
                motores.girar_izquierda()
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "4":
                print(f"Girando derecha por {DURACION}s...")
                motores.girar_derecha()
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "5":
                print(f"Motor izquierdo adelante por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=True)
                motores._motor_derecho(adelante=True, activo=False)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "6":
                print(f"Motor izquierdo atrás por {DURACION}s...")
                motores._motor_izquierdo(adelante=False, activo=True)
                motores._motor_derecho(adelante=True, activo=False)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "7":
                print(f"Motor derecho adelante por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=False)
                motores._motor_derecho(adelante=True, activo=True)
                time.sleep(DURACION)
                motores.detener()

            elif opcion == "8":
                print(f"Motor derecho atrás por {DURACION}s...")
                motores._motor_izquierdo(adelante=True, activo=False)
                motores._motor_derecho(adelante=False, activo=True)
                time.sleep(DURACION)
                motores.detener()

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
