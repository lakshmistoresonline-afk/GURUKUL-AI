from .extractor import Class6ScienceOverviewExtractor
from .normalizer import Class6ScienceOverviewNormalizer
from .validator import Class6ScienceOverviewValidator
from .mapper import Class6ScienceOverviewMapper

class Class6ScienceOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceOverviewExtractor.extract(source_path)
        if not Class6ScienceOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class6ScienceOverviewNormalizer.normalize(raw)
        return Class6ScienceOverviewMapper.map_to_runtime(normalized)
