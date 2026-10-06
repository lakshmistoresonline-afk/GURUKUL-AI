from .extractor import Class7ScienceOverviewExtractor
from .normalizer import Class7ScienceOverviewNormalizer
from .validator import Class7ScienceOverviewValidator
from .mapper import Class7ScienceOverviewMapper

class Class7ScienceOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceOverviewExtractor.extract(source_path)
        if not Class7ScienceOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7ScienceOverviewNormalizer.normalize(raw)
        return Class7ScienceOverviewMapper.map_to_runtime(normalized)
