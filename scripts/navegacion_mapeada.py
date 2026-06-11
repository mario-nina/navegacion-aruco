"""
Navegación mapeada — escaneo inicial y secuencia inteligente.

El robot primero gira 360° registrando qué marcadores ve y en qué
dirección están. Luego navega en secuencia hacia cada marcador
usando el mapa para girar directamente hacia él.

Uso (en la Pi):
    python3 scripts/navegacion_mapeada.py --ids 0 1 2
    python3 scripts/navegacion_mapeada.py --ids 0 1 2 --pausa 3
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from navegacion_aruco.navegacion.navegador import Navegador
from navegacion_aruco.vision.pipeline import Pipeline

VELOCIDAD_ESCANEO = 0.25
TIEMPO_ESCANEO = 6.0  # segundos para girar ~360°
MUESTRAS_POR_FRAME = 3  # lecturas por posición para reducir ruido


def escanear_ambiente(pipeline: Pipeline, ids_objetivo: list[int]) -> dict[int, float]:
    """
    Gira 360° y registra qué marcadores son visibles y en qué ángulo.

    Returns:
        Diccionario {id: angulo_deg} de marcadores detectados.
    """
    from navegacion_aruco.control.motor_driver import MotorDriver

    print("\nEscaneando ambiente...")
    mapa = {}
    detecciones: dict[int, list[float]] = {id: [] for id in ids_objetivo}

    with MotorDriver() as motores:
        motores.girar_derecha(VELOCIDAD_ESCANEO)
        inicio = time.monotonic()

        while time.monotonic() - inicio < TIEMPO_ESCANEO:
            for _ in range(MUESTRAS_POR_FRAME):
                observaciones = pipeline.observar_todos()
                for obs in observaciones:
                    if obs.id in ids_objetivo:
                        detecciones[obs.id].append(obs.angulo_deg)

            tiempo = time.monotonic() - inicio
            progreso = int((tiempo / TIEMPO_ESCANEO) * 20)
            barra = "█" * progreso + "░" * (20 - progreso)
            print(f"\r  Escaneando [{barra}] {tiempo:.1f}s", end="")
            time.sleep(0.1)

        motores.detener()

    print("\n")

    # Calcular ángulo promedio para cada marcador detectado
    for id_marcador, angulos in detecciones.items():
        if angulos:
            promedio = sum(angulos) / len(angulos)
            mapa[id_marcador] = round(promedio, 1)
            print(f"  Marcador ID:{id_marcador} → ángulo promedio: {promedio:+.1f}°")
        else:
            print(f"  Marcador ID:{id_marcador} → NO detectado")

    return mapa


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Navegación mapeada con escaneo inicial del ambiente"
    )
    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        required=True,
        help="Lista de IDs de marcadores en orden (ej: --ids 0 1 2)",
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

    print("=== Navegación mapeada ===")
    print(f"Secuencia: {' → '.join(str(i) for i in args.ids)}")
    print(f"Pausa entre marcadores: {args.pausa}s\n")

    # Escaneo inicial
    with Pipeline() as pipeline:
        mapa = escanear_ambiente(pipeline, args.ids)

    if not mapa:
        print("No se detectó ningún marcador. Verifica el ambiente.")
        sys.exit(1)

    print(f"\nMapa generado: {mapa}")
    marcadores_no_encontrados = [id for id in args.ids if id not in mapa]
    if marcadores_no_encontrados:
        print(f"ADVERTENCIA: marcadores no detectados: {marcadores_no_encontrados}")

    input("\nPresiona ENTER para iniciar la secuencia...")

    # Navegación en secuencia
    completados = 0
    fallidos = []

    with Navegador() as navegador:
        for i, id_objetivo in enumerate(args.ids):
            if id_objetivo not in mapa:
                print(
                    f"\n[{i+1}/{len(args.ids)}] Marcador ID:{id_objetivo} no está en el mapa — saltando"
                )
                fallidos.append(id_objetivo)
                continue

            print(
                f"\n[{i+1}/{len(args.ids)}] Navegando hacia marcador ID:{id_objetivo}"
            )
            exito = navegador.navegar_hacia(id_objetivo)

            if exito:
                completados += 1
                print(f"✓ Llegado al marcador ID:{id_objetivo}")
                if i < len(args.ids) - 1:
                    print(f"Esperando {args.pausa}s...")
                    time.sleep(args.pausa)
            else:
                fallidos.append(id_objetivo)
                print(f"✗ No se encontró marcador ID:{id_objetivo}")

    print("\n=== Resumen ===")
    print(f"Completados: {completados}/{len(args.ids)}")
    if fallidos:
        print(f"Fallidos: {fallidos}")


if __name__ == "__main__":
    main()
