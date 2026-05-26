"""
Script de prueba interactiva de motores.

Uso (en la Pi, con el chasis elevado):
    python3 scripts/probar_motores.py

Permite probar cada movimiento del robot de forma manual.
"""

import time
from navegacion_aruco.control.motor_driver import MotorDriver

DURACION = 1.0  # segundos por movimiento


def menu():
    print("\n=== Prueba de motores ===")
    print("  1 → Adelante")
    print("  2 → Atrás")
    print("  3 → Girar izquierda")
    print("  4 → Girar derecha")
    print("  5 → Detener")
    print("  Q → Salir")
    return input("\nOpción: ").strip().lower()


def main():
    print("Iniciando MotorDriver...")
    print("ADVERTENCIA: asegurarse de que el chasis esté elevado")

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
                motores.detener()
                print("Detenido.")

            elif opcion == "q":
                print("Saliendo...")
                break

            else:
                print("Opción no válida")


if __name__ == "__main__":
    main()
