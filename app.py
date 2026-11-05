from io import BytesIO
from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st

from datos import CSV_PATH, TIMEZONE, daily_counts, filter_rows, kpis, load_raw, prepare
from ui import MINT, VIOLET, activity_figure, load_styles, observations, recent_feed, style_figure, topbar

st.set_page_config(page_title="Tótem IoT · EAFIT", layout="wide")
load_styles()
STATUS_COLORS = {"valid": MINT, "invalid": VIOLET}
LABELS = {
    "heart_rate_bpm": "Frecuencia cardíaca (bpm)",
    "spo2_percent": "SpO₂ (%)",
    "signal_quality": "Calidad de señal (0 a 1)",
    "measurement_status": "Estado del CSV",
    "fecha": "Fecha en Bogotá", "hora": "Hora en Bogotá",
    "mediciones": "Mediciones", "hora_local": "Fecha y hora en Bogotá",
}


@st.cache_data(show_spinner=False)
def load_data(content):
    return prepare(load_raw(BytesIO(content)))


def chart(figure, height=300):
    st.plotly_chart(style_figure(figure, height), use_container_width=True, theme=None,
                    config={"displaylogo": False})


def formatted(value, suffix=""):
    return "Sin datos" if value is None else f"{value:.2f}{suffix}"


topbar()
try:
    with st.spinner("Leyendo las mediciones…"):
        data = load_data(CSV_PATH.read_bytes())
except (OSError, ValueError, pd.errors.ParserError) as error:
    st.error(f"No se pudo cargar el CSV: {error}")
    st.stop()

start, end = data["fecha"].min(), data["fecha"].max()
with st.container(key="filters"):
    date_filter, student_filter, status_filter = st.columns([1.4, 1, 1.1])
    with date_filter:
        dates = st.date_input("Período · hora de Bogotá", value=(start, end), min_value=start,
                          max_value=end, format="DD/MM/YYYY", key="dates")
    with student_filter:
        student = st.selectbox("Estudiante", ["Todos"] + sorted(data["student_id"].dropna().unique()), key="student")
    with status_filter:
        statuses = st.multiselect("Estado del CSV", sorted(data["measurement_status"].dropna().unique()),
                              default=sorted(data["measurement_status"].dropna().unique()), key="statuses")

if len(dates) != 2:
    st.info("Selecciona la fecha final para completar el período.")
    st.stop()
selected = filter_rows(data, dates[0], dates[1], None if student == "Todos" else student, statuses)
if selected.empty:
    st.info("No hay mediciones con estos filtros. Amplía el período o cambia estudiante y estado.")
    st.stop()

metrics = kpis(selected)
with st.container(key="selection_note"):
    st.caption(f"{dates[0]:%d/%m/%Y} a {dates[1]:%d/%m/%Y} · {len(selected):,} de {len(data):,} registros · {TIMEZONE}")

numbers, station, feed = st.columns([1.05, 1.7, 1.12])
with numbers:
    with st.container(key="kpi_stack"):
        with st.container(key="stat_total"):
            st.metric("Mediciones", f"{metrics['mediciones']:,}")
        with st.container(key="stat_students"):
            st.metric("Estudiantes", str(metrics["estudiantes"]))
        bpm_column, spo2_column = st.columns(2)
        with bpm_column:
            with st.container(key="stat_bpm"):
                st.metric("BPM promedio", formatted(metrics["bpm_promedio"]))
        with spo2_column:
            with st.container(key="stat_spo2"):
                st.metric("SpO₂ promedio", formatted(metrics["spo2_promedio"], "%"))
with station:
    with st.container(key="station"):
        device = selected["device_id"].iloc[0] if selected["device_id"].nunique() == 1 else "Varios dispositivos"
        st.markdown(f'<div class="station-heading"><span>{escape(str(device))}</span><span>Sensor MAX30102</span></div>', unsafe_allow_html=True)
        st.markdown('''<div class="sensor-icon" aria-hidden="true"><svg viewBox="0 0 44 34" fill="none"><rect x="7" y="3" width="30" height="28" rx="6" stroke="currentColor"/><path d="M16 3v8H7m30 0h-9V3M7 23h9v8m12 0v-8h9M19 13h6v8h-6z" stroke="currentColor"/><path d="M1 11h6M1 23h6M37 11h6M37 23h6" stroke="currentColor"/></svg></div>''', unsafe_allow_html=True)
        st.metric("Mediciones válidas", formatted(metrics["porcentaje_valido"], "%"))
        st.progress(metrics["validas"] / metrics["mediciones"])
        st.markdown(f'<p class="station-foot">{metrics["validas"]:,} de {metrics["mediciones"]:,} registros con estado valid</p>', unsafe_allow_html=True)
with feed:
    with st.container(key="feed"):
        recent_feed(selected)

st.markdown('<p class="method-note">BPM y SpO₂: promedios sólo de filas valid. Porcentaje válido: filas valid / todas las filas seleccionadas. Datos simulados, sin uso diagnóstico.</p>', unsafe_allow_html=True)

valid = selected.loc[selected["es_valida"]]
overview, individual, quality = st.tabs(["Actividad y mediciones", "Seguimiento individual", "Calidad y registros"])

with overview:
    daily = daily_counts(selected, dates[0], dates[1])
    plot_column, findings_column = st.columns([2.55, 1])
    with plot_column:
        with st.container(key="activity"):
            st.subheader("Actividad del tótem")
            st.caption("Mediciones por fecha · todos los estados seleccionados")
            chart(activity_figure(daily), height=260)
    with findings_column:
        with st.container(key="observations"):
            observations(selected, daily)

    with st.container(key="registry"):
        st.markdown('<div class="registry-heading"><h3>Registros recientes</h3><span>Selección actual</span></div>', unsafe_allow_html=True)
        preview = selected.iloc[::-1][["timestamp_bogota", "student_id", "heart_rate_bpm", "spo2_percent", "measurement_status"]]
        st.dataframe(preview.head(5), hide_index=True, width="stretch", height=212,
                     column_config={"timestamp_bogota": st.column_config.DatetimeColumn("Fecha · Bogotá", format="DD/MM/YYYY HH:mm"),
                                    "student_id": "Estudiante", "heart_rate_bpm": "BPM", "spo2_percent": "SpO₂ (%)", "measurement_status": "Estado"})
        st.download_button("Exportar selección (CSV)", selected[["timestamp", "timestamp_bogota", "student_id", "nfc_id", "device_id", "heart_rate_bpm", "spo2_percent", "signal_quality", "measurement_status"]].to_csv(index=False).encode("utf-8-sig"),
                           file_name="mediciones_filtradas.csv", mime="text/csv", key="export_overview")
        st.caption("Vista previa de las últimas cinco filas. La descarga incluye toda la selección.")

    st.subheader("Distribución de las mediciones")
    with st.container(key="distributions"):
        left, right = st.columns(2)
    with left:
        st.subheader("Actividad por hora")
        hourly = selected.groupby("hora").size().reindex(range(24), fill_value=0).rename("mediciones").reset_index()
        fig = px.bar(hourly, x="hora", y="mediciones", labels=LABELS, color_discrete_sequence=[MINT])
        fig.update_xaxes(dtick=3, range=[-0.5, 23.5])
        chart(fig)
    with right:
        st.subheader("Frecuencia cardíaca")
        if valid.empty:
            st.info("No hay mediciones válidas para mostrar esta distribución.")
        else:
            chart(px.histogram(valid, x="heart_rate_bpm", nbins=30, labels=LABELS,
                               color_discrete_sequence=[MINT]).update_layout(yaxis_title="Mediciones válidas"))

    with st.container(key="distributions_more"):
        left, right = st.columns(2)
    with left:
        st.subheader("Distribución de SpO₂")
        if valid.empty:
            st.info("No hay mediciones válidas para mostrar esta distribución.")
        else:
            chart(px.histogram(valid, x="spo2_percent", nbins=30, labels=LABELS,
                               color_discrete_sequence=[MINT]).update_layout(yaxis_title="Mediciones válidas"))
    with right:
        st.subheader("BPM y SpO₂")
        if valid.empty:
            st.info("No hay mediciones válidas para comparar ambas variables.")
        else:
            chart(px.scatter(valid, x="heart_rate_bpm", y="spo2_percent", labels=LABELS,
                             hover_data=["student_id", "timestamp"], opacity=0.45,
                             color_discrete_sequence=[MINT]))
    st.caption("Las tres gráficas del sensor incluyen sólo filas valid. Una distribución o asociación visual no constituye un diagnóstico ni prueba causalidad.")

    st.caption("Estas observaciones se recalculan con los filtros. Consulta el informe del proyecto para el análisis del archivo completo.")

with individual:
    st.subheader("Histórico de un estudiante")
    person = st.selectbox("Estudiante para seguimiento", sorted(selected["student_id"].dropna().unique()), key="person")
    history = selected.loc[selected["student_id"].eq(person)].copy()
    # Plotly recibe hora local sin zona para que el navegador no vuelva a convertirla.
    history["hora_local"] = history["timestamp_bogota"].dt.tz_localize(None)
    history_valid = history.loc[history["es_valida"]]
    st.write(f"{len(history):,} registros en el período filtrado; {len(history_valid):,} marcados valid.")
    st.caption("Línea verde: mediciones válidas ordenadas por fecha. Cruces violetas: inválidas, conservadas para revisar calidad.")
    for variable in ["heart_rate_bpm", "spo2_percent"]:
        st.markdown(f"#### {LABELS[variable]}")
        # Las inválidas interrumpen la línea para no sugerir continuidad a través de ellas.
        plot_history = history.copy()
        plot_history.loc[~plot_history["es_valida"], variable] = float("nan")
        fig = px.line(plot_history, x="hora_local", y=variable, markers=True,
                      labels=LABELS, color_discrete_sequence=[MINT])
        fig.update_traces(name="valid", showlegend=True, connectgaps=False)
        invalid_history = history.loc[~history["es_valida"]]
        if not invalid_history.empty:
            scatter = px.scatter(invalid_history, x="hora_local", y=variable, labels=LABELS,
                                 color_discrete_sequence=[VIOLET])
            scatter.update_traces(name="invalid", showlegend=True, marker_symbol="x", marker_size=10)
            fig.add_traces(scatter.data)
        chart(fig)
    st.dataframe(history[["timestamp_bogota", "heart_rate_bpm", "spo2_percent", "signal_quality", "measurement_status"]],
                 hide_index=True, width="stretch")

with quality:
    left, right = st.columns(2)
    with left:
        with st.container(key="quality_status"):
            st.subheader("Estado de las mediciones")
            counts = selected.groupby("measurement_status").size().rename("mediciones").reset_index()
            chart(px.bar(counts, x="measurement_status", y="mediciones", color="measurement_status",
                         color_discrete_map=STATUS_COLORS, labels=LABELS))
    with right:
        with st.container(key="quality_signal"):
            st.subheader("Calidad de señal por estado")
            chart(px.box(selected, x="measurement_status", y="signal_quality", color="measurement_status",
                         color_discrete_map=STATUS_COLORS, labels=LABELS, points="outliers"))
    st.caption("El estado se toma del CSV. La calidad de señal no se usa para reclasificar mediciones.")
    st.subheader("Registros seleccionados")
    export_columns = ["timestamp", "timestamp_bogota", "student_id", "nfc_id", "device_id",
                      "heart_rate_bpm", "spo2_percent", "signal_quality", "measurement_status"]
    export = selected[export_columns]
    st.dataframe(export, hide_index=True, width="stretch")
    st.download_button("Descargar registros filtrados (CSV)", export.to_csv(index=False).encode("utf-8-sig"),
                       file_name="mediciones_filtradas.csv", mime="text/csv", key="download")
    with st.expander("Cómo se prepararon los datos"):
        st.write("Se conserva el CSV original. Las fechas se interpretan con su zona UTC y se convierten a America/Bogota. No se imputan valores ni se eliminan filas marcadas invalid. Los indicadores se recalculan después de aplicar los tres filtros.")
        st.write("Las mediciones simuladas no permiten inferir diagnósticos. Los valores atípicos estadísticos se documentan en el informe y se mantienen en las gráficas.")
