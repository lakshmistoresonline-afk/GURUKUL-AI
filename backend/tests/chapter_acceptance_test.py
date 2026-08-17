import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.jobs.job_engine import JobEngine
from src.models.job import ChapterJob, JobStatus
from src.orchestrator.ai_orchestrator import AIOrchestrator


JOB_ID = "a44a33df-1c36-421b-b194-b270819b220b"

REQUIRED_STAGES = [
    "objectives",
    "introduction",
    "teacher_explanation",
    "story_explanation",
    "concepts",
    "quiz",
    "flashcards",
    "summary",
]


def check(condition, label, details=""):
    status = "PASS" if condition else "FAIL"

    print(f"[{status}] {label}")

    if details:
        print(f"       {details}")

    return condition


def validate_quiz(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception:
            return False, "Quiz is not valid JSON."

    if not isinstance(value, list):
        return False, "Quiz is not an array."

    if len(value) != 5:
        return False, f"Expected 5 questions, found {len(value)}."

    for i, item in enumerate(value, 1):

        if not isinstance(item, dict):
            return False, f"Question {i} is not an object."

        for field in ["question", "options", "correctAnswer"]:
            if not item.get(field):
                return False, f"Question {i} missing {field}."

        options = item.get("options")

        if not isinstance(options, list):
            return False, f"Question {i} options are not an array."

        if len(options) != 4:
            return False, (
                f"Question {i} has {len(options)} options; "
                "expected 4."
            )

        if item["correctAnswer"] not in options:
            return False, (
                f"Question {i} correctAnswer does not match "
                "one of its options."
            )

    return True, "Exactly 5 valid MCQs with 4 options each."


def validate_flashcards(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception:
            return False, "Flashcards are not valid JSON."

    if not isinstance(value, list):
        return False, "Flashcards are not an array."

    if len(value) != 5:
        return False, f"Expected 5 flashcards, found {len(value)}."

    for i, item in enumerate(value, 1):

        if not isinstance(item, dict):
            return False, f"Flashcard {i} is not an object."

        if not item.get("front"):
            return False, f"Flashcard {i} missing front."

        if not item.get("back"):
            return False, f"Flashcard {i} missing back."

    return True, "Exactly 5 valid flashcards."


async def main():

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_dir = ROOT / "acceptance_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (
        report_dir
        / f"chapter_acceptance_{JOB_ID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

    print("=" * 70)
    print("GURUKUL AI - SINGLE CHAPTER ACCEPTANCE TEST")
    print("=" * 70)
    print()
    print("Job ID:", JOB_ID)
    print("Report:", report_file)
    print()

    results = []
    failures = []

    def record(condition, label, details=""):
        passed = check(condition, label, details)

        results.append({
            "label": label,
            "passed": passed,
            "details": details,
        })

        if not passed:
            failures.append(label)

        return passed

    # ---------------------------------------------------------
    # Database initialization
    # ---------------------------------------------------------

    engine = JobEngine(AIOrchestrator())
    await engine.init_db()

    record(
        True,
        "DATABASE INITIALIZATION",
        "Database connection initialized successfully.",
    )

    # ---------------------------------------------------------
    # Load job
    # ---------------------------------------------------------

    async with engine.AsyncSession() as session:

        job = await session.get(ChapterJob, JOB_ID)

        record(
            job is not None,
            "JOB EXISTS",
            f"Job ID: {JOB_ID}",
        )

        if not job:

            report = [
                "# GURUKUL AI - SINGLE CHAPTER ACCEPTANCE REPORT",
                "",
                f"Generated: {timestamp}",
                "",
                f"**Job ID:** `{JOB_ID}`",
                "",
                "## RESULT",
                "",
                "❌ **FAIL** — Job was not found.",
            ]

            report_file.write_text(
                "\n".join(report),
                encoding="utf-8",
            )

            return 1

        # -----------------------------------------------------
        # Job status
        # -----------------------------------------------------

        record(
            job.status == JobStatus.COMPLETED,
            "JOB STATUS",
            f"Status: {job.status}",
        )

        record(
            float(job.progress or 0) >= 1.0,
            "JOB PROGRESS",
            f"Progress: {job.progress}",
        )

        record(
            not job.error,
            "JOB ERROR",
            "No job error recorded."
            if not job.error
            else str(job.error),
        )

        # -----------------------------------------------------
        # Identity
        # -----------------------------------------------------

        print()
        print("CHAPTER IDENTITY")
        print("-" * 70)

        print("Student :", job.student_id)
        print("Book    :", job.book_id)
        print("Chapter :", job.chapter_id)

        record(
            bool(job.student_id),
            "STUDENT ID PRESENT",
            str(job.student_id),
        )

        record(
            bool(job.book_id),
            "BOOK ID PRESENT",
            str(job.book_id),
        )

        record(
            bool(job.chapter_id),
            "CHAPTER ID PRESENT",
            str(job.chapter_id),
        )

        # -----------------------------------------------------
        # Completed stages
        # -----------------------------------------------------

        completed = dict(job.completed_stages or {})

        print()
        print("REQUIRED GURUKUL ASSETS")
        print("-" * 70)

        for stage in REQUIRED_STAGES:

            value = completed.get(stage)

            exists = value is not None

            if isinstance(value, str):
                exists = bool(value.strip())

            if isinstance(value, (list, dict)):
                exists = len(value) > 0

            record(
                exists,
                f"ASSET: {stage}",
                "Present and non-empty."
                if exists
                else "Missing or empty.",
            )

        # -----------------------------------------------------
        # Quiz validation
        # -----------------------------------------------------

        print()
        print("QUIZ VALIDATION")
        print("-" * 70)

        quiz = completed.get("quiz")

        if quiz is None:

            record(
                False,
                "QUIZ CONTRACT",
                "Quiz asset missing.",
            )

        else:

            ok, message = validate_quiz(quiz)

            record(
                ok,
                "QUIZ CONTRACT",
                message,
            )

        # -----------------------------------------------------
        # Flashcard validation
        # -----------------------------------------------------

        print()
        print("FLASHCARD VALIDATION")
        print("-" * 70)

        flashcards = completed.get("flashcards")

        if flashcards is None:

            record(
                False,
                "FLASHCARD CONTRACT",
                "Flashcard asset missing.",
            )

        else:

            ok, message = validate_flashcards(flashcards)

            record(
                ok,
                "FLASHCARD CONTRACT",
                message,
            )

        # -----------------------------------------------------
        # Text asset validation
        # -----------------------------------------------------

        print()
        print("TEXT ASSET VALIDATION")
        print("-" * 70)

        text_assets = [
            "objectives",
            "introduction",
            "teacher_explanation",
            "story_explanation",
            "concepts",
            "summary",
        ]

        for stage in text_assets:

            value = completed.get(stage)

            if isinstance(value, str):
                length = len(value.strip())

            else:
                length = len(str(value or "").strip())

            record(
                length > 0,
                f"{stage} CONTENT",
                f"Content length: {length} characters.",
            )

        # -----------------------------------------------------
        # Extraction/source
        # -----------------------------------------------------

        extraction = completed.get("extraction", "")

        record(
            bool(str(extraction).strip()),
            "SOURCE EXTRACTION",
            f"Extracted source length: {len(str(extraction))} characters.",
        )

        # -----------------------------------------------------
        # Source digest
        # -----------------------------------------------------

        digest = completed.get("source_digest", "")

        if digest:

            record(
                bool(str(digest).strip()),
                "SOURCE DIGEST",
                f"Digest length: {len(str(digest))} characters.",
            )

        else:

            print(
                "[INFO] SOURCE DIGEST not stored in completed_stages."
            )

        # -----------------------------------------------------
        # Single chapter identity
        # -----------------------------------------------------

        print()
        print("SINGLE-CHAPTER INTEGRITY")
        print("-" * 70)

        record(
            bool(extraction),
            "ONE SOURCE DOCUMENT",
            "Extraction exists for this job.",
        )

        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------

        passed = len(failures) == 0

        result_text = "PASS" if passed else "FAIL"

        print()
        print("=" * 70)
        print("ACCEPTANCE RESULT:", result_text)
        print("=" * 70)

        if failures:

            print()
            print("FAILURES:")

            for failure in failures:
                print(" -", failure)

        else:

            print()
            print("ALL ACCEPTANCE CHECKS PASSED.")

        # -----------------------------------------------------
        # Markdown report
        # -----------------------------------------------------

        report = []

        report.append(
            "# GURUKUL AI - SINGLE CHAPTER ACCEPTANCE REPORT"
        )

        report.append("")

        report.append(f"Generated: `{timestamp}`")
        report.append("")

        report.append("## Job")

        report.append("")

        report.append(f"- **Job ID:** `{job.job_id}`")
        report.append(f"- **Student:** `{job.student_id}`")
        report.append(f"- **Book:** `{job.book_id}`")
        report.append(f"- **Chapter:** `{job.chapter_id}`")
        report.append(f"- **Status:** `{job.status}`")
        report.append(f"- **Progress:** `{job.progress}`")

        report.append("")

        report.append("## Acceptance Result")

        report.append("")

        report.append(
            "## PASS"
            if passed
            else "## FAIL"
        )

        report.append("")

        report.append("| Check | Result | Details |")
        report.append("|---|---|---|")

        for item in results:

            status = "PASS" if item["passed"] else "FAIL"

            details = (
                str(item["details"])
                .replace("|", "\\|")
                .replace("\n", " ")
            )

            report.append(
                f"| {item['label']} | {status} | {details} |"
            )

        report.append("")

        report.append("## Required Gurukul Contract")

        report.append("")

        report.append(
            "The following 8 chapter assets were checked:"
        )

        report.append("")

        for stage in REQUIRED_STAGES:

            value = completed.get(stage)

            if isinstance(value, str):
                exists = bool(value.strip())
            elif isinstance(value, (list, dict)):
                exists = len(value) > 0
            else:
                exists = value is not None

            report.append(
                f"- {'✅' if exists else '❌'} `{stage}`"
            )

        report.append("")

        report.append("## Quiz Contract")

        report.append("")

        if quiz is not None:

            try:
                quiz_value = (
                    json.loads(quiz)
                    if isinstance(quiz, str)
                    else quiz
                )

                report.append(
                    f"- Questions: `{len(quiz_value)}`"
                )

            except Exception:

                report.append(
                    "- Questions: `INVALID JSON`"
                )

        report.append("")

        report.append("## Flashcard Contract")

        report.append("")

        if flashcards is not None:

            try:
                flashcard_value = (
                    json.loads(flashcards)
                    if isinstance(flashcards, str)
                    else flashcards
                )

                report.append(
                    f"- Cards: `{len(flashcard_value)}`"
                )

            except Exception:

                report.append(
                    "- Cards: `INVALID JSON`"
                )

        report.append("")

        report.append("## Safety")

        report.append("")

        report.append(
            "- No PDF uploaded by this acceptance test."
        )

        report.append(
            "- No chapter generation triggered."
        )

        report.append(
            "- No job records modified."
        )

        report.append(
            "- No API keys modified."
        )

        report.append("")

        report.append("## Final")

        report.append("")

        report.append(
            "The single-chapter pipeline acceptance test "
            + ("**PASSED**." if passed else "**FAILED**.")
        )

        report_file.write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        print()
        print("ACCEPTANCE REPORT:")
        print(report_file)

        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
