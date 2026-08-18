import os
import uuid
import json
import logging
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends

from ..config.app_config import settings
from ..jobs.job_engine import JobEngine
from ..models.job import ChapterJob
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.pdf_utils import calculate_file_hash
from ..utils.security import get_authorized_class, validate_chapter_access, get_admin_user
from ..utils.auth import get_current_user, AuthUser, get_current_admin
from ..utils.path_resolver import PathResolver
from ..utils.package_adapter import PackageAdapter


logger = logging.getLogger(__name__)

router = APIRouter()
orchestrator = AIOrchestrator()
engine = JobEngine(orchestrator)

os.makedirs(settings.STORAGE_PATH, exist_ok=True)


@router.post("/process")
async def start_chapter_processing(
    book_id: str = Form(...),
    chapter_id: str = Form(...),
    subject: Optional[str] = Form(None),
    file: UploadFile = File(...),
    user: AuthUser = Depends(get_current_user)
):
    """
    Accept exactly ONE PDF for ONE chapter.
    Only authorized for specific roles if restricted, otherwise any student for now.
    Derives student identity from verified token.
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A chapter PDF is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF chapter files are supported.",
        )

    file_id = str(uuid.uuid4())
    file_path = os.path.join(
        settings.STORAGE_PATH,
        f"{file_id}.pdf",
    )

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty.",
            )

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        file_hash = calculate_file_hash(file_path)

        await engine.init_db()

        try:
            job = await engine.create_job(
                user.uid,
                book_id,
                chapter_id,
                file_path,
                file_hash,
                class_name=user.class_name,
                subject=subject,
            )

        except RuntimeError as exc:
            if str(exc).startswith("ACTIVE_CHAPTER_EXISTS:"):
                parts = str(exc).split(":", 2)

                active_job_id = (
                    parts[1] if len(parts) > 1 else "unknown"
                )
                active_chapter_id = (
                    parts[2] if len(parts) > 2 else "unknown"
                )

                try:
                    os.remove(file_path)
                except OSError:
                    pass

                raise HTTPException(
                    status_code=409,
                    detail={
                        "code": "CHAPTER_ALREADY_PROCESSING",
                        "message": (
                            "You already have a chapter being processed. "
                            "Wait until it is completed before uploading "
                            "the next chapter."
                        ),
                        "active_job_id": active_job_id,
                        "active_chapter_id": active_chapter_id,
                    },
                ) from exc

            raise

        return job.to_dict()

    except HTTPException:
        raise

    except Exception as exc:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass

        raise HTTPException(
            status_code=500,
            detail="Unable to create chapter job due to an internal error.",
        ) from exc


@router.get("/status/{job_id}")
async def get_job_status(
    job_id: str,
    user: AuthUser = Depends(get_current_user)
):
    async with engine.AsyncSession() as session:
        job = await session.get(
            ChapterJob,
            job_id,
        )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found",
            )

        return job.to_dict()


@router.get("/package/{class_name}/{subject}/{chapter_id}")
async def get_chapter_package(
    class_name: str,
    subject: str,
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """
    Retrieve a completed chapter package using hierarchical path.
    Enforces class isolation via verified identity.
    """
    authorized_class = await get_authorized_class(user, class_name)
    validate_chapter_access(chapter_id, authorized_class, subject=subject)

    # Priority 1: Master Content Package
    if settings.USE_MASTER_CONTENT:
        master_path = PathResolver.get_chapter_path(authorized_class, chapter_id, subject=subject)
        if master_path:
            package_path = os.path.join(master_path, "package.json")
            if os.path.exists(package_path):
                try:
                    with open(package_path, "r", encoding="utf-8") as f:
                        return PackageAdapter.adapt(json.load(f))
                except Exception as e:
                    logger.error(f"Error reading master package: {e}")

    # Priority 2: storage/output (Generated content)
    def sanitize(s: str) -> str:
        return "".join([c for c in s if c.isalnum() or c in (" ", "-", "_")]).strip().replace(" ", "_").lower()

    safe_class = sanitize(authorized_class)
    safe_subject = sanitize(subject)

    variations = [chapter_id, chapter_id.lower(), chapter_id.upper(), sanitize(chapter_id)]

    package_path = None
    for var in list(dict.fromkeys(variations)):
        candidate = os.path.join(settings.STORAGE_PATH, "output", safe_class, safe_subject, var, "package.json")
        if os.path.exists(candidate):
            package_path = candidate
            break

    if not package_path:
        subject_dir = os.path.join(settings.STORAGE_PATH, "output", safe_class, safe_subject)
        if os.path.exists(subject_dir):
            for folder in os.listdir(subject_dir):
                if folder.lower() == chapter_id.lower():
                    package_path = os.path.join(subject_dir, folder, "package.json")
                    break

    if not package_path:
        raise HTTPException(
            status_code=404,
            detail=f"Package not found for chapter {chapter_id} in your curriculum.",
        )

    try:
        with open(package_path, "r", encoding="utf-8") as f:
            return PackageAdapter.adapt(json.load(f))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error reading package data.",
        )


@router.get("/package/job/{job_id}")
async def get_chapter_package_by_job_id(
    job_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """
    Retrieve a completed chapter package using Job ID.
    """
    async with engine.AsyncSession() as session:
        job = await session.get(ChapterJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

    package_path = os.path.join(
        settings.STORAGE_PATH,
        "output",
        job_id,
        "package.json"
    )

    if not os.path.exists(package_path):
        raise HTTPException(
            status_code=404,
            detail="Package not found for this Job ID.",
        )

    try:
        with open(package_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error reading package.",
        )


@router.get("/explorer/hierarchy")
async def list_hierarchical_content(user: AuthUser = Depends(get_current_user)):
    """
    Returns the Subject -> Chapter hierarchy for the AUTHORIZED class of the student.
    Handles Part I / Part II grouping if present in package metadata.
    """
    authorized_class = user.class_name # e.g. class_5
    logger.info(f"Hierarchy requested for class: {authorized_class}")
    logger.info(f"USE_MASTER_CONTENT: {settings.USE_MASTER_CONTENT}")

    # Priority 1: Master Content Package
    if settings.USE_MASTER_CONTENT:
        hierarchy_data = PathResolver.get_class_hierarchy(authorized_class)
        logger.info(f"Master hierarchy found: {bool(hierarchy_data)}")
        if hierarchy_data:
            return {authorized_class: hierarchy_data}

    # Priority 2: storage/output (Dynamic/Generated content fallback)
    logger.info("Falling back to storage/output hierarchy")
    hierarchy = {}
    base_dir = os.path.join(settings.STORAGE_PATH, "output")

    if not os.path.exists(base_dir):
        return hierarchy

    # Support case-insensitive class directory lookup
    class_path = None
    if os.path.exists(os.path.join(base_dir, authorized_class)):
        class_path = os.path.join(base_dir, authorized_class)
    else:
        # Try finding it manually if casing is weird
        for item in os.listdir(base_dir):
            if item.lower() == authorized_class:
                class_path = os.path.join(base_dir, item)
                break

    if not class_path or not os.path.isdir(class_path):
        return {user.class_name: {}}

    # Return key matching the requested class name for frontend consistency
    res_key = user.class_name
    hierarchy[res_key] = {}

    for subject in os.listdir(class_path):
        subject_path = os.path.join(class_path, subject)
        if not os.path.isdir(subject_path):
            continue

        # We'll return either a list of chapters OR a dict of parts -> chapters
        chapters_data = []

        for chapter_id in os.listdir(subject_path):
            chapter_path = os.path.join(subject_path, chapter_id)
            if not os.path.isdir(chapter_path):
                continue

            pkg_file = os.path.join(chapter_path, "package.json")
            if os.path.exists(pkg_file):
                try:
                    with open(pkg_file, "r", encoding="utf-8") as f:
                        pkg = PackageAdapter.adapt(json.load(f))

                        # Extract metadata
                        metadata = pkg.get("metadata", {})
                        original = pkg.get("original_data", {}).get("curriculum", {})

                        name = (original.get("displayName") or
                                metadata.get("chapter_name") or
                                pkg.get("content", {}).get("topic") or
                                chapter_id)

                        part = original.get("part") or metadata.get("part")
                        if part == "Single Book": part = None

                        num = original.get("chapterNumber") or metadata.get("chapterNumber")

                        chapters_data.append({
                            "id": chapter_id,
                            "name": name,
                            "part": part,
                            "number": num
                        })
                except:
                    chapters_data.append({
                        "id": chapter_id,
                        "name": chapter_id
                    })

        # Sort by part then number
        chapters_data.sort(key=lambda x: (str(x.get("part") or ""), int(x.get("number") or 0)))
        hierarchy[authorized_class][subject] = chapters_data

    return hierarchy


