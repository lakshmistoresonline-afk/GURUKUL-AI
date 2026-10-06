from .extractor import Class6EnglishQuizExtractor
from .normalizer import Class6EnglishQuizNormalizer
from .validator import Class6EnglishQuizValidator
from .mapper import Class6EnglishQuizMapper

class Class6EnglishQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishQuizExtractor.extract(source_path)
        if not Class6EnglishQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class6EnglishQuizNormalizer.normalize(raw)
        return Class6EnglishQuizMapper.map_to_runtime(normalized)
