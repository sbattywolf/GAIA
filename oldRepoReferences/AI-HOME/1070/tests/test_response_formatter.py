import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from response_formatter import ResponseFormatter


class ResponseFormatterTests(unittest.TestCase):
    def test_window_open_single_name(self):
        results = [{"name": "Finestra cucina"}]

        response = ResponseFormatter.format_home_state_results(
            results,
            "window",
            "on",
        )

        self.assertEqual(
            response,
            "Risultano aperte: Finestra cucina.",
        )

    def test_door_closed_single_name(self):
        results = [{"name": "Porta ingresso"}]

        response = ResponseFormatter.format_home_state_results(
            results,
            "door",
            "off",
        )

        self.assertEqual(
            response,
            "Risultano chiuse: Porta ingresso.",
        )

    def test_window_closed_single_name(self):
        results = [{"name": "Finestra soggiorno"}]

        response = ResponseFormatter.format_home_state_results(
            results,
            "window",
            "off",
        )

        self.assertEqual(
            response,
            "Risultano chiuse: Finestra soggiorno.",
        )

    def test_door_open_single_name(self):
        results = [{"name": "Porta ripostiglio"}]

        response = ResponseFormatter.format_home_state_results(
            results,
            "door",
            "on",
        )

        self.assertEqual(
            response,
            "Risultano aperte: Porta ripostiglio.",
        )

    def test_light_on_single_name(self):
        results = [{"name": "Luce ufficio"}]

        response = ResponseFormatter.format_home_state_results(
            results,
            "light",
            "on",
        )

        self.assertEqual(
            response,
            "Risultano accese: Luce ufficio.",
        )

    def test_light_off_multiple_names(self):
        results = [
            {"name": "Luce corridoio"},
            {"name": "Luce ingresso"},
            {"name": "Luce cucina"},
        ]

        response = ResponseFormatter.format_home_state_results(
            results,
            "light",
            "off",
        )

        self.assertEqual(
            response,
            "Risultano spente: Luce corridoio, Luce ingresso e Luce cucina.",
        )

    def test_empty_results(self):
        response = ResponseFormatter.format_home_state_results(
            [],
            "window",
            "on",
        )

        self.assertEqual(
            response,
            "Non risultano entit\u00e0 corrispondenti alla richiesta.",
        )


if __name__ == "__main__":
    unittest.main()




