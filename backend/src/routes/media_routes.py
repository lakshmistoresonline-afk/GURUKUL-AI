import os
import json
import uuid
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends, Body
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from ..services.media_manager import MediaManager
from ..services.external_media_service import ExternalMediaService
from ..services.mastery_service import MasteryService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..models.job import ChapterJob, JobStatus
from ..utils.security import get_authorized_class, validate_chapter_access, get_admin_user
from ..utils.auth import get_current_user, AuthUser, get_current_admin

router = APIRouter()
orchestrator = AIOrchestrator()
media_manager = MediaManager(orchestrator)
mastery_service = MasteryService()
external_media_service = ExternalMediaService(mastery_service)

@router.get("/hub")
async def get_multimedia_hub_data(
    user: AuthUser = Depends(get_current_user)
):
    """
    Returns consolidated hierarchy and availability summary for the Multimedia Hub.
    Optimized for single-trip dashboard loading.
    """
    from .chapter_routes import list_hierarchical_content

    # 1. Get Hierarchy (scoped to user class)
    hierarchy = await list_hierarchical_content(user)

    # 2. Get Summary
    summary = await external_media_service.get_class_multimedia_summary(user.class_name)

    return {
        "class_id": user.class_id,
        "class_name": user.class_name,
        "hierarchy": hierarchy.get(user.class_name, {}),
        "summary": summary
    }

@router.get("/external")
async def list_verified_external_resources(
    subject: Optional[str] = Query(None),
    chapter_id: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100),
    user: AuthUser = Depends(get_current_user)
):
    """List verified external multimedia resources scoped to the user's verified class."""
    authorized_class = user.class_name

    if chapter_id:
        validate_chapter_access(chapter_id, authorized_class)

    return await external_media_service.get_verified_resources(
        class_name=authorized_class,
        subject=subject,
        chapter_id=chapter_id,
        resource_type=resource_type,
        search=search,
        limit=min(limit, 100)
    )

@router.get("/external/stats")
async def get_external_media_stats(admin_uid: str = Depends(get_admin_user)):
    """Get statistics for external multimedia resources (Admin only)."""
    return await external_media_service.get_stats()

@router.get("/summary/{class_name}")
async def get_class_multimedia_summary(
    class_name: str,
    user: AuthUser = Depends(get_current_user)
):
    """Get a summary of multimedia availability for the student's authorized class."""
    authorized_class = await get_authorized_class(user, class_name)
    return await external_media_service.get_class_multimedia_summary(authorized_class)

@router.get("/admin/external/pending")
async def list_pending_resources(
    class_name: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    admin_uid: str = Depends(get_admin_user)
):
    """List resources pending verification (Admin only)."""
    return await external_media_service.get_admin_pending_resources(
        class_name=class_name,
        subject=subject,
        provider=provider
    )

@router.get("/admin/external/all")
async def list_all_external_resources(
    class_name: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(200),
    admin_uid: str = Depends(get_admin_user)
):
    """List all external resources with filters (Admin only)."""
    return await external_media_service.get_all_resources(
        class_name=class_name,
        subject=subject,
        status=status,
        limit=limit
    )

@router.post("/admin/external/{resource_id}/verify")
async def verify_resource(resource_id: str, admin_uid: str = Depends(get_admin_user)):
    """Verify an external resource (Admin only)."""
    await external_media_service.verify_resource(resource_id, admin_uid)
    return {"status": "SUCCESS"}

@router.post("/admin/external/{resource_id}/reject")
async def reject_resource(resource_id: str, admin_uid: str = Depends(get_admin_user)):
    """Reject an external resource (Admin only)."""
    await external_media_service.reject_resource(resource_id)
    return {"status": "SUCCESS"}

@router.post("/admin/external/reload")
async def reload_catalogs(admin_uid: str = Depends(get_admin_user)):
    """Reload JSON catalogs into the database (Admin only)."""
    await external_media_service.reload_catalogs()
    return {"status": "SUCCESS"}

class MediaJobRequest(BaseModel):
    chapter_id: str
    class_name: str
    subject: str
    type: str = "animation"

@router.post("/generate")
async def create_media_job(request: MediaJobRequest, admin_uid: str = Depends(get_admin_user)):
    """Start a new multimedia generation job (Admin only)."""
    try:
        job = await media_manager.create_media_job(
            request.chapter_id,
            request.class_name,
            request.subject,
            request.type
        )
        return job.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to initiate media job.")

@router.get("/status/{job_id}")
async def get_media_job_status(
    job_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Check the status of a media job."""
    async with media_manager.AsyncSession() as session:
        from ..models.job import MediaJob
        job = await session.get(MediaJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return job.to_dict()

@router.get("/discover")
async def discover_media(
    subject: Optional[str] = Query(None),
    limit: int = Query(10),
    user: AuthUser = Depends(get_current_user)
):
    """List recently completed media jobs for discovery within the user's verified class."""
    authorized_class = user.class_name
    async with media_manager.AsyncSession() as session:
        from ..models.job import MediaJob
        from sqlalchemy import select, and_

        filters = [MediaJob.status == JobStatus.COMPLETED, MediaJob.class_name == authorized_class]
        if subject: filters.append(MediaJob.subject == subject)

        stmt = select(MediaJob).where(and_(*filters)).order_by(MediaJob.completed_at.desc()).limit(min(limit, 20))
        result = await session.execute(stmt)
        jobs = result.scalars().all()
        return [j.to_dict() for j in jobs]

@router.get("/chapter/{chapter_id}")
async def list_chapter_media(
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """List all media (bundled, AI-generated, and YouTube) associated with a chapter."""
    authorized_class = user.class_name

    # 1. Check Master Package for bundled multimedia
    from ..utils.path_resolver import PathResolver
    from ..utils.package_adapter import PackageAdapter
    master_path = PathResolver.get_chapter_path(authorized_class, chapter_id)
    master_media = []
    youtube_media = []

    if master_path:
        pkg_path = os.path.join(master_path, "package.json")
        if os.path.exists(pkg_path):
            try:
                with open(pkg_path, 'r', encoding='utf-8') as f:
                    pkg = PackageAdapter.adapt(json.load(f))

                    # AI Enrichment / Multimedia Learning
                    ai_enrichment = pkg.get("original_data", {}).get("aiEnrichment", {})

                    # Storyboard (Multi-scene)
                    storyboard = ai_enrichment.get("multimedia_learning") or \
                                 ai_enrichment.get("multimedia")

                    if storyboard and isinstance(storyboard, dict) and "scenes" in storyboard:
                        master_media.append({
                            "job_id": f"master_sb_{chapter_id}",
                            "chapter_id": chapter_id,
                            "type": "storyboard",
                            "status": "COMPLETED",
                            "output_url": storyboard.get("url", ""),
                            "metadata": storyboard
                        })

                    # Individual bundled media
                    m_list = pkg.get("content", {}).get("multimedia")
                    if m_list and isinstance(m_list, list):
                        for item in m_list:
                            master_media.append({
                                "job_id": f"master_{item.get('id', uuid.uuid4())}",
                                "chapter_id": chapter_id,
                                "type": item.get("type", "visual"),
                                "status": "COMPLETED",
                                "output_url": item.get("url", ""),
                                "metadata": item
                            })

                    # YouTube Resources
                    yt_data = ai_enrichment.get("youtube_resources", {}) or \
                              ai_enrichment.get("youtube", {})

                    if yt_data:
                        # Direct Videos
                        direct_found = False
                        for v in yt_data.get("directVerifiedVideos", []):
                            direct_found = True
                            youtube_media.append({
                                "job_id": f"yt_{v.get('id', uuid.uuid4())}",
                                "chapter_id": chapter_id,
                                "type": "video",
                                "status": "COMPLETED",
                                "output_url": v.get("url"),
                                "metadata": {**v, "is_direct": True}
                            })

                        # Discovery Links
                        disc_found = False
                        for d in yt_data.get("discoveryLinks", []):
                            disc_found = True
                            youtube_media.append({
                                "job_id": f"yt_disc_{d.get('id', uuid.uuid4())}",
                                "chapter_id": chapter_id,
                                "type": "video_discovery",
                                "status": "COMPLETED",
                                "output_url": d.get("url"),
                                "metadata": {**d, "is_direct": False}
                            })

                        # Fallback: Auto-generate discovery link using terms
                        if not direct_found and not disc_found:
                            terms = yt_data.get("chapterSpecificDiscoveryTerms", []) or \
                                    yt_data.get("suggestedTopics", [])
                            if terms:
                                term = terms[0]
                                youtube_media.append({
                                    "job_id": f"yt_auto_{uuid.uuid4()}",
                                    "chapter_id": chapter_id,
                                    "type": "video_discovery",
                                    "status": "COMPLETED",
                                    "output_url": f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}",
                                    "metadata": {
                                        "title": f"Explore: {term}",
                                        "channel": "YouTube Discovery",
                                        "url": f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}",
                                        "resource_type": "smart_discovery",
                                        "is_direct": False
                                    }
                                })
            except Exception as e:
                logger.error(f"Error parsing master media for {chapter_id}: {e}")

    # 2. Check AI Generated Media (DB-backed)
    ai_media = []
    async with media_manager.AsyncSession() as session:
        from ..models.job import MediaJob
        from sqlalchemy import select
        stmt = select(MediaJob).where(MediaJob.chapter_id == chapter_id)
        result = await session.execute(stmt)
        jobs = result.scalars().all()
        ai_media = [j.to_dict() for j in jobs]

    # 3. Check Global YouTube Mapping (Legacy fallback)
    if not youtube_media:
        mapping_path = os.path.join(settings.STORAGE_PATH, "video_resources_mapped.json")
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    all_v = json.load(f)

                chapter_v = all_v.get(chapter_id)
                if chapter_v:
                    for v in chapter_v.get("verified_direct_resources", []):
                        youtube_media.append({
                            "job_id": f"yt_{v.get('id', uuid.uuid4())}",
                            "chapter_id": chapter_id,
                            "type": "video",
                            "status": "COMPLETED",
                            "output_url": v.get("url"),
                            "metadata": {**v, "is_direct": True}
                        })
                    for d in chapter_v.get("live_discovery_links", []):
                        youtube_media.append({
                            "job_id": f"yt_disc_{d.get('id', uuid.uuid4())}",
                            "chapter_id": chapter_id,
                            "type": "video_discovery",
                            "status": "COMPLETED",
                            "output_url": d.get("url"),
                            "metadata": {**d, "is_direct": False}
                        })
            except: pass

    return master_media + ai_media + youtube_media
