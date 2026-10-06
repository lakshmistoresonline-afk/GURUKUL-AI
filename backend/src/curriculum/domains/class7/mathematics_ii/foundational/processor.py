from .extractor import Class7MathematicsiiFoundationalExtractor
from .normalizer import Class7MathematicsiiFoundationalNormalizer
from .validator import Class7MathematicsiiFoundationalValidator
from .mapper import Class7MathematicsiiFoundationalMapper

class Class7MathematicsiiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiFoundationalExtractor.extract(source_path)
        if not Class7MathematicsiiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7MathematicsiiFoundationalNormalizer.normalize(raw)
        return Class7MathematicsiiFoundationalMapper.map_to_runtime(normalized)
