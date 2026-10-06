from .extractor import Class5MathematicsNotesExtractor
from .normalizer import Class5MathematicsNotesNormalizer
from .validator import Class5MathematicsNotesValidator
from .mapper import Class5MathematicsNotesMapper

class Class5MathematicsNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsNotesExtractor.extract(source_path)
        if not Class5MathematicsNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class5MathematicsNotesNormalizer.normalize(raw)
        return Class5MathematicsNotesMapper.map_to_runtime(normalized)
