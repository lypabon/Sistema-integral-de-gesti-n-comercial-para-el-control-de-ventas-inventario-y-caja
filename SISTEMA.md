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
| `apps/inventario` | Gestión de Inventario (IN-01 a IN-04) | ✅ Funcionando | Jannin |
| `apps/ventas` | Gestión de Ventas (VE-01 a VE-04) | ✅ Funcionando | Liseth |
| `apps/clientes` | Gestión de Clientes (CL-01, CL-02) | Pendiente | Liseth |
| `apps/compras` | Compras y Proveedores (CP-01, CP-02) | Pendiente | Liseth |
| `apps/caja` | Caja (CJ-01 a CJ-03) | ✅ Funcionando | Leidy |
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

Hay 43 pruebas automáticas y cubren el 84,9 % del código de `apps/` (sin contar migraciones):

| Módulo | Pruebas |
|---|---|
| Productos | 11 |
| Usuarios y Roles | 3 |
| Inventario | 9 |
| Caja | 7 |
| Ventas | 13 |

Para medir la cobertura:

```bash
pip install coverage
coverage run --source=apps manage.py test
coverage report --omit="*/migrations/*"
```

## Flujo de uso

1. El encargado de bodega registra productos y sus entradas de inventario.
2. El vendedor abre su caja con el fondo inicial.
3. El vendedor registra ventas; cada venta descuenta el inventario y suma el cobro a su caja.
4. Al final del turno, el vendedor cuenta el efectivo y cierra la caja; el sistema calcula el descuadre.

## Reglas de negocio configurables

En `gestion_comercial/settings.py`:

| Variable | Valor | Significado |
|---|---|---|
| `VENTAS_IVA` | `0.19` | IVA aplicado sobre el valor con descuento |
| `VENTAS_DESCUENTO_MAX` | `10` | Descuento máximo que puede dar un vendedor, en % |

## Roles

| Rol | Puede |
|---|---|
| Administrador | Todo el sistema, incluidos precios y usuarios |
| Vendedor | Ventas, clientes, caja y consultar productos |
| Encargado de bodega | Productos, inventario y compras (no cambia precios) |
