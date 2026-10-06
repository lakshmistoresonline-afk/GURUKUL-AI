from .extractor import Class6ScienceQuizExtractor
from .normalizer import Class6ScienceQuizNormalizer
from .validator import Class6ScienceQuizValidator
from .mapper import Class6ScienceQuizMapper

class Class6ScienceQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceQuizExtractor.extract(source_path)
        if not Class6ScienceQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class6ScienceQuizNormalizer.normalize(raw)
        return Class6ScienceQuizMapper.map_to_runtime(normalized)
