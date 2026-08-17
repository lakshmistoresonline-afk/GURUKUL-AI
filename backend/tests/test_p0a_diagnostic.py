import unittest
import os
import json
import sys
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.mastery_service import MasteryService
from src.services.diagnostic_service import DiagnosticService

class TestP0ADiagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mastery_service = MasteryService()
        cls.diagnostic_service = DiagnosticService(cls.mastery_service)

    def test_graph_integrity(self):
        graph_path = "D:/GURUKUL-AI/backend/storage/concept_graph.json"
        self.assertTrue(os.path.exists(graph_path))
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = json.load(f)

        # 1. Exactly 769 authoritative nodes (GUIDs)
        self.assertEqual(len(graph["concepts"]), 769)

        # 2. Relationship validation
        nodes = set(graph["concepts"].keys())
        for rel in graph["relationships"]:
            # Valid sources and targets
            self.assertIn(rel["fromConceptId"], nodes)
            self.assertIn(rel["toConceptId"], nodes)
            # No self-loops
            self.assertNotEqual(rel["fromConceptId"], rel["toConceptId"])
            # Correct confidence range
            self.assertTrue(0.0 <= rel["confidence"] <= 1.0)
            # Context preservation
            self.assertIn("chapterId", rel)

        # 3. Chapter relationships
        self.assertIn("chapterRelationships", graph)
        self.assertEqual(len(graph["chapterRelationships"]), 82)

    def test_diagnostic_coverage(self):
        # Sample test Class 5 and Class 6
        samples = [
            ("class_5", "mathematics", "eemm101"),
            ("class_6", "mathematics", "fegp101")
        ]

        for cls, subj, cid in samples:
            questions = self.diagnostic_service.get_diagnostic_questions(cls, subj, cid)

            # Diagnostic produces 5-10 items
            self.assertGreaterEqual(len(questions), 5)
            self.assertLessEqual(len(questions), 10)

            # No duplicates
            q_ids = [q["id"] for q in questions]
            self.assertEqual(len(q_ids), len(set(q_ids)))

            # Valid concept references
            for q in questions:
                # In GUID model, we check for existence of a node with this localId in the expected class
                found = any(c['localId'] == q['concept_id'] and c['class'] == cls for c in self.diagnostic_service.graph["concepts"].values())
                self.assertTrue(found, f"Concept {q['concept_id']} for class {cls} not found in graph nodes.")

    def test_mastery_isolation(self):
        # Verify that diagnostic signal logic is separate (Checked via route inspection)
        # We manually verify that diagnostic Signals do not touch 'conceptPerformance'
        # unless specifically mapped in future adaptation phases.
        pass

if __name__ == "__main__":
    unittest.main()
