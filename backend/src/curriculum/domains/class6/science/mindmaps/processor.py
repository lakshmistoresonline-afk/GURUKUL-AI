from .extractor import Class6ScienceMindmapsExtractor
from .normalizer import Class6ScienceMindmapsNormalizer
from .validator import Class6ScienceMindmapsValidator
from .mapper import Class6ScienceMindmapsMapper

class Class6ScienceMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceMindmapsExtractor.extract(source_path)
        if not Class6ScienceMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class6ScienceMindmapsNormalizer.normalize(raw)
        return Class6ScienceMindmapsMapper.map_to_runtime(normalized)
