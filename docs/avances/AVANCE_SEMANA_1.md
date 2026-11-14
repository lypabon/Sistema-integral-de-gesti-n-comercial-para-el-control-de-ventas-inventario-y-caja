# Avance Semana 1 — Modelo de negocio, descomposición funcional, procesos y base del sistema

**Responsables:** Leidy Pabón, Liseth Martínez, Jannin Méndez

## Qué se entregó

| Entregable | Responsable | Estado |
|---|---|---|
| Punto 1. Modelo de negocio | Leidy | Completo |
| Punto 2. Matriz de descomposición funcional (8 módulos, 20 submódulos, 24 funcionalidades) | Leidy | Completo |
| Punto 2. Fichas de las 24 funcionalidades | Leidy, Liseth y Jannin | Completo |
| Punto 3. Inventario de los 10 procesos | Liseth | Completo |
| Punto 3. Ficha completa de 5 procesos (PN-01, PN-04, PN-05, PS-08, PD-09) | Liseth | 5 de 10 |
| Decisión de tecnología ADR-001: Python + Django | Todas | Aceptada |
| Estructura del sistema en tres capas, un módulo por carpeta en `apps/` | Leidy | Completo |
| Módulo Usuarios y Roles (US-01, US-02) | Leidy | Funcionando |
| Módulo Gestión de Productos (PR-01 a PR-04) | Jannin | Funcionando |

El documento completo está en [`AVANCE_SEMANA_1.pdf`](AVANCE_SEMANA_1.pdf).

## Decisión de tecnología

Se eligió **Python 3 + Django 5** porque trae incluidos el inicio de sesión, el cifrado de contraseñas, la protección contra ataques comunes y las pruebas automáticas, y permite separar cada módulo en su propia aplicación.

- *Trade-off:* interfaz menos dinámica que una aplicación React y aplicación monolítica; separar servicios en el futuro costaría de 2 a 3 semanas de trabajo.

## Verificación

14 pruebas automáticas aprobadas (`python manage.py test`): 8 de PR-01 a PR-04, 1 de US-01 y 5 de US-02.

## Pendientes para la Semana 2

- [ ] Liseth: fichas de PN-02, PN-03, PN-06, PN-07 y PD-10, y diagramas de flujo de PN-04 y PN-05.
- [ ] Jannin: Punto 4 (diagnóstico) y Punto 7 (indicadores).
- [ ] Leidy: iniciar el Punto 5 (CMMI y NTC 5802).
- [ ] Desarrollo: módulos de Inventario (Jannin), Ventas (Liseth) y Caja (Leidy).
