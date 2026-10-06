from .extractor import Class6SocialscienceMindmapsExtractor
from .normalizer import Class6SocialscienceMindmapsNormalizer
from .validator import Class6SocialscienceMindmapsValidator
from .mapper import Class6SocialscienceMindmapsMapper

class Class6SocialscienceMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceMindmapsExtractor.extract(source_path)
        if not Class6SocialscienceMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class6SocialscienceMindmapsNormalizer.normalize(raw)
        return Class6SocialscienceMindmapsMapper.map_to_runtime(normalized)
