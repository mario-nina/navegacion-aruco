# Guía de calibración de la cámara

## ¿Por qué calibrar?

La calibración obtiene los parámetros intrínsecos de la cámara — la matriz
de cámara y los coeficientes de distorsión del lente. Sin estos parámetros,
la estimación de distancia y ángulo a los marcadores ArUco tiene errores
sistemáticos de 10-30%.

Los parámetros se calculan una sola vez y se guardan en
`config/camera_calibration.npz`. Se recalibra solo si se cambia la cámara
o el ángulo de montaje.

## Materiales necesarios

- Tablero de ajedrez impreso (generado con `calibracion/generar_tablero.py`)
- Superficie rígida y plana para pegar el tablero
- Regla para medir el tamaño real de un cuadro
- Robot con la cámara montada en su posición final

## Detalles del tablero utilizado

- Cuadros: 10×7
- Tamaño real por cuadro: 26 mm
- Esquinas internas detectables: 9×6

## Procedimiento

### Paso 1 — Preparar el tablero

1. Ejecutar `python3 calibracion/generar_tablero.py`
2. Imprimir `calibracion/tablero_calibracion.png` al 100% de escala
3. Pegar sobre superficie rígida y plana sin arrugas
4. Medir con regla el tamaño real de un cuadro y verificar que sea 26mm

### Paso 2 — Capturar imágenes

```bash
# En la Pi, con el entorno virtual activado
source .venv/bin/activate
python3 calibracion/capturar_imagenes.py
```

Recomendaciones para las fotos:
- Objetivo: 20-25 imágenes válidas con el tablero detectado
- Variar distancia: 20cm, 40cm, 60cm
- Variar ángulo horizontal: izquierda, centro, derecha
- Variar inclinación: recto, ~30° hacia cada lado
- Variar posición en el frame: esquinas y centro
- Iluminación: la misma que tendrá el ambiente controlado

### Paso 3 — Calibrar

```bash
python3 calibracion/calibrar_camara.py
```

### Paso 4 — Verificar resultado

Error de reproyección aceptable: < 1.0 px
Error de reproyección excelente: < 0.5 px

Si el error es mayor a 1.0 px:
- Verificar que el tablero esté completamente plano
- Descartar imágenes borrosas o con tablero parcialmente fuera del frame
- Capturar más imágenes con mayor variedad de ángulos

## Archivos generados

| Archivo | Descripción |
|---|---|
| `calibracion/imagenes/` | Fotos del tablero capturadas (no versionadas) |
| `config/camera_calibration.npz` | Parámetros de calibración (no versionado) |
