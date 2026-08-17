import os
import uuid
import asyncio
import logging
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config.app_config import settings
from ..models.job import MediaJob, JobStatus
from ..orchestrator.ai_orchestrator import AIOrchestrator
from .animation_service import AnimationService
from .ffmpeg_service import FFmpegService
from .tts_service import TTSService

logger = logging.getLogger(__name__)

class MediaManager:
    """
    Coordinates the asynchronous generation of narrated educational multimedia.
    """

    def __init__(self, orchestrator: AIOrchestrator):
        self.engine = create_async_engine(settings.DATABASE_URL)
        self.AsyncSession = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.orchestrator = orchestrator
        self.animation_service = AnimationService(orchestrator)
        self.ffmpeg_service = FFmpegService()
        self.tts_service = TTSService()

        # Ensure media directories exist
        self.media_root = os.path.join(settings.STORAGE_PATH, "media")
        os.makedirs(os.path.join(self.media_root, "animations"), exist_ok=True)
        os.makedirs(os.path.join(self.media_root, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.media_root, "audio"), exist_ok=True)
        os.makedirs(os.path.join(self.media_root, "subtitles"), exist_ok=True)
        os.makedirs(os.path.join(self.media_root, "thumbnails"), exist_ok=True)
        os.makedirs(os.path.join(self.media_root, "jobs"), exist_ok=True)

    async def init_db(self):
        from ..models.job import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_media_job(self, chapter_id: str, class_name: str, subject: str, type: str = "animation") -> MediaJob:
        """Create and queue a new media generation job."""
        async with self.AsyncSession() as session:
            job = MediaJob(
                chapter_id=chapter_id,
                class_name=class_name,
                subject=subject,
                type=type,
                status=JobStatus.UPLOADED,
                current_stage="QUEUED",
                progress=0.0
            )
            session.add(job)
            await session.commit()
            await session.refresh(job)

            # Start background task
            asyncio.create_task(self.process_media_job(job.job_id))
            return job

    async def process_media_job(self, job_id: str):
        """Asynchronously process a media job through the production pipeline."""
        async with self.AsyncSession() as session:
            job = await session.get(MediaJob, job_id)
            if not job: return

            try:
                # 1. Fetch chapter content (READ-ONLY)
                chapter_package = await self._get_chapter_package(job.class_name, job.subject, job.chapter_id)
                if not chapter_package:
                    raise ValueError(f"Chapter content not found for {job.chapter_id}")

                # 2. Stage: Storyboard/Plan Generation
                job.status = JobStatus.GENERATING
                job.current_stage = "GENERATING_STORYBOARD"
                job.progress = 0.1
                await session.commit()

                plan = await self.animation_service.generate_animation_plan(chapter_package.get('content', {}), job.subject)
                job.metadata_json = {"plan": plan}
                job.progress = 0.2
                await session.commit()

                # Robustly extract scenes and narration
                scenes = []
                if isinstance(plan, list):
                    scenes = plan
                elif isinstance(plan, dict):
                    scenes = plan.get('scenes', [])

                # 3. Stage: Audio Generation (Narration)
                job.current_stage = "SYNTHESIZING_NARRATION"
                full_narration = " ".join([s.get('narration', '') for s in scenes if isinstance(s, dict)])
                audio_filename = f"{job_id}.wav"
                audio_path = os.path.join(self.media_root, "audio", audio_filename)

                tts_success = self.tts_service.synthesize(full_narration, audio_path)
                if not tts_success:
                     logger.warning("TTS failed, proceeding with silent animation")

                job.progress = 0.4
                await session.commit()

                # 4. Stage: Manim Scripting
                job.current_stage = "SCRIPTING_ANIMATION"
                script_filename = f"{job_id}_scene.py"
                script_path = os.path.join(self.media_root, "jobs", script_filename)
                self.animation_service.create_manim_script(plan, script_path)
                job.progress = 0.5
                await session.commit()

                # 5. Stage: Real Manim Rendering
                job.current_stage = "RENDERING_VIDEO"
                rendered_video_path = await self.animation_service.render_animation(script_path, self.media_root)
                job.progress = 0.8
                await session.commit()

                # 6. Stage: Composition (Merging Audio)
                job.current_stage = "FINAL_COMPOSITION"
                final_filename = f"{job_id}_final.mp4"
                final_path = os.path.join(self.media_root, "videos", final_filename)

                if os.path.exists(audio_path) and self.ffmpeg_service.check_availability():
                    self.ffmpeg_service.merge_audio_video(rendered_video_path, audio_path, final_path)
                else:
                    # Just copy the rendered video if no audio or no ffmpeg
                    shutil.copy2(rendered_video_path, final_path)

                job.output_path = f"/media/videos/{final_filename}"
                job.progress = 0.9
                await session.commit()

                # 7. Stage: Thumbnails
                thumbnail_filename = f"{job_id}.jpg"
                thumb_path = os.path.join(self.media_root, "thumbnails", thumbnail_filename)
                if self.ffmpeg_service.check_availability():
                    self.ffmpeg_service.generate_thumbnail(final_path, thumb_path)

                job.thumbnail_path = f"/media/thumbnails/{thumbnail_filename}"

                # 8. Stage: Subtitles
                job.current_stage = "GENERATING_SUBTITLES"
                vtt_filename = f"{job_id}.vtt"
                vtt_path = os.path.join(self.media_root, "subtitles", vtt_filename)
                self._generate_vtt(plan, vtt_path)
                job.subtitles_path = f"/media/subtitles/{vtt_filename}"

                # 9. Complete
                job.status = JobStatus.COMPLETED
                job.current_stage = "COMPLETED"
                job.progress = 1.0
                job.completed_at = datetime.utcnow()
                await session.commit()

            except Exception as e:
                logger.exception(f"Media production job {job_id} failed")
                job.status = JobStatus.FAILED
                job.error = str(e)
                await session.commit()

    async def _get_chapter_package(self, class_name: str, subject: str, chapter_id: str) -> Optional[Dict[str, Any]]:
        import json
        # Handle hierarchical search
        # Note: routes sanitize to lowercase, ensure consistency here
        safe_class = class_name.lower().strip()
        safe_subject = subject.lower().strip()

        path = os.path.join(settings.STORAGE_PATH, "output", safe_class, safe_subject, chapter_id, "package.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None

    def _generate_vtt(self, plan: Any, output_path: str):
        """Generate a WebVTT subtitle file from the animation plan."""
        content = ["WEBVTT", ""]

        scenes = []
        if isinstance(plan, list): scenes = plan
        elif isinstance(plan, dict): scenes = plan.get('scenes', [])

        current_time = 0.0
        for i, scene in enumerate(scenes):
            if not isinstance(scene, dict): continue

            start = current_time
            duration = float(scene.get('duration', 5.0))
            end = start + duration

            # Format: 00:00:01.000
            def fmt(t):
                hours = int(t // 3600)
                mins = int((t % 3600) // 60)
                secs = int(t % 60)
                msecs = int((t * 1000) % 1000)
                return f"{hours:02}:{mins:02}:{secs:02}.{msecs:03}"

            content.append(f"{i+1}")
            content.append(f"{fmt(start)} --\u003e {fmt(end)}")
            content.append(scene.get('narration', ''))
            content.append("")

            current_time = end

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
