import os
import json
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config.app_config import settings
from ..models.resource import ExternalMultimediaResource
from .mastery_service import MasteryService

logger = logging.getLogger(__name__)

class ExternalMediaService:
    def __init__(self, mastery_service: MasteryService):
        self.engine = create_async_engine(settings.DATABASE_URL)
        self.AsyncSession = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.mastery_service = mastery_service

    async def init_db(self):
        from ..models.job import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Initial load from catalogs
        await self.reload_catalogs()

    async def reload_catalogs(self):
        """Loads and validates both JSON catalogs into the database."""
        await self.load_catalog_v3()
        await self.load_api_import_catalog()

    async def load_catalog_v3(self):
        # Load catalogs class-wise from GURUKUL_AI_CONTENT
        total_loaded = 0
        for cid in ["05", "06", "07"]:
            class_folder = f"class_{cid}"
            path = os.path.join(settings.MASTER_CONTENT_ROOT, class_folder, settings.MULTIMEDIA_CATALOG_FILENAME)

            if not os.path.exists(path):
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                resources_to_add = []
                # Support 'resources' (as a flat list in distributed files)
                # or the original nested structure
                resources_list = data.get("resources") or []

                # If it's the old nested structure (unlikely in distributed files but for safety)
                chapters = data.get("chapters") or data.get("chapter_resources") or []
                for chapter in chapters:
                    resources_list.extend(chapter.get("resources") or chapter.get("external_resources") or [])

                for res in resources_list:
                    # Validate and Normalize
                    url = res.get("url")
                    chapter_id = res.get("chapter_id") or res.get("chapterId") # distributed file uses chapterId

                    if url is None:
                        url = f"local://{chapter_id}/{res.get('id')}"

                    url = url.strip().rstrip("/")
                    if not url: continue

                    # Exclude YouTube
                    if "youtube.com" in url.lower() or "youtu.be" in url.lower():
                        continue

                    subject = res.get("subject") or "General"
                    provider = res.get("provider")

                    resource_data = {
                        "chapter_id": chapter_id,
                        "class_name": class_folder,
                        "subject": subject,
                        "provider": provider,
                        "title": f"{provider} — {subject.capitalize()}",
                        "url": url,
                        "resource_types": res.get("resource_types", []),
                        "search_url": res.get("search_url"),
                        "search_terms": res.get("search_terms", []),
                        "chapter_deep_link_verified": res.get("chapter_deep_link_verified", False),
                        "enabled": res.get("chapter_deep_link_verified", False),
                        "verification_status": "VERIFIED" if res.get("chapter_deep_link_verified", False) else "PENDING",
                        "source": "CATALOG_V3"
                    }
                    resources_to_add.append(resource_data)

                await self._persist_resources(resources_to_add)
                total_loaded += len(resources_to_add)

            except Exception as e:
                logger.error(f"Error loading Multimedia Catalog for {class_folder}: {e}")

        if total_loaded > 0:
            logger.info(f"Loaded {total_loaded} resources from class-wise Catalog V3.")

    async def load_api_import_catalog(self):
        path = settings.MULTIMEDIA_EXTERNAL_API_IMPORT_PATH
        if not os.path.exists(path):
            logger.warning(f"External Multimedia API Import Catalog not found at {path}")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            resources_to_add = []
            # API Import catalog is often a list of resource objects
            # but sometimes wrapped in a "resources" key.
            res_list = data if isinstance(data, list) else data.get("resources", [])

            for res in res_list:
                url = res.get("url")
                if url is None: url = f"api://{res.get('chapter_id')}/{res.get('id') or uuid.uuid4()}"

                url_norm = url.strip().rstrip("/")
                if not url_norm: continue
                if "youtube.com" in url_norm.lower() or "youtu.be" in url_norm.lower():
                    continue

                resource_data = {
                    "chapter_id": res.get("chapter_id"),
                    "class_name": res.get("class_name"),
                    "subject": res.get("subject"),
                    "provider": res.get("provider"),
                    "title": res.get("title"),
                    "url": url_norm,
                    "resource_types": res.get("resource_types", []),
                    "search_url": res.get("search_url"),
                    "search_terms": res.get("search_terms", []),
                    "chapter_deep_link_verified": res.get("chapter_deep_link_verified", False),
                    "enabled": res.get("enabled", False),
                    "source": "API_IMPORT"
                }
                resources_to_add.append(resource_data)

            await self._persist_resources(resources_to_add)
            logger.info(f"Loaded {len(resources_to_add)} resources from API Import Catalog.")

        except Exception as e:
            logger.error(f"Error loading API Import Catalog: {e}")

    async def _persist_resources(self, resources: List[Dict[str, Any]]):
        async with self.AsyncSession() as session:
            for r_data in resources:
                # Deduplication: chapter_id + provider + url
                stmt = select(ExternalMultimediaResource).where(
                    and_(
                        ExternalMultimediaResource.chapter_id == r_data['chapter_id'],
                        ExternalMultimediaResource.provider == r_data['provider'],
                        ExternalMultimediaResource.url == r_data['url']
                    )
                )
                res = await session.execute(stmt)
                existing = res.scalars().first()

                if existing:
                    # Update fields but preserve verification status if already verified
                    for k, v in r_data.items():
                        if k == "chapter_deep_link_verified" and existing.verification_status == "VERIFIED":
                            continue
                        if k == "enabled" and existing.verification_status == "VERIFIED":
                            continue
                        setattr(existing, k, v)
                    existing.last_checked = datetime.utcnow()
                else:
                    resource = ExternalMultimediaResource(**r_data)
                    session.add(resource)

            await session.commit()

    async def get_verified_resources(self,
                                   class_name: Optional[str] = None,
                                   subject: Optional[str] = None,
                                   chapter_id: Optional[str] = None,
                                   resource_type: Optional[str] = None,
                                   search: Optional[str] = None,
                                   limit: int = 100) -> List[Dict[str, Any]]:
        async with self.AsyncSession() as session:
            filters = [
                ExternalMultimediaResource.enabled == True,
                ExternalMultimediaResource.chapter_deep_link_verified == True,
                ExternalMultimediaResource.youtube == False
            ]
            if class_name: filters.append(ExternalMultimediaResource.class_name == class_name)
            if subject: filters.append(ExternalMultimediaResource.subject == subject)
            if chapter_id: filters.append(ExternalMultimediaResource.chapter_id == chapter_id)
            if search:
                filters.append(or_(
                    ExternalMultimediaResource.title.ilike(f"%{search}%"),
                    ExternalMultimediaResource.provider.ilike(f"%{search}%")
                ))

            stmt = select(ExternalMultimediaResource).where(and_(*filters)).limit(limit)
            res = await session.execute(stmt)
            resources = [r.to_dict() for r in res.scalars().all()]

            if resource_type:
                resources = [r for r in resources if resource_type in r.get("resource_types", [])]

            return resources

    async def get_admin_pending_resources(self,
                                        class_name: Optional[str] = None,
                                        subject: Optional[str] = None,
                                        provider: Optional[str] = None) -> List[Dict[str, Any]]:
        async with self.AsyncSession() as session:
            filters = [ExternalMultimediaResource.verification_status == "PENDING"]
            if class_name: filters.append(ExternalMultimediaResource.class_name == class_name)
            if subject: filters.append(ExternalMultimediaResource.subject == subject)
            if provider: filters.append(ExternalMultimediaResource.provider == provider)

            stmt = select(ExternalMultimediaResource).where(and_(*filters)).order_by(ExternalMultimediaResource.created_at.desc())
            res = await session.execute(stmt)
            return [r.to_dict() for r in res.scalars().all()]

    async def get_all_resources(self,
                               class_name: Optional[str] = None,
                               subject: Optional[str] = None,
                               status: Optional[str] = None,
                               limit: int = 200) -> List[Dict[str, Any]]:
        async with self.AsyncSession() as session:
            filters = []
            if class_name: filters.append(ExternalMultimediaResource.class_name == class_name)
            if subject: filters.append(ExternalMultimediaResource.subject == subject)
            if status: filters.append(ExternalMultimediaResource.verification_status == status)

            stmt = select(ExternalMultimediaResource)
            if filters:
                stmt = stmt.where(and_(*filters))

            stmt = stmt.order_by(ExternalMultimediaResource.created_at.desc()).limit(limit)
            res = await session.execute(stmt)
            return [r.to_dict() for r in res.scalars().all()]

    async def verify_resource(self, resource_id: str, admin_id: str):
        async with self.AsyncSession() as session:
            stmt = update(ExternalMultimediaResource).where(
                ExternalMultimediaResource.id == resource_id
            ).values(
                verification_status="VERIFIED",
                chapter_deep_link_verified=True,
                enabled=True,
                admin_verified_by=admin_id,
                admin_verified_at=datetime.utcnow()
            )
            await session.execute(stmt)
            await session.commit()

    async def reject_resource(self, resource_id: str):
        async with self.AsyncSession() as session:
            stmt = update(ExternalMultimediaResource).where(
                ExternalMultimediaResource.id == resource_id
            ).values(
                verification_status="REJECTED",
                enabled=False
            )
            await session.execute(stmt)
            await session.commit()

    async def toggle_resource_enabled(self, resource_id: str, enabled: bool):
        async with self.AsyncSession() as session:
            stmt = update(ExternalMultimediaResource).where(
                ExternalMultimediaResource.id == resource_id
            ).values(enabled=enabled)
            await session.execute(stmt)
            await session.commit()

    async def get_stats(self) -> Dict[str, Any]:
        async with self.AsyncSession() as session:
            total = await session.scalar(select(func.count(ExternalMultimediaResource.id)))
            verified = await session.scalar(select(func.count(ExternalMultimediaResource.id)).where(ExternalMultimediaResource.verification_status == "VERIFIED"))
            pending = await session.scalar(select(func.count(ExternalMultimediaResource.id)).where(ExternalMultimediaResource.verification_status == "PENDING"))
            rejected = await session.scalar(select(func.count(ExternalMultimediaResource.id)).where(ExternalMultimediaResource.verification_status == "REJECTED"))
            enabled = await session.scalar(select(func.count(ExternalMultimediaResource.id)).where(ExternalMultimediaResource.enabled == True))

            return {
                "total_resources": total,
                "verified": verified,
                "pending": pending,
                "rejected": rejected,
                "enabled": enabled
            }

    async def get_class_multimedia_summary(self, class_name: str) -> Dict[str, Any]:
        """Returns a mapping of chapter_id to multimedia counts including YouTube resources."""
        async with self.AsyncSession() as session:
            # 1. External Resources counts
            stmt = select(
                ExternalMultimediaResource.chapter_id,
                func.count(ExternalMultimediaResource.id)
            ).where(
                and_(
                    ExternalMultimediaResource.class_name == class_name,
                    ExternalMultimediaResource.enabled == True,
                    ExternalMultimediaResource.chapter_deep_link_verified == True
                )
            ).group_by(ExternalMultimediaResource.chapter_id)

            res = await session.execute(stmt)
            external_counts = {cid: count for cid, count in res.all()}

            # 2. AI Generated Media check
            from ..models.job import MediaJob, JobStatus
            stmt_ai = select(
                MediaJob.chapter_id,
                func.count(MediaJob.job_id)
            ).where(
                and_(
                    MediaJob.class_name == class_name,
                    MediaJob.status == JobStatus.COMPLETED
                )
            ).group_by(MediaJob.chapter_id)

            res_ai = await session.execute(stmt_ai)
            ai_counts = {cid: count for cid, count in res_ai.all()}

            # 3. YouTube Mapping counts
            youtube_stats = {}
            mapping_path = os.path.join(settings.STORAGE_PATH, "video_resources_mapped.json")
            if os.path.exists(mapping_path):
                try:
                    with open(mapping_path, 'r', encoding='utf-8') as f:
                        all_v = json.load(f)

                    for cid, data in all_v.items():
                        direct = len(data.get("verified_direct_resources", []))
                        disc = len(data.get("live_discovery_links", []))
                        if direct > 0 or disc > 0:
                            youtube_stats[cid] = {
                                "direct": direct,
                                "discovery": disc
                            }
                except:
                    pass

            # 4. Master Content Multimedia Counts
            if settings.USE_MASTER_CONTENT:
                from ..utils.path_resolver import PathResolver
                class_id = PathResolver.extract_class_id(class_name)
                master_index = PathResolver._get_master_index(class_id)
                if master_index:
                    for chapter in master_index.get("chapters", []):
                        cid = chapter.get("chapterId")
                        c_path = PathResolver.get_chapter_path(class_name, cid)
                        if c_path:
                            # Check multimedia_learning.json
                            m_file = os.path.join(c_path, "multimedia_learning.json")
                            if os.path.exists(m_file):
                                try:
                                    with open(m_file, 'r') as f:
                                        m_data = json.load(f)
                                        if m_data:
                                            ai_counts[cid] = ai_counts.get(cid, 0) + len(m_data)
                                except: pass

                            # Check youtube_resources.json
                            y_file = os.path.join(c_path, "youtube_resources.json")
                            if os.path.exists(y_file):
                                try:
                                    with open(y_file, 'r') as f:
                                        y_data = json.load(f)
                                        direct = len(y_data.get("directVerifiedVideos", []))
                                        disc = len(y_data.get("discoveryLinks", []))
                                        if direct > 0 or disc > 0:
                                            if cid not in youtube_stats:
                                                youtube_stats[cid] = {"direct": direct, "discovery": disc}
                                            else:
                                                youtube_stats[cid]["direct"] += direct
                                                youtube_stats[cid]["discovery"] += disc
                                except: pass

            return {
                "external": external_counts,
                "ai_generated": ai_counts,
                "youtube": youtube_stats
            }
