# Sistema — cómo ejecutarlo

Aplicación web en **Python + Django** organizada en tres capas:

| Capa | Dónde está |
|---|---|
| Presentación | `templates/` y `views.py` de cada módulo |
| Lógica de negocio | `servicios.py` y `permisos.py` de cada módulo |
| Persistencia | `models.py` de cada módulo (SQLite en desarrollo) |

Cada módulo del diseño es una aplicación dentro de `apps/`:

| Carpeta | Módulo | Estado | Responsable |
|---|---|---|---|
| `apps/usuarios` | Usuarios y Roles (US-01, US-02) | ✅ Funcionando | Leidy |
| `apps/productos` | Gestión de Productos (PR-01 a PR-04) | ✅ Funcionando | Jannin |
| `apps/inventario` | Gestión de Inventario (IN-01 a IN-04) | Pendiente | Jannin |
| `apps/ventas` | Gestión de Ventas (VE-01 a VE-04) | Pendiente | Liseth |
| `apps/clientes` | Gestión de Clientes (CL-01, CL-02) | Pendiente | Liseth |
| `apps/compras` | Compras y Proveedores (CP-01, CP-02) | Pendiente | Liseth |
| `apps/caja` | Caja (CJ-01 a CJ-03) | Pendiente | Leidy |
| `apps/reportes` | Reportes (RE-01 a RE-03) | Pendiente | Leidy |

## Instalación

Se necesita Python 3.10 o superior.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego abrir http://127.0.0.1:8000 e ingresar con el usuario creado.

## Pruebas

```bash
python manage.py test
```

Hay 14 pruebas automáticas: 11 del módulo de Productos y 3 de Usuarios y Roles.

## Roles

| Rol | Puede |
|---|---|
| Administrador | Todo el sistema, incluidos precios y usuarios |
| Vendedor | Ventas, clientes, caja y consultar productos |
| Encargado de bodega | Productos, inventario y compras (no cambia precios) |
