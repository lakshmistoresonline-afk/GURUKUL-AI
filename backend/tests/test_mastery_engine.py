import sys
import os
import json
import unittest

from src.services.mastery_service import MasteryService

class TestMasteryEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use real data path
        cls.service = MasteryService()

    def test_chapter_config_lookup(self):
        # Class 5 English Chapter 1 (eesa101)
        config = self.service.get_chapter_mastery_config("class_5", "english", "eesa101")
        self.assertIsNotNone(config)
        self.assertEqual(config["source"]["chapterTitle"], "Papa’s Spectacles")

        # Class 6 English Chapter 1 (c6_english_001)
        config = self.service.get_chapter_mastery_config("class_6", "english", "c6_english_001")
        self.assertIsNotNone(config)
        self.assertEqual(config["source"]["chapterTitle"], "A Bottle of Dew")

    def test_state_transitions(self):
        config = self.service.get_chapter_mastery_config("class_5", "english", "eesa101")
        concepts = config["concepts"]

        # Scenario 1: NOT_STARTED
        record = {"uid": "test_user", "className": "class_5", "chapterId": "eesa101", "conceptPerformance": {}}
        state = self.service.calculate_mastery_state(record, config)
        self.assertEqual(state["status"], "NOT_STARTED")
        self.assertEqual(state["progress"], 0)

        # Scenario 2: LEARNING
        c1_id = concepts[0].get("conceptId") or concepts[0].get("id")
        record["conceptPerformance"] = {c1_id: {"foundation": 0.8, "application": 0.0}}
        state = self.service.calculate_mastery_state(record, config)
        self.assertEqual(state["status"], "LEARNING")
        self.assertGreater(state["progress"], 0)

        # Scenario 3: ASSESSMENT_READY (all concepts foundation >= 0.7)
        perf = {}
        for c in concepts:
            cid = c.get("conceptId") or c.get("id")
            if cid: perf[cid] = {"foundation": 0.9, "application": 0.0}
        record["conceptPerformance"] = perf
        state = self.service.calculate_mastery_state(record, config)
        self.assertEqual(state["status"], "ASSESSMENT_READY")
        self.assertEqual(state["progress"], 1.0)

        # Scenario 4: ASSESSING (Average application >= 0.6)
        for c_id in perf:
            perf[c_id]["application"] = 0.7
        record["last_quiz_score"] = 0.9
        state = self.service.calculate_mastery_state(record, config)
        self.assertEqual(state["status"], "ASSESSING")
        self.assertTrue(state["evidence"]["apply"])

    def test_remediation_trigger(self):
        config = self.service.get_chapter_mastery_config("class_5", "english", "eesa101")
        concepts = config["concepts"]

        perf = {}
        for c in concepts:
            cid = c.get("conceptId") or c.get("id")
            if cid: perf[cid] = {"foundation": 0.9, "application": 0.7}

        # One weak concept
        weak_cid = concepts[0].get("conceptId") or concepts[0].get("id")
        perf[weak_cid] = {"foundation": 0.5, "application": 0.3}

        record = {
            "uid": "test_user",
            "className": "class_5",
            "chapterId": "eesa101",
            "conceptPerformance": perf,
            "status": "ASSESSING",
            "attempts": 2
        }

        state = self.service.calculate_mastery_state(record, config)
        self.assertEqual(state["status"], "NEEDS_REMEDIATION")
        self.assertIn(weak_cid, state["remediation_needed"])

    def test_class5_flow(self):
        config = self.service.get_chapter_mastery_config("class_5", "english", "eesa101")
        self.assertIsNotNone(config)

        # Scenario: Start learning
        record = {
            "uid": "user5", "className": "class_5", "chapterId": "eesa101",
            "conceptPerformance": {}, "status": "NOT_STARTED", "attempts": 0
        }

        # Simulate some results
        concepts = config["concepts"]
        c1_id = concepts[0].get("conceptId") or concepts[0].get("id")

        # Partial results
        # transfer-1 question text contains "misplaced spectacles"
        quiz_results = [{"question_id": "transfer-1", "is_correct": True}]

        # Test process_quiz_results
        update = self.service.process_quiz_results(record, quiz_results, config)
        updated_record = update["updated_record"]

        self.assertEqual(updated_record["status"], "LEARNING")
        self.assertIn(c1_id, updated_record["conceptPerformance"])
        # It maps to 'application' because type is 'application'
        perf = updated_record["conceptPerformance"][c1_id]
        self.assertGreater(perf.get("foundation", 0) + perf.get("application", 0) + perf.get("mastery", 0), 0)

if __name__ == '__main__':
    unittest.main()
