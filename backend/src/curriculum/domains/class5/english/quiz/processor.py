from .extractor import Class5EnglishQuizExtractor
from .normalizer import Class5EnglishQuizNormalizer
from .validator import Class5EnglishQuizValidator
from .mapper import Class5EnglishQuizMapper

class Class5EnglishQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishQuizExtractor.extract(source_path)
        if not Class5EnglishQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class5EnglishQuizNormalizer.normalize(raw)
        return Class5EnglishQuizMapper.map_to_runtime(normalized)
