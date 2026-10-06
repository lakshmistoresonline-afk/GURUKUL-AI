from .extractor import Class7MathematicsiiQuizExtractor
from .normalizer import Class7MathematicsiiQuizNormalizer
from .validator import Class7MathematicsiiQuizValidator
from .mapper import Class7MathematicsiiQuizMapper

class Class7MathematicsiiQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiQuizExtractor.extract(source_path)
        if not Class7MathematicsiiQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7MathematicsiiQuizNormalizer.normalize(raw)
        return Class7MathematicsiiQuizMapper.map_to_runtime(normalized)
