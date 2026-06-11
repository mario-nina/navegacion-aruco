"""
Navegación en secuencia — carrera de postas.

El robot navega hacia una lista de marcadores en orden,
deteniéndose en cada uno antes de continuar al siguiente.

Uso (en la Pi):
    python3 scripts/secuencia_marcadores.py --ids 0 1 2 3

    python3 scripts/secuencia_marcadores.py --ids 0 2 1 --pausa 3
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from navegacion_aruco.navegacion.navegador import Navegador


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Navegación en secuencia hacia múltiples marcadores ArUco"
    )
    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        required=True,
        help="Lista de IDs de marcadores en orden (ej: --ids 0 1 2 3)",
    )
    parser.add_argument(
        "--pausa",
        type=float,
        default=2.0,
        help="Segundos de pausa entre marcadores (default: 2)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=== Navegación en secuencia ===")
    print(f"Secuencia: {' → '.join(str(i) for i in args.ids)}")
    print(f"Pausa entre marcadores: {args.pausa}s")
    print("Ctrl+C para detener\n")

    completados = 0
    fallidos = []

    with Navegador() as navegador:
        for i, id_objetivo in enumerate(args.ids):
            print(
                f"\n[{i+1}/{len(args.ids)}] Navegando hacia marcador ID:{id_objetivo}"
            )

            exito = navegador.navegar_hacia(id_objetivo)

            if exito:
                completados += 1
                print(f"✓ Llegado al marcador ID:{id_objetivo}")
                if i < len(args.ids) - 1:
                    print(f"Esperando {args.pausa}s antes del siguiente...")
                    time.sleep(args.pausa)
            else:
                fallidos.append(id_objetivo)
                print(f"✗ No se encontró marcador ID:{id_objetivo} — continuando...")

    print("\n=== Resumen ===")
    print(f"Completados: {completados}/{len(args.ids)}")
    if fallidos:
        print(f"Fallidos: {fallidos}")


if __name__ == "__main__":
    main()
