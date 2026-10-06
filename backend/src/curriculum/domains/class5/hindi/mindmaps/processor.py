from .extractor import Class5HindiMindmapsExtractor
from .normalizer import Class5HindiMindmapsNormalizer
from .validator import Class5HindiMindmapsValidator
from .mapper import Class5HindiMindmapsMapper

class Class5HindiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiMindmapsExtractor.extract(source_path)
        if not Class5HindiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class5HindiMindmapsNormalizer.normalize(raw)
        return Class5HindiMindmapsMapper.map_to_runtime(normalized)
