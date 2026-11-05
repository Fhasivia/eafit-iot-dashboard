# Dirección visual

Referencia: captura facilitada por el usuario el 5 de noviembre de 2026. El usuario pide adaptar el dashboard existente a su aspecto oscuro, translúcido y luminoso.

Panel de análisis IoT para el equipo y docente de EAFIT. Intensidad visual 2, ritmo 2, movimiento 1. Se mantiene Streamlit y el análisis del CSV real.

- Fondo azul noche y paneles de superficies translúcidas: reproducen la profundidad de la referencia.
- Violeta y verde menta: acentos de la referencia. Verde identifica filas válidas, violeta identifica inválidas con una cruz y una etiqueta que también las distingue.
- Tarjeta central de borde luminoso: jerarquiza el porcentaje válido, que determina cómo interpretar los promedios del sensor.
- Tarjetas pequeñas a la izquierda: agrupan volumen de uso y medias sin competir con la tarjeta central.
- Actividad reciente a la derecha: sustituye el registro de transacciones de la referencia por las tres últimas mediciones filtradas; no representa una conexión en tiempo real.
- Gráfico principal de líneas: muestra conteos diarios reales, sin suavizado ni datos adicionales. El degradado recorre el tiempo y no codifica el estado de validez.
- Registros recientes debajo del gráfico: permite comprobar filas y descargar la selección completa.
- Tipografía del sistema: aproxima la referencia con buena legibilidad y sin descargar fuentes.
- Desenfoque limitado a la barra superior y brillo limitado a la tarjeta central: mantiene profundidad sin dificultar la lectura de tablas o gráficos.
- Diseño oscuro como tema predeterminado por petición visual expresa del usuario. No se añade un interruptor de tema decorativo.
- Sin animación añadida: los cambios de filtros y pestañas conservan el comportamiento nativo.
- La barra de herramientas de desarrollo de Streamlit se oculta para que no se superponga al contenido durante el desplazamiento móvil.
- La marca de escaneo y el icono del sensor son símbolos de interfaz, no un logotipo institucional ni una señal medida.

La captura bancaria sólo define estilo y composición. No se incorporan saldos, tarjetas bancarias, publicidad ni actividad ficticia.

## Ajuste de cabecera solicitado

La cabecera agrupa icono y título como una unidad centrada verticalmente. El contexto del archivo ocupa el bloque intermedio y el logo oficial blanco de EAFIT se sitúa en el extremo derecho, con separación y proporciones originales. En móvil se conservan título y logo, mientras los filtros y la nota de selección mantienen el contexto de los datos. El contenedor principal declara márgenes automáticos simétricos para centrar el conjunto en pantallas anchas.
