import pytest
from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

def test_real_data_discovery():
    grades = ContentLoaderService.discover_grades()
    assert "5" in grades

    subjects = ContentLoaderService.discover_subjects("5")
    assert "English" in subjects

def test_chapter_processing_and_idempotency():
    # First Run
    ch_id = "G5-ENG-U01-C01"
    data1 = ContentLoaderService.load_chapter_source("5", "English", ch_id)
    assert data1 is not None

    adapter1 = AdapterResolver.resolve("NCERT", "5", "English", data1)
    blocks1 = adapter1.parse_chapter(data1, ch_id)
    manifest1 = adapter1.generate_manifest(ch_id, blocks1)
    nav1 = BackendNavigationBuilder.build_navigation("English", manifest1)

    # Second Run
    data2 = ContentLoaderService.load_chapter_source("5", "English", ch_id)
    adapter2 = AdapterResolver.resolve("NCERT", "5", "English", data2)
    blocks2 = adapter2.parse_chapter(data2, ch_id)
    manifest2 = adapter2.generate_manifest(ch_id, blocks2)
    nav2 = BackendNavigationBuilder.build_navigation("English", manifest2)

    # IDEMPOTENCY CHECK
    assert [b.id for b in blocks1] == [b.id for b in blocks2]
    assert [b.sourceType for b in blocks1] == [b.sourceType for b in blocks2]
    assert manifest1.dict() == manifest2.dict()
    assert nav1 == nav2

def test_all_10_chapters_processed():
    files = ContentLoaderService.load_raw_subject_files("5", "English")
    notes = files.get("santoor_chapters_notes.json", {}).get("chapters", [])
    assert len(notes) == 10

    total_blocks = 0
    for c in notes:
        u = c["unitNumber"]
        ch = c["chapterNumber"]
        ch_id = f"G5-ENG-U{u:02d}-C{ch:02d}"

        data = ContentLoaderService.load_chapter_source("5", "English", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
        blocks = adapter.parse_chapter(data, ch_id)
        manifest = adapter.generate_manifest(ch_id, blocks)

        assert len(blocks) > 0
        assert len(manifest.contentTypes) > 0
        total_blocks += len(blocks)

    assert total_blocks > 30
