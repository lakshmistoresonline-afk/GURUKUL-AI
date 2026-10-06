from typing import Dict, Type
from ..core.curriculum_identity import CurriculumIdentity
from ..core.subject_registry import SubjectRegistry
from .base.base_processor import BaseProcessor

# Import class/subject processors
from .class5.english_processor import Class5EnglishProcessor
from .class5.hindi_processor import Class5HindiProcessor
from .class5.mathematics_processor import Class5MathematicsProcessor
from .class5.science_processor import Class5ScienceProcessor

from .class6.english_processor import Class6EnglishProcessor
from .class6.hindi_processor import Class6HindiProcessor
from .class6.mathematics_processor import Class6MathematicsProcessor
from .class6.science_processor import Class6ScienceProcessor
from .class6.social_science_processor import Class6SocialScienceProcessor

from .class7.english_processor import Class7EnglishProcessor
from .class7.hindi_processor import Class7HindiProcessor
from .class7.mathematics_i_processor import Class7MathematicsIProcessor
from .class7.mathematics_ii_processor import Class7MathematicsIIProcessor
from .class7.science_processor import Class7ScienceProcessor
from .class7.social_science_i_processor import Class7SocialScienceIProcessor
from .class7.social_science_ii_processor import Class7SocialScienceIIProcessor

class ProcessorRegistry:
    """
    Central Processor Registry for Gurukul AI.
    Selects explicit subject-specific and class-specific processors
    using grade + canonical subject + book/part.
    """

    _REGISTRY: Dict[str, Type[BaseProcessor]] = {
        "5:english:main": Class5EnglishProcessor,
        "5:hindi:main": Class5HindiProcessor,
        "5:mathematics:main": Class5MathematicsProcessor,
        "5:science:main": Class5ScienceProcessor,

        "6:english:main": Class6EnglishProcessor,
        "6:hindi:main": Class6HindiProcessor,
        "6:mathematics:main": Class6MathematicsProcessor,
        "6:science:main": Class6ScienceProcessor,
        "6:social_science:main": Class6SocialScienceProcessor,

        "7:english:main": Class7EnglishProcessor,
        "7:hindi:main": Class7HindiProcessor,
        "7:mathematics:maths_i": Class7MathematicsIProcessor,
        "7:mathematics:maths_ii": Class7MathematicsIIProcessor,
        "7:science:main": Class7ScienceProcessor,
        "7:social_science:social_i": Class7SocialScienceIProcessor,
        "7:social_science:social_ii": Class7SocialScienceIIProcessor,
    }

    @classmethod
    def resolve(cls, identity: CurriculumIdentity) -> BaseProcessor:
        canonical_subj = SubjectRegistry.resolve_canonical_subject(identity.subject)
        book_key = identity.book.lower()
        if book_key == "none":
            book_key = "main"

        key = f"{identity.grade}:{canonical_subj}:{book_key}"
        if key not in cls._REGISTRY:
            # Try fallback generic match for grade + subject
            fallback_key = f"{identity.grade}:{canonical_subj}:main"
            if fallback_key in cls._REGISTRY:
                return cls._REGISTRY[fallback_key]
            raise ValueError(f"No processor registered for identity: {identity.to_cache_key()} (Key: {key})")

        return cls._REGISTRY[key]()

    @classmethod
    def registered_keys(cls) -> list:
        return list(cls._REGISTRY.keys())
