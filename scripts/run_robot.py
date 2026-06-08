"""
Punto de entrada principal del robot.

Recibe el ID del marcador destino y ejecuta la navegación autónoma.

Uso (en la Pi):
    python3 scripts/run_robot.py --id 2

Desde la laptop via SSH:
    ssh malber@marionina.local "cd ~/navegacion-aruco && python3 scripts/run_robot.py --id 2"
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from navegacion_aruco.navegacion.navegador import Navegador


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Navegación autónoma hacia marcador ArUco"
    )
    parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="ID del marcador ArUco destino (0-49)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activar logging de debug",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configurar_logging()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    print(f"Robot iniciado — destino: marcador ID:{args.id}")

    with Navegador() as navegador:
        exito = navegador.navegar_hacia(args.id)

    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
