from .extractor import Class5MathematicsMindmapsExtractor
from .normalizer import Class5MathematicsMindmapsNormalizer
from .validator import Class5MathematicsMindmapsValidator
from .mapper import Class5MathematicsMindmapsMapper

class Class5MathematicsMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsMindmapsExtractor.extract(source_path)
        if not Class5MathematicsMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class5MathematicsMindmapsNormalizer.normalize(raw)
        return Class5MathematicsMindmapsMapper.map_to_runtime(normalized)
