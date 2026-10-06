from .extractor import Class6HindiMindmapsExtractor
from .normalizer import Class6HindiMindmapsNormalizer
from .validator import Class6HindiMindmapsValidator
from .mapper import Class6HindiMindmapsMapper

class Class6HindiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiMindmapsExtractor.extract(source_path)
        if not Class6HindiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class6HindiMindmapsNormalizer.normalize(raw)
        return Class6HindiMindmapsMapper.map_to_runtime(normalized)
