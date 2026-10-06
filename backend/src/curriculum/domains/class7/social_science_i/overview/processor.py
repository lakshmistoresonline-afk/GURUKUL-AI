from .extractor import Class7SocialscienceiOverviewExtractor
from .normalizer import Class7SocialscienceiOverviewNormalizer
from .validator import Class7SocialscienceiOverviewValidator
from .mapper import Class7SocialscienceiOverviewMapper

class Class7SocialscienceiOverviewProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiOverviewExtractor.extract(source_path)
        if not Class7SocialscienceiOverviewValidator.validate(raw):
            raise ValueError("Validation failed for Overview")
        normalized = Class7SocialscienceiOverviewNormalizer.normalize(raw)
        return Class7SocialscienceiOverviewMapper.map_to_runtime(normalized)
