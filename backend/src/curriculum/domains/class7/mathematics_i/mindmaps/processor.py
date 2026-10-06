from .extractor import Class7MathematicsiMindmapsExtractor
from .normalizer import Class7MathematicsiMindmapsNormalizer
from .validator import Class7MathematicsiMindmapsValidator
from .mapper import Class7MathematicsiMindmapsMapper

class Class7MathematicsiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiMindmapsExtractor.extract(source_path)
        if not Class7MathematicsiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7MathematicsiMindmapsNormalizer.normalize(raw)
        return Class7MathematicsiMindmapsMapper.map_to_runtime(normalized)
