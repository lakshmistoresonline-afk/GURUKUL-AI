from .extractor import Class6MathematicsNotesExtractor
from .normalizer import Class6MathematicsNotesNormalizer
from .validator import Class6MathematicsNotesValidator
from .mapper import Class6MathematicsNotesMapper

class Class6MathematicsNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsNotesExtractor.extract(source_path)
        if not Class6MathematicsNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class6MathematicsNotesNormalizer.normalize(raw)
        return Class6MathematicsNotesMapper.map_to_runtime(normalized)
