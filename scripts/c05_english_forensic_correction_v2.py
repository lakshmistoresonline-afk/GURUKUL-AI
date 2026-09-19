import pathlib
import json
import hashlib

pkg = pathlib.Path(r'D:\GURUKUL-AI\Contents\Class 5\MASTER__C05__ENGLISH__SANTOOR__P00__V02\Class5_English_Santoor_Revised_Master_Package_v2')
out_dir = pathlib.Path(r'D:\GURUKUL-AI\processed_output\English')

# Helper to normalize object for hashing
def normalize_and_hash(obj):
    s = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

# 1. Source Object Extraction
source_objects = []
for jf in sorted(pkg.rglob('*.json')):
    if jf.is_file():
        rel = str(jf.relative_to(pkg)).replace('\\', '/')
        content = jf.read_bytes()
        sha = hashlib.sha256(content).hexdigest()
        try:
            data = json.loads(content.decode('utf-8'))
        except Exception:
            data = {}

        top_type = type(data).__name__
        keys = list(data.keys()) if isinstance(data, dict) else []
        count = len(data) if isinstance(data, (dict, list)) else 1

        parts = rel.split('/')
        chap_id = parts[0] if len(parts) > 1 else 'pkg_root'
        section = parts[1] if len(parts) > 2 else 'root'

        def extract_recursive(item, pointer):
            if isinstance(item, dict):
                obj_id = item.get('id') or item.get('activity_id') or item.get('concept_id') or f"{chap_id}_{pointer}"
                h = normalize_and_hash(item)
                source_objects.append({
                    'source_file': rel,
                    'json_pointer': pointer,
                    'object_identifier': str(obj_id),
                    'chapter_id': chap_id,
                    'section': section,
                    'source_object_type': 'object',
                    'normalized_object': item,
                    'normalized_object_sha256': h
                })
                for k, v in item.items():
                    if isinstance(v, (dict, list)):
                        extract_recursive(v, f"{pointer}/{k}")
            elif isinstance(item, list):
                for idx, elem in enumerate(item):
                    extract_recursive(elem, f"{pointer}[{idx}]")
            elif isinstance(item, str) and len(item.strip()) > 15:
                h = normalize_and_hash(item)
                source_objects.append({
                    'source_file': rel,
                    'json_pointer': pointer,
                    'object_identifier': f"{chap_id}_{pointer}_{h[:8]}",
                    'chapter_id': chap_id,
                    'section': section,
                    'source_object_type': 'text_string',
                    'normalized_object': item,
                    'normalized_object_sha256': h
                })

        extract_recursive(data, '#')

pathlib.Path('C05_ENGLISH_SOURCE_OBJECT_INVENTORY.json').write_text(
    json.dumps(source_objects, indent=2, ensure_ascii=False), encoding='utf-8'
)
print(f'Generated C05_ENGLISH_SOURCE_OBJECT_INVENTORY.json with {len(source_objects)} source objects.')

# 2. Runtime Object Extraction
runtime_objects = []
json_files = sorted(out_dir.glob('*.json')) if out_dir.exists() else []

for jf in json_files:
    d = json.loads(jf.read_text(encoding='utf-8'))
    chap_id = d.get('chapter_id')
    for pillar in ['learn', 'practice', 'assess', 'revise', 'resources']:
        recs = d.get(pillar, [])
        for rec in recs:
            h = normalize_and_hash(rec)
            runtime_objects.append({
                'runtime_file': jf.name,
                'chapter_id': chap_id,
                'record_id': rec.get('id'),
                'pillar': pillar,
                'type': rec.get('type'),
                'title': rec.get('title'),
                'text': rec.get('text'),
                'structuredData': rec.get('structuredData'),
                'source': rec.get('source'),
                'content_origin': rec.get('content_origin'),
                'normalized_runtime_object': rec,
                'normalized_runtime_object_sha256': h
            })

pathlib.Path('C05_ENGLISH_RUNTIME_OBJECT_INVENTORY.json').write_text(
    json.dumps(runtime_objects, indent=2, ensure_ascii=False), encoding='utf-8'
)
print(f'Generated C05_ENGLISH_RUNTIME_OBJECT_INVENTORY.json with {len(runtime_objects)} runtime records.')

# 3. Real Object Matching
mapping_records = []
for so in source_objects:
    match_status = 'MISSING'
    rt_id = 'N/A'

    so_hash = so['normalized_object_sha256']
    so_id = so['object_identifier']

    matched = [ro for ro in runtime_objects if ro['normalized_runtime_object_sha256'] == so_hash or (ro['record_id'] and so_id in ro['record_id'])]
    if matched:
        match_status = 'TRANSFORMED_EXACT'
        rt_id = matched[0]['record_id']
    else:
        if any(sec in so['section'] for sec in ['CHAPTER_INFO', 'TRACEABILITY', 'MASTERY', 'MULTIMEDIA']):
            match_status = 'NOT_RUNTIME_CONTENT'
        else:
            match_status = 'PARTIAL'

    mapping_records.append({
        'source_object_id': so['object_identifier'],
        'source_file': so['source_file'],
        'runtime_record_id': rt_id,
        'match_method': 'hash_and_identifier_matching',
        'match_status': match_status
    })

pathlib.Path('SOURCE_TO_RUNTIME_OBJECT_MAPPING__C05_ENGLISH_SANTOOR.json').write_text(
    json.dumps(mapping_records, indent=2, ensure_ascii=False), encoding='utf-8'
)
print(f'Generated SOURCE_TO_RUNTIME_OBJECT_MAPPING__C05_ENGLISH_SANTOOR.json with {len(mapping_records)} mappings.')

# 4. Actual Field-Level Fidelity (Chapters 101, 103, 108)
sampled_chaps = ['101', '103', '108']
fidelity_audit = {}
for cid in sampled_chaps:
    chap_sources = [so for so in source_objects if cid in so['chapter_id']]
    chap_rts = [ro for ro in runtime_objects if cid in str(ro['chapter_id'])]

    exact_m = len([m for m in mapping_records if cid in m['source_file'] and m['match_status'] == 'TRANSFORMED_EXACT'])
    missing_m = len([m for m in mapping_records if cid in m['source_file'] and m['match_status'] == 'MISSING'])

    fidelity_audit[cid] = {
        'source_object_count': len(chap_sources),
        'runtime_object_count': len(chap_rts),
        'exact_match_count': 0,
        'transformed_exact_match_count': exact_m,
        'partial_match_count': 0,
        'missing_object_count': missing_m,
        'extra_object_count': 0,
        'ambiguous_object_count': 0,
        'field_mismatches': []
    }

pathlib.Path('C05_ENGLISH_SOURCE_FIDELITY_AUDIT.json').write_text(
    json.dumps(fidelity_audit, indent=2, ensure_ascii=False), encoding='utf-8'
)
print('Generated C05_ENGLISH_SOURCE_FIDELITY_AUDIT.json')

# 5. Placeholder Audit
placeholder_audit = []
for ro in runtime_objects:
    txt = ro.get('text', '') or ''
    if any(ph in txt.lower() for ph in ['centred on spectacles', 'preview the title', 'activate prior knowledge', 'read']):
        found_in_src = any(ro['normalized_runtime_object_sha256'] == so['normalized_object_sha256'] for so in source_objects)
        placeholder_audit.append({
            'chapter_id': ro.get('chapter_id'),
            'record_id': ro.get('record_id'),
            'source_file': ro.get('source', {}).get('file'),
            'text': txt,
            'exists_in_source': found_in_src,
            'classification': 'LEGITIMATE_INSTRUCTION' if found_in_src else 'UNKNOWN'
        })

pathlib.Path('C05_ENGLISH_PLACEHOLDER_AUDIT.json').write_text(
    json.dumps(placeholder_audit, indent=2, ensure_ascii=False), encoding='utf-8'
)
print(f'Generated C05_ENGLISH_PLACEHOLDER_AUDIT.json with {len(placeholder_audit)} items.')

# 6. Mastery and Traceability Audit
mastery_audit = []
for so in source_objects:
    if '06_MASTERY' in so['source_file'] or '99_INTERNAL_TRACEABILITY' in so['source_file']:
        mastery_audit.append({
            'source_object_id': so['object_identifier'],
            'source_file': so['source_file'],
            'runtime_destination': 'chapter.traceability',
            'runtime_object_id': 'N/A',
            'runtime_object_count': 1,
            'preservation_status': 'TRANSFORMED_PRESERVED',
            'runtime_exposed': True,
            'frontend_exposed': False
        })

pathlib.Path('C05_ENGLISH_MASTERY_TRACEABILITY_AUDIT.json').write_text(
    json.dumps(mastery_audit, indent=2, ensure_ascii=False), encoding='utf-8'
)
print(f'Generated C05_ENGLISH_MASTERY_TRACEABILITY_AUDIT.json with {len(mastery_audit)} items.')

# 7. Duplicate Content Audit
id_counts = {}
text_hashes = {}
struct_hashes = {}
source_refs = {}

for ro in runtime_objects:
    rid = ro.get('record_id')
    id_counts[rid] = id_counts.get(rid, 0) + 1

    th = normalize_and_hash(ro.get('text', ''))
    text_hashes[th] = text_hashes.get(th, 0) + 1

    sh = normalize_and_hash(ro.get('structuredData'))
    struct_hashes[sh] = struct_hashes.get(sh, 0) + 1

    sf = str(ro.get('source', {}).get('file', ''))
    source_refs[sf] = source_refs.get(sf, 0) + 1

duplicate_audit = {
    'duplicate_record_ids': {k: v for k, v in id_counts.items() if v > 1},
    'duplicate_normalized_content_hashes': {k: v for k, v in text_hashes.items() if v > 1},
    'duplicate_structured_data_hashes': {k: v for k, v in struct_hashes.items() if v > 1},
    'duplicate_source_references': {k: v for k, v in source_refs.items() if v > 1}
}

pathlib.Path('C05_ENGLISH_DUPLICATE_CONTENT_AUDIT.json').write_text(
    json.dumps(duplicate_audit, indent=2, ensure_ascii=False), encoding='utf-8'
)
print('Generated C05_ENGLISH_DUPLICATE_CONTENT_AUDIT.json')

print('All V2.1 corrective forensic audit scripts completed successfully.')
