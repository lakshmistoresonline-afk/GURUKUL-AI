from .extractor import Class5EnglishFoundationalExtractor
from .normalizer import Class5EnglishFoundationalNormalizer
from .validator import Class5EnglishFoundationalValidator
from .mapper import Class5EnglishFoundationalMapper

class Class5EnglishFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishFoundationalExtractor.extract(source_path)
        if not Class5EnglishFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class5EnglishFoundationalNormalizer.normalize(raw)
        return Class5EnglishFoundationalMapper.map_to_runtime(normalized)
