from .extractor import Class7EnglishFoundationalExtractor
from .normalizer import Class7EnglishFoundationalNormalizer
from .validator import Class7EnglishFoundationalValidator
from .mapper import Class7EnglishFoundationalMapper

class Class7EnglishFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishFoundationalExtractor.extract(source_path)
        if not Class7EnglishFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7EnglishFoundationalNormalizer.normalize(raw)
        return Class7EnglishFoundationalMapper.map_to_runtime(normalized)
