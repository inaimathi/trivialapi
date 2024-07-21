import unittest

from src.pytoda import core


class TestBasics(unittest.TestCase):
    def test_basics(self):
        core.Twin
        self.assertTrue(True)
        self.assertIsNone(None)
        self.assertEqual("a", "a")
