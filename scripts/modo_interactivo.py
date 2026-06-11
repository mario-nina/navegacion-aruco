"""
Modo interactivo de navegación.

Permite enviar el robot a distintos marcadores sin reiniciar el programa.

Uso (en la Pi):
    python3 scripts/modo_interactivo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from navegacion_aruco.navegacion.navegador import Navegador


def main() -> None:
    print("=== Modo interactivo de navegación ===")
    print("Escribe el ID del marcador destino y presiona ENTER.")
    print("Q para salir.\n")

    with Navegador() as navegador:
        while True:
            entrada = input("Marcador destino (ID): ").strip().lower()

            if entrada == "q":
                print("Saliendo...")
                break

            if not entrada.isdigit():
                print("Ingresa un número válido (0-49)")
                continue

            id_objetivo = int(entrada)
            exito = navegador.navegar_hacia(id_objetivo)

            if exito:
                print(f"\nLlegado al marcador ID:{id_objetivo}")
            else:
                print(f"\nNo se encontró el marcador ID:{id_objetivo}")

            print("\nListo para el siguiente destino.")


if __name__ == "__main__":
    main()
