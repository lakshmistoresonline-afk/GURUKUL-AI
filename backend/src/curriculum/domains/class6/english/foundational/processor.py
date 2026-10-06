from .extractor import Class6EnglishFoundationalExtractor
from .normalizer import Class6EnglishFoundationalNormalizer
from .validator import Class6EnglishFoundationalValidator
from .mapper import Class6EnglishFoundationalMapper

class Class6EnglishFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishFoundationalExtractor.extract(source_path)
        if not Class6EnglishFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class6EnglishFoundationalNormalizer.normalize(raw)
        return Class6EnglishFoundationalMapper.map_to_runtime(normalized)
