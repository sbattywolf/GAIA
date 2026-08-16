import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from home_config import load_max_entity_list


class HomeConfigTests(unittest.TestCase):
    def test_missing_threshold_uses_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                load_max_entity_list(),
                10,
            )

    def test_empty_threshold_uses_default(self):
        with patch.dict(
            os.environ,
            {"ZEUS_MAX_ENTITY_LIST": ""},
            clear=True,
        ):
            self.assertEqual(
                load_max_entity_list(),
                10,
            )

    def test_non_numeric_threshold_uses_default(self):
        with patch.dict(
            os.environ,
            {"ZEUS_MAX_ENTITY_LIST": "abc"},
            clear=True,
        ):
            self.assertEqual(
                load_max_entity_list(),
                10,
            )

    def test_zero_threshold_uses_default(self):
        with patch.dict(
            os.environ,
            {"ZEUS_MAX_ENTITY_LIST": "0"},
            clear=True,
        ):
            self.assertEqual(
                load_max_entity_list(),
                10,
            )

    def test_negative_threshold_uses_default(self):
        with patch.dict(
            os.environ,
            {"ZEUS_MAX_ENTITY_LIST": "-4"},
            clear=True,
        ):
            self.assertEqual(
                load_max_entity_list(),
                10,
            )

    def test_positive_threshold_is_used(self):
        with patch.dict(
            os.environ,
            {"ZEUS_MAX_ENTITY_LIST": "15"},
            clear=True,
        ):
            self.assertEqual(
                load_max_entity_list(),
                15,
            )


if __name__ == "__main__":
    unittest.main()

