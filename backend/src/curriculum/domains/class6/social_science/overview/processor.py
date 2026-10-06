from .extractor import Class6SocialscienceOverviewExtractor
from .normalizer import Class6SocialscienceOverviewNormalizer
from .validator import Class6SocialscienceOverviewValidator
from .mapper import Class6SocialscienceOverviewMapper

class Class6SocialscienceOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceOverviewExtractor.extract(source_path)
        if not Class6SocialscienceOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class6SocialscienceOverviewNormalizer.normalize(raw)
        return Class6SocialscienceOverviewMapper.map_to_runtime(normalized)
