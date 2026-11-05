"""Carga y cálculos compartidos por el informe y la aplicación."""

from datetime import date
from pathlib import Path
from typing import Optional

import pandas as pd

CSV_PATH = Path(__file__).parent / "proyecto_integrador_eafit_max30102.csv"
TIMEZONE = "America/Bogota"
COLUMNS = [
    "timestamp", "student_id", "nfc_id", "device_id", "heart_rate_bpm",
    "spo2_percent", "signal_quality", "measurement_status",
]
NUMERIC = ["heart_rate_bpm", "spo2_percent", "signal_quality"]


def load_raw(path=CSV_PATH):
    frame = pd.read_csv(path, encoding="utf-8-sig")
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError("Faltan columnas: " + ", ".join(sorted(missing)))
    if frame.empty:
        raise ValueError("El archivo no contiene mediciones.")
    return frame


def prepare(raw):
    frame = raw.copy()
    timestamp = frame["timestamp"].astype("string")
    explicit_zone = timestamp.str.contains(r"(?:Z|[+-]\d{2}:?\d{2})$", na=False)
    if not explicit_zone.all():
        raise ValueError("Hay fechas vacías o sin zona horaria explícita.")
    frame["timestamp_utc"] = pd.to_datetime(timestamp, utc=True, errors="raise")
    frame["timestamp_bogota"] = frame["timestamp_utc"].dt.tz_convert(TIMEZONE)
    frame["fecha"] = frame["timestamp_bogota"].dt.date
    frame["hora"] = frame["timestamp_bogota"].dt.hour
    for column in NUMERIC:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
        if frame[column].isin([float("inf"), -float("inf")]).any():
            raise ValueError(f"La columna {column} contiene valores infinitos.")
    # El estado proviene del CSV. No se deduce de los valores del sensor.
    frame["es_valida"] = frame["measurement_status"].eq("valid")
    return frame.sort_values("timestamp_utc", kind="stable").reset_index(drop=True)


def filter_rows(frame, start: date, end: date, student: Optional[str] = None,
                statuses=None):
    mask = frame["fecha"].between(start, end)
    if student is not None:
        mask &= frame["student_id"].eq(student)
    if statuses is not None:
        mask &= frame["measurement_status"].isin(statuses)
    return frame.loc[mask].copy()


def kpis(frame):
    valid = frame.loc[frame["es_valida"]]
    total = len(frame)
    return {
        "mediciones": total,
        "estudiantes": int(frame["student_id"].nunique()),
        "validas": len(valid),
        "porcentaje_valido": 100 * len(valid) / total if total else None,
        "bpm_promedio": float(valid["heart_rate_bpm"].mean()) if valid["heart_rate_bpm"].notna().any() else None,
        "spo2_promedio": float(valid["spo2_percent"].mean()) if valid["spo2_percent"].notna().any() else None,
    }


def daily_counts(frame, start, end):
    days = pd.date_range(start, end, freq="D").date
    return (frame.groupby("fecha").size().reindex(days, fill_value=0)
            .rename_axis("fecha").rename("mediciones").reset_index())
