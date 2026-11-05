from datetime import date
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(APP), default_timeout=30).run()

    def assert_healthy(self):
        self.assertEqual(len(self.app.exception), 0)

    def metrics(self):
        return {metric.label: metric.value for metric in self.app.metric}

    def test_initial_values_and_charts(self):
        self.assert_healthy()
        self.assertEqual(self.metrics(), {"Mediciones": "2,667", "Estudiantes": "295",
                                         "Mediciones válidas": "97.11%", "BPM promedio": "75.47", "SpO₂ promedio": "97.72%"})
        self.assertEqual(len(self.app.get("plotly_chart")), 9)

    def test_invalid_and_empty_states(self):
        self.app.multiselect(key="statuses").set_value(["invalid"]).run()
        self.assert_healthy()
        self.assertEqual(self.metrics()["Mediciones"], "77")
        self.assertEqual(self.metrics()["Mediciones válidas"], "0.00%")
        self.assertEqual(self.metrics()["BPM promedio"], "Sin datos")
        self.assertEqual(self.metrics()["SpO₂ promedio"], "Sin datos")
        self.app.multiselect(key="statuses").set_value([]).run()
        self.assert_healthy()
        self.assertEqual(len(self.app.metric), 0)
        self.assertIn("No hay mediciones", self.app.info[0].value)

    def test_student_date_and_individual_followup(self):
        self.app.selectbox(key="student").set_value("EST-0241").run()
        self.assert_healthy()
        self.assertEqual(self.metrics()["Mediciones"], "21")
        self.assertEqual(self.metrics()["Estudiantes"], "1")
        self.assertEqual(self.app.selectbox(key="person").value, "EST-0241")
        self.app.selectbox(key="student").set_value("Todos").run()
        self.app.date_input(key="dates").set_value((date(2026, 9, 29), date(2026, 9, 29))).run()
        self.assert_healthy()
        self.assertEqual(self.metrics()["Mediciones"], "10")
        person = self.app.selectbox(key="person").options[-1]
        self.app.selectbox(key="person").set_value(person).run()
        self.assert_healthy()
        self.assertEqual(self.app.selectbox(key="person").value, person)

    def test_incomplete_date_range(self):
        self.app.date_input(key="dates").set_value((date(2026, 9, 29),)).run()
        self.assert_healthy()
        self.assertIn("Selecciona la fecha final", self.app.info[0].value)


if __name__ == "__main__":
    unittest.main()
