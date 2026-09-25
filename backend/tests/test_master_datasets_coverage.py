import pytest
from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

REGISTERED_RENDERERS = {"overview", "terminology", "vocabulary", "text-section", "study-questions", "quiz", "flashcard-deck", "mindmap", "generic-structured"}

def test_all_47_chapters_ingestion_and_renderers():
    """Verify that all 47 chapters across all 4 subjects parse into valid ContentBlocks with assigned renderers."""
    subjects = ["English", "Hindi", "Maths", "Science"]
    total_chapters_audited = 0
    total_blocks_audited = 0

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        assert meta["curriculumFramework"] is not None
        assert len(meta["curricularGoals"]) == 4

        units = meta.get("units", [])
        assert len(units) > 0

        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                assert ch_source is not None, f"Source for {sub} {ch_id} must not be None"

                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)
                assert len(blocks) > 0, f"Blocks for {sub} {ch_id} must be > 0"

                for b in blocks:
                    assert b.renderer in REGISTERED_RENDERERS, f"Renderer '{b.renderer}' for block '{b.id}' must be registered"
                    total_blocks_audited += 1

                total_chapters_audited += 1

    assert total_chapters_audited == 47, f"Expected 47 chapters audited, got {total_chapters_audited}"
    assert total_blocks_audited >= 250, f"Expected >= 250 blocks audited, got {total_blocks_audited}"

def test_master_datasets_idempotency():
    """Idempotency Test: Running ingestion twice produces identical block counts."""
    ch_source = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    adapter1 = AdapterResolver.resolve("NCERT", "5", "English", ch_source)
    blocks1 = adapter1.parse_chapter(ch_source, "G5-ENG-U01-C01")

    adapter2 = AdapterResolver.resolve("NCERT", "5", "English", ch_source)
    blocks2 = adapter2.parse_chapter(ch_source, "G5-ENG-U01-C01")

    assert len(blocks1) == len(blocks2)
    assert [b.id for b in blocks1] == [b.id for b in blocks2]
