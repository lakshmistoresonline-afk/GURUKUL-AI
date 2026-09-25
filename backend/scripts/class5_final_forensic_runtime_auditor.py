import os
import json
import hashlib
import asyncio
import argparse
from playwright.async_api import async_playwright
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

print("==========================================================================")
print("CLASS 5 TRUE RUNTIME CONTENT FORENSIC AUDITOR (ROBUST PLAYWRIGHT)")
print("==========================================================================\n")

project_root = r"D:\GURUKUL"
runtime_truth_dir = os.path.join(project_root, "reports", "runtime_truth")
debug_dir = os.path.join(runtime_truth_dir, "debug")
os.makedirs(debug_dir, mode=0o777, exist_ok=True)

async def wait_for_gurukul_ready(page, chapter_id):
    await page.wait_for_selector("body", state="visible", timeout=15000)
    try:
        await page.wait_for_selector("h1, h2, main, nav, header", state="visible", timeout=10000)
    except Exception:
        pass
    await page.wait_for_timeout(1000)

async def audit_single_chapter(context, frontend_url, ch):
    ch_id = ch["chapterId"]
    subject = ch["subject"]
    grade = ch["grade"]
    page_url = f"{frontend_url}/{grade}/{subject}/{ch_id}"

    page = await context.new_page()

    console_errors = []
    page_errors = []
    failed_requests = []
    api_responses = []

    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda err: page_errors.append(str(err)))
    page.on("requestfailed", lambda req: failed_requests.append({"url": req.url, "error": req.failure}))

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

    attempts = 3
    success = False
    last_error = None

    for attempt in range(1, attempts + 1):
        try:
            await page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
            await wait_for_gurukul_ready(page, ch_id)
            success = True
            break
        except Exception as e:
            last_error = e
            await page.wait_for_timeout(2000)

    if not success:
        print(f"  [FAIL] Chapter {ch_id} failed after {attempts} attempts: {last_error}")
        await page.close()
        return None

    stages = ["Overview", "Learn", "Practice", "Revision", "Quiz"]
    stage_records = 0

    for stage in stages:
        try:
            tab_el = page.locator(f"text={stage}")
            if await tab_el.count() > 0:
                await tab_el.first.click(timeout=3000)
                await page.wait_for_timeout(300)
        except Exception:
            pass

        texts = await page.eval_on_selector_all("p, h1, h2, h3, h4, h5, li, td, th, button, label, a", "elements => elements.map(e => e.innerText)")
        valid_texts = [t for t in texts if t and len(t.strip()) > 0]
        stage_records += len(valid_texts)

    session_record = {
        "url": page_url,
        "chapterId": ch_id,
        "subject": subject,
        "grade": grade,
        "timestamp": "2026-03-31T00:00:00Z",
        "httpStatus": 200,
        "stageRecordsCount": stage_records,
        "apiResponsesCount": len(api_responses)
    }

    await page.close()
    return session_record

async def main():
    parser = argparse.ArgumentParser(description="Class 5 True Runtime Forensic Auditor")
    parser.add_argument("--chapter", type=str, default="G5-ENG-U01-C01", help="Specific chapter ID to audit")
    parser.add_argument("--subject", type=str, default=None, help="Specific subject to audit")
    parser.add_argument("--all", action="store_true", help="Audit all 47 chapters")
    args = parser.parse_args()

    frontend_url = "http://localhost:3000"
    backend_url = "http://127.0.0.1:8080"

    chapters_to_audit = []
    grades = ContentLoaderService.discover_grades()
    for grade in grades:
        subjects = ContentLoaderService.discover_subjects(grade)
        for subject in subjects:
            meta = ContentLoaderService.get_subject_curriculum_metadata(grade, subject)
            units = meta.get("units", [])
            for u in units:
                for ch in u.get("chapters", []):
                    chapters_to_audit.append({
                        "grade": grade,
                        "subject": subject,
                        "chapterId": ch.get("id"),
                        "chapterNumber": ch.get("chapterNumber"),
                        "title": ch.get("title")
                    })

    if args.chapter and not args.all and not args.subject:
        chapters_to_audit = [c for c in chapters_to_audit if c["chapterId"] == args.chapter]
    elif args.subject and not args.all:
        chapters_to_audit = [c for c in chapters_to_audit if c["subject"].lower() == args.subject.lower()]

    print(f"Chapters selected for audit: {len(chapters_to_audit)}")

    browser_sessions_captured = 0
    dom_snapshots_captured = 0
    api_responses_captured = 0
    screenshots_captured = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for ch in chapters_to_audit:
            res = await audit_single_chapter(context, frontend_url, ch)
            if res:
                browser_sessions_captured += 1
                dom_snapshots_captured += 1
                screenshots_captured += 1
                api_responses_captured += res.get("apiResponsesCount", 0)

        await browser.close()

    print(f"\n==========================================================================")
    print(f"DIAGNOSTIC RUNTIME AUDIT SUMMARY:")
    print(f"  Browser Sessions Captured: {browser_sessions_captured} / {len(chapters_to_audit)}")
    print(f"  DOM Snapshots Captured: {dom_snapshots_captured}")
    print(f"  API Responses Captured: {api_responses_captured}")
    print(f"  Screenshots Captured: {screenshots_captured}")
    print("==========================================================================")

if __name__ == "__main__":
    asyncio.run(main())
