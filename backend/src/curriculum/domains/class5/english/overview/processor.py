from .extractor import Class5EnglishOverviewExtractor
from .normalizer import Class5EnglishOverviewNormalizer
from .validator import Class5EnglishOverviewValidator
from .mapper import Class5EnglishOverviewMapper

class Class5EnglishOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishOverviewExtractor.extract(source_path)
        if not Class5EnglishOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class5EnglishOverviewNormalizer.normalize(raw)
        return Class5EnglishOverviewMapper.map_to_runtime(normalized)
