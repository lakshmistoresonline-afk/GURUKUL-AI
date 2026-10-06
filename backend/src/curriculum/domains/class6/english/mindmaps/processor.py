from .extractor import Class6EnglishMindmapsExtractor
from .normalizer import Class6EnglishMindmapsNormalizer
from .validator import Class6EnglishMindmapsValidator
from .mapper import Class6EnglishMindmapsMapper

class Class6EnglishMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishMindmapsExtractor.extract(source_path)
        if not Class6EnglishMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class6EnglishMindmapsNormalizer.normalize(raw)
        return Class6EnglishMindmapsMapper.map_to_runtime(normalized)
