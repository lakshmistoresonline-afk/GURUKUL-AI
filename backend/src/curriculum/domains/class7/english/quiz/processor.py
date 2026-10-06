from .extractor import Class7EnglishQuizExtractor
from .normalizer import Class7EnglishQuizNormalizer
from .validator import Class7EnglishQuizValidator
from .mapper import Class7EnglishQuizMapper

class Class7EnglishQuizProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishQuizExtractor.extract(source_path)
        if not Class7EnglishQuizValidator.validate(raw):
            raise ValueError("Validation failed for Quiz")
        normalized = Class7EnglishQuizNormalizer.normalize(raw)
        return Class7EnglishQuizMapper.map_to_runtime(normalized)
