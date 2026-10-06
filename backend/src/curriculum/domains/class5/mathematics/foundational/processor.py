from .extractor import Class5MathematicsFoundationalExtractor
from .normalizer import Class5MathematicsFoundationalNormalizer
from .validator import Class5MathematicsFoundationalValidator
from .mapper import Class5MathematicsFoundationalMapper

class Class5MathematicsFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsFoundationalExtractor.extract(source_path)
        if not Class5MathematicsFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class5MathematicsFoundationalNormalizer.normalize(raw)
        return Class5MathematicsFoundationalMapper.map_to_runtime(normalized)
