from .extractor import Class6HindiOverviewExtractor
from .normalizer import Class6HindiOverviewNormalizer
from .validator import Class6HindiOverviewValidator
from .mapper import Class6HindiOverviewMapper

class Class6HindiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiOverviewExtractor.extract(source_path)
        if not Class6HindiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class6HindiOverviewNormalizer.normalize(raw)
        return Class6HindiOverviewMapper.map_to_runtime(normalized)
