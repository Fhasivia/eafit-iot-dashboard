from datetime import date
import unittest

from datos import daily_counts, filter_rows, kpis, load_raw, prepare


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw()
        cls.data = prepare(cls.raw)

    def test_dataset_totals(self):
        self.assertEqual(self.raw.shape, (2667, 8))
        self.assertEqual(int(self.raw.isna().sum().sum()), 0)
        self.assertEqual(int(self.raw.duplicated().sum()), 0)
        metrics = kpis(self.data)
        self.assertEqual(metrics["estudiantes"], 295)
        self.assertEqual(metrics["validas"], 2590)
        self.assertAlmostEqual(metrics["porcentaje_valido"], 97.11286089238845)
        self.assertAlmostEqual(metrics["bpm_promedio"], 75.47142857142858)
        self.assertAlmostEqual(metrics["spo2_promedio"], 97.71679536679537)

    def test_timezone_and_inclusive_dates(self):
        self.assertEqual(str(self.data.iloc[0]["timestamp_bogota"]), "2026-09-29 19:50:00-05:00")
        first_day = filter_rows(self.data, date(2026, 9, 29), date(2026, 9, 29))
        last_day = filter_rows(self.data, date(2026, 10, 28), date(2026, 10, 28))
        self.assertEqual(len(first_day), 10)
        self.assertEqual(len(last_day), 102)
        self.assertTrue(first_day["timestamp_utc"].dt.date.eq(date(2026, 9, 30)).all())

    def test_invalid_numeric_values_are_excluded_from_means(self):
        invalid = filter_rows(self.data, date(2026, 9, 29), date(2026, 10, 28), statuses=["invalid"])
        self.assertEqual(len(invalid), 77)
        self.assertEqual(int(invalid[["heart_rate_bpm", "spo2_percent"]].isna().sum().sum()), 0)
        metrics = kpis(invalid)
        self.assertEqual(metrics["porcentaje_valido"], 0)
        self.assertIsNone(metrics["bpm_promedio"])
        self.assertIsNone(metrics["spo2_promedio"])

    def test_student_and_empty_filters(self):
        subset = filter_rows(self.data, date(2026, 9, 29), date(2026, 10, 28), "EST-0241")
        self.assertEqual(len(subset), 21)
        self.assertEqual(kpis(subset)["estudiantes"], 1)
        empty = filter_rows(self.data, date(2026, 9, 29), date(2026, 10, 28), statuses=[])
        self.assertTrue(empty.empty)
        self.assertIsNone(kpis(empty)["porcentaje_valido"])

    def test_calendar_and_timestamp_collisions(self):
        daily = daily_counts(self.data, date(2026, 9, 29), date(2026, 10, 28))
        self.assertEqual(len(daily), 30)
        self.assertEqual(int(daily["mediciones"].sum()), 2667)
        self.assertEqual(int(self.data["timestamp_utc"].duplicated().sum()), 11)
        self.assertEqual(int(self.data.duplicated(["student_id", "timestamp_utc"]).sum()), 0)

    def test_ambiguous_dates_and_bad_schema_rejected(self):
        raw = self.raw.iloc[:1].copy()
        raw.loc[raw.index[0], "timestamp"] = "2026-09-30 00:50:00"
        with self.assertRaisesRegex(ValueError, "zona horaria"):
            prepare(raw)


if __name__ == "__main__":
    unittest.main()
