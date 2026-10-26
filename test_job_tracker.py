"""Simple tests for the Job Application Tracker (standard library only).

Run with:  python -m unittest discover
"""

import tempfile
import unittest
from pathlib import Path

from job_tracker import Application, Tracker


class TrackerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_file = Path(self.tmp.name) / "data.json"
        self.tracker = Tracker(self.data_file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_reload(self):
        self.tracker.add(
            Application("Example Inc.", "Backend Engineer", "Indeed", "2026-10-01")
        )
        reloaded = Tracker(self.data_file)
        self.assertEqual(len(reloaded.applications), 1)
        self.assertEqual(reloaded.applications[0].company, "Example Inc.")

    def test_update_status(self):
        self.tracker.add(
            Application("Example Inc.", "Help Desk", "doda", "2026-10-02")
        )
        updated = self.tracker.update_status(0, "interview")
        self.assertEqual(updated.status, "interview")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.tracker.add(
                Application("Example Inc.", "SE", "Indeed", "2026-10-03", "unknown")
            )

    def test_stats(self):
        self.tracker.add(Application("A Corp", "SE", "Indeed", "2026-10-01"))
        self.tracker.add(
            Application("B Corp", "SE", "doda", "2026-10-02", "rejected")
        )
        counts = self.tracker.stats()
        self.assertEqual(counts["total"], 2)
        self.assertEqual(counts["applied"], 1)
        self.assertEqual(counts["rejected"], 1)


if __name__ == "__main__":
    unittest.main()

