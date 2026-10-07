from typing import Dict, Type, List, Any
from ..core.curriculum_identity import CurriculumIdentity
from ..core.subject_registry import SubjectRegistry
from .base.base_processor import BaseProcessor

# Import explicit class/subject/book processors
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

class ProcessorNotFoundError(ValueError):
    """Raised when no explicit processor is registered for the requested complete identity key."""
    pass

class ProcessorIdentityMismatchError(ValueError):
    """Raised when resolved processor identity does not match requested identity."""
    pass

class ProcessorRegistry:
    """
    Gen-2 Authoritative Processor Registry with Complete Identity Keys.
    Key format: grade:canonical_subject:book:part
    Zero inference from part or subject strings. Zero generic fallbacks.
    """

    _REGISTRY: Dict[str, Type[BaseProcessor]] = {
        "5:english:english:main": Class5EnglishProcessor,
        "5:hindi:hindi:main": Class5HindiProcessor,
        "5:mathematics:mathematics:main": Class5MathematicsProcessor,
        "5:science:science:main": Class5ScienceProcessor,

        "6:english:english:main": Class6EnglishProcessor,
        "6:hindi:hindi:main": Class6HindiProcessor,
        "6:mathematics:mathematics:main": Class6MathematicsProcessor,
        "6:science:science:main": Class6ScienceProcessor,
        "6:social_science:social_science:main": Class6SocialScienceProcessor,

        "7:english:english:main": Class7EnglishProcessor,
        "7:hindi:hindi:main": Class7HindiProcessor,
        "7:mathematics:maths_i:part1": Class7MathematicsIProcessor,
        "7:mathematics:maths_ii:part2": Class7MathematicsIIProcessor,
        "7:science:science:main": Class7ScienceProcessor,
        "7:social_science:social_i:part1": Class7SocialScienceIProcessor,
        "7:social_science:social_ii:part2": Class7SocialScienceIIProcessor,
    }

    @classmethod
    def resolve(cls, identity: CurriculumIdentity) -> BaseProcessor:
        canonical_subj = SubjectRegistry.resolve_canonical_subject(identity.subject)
        grade = str(identity.grade).lower()
        book = identity.book.lower()
        part = identity.part.lower()

        key = f"{grade}:{canonical_subj}:{book}:{part}"
        if key not in cls._REGISTRY:
            raise ProcessorNotFoundError(
                f"Strict resolution failure: No explicit processor registered for complete identity key '{key}' "
                f"(Requested identity: {identity.to_cache_key()}). Inference and generic fallbacks are strictly prohibited."
            )

        processor_cls = cls._REGISTRY[key]
        processor = processor_cls()

        # Validate declared identity matches requested identity
        if hasattr(processor, "grade") and str(processor.grade).lower() != grade:
            raise ProcessorIdentityMismatchError(f"Processor grade mismatch: {processor.grade} != {grade}")

        return processor

    @classmethod
    def registered_keys(cls) -> List[str]:
        return list(cls._REGISTRY.keys())

    @classmethod
    def introspect(cls) -> List[Dict[str, Any]]:
        """
        Registry introspection reporting key, grade, subject, book, part, processor class, and version.
        """
        details = []
        for key, proc_cls in cls._REGISTRY.items():
            parts = key.split(":")
            grade = parts[0]
            subject = parts[1]
            book = parts[2]
            part = parts[3] if len(parts) > 3 else "main"

            version = "V14-STRICT"
            try:
                inst = proc_cls()
                if hasattr(inst, "version"):
                    version = inst.version
            except:
                pass

            details.append({
                "key": key,
                "grade": grade,
                "subject": subject,
                "book": book,
                "part": part,
                "processor_class": proc_cls.__name__,
                "processor_version": version
            })
        return details
