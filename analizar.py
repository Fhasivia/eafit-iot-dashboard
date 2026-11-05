"""Regenera el informe y los agregados a partir del CSV original."""

import hashlib
import json
from pathlib import Path

import pandas as pd

from datos import COLUMNS, CSV_PATH, NUMERIC, daily_counts, kpis, load_raw, prepare


def analyze():
    raw = load_raw()
    data = prepare(raw)
    valid = data.loc[data["es_valida"]]
    metrics = kpis(data)
    output = Path(__file__).parent / "analisis"
    output.mkdir(exist_ok=True)
    daily = daily_counts(data, data["fecha"].min(), data["fecha"].max())
    daily.to_csv(output / "actividad_diaria.csv", index=False)
    hours = data.groupby("hora").size().reindex(range(24), fill_value=0)
    hours.rename("mediciones").to_csv(output / "actividad_por_hora.csv")
    by_status = data.groupby("measurement_status")[NUMERIC].agg(["count", "mean", "min", "max"])
    by_status.to_csv(output / "resumen_por_estado.csv")

    outliers = {}
    for col in NUMERIC:
        q1, q3 = valid[col].quantile([0.25, 0.75])
        lower, upper = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
        outliers[col] = {"limite_inferior": float(lower), "limite_superior": float(upper),
                         "n": int((valid[col].lt(lower) | valid[col].gt(upper)).sum())}

    # Se omiten las fechas extremas para no comparar jornadas de borde con interiores.
    interior = daily.iloc[1:-1].copy()
    interior["fin_semana"] = pd.to_datetime(interior["fecha"]).dt.dayofweek.ge(5)
    calendar = interior.groupby("fin_semana")["mediciones"].agg(["count", "sum", "mean"])
    shared = data["timestamp_utc"].value_counts()
    report = {
        "archivo": CSV_PATH.name,
        "sha256": hashlib.sha256(CSV_PATH.read_bytes()).hexdigest(),
        "filas": len(raw), "columnas": len(raw.columns),
        "tipos_originales": {c: str(raw[c].dtype) for c in raw.columns},
        "nulos": {c: int(raw[c].isna().sum()) for c in raw.columns},
        "duplicados_exactos": int(raw.duplicated().sum()),
        "estados": {str(k): int(v) for k, v in raw["measurement_status"].value_counts(dropna=False).items()},
        "kpi": metrics,
        "rango_utc": [str(data["timestamp_utc"].min()), str(data["timestamp_utc"].max())],
        "rango_bogota": [str(data["timestamp_bogota"].min()), str(data["timestamp_bogota"].max())],
        "cambios_fecha_por_zona": int((data["timestamp_utc"].dt.date != data["fecha"]).sum()),
        "fechas_observadas": int(data["fecha"].nunique()),
        "dispositivos": int(data["device_id"].nunique()),
        "nfc_distintos": int(data["nfc_id"].nunique()),
        "nfc_con_varios_estudiantes": int(data.groupby("nfc_id")["student_id"].nunique().gt(1).sum()),
        "estudiantes_con_varios_nfc": int(data.groupby("student_id")["nfc_id"].nunique().gt(1).sum()),
        "instantes_compartidos": int(shared.gt(1).sum()),
        "filas_en_instantes_compartidos": int(shared.loc[shared.gt(1)].sum()),
        "duplicados_estudiante_instante": int(data.duplicated(["student_id", "timestamp_utc"]).sum()),
        "estados_desconocidos": int((~data["measurement_status"].isin(["valid", "invalid"])).sum()),
        "bpm_no_positivo": int(data["heart_rate_bpm"].le(0).sum()),
        "spo2_fuera_0_100": int((data["spo2_percent"].lt(0) | data["spo2_percent"].gt(100)).sum()),
        "senal_fuera_0_1": int((data["signal_quality"].lt(0) | data["signal_quality"].gt(1)).sum()),
        "atipicos_iqr_solo_validas": outliers,
        "calendario_interior": {
            "entre_semana": {k: float(v) for k, v in calendar.loc[False].items()},
            "fin_semana": {k: float(v) for k, v in calendar.loc[True].items()},
        },
    }
    (output / "resumen.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    column_rows = "\n".join(f"| `{c}` | {raw[c].dtype} | {raw[c].isna().sum()} |" for c in COLUMNS)
    invalid = report["estados"].get("invalid", 0)
    weekday, weekend = calendar.loc[False], calendar.loc[True]
    signal_means = data.groupby("measurement_status")["signal_quality"].mean()
    outlier_rows = "\n".join(f"| {c} | {v['limite_inferior']:.3f} | {v['limite_superior']:.3f} | {v['n']} |" for c, v in outliers.items())
    text = f"""# Exploración real del CSV del tótem IoT

Fuente: `{CSV_PATH.name}`, descargado del enlace de Notion facilitado por el usuario el 5 de noviembre de 2026. Datos simulados según las instrucciones del proyecto compartidas. No representan diagnósticos médicos.

SHA-256: `{report['sha256']}`. El CSV se conserva byte por byte. Para regenerar este informe: `python analizar.py`.

## Estructura y calidad

**{len(raw):,} filas y {len(raw.columns)} columnas**, {metrics['estudiantes']} estudiantes, {report['nfc_distintos']} NFC y {report['dispositivos']} dispositivo.

| Columna original | Tipo leído por Pandas | Nulos |
| --- | --- | ---: |
{column_rows}

No hay filas idénticas duplicadas, fechas sin zona, fallos de conversión numérica ni estados desconocidos. Tampoco hay BPM no positivos, SpO₂ fuera de 0 a 100 o calidad de señal fuera de 0 a 1. Estos controles describen consistencia técnica, no validación clínica.

Hay {report['instantes_compartidos']} instantes compartidos por {report['filas_en_instantes_compartidos']} filas. Cada uno corresponde a estudiantes distintos. No se eliminan por compartir fecha y hora, y no hay duplicados de estudiante e instante. El archivo sólo tiene resolución temporal de un minuto; no permite determinar la secuencia dentro de ese minuto.

Cada estudiante tiene un único NFC y cada NFC corresponde a un único estudiante en este archivo.

## Cinco KPI propuestos

| Indicador | Resultado sin filtros | Regla |
| --- | ---: | --- |
| Mediciones | {metrics['mediciones']:,} | Todas las filas del filtro |
| Estudiantes | {metrics['estudiantes']} | Identificadores distintos del filtro |
| Mediciones válidas | {metrics['porcentaje_valido']:.2f}% | Filas `valid` / todas las filas del filtro |
| BPM promedio | {metrics['bpm_promedio']:.2f} bpm | Media de `heart_rate_bpm`, sólo `valid` |
| SpO₂ promedio | {metrics['spo2_promedio']:.2f}% | Media de `spo2_percent`, sólo `valid` |

La selección del estado también afecta el denominador. Al seleccionar sólo `invalid`, el porcentaje válido es 0% y los dos promedios no están disponibles. Si faltan datos numéricos en una futura versión del archivo, las medias omiten esos nulos sin imputarlos. No se equipara un valor ausente a cero.

Los cinco KPI son una propuesta inicial. La conversación recuperada menciona cinco obligatorios, pero no incluye su listado exacto; deben cotejarse con la rúbrica completa antes de la entrega.

## Fechas y horas

- UTC: {report['rango_utc'][0]} hasta {report['rango_utc'][1]}.
- America/Bogota: {report['rango_bogota'][0]} hasta {report['rango_bogota'][1]}.
- Hay {report['fechas_observadas']} fechas locales con registros y {report['cambios_fecha_por_zona']} filas cambian de fecha al convertir la zona.

Se interpreta el desplazamiento explícito del CSV con `pd.to_datetime(..., utc=True)` y se convierte con `.dt.tz_convert('America/Bogota')`. La columna original se conserva. Los filtros incluyen ambas fechas extremas y los agrupamientos diarios y horarios usan Bogotá. El primer y último día del archivo son fechas de borde; no se asume cobertura completa.

## Hallazgos verificables

1. **Los valores no vacíos no garantizan validez.** Hay {metrics['validas']:,} filas `valid` y {invalid} `invalid` ({invalid / len(data) * 100:.2f}% del total). Las {invalid} inválidas contienen BPM, SpO₂ y calidad de señal numéricos. Se conservan para analizar calidad, pero no entran en promedios del sensor. Ver `resumen_por_estado.csv`.
2. **La actividad registrada es menor los fines de semana.** Al excluir las dos fechas extremas, hay {int(weekday['count'])} fechas de lunes a viernes con {weekday['mean']:.2f} registros/día y {int(weekend['count'])} fechas de fin de semana con {weekend['mean']:.2f}. Describe el patrón del archivo, sin atribuirlo a horarios o causas no documentadas. Ver `actividad_diaria.csv`.
3. **La calidad de señal no explica por sí sola el estado.** La media es {signal_means['valid']:.4f} en válidas y {signal_means['invalid']:.4f} en inválidas. Los intervalos se solapan: válidas de {valid['signal_quality'].min():.3f} a {valid['signal_quality'].max():.3f}, inválidas de {data.loc[~data['es_valida'], 'signal_quality'].min():.3f} a {data.loc[~data['es_valida'], 'signal_quality'].max():.3f}. No hay base para deducir un umbral único ni causalidad. Ver `resumen_por_estado.csv`.
4. **La zona horaria cambia la interpretación del calendario.** El primer registro es 30 de septiembre en UTC y 29 de septiembre en Bogotá. Agrupar directamente el texto UTC desplazaría parte de la actividad a otro día.

## Valores atípicos estadísticos

Se usa el criterio de Tukey por variable sobre filas `valid`: menor que Q1 − 1,5 × IQR o mayor que Q3 + 1,5 × IQR. Se mantienen los registros. Los límites no son rangos clínicos y no reclasifican el estado original.

| Variable | Límite inferior | Límite superior | Filas fuera |
| --- | ---: | ---: | ---: |
{outlier_rows}

## Alcance

Este análisis describe mediciones simuladas. No se infieren diagnósticos, salud individual, causas de invalidez ni relaciones causales. Las medias por medición dan más peso a estudiantes con más registros; no son medias con igual peso por estudiante. Los valores observados y la etiqueta `valid` no prueban exactitud del sensor.
"""
    (output / "informe.md").write_text(text, encoding="utf-8")
    print(json.dumps({"filas": len(raw), "columnas": len(raw.columns), **metrics}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    analyze()
