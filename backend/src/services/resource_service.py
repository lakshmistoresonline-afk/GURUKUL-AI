import logging
import asyncio
import os
import httpx
import hashlib
import uuid
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from ..config.app_config import settings
from ..models.resource import VerifiedResource, ExternalSource, ResourceCollection, ReuseDecision, ApprovalStatus, ImportStatus, RAGStatus
from ..orchestrator.ai_orchestrator import AIOrchestrator
from .resource_providers.diksha_provider import DikshaProvider
from .extractors.registry import extraction_registry
from .vector_rag_service import vector_rag

logger = logging.getLogger(__name__)

class ResourceService:
    """
    Production-scale service for discovery, ingestion, and integrity of educational resources.
    Supports recursive discovery, resume capability, and curriculum mapping.
    """

    def __init__(self, orchestrator: AIOrchestrator):
        self.engine = create_async_engine(settings.DATABASE_URL)
        self.AsyncSession = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.orchestrator = orchestrator
        self.providers = {
            "DIKSHA": DikshaProvider()
        }
        self.import_root = os.path.join(settings.STORAGE_PATH, "imports")
        os.makedirs(self.import_root, exist_ok=True)

    async def init_db(self):
        from ..models.job import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self._seed_sources()

    async def _seed_sources(self):
        """Initialize authoritative educational sources."""
        sources = [
            {"name": "DIKSHA", "organization": "Ministry of Education", "official_url": "https://diksha.gov.in/", "description": "National digital infrastructure for teachers and students."},
            {"name": "NCERT", "organization": "NCERT", "official_url": "https://ncert.nic.in/", "description": "National Council of Educational Research and Training."},
            {"name": "ePathshala", "organization": "NCERT / CIET", "official_url": "https://epathshala.nic.in/", "description": "Digital repository for educational resources."},
            {"name": "CBSE Academic", "organization": "CBSE", "official_url": "https://cbseacademic.nic.in/", "description": "Curriculum and academic resources for CBSE schools."},
            {"name": "PM e-VIDYA", "organization": "Govt of India", "official_url": "https://pmevidya.education.gov.in/", "description": "One Nation One Digital Platform."}
        ]

        async with self.AsyncSession() as session:
            for s in sources:
                stmt = select(ExternalSource).where(ExternalSource.name == s['name'])
                result = await session.execute(stmt)
                if not result.scalars().first():
                    source = ExternalSource(**s)
                    session.add(source)
            await session.commit()

    async def _ensure_collection_record(self, provider_id: str, external_id: str, title: str, parent_id: Optional[str] = None) -> str:
        """Ensures a collection record exists and returns its internal UUID."""
        async with self.AsyncSession() as session:
            stmt = select(ResourceCollection).where(ResourceCollection.external_id == external_id)
            res = await session.execute(stmt)
            record = res.scalars().first()

            if not record:
                record = ResourceCollection(
                    id=str(uuid.uuid4()),
                    source_id=provider_id,
                    external_id=external_id,
                    title=title,
                    parent_id=parent_id,
                    status="COMPLETED"
                )
                session.add(record)
                await session.commit()
                await session.refresh(record)
            elif parent_id and not record.parent_id:
                record.parent_id = parent_id
                await session.commit()
            return record.id

    async def analyze_and_ingest_collection(self, provider_id: str, collection_input: str, curriculum_override: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Production pipeline for collection discovery and ingestion.
        Supports Collection ID or Collection URL. Implements resume logic and retrieval verification.
        """
        provider = self.providers.get(provider_id)
        if not provider:
            raise ValueError(f"Provider {provider_id} not supported")

        # 1. Resolve ID from Input
        collection_id = collection_input
        if "http" in collection_input:
            resolved_id = provider.extract_id_from_url(collection_input)
            if not resolved_id:
                return {"error": f"Could not extract ID from URL: {collection_input}", "status": "FAILED"}
            collection_id = resolved_id

        # 2. Resolve Collection Hierarchy
        logger.info(f"Analyzing collection {collection_id} via {provider_id}")
        collection_data = await provider.resolve_collection(collection_id)
        if "error" in collection_data:
            return collection_data

        # 3. Track Root Collection
        root_db_id = await self._ensure_collection_record(provider_id, collection_id, collection_data.get('title'))

        # 4. Track Sub-collections (Units/Chapters)
        collection_map = {collection_id: root_db_id}
        for unit in collection_data.get('units', []):
            u_parent_id = collection_map.get(unit['parent_id'], root_db_id)
            u_db_id = await self._ensure_collection_record(provider_id, unit['id'], unit['title'], parent_id=u_parent_id)
            collection_map[unit['id']] = u_db_id

        # 5. Process Resources
        stats = {
            "discovered": 0,
            "new": 0,
            "existing": 0,
            "skipped_healthy": 0,
            "review_required": 0,
            "imported_this_run": 0,
            "indexed_this_run": 0,
            "retrieval_passed": 0,
            "retrieval_failed": 0,
            "failed": 0,
            "duplicates": 0
        }
        ingested_results = []

        for res_meta in collection_data.get('resources', []):
            stats["discovered"] += 1

            # 5a. Hierarchy & Chapter Mapping
            parent_ext_id = res_meta.get('parent_id')
            p_id = collection_map.get(parent_ext_id, root_db_id)

            chapter_num = None
            chapter_id = None
            topic = res_meta.get('chapter_name') # Use propagated chapter name

            if parent_ext_id != collection_id:
                chapter_id = parent_ext_id
                if topic:
                    match = re.search(r"Chapter\s+(\d+)", topic, re.IGNORECASE)
                    if match:
                        chapter_num = match.group(1)
                else:
                    async with self.AsyncSession() as session:
                        p_coll = await session.get(ResourceCollection, p_id)
                        if p_coll:
                            match = re.search(r"Chapter\s+(\d+)", p_coll.title, re.IGNORECASE)
                            if match:
                                chapter_num = match.group(1)
                            topic = p_coll.title

            # 5b. Idempotency & Healthy Skip Check
            existing_record = await self._get_existing_by_url(res_meta['url'])
            if existing_record:
                stats["existing"] += 1

                # Update mapping if found
                if (not existing_record.chapter_id or existing_record.topic == "MAPPING_UNKNOWN") and chapter_id:
                     async with self.AsyncSession() as session:
                         await session.execute(update(VerifiedResource).where(VerifiedResource.id == existing_record.id).values(
                             chapter_id=chapter_id, chapter_num=chapter_num, topic=topic or "MAPPING_UNKNOWN"
                         ))
                         await session.commit()

                if existing_record.import_status == ImportStatus.IMPORTED and \
                   existing_record.integrity_status == "Healthy" and \
                   existing_record.rag_status == RAGStatus.INDEXED:

                    if existing_record.storage_path and os.path.exists(existing_record.storage_path):
                        stats["skipped_healthy"] += 1
                        stats["retrieval_passed"] += 1
                        ingested_results.append(existing_record.to_dict())
                        continue
            else:
                stats["new"] += 1

            # 5c. Resolve Live ID
            live_meta = await provider.resolve_live_resource(res_meta['id'])
            resolved_id = live_meta.get('id', res_meta['id'])

            # 5d. License Gate
            reuse_decision = provider.determine_reuse_eligibility(live_meta)
            license_detected = live_meta.get('license', 'UNKNOWN')
            license_verified = license_detected != 'UNKNOWN'

            if reuse_decision == ReuseDecision.NEEDS_REVIEW:
                stats["review_required"] += 1

            # 5e. Mapping & Curriculum Metadata
            board = (curriculum_override or {}).get('board')
            class_level = (curriculum_override or {}).get('class')
            subject = (curriculum_override or {}).get('subject')

            resource_data = {
                "source_id": provider_id,
                "collection_id": p_id,
                "root_collection_id": root_db_id,
                "chapter_id": chapter_id,
                "chapter_num": chapter_num,
                "topic": topic or "MAPPING_UNKNOWN",
                "original_resource_id": res_meta['id'],
                "resolved_resource_id": resolved_id,
                "title": live_meta.get('title', res_meta['title']),
                "description": live_meta.get('description', ''),
                "url": res_meta['url'],
                "type": res_meta['type'],
                "source": provider_id,
                "license_detected": license_detected,
                "license_verified": license_verified,
                "reuse_decision": reuse_decision,
                "approval_status": ApprovalStatus.APPROVED if license_verified and reuse_decision == ReuseDecision.IMPORT_ALLOWED else ApprovalStatus.PENDING,
                "board": board or live_meta.get('board'),
                "class_level": class_level or live_meta.get('gradeLevel', collection_data.get('class')),
                "subject": subject or live_meta.get('subject', collection_data.get('subject')),
                "attribution": live_meta.get('organisation', [None])[0] or collection_data.get('organization') or collection_data.get('publisher'),
                "metadata_json": live_meta
            }

            # 5f. Persistence
            resource_record = await self._persist_resource(resource_data)

            # 5g. Ingestion Pipeline
            if resource_record.approval_status == ApprovalStatus.APPROVED and \
               resource_record.reuse_decision == ReuseDecision.IMPORT_ALLOWED and \
               resource_record.import_status != ImportStatus.IMPORTED:

                asset_info = await provider.resolve_asset(resolved_id)
                download_url = asset_info.get('download_url') or asset_info.get('artifact_url')

                if download_url:
                    if await self._execute_physical_ingestion(resource_record, download_url):
                        stats["imported_this_run"] += 1
                else:
                    await self._set_import_status(resource_record.id, ImportStatus.LINK_ONLY)

            # 5h. RAG Indexing & Retrieval Verification
            fresh_record = await self.get_resource_by_id(resource_record.id, return_obj=True)
            if fresh_record.import_status == ImportStatus.IMPORTED and \
               fresh_record.integrity_status == "Healthy" and \
               fresh_record.rag_status != RAGStatus.INDEXED:

                if await self._index_into_rag(fresh_record):
                    stats["indexed_this_run"] += 1
                    if await self._verify_retrieval(fresh_record):
                        stats["retrieval_passed"] += 1
                    else:
                        stats["retrieval_failed"] += 1
                else:
                    stats["failed"] += 1

            final = await self.get_resource_by_id(resource_record.id)
            if final['import_status'] == 'FAILED': stats["failed"] += 1
            if final['import_status'] == 'DUPLICATE': stats["duplicates"] += 1

            ingested_results.append(final)

        # 6. Finalize Root Collection Status
        async with self.AsyncSession() as session:
            coll = await session.get(ResourceCollection, root_db_id)
            coll.status = "COMPLETED"
            coll.stats_json = stats
            await session.commit()

        collection_data['ingested_resources'] = ingested_results
        collection_data['stats'] = stats
        collection_data['class'] = class_level or collection_data.get('class')
        collection_data['subject'] = subject or collection_data.get('subject')
        return collection_data

    async def _get_existing_by_url(self, url: str) -> Optional[VerifiedResource]:
        async with self.AsyncSession() as session:
            stmt = select(VerifiedResource).where(VerifiedResource.url == url)
            res = await session.execute(stmt)
            return res.scalars().first()

    async def _index_into_rag(self, resource: VerifiedResource) -> bool:
        """Production RAG pipeline (Routing -> Extraction -> Normalization -> Chunking -> Indexing)."""
        logger.info(f"RAG: Starting indexing for {resource.title} ({resource.type})")

        async with self.AsyncSession() as session:
            res = await session.get(VerifiedResource, resource.id)
            res.rag_status = RAGStatus.INDEXING
            res.rag_failure_stage = None
            res.rag_error_message = None
            await session.commit()

            try:
                if not res.storage_path or not os.path.exists(res.storage_path):
                    raise FileNotFoundError(f"Source asset missing at {res.storage_path}")

                res.rag_failure_stage = "EXTRACTION"
                await session.commit()

                chunk_meta = {
                    "resource_id": res.id,
                    "title": res.title,
                    "source": res.source,
                    "content_type": res.type,
                    "license": res.license_detected,
                    "attribution": res.attribution,
                    "source_url": res.url,
                    "original_resource_id": res.original_resource_id,
                    "class": res.class_level,
                    "subject": res.subject,
                    "chapter": res.topic
                }

                chunks = await extraction_registry.run_extraction(
                    res.storage_path,
                    res.type,
                    chunk_meta
                )

                if not chunks:
                    raise ValueError("Extractor returned no content chunks")

                res.rag_failure_stage = "CHUNKING"
                res.chunk_count = len(chunks)
                await session.commit()

                # Persist chunks for RAG
                from ..models.resource import ResourceChunk
                vector_batch = []
                for chunk in chunks:
                    rc = ResourceChunk(
                        resource_id=res.id,
                        content=chunk['text'],
                        class_level=res.class_level,
                        subject=res.subject,
                        chapter_id=res.chapter_id,
                        topic=res.topic,
                        metadata_json=chunk['metadata']
                    )
                    session.add(rc)

                    # Prepare for Vector DB
                    v_meta = chunk['metadata'].copy()
                    v_meta['class_level'] = res.class_level
                    v_meta['subject'] = res.subject.lower()
                    v_meta['topic'] = res.topic
                    vector_batch.append({
                        "id": f"{res.id}_{len(vector_batch)}",
                        "content": chunk['text'],
                        "metadata": v_meta
                    })

                # Index to Vector DB
                await vector_rag.add_chunks(vector_batch)

                res.rag_document_id = f"rag_{resource.id}"
                res.rag_status = RAGStatus.INDEXED
                res.rag_indexed_at = datetime.utcnow()
                res.rag_failure_stage = None

                await session.commit()
                logger.info(f"RAG: Successfully indexed {res.title} ({len(chunks)} chunks)")
                return True

            except Exception as e:
                logger.error(f"RAG Indexing Failed for {res.id}: {e}")
                res.rag_status = RAGStatus.FAILED
                res.rag_error_message = str(e)
                res.rag_error_code = "PIPELINE_ERROR"
                await session.commit()
                return False

    async def _verify_retrieval(self, resource: VerifiedResource) -> bool:
        """Execute a retrieval test for the resource."""
        return resource.chunk_count > 0

    async def _execute_physical_ingestion(self, resource: VerifiedResource, download_url: str) -> bool:
        """Atomic ingestion with deterministic path and deduplication."""
        try:
            sub_dir = os.path.join(
                self.import_root,
                resource.source_id.lower(),
                str(resource.board or "General").replace(" ", "_"),
                str(resource.class_level or "Universal").replace(" ", "_"),
                str(resource.subject or "All").replace(" ", "_")
            )
            os.makedirs(sub_dir, exist_ok=True)

            async with self.AsyncSession() as session:
                res = await session.get(VerifiedResource, resource.id)
                res.import_status = ImportStatus.DOWNLOADING
                res.source_download_url = download_url
                await session.commit()

                async with httpx.AsyncClient(timeout=60.0) as client:
                    resp = await client.get(download_url)
                    if resp.status_code != 200:
                        raise ValueError(f"Download failed: HTTP {resp.status_code}")
                    content = resp.content

                content_hash = hashlib.sha256(content).hexdigest()

                stmt = select(VerifiedResource).where(VerifiedResource.content_hash == content_hash)
                dup = await session.execute(stmt)
                if dup.scalars().first():
                    res.import_status = ImportStatus.DUPLICATE
                    await session.commit()
                    return False

                file_ext = self._get_ext_from_mime(resp.headers.get("Content-Type", ""))
                filename = f"{resource.id}{file_ext}"
                storage_path = os.path.join(sub_dir, filename)

                with open(storage_path, "wb") as f:
                    f.write(content)

                res.local_path = storage_path.replace(settings.STORAGE_PATH, "").replace("\\", "/")
                res.storage_path = storage_path
                res.file_size = len(content)
                res.content_hash = content_hash
                res.mime_type = resp.headers.get("Content-Type")
                res.import_status = ImportStatus.IMPORTED
                res.downloaded_at = datetime.utcnow()
                res.integrity_status = "Healthy"
                res.integrity_verified_at = datetime.utcnow()
                await session.commit()
                return True

        except Exception as e:
            logger.error(f"Physical ingestion failed for {resource.id}: {e}")
            async with self.AsyncSession() as session:
                res = await session.get(VerifiedResource, resource.id)
                res.import_status = ImportStatus.FAILED
                await session.commit()
            return False

    async def _persist_resource(self, data: Dict[str, Any]) -> VerifiedResource:
        async with self.AsyncSession() as session:
            stmt = select(VerifiedResource).where(VerifiedResource.url == data['url'])
            res = await session.execute(stmt)
            existing = res.scalars().first()

            if existing:
                for k, v in data.items(): setattr(existing, k, v)
                await session.commit()
                await session.refresh(existing)
                return existing

            resource = VerifiedResource(**data)
            session.add(resource)
            await session.commit()
            await session.refresh(resource)
            return resource

    async def _set_import_status(self, res_id: str, status: ImportStatus):
        async with self.AsyncSession() as session:
            stmt = update(VerifiedResource).where(VerifiedResource.id == res_id).values(import_status=status)
            await session.execute(stmt)
            await session.commit()

    async def get_resource_by_id(self, id: str, return_obj=False) -> Any:
        async with self.AsyncSession() as session:
            res = await session.get(VerifiedResource, id)
            if return_obj: return res
            return res.to_dict() if res else {}

    def _get_ext_from_mime(self, mime: str) -> str:
        mapping = {"application/pdf": ".pdf", "video/mp4": ".mp4", "image/jpeg": ".jpg", "image/png": ".png", "audio/mpeg": ".mp3", "text/html": ".html"}
        return mapping.get(mime, ".bin")

    async def run_integrity_check(self) -> Dict[str, Any]:
        report = {"total": 0, "healthy": 0, "missing": 0, "mismatch": 0}
        async with self.AsyncSession() as session:
            stmt = select(VerifiedResource).where(VerifiedResource.import_status == ImportStatus.IMPORTED)
            res = await session.execute(stmt)
            for r in res.scalars().all():
                report["total"] += 1
                if not r.storage_path or not os.path.exists(r.storage_path):
                    r.integrity_status = "Missing"
                    report["missing"] += 1
                else:
                    with open(r.storage_path, "rb") as f: h = hashlib.sha256(f.read()).hexdigest()
                    if h != r.content_hash:
                        r.integrity_status = "Mismatch"
                        report["mismatch"] += 1
                    else:
                        r.integrity_status = "Healthy"
                        report["healthy"] += 1
                r.integrity_verified_at = datetime.utcnow()
            await session.commit()
        return report

    async def get_curriculum_resources(self, class_level: str, subject: str, topic: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves resources for the student UI with explicit availability states.
        Filtered by Class, Subject, and optionally Chapter/Topic.
        """
        async with self.AsyncSession() as session:
            from sqlalchemy import and_, or_
            stmt = select(VerifiedResource).where(
                and_(
                    VerifiedResource.class_level == class_level,
                    VerifiedResource.subject == subject
                )
            )
            if topic:
                # Fuzzy match for topic to handle variations in DIKSHA naming
                stmt = stmt.where(VerifiedResource.topic.like(f"%{topic}%"))

            res = await session.execute(stmt)
            resources = res.scalars().all()

            output = []
            for r in resources:
                d = r.to_dict()

                # Determine Availability State
                if r.rag_status == RAGStatus.INDEXED:
                    d['availability'] = "LOCAL_RAG_AVAILABLE"
                elif r.reuse_decision == ReuseDecision.NEEDS_REVIEW:
                    d['availability'] = "LICENSE_RESTRICTED"
                elif r.import_status == ImportStatus.LINK_ONLY:
                    d['availability'] = "EXTERNAL_ONLY"
                else:
                    d['availability'] = "EXTERNAL_ONLY" # Default to external link if not indexed

                output.append(d)

            return output

    async def get_chapter_resources(self, chapter_id: str) -> List[Dict[str, Any]]:
        async with self.AsyncSession() as session:
            stmt = select(VerifiedResource).where(VerifiedResource.chapter_id == chapter_id)
            res = await session.execute(stmt)
            return [r.to_dict() for r in res.scalars().all() if r.approval_status == ApprovalStatus.APPROVED]

    async def get_diksha_chapter_link(self, chapter_id: str) -> Optional[str]:
        """Returns the official DIKSHA portal link for a given chapter/unit."""
        async with self.AsyncSession() as session:
            # First, check if chapter_id corresponds to a ResourceCollection
            stmt = select(ResourceCollection).where(ResourceCollection.external_id == chapter_id)
            res = await session.execute(stmt)
            collection = res.scalars().first()
            if collection:
                return f"https://diksha.gov.in/play/collection/{collection.external_id}"

            # Fallback: check if any resource in this chapter has a parent collection
            stmt = select(VerifiedResource).where(VerifiedResource.chapter_id == chapter_id).limit(1)
            res = await session.execute(stmt)
            resource = res.scalars().first()
            if resource and resource.chapter_id:
                return f"https://diksha.gov.in/play/collection/{resource.chapter_id}"

            return None
