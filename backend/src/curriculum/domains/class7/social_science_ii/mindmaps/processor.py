from .extractor import Class7SocialscienceiiMindmapsExtractor
from .normalizer import Class7SocialscienceiiMindmapsNormalizer
from .validator import Class7SocialscienceiiMindmapsValidator
from .mapper import Class7SocialscienceiiMindmapsMapper

class Class7SocialscienceiiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiMindmapsExtractor.extract(source_path)
        if not Class7SocialscienceiiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7SocialscienceiiMindmapsNormalizer.normalize(raw)
        return Class7SocialscienceiiMindmapsMapper.map_to_runtime(normalized)
