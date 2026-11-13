# Convenciones de trabajo

Estas reglas sirven para trabajar ordenadas y, además, para que el repositorio deje la evidencia que pide el Parcial 3 (Puntos 4 y 7): quién hizo qué, cuándo, cuántos errores hubo y cuánto se tardó en corregirlos.

## Ramas

- `main`: versión estable. No se trabaja directamente en ella.
- Una rama por tarea, con este formato:
  - `docs/p3-procesos` — documentación de un apartado
  - `feat/ventas-registro` — nueva funcionalidad
  - `fix/caja-cierre-descuadre` — corrección de un error

## Commits

Formato: `tipo(alcance): descripción corta en presente`

| Tipo | Uso | Ejemplo |
|---|---|---|
| `docs` | Documentación | `docs(p4): agrega problemas 1 a 5 del diagnóstico` |
| `feat` | Funcionalidad nueva | `feat(VE-01): crea registro de venta` |
| `fix` | Corrección de error | `fix(CJ-02): corrige cálculo de descuadre` |
| `test` | Pruebas | `test(IN-02): prueba descuento de stock por venta` |
| `chore` | Configuración y orden | `chore: agrega estructura de carpetas` |

Usar el código de la funcionalidad (PR-01, VE-03, …) cuando aplique. Así cada cambio queda trazado a la matriz funcional.

## Issues (tareas)

- Cada actividad del [plan de trabajo](docs/PLAN_DE_TRABAJO.md) es un issue.
- Etiquetas sugeridas:
  - Responsable: `leidy`, `liseth`, `jannin`
  - Avance: `avance-1`, `avance-2`, `avance-3`, `avance-4`
  - Tipo: `documentación`, `desarrollo`, `error`
- Al cerrar un issue, dejar un comentario corto con lo que se hizo o el enlace al commit.

## Pull requests

1. Subir la rama y abrir el pull request hacia `main`.
2. Asignar como revisora a otra integrante (Leidy → Liseth → Jannin → Leidy).
3. Fusionar solo después de la revisión.

## Registro de avances

Al cerrar cada avance, crear `docs/avances/AVANCE_0X.md` con lo entregado, responsables, problemas encontrados y fecha.
