import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from home_aggregate import (
    CountResults,
    HomeReport,
    TruncatedResults,
)
from response_formatter import ResponseFormatter


class ResponseFormatterM2Tests(unittest.TestCase):
    def test_singular_and_plural_for_counts(self):
        count_results = CountResults(
            counts={
                "window": 1,
                "door": 2,
                "light": 3,
                "switch": 1,
            }
        )

        response = ResponseFormatter.format_count_results(
            count_results,
        )

        self.assertEqual(
            response,
            "Risultano 1 finestra, 2 porte, 3 entit\u00e0 light e 1 switch.",
        )

    def test_automation_breakdown_for_counts(self):
        count_results = CountResults(
            counts={"automation": 35},
            automation_on=28,
            automation_off=6,
            automation_unknown=0,
            automation_unavailable=1,
        )

        response = ResponseFormatter.format_count_results(
            count_results,
        )

        self.assertEqual(
            response,
            (
                "Risultano 35 automazioni. "
                "Automazioni: 28 abilitate, 6 disabilitate, 0 unknown e 1 unavailable."
            ),
        )

    def test_truncated_state_results_show_remaining(self):
        truncated = TruncatedResults(
            items=[
                {"name": "Luce 1"},
                {"name": "Luce 2"},
            ],
            total_count=5,
            remaining_count=3,
        )

        response = ResponseFormatter.format_truncated_state_results(
            truncated,
            "light",
            "on",
        )

        self.assertEqual(
            response,
            "Risultano accese: Luce 1 e Luce 2 e altre 3 entit\u00e0.",
        )

    def test_home_report_shows_nessuna_for_empty_sections(self):
        report = HomeReport(
            windows_open=TruncatedResults(
                items=[],
                total_count=0,
                remaining_count=0,
            ),
            doors_open=TruncatedResults(
                items=[],
                total_count=0,
                remaining_count=0,
            ),
            lights_on=TruncatedResults(
                items=[],
                total_count=0,
                remaining_count=0,
            ),
            automation_on=28,
            automation_off=6,
            automation_unknown=0,
            automation_unavailable=1,
            unavailable_total=1,
        )

        response = ResponseFormatter.format_home_report(
            report,
        )

        self.assertEqual(
            response,
            (
                "Finestre aperte: nessuna. "
                "Porte aperte: nessuna. "
                "Entit\u00e0 light accese: nessuna. "
                "Automazioni: 28 abilitate, 6 disabilitate, 0 unknown e 1 unavailable. "
                "Entit\u00e0 unavailable: 1."
            ),
        )

    def test_home_report_shows_remaining_count(self):
        report = HomeReport(
            windows_open=TruncatedResults(
                items=[{"name": "Finestra 1"}],
                total_count=1,
                remaining_count=0,
            ),
            doors_open=TruncatedResults(
                items=[{"name": "Porta 1"}],
                total_count=1,
                remaining_count=0,
            ),
            lights_on=TruncatedResults(
                items=[{"name": "Luce 1"}, {"name": "Luce 2"}],
                total_count=5,
                remaining_count=3,
            ),
            automation_on=2,
            automation_off=1,
            automation_unknown=1,
            automation_unavailable=0,
            unavailable_total=2,
        )

        response = ResponseFormatter.format_home_report(
            report,
        )

        self.assertIn(
            "Entit\u00e0 light accese: Luce 1 e Luce 2 e altre 3 entit\u00e0.",
            response,
        )


if __name__ == "__main__":
    unittest.main()


