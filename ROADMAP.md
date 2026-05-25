# ROADMAP — navegacion-aruco

Hoja de ruta completa del proyecto de navegación autónoma con marcadores ArUco.

## Estado actual

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Infraestructura y GitHub | ✅ Completo |
| 1 | Verificación de cámara | ✅ Completo |
| 2 | Calibración de cámara | ⏸ Pendiente (requiere ambiente controlado) |
| 3 | Detección de marcadores ArUco | ✅ Completo |
| 4 | Estimación de pose | ⏳ Pendiente |
| 5 | Validación con métricas reales | ⏳ Pendiente |
| 6 | Pipeline de visión integrado | ⏳ Pendiente |
| 7 | Driver de motores L298N | ⏳ Pendiente |
| 8 | Controlador PID | ⏳ Pendiente |
| 9 | Lógica de navegación completa | ⏳ Pendiente |
| 10 | Interfaz de comando laptop → robot | ⏳ Pendiente |
| 11 | Pruebas en ambiente controlado y ajuste PID | ⏳ Pendiente |
| 12 | Preparación para presentación | ⏳ Pendiente |
| 13 | Alcance extendido (condicional) | ⏳ Pendiente |

## Hitos intermedios

| Hito | Descripción | Estado |
|---|---|---|
| Avance docente | Detección ArUco + respuesta básica de motores | ⏳ Pendiente |

## Milestones principales

| Milestone | Fases | Issues |
|---|---|---|
| M0 — Infraestructura | Fase 0 | #1 |
| M1 — Visión: Calibración y Detección | Fases 1, 2, 3 | #2, #3 |
| M2 — Visión: Pose y Validación | Fases 4, 5, 6 | |
| M3 — Control: Motores y PID | Fases 7, 8 | |
| M4 — Integración y Navegación | Fases 9, 10 | |
| M5 — Demo | Fases 11, 12 | |
| M6 — Alcance Extendido | Fase 13 | |

## Hitos académicos

| Hito | Descripción | Requisitos | Estado |
|---|---|---|---|
| Avance — Detección ArUco y respuesta de motores | Robot activa motores al detectar un ArUco específico y simula giro según posición del marcador en el frame. Sin PID ni navegación completa. | Detección ArUco (Fase 3) + control básico de motores (Fase 7) | ⏳ Pendiente |

## Notas de desarrollo

### Orden de implementación

Las fases 2 y 3 se pueden desarrollar en paralelo:
- Fase 3 (detección ArUco) no requiere calibración
- Fase 2 (calibración) requiere el ambiente controlado físico terminado
- Fase 4 (estimación de pose) requiere que la Fase 2 esté completa

### Ambiente controlado

La calibración y las pruebas finales requieren el ambiente controlado:
- Estructura física: ~1.5m × 1.5m
- Iluminación LED interior fija
- Piso de color uniforme
- Marcadores ArUco en posiciones fijas en las paredes

### Convenciones

- Commits: Conventional Commits en inglés
- Nombres de archivos y carpetas: español (excepto convenciones)
- Código: inglés para APIs de librerías, español para lógica del proyecto
- Ramas: `feature/`, `fix/` en inglés (convención Git)
