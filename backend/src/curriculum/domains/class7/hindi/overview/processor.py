from .extractor import Class7HindiOverviewExtractor
from .normalizer import Class7HindiOverviewNormalizer
from .validator import Class7HindiOverviewValidator
from .mapper import Class7HindiOverviewMapper

class Class7HindiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiOverviewExtractor.extract(source_path)
        if not Class7HindiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7HindiOverviewNormalizer.normalize(raw)
        return Class7HindiOverviewMapper.map_to_runtime(normalized)
