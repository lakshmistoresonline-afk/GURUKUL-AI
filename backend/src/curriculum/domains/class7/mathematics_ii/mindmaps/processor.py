from .extractor import Class7MathematicsiiMindmapsExtractor
from .normalizer import Class7MathematicsiiMindmapsNormalizer
from .validator import Class7MathematicsiiMindmapsValidator
from .mapper import Class7MathematicsiiMindmapsMapper

class Class7MathematicsiiMindmapsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiMindmapsExtractor.extract(source_path)
        if not Class7MathematicsiiMindmapsValidator.validate(raw):
            raise ValueError("Validation failed for Mindmaps")
        normalized = Class7MathematicsiiMindmapsNormalizer.normalize(raw)
        return Class7MathematicsiiMindmapsMapper.map_to_runtime(normalized)
