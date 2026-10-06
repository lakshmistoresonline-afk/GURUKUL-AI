from .extractor import Class6EnglishOverviewExtractor
from .normalizer import Class6EnglishOverviewNormalizer
from .validator import Class6EnglishOverviewValidator
from .mapper import Class6EnglishOverviewMapper

class Class6EnglishOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishOverviewExtractor.extract(source_path)
        if not Class6EnglishOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class6EnglishOverviewNormalizer.normalize(raw)
        return Class6EnglishOverviewMapper.map_to_runtime(normalized)
