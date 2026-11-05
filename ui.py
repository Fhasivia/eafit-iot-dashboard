"""Presentación del dashboard, sin modificar las mediciones ni sus cálculos."""

from html import escape
from pathlib import Path
import base64

import plotly.graph_objects as go
import streamlit as st

VIOLET = "#BA9AF7"
MINT = "#87E5B4"
TEXT = "#F0F3FA"
MUTED = "#B2BDD1"


def load_styles():
    css = Path(__file__).with_name("theme.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def topbar():
    logo = base64.b64encode(Path(__file__).with_name("assets").joinpath("eafit-blanco.svg").read_bytes()).decode("ascii")
    with st.container(key="topbar"):
        st.markdown(f'''
        <div class="brandbar">
          <div class="brand-identity">
            <div class="brand-symbol" aria-hidden="true">
              <svg viewBox="0 0 32 32" fill="none"><path d="M5 12V6h6M21 6h6v6M27 21v6h-6M11 27H5v-6" stroke="currentColor" stroke-width="2"/><path d="M9 17h4l3-7 3 12 3-5h3" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
            </div>
            <div class="brand-copy"><h1>Tótem IoT</h1><p>EAFIT · Proyecto integrador</p></div>
          </div>
          <div class="header-context">
            <div class="header-source"><span>Fuente de datos</span><strong>MAX30102 / CSV</strong></div>
            <div class="dataset-label"><i></i>Datos simulados</div>
          </div>
          <div class="eafit-brand"><img src="data:image/svg+xml;base64,{logo}" alt="Universidad EAFIT" width="134" height="50" /></div>
        </div>''', unsafe_allow_html=True)


def recent_feed(frame):
    rows = []
    for row in frame.tail(3).iloc[::-1].itertuples():
        valid = row.measurement_status == "valid"
        label = "Válida" if valid else "Inválida"
        symbol = "✓" if valid else "×"
        rows.append(f'''<div class="feed-row">
          <span class="feed-symbol {'valid' if valid else 'invalid'}" aria-hidden="true">{symbol}</span>
          <div><strong>{escape(str(row.student_id))}</strong><span>{row.timestamp_bogota:%d/%m · %H:%M} · {label}</span></div>
        </div>''')
    st.markdown('<div class="feed-title">Actividad reciente</div>' + ''.join(rows) +
                '<p class="feed-foot">Últimos registros de la selección</p>', unsafe_allow_html=True)


def observations(frame, daily):
    invalid = int(frame["measurement_status"].eq("invalid").sum())
    peak = daily.loc[daily["mediciones"].idxmax()]
    weekend = int(frame["timestamp_bogota"].dt.dayofweek.ge(5).sum())
    st.markdown(f'''<div class="feed-title">Lecturas del período</div>
    <div class="finding"><span>Calidad del registro</span><strong>{invalid:,} inválidas <small>/ {len(frame):,}</small></strong><p>{100 * invalid / len(frame):.2f}% de las mediciones seleccionadas</p></div>
    <div class="finding"><span>Mayor actividad diaria</span><strong>{int(peak['mediciones']):,} mediciones</strong><p>{peak['fecha']:%d/%m/%Y} · uno de los máximos</p></div>
    <div class="finding"><span>Fin de semana</span><strong>{weekend:,} registros</strong><p>{100 * weekend / len(frame):.2f}% corresponden a sábado o domingo</p></div>''', unsafe_allow_html=True)


def activity_figure(daily):
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=daily["fecha"], y=daily["mediciones"], mode="lines+markers",
        name="Mediciones", line=dict(color=MINT, width=2.5),
        marker=dict(size=4, color=MINT), fill="tozeroy",
        fillgradient=dict(type="horizontal", colorscale=[
            [0, "rgba(186,154,247,0.19)"], [1, "rgba(135,229,180,0.19)"]]),
        hovertemplate="%{x|%d/%m/%Y}<br><b>%{y} mediciones</b><extra></extra>",
    ))
    # El color recorre el tiempo; los segmentos unen conteos diarios sin suavizarlos.
    for index in range(len(daily) - 1):
        fraction = index / max(len(daily) - 2, 1)
        rgb = [round(a + (b - a) * fraction) for a, b in zip((186, 154, 247), (135, 229, 180))]
        figure.add_trace(go.Scatter(
            x=daily["fecha"].iloc[index:index + 2], y=daily["mediciones"].iloc[index:index + 2],
            mode="lines", line=dict(color=f"rgb({rgb[0]},{rgb[1]},{rgb[2]})", width=3),
            hoverinfo="skip", showlegend=False,
        ))
    figure.update_layout(showlegend=False, yaxis_title="Mediciones", xaxis_title=None)
    figure.update_xaxes(tickformat="%d/%m")
    figure.update_yaxes(rangemode="tozero")
    return figure


def style_figure(figure, height=300):
    figure.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color=MUTED),
        margin=dict(l=12, r=12, t=14, b=18), height=height,
        legend=dict(title_text="Estado del CSV", orientation="h", y=-0.24),
        hoverlabel=dict(bgcolor="#1C2941", bordercolor="#53617A", font_color=TEXT),
    )
    figure.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(178,189,209,0.12)")
    figure.update_yaxes(gridcolor="rgba(178,189,209,0.10)", zeroline=False)
    return figure
