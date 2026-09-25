import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder, PRESENTATION_CONFIGS

ch_id = "G5-SCI-U01-C01"
ch_source = ContentLoaderService.load_chapter_source("5", "Science", ch_id)

print("==========================================================================")
print(f"FORENSIC SCIENCE NAVIGATION PIPELINE TRACE FOR {ch_id}")
print("==========================================================================\n")

print("Science PRESENTATION_CONFIGS keys in navigation_builder.py:", list(PRESENTATION_CONFIGS.keys()))
sci_config = PRESENTATION_CONFIGS.get("science", {})
print("\nScience Config Groups in navigation_builder.py:")
for g in sci_config.get("groups", []):
    print(f"  Group ID: {g['id']:<15} | Label: {g['label']:<15} | order: {g.get('order')} | contentTypes: {g['contentTypes']}")

adapter = AdapterResolver.resolve("NCERT", "5", "Science", ch_source)
blocks = adapter.parse_chapter(ch_source, ch_id)
manifest = adapter.generate_manifest(ch_id, blocks)

print(f"\nManifest contentTypes for {ch_id}: {[t.type for t in manifest.contentTypes]}")

tabs = BackendNavigationBuilder.build_navigation("Science", manifest)
print(f"\nComputed Navigation Tabs for {ch_id}:")
for t in tabs:
    print(f"  Tab ID: {t['id']:<15} | Label: {t['label']:<15} | contentTypes: {t['contentTypes']}")
