from .extractor import Class7EnglishOverviewExtractor
from .normalizer import Class7EnglishOverviewNormalizer
from .validator import Class7EnglishOverviewValidator
from .mapper import Class7EnglishOverviewMapper

class Class7EnglishOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishOverviewExtractor.extract(source_path)
        if not Class7EnglishOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7EnglishOverviewNormalizer.normalize(raw)
        return Class7EnglishOverviewMapper.map_to_runtime(normalized)
