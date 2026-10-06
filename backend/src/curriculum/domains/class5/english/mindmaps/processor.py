from .extractor import Class5EnglishMindmapsExtractor
from .normalizer import Class5EnglishMindmapsNormalizer
from .validator import Class5EnglishMindmapsValidator
from .mapper import Class5EnglishMindmapsMapper

class Class5EnglishMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishMindmapsExtractor.extract(source_path)
        if not Class5EnglishMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class5EnglishMindmapsNormalizer.normalize(raw)
        return Class5EnglishMindmapsMapper.map_to_runtime(normalized)
