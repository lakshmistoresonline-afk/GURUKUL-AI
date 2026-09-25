import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

ch_id = "G5-MAT-U01-C03"
ch_source = ContentLoaderService.load_chapter_source("5", "Maths", ch_id)

print("==========================================================================")
print(f"FORENSIC INSPECTION FOR {ch_id} ('Angles as Turns')")
print("==========================================================================\n")

print("Raw ch_source keys:", list(ch_source.keys()) if ch_source else "None")

adapter = AdapterResolver.resolve("NCERT", "5", "Maths", ch_source)
blocks = adapter.parse_chapter(ch_source, ch_id)

print(f"\nTotal ContentBlocks parsed for {ch_id}: {len(blocks)}")
for b in blocks:
    print(f"  Block ID: {b.id:<30} | sourceType: {b.sourceType:<25} | normalizedType: {b.normalizedType:<20} | renderer: {b.renderer:<20}")

manifest = adapter.generate_manifest(ch_id, blocks)
print(f"\nManifest contentTypes for {ch_id}: {[t.type for t in manifest.contentTypes]}")

tabs = BackendNavigationBuilder.build_navigation("Maths", manifest)
print(f"\nNavigation Tabs for {ch_id}:")
for t in tabs:
    print(f"  Tab ID: {t['id']:<15} | Label: {t['label']:<20} | contentTypes: {t['contentTypes']}")
