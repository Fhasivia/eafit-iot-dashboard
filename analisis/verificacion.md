# Verificación de la primera versión local

Registro histórico de la interfaz clara inicial. La revisión del rediseño oscuro está en `../anti-slop/audit-001-2026-11-05.md`.

5 de noviembre de 2026. No verifica una publicación remota.

- PASS, cálculos: 10 pruebas de `unittest`, incluyendo los cinco KPI sin filtros, estado inválido, selección vacía, estudiante y límites de fecha en Bogotá.
- PASS, ejecución: servidor Streamlit iniciado y respuesta `ok` de su comprobación de salud.
- PASS, interacción: recorrido en navegador por las tres pestañas, fecha, estudiante, estado, selección individual por teclado, descarga y explicación desplegable.
- PASS, exportación: descarga real con 2.667 filas y 9 columnas; las marcas UTC y Bogotá representan los mismos instantes.
- PASS, original: comparación byte por byte con la descarga; huella SHA-256 en `resumen.json`.
- PASS, presentación: vistas de escritorio y móvil revisadas; en la vista estrecha el ancho del documento coincidió con el ancho de la ventana (433 píxeles CSS efectivos), sin desbordamiento horizontal de página. Temas claro y oscuro revisados. Las tablas permiten desplazamiento interno.

## Revisión antislop al terminar

### Reglas obligatorias

- R-02 PASS: el texto escrito no contiene raya larga.
- R-03 PASS: indicadores apilados, gráficos contenidos y barra lateral plegada en la vista móvil observada.
- R-17 PASS: los indicadores provienen del CSV y se contrastan en las pruebas.
- R-18 PASS: no hay testimonios.
- R-23 PASS: no se crearon logotipos, avatares ni imágenes ilustrativas; la captura muestra la aplicación real.
- R-24 PASS: no hay enlaces a páginas ficticias; las pestañas corresponden a contenido real.
- R-25 PASS: texto nativo oscuro sobre fondo claro y claro sobre oscuro; las notas se ajustaron de opacidad 0,6 a 0,85. Con el color observado rgb(49,51,63) sobre blanco, la nota supera contraste 4,5:1.
- R-26 PASS: los controles de la aplicación recalculan datos, cambian vistas, despliegan información o descargan CSV, según el recorrido registrado.
- R-27 PASS: carga con indicador, error de archivo explícito y estados vacíos implementados; selección vacía e inválidas comprobadas.
- R-28 PASS: no se añadió una sección de preguntas genéricas.
- R-32 PASS: selección por teclado comprobada con flecha y Enter; foco visible y controles nativos conservados.
- R-33 PASS: estilos escritos directamente en `app.py`, sin programas que reescriban estilos.
- R-34 PASS: temas claro y oscuro nativos revisados sin estilos de fondo o texto fijos que rompan el cambio.
- R-35 PASS: aplicación ejecutada, nueve gráficos renderizados y controles propios recorridos; diez pruebas automáticas aprobadas.
- R-36 PASS: no se hacen afirmaciones inventadas de seguridad, rendimiento o cumplimiento.
- R-37 PASS: dirección de panel académico, azul para series y ámbar para inválidas, declarada antes de construir; decisiones documentadas en README.
- R-38 PASS: los registros son los datos simulados suministrados y se identifican como tales.

### Propósito de los recursos visuales

- R-01 PASS: no hay degradados ni brillos.
- R-04 PASS: no se añadieron iconos decorativos; sólo se conservan controles nativos de las bibliotecas.
- R-06 PASS: tipografía nativa por legibilidad y compatibilidad con los temas; sin titulares monoespaciados ni espaciado ornamental.
- R-07 PASS: no hay cuadrícula de fondo decorativa; las guías de los gráficos sirven para leer cantidades.
- R-08 PASS: no hay flechas ornamentales añadidas.
- R-09 PASS: no hay distintivos promocionales.
- R-10 PASS: no hay transparencias decorativas ni desenfoques.
- R-12 PASS: no hay sombras añadidas.
- R-13 PASS: no hay resplandores.
- R-14 PASS: la fila de cinco indicadores permite comparar magnitudes; no se añadió una cuadrícula de tarjetas decorativas.
- R-19 PASS: no se añadieron animaciones; los cambios responden a los filtros.
- R-22 PASS: no hay ilustraciones genéricas.

### Jerarquía y carácter

- PASS, intensidad 1: título del análisis e indicadores dominan antes de los gráficos.
- PASS, ritmo 1: calendario a ancho completo y distribuciones en pares con unidades explícitas.
- PASS, movimiento 1: interacción y foco nativos, sin animación añadida.
- PASS, foco: el gráfico diario ocupa la zona principal de la vista de actividad.
- PASS, espacio: separación entre indicadores, filtros y preguntas de análisis.
- PASS, acento: azul para series; ámbar y marcador de cruz para mediciones inválidas.
- PASS, motivo: fecha local, estado y unidades se repiten de forma coherente en actividad, seguimiento y calidad.
- PASS, lectura de diseño: panel académico para explorar el tótem, registrada antes de implementación y en README.

### Calidad

- C-1 PASS: colores, estructura, tipografía y notas tienen motivos escritos en README.
- C-2 PASS: los controles propios tienen comportamiento comprobado.
- C-3 PASS: las secciones responden a actividad, seguimiento y calidad del conjunto suministrado.
- C-4 PASS: filtros vacíos e inválidas, vista estrecha y cambio de tema comprobados.
- C-5 PASS: métricas y conclusiones se rastrean al CSV conservado.
- R-05 PASS: organización por preguntas del análisis, sin secciones de publicidad ni contenido de relleno.
- R-11 PASS: controles nativos; no se impone forma de cápsula a todos los componentes.
- R-15 PASS: acción específica «Descargar registros filtrados (CSV)».
- R-16 PASS: no se usan reclamos publicitarios.
- R-20 PASS: variables MAX30102, estados del CSV y conversión a Bogotá determinan la interfaz.
- R-21 PASS: elección de tema disponible en Settings y probada.
- R-29 PASS: azul y ámbar en gráficos, neutros y controles nativos del tema.
- R-30 PASS: no se copió la identidad de otro producto; se usan los componentes requeridos de Streamlit.
- R-31 PASS: las decisiones principales tienen justificación en README.

## Límites pendientes

No se ha cotejado el listado exacto de KPI con la rúbrica completa, ni creado un repositorio GitHub, ni publicado en Streamlit Cloud, ni grabado el video. Las comprobaciones se refieren a esta primera versión local; no constituyen una auditoría exhaustiva de accesibilidad de las bibliotecas de terceros.
