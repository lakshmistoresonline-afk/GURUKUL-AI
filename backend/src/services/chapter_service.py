import json
import os
import re
import shutil
import logging
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from ..config.app_config import settings
from ..config.subject_frameworks import get_framework_for_subject
from ..models.job import ChapterJob, JobStatus
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.ai_utils import normalize_structured_response
from ..utils.staging_manager import StagingManager

logger = logging.getLogger(__name__)

class SourceClassificationError(ValueError):
    """Raised when source validation fails (multi-chapter, index, etc.)."""
    def __init__(self, message, category):
        super().__init__(message)
        self.category = category


class ChapterService:
    """
    Generates one complete textbook chapter at a time.

    Gurukul chapter contract:
    objectives
    introduction
    teacher_explanation
    story_explanation
    concepts
    quiz
    flashcards
    summary
    """

    REQUIRED_STAGES = [
        {
            "name": "prerequisites",
            "type": "structured",
            "prompt": "Identify required knowledge/concepts from previous classes or chapters needed to understand this one.",
        },
        {
            "name": "objectives",
            "prompt": "Generate learning objectives.",
        },
        {
            "name": "introduction",
            "prompt": "Generate a student-friendly introduction. For non-English subjects, ensure an engaging 'Kahani Mode' (Story Mode) vibe. If the subject is not Hindi, also provide a 'hindi_summary' field.",
        },
        {
            "name": "teacher_explanation",
            "prompt": (
                "Generate a detailed formal explanation (>300 words). "
                "Include a 'simplified_version' field that explains it in simple terms."
            ),
        },
        {
            "name": "story_explanation",
            "prompt": (
                "Generate an engaging story-based explanation. For subjects like Hindi, use 'Kahani Mode'. "
                "The response should be very descriptive and use analogies."
            ),
        },
        {
            "name": "concepts",
            "type": "structured",
            "prompt": "Identify and define key concepts. For each, provide a 'socratic_hint' and a 'real_world_application'.",
        },
        {
            "name": "quiz",
            "type": "structured",
            "prompt": (
                "Generate exactly 8 assessment questions for this chapter: "
                "4 Multiple Choice Questions (MCQs), "
                "2 True/False questions, and "
                "2 Fill in the Blanks. "
                "Include options for MCQs and correct answers for all. "
                "Assign a 'difficulty' level (Easy, Medium, Hard) to each."
            ),
        },
        {
            "name": "flashcards",
            "type": "structured",
            "prompt": (
                "Generate exactly 5 revision flashcards."
            ),
        },
        {
            "name": "summary",
            "prompt": (
                "Generate a concise revision summary."
            ),
        },
        {
            "name": "mind_map",
            "type": "structured",
            "prompt": (
                "Create a conceptual mind map for this chapter. "
                "Include a central topic and at least 5 main branches with sub-points."
            ),
        },
        {
            "name": "related_chapters",
            "type": "structured",
            "prompt": "Suggest related chapters from the same grade or other subjects (e.g. Math concepts used in EVS).",
        },
    ]

    def __init__(self, orchestrator: AIOrchestrator):
        self.orchestrator = orchestrator
        self.staging_manager = StagingManager()

    def get_stages_for_subject(self, subject: str) -> List[Dict[str, Any]]:
        framework = get_framework_for_subject(subject)
        stages = self.REQUIRED_STAGES.copy()

        # Insert subject specific knowledge stage after concepts
        if framework:
            subject_stage = {
                "name": "subject_knowledge",
                "type": "structured",
                "prompt": (
                    f"Identify and generate the following subject-specific content categories as applicable to this chapter: "
                    f"{', '.join(framework['content_types'])}. \n\n"
                    f"SPECIFIC INSTRUCTIONS:\n{framework['prompt_instructions']}\n\n"
                    "For each category, provide a detailed structured response based ONLY on the source. "
                    "Do NOT generate irrelevant categories if they do not exist in the source."
                )
            }
            # Find concepts index to insert after
            try:
                idx = next(i for i, s in enumerate(stages) if s["name"] == "concepts")
                stages.insert(idx + 1, subject_stage)
            except StopIteration:
                stages.append(subject_stage)

        return stages

    def _validate_single_chapter_source(
        self,
        context: str,
    ) -> None:
        """
        Reject obvious whole-book or multi-chapter documents.
        Identifies and skips Index/TOC documents.
        """

        if not settings.REJECT_MULTI_CHAPTER_DOCUMENTS:
            return

        text = str(context or "").strip()

        if not text:
            raise ValueError(
                "Uploaded chapter contains no extractable text."
            )

        # Pattern for chapter/lesson/unit markers at start of lines
        patterns = [
            r"(?im)^\s*(?:chapter|lesson|unit)\s+([ivxlcdm\d]+)\b",
        ]

        occurrences = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                occurrences.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group(0).strip().lower(),
                    'id': match.group(1).lower()
                })

        occurrences.sort(key=lambda x: x['start'])

        if not occurrences:
            return

        unique_marker_ids = set(o['id'] for o in occurrences)
        unique_marker_texts = set(o['text'] for o in occurrences)

        # Calculate word counts for blocks following each marker to distinguish TOC vs Content
        substantial_blocks = 0
        for i in range(len(occurrences)):
            start = occurrences[i]['end']
            end = occurrences[i+1]['start'] if i+1 < len(occurrences) else len(text)
            block_text = text[start:end]
            # A block is substantial if it has > 400 words
            if len(block_text.split()) > 400:
                substantial_blocks += 1

        threshold = max(
            2,
            int(settings.MULTI_CHAPTER_MARKER_THRESHOLD),
        )

        # Detect INDEX / CONTENTS / TABLE OF CONTENTS
        index_keywords = [r"(?im)^\s*contents\b", r"(?im)^\s*table\s+of\s+contents\b", r"(?im)^\s*index\b"]
        is_index_header = any(re.search(p, text[:4000]) for p in index_keywords)

        # Prelims markers
        prelims_keywords = [r"(?im)^\s*foreword\b", r"(?im)^\s*preface\b", r"(?im)^\s*note\s+to\s+the\s+teacher\b"]
        is_prelims = any(re.search(p, text[:4000]) for p in prelims_keywords)

        # TOC Indicator: many lines ending in numbers AND containing dotted leaders
        # Stricter than before to avoid matching numbered lists/steps
        toc_like_lines = len([l for l in text.split('\n') if '....' in l and re.search(r'\d+$', l.strip())])
        is_toc_structure = toc_like_lines > 5

        # Logic:
        # 1. If multiple unique chapter/unit IDs are found and they cover a range -> likely TOC/Overview
        # 2. If 0 substantial blocks + (index header OR low word count OR TOC structure) -> Index Skip
        # 3. If >= threshold substantial blocks -> Genuine multi-chapter Reject
        # 4. If is_prelims and only 1 substantial block (often Note to Teacher) -> Index Skip

        # 1. Wide marker range check (TOC/Overview signal)
        if len(unique_marker_ids) > 2 and substantial_blocks < threshold:
             raise SourceClassificationError(
                "VALIDATION_ERROR:INDEX_OR_CONTENTS_SKIP - Detected multiple chapter markers in likely index/overview structure.",
                "CONTENTS_INDEX_DOCUMENT"
            )

        # 2. Traditional TOC signals
        if substantial_blocks == 0 or is_toc_structure:
            if is_index_header or is_toc_structure or (len(text.split()) < 1500 and not is_prelims):
                raise SourceClassificationError(
                    "VALIDATION_ERROR:INDEX_OR_CONTENTS_SKIP - Detected INDEX or CONTENTS document.",
                    "CONTENTS_INDEX_DOCUMENT"
                )

        # 3. Prelims with limited content
        if is_prelims and substantial_blocks < threshold:
             raise SourceClassificationError(
                "VALIDATION_ERROR:INDEX_OR_CONTENTS_SKIP - Detected PRELIMS/FRONT-MATTER document.",
                "CONTENTS_INDEX_DOCUMENT"
            )

        # 4. Genuine Multi-chapter
        if substantial_blocks >= threshold:
            markers_found = ", ".join(sorted(list(unique_marker_texts))[:10])
            raise SourceClassificationError(
                f"ONE-CHAPTER-UPLOAD REQUIRED: the uploaded PDF contains substantial content for "
                f"{substantial_blocks} sections. Detected markers: {markers_found}.",
                "MULTI_CHAPTER_DOCUMENT"
            )

    async def run_chapter_generation(
        self,
        session: AsyncSession,
        job: ChapterJob,
    ):
        """
        Generate all chapter assets sequentially.
        """

        completed = dict(
            job.completed_stages or {}
        )

        context = completed.get(
            "extraction",
            "",
        )

        if not context:
            raise ValueError(
                "No source context found for generation."
            )

        self._validate_single_chapter_source(
            context
        )

        stages = self.get_stages_for_subject(job.subject)
        total_stages = len(stages)

        for index, stage in enumerate(stages):
            stage_name = stage["name"]

            # ... rest of logic

            if stage_name in completed:
                continue

            job.current_stage = (
                f"GENERATING_{stage_name.upper()}"
            )

            job.progress = (
                index / total_stages
            )

            await session.commit()

            framework = get_framework_for_subject(job.subject)
            framework_context = f"\nSUBJECT FRAMEWORK ({job.subject}):\n{framework.get('prompt_instructions', '')}\n" if framework else ""

            prompt = (
                "You are generating content for ONE "
                "textbook chapter only.\n\n"
                f"SUBJECT: {job.subject}\n"
                "Use ONLY the supplied chapter-derived "
                "source context. Do not invent facts that "
                "are not supported by it.\n\n"
                f"{framework_context}"
                f"CHAPTER CONTEXT:\n{context}\n\n"
                f"TASK:\n{stage['prompt']}"
            )

            # Stage-level retry loop for structured repair
            max_stage_attempts = 3 if stage.get("type") == "structured" else 1
            stage_error = None
            response = None

            for s_attempt in range(max_stage_attempts):
                try:
                    if stage.get("type") == "structured":
                        schema = self._get_schema_for_stage(stage_name)
                        result = await self.orchestrator.generate_structured(
                            prompt, schema, task_type=stage_name
                        )
                    else:
                        result = await self.orchestrator.generate(
                            prompt, task_type=stage_name
                        )

                    if not result.get("success"):
                        if result.get("is_all_failed"):
                            from ..orchestrator.ai_orchestrator import AllProvidersUnavailableError
                            raise AllProvidersUnavailableError(result.get("error"))
                        raise RuntimeError(f"Provider error: {result.get('error')}")

                    response = result.get("response")

                    if stage.get("type") == "structured":
                        response = normalize_structured_response(response)

                    self._validate_stage_result(stage_name, response)
                    stage_error = None
                    break # Success

                except Exception as exc:
                    stage_error = exc
                    if isinstance(exc, (RuntimeError, ValueError)):
                        logger.warning(
                            "Stage %s attempt %d failed: %s. Retrying...",
                            stage_name, s_attempt + 1, str(exc)
                        )
                        continue
                    else:
                        # Update progress in staging manifest for fatal error
                        self.staging_manager.update_progress(job.chapter_id, success=False, error=str(exc))
                        raise # Fatal/Transient provider error

            if stage_error:
                self.staging_manager.update_progress(job.chapter_id, success=False, error=str(stage_error))
                raise stage_error

            completed[stage_name] = response
            job.completed_stages = completed
            await session.commit()

        # ----------------------------------------------------
        # FINAL VALIDATION
        # ----------------------------------------------------

        self._validate_complete_package(
            completed,
            job.subject
        )

        job.status = JobStatus.VALIDATING
        job.current_stage = (
            "VALIDATING_ALL_CHAPTER_ASSETS"
        )
        job.progress = 0.90

        await session.commit()

        # ----------------------------------------------------
        # FINAL PERSISTENCE
        # ----------------------------------------------------

        await self._persist_final_package(
            job
        )

        job.status = JobStatus.COMPLETED
        job.current_stage = "COMPLETED"
        job.progress = 1.0
        job.error = None

        await session.commit()

    def _get_schema_for_stage(
        self,
        stage_name: str,
    ) -> Dict[str, Any]:

        if stage_name == "quiz":
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["mcq", "true_false", "fill_blanks"]
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["Easy", "Medium", "Hard"]
                        },
                        "question": {
                            "type": "string"
                        },
                        "options": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                        },
                        "correctAnswer": {
                            "type": "string"
                        },
                        "explanation": {
                            "type": "string"
                        },
                    },
                    "required": [
                        "type",
                        "difficulty",
                        "question",
                        "correctAnswer",
                    ],
                },
            }

        if stage_name == "flashcards":
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "front": {
                            "type": "string"
                        },
                        "back": {
                            "type": "string"
                        },
                    },
                    "required": [
                        "front",
                        "back",
                    ],
                },
            }

        if stage_name == "mind_map":
            return {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "branches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "details": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["label"]
                        }
                    }
                },
                "required": ["topic", "branches"]
            }

        if stage_name == "concepts":
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {"type": "string"},
                        "definition": {"type": "string"},
                        "socratic_hint": {"type": "string"}
                    },
                    "required": ["term", "definition", "socratic_hint"]
                }
            }

        if stage_name == "prerequisites" or stage_name == "related_chapters":
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "reason": {"type": "string"},
                        "subject": {"type": "string"}
                    },
                    "required": ["title", "reason"]
                }
            }

        if stage_name == "subject_knowledge":
            return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "content": {"type": "string", "description": "The detailed structured content for this category as defined in the framework."}
                    },
                    "required": ["category", "content"]
                }
            }

        return {
            "type": "object"
        }

    def _validate_stage_result(
        self,
        stage_name: str,
        response: Any,
    ) -> None:

        if response is None:
            raise ValueError(
                f"Stage {stage_name} returned empty content."
            )

        if stage_name in {
            "quiz",
            "flashcards",
            "concepts",
            "prerequisites",
            "related_chapters",
            "subject_knowledge"
        }:
            if not isinstance(response, list):
                raise ValueError(
                    f"Stage {stage_name} must return an array."
                )

            if stage_name == "quiz":
                if len(response) < 5:
                    raise ValueError(
                        "Quiz must contain at least 5 questions."
                    )

                for index, item in enumerate(
                    response,
                    start=1,
                ):
                    if not isinstance(item, dict):
                        raise ValueError(
                            f"Quiz item {index} must be an object."
                        )

                    if not item.get("type"):
                         raise ValueError(f"Quiz item {index} is missing 'type'.")

                    if not item.get("difficulty"):
                         raise ValueError(f"Quiz item {index} is missing 'difficulty'.")

                    if item.get("type") == "mcq":
                        options = item.get("options")
                        if not isinstance(options, list) or len(options) != 4:
                            raise ValueError(
                                f"Quiz item {index} (MCQ) must contain exactly 4 options."
                            )

                    if not item.get("question"):
                        raise ValueError(
                            f"Quiz item {index} has no question."
                        )

                    if not item.get("correctAnswer"):
                        raise ValueError(
                            f"Quiz item {index} has no correct answer."
                        )

            if stage_name == "flashcards":
                if len(response) != 5:
                    raise ValueError(
                        "Flashcards must contain exactly 5 cards."
                    )

                for index, item in enumerate(
                    response,
                    start=1,
                ):
                    if not isinstance(item, dict):
                        raise ValueError(
                            f"Flashcard {index} must be an object."
                        )

                    if not item.get("front"):
                        raise ValueError(
                            f"Flashcard {index} has no front."
                        )

                    if not item.get("back"):
                        raise ValueError(
                            f"Flashcard {index} has no back."
                        )

            if stage_name == "concepts":
                for index, item in enumerate(response, start=1):
                    if not isinstance(item, dict) or not item.get("term") or not item.get("definition") or not item.get("socratic_hint"):
                        raise ValueError(f"Concept {index} is missing required fields.")

    def _validate_complete_package(
        self,
        completed: Dict[str, Any],
        subject: str
    ) -> None:

        stages = self.get_stages_for_subject(subject)
        required = [
            stage["name"]
            for stage in stages
        ]

        missing = [
            name
            for name in required
            if name not in completed
            or completed[name] in (
                None,
                "",
                [],
                {},
            )
        ]

        if missing:
            raise ValueError(
                "Incomplete chapter package. "
                f"Missing: {', '.join(missing)}"
            )

        self._validate_stage_result(
            "quiz",
            completed["quiz"],
        )

        self._validate_stage_result(
            "flashcards",
            completed["flashcards"],
        )

    async def _persist_final_package(
        self,
        job: ChapterJob,
    ):
        """
        Persist the completed chapter package in a human-readable hierarchy in the STAGING AREA.
        storage/generation_staging/<run_id>/{class_name}/{subject}/{chapter_id}/package.json
        """

        # Get staging directory from manager
        package_dir = self.staging_manager.get_chapter_staging_dir(
            job.class_name,
            job.subject,
            job.chapter_id
        )

        # Include metadata in the package
        package_data = {
            "metadata": {
                "run_id": self.staging_manager.run_id,
                "job_id": job.job_id,
                "class_name": job.class_name,
                "subject": job.subject,
                "chapter_id": job.chapter_id,
                "completed_at": datetime.utcnow().isoformat() if not job.completed_at else job.completed_at.isoformat(),
                "provider": job.provider,
                "model": job.model,
                "diksha_link": f"https://diksha.gov.in/play/collection/{job.chapter_id}" if job.chapter_id.startswith("do_") else None,
                "source_file_hash": job.source_file_hash
            },
            "content": job.completed_stages
        }

        package_path = os.path.join(package_dir, "package.json")

        with open(
            package_path,
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                package_data,
                handle,
                indent=2,
                ensure_ascii=False,
            )

        # Record in staging manifest
        self.staging_manager.record_generated_file({
            "job_id": job.job_id,
            "class": job.class_name,
            "subject": job.subject,
            "chapter_id": job.chapter_id,
            "generated_path": package_path,
            "hash": self.staging_manager.calculate_hash(package_path),
            "provider": job.provider,
            "model": job.model
        })

        # Update progress
        self.staging_manager.update_progress(job.chapter_id, success=True)

        # Also keep a copy by Job ID in staging for quick lookup
        job_lookup_dir = os.path.join(self.staging_manager.run_dir, "jobs", job.job_id)
        os.makedirs(job_lookup_dir, exist_ok=True)
        shutil.copy2(package_path, os.path.join(job_lookup_dir, "package.json"))
