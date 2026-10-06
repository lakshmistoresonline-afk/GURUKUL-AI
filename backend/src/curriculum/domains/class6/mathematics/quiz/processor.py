from .extractor import Class6MathematicsQuizExtractor
from .normalizer import Class6MathematicsQuizNormalizer
from .validator import Class6MathematicsQuizValidator
from .mapper import Class6MathematicsQuizMapper

class Class6MathematicsQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsQuizExtractor.extract(source_path)
        if not Class6MathematicsQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class6MathematicsQuizNormalizer.normalize(raw)
        return Class6MathematicsQuizMapper.map_to_runtime(normalized)
