from typing import Dict, Any, Type, Optional
from .base_adapter import BaseContentAdapter
from .english.english_master_adapter import EnglishMasterAdapter
from .english.class5_english_adapter import Class5EnglishAdapter
from .hindi.hindi_master_adapter import HindiMasterAdapter
from .science.science_master_adapter import ScienceMasterAdapter
from .maths.maths_master_adapter import MathsMasterAdapter
from .generic_adapter import GenericContentAdapter

class AdapterResolver:
    """
    Universal Adapter Resolution Engine.
    Resolves adapters based on curriculum, grade, subject, and schema fingerprint.
    Falls back gracefully to GenericContentAdapter for novel unknown schemas without crashing.
    """

    _fallback_adapter = GenericContentAdapter()

    @classmethod
    def resolve(
        cls,
        curriculum: str,
        grade: str,
        subject: str,
        source_data: Optional[Dict[str, Any]]
    ) -> BaseContentAdapter:
        if not source_data or not isinstance(source_data, dict):
            return cls._fallback_adapter

        sub_key = subject.lower().strip()

        if sub_key == "english":
            if "keyTerminology" in source_data or "detailedBreakdown" in source_data or "studyQuestions" in source_data or "overview" in source_data:
                return Class5EnglishAdapter()
            if ("chapters_master_data" in source_data or "summaryStatistics" in source_data or "English Master.json" in source_data) and grade == "5":
                return EnglishMasterAdapter()
            return cls._fallback_adapter

        if sub_key == "hindi":
            if "chapters_master_data" in source_data or "shabdart" in source_data:
                return HindiMasterAdapter()
            return cls._fallback_adapter

        if sub_key == "science":
            if "scientificPrinciples" in source_data or "glossary" in source_data:
                return ScienceMasterAdapter()
            return cls._fallback_adapter

        if sub_key in ["maths", "mathematics"]:
            if "quizzes_mcq" in source_data or "case_study_questions" in source_data:
                return MathsMasterAdapter()
            return cls._fallback_adapter

        return cls._fallback_adapter
