import unittest

from app.data_pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):
    def setUp(self):  # type: ignore[override]
        self.pipeline = DataPipeline()

    def test_pipeline_persists_records(self):
        rows = [
            {"customer": "A", "amount": 50},
            {"customer": "B", "amount": -5},
        ]
        result = self.pipeline.run(rows)
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].payload["is_active"])
        self.assertFalse(result[1].payload["is_active"])
        self.assertEqual(len(self.pipeline.storage), 2)


if __name__ == "__main__":
    unittest.main()
