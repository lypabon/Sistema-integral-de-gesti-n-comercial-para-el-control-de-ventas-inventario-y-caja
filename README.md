# Sistema integral de gestión comercial para el control de ventas, inventario y caja

Proyecto semestral de **Arquitectura de Software** — Ingeniería de Sistemas, Unidades Tecnológicas de Santander (UTS).
Docente: **Edward Villamizar** · Bucaramanga, 2026.

## Equipo

| Integrante | Rol en el proyecto |
|---|---|
| Leidy Yulieth Pabón Antolínez | Coordinación, dueña del repositorio, integración del documento final |
| Liseth Dayana Martínez Rueda | Procesos, diagramas de flujo y ciclo PHVA |
| Jannin Katerine Méndez Hernández | Diagnóstico de calidad e indicadores |

La división completa de actividades está en [`docs/PLAN_DE_TRABAJO.md`](docs/PLAN_DE_TRABAJO.md).

## ¿Qué problema resuelve?

Muchos comercios minoristas (tiendas de ropa, papelerías, ferreterías, minimercados) llevan sus ventas, inventario y caja en cuadernos u hojas de cálculo aisladas. Eso genera mercancía perdida de vista, descuadres de caja, incertidumbre sobre el stock real y poca claridad sobre las ganancias.

Este sistema centraliza toda la operación del comercio en un solo lugar: recibir mercancía, controlar el inventario, vender al detal, procesar pagos, cuadrar la caja y generar reportes para tomar decisiones.

**Usuarios:** administrador/dueño, vendedores y encargado de bodega (los clientes participan de forma indirecta).

## Módulos del sistema

![Mapa de módulos](docs/img/mapa-modulos.jpg)

| Código | Módulo | Funcionalidades |
|---|---|---|
| PR | Gestión de Productos | PR-01 a PR-04 |
| IN | Gestión de Inventario | IN-01 a IN-04 |
| VE | Gestión de Ventas | VE-01 a VE-04 |
| CL | Gestión de Clientes | CL-01 a CL-02 |
| CP | Compras y Proveedores | CP-01 a CP-02 |
| CJ | Caja | CJ-01 a CJ-03 |
| RE | Reportes | RE-01 a RE-03 |
| US | Usuarios y Roles | US-01 a US-02 |

**Arquitectura propuesta:** tres capas (presentación, lógica de negocio y persistencia), con la capa de negocio dividida por módulos de bajo acoplamiento. Atributos de calidad prioritarios: fiabilidad, seguridad, usabilidad y mantenibilidad.

El detalle está en el trabajo escrito del Parcial 1: [`docs/parcial-1/Parcial_1_Corte1_AS.docx`](docs/parcial-1/Parcial_1_Corte1_AS.docx).

## Avances

| Avance | Contenido | Estado |
|---|---|---|
| [Avance 1](docs/avances/AVANCE_01.md) | Organización del repositorio, división de actividades y roadmap | ✅ Entregado |
| Avance 2 | Puntos 1, 2 y 3 del Parcial 3 + arranque del MVP | ⏳ Pendiente |
| Avance 3 | Puntos 4, 5, 6 y 7 + módulos del flujo de venta | ⏳ Pendiente |
| Avance 4 | Punto 8, integración y entrega del PDF final | ⏳ Pendiente |

Ver el plan completo en [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Estructura del repositorio

```
├── README.md
├── CONTRIBUTING.md          # Convenciones de ramas, commits e issues
└── docs/
    ├── PLAN_DE_TRABAJO.md   # Quién hace qué
    ├── ROADMAP.md           # Fases, fechas y entregables
    ├── avances/             # Registro de cada avance
    ├── img/                 # Imágenes y diagramas
    └── parcial-1/           # Trabajo escrito base (Corte 1)
```
