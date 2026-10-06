from .extractor import Class7SocialscienceiiOverviewExtractor
from .normalizer import Class7SocialscienceiiOverviewNormalizer
from .validator import Class7SocialscienceiiOverviewValidator
from .mapper import Class7SocialscienceiiOverviewMapper

class Class7SocialscienceiiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiOverviewExtractor.extract(source_path)
        if not Class7SocialscienceiiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7SocialscienceiiOverviewNormalizer.normalize(raw)
        return Class7SocialscienceiiOverviewMapper.map_to_runtime(normalized)
