from .extractor import Class7MathematicsiFoundationalExtractor
from .normalizer import Class7MathematicsiFoundationalNormalizer
from .validator import Class7MathematicsiFoundationalValidator
from .mapper import Class7MathematicsiFoundationalMapper

class Class7MathematicsiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiFoundationalExtractor.extract(source_path)
        if not Class7MathematicsiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7MathematicsiFoundationalNormalizer.normalize(raw)
        return Class7MathematicsiFoundationalMapper.map_to_runtime(normalized)
