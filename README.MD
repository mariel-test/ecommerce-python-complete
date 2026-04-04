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

[🚀 Ver Reporte Interactivo](https://tu-usuario.github.io/ecommerce-paython-complet/ecommerce_covarege_test_case.html)

- El set completo suma 52 casos de prueba: 15 de Usuarios, 10 de Autenticación, 10 de Productos, 5 de Marcas, 5 flujos E2E y 12 de UI/Integración.
- La lógica de triaje por tiempo funciona así:
  - Con tiempo al 50% (30 TC) ejecutás todos los S1 más los S2 del camino crítico y los 5 flujos E2E. Es el punto de equilibrio ideal: cubrís el 100% de lo que puede bloquear un release y el ~85% del riesgo de negocio real.
  - Con tiempo al 25% (16 TC) bajás a solo el camino feliz de cada módulo más E2E-01 y E2E-04. Esto confirma que el flujo de conversión principal está vivo, pero deja expuesto el manejo de errores.
  - El smoke de 8 TC es la red de seguridad mínima antes de un deploy: 1 caso por módulo + el E2E completo de ciclo de vida. Si algo falla acá, el release no sale.
- Regla de oro para el triaje: los S1 no se negocian. Los que se pueden diferir sin demasiado riesgo son los casos de método no soportado (405), los de borde con inputs muy largos o caracteres raros, y los de consistencia cross-endpoint, porque esos suelen ser más estables una vez que el camino crítico pasa.
