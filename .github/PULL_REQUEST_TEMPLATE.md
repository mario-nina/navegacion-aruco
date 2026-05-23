## Descripción

<!-- Qué hace este PR y por qué -->

## Issue relacionado

Closes #

## Tipo de cambio

- [ ] Nueva feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Refactor (`refactor`)
- [ ] Documentación (`docs`)
- [ ] Ajuste de parámetros (`tune`)
- [ ] Infraestructura / CI (`chore`)

## Checklist

### Código
- [ ] El código pasa `ruff check` sin errores
- [ ] No hay `print()` de debug en el código final
- [ ] Las funciones y clases nuevas tienen docstrings

### Tests
- [ ] Los tests unitarios pasan: `pytest tests/unit/ -v`
- [ ] Si modifica visión: probado en la Pi con cámara real
- [ ] Si modifica control: probado en la Pi con motores conectados

### Documentación
- [ ] `CHANGELOG.md` actualizado bajo `[Unreleased]`
- [ ] `docs/` actualizado si cambió arquitectura o conexiones
