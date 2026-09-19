import unittest
from pathlib import Path
import tempfile
import shutil

from processors.common.source.context import ProcessingContext
from processors.common.source.profile import SourceProfile
from processors.common.registry import SubjectRegistry
from processors.english.processor import EnglishSubjectProcessor
from processors.hindi.processor import HindiSubjectProcessor
from processors.mathematics.processor import MathematicsSubjectProcessor
from processors.evs.processor import EVSSubjectProcessor

class TestProcessorArchitecture(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.package_dir = self.temp_path / "pkg"
        self.package_dir.mkdir()
        self.output_dir = self.temp_path / "out"
        self.output_dir.mkdir()

        # Create valid synthetic chapter folder
        chap_dir = self.package_dir / "101_Test_Chapter"
        chap_dir.mkdir()
        (chap_dir / "00_CHAPTER_INFO").mkdir()
        (chap_dir / "00_CHAPTER_INFO" / "CHAPTER_INFO.json").write_text(
            '{"chapter_id": "101", "title": "Test Chapter"}', encoding="utf-8"
        )
        (chap_dir / "01_LEARN" / "04_SOURCE_DERIVED").mkdir(parents=True)
        (chap_dir / "01_LEARN" / "04_SOURCE_DERIVED" / "SOURCE_PAGES.json").write_text(
            '{"pages": [{"source_page": 1, "text": "Sample source content for testing architecture."}]}', encoding="utf-8"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_1_context_requires_class(self):
        with self.assertRaises(ValueError):
            ProcessingContext(job_id="j1", class_level=None, subject="English", source_package="pkg.zip")

    def test_2_context_requires_subject(self):
        with self.assertRaises(ValueError):
            ProcessingContext(job_id="j1", class_level=5, subject="", source_package="pkg.zip")

    def test_3_profile_requires_class(self):
        with self.assertRaises(ValueError):
            SourceProfile(class_level=None, subject="English", book="Book", source_package="pkg.zip")

    def test_4_profile_requires_subject(self):
        with self.assertRaises(ValueError):
            SourceProfile(class_level=5, subject="", book="Book", source_package="pkg.zip")

    def test_5_profile_requires_book(self):
        with self.assertRaises(ValueError):
            SourceProfile(class_level=5, subject="English", book="", source_package="pkg.zip")

    def test_6_profile_requires_source_package(self):
        with self.assertRaises(ValueError):
            SourceProfile(class_level=5, subject="English", book="Book", source_package="")

    def test_7_matching_context_profile_succeeds(self):
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j1", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile)
        profile.validate_compatibility(context)  # Should not raise

    def test_8_class_mismatch_fails(self):
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j1", 6, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile)
        with self.assertRaises(ValueError):
            profile.validate_compatibility(context)

    def test_9_subject_mismatch_fails(self):
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j1", 5, "Hindi", "01_ENGLISH_COMPLETE.zip", source_profile=profile)
        with self.assertRaises(ValueError):
            profile.validate_compatibility(context)

    def test_10_source_package_mismatch_fails(self):
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j1", 5, "English", "other_package.zip", source_profile=profile)
        with self.assertRaises(ValueError):
            profile.validate_compatibility(context)

    def test_11_english_processor_class_5(self):
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j5", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile, output_dir=self.output_dir)
        processor = EnglishSubjectProcessor()
        res = processor.process(context, self.package_dir)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(str(res["class_level"]), "5")

    def test_12_english_processor_class_6(self):
        profile = SourceProfile(6, "English", "Poorvi Grade 6", "02_ENGLISH_COMPLETE_GRADE6.zip")
        context = ProcessingContext("j6", 6, "English", "02_ENGLISH_COMPLETE_GRADE6.zip", source_profile=profile, output_dir=self.output_dir)
        processor = EnglishSubjectProcessor()
        res = processor.process(context, self.package_dir)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(str(res["class_level"]), "6")

    def test_13_english_processor_class_7(self):
        profile = SourceProfile(7, "English", "Poorvi Grade 7", "02_ENGLISH_GRADE7_COMPLETE.zip")
        context = ProcessingContext("j7", 7, "English", "02_ENGLISH_GRADE7_COMPLETE.zip", source_profile=profile, output_dir=self.output_dir)
        processor = EnglishSubjectProcessor()
        res = processor.process(context, self.package_dir)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(str(res["class_level"]), "7")

    def test_14_sequential_reuse_no_stale_metadata(self):
        profile5 = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        ctx5 = ProcessingContext("j5", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile5, output_dir=self.output_dir)

        profile7 = SourceProfile(7, "English", "Poorvi Grade 7", "02_ENGLISH_GRADE7_COMPLETE.zip")
        ctx7 = ProcessingContext("j7", 7, "English", "02_ENGLISH_GRADE7_COMPLETE.zip", source_profile=profile7, output_dir=self.output_dir)

        processor = EnglishSubjectProcessor()
        res5 = processor.process(ctx5, self.package_dir)
        self.assertEqual(str(res5["class_level"]), "5")
        self.assertEqual(res5["book"], "Santoor")

        res7 = processor.process(ctx7, self.package_dir)
        self.assertEqual(str(res7["class_level"]), "7")
        self.assertEqual(res7["book"], "Poorvi Grade 7")

    def test_15_missing_chapter_id_fails(self):
        bad_chap = self.package_dir / "102_Bad_Chapter"
        bad_chap.mkdir()
        (bad_chap / "00_CHAPTER_INFO").mkdir()
        (bad_chap / "00_CHAPTER_INFO" / "CHAPTER_INFO.json").write_text(
            '{"title": "Missing ID"}', encoding="utf-8"
        )
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j_bad", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile, output_dir=self.output_dir)
        processor = EnglishSubjectProcessor()
        with self.assertRaises(ValueError):
            processor.process(context, self.package_dir)

    def test_16_invalid_chapter_metadata_fails(self):
        bad_chap = self.package_dir / "103_Invalid_Chapter"
        bad_chap.mkdir()
        (bad_chap / "00_CHAPTER_INFO").mkdir()
        (bad_chap / "00_CHAPTER_INFO" / "CHAPTER_INFO.json").write_text(
            '{"chapter_id": "   ", "title": "Blank ID"}', encoding="utf-8"
        )
        profile = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        context = ProcessingContext("j_blank", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile, output_dir=self.output_dir)
        processor = EnglishSubjectProcessor()
        with self.assertRaises(ValueError):
            processor.process(context, self.package_dir)

    def test_17_registry_resolves_supported_subjects(self):
        self.assertEqual(SubjectRegistry.get_processor("English"), EnglishSubjectProcessor)
        self.assertEqual(SubjectRegistry.get_processor("Hindi"), HindiSubjectProcessor)
        self.assertEqual(SubjectRegistry.get_processor("Mathematics"), MathematicsSubjectProcessor)
        self.assertEqual(SubjectRegistry.get_processor("EVS"), EVSSubjectProcessor)

    def test_18_registry_rejects_unsupported(self):
        with self.assertRaises(ValueError):
            SubjectRegistry.get_processor("Science")

    def test_19_no_class_specific_processors(self):
        self.assertNotIn("Class5EnglishProcessor", globals())

    def test_20_no_constructor_class_default(self):
        import inspect
        sig = inspect.signature(EnglishSubjectProcessor.__init__)
        for param in sig.parameters.values():
            if param.name == "class_level":
                self.fail("Found hardcoded class_level parameter in constructor")

    def test_21_cross_class_contamination_prevention(self):
        profile5 = SourceProfile(5, "English", "Santoor", "01_ENGLISH_COMPLETE.zip")
        ctx5 = ProcessingContext("j5", 5, "English", "01_ENGLISH_COMPLETE.zip", source_profile=profile5, output_dir=self.output_dir)

        profile6 = SourceProfile(6, "English", "Poorvi Grade 6", "02_ENGLISH_COMPLETE_GRADE6.zip")
        ctx6 = ProcessingContext("j6", 6, "English", "02_ENGLISH_COMPLETE_GRADE6.zip", source_profile=profile6, output_dir=self.output_dir)

        processor = EnglishSubjectProcessor()
        res5 = processor.process(ctx5, self.package_dir)
        res6 = processor.process(ctx6, self.package_dir)

        self.assertNotEqual(res5["class_level"], res6["class_level"])
        self.assertNotEqual(res5["book"], res6["book"])
        for chap in res6["chapters"]:
            self.assertTrue(chap.startswith("class_6"))
