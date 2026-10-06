from .extractor import Class5MathematicsQuizExtractor
from .normalizer import Class5MathematicsQuizNormalizer
from .validator import Class5MathematicsQuizValidator
from .mapper import Class5MathematicsQuizMapper

class Class5MathematicsQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsQuizExtractor.extract(source_path)
        if not Class5MathematicsQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class5MathematicsQuizNormalizer.normalize(raw)
        return Class5MathematicsQuizMapper.map_to_runtime(normalized)
