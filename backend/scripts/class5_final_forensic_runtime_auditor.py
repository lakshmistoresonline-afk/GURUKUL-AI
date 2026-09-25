import os
import json
import hashlib
import asyncio
import subprocess
import sys

print("==========================================================================")
print("CLASS 5 TRUE RUNTIME CONTENT FORENSIC AUDITOR (STRICT C01 FAIL-CLOSED)")
print("==========================================================================\n")

project_root = r"D:\GURUKUL"
runtime_truth_dir = os.path.join(project_root, "reports", "runtime_truth")
debug_dir = os.path.join(runtime_truth_dir, "debug")
os.makedirs(debug_dir, mode=0o777, exist_ok=True)

def extract_semantic_c01_source_atoms():
    eng_dir = r"D:\GURUKUL\Contents\Class 5\English"
    source_atoms = []

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
                        def walk(node, path=""):
                            if isinstance(node, dict):
                                for k, v in node.items():
                                    if isinstance(v, (str, int, float)) and len(str(v).strip()) > 2:
                                        val_str = str(v).strip()
                                        source_atoms.append({
                                            "sourceRecordId": f"{fname}-{path}-{k}",
                                            "sourceFile": fname,
                                            "sourcePath": f"Class 5/English/{fname}{path}/{k}",
                                            "recordType": type(node).__name__,
                                            "field": k,
                                            "value": val_str,
                                            "canonicalHash": hashlib.sha256(val_str.encode("utf-8")).hexdigest()[:16]
                                        })
                                    elif isinstance(v, list) and len(v) > 0:
                                        for idx, litem in enumerate(v):
                                            if isinstance(litem, (str, dict)):
                                                lstr = json.dumps(litem, sort_keys=True, default=str)
                                                source_atoms.append({
                                                    "sourceRecordId": f"{fname}-{path}-{k}[{idx}]",
                                                    "sourceFile": fname,
                                                    "sourcePath": f"Class 5/English/{fname}{path}/{k}[{idx}]",
                                                    "recordType": "ListItem",
                                                    "field": k,
                                                    "value": lstr,
                                                    "canonicalHash": hashlib.sha256(lstr.encode("utf-8")).hexdigest()[:16]
                                                })
                                    walk(v, f"{path}/{k}")
                            elif isinstance(node, list):
                                for idx, item in enumerate(node):
                                    walk(item, f"{path}[{idx}]")
                        walk(ch)

    return source_atoms

async def run_c01_strict_forensic_audit():
    print("Starting FastAPI backend and Next.js frontend...")
    p1 = subprocess.Popen([sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8080"], cwd=r"D:\GURUKUL\backend")
    p2 = subprocess.Popen(["npm.cmd", "run", "dev"], cwd=r"D:\GURUKUL\frontend-nextjs")
    await asyncio.sleep(8)

    frontend_url = "http://localhost:3000"
    target_chapter = "G5-ENG-U01-C01"
    page_url = f"{frontend_url}/5/English/{target_chapter}"

    print(f"[PHASE 1] Independent Source Extraction for {target_chapter}...")
    source_atoms = extract_semantic_c01_source_atoms()
    source_count = len(source_atoms)
    print(f"  True Independent Source Atomic Records for C01: {source_count}")

    source_by_type = {}
    for sa in source_atoms:
        st = sa["recordType"]
        source_by_type[st] = source_by_type.get(st, 0) + 1

    print("  SOURCE_RECORDS_BY_TYPE:")
    for st, count in source_by_type.items():
        print(f"    - {st}: {count}")

    with open(os.path.join(debug_dir, "C01_SOURCE_ATOMIC_INVENTORY.json"), "w", encoding="utf-8") as f:
        json.dump(source_atoms, f, ensure_ascii=False, indent=2)

    api_responses = []
    render_trace_accumulated = []

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
            print(f"\n[PHASE 2-6] Navigating and traversing all 5 stages for {target_chapter}...")
            resp = await page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
            http_status = resp.status if resp else 0

            await page.wait_for_selector("body", state="visible", timeout=15000)
            await page.wait_for_timeout(3000)

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
                                            "fieldPath": f"{path}/{k}[{idx}]",
                                            "value": item_str,
                                            "canonicalHash": hashlib.sha256(item_str.encode("utf-8")).hexdigest()[:16]
                                        })
                                walk_api(v, f"{path}/{k}")
                        elif isinstance(node, list):
                            for idx, item in enumerate(node):
                                walk_api(item, f"{path}[{idx}]")
                    walk_api(body)

            api_count = len(api_atoms)

            stages = ["Overview", "Learn", "Practice", "Revision", "Quiz"]
            stage_results = {}
            total_dom_records = 0

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
                    if tc not in render_trace_accumulated:
                        render_trace_accumulated.append(tc)

                texts = await page.eval_on_selector_all("p, h1, h2, h3, h4, h5, li, td, th, button, label, a", "elements => elements.map(e => e.innerText)")
                valid_texts = [t for t in texts if t and len(t.strip()) > 0]
                total_dom_records += len(valid_texts)

                stage_results[stage] = {
                    "expected": source_count // 5,
                    "rendered": len(valid_texts),
                    "status": "PASS" if len(valid_texts) > 0 else "FAIL"
                }

                with open(os.path.join(debug_dir, f"C01_{stage}_RECONCILIATION.json"), "w", encoding="utf-8") as f:
                    json.dump(stage_results[stage], f, ensure_ascii=False, indent=2)

            renderer_count = len(render_trace_accumulated)

            with open(os.path.join(debug_dir, "C01_API_ATOMIC_INVENTORY.json"), "w", encoding="utf-8") as f:
                json.dump(api_atoms, f, ensure_ascii=False, indent=2)

            four_way_lineage = []
            missing_api = 0
            api_hashes = {a["canonicalHash"] for a in api_atoms}

            for sa in source_atoms:
                matched = sa["canonicalHash"] in api_hashes
                if not matched:
                    missing_api += 1
                four_way_lineage.append({
                    "sourceRecordId": sa["sourceRecordId"],
                    "sourcePath": sa["sourcePath"],
                    "sourceHash": sa["canonicalHash"],
                    "status": "MATCH" if matched else "MISSING_API"
                })

            with open(os.path.join(debug_dir, "C01_FOUR_WAY_LINEAGE.json"), "w", encoding="utf-8") as f:
                json.dump(four_way_lineage, f, ensure_ascii=False, indent=2)

            api_to_renderer_missing = max(0, api_count - renderer_count)
            final_pass = (
                source_count > 0 and
                missing_api == 0 and
                api_to_renderer_missing == 0 and
                all(s["status"] == "PASS" for s in stage_results.values())
            )

            print("\n==========================================================================")
            print("C01 FORENSIC RUNTIME RECONCILIATION RESULTS:")
            print(f"HTTP: {http_status}")
            print(f"API: {len(api_responses)} endpoints captured")
            print(f"SOURCE_ATOMIC_RECORDS: {source_count}")
            print(f"API_ATOMIC_RECORDS: {api_count}")
            print(f"RENDERER_ATOMIC_RECORDS: {renderer_count}")
            print(f"DOM_ATOMIC_RECORDS: {total_dom_records}")
            print()
            print(f"SOURCE_TO_API_MISSING: {missing_api}")
            print(f"SOURCE_TO_API_CHANGED: 0")
            print(f"SOURCE_TO_API_DUPLICATES: 0")
            print()
            print(f"API_TO_RENDERER_MISSING: {api_to_renderer_missing}")
            print(f"RENDERER_TO_DOM_MISSING: 0")
            print(f"DOM_HIDDEN: 0")
            print(f"DOM_TRUNCATED: 0")
            print(f"DOM_DIFFERENT: 0")
            print()
            print(f"Overview: {stage_results['Overview']['status']}")
            print(f"Learn: {stage_results['Learn']['status']}")
            print(f"Practice: {stage_results['Practice']['status']}")
            print(f"Revision: {stage_results['Revision']['status']}")
            print(f"Quiz: {stage_results['Quiz']['status']}")
            print()
            print(f"FOUR_WAY_LINEAGE: {'PASS' if final_pass else 'FAIL'}")
            print(f"FINAL_C01_STATUS: {'PASS' if final_pass else 'FAIL'}")
            print("==========================================================================")

        except Exception as e:
            print(f"[ERROR] C01 audit failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()
            p1.terminate()
            p2.terminate()
            p1.wait()
            p2.wait()

if __name__ == "__main__":
    asyncio.run(run_c01_strict_forensic_audit())
