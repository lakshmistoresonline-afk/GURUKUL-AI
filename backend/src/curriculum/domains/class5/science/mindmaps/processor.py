from .extractor import Class5ScienceMindmapsExtractor
from .normalizer import Class5ScienceMindmapsNormalizer
from .validator import Class5ScienceMindmapsValidator
from .mapper import Class5ScienceMindmapsMapper

class Class5ScienceMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceMindmapsExtractor.extract(source_path)
        if not Class5ScienceMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class5ScienceMindmapsNormalizer.normalize(raw)
        return Class5ScienceMindmapsMapper.map_to_runtime(normalized)
