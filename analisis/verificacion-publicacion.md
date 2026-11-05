# Verificación de la publicación

5 de noviembre de 2026.

- Repositorio: https://github.com/Fhasivia/eafit-iot-dashboard
- Aplicación: https://eafit-iot-fhasivia.streamlit.app/
- Rama y archivo principal: `main`, `app.py`.
- Plataforma: Streamlit Community Cloud, opción de aplicación pública desde GitHub.
- Versión de Python configurada al desplegar: 3.12.
- Código verificado en el despliegue inicial: commit `0e71beeede82378bce78bf80ca0daea729734407`. Los cambios posteriores de esta entrega actualizan documentación.

## Archivos publicados

PASS: los 28 archivos iniciales se subieron y se verificó el SHA de cada objeto. El árbol remoto coincidió con el árbol de Git preparado localmente. Se incluyen el CSV original, el logo EAFIT, estilos, módulos, pruebas, README y `.streamlit/config.toml`. Se excluyen entornos locales y credenciales.

## Pruebas de la aplicación publicada

| Caso | Resultado observado | Estado |
| --- | --- | --- |
| Sin filtros | 2.667 mediciones, 295 estudiantes, 75,47 BPM, 97,72% SpO₂ y 97,11% válidas | PASS |
| Gráficos | Nueve componentes Plotly presentes | PASS |
| Estudiante EST-0241 | 21 mediciones, un estudiante, 96,24 BPM, 97,70% SpO₂ y 100% válidas | PASS |
| Descarga de EST-0241 | CSV real descargado: 21 filas, nueve columnas y sólo ese estudiante | PASS |
| Fechas exportadas | UTC y Bogotá representan los mismos instantes | PASS |
| Sólo invalid | 77 mediciones, 67 estudiantes, 0% válidas y ambos promedios sin datos | PASS |
| Estados vacíos | Mensaje de selección vacía y cero indicadores renderizados | PASS |
| 29/09/2026, Bogotá | Diez mediciones, nueve estudiantes, 67,40 BPM, 98,28% SpO₂ y 100% válidas | PASS |
| Seguimiento individual | Pestaña e histórico visibles | PASS |
| Calidad y registros | Pestaña y gráfico de calidad de señal visibles | PASS |
| Cabecera | Logo de Universidad EAFIT cargado | PASS |
| Vista estrecha | Ancho de documento y contenido coinciden en 400 píxeles CSS efectivos | PASS |
| Estado final | Vista de actividad, período completo y ambos estados seleccionados | PASS |
| Acceso sin credenciales | Sesión HTTP nueva sin autenticación: portada y aplicación responden 200; comprobación de salud responde 200 con `ok` | PASS |

## Pruebas locales previas

Diez pruebas automáticas aprobadas con Python 3.12.14 y las dependencias de `requirements.txt`, sin incompatibilidades detectadas por `pip check`.

## Pendientes de entrega académica

Cotejar el listado exacto de KPI con la rúbrica, completar los datos del equipo y preparar y grabar el video de 5 a 8 minutos. La publicación no sustituye esas comprobaciones académicas.
