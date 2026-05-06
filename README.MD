# Ecommerce Automation – UI + API

Este proyecto combina pruebas de API y pruebas de UI para un sitio de ecommerce.

## Setup

```bash
cd /home/mariel/MyProject/ecommerce
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus datos
```
## Setup en CodeSpace de GitHUb

```
Troubleshooting: Chromium no levanta en GitHub Codespaces
Si al correr los tests de UI aparece este error:
error while loading shared libraries: libatk-1.0.so.0: cannot open shared object file
Es porque el contenedor del Codespace no tiene las dependencias del sistema que Chromium necesita. Instalarse con:

´´´bash
sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2t64

Nota: No usar apt-get update antes de este comando si el repo de yarn está configurado en el Codespace, ya que el update falla por un error de firma GPG y corta la ejecución antes de llegar al install.

Verificar que quedó instalado:
bashldconfig -p | grep libatk
Debe aparecer libatk-1.0.so.0 en el output. Luego correr los tests normalmente.

```

## Ejecutar los tests

```bash
# Todos los tests
pytest tests/ -v

# Solo pruebas de API
pytest tests/api/ -v

# Solo pruebas de UI
pytest tests/ui/ -v

# Generar reporte HTML de pytest
pytest --html=python-report/report.html --self-contained-html

# Ejecutar tests y abrir el reporte automáticamente
python3 run_tests_open_report.py
```

## Reportes disponibles

- `python-report/report.html` – reporte HTML generado por `pytest-html`.
- `ecommerce_covarege_test_case.html` – reporte de cobertura de casos y decisiones estratégicas.

## Estructura del proyecto

```
ecommerce/
├── conftest.py
├── requirements.txt
├── .env.example
├── pytest.ini
├── run_tests_open_report.py
├── services/
│   ├── __init__.py
│   ├── api_client.py
│   ├── api_ecommrce.json
│   ├── api_products.json
│   ├── api_brands.json
│   ├── api_login.json
│   └── api_user_crud.json
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── home_page.py
├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── test_api_products.py
│   │   └── test_example.py
│   └── ui/
│       ├── __init__.py
│       └── test_ui_home.py
├── fixtures/
├── models/
└── python-report/
```

> Los endpoints de Postman se han dividido en 4 archivos JSON por funcionalidad:
> `api_products.json`, `api_brands.json`, `api_login.json` y `api_user_crud.json`.

## Convenciones principales

- `tests/api/` para pruebas de servicios REST.
- `tests/ui/` para pruebas de interfaz con Playwright.
- `pages/` para Page Objects de UI.
- `services/api_client.py` para la lógica común de llamadas HTTP.
- `conftest.py` para fixtures reutilizables como `api_base_url`, `ui_base_url` y credenciales.

## Cobertura de casos y decisiones estratégicas

[Ver Reporte Interactivo](https://mariel-test.github.io/ecommerce-python-complete/ecommerce_coverage_test_case.html)

- El set completo suma 52 casos de prueba: 15 de Usuarios, 10 de Autenticación, 10 de Productos, 5 de Marcas, 5 flujos E2E y 12 de UI/Integración.
- La lógica de triaje por tiempo funciona así:
  - Con tiempo al 50% (30 TC) ejecutás todos los S1 más los S2 del camino crítico y los 5 flujos E2E. Es el punto de equilibrio ideal: cubrís el 100% de lo que puede bloquear un release y el ~85% del riesgo de negocio real.
  - Con tiempo al 25% (16 TC) bajás a solo el camino feliz de cada módulo más E2E-01 y E2E-04. Esto confirma que el flujo de conversión principal está vivo, pero deja expuesto el manejo de errores.
  - El smoke de 8 TC es la red de seguridad mínima antes de un deploy: 1 caso por módulo + el E2E completo de ciclo de vida. Si algo falla acá, el release no sale.
- Regla de oro para el triaje: los S1 no se negocian. Los que se pueden diferir sin demasiado riesgo son los casos de método no soportado (405), los de borde con inputs muy largos o caracteres raros, y los de consistencia cross-endpoint, porque esos suelen ser más estables una vez que el camino crítico pasa.

---

## Catálogo completo de casos de prueba

**52 TC en total** — 🔥 Smoke (8 TC) · ⚡ Al 25% (16 TC)

> Los 16 TC al 25% incluyen todos los 8 smoke. Los 8 smoke cubren 1 caso por área funcional + E2E-01 completo.

### Usuarios CRUD — 15 TC

| ID | Nombre del caso | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|:---:|:---:|
| TC-USR-01 | Registro exitoso con todos los campos válidos | responseCode 201, message "User created!" | S1 | P1 | 🔥 | ⚡ |
| TC-USR-02 | Registro con email ya existente | responseCode 400, mensaje de email duplicado | S1 | P1 | | |
| TC-USR-03 | Registro con campos obligatorios vacíos | responseCode 400, mensaje de campo faltante | S2 | P1 | | |
| TC-USR-04 | Registro con email inválido (sin @) | responseCode 400, validación de formato | S2 | P2 | | |
| TC-USR-05 | Obtener detalle de usuario existente | responseCode 200, objeto user con email y name correctos | S1 | P1 | | ⚡ |
| TC-USR-06 | Obtener detalle de usuario inexistente | responseCode 404, mensaje de usuario no encontrado | S2 | P2 | | |
| TC-USR-07 | Obtener detalle sin parámetro email | responseCode 400, parámetro faltante | S2 | P2 | | |
| TC-USR-08 | Actualizar usuario con datos válidos | responseCode 200, message "User updated!" | S1 | P1 | | ⚡ |
| TC-USR-09 | Actualizar usuario inexistente | responseCode 404, usuario no encontrado | S2 | P2 | | |
| TC-USR-10 | Actualizar sin campos requeridos | responseCode 400, validación de campos | S2 | P2 | | |
| TC-USR-11 | Eliminar cuenta con credenciales correctas | responseCode 200, message "Account deleted!" | S1 | P1 | 🔥 | ⚡ |
| TC-USR-12 | Eliminar cuenta con password incorrecto | responseCode 401/403, acceso denegado | S1 | P1 | | |
| TC-USR-13 | Eliminar usuario inexistente | responseCode 404, usuario no encontrado | S2 | P2 | | |
| TC-USR-14 | Idempotencia: eliminar cuenta ya eliminada | responseCode 404, no error 500 | S2 | P2 | | |
| TC-USR-15 | Verificar persistencia post-actualización | Nuevos datos reflejados correctamente en GET posterior | S1 | P1 | | ⚡ |

### Autenticación — 10 TC

| ID | Nombre del caso | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|:---:|:---:|
| TC-AUTH-01 | Login con credenciales válidas | responseCode 200, message "User exists!" | S1 | P1 | 🔥 | ⚡ |
| TC-AUTH-02 | Login con email inexistente | responseCode 404, message "User not found!" | S1 | P1 | | |
| TC-AUTH-03 | Login con password incorrecto | responseCode 404, message "User not found!" | S1 | P1 | | |
| TC-AUTH-04 | Login sin parámetro email | responseCode 400, parámetro faltante | S2 | P2 | | |
| TC-AUTH-05 | Login sin parámetro password | responseCode 400, parámetro faltante | S2 | P2 | | |
| TC-AUTH-06 | Login sin body (request vacío) | responseCode 400, no error 500 | S2 | P2 | | |
| TC-AUTH-07 | Method not allowed: DELETE en /verifyLogin | responseCode 405, "This request method is not supported" | S3 | P3 | | |
| TC-AUTH-08 | Login con email en formato vacío "" | responseCode 400, parámetro inválido | S2 | P2 | | |
| TC-AUTH-09 | Login con password en mayúsculas (case sensitivity) | responseCode 404, passwords son case-sensitive | S3 | P3 | | |
| TC-AUTH-10 | Login luego de eliminar la cuenta | responseCode 404, "User not found!" | S1 | P1 | | |

### Productos — 10 TC

| ID | Nombre del caso | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|:---:|:---:|
| TC-PROD-01 | Listar todos los productos | responseCode 200, array products no vacío con id/name/price/brand/category | S1 | P1 | 🔥 | ⚡ |
| TC-PROD-02 | Estructura del objeto producto completa | Cada producto contiene id, name, price, brand, category (no nulos) | S1 | P1 | | ⚡ |
| TC-PROD-03 | Method not allowed: POST en /productsList | responseCode 405, método no soportado | S3 | P3 | | |
| TC-PROD-04 | Buscar producto con término válido "top" | responseCode 200, array products con resultados relevantes | S1 | P1 | 🔥 | ⚡ |
| TC-PROD-05 | Buscar producto con término "tshirt" | responseCode 200, productos de tipo tshirt | S1 | P1 | | ⚡ |
| TC-PROD-06 | Buscar sin parámetro search_product | responseCode 400, "search_product parameter is missing" | S2 | P2 | | |
| TC-PROD-07 | Buscar término sin resultados | responseCode 200, products array vacío | S2 | P2 | | |
| TC-PROD-08 | Buscar con caracteres especiales (SQLi) | responseCode 400 o 200 con array vacío, sin error 500 | S1 | P1 | | |
| TC-PROD-09 | Buscar con término muy largo (+500 chars) | Respuesta sin error 500, manejo gracioso | S2 | P3 | | |
| TC-PROD-10 | Verificar precios son valores numéricos positivos | Todos los productos tienen price > 0, formato "Rs. X" | S2 | P2 | | |

### Marcas — 5 TC

| ID | Nombre del caso | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|:---:|:---:|
| TC-BRAND-01 | Listar todas las marcas | responseCode 200, array brands no vacío con id y brand | S1 | P1 | 🔥 | ⚡ |
| TC-BRAND-02 | Estructura del objeto brand completa | Cada brand tiene id (int) y brand (string no vacío) | S2 | P2 | | |
| TC-BRAND-03 | Method not allowed: PUT en /brandsList | responseCode 405, método no soportado | S3 | P3 | | |
| TC-BRAND-04 | IDs de marcas son únicos y no duplicados | Todos los brand.id son únicos en el array | S2 | P3 | | |
| TC-BRAND-05 | Marcas de /brandsList coinciden con /productsList | Todas las marcas de productos existen en brandsList | S2 | P2 | | |

### Flujos E2E — 5 TC

| ID | Nombre del flujo | Pasos clave | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|---|:---:|:---:|
| E2E-01 | Ciclo completo de vida de usuario | createAccount → verifyLogin → getUserDetail → updateAccount → getUserDetail → deleteAccount → verifyLogin | Todos los pasos retornan códigos esperados; cuenta inexistente tras delete | S1 | P1 | 🔥 | ⚡ |
| E2E-02 | Búsqueda y catálogo como usuario autenticado | createAccount → verifyLogin → productsList → brandsList → searchProduct → deleteAccount | Catálogo y búsqueda accesibles; cleanup exitoso | S1 | P1 | | |
| E2E-03 | Intento de registro bloqueado por duplicado | createAccount (201) → createAccount mismo email (400) → verifyLogin cuenta original | Duplicado bloqueado; login original sigue funcionando | S2 | P2 | | |
| E2E-04 | Sesión inválida: acceso post-eliminación | createAccount → deleteAccount → verifyLogin → getUserDetail → updateAccount | Todas las operaciones retornan 404 tras eliminar la cuenta | S1 | P1 | | ⚡ |
| E2E-05 | Consistencia de datos cross-endpoint | GET productsList → GET brandsList → comparar sets → searchProduct | brands(productos) ⊆ brandsList; resultados de búsqueda tienen marcas válidas | S2 | P2 | | |

### UI + Integración — 12 TC

| ID | Nombre del caso | Resultado esperado | Sev | Prio | 🔥 | ⚡ |
|---|---|---|---|---|:---:|:---:|
| TC-UI-01 | Formulario de registro: campos requeridos marcados | Validación HTML5 + mensajes de error visibles antes del request | S1 | P1 | | ⚡ |
| TC-UI-02 | Mensaje de éxito post-registro | UI renderiza "Account Created!" y redirige sin quedarse en pantalla de carga | S1 | P1 | | |
| TC-UI-03 | Login fallido: mensaje claro de error | "Email or password is incorrect!" visible sin redirección ni recarga | S1 | P1 | | |
| TC-UI-04 | Catálogo carga productos del API | Número de cards = total_products del API, sin cards vacías | S1 | P1 | 🔥 | ⚡ |
| TC-UI-05 | Barra de búsqueda: muestra resultados | UI muestra solo productos del array retornado por la API | S1 | P1 | | ⚡ |
| TC-UI-06 | Búsqueda sin resultados: estado vacío | "No products found" visible, sin errores de consola | S2 | P2 | | |
| TC-UI-07 | Filtro por marcas en sidebar | Solo se muestran productos cuyo brand coincide con el seleccionado | S2 | P2 | | |
| TC-UI-08 | Eliminación de cuenta desde perfil | Sesión invalidada, redirección a home, no se puede volver sin login | S1 | P1 | | |
| TC-UI-09 | Timeout de API: UI no se congela | Spinner y mensaje de error visible; UI no queda en estado de carga indefinido | S2 | P2 | | |
| TC-UI-10 | Responsive: catálogo en mobile | Cards sin overflow horizontal en viewport 375px y 768px | S2 | P3 | | |
| TC-UI-11 | Persistencia de sesión post-actualización de perfil | Nombre en navbar se actualiza tras el PUT sin cerrar sesión | S1 | P1 | | |
| TC-UI-12 | Seguridad: campos de password no quedan en localStorage | Password ausente en localStorage/sessionStorage tras login exitoso | S1 | P1 | | |

---

### Resumen de triaje

| Nivel | TC | Qué cubre |
|---|:---:|---|
| 🔥 Smoke | 8 | 1 caso por área funcional + E2E completo. Red mínima antes de deploy; si algo falla acá el release no sale. |
| ⚡ 25% | 16 | Smoke + camino feliz de cada módulo + E2E-04. Confirma que el flujo de conversión principal está vivo. |
| 50% | 30 | Todos los S1 + S2 de camino crítico + 5 flujos E2E. Cubre ~85% del riesgo de negocio. |
| 100% | 52 | Set completo: bordes, seguridad, rendimiento, consistencia cross-endpoint y responsive. |
