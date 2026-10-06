from .extractor import Class7SocialscienceiMindmapsExtractor
from .normalizer import Class7SocialscienceiMindmapsNormalizer
from .validator import Class7SocialscienceiMindmapsValidator
from .mapper import Class7SocialscienceiMindmapsMapper

class Class7SocialscienceiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiMindmapsExtractor.extract(source_path)
        if not Class7SocialscienceiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7SocialscienceiMindmapsNormalizer.normalize(raw)
        return Class7SocialscienceiMindmapsMapper.map_to_runtime(normalized)
