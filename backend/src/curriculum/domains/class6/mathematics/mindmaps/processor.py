from .extractor import Class6MathematicsMindmapsExtractor
from .normalizer import Class6MathematicsMindmapsNormalizer
from .validator import Class6MathematicsMindmapsValidator
from .mapper import Class6MathematicsMindmapsMapper

class Class6MathematicsMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsMindmapsExtractor.extract(source_path)
        if not Class6MathematicsMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class6MathematicsMindmapsNormalizer.normalize(raw)
        return Class6MathematicsMindmapsMapper.map_to_runtime(normalized)
