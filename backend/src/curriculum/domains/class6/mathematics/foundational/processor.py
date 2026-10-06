from .extractor import Class6MathematicsFoundationalExtractor
from .normalizer import Class6MathematicsFoundationalNormalizer
from .validator import Class6MathematicsFoundationalValidator
from .mapper import Class6MathematicsFoundationalMapper

class Class6MathematicsFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsFoundationalExtractor.extract(source_path)
        if not Class6MathematicsFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class6MathematicsFoundationalNormalizer.normalize(raw)
        return Class6MathematicsFoundationalMapper.map_to_runtime(normalized)
