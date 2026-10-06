from .extractor import Class7HindiMindmapsExtractor
from .normalizer import Class7HindiMindmapsNormalizer
from .validator import Class7HindiMindmapsValidator
from .mapper import Class7HindiMindmapsMapper

class Class7HindiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiMindmapsExtractor.extract(source_path)
        if not Class7HindiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7HindiMindmapsNormalizer.normalize(raw)
        return Class7HindiMindmapsMapper.map_to_runtime(normalized)
