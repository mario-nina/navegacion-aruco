# Registro de validación de pose

## Descripción

Mediciones del error real de distancia y ángulo estimados por el sistema
de visión, comparados contra valores reales medidos con regla y transportador.

Se completa durante la Fase 5, después de calibrar la cámara.

## Configuración de la prueba

<!-- Completar durante la Fase 5 -->

| Parámetro | Valor |
|---|---|
| Fecha | |
| Marcador ID | |
| Tamaño físico del marcador | mm |
| Diccionario ArUco | DICT_4X4_50 |
| Resolución cámara | 640×480 |
| Error de reproyección (calibración) | px |

## Validación de distancia

Marcador centrado frente a la cámara, distintas distancias reales.

| Real (cm) | Medido (cm) | Error (cm) | σ (cm) |
|---|---|---|---|
| 20 | | | |
| 30 | | | |
| 40 | | | |
| 50 | | | |
| 60 | | | |
| 80 | | | |

## Validación de ángulo

Marcador a 40 cm de distancia, distintos ángulos reales.

| Real (°) | Medido (°) | Error (°) | σ (°) |
|---|---|---|---|
| -30 | | | |
| -15 | | | |
| 0 | | | |
| +15 | | | |
| +30 | | | |

## Conclusiones

<!-- Completar después de las mediciones -->

| Métrica | Valor | Objetivo |
|---|---|---|
| Rango confiable de distancia | cm a cm | 15-80 cm |
| Error típico de distancia | ± cm | < ±3 cm |
| Error típico de ángulo | ± ° | < ±3° |
| Umbral de llegada recomendado | cm | 15 cm |
| Zona muerta angular recomendada | ± ° | ±3° |
