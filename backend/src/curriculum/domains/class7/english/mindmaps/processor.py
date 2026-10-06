from .extractor import Class7EnglishMindmapsExtractor
from .normalizer import Class7EnglishMindmapsNormalizer
from .validator import Class7EnglishMindmapsValidator
from .mapper import Class7EnglishMindmapsMapper

class Class7EnglishMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishMindmapsExtractor.extract(source_path)
        if not Class7EnglishMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7EnglishMindmapsNormalizer.normalize(raw)
        return Class7EnglishMindmapsMapper.map_to_runtime(normalized)
