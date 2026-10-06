from .extractor import Class7ScienceMindmapsExtractor
from .normalizer import Class7ScienceMindmapsNormalizer
from .validator import Class7ScienceMindmapsValidator
from .mapper import Class7ScienceMindmapsMapper

class Class7ScienceMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceMindmapsExtractor.extract(source_path)
        if not Class7ScienceMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7ScienceMindmapsNormalizer.normalize(raw)
        return Class7ScienceMindmapsMapper.map_to_runtime(normalized)
