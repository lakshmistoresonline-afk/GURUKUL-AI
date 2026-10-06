from .extractor import Class5ScienceOverviewExtractor
from .normalizer import Class5ScienceOverviewNormalizer
from .validator import Class5ScienceOverviewValidator
from .mapper import Class5ScienceOverviewMapper

class Class5ScienceOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceOverviewExtractor.extract(source_path)
        if not Class5ScienceOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class5ScienceOverviewNormalizer.normalize(raw)
        return Class5ScienceOverviewMapper.map_to_runtime(normalized)
