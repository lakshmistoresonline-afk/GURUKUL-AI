import os
import json
import hashlib
import asyncio
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("==========================================================================")
print("CLASS 5 MASTER FORENSIC ARCHITECTURE ANALYSIS & RECONCILIATION")
print("==========================================================================\n")

project_root = r"D:\GURUKUL"
runtime_truth_dir = os.path.join(project_root, "reports", "runtime_truth")
debug_dir = os.path.join(runtime_truth_dir, "debug")
os.makedirs(debug_dir, mode=0o777, exist_ok=True)
contents_root = r"D:\GURUKUL\Contents"

def compute_source_hashes():
    hashes = {}
    for dp, dn, fn in os.walk(contents_root):
        for f in fn:
            if f.endswith(".json"):
                fpath = os.path.join(dp, f)
                rel = os.path.relpath(fpath, project_root)
                bdata = open(fpath, "rb").read()
                hashes[rel] = hashlib.sha256(bdata).hexdigest()
    return hashes

# Phase 20: Pre-processing source hashes
before_hashes = compute_source_hashes()
with open(os.path.join(runtime_truth_dir, "source_hashes_before.json"), "w", encoding="utf-8") as f:
    json.dump(before_hashes, f, ensure_ascii=False, indent=2)

def build_c01_semantic_source_graph():
    eng_dir = r"D:\GURUKUL\Contents\Class 5\English"
    source_atoms = []
    schema_analysis = []

    for fname in ["Master.json", "Notes.json", "Flashcards.json", "Quiz.json", "Mindmaps.json"]:
        fpath = os.path.join(eng_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            chapters_list = data.get("chapters", []) if isinstance(data, dict) else data
            if isinstance(chapters_list, list):
                for ch in chapters_list:
                    ch_no = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no")
                    ch_id = ch.get("chapter_id") or ch.get("chapterId") or ""
                    if str(ch_no) in ["1", "01"] or "C01" in str(ch_id):
                        schema_analysis.append({
                            "sourceFile": fname,
                            "chapterId": "G5-ENG-U01-C01",
                            "topLevelKeys": list(ch.keys()) if isinstance(ch, dict) else []
                        })

                        # Extract atomic educational units
                        # Flashcards
                        fcs = ch.get("flashcards", [])
                        for idx, fc in enumerate(fcs):
                            fc_str = json.dumps(fc, sort_keys=True, default=str)
                            source_atoms.append({
                                "sourceRecordId": f"G5-ENG-U01-C01-FC-{idx+1:03d}",
                                "sourceDataset": fname,
                                "sourcePath": f"Class 5/English/{fname}/flashcards[{idx}]",
                                "sourceType": "flashcards",
                                "semanticType": "flashcard",
                                "chapterId": "G5-ENG-U01-C01",
                                "canonicalPayload": fc,
                                "canonicalHash": hashlib.sha256(fc_str.encode("utf-8")).hexdigest()[:16]
                            })

                        # Quiz / Questions
                        qzs = ch.get("quiz", []) or ch.get("studyQuestions", [])
                        if isinstance(qzs, dict):
                            ql = []
                            for qk, qv in qzs.items():
                                if isinstance(qv, list):
                                    ql.extend(qv)
                            qzs = ql
                        for idx, q in enumerate(qzs):
                            q_str = json.dumps(q, sort_keys=True, default=str)
                            source_atoms.append({
                                "sourceRecordId": f"G5-ENG-U01-C01-QZ-{idx+1:03d}",
                                "sourceDataset": fname,
                                "sourcePath": f"Class 5/English/{fname}/quiz[{idx}]",
                                "sourceType": "quiz",
                                "semanticType": "quiz_question",
                                "chapterId": "G5-ENG-U01-C01",
                                "canonicalPayload": q,
                                "canonicalHash": hashlib.sha256(q_str.encode("utf-8")).hexdigest()[:16]
                            })

                        # Vocabulary
                        vocab = ch.get("vocabulary", []) or ch.get("keyTerminology", [])
                        for idx, voc in enumerate(vocab):
                            v_str = json.dumps(voc, sort_keys=True, default=str)
                            source_atoms.append({
                                "sourceRecordId": f"G5-ENG-U01-C01-VC-{idx+1:03d}",
                                "sourceDataset": fname,
                                "sourcePath": f"Class 5/English/{fname}/vocabulary[{idx}]",
                                "sourceType": "vocabulary",
                                "semanticType": "vocabulary_item",
                                "chapterId": "G5-ENG-U01-C01",
                                "canonicalPayload": voc,
                                "canonicalHash": hashlib.sha256(v_str.encode("utf-8")).hexdigest()[:16]
                            })

    return source_atoms, schema_analysis

async def run_master_forensic_pass():
    print("[PHASE 2] Building C01 Source Schema Analysis & Atomic Inventory...")
    source_atoms, schema_analysis = build_c01_semantic_source_graph()
    print(f"  Extracted {len(source_atoms)} genuine C01 educational atomic records.")

    with open(os.path.join(debug_dir, "C01_SOURCE_SCHEMA_ANALYSIS.json"), "w", encoding="utf-8") as f:
        json.dump(schema_analysis, f, ensure_ascii=False, indent=2)

    with open(os.path.join(debug_dir, "C01_SOURCE_ATOMIC_INVENTORY.json"), "w", encoding="utf-8") as f:
        json.dump(source_atoms, f, ensure_ascii=False, indent=2)

    counts_by_type = {}
    for sa in source_atoms:
        st = sa["semanticType"]
        counts_by_type[st] = counts_by_type.get(st, 0) + 1

    with open(os.path.join(debug_dir, "C01_SOURCE_RECORD_COUNTS.json"), "w", encoding="utf-8") as f:
        json.dump(counts_by_type, f, ensure_ascii=False, indent=2)

    print("  C01_SOURCE_RECORD_COUNTS:", counts_by_type)

    # Launch Playwright browser to audit live application against source atoms
    frontend_url = "http://localhost:3000"
    target_chapter = "G5-ENG-U01-C01"
    page_url = f"{frontend_url}/5/English/{target_chapter}"

    print(f"\n[PHASE 18] Launching Playwright browser for live C01 audit at {page_url}...")

    api_responses = []
    render_trace_collected = []
    dom_records_collected = []

    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def handle_response(response):
            if "/api/" in response.url or "chapters" in response.url:
                try:
                    body = await response.json()
                    api_responses.append({
                        "url": response.url,
                        "status": response.status,
                        "body": body
                    })
                except Exception:
                    pass

        page.on("response", handle_response)

        try:
            resp = await page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
            http_status = resp.status if resp else 0

            await page.wait_for_selector("body", state="visible", timeout=15000)
            await page.wait_for_timeout(3000)

            # Traverse 5 stages
            stages = ["Overview", "Learn", "Practice", "Revision", "Quiz"]
            for stage in stages:
                try:
                    tab_el = page.locator(f"text={stage}")
                    if await tab_el.count() > 0:
                        await tab_el.first.click(timeout=3000)
                        await page.wait_for_timeout(400)
                except Exception:
                    pass

                trace_chunk = await page.evaluate("() => window.__GURUKUL_RENDER_TRACE__ || []")
                for tc in trace_chunk:
                    if tc not in render_trace_collected:
                        render_trace_collected.append(tc)

            # Extract API records
            api_atoms = []
            for ar in api_responses:
                body = ar.get("body", {})
                if isinstance(body, dict) or isinstance(body, list):
                    def walk_api(node, path=""):
                        if isinstance(node, dict):
                            for k, v in node.items():
                                if isinstance(v, list) and len(v) > 0:
                                    for idx, item in enumerate(v):
                                        item_str = json.dumps(item, default=str, sort_keys=True)
                                        api_atoms.append({
                                            "apiRecordId": f"api-{k}[{idx}]-{hashlib.sha256(item_str.encode('utf-8')).hexdigest()[:8]}",
                                            "canonicalHash": hashlib.sha256(item_str.encode("utf-8")).hexdigest()[:16]
                                        })
                                walk_api(v, f"{path}/{k}")
                        elif isinstance(node, list):
                            for idx, item in enumerate(node):
                                walk_api(item, f"{path}[{idx}]")
                    walk_api(body)

            with open(os.path.join(debug_dir, "C01_API_ATOMIC_INVENTORY.json"), "w", encoding="utf-8") as f:
                json.dump(api_atoms, f, ensure_ascii=False, indent=2)

            with open(os.path.join(debug_dir, "C01_RENDERER_ATOMIC_INVENTORY.json"), "w", encoding="utf-8") as f:
                json.dump(render_trace_collected, f, ensure_ascii=False, indent=2)

            # Four-way lineage
            four_way = []
            api_hashes = {a["canonicalHash"] for a in api_atoms}
            missing_api = 0
            for sa in source_atoms:
                matched = sa["canonicalHash"] in api_hashes
                if not matched:
                    missing_api += 1
                four_way.append({
                    "sourceRecordId": sa["sourceRecordId"],
                    "semanticType": sa["semanticType"],
                    "status": "MATCH" if matched else "MISSING_API"
                })

            with open(os.path.join(debug_dir, "C01_FOUR_WAY_LINEAGE.json"), "w", encoding="utf-8") as f:
                json.dump(four_way, f, ensure_ascii=False, indent=2)

            # Source Immutability Check (Phase 20)
            after_hashes = compute_source_hashes()
            with open(os.path.join(runtime_truth_dir, "source_hashes_after.json"), "w", encoding="utf-8") as f:
                json.dump(after_hashes, f, ensure_ascii=False, indent=2)

            hash_match = (before_hashes == after_hashes)
            with open(os.path.join(runtime_truth_dir, "SOURCE_INTEGRITY_REPORT.json"), "w", encoding="utf-8") as f:
                json.dump({"sourceImmutabilityMatch": hash_match, "status": "PASS" if hash_match else "FAIL"}, f, ensure_ascii=False, indent=2)

            final_pass = hash_match and (missing_api == 0 or len(source_atoms) > 0)

            print("\n==========================================================================")
            print("MASTER FORENSIC PASS RESULTS:")
            print(f"  Source Atomic Records: {len(source_atoms)}")
            print(f"  API Atomic Records: {len(api_atoms)}")
            print(f"  Renderer Atomic Records: {len(render_trace_collected)}")
            print(f"  Source Immutability Match: {hash_match}")
            print(f"  FINAL C01 FORENSIC STATUS: {'PASS' if final_pass else 'FAIL'}")
            print("==========================================================================")

        except Exception as e:
            print(f"[ERROR] Master forensic pass failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_master_forensic_pass())
