from .extractor import Class5HindiOverviewExtractor
from .normalizer import Class5HindiOverviewNormalizer
from .validator import Class5HindiOverviewValidator
from .mapper import Class5HindiOverviewMapper

class Class5HindiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiOverviewExtractor.extract(source_path)
        if not Class5HindiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class5HindiOverviewNormalizer.normalize(raw)
        return Class5HindiOverviewMapper.map_to_runtime(normalized)
