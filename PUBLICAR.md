# Publicar el dashboard

Configuración prevista del repositorio y la aplicación:

| Campo | Valor |
| --- | --- |
| Cuenta propietaria | `Fhasivia` |
| Repositorio | `Fhasivia/eafit-iot-dashboard` |
| Rama | `main` |
| Archivo principal | `app.py` |
| Versión de Python | `3.12` |
| Dependencias | `requirements.txt` |
| Secretos de la aplicación | No requiere |

## GitHub

La carpeta `eafit-iot` debe ser la raíz del repositorio. Se incluyen el código, el CSV, los estilos, el logo local y `.streamlit/config.toml`.

El repositorio está en https://github.com/Fhasivia/eafit-iot-dashboard. No se deben publicar el entorno de Python, credenciales ni el contenido de otras carpetas del proyecto.

Si se suben los archivos mediante la web de GitHub, comprobar que `.streamlit/config.toml` y `.gitignore` también estén presentes. Al subir mediante Git se conservan ambos archivos ocultos.

## Streamlit Community Cloud

1. Iniciar sesión en https://share.streamlit.io con la cuenta que tenga acceso al repositorio.
2. Elegir **Create app** y **Yup, I have an app**.
3. Seleccionar el repositorio, la rama `main` y el archivo `app.py`.
4. En **Advanced settings**, elegir **Python 3.12**. El campo de secretos se deja vacío.
5. Elegir un subdominio disponible o conservar el que asigne Streamlit.
6. Desplegar y esperar a que la aplicación termine de iniciar.

Si aparece una autorización nueva de GitHub, revisar y completar esa autorización desde la cuenta del propietario. Esta guía no contiene credenciales.

## Comprobar la aplicación publicada

| Caso | Resultado esperado |
| --- | --- |
| Sin filtros | 2.667 mediciones, 295 estudiantes, 97,11% válidas, 75,47 BPM y 97,72% SpO₂ |
| Sólo `invalid` | 77 mediciones, 67 estudiantes, 0% válidas y promedios sin datos |
| Estudiante `EST-0241` | 21 mediciones y un estudiante |
| Sólo el 29/09/2026 | 10 mediciones, usando fecha de Bogotá |
| Ningún estado seleccionado | Mensaje de selección vacía, sin indicadores |
| Exportación del estudiante `EST-0241` | 21 filas, además del encabezado, aunque la vista previa muestre cinco |
| Seguimiento individual | El estudiante y sus gráficos respetan los filtros |
| Cabecera | Logo EAFIT cargado y bloques centrados en escritorio y móvil |

Después de publicar, abrir el enlace en una ventana sin sesión para verificar el acceso que tendrá el docente. Registrar los enlaces definitivos de GitHub, Streamlit y video en los medios de entrega que indique la rúbrica.

## Validación local

Comprobación realizada el 5 de noviembre de 2026 en un entorno nuevo de macOS con Python 3.12.14 y las versiones de `requirements.txt`: diez pruebas aprobadas y ninguna dependencia incompatible detectada por `pip check`. Se verificaron los 28 archivos preparados, la inclusión del logo y de `.streamlit/config.toml`, y la huella original del CSV. Esto corresponde a validación local; el despliegue remoto todavía no se ha realizado.

Desde la raíz del repositorio, con las dependencias instaladas:

```bash
python -m unittest discover -s tests -v
streamlit run app.py
```

## Pendientes académicos

- Cotejar los cinco KPI implementados con el listado exacto de la rúbrica.
- Incorporar nombres de integrantes y datos del curso donde lo exija la entrega.
- Preparar el guion y el video de 5 a 8 minutos.

Fuentes: [despliegue oficial](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) y [dependencias oficiales](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).
